#BSD 3-Clause License
#
#Copyright (c) 2026, ASU-VDA-Lab
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met:
#
#1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
#2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
#3. Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#################################################################################

"""Recursive bisection of merged DRC clips into per-agent repair leaves.

Each clip is split until it fits both a physical extent gate and a cap on the
number of polygons in its layer band. Splitting prefers a Stoer-Wagner min-cut
of the polygon connectivity graph, falling back to a spatial median bisection
when the cut cannot shrink the clip. The resulting leaves are annotated with
their layer band, editable polygons and owned instances, merged where their
windows overlap, and renumbered into a contiguous, deterministic id sequence
stored on the context as ``ctx.leaves``.
"""


import os
from typing import Dict, List, Tuple

from .clips import _SEED_EXCLUDE_LAYERS
from .dependency_graph import Graph, build_polygon_graph
from .enforcer_p5e import enforce_bridge_ownership
from .enforcer_p5e import assign_instance_owners
from . import layer_band
from . import subcell_inclusion
from . import longstripe
from . import _invariant
from . import _relocate
from .logging_setup import get_logger, stage_extra
from .model import (instance_block_bbox_dbu, clip_bbox_dbu,
                    per_violation_bbox_dbu, is_pdn_editable_pid)
from .prompt_format import (_build_klayout_header_lines,
                            _build_klayout_snippet_body)
from .types import (BlockStats, CaseContext, Clip, Leaf, Polygon,
                    SubcellInstance, Violation)


MAX_DEPTH = 20
MAX_LEAF_SIDE_DBU = 16000  # 4um, expressed in database units
# Die-relative leaf-side gate. On a die only a few micrometres across, the
# absolute 4um gate covers practically the whole die, so an over-merged clip
# would never be split. The effective gate is therefore
# min(MAX_LEAF_SIDE_DBU, _GATE_FRAC * die_side) floored at _GATE_FLOOR_DBU.
# MAX_LEAF_SIDE_DBU itself is left alone so it stays equal to the merge extent
# cap in clips.py.
_GATE_FRAC = 0.5
_GATE_FLOOR_DBU = 4000

# How hard a crop is to repair scales with the number of top-level polygons in
# its layer band [N-3..N+3], not with its physical size. Two mechanisms keep
# every final leaf at or below _BAND_SPLIT_CAP band polygons:
#   (1) a second leaf-gate term in hrd_split_recursive, alongside the extent
#       gate that remains as the geometric backstop: a clip is a leaf only if
#       its band count is within the cap. A clip over the cap with more than
#       one violation keeps splitting; the spatial-bisect fallback halves the
#       violation set, so recursion always reaches a single violation.
#   (2) _merge_overlapping_leaves, a fixpoint that unions contained or heavily
#       overlapping crops for parallel safety but refuses any merge that would
#       push the recomputed band count over the cap. That refusal is the only
#       source of residual overlap between crops.
_BAND_SPLIT_CAP = 96
_MERGE_MAX_PASSES = 40        # fixpoint pass cap


def stage_hrd_split(ctx: CaseContext) -> None:
    log = get_logger()
    log.info("start", extra=stage_extra("S6"))
    if ctx.block_stats is None:
        raise RuntimeError("stage_hrd_split called before stage_calibrate")

    polys_by_id = ctx.geometry_model.polygons if ctx.geometry_model else {}
    insts_by_id = ctx.geometry_model.instances if ctx.geometry_model else {}
    cell_defs = ctx.geometry_model.cell_defs if ctx.geometry_model else {}
    violations_by_id = {v.violation_id: v for v in ctx.violations}

    # Effective leaf-side gate, scaled to the die (see the constants above).
    bb = ctx.geometry_model.block_bounds_dbu if ctx.geometry_model else None
    die_side = max(bb[2] - bb[0], bb[3] - bb[1]) if bb else 0
    if die_side <= 0:
        eff_gate = MAX_LEAF_SIDE_DBU
    else:
        eff_gate = max(_GATE_FLOOR_DBU,
                       min(MAX_LEAF_SIDE_DBU, int(_GATE_FRAC * die_side)))

    # Per-layer bbox index of the top-level polygons, built once: geometry is
    # immutable during split and merge, so every band count can reuse it.
    band_index = _build_band_layer_index(polys_by_id)

    leaves: List[Leaf] = []
    for clip in ctx.merged_clips:
        sub = hrd_split_recursive(
            clip, ctx.block_stats, ctx.rule_db,
            polys_by_id, violations_by_id, insts_by_id, cell_defs,
            eff_gate=eff_gate, band_index=band_index)
        leaves.extend(sub)

    _annotate_band_layers(leaves, ctx)        # editable/background + case_deck_layers
    _promote_band_editables_all(leaves, ctx)  # promote in-band polygons to editable

    # Mark cross-leaf bridge polygons. A polygon appearing in multiple
    # leaves is a "bridge"; its owner_kind is upgraded so the enforcer can
    # pick a single owning leaf.
    _mark_bridges(leaves, polys_by_id)        # now sees promoted shared polys

    # Give every bridge polygon exactly one owning leaf.
    leaves = enforce_bridge_ownership(leaves, polys_by_id)

    # Annotate per-leaf rule families, instance lists, bounds and nets, then
    # refine subcell inclusion and classify long stripes.
    _annotate_leaves(leaves, ctx)
    _demote_out_of_band(leaves, ctx)          # out-of-band bridges -> background
    insts = ctx.geometry_model.instances if ctx.geometry_model else {}
    # Exclude the PDN power vias: they are spliced into dedicated PDN leaves
    # further down, with owned_instances preset by the PDN prepass, so a regular
    # leaf must not also claim them -- otherwise a power via has two owners and
    # single ownership, which parallel repair relies on, is broken.
    assign_instance_owners(leaves, insts,
                           exclude_iids=getattr(ctx, "pdn_owned_via_iids", None) or ())
    _invariant.set_polys_for_lever(polys_by_id)   # polygon lookup for lever counting

    # A violation whose editable touchers are all PDN-owned can only be repaired
    # inside a PDN power crop, but relocate_c2_empty below indexes regular leaves
    # only and the PDN crops are spliced in after relocation, so PDN owners are
    # invisible to it. Move each such violation into its net's PDN proto-leaf
    # now, before the C2-empty pass can mis-home it into a signal leaf and grow
    # that leaf's bbox.
    leaves, _npdn, _ndrop = _relocate.relocate_pdn_owned(leaves, ctx)
    if _npdn:
        log.info("S6 pdn-relocate: moved %d PDN-owned-toucher violations into "
                 "PDN crops, dropped %d emptied leaves", _npdn, _ndrop,
                 extra=stage_extra("S6"))

    # Move each violation of a leaf that owns no usable target to the leaf that
    # does own an editable item -- a polygon or a single-owner mobile instance --
    # able to fix it, then drop the emptied leaf. Runs after
    # assign_instance_owners and reuses the ownership it computed, so single
    # ownership is preserved. Only violations, bboxes and rule families change.
    leaves, _nr, _nu, _ng = _relocate.relocate_c2_empty(leaves, ctx)
    if _nr or _nu:
        log.info("S6 relocate: moved %d C2-empty leaves, %d unrelocatable, "
                 "%d owner-bbox growths", _nr, _nu, _ng, extra=stage_extra("S6"))

    # Union crops whose bboxes are contained in, or more than half overlapped by,
    # another crop, so no two parallel repair agents edit the same physical
    # region. Runs after relocation, the last bbox-growing step, so the overlap
    # test sees the exact final leaves, and before mark_invariant_skips. It is
    # cheap in polygons (overlapping crops share band polygons) and band-capped.
    leaves, _mp, _mref, _merged_leaves = _merge_overlapping_leaves(
        leaves, ctx, band_index)
    if _merged_leaves:
        # Re-derive band layers, net map and subcell/longstripe context on the
        # grown bboxes. owned_instances and editable_polygons are carried over
        # from the union rather than recomputed, so single ownership survives.
        # Only the merged leaves change.
        _annotate_band_layers(_merged_leaves, ctx)
        _annotate_leaves(_merged_leaves, ctx)
        log.info("S6 merge: %d passes, %d band-cap refusals, %d merged leaves",
                 _mp, _mref, len(_merged_leaves), extra=stage_extra("S6"))

    # Enforce the final-leaf invariant. Runs after demotion, owner assignment
    # and relocation, so a leaf is skipped only when none of those passes could
    # give it an editable target -- a violation whose only nearby item sits on
    # V0 or another out-of-band layer. A nonzero skip count is a failure.
    _kept, _skipped = _invariant.mark_invariant_skips(leaves)
    if _skipped:
        log.warning("S6 invariant: %d/%d leaves skipped_empty_crop %s",
                    len(_skipped), len(leaves),
                    [l.leaf_id for l in _skipped][:20], extra=stage_extra("S6"))

    # Append the per-net PDN power crops after all splitting, merging,
    # relocating and invariant marking, so they are never split, merged,
    # relocated or skipped, but before the final renumber, so power and
    # non-power crops share one continuous id sequence. The splice annotates
    # their context and keeps the whole net and own-violation levers editable.
    _splice_pdn_leaves(leaves, ctx)

    # Last mutation before ctx.leaves is assembled: collapse the id gaps left by
    # merging and relocation into a continuous leaf_0001..leaf_000N, so every
    # downstream consumer sees 1..N with no dead numbers. Ids only -- geometry,
    # violations and bboxes are identical to the pre-renumber decomposition.
    leaves = _renumber_leaves_final(leaves, polys_by_id)

    ctx.leaves = {leaf.leaf_id: leaf for leaf in leaves}
    dump_crops(ctx)
    log.info("end leaves=%d", len(leaves), extra=stage_extra("S6"))


def dump_crops(ctx: CaseContext) -> None:
    """Write each leaf's KLayout crop snippet to a per-run ``crops/`` dir.

    The output directory is the first of these that resolves:
      0. ``${EVODRC_CROPS_DIR}``             (explicit override; the iterative
         leaf runner points it at ``<unit_dir>/ctx/crops`` so the crops land
         next to the other context carriers)
      1. ``${AGENT_CALLS_DIR}/../crops``     (set by the host when token
         recording is enabled)
      2. a score directory derived from ``ctx.case_info.output_path`` -- always
         persistent, because ``result/`` and ``score/`` are both host bind
         mounts with a layout the host knows:
         output_path = /workspace/result/<run_id>/<design>/<task>/<case>/<case>_repaired.py
         crops_dir   = /workspace/score/<run_id>/<design>/<task>/crops
      3. ``ctx.temp_dir/crops``               (last resort; wiped by the host
                                              at the end of the run)
    """
    log = get_logger()
    calls_dir = os.environ.get("AGENT_CALLS_DIR", "").strip()
    crops_dir = os.environ.get("EVODRC_CROPS_DIR", "").strip()   # explicit override
    if crops_dir:
        pass
    elif calls_dir:
        crops_dir = os.path.join(os.path.dirname(calls_dir), "crops")
    else:
        # Derive the score directory from output_path; it persists in the
        # host-mounted ``score/`` tree even without token recording enabled.
        ci = getattr(ctx, "case_info", None)
        out_path = getattr(ci, "output_path", "") if ci else ""
        if out_path and "/result/" in out_path:
            # /workspace/result/<run_id>/<design>/<task>/<case>/<file>.py
            #   dirname  -> .../<case>
            #   dirname  -> .../<task>
            #   replace  -> /workspace/score/<run_id>/<design>/<task>
            score_root = os.path.dirname(os.path.dirname(out_path))
            score_root = score_root.replace("/result/", "/score/", 1)
            crops_dir = os.path.join(score_root, "crops")
        elif getattr(ctx, "temp_dir", ""):
            # Last resort: the volatile temp dir.
            crops_dir = os.path.join(ctx.temp_dir, "crops")
    if not crops_dir:
        log.warning("dump_crops: no output directory resolvable; skipping",
                    extra=stage_extra("S6"))
        return
    try:
        os.makedirs(crops_dir)
    except OSError:
        if not os.path.isdir(crops_dir):
            log.warning("dump_crops: cannot create %s; skipping",
                        crops_dir, extra=stage_extra("S6"))
            return
    case_info = getattr(ctx, "case_info", None)
    case_name = getattr(case_info, "case_name", "") if case_info else ""
    n = 0
    for leaf in ctx.leaves.values():
        header = _build_klayout_header_lines(leaf, ctx)
        body = _build_klayout_snippet_body(leaf, ctx)
        lines = [
            "# Crop snippet for inspection -- leaf_id={0}".format(leaf.leaf_id),
            "# Case: {0}  Wave: (TBD)  Generated by S6 dump_crops".format(
                case_name or "unknown"),
            "# ----",
        ]
        lines.extend(header)
        lines.append("")
        lines.append("```python")
        lines.extend(body)
        lines.append("```")
        out_path = os.path.join(crops_dir, "{0}.py".format(leaf.leaf_id))
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
        n += 1
    log.info("dumped %d crop snippets to %s", n, crops_dir,
             extra=stage_extra("S6"))


def hrd_split_recursive(clip: Clip, block_stats: BlockStats, rule_db,
                        polys_by_id: Dict[str, Polygon],
                        violations_by_id: Dict[str, Violation],
                        insts_by_id=None,
                        cell_defs=None,
                        eff_gate=MAX_LEAF_SIDE_DBU,
                        band_index=None) -> List[Leaf]:
    """Recursively bisect a clip until it passes the size and band gates.

    Bridge ownership is left to stage_hrd_split, which resolves it once the
    recursion has finished and the bridge owners exist.
    """
    if insts_by_id is None:
        insts_by_id = {}
    if cell_defs is None:
        cell_defs = {}
    g = build_polygon_graph(clip, polys_by_id, violations_by_id)
    bbox = clip_bbox_dbu(clip.violation_ids, violations_by_id,
                         polys_by_id, insts_by_id, cell_defs)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    # A clip is a final leaf only if it both fits the extent gate and keeps its
    # band-polygon count within the cap. A band_index of None makes the band
    # term 0, leaving an extent-only gate. The layer set used here has to match
    # the final leaf's band (editable layers unioned with background layers
    # after longstripe widening): longstripe widens editable_layers to the layer
    # of every editable polygon the clip carries, so those layers are folded in
    # here -- otherwise a rule-band-only count under-counts and lets a
    # polygon-dense leaf through.
    band_layers = _clip_band_layers(clip.violation_ids, violations_by_id)
    if band_index is not None:
        for pid in clip.polygon_ids:
            p = polys_by_id.get(pid)
            if p is not None and p.owner_kind == "editable":
                band_layers.add(p.layer_name)
    band_ok = _band_count(bbox, band_layers, band_index) <= _BAND_SPLIT_CAP
    if w <= eff_gate and h <= eff_gate and band_ok:
        return [_leaf_from_clip(clip, polys_by_id,
                                len(_global_leaf_counter()),
                                violations_by_id, insts_by_id, cell_defs)]

    # Still oversized. Every final leaf must fit the gate on both edges. A
    # single violation's bbox is at most 8000 dbu on both axes by construction
    # (model._clamp_long_axis), so once the clip is down to one violation it
    # cannot be oversized. If it somehow is, the recursion still terminates
    # here rather than spinning, because one violation cannot be split further.
    if len(clip.violation_ids) <= 1 or clip.depth >= MAX_DEPTH:
        leaf = _leaf_from_clip(clip, polys_by_id,
                               len(_global_leaf_counter()),
                               violations_by_id, insts_by_id, cell_defs)
        if clip.depth >= MAX_DEPTH:
            leaf.warn_depth_exceeded = True
        return [leaf]

    # More than one violation and still oversized, so the clip must be split.
    # The preferred route is the connectivity min-cut plus the round-robin
    # _split_clip: it keeps electrically related geometry together and shares
    # the violations evenly between the two sides. It counts as progress only
    # when both sides are non-empty and strictly smaller than the parent.
    #
    # Violations sharing one long stripe polygon form a single graph component
    # that min-cut cannot cleave, or from which it only peels a single node, so
    # the round-robin split can leave two far-apart violations in the same half
    # and the union bbox stays huge. When the connectivity split makes no
    # progress, fall back to a purely spatial median bisection of the violation
    # set along its longest axis: that always halves the violation count, so
    # the recursion is guaranteed to reach a single violation.
    clip_a = clip_b = None
    if len(g.nodes) >= 2:
        g_a, g_b = min_cut_bisect(g)
        ca, cb = _split_clip(clip, g_a.nodes, g_b.nodes,
                             violations_by_id, polys_by_id,
                             insts_by_id, cell_defs)
        n = len(clip.violation_ids)
        if (ca.violation_ids and cb.violation_ids
                and len(ca.violation_ids) < n and len(cb.violation_ids) < n):
            clip_a, clip_b = ca, cb
    if clip_a is None:
        clip_a, clip_b = _spatial_bisect_clip(
            clip, violations_by_id, polys_by_id, insts_by_id, cell_defs)
    return (hrd_split_recursive(clip_a, block_stats, rule_db,
                                polys_by_id, violations_by_id,
                                insts_by_id, cell_defs, eff_gate=eff_gate,
                                band_index=band_index)
            + hrd_split_recursive(clip_b, block_stats, rule_db,
                                  polys_by_id, violations_by_id,
                                  insts_by_id, cell_defs, eff_gate=eff_gate,
                                  band_index=band_index))


# ---------------------------------------------------------------------------
# Stoer-Wagner min-cut bisection
# ---------------------------------------------------------------------------

def min_cut_bisect(g: Graph) -> Tuple[Graph, Graph]:
    """Return two disjoint subgraphs that together cover `g`, partitioned by a
    Stoer-Wagner min-cut."""
    if len(g.nodes) <= 1:
        return _subgraph(g, set(g.nodes)), _subgraph(g, set())
    try:
        import networkx as nx
        from networkx.algorithms.connectivity.stoerwagner import stoer_wagner
        nxg = nx.Graph()
        for n in g.nodes:
            nxg.add_node(n)
        for u, neigh in g.adj.items():
            for v in neigh:
                if u < v:
                    nxg.add_edge(u, v, weight=1)
        if nxg.number_of_edges() == 0:
            return _split_disconnected(g)
        _cut_weight, partition = stoer_wagner(nxg)
        set_a, set_b = partition
        return _subgraph(g, set(set_a)), _subgraph(g, set(set_b))
    except Exception:
        # When networkx is unavailable or stoer_wagner raises, split the graph
        # in half by node id so the pipeline keeps making progress.
        return _split_disconnected(g)


def _split_disconnected(g: Graph) -> Tuple[Graph, Graph]:
    """Split the graph into two halves by sorted node id."""
    nodes = sorted(g.nodes)
    mid = len(nodes) // 2
    return _subgraph(g, set(nodes[:mid])), _subgraph(g, set(nodes[mid:]))


def _subgraph(g: Graph, keep: set) -> Graph:
    sub = Graph()
    for pid in keep:
        poly = g.polygons_by_id.get(pid)
        if poly is not None:
            sub.add_node(poly)
    for u in keep:
        for v in g.adj.get(u, ()):
            if v in keep and u < v:
                sub.add_edge(u, v)
    sub.violations = [v for v in g.violations
                      if any(pid in keep for pid in v.involves)]
    return sub


# ---------------------------------------------------------------------------
# Leaf construction helpers
# ---------------------------------------------------------------------------

_LEAF_COUNTER = [0]


def _global_leaf_counter() -> list:
    """Return the leaf counter as a mutable list, so callers can read the count
    without touching module-private state."""
    return _LEAF_COUNTER


def _leaf_from_clip(clip: Clip, polys_by_id: Dict[str, Polygon],
                    sequence: int, violations_by_id=None,
                    insts_by_id=None, cell_defs=None) -> Leaf:
    _LEAF_COUNTER[0] += 1
    leaf_id = "leaf_{0:04d}".format(_LEAF_COUNTER[0])
    # Editable polygons are the ones whose owner_kind is "editable". Everything
    # else, subcell geometry included, is demoted to read-only context so it
    # cannot be targeted by polygon ops.
    editable: List[str] = []
    context: List[str] = []
    for pid in clip.polygon_ids:
        poly = polys_by_id.get(pid)
        if poly is None:
            continue
        # A PDN power-net polygon is editable only in its own power crop; in
        # any other leaf it is view-only context.
        if poly.owner_kind == "editable" and not is_pdn_editable_pid(pid):
            editable.append(pid)
        else:
            context.append(pid)
    # Same bbox helper the size gate and the crop header use.
    if violations_by_id is None:
        bbox = _compute_bbox(clip.polygon_ids, polys_by_id)
    else:
        bbox = clip_bbox_dbu(clip.violation_ids, violations_by_id,
                             polys_by_id, insts_by_id or {}, cell_defs or {})
    return Leaf(
        leaf_id=leaf_id,
        editable_polygons=editable,
        bridge_polygons=[],
        subcell_instances=[],
        violations=list(clip.violation_ids),
        block_bounds_dbu=(0, 0, 0, 0),
        bbox_dbu=bbox,
        depth=clip.depth,
        context_readonly=context,
    )


def _renumber_leaves_final(leaves, polys_by_id):
    """Reassign every surviving leaf a contiguous, deterministic id.

    Splitting, merging and relocation leave gaps in the leaf ids, because
    ``_merge_overlapping_leaves`` keeps ``members[0]``'s id and drops the folded
    away leaves while ``_relocate.relocate_c2_empty`` drops emptied ones. The
    survivors are renumbered leaf_0001..leaf_000N under a stable total order, so
    the same input always yields the same numbering and every downstream
    consumer -- the returned list, ctx.leaves keys, dump_crops file names, the
    scheduler waves -- sees the same gap-free ids.

    The ordering key is the leaf bbox (y_min, x_min, y_max, x_max) then its
    smallest violation id. Violations are partitioned one-to-one across leaves,
    so that tiebreaker is unique and the key is a strict total order even when
    two bboxes match. The result is stable across dict and set iteration orders.

    The PDN power-net crops are forced to the last two ids: non-PDN leaves take
    1..N-2 in key order, then the smaller-key PDN crop takes N-1 and is labelled
    "VDD" and the last takes N and is labelled "VSS" on ``leaf.pdn_rail``. That
    labelling is geometric, not electrical -- no net names are available here.

    Geometry, violations and bboxes are unchanged; only the id string and the
    two rail labels are rewritten. ``polygon.bridge_owner_leaf_id`` pointers to
    a surviving leaf are remapped to the new id, while pointers to leaves that
    were already merged away are left alone -- they were stale before the
    renumber too, and are only null-checked or displayed, never id-matched.
    Returns the leaves re-sorted into the new id order, leaf_0001 first."""
    def _key(L):
        bb = L.bbox_dbu or (0, 0, 0, 0)
        vids = sorted(L.violations)
        return (bb[1], bb[0], bb[3], bb[2], vids[0] if vids else "")
    # Both partitions are sorted by the same key, so the same set of leaves
    # yields the same order whichever order they arrive in.
    non_pdn = sorted((L for L in leaves if not getattr(L, "is_pdn", False)),
                     key=_key)
    pdn = sorted((L for L in leaves if getattr(L, "is_pdn", False)), key=_key)
    ordered = non_pdn + pdn                       # PDN power-net crops go last
    id_map = {}                                  # old leaf_id -> new leaf_id
    for i, L in enumerate(ordered, start=1):
        new_id = "leaf_{0:04d}".format(i)
        id_map[L.leaf_id] = new_id
        L.leaf_id = new_id
    # Rail-label the trailing PDN crops: the smaller key (id N-1) becomes "VDD"
    # and the very last id (N) becomes "VSS". pdn is sorted by the same key, so
    # pdn[-2] is VDD and pdn[-1] is VSS. Any earlier PDN crop, which only occurs
    # if a block ever carries more than two, is left unlabelled.
    for off in range(len(pdn)):
        if off == len(pdn) - 1:
            pdn[off].pdn_rail = "VSS"
        elif off == len(pdn) - 2:
            pdn[off].pdn_rail = "VDD"
        else:
            pdn[off].pdn_rail = ""
    for p in (polys_by_id or {}).values():
        old = getattr(p, "bridge_owner_leaf_id", None)
        if old is not None and old in id_map:
            p.bridge_owner_leaf_id = id_map[old]
    return ordered


def _splice_pdn_leaves(leaves: List[Leaf], ctx: CaseContext) -> None:
    """Annotate the PDN power crops with the same neighbourhood context the
    other leaves get -- subcell instances, read-only neighbours, net map --
    then restore the traced net as their editable set and append them to
    ``leaves`` in place.

    The editability contract is restored after annotation: editable_polygons is
    exactly the traced net polygon ids and editable_layers is the net's actual
    layers, so the validator's band gate admits edits on every strap layer. A
    net polygon that an annotator parked in a context channel is removed from
    that channel; a non-net polygon stays as view-only context.
    """
    pdn_leaves = list(getattr(ctx, "pdn_leaves", []) or [])
    if not pdn_leaves:
        return
    # Snapshot the editability contract before the shared annotators run.
    saved = {id(L): (list(L.editable_polygons), tuple(L.editable_layers))
             for L in pdn_leaves}
    _annotate_band_layers(pdn_leaves, ctx)    # context only (editable restored)
    _annotate_leaves(pdn_leaves, ctx)         # subcell/ro/net map; no promotion
    # The scheduler treats any shared editable polygon involving power as a hard
    # parallel-safety fault, so the promotion below takes only polygons that no
    # other leaf holds as editable -- a signal leaf, or the sibling PDN crop
    # processed in ctx.pdn_leaves order. Promotions are registered here so the
    # second rail cannot claim a polygon the first already took.
    taken = set()
    for other in leaves:
        taken.update(other.editable_polygons)
    for other in pdn_leaves:
        taken.update(saved[id(other)][0])
    for L in pdn_leaves:
        net_pids, net_layers = saved[id(L)]
        net_set = set(net_pids)
        L.editable_polygons = list(net_pids)
        L.editable_layers = net_layers
        # Keep net polygons out of every view-only channel; they are editable.
        L.context_readonly = [p for p in L.context_readonly if p not in net_set]
        L.ro_neighbor_ids = [p for p in L.ro_neighbor_ids if p not in net_set]
        L.band_background = [p for p in L.band_background if p not in net_set]
        L.bridge_polygons = [p for p in L.bridge_polygons if p not in net_set]
        L.is_pdn = True
        # Expose the restore snapshot as a plain attribute rather than a
        # dataclass field, so leaves.json and the scheduler and validator field
        # enumerations pass over it.
        L.pdn_net_pids = tuple(net_pids)
        _pdn_own_violation_levers(L, ctx, net_set, taken)
    leaves.extend(pdn_leaves)


# Die-span guard threshold. A polygon spanning at least this fraction of the
# die on either axis is die-spanning: only its whole-edge `resize` is pooled and
# measured block-wide by the harness, so a move or delete on it would be an
# unpooled, block-wide edit standing behind the connectivity-only unit gate
# alone. The harness keeps an equal constant (cu_drc.DIE_SPAN_FRAC); this
# package cannot import the harness, so the two are kept in sync by hand.
_DIE_SPAN_FRAC = 0.6


def _pdn_own_violation_levers(L, ctx, net_set, taken):
    """Grant a PDN crop editability over the lever objects that take part in its
    own violations.

    A PDN crop renders only its own net, so an in-window object participating in
    one of the crop's violation clusters would otherwise be frozen or not drawn
    at all. The windows are the raw per-violation bboxes rather than dilated
    ones: an object intersecting the raw bbox physically contains part of the
    violated geometry, whereas dilating the window pulls in bystanders and
    inflates the prompt for no gain.

    Polygon guards, in order: the owner_kind freeze is never overridden; die
    boundary layers are excluded; polygons already editable in this leaf are
    skipped; a polygon editable in any other leaf is skipped, and each promotion
    is registered so the sibling rail cannot claim it; a PDN polygon belonging
    to the sibling rail is never promoted, including its die-spanning straps;
    the polygon must intersect an own-violation window and must be a real lever.
    A polygon whose whole bbox is in-window and which spans less than
    _DIE_SPAN_FRAC of the die becomes fully editable; anything else, every
    die-spanning polygon included, is editable only through an in-window or
    on-edge open end, whose whole-edge resize stays reachable through the pool.

    Via instances: an in-window mobile via not already owned by this leaf
    becomes owned, so crop_body renders it with move handles. That deliberately
    double-owns the via across the PDN leaf and the signal leaf; assemble
    deduplicates identical instance edits and drops all of them when they
    conflict, and via-def structure ops route through the pool whichever leaf
    proposed them. Power vias belonging to another rail are excluded.
    """
    geom = ctx.geometry_model
    if geom is None:
        return
    viol_by_id = {v.violation_id: v for v in (ctx.violations or [])}
    windows = []
    for vid in L.violations:
        v = viol_by_id.get(vid)
        if v is not None:
            windows.append(v.bbox_dbu)     # raw bbox, not dilated
    if not windows:
        return
    lx1, ly1, lx2, ly2 = L.bbox_dbu
    bb_die = L.block_bounds_dbu or geom.block_bounds_dbu
    die_w = max(1, bb_die[2] - bb_die[0])
    die_h = max(1, bb_die[3] - bb_die[1])
    from .crop_body import poly_is_real_lever          # local: no import cycle
    for pid in sorted(geom.polygons.keys()):
        poly = geom.polygons[pid]
        if poly.owner_kind != "editable":              # frozen stays frozen
            continue
        if poly.layer_name in _SEED_EXCLUDE_LAYERS:    # die boundary
            continue
        if pid in L.editable_polygons:                 # own net polygons
            continue
        if pid in taken:                               # editable in another leaf
            continue
        if is_pdn_editable_pid(pid) and pid not in net_set:
            continue                                   # sibling rail
        bb = poly.bbox_dbu
        if not any(_invariant.bbox_intersect(bb, w) for w in windows):
            continue                                   # no own-violation window
        if not poly_is_real_lever(poly, L.bbox_dbu):   # not a usable lever
            continue
        bx1, by1, bx2, by2 = bb
        span = max((bx2 - bx1) / float(die_w), (by2 - by1) / float(die_h))
        fully_inside = (bx1 >= lx1 and by1 >= ly1
                        and bx2 <= lx2 and by2 <= ly2)
        if fully_inside and span < _DIE_SPAN_FRAC:
            # Fully editable: whole bbox in-window and not die-spanning.
            L.editable_polygons.append(pid)
            taken.add(pid)
            L.long_open_ends.pop(pid, None)
        else:
            # Otherwise editable only through an in-window or on-edge open end.
            # Die-spanning polygons always land here.
            w = bx2 - bx1
            h = by2 - by1
            axis = "x" if w >= h else "y"
            if axis == "x":
                open_low = bx1 >= lx1
                open_high = bx2 <= lx2
            else:
                open_low = by1 >= ly1
                open_high = by2 <= ly2
            if not (open_low or open_high):
                continue
            L.editable_polygons.append(pid)
            taken.add(pid)
            L.long_open_ends[pid] = {"axis": axis, "open_low": open_low,
                                     "open_high": open_high}
        L.editable_layers = tuple(sorted(set(L.editable_layers)
                                         | {poly.layer_name}))
        L.context_readonly = [q for q in L.context_readonly if q != pid]
        L.ro_neighbor_ids = [q for q in L.ro_neighbor_ids if q != pid]
        L.band_background = [q for q in L.band_background if q != pid]
    # Via instances, reusing the same rotation-correct instance bbox helper as
    # _annotate_leaves. subcell_inclusion.refine has already narrowed
    # L.subcell_instances to owned vias, so candidates are re-derived from the
    # instance table; a promoted via is put back into subcell_instances so
    # crop_body renders it with move handles.
    inst_by_id = geom.instances
    cell_defs = geom.cell_defs
    pdn_via_union = set(getattr(ctx, "pdn_owned_via_iids", None) or ())
    owned = set(L.owned_instances or ())
    new_owned = []
    for iid in sorted(inst_by_id.keys()):
        if iid in owned:
            continue
        inst = inst_by_id[iid]
        if getattr(inst, "kind", "") != "via":
            continue
        if not inst.allowed_ops:
            continue
        if iid in pdn_via_union:
            # Own-net power vias are already in owned_instances and were
            # skipped above, so any prepass power via reaching this point
            # belongs to another rail and stays with that rail's crop.
            continue
        ibb = instance_block_bbox_dbu(inst, cell_defs)
        if any(_invariant.bbox_intersect(ibb, w) for w in windows):
            new_owned.append(iid)
    if new_owned:
        L.owned_instances = tuple(list(L.owned_instances) + new_owned)
        for iid in new_owned:
            if iid not in L.subcell_instances:
                L.subcell_instances.append(iid)


def _spatial_bisect_clip(clip, violations_by_id, polys_by_id,
                         insts_by_id, cell_defs):
    # type: (Clip, dict, dict, dict, dict) -> Tuple[Clip, Clip]
    """Geometry-guaranteed bisection, used when the connectivity min-cut and
    round-robin split cannot shrink an oversized clip -- for example when
    several violations share one long stripe polygon.

    The clip's violations are split into two even halves by the median of their
    per-violation bbox centre on the clip's longer axis. A polygon is kept on a
    side if its bbox touches at least one violation bbox on that side, so a
    shared stripe is kept on both sides and rendering later clips it to each
    side's own bbox. Halving the violation count guarantees progress, so the
    recursion always reaches a single violation.
    """
    vids = list(clip.violation_ids)
    bb = clip_bbox_dbu(clip.violation_ids, violations_by_id,
                       polys_by_id, insts_by_id, cell_defs)
    axis = 0 if (bb[2] - bb[0]) >= (bb[3] - bb[1]) else 1  # 0=x, 1=y

    def _center(vid):
        v = violations_by_id.get(vid)
        if v is None:
            return 0
        pb = per_violation_bbox_dbu(v, polys_by_id, insts_by_id, cell_defs)
        return (pb[0] + pb[2]) // 2 if axis == 0 else (pb[1] + pb[3]) // 2

    vids.sort(key=_center)
    mid = len(vids) // 2
    if mid == 0:                       # defensive: never let one side be empty
        mid = 1
    a_vids = set(vids[:mid])
    b_vids = set(vids[mid:])

    def _vbbox(vid):
        v = violations_by_id.get(vid)
        if v is None:
            return None
        return per_violation_bbox_dbu(v, polys_by_id, insts_by_id, cell_defs)

    a_boxes = [b for b in (_vbbox(v) for v in a_vids) if b is not None]
    b_boxes = [b for b in (_vbbox(v) for v in b_vids) if b is not None]

    def _touches_any(poly, boxes):
        if poly is None:
            return False
        pb = poly.bbox_dbu
        for q in boxes:
            if (pb[0] <= q[2] and q[0] <= pb[2]
                    and pb[1] <= q[3] and q[1] <= pb[3]):
                return True
        return False

    pa, pb_ = [], []
    for pid in clip.polygon_ids:
        poly = polys_by_id.get(pid)
        in_a = _touches_any(poly, a_boxes)
        in_b = _touches_any(poly, b_boxes)
        if in_a or not in_b:           # unmatched polygons default to side A
            pa.append(pid)
        if in_b:
            pb_.append(pid)

    return (
        Clip(clip_id=clip.clip_id + "sa",
             violation_ids=tuple(v for v in vids if v in a_vids),
             polygon_ids=tuple(pa),
             depth=clip.depth + 1),
        Clip(clip_id=clip.clip_id + "sb",
             violation_ids=tuple(v for v in vids if v in b_vids),
             polygon_ids=tuple(pb_),
             depth=clip.depth + 1),
    )


def _split_clip(clip: Clip, set_a: set, set_b: set,
                violations_by_id=None, polys_by_id=None,
                insts_by_id=None, cell_defs=None) -> Tuple[Clip, Clip]:
    pa = tuple(p for p in clip.polygon_ids if p in set_a)
    pb = tuple(p for p in clip.polygon_ids if p in set_b)
    # Send each violation to the side whose polygons spatially overlap the
    # violation's bbox, so a violation stays in the same clip -- and therefore
    # the same leaf -- as the editable polygon it sits on. `involves` is
    # normally empty, so the association is spatial, using the same test as
    # _spatial_bisect_clip._touches_any. A tie, or no overlap on either side,
    # falls back to round-robin, which keeps the two sides balanced.
    via, vib = [], []
    polys = polys_by_id or {}

    def _side_overlap(vid, side_pids):
        v = (violations_by_id or {}).get(vid)
        if v is None:
            return False
        vb = per_violation_bbox_dbu(v, polys, insts_by_id or {}, cell_defs or {})
        for pid in side_pids:
            poly = polys.get(pid)
            if poly is None:
                continue
            q = poly.bbox_dbu
            if (vb[0] <= q[2] and q[0] <= vb[2]
                    and vb[1] <= q[3] and q[1] <= vb[3]):
                return True
        return False

    for vid in clip.violation_ids:
        in_a = _side_overlap(vid, pa)
        in_b = _side_overlap(vid, pb)
        if in_a and not in_b:
            via.append(vid)
        elif in_b and not in_a:
            vib.append(vid)
        else:
            # Both sides (a shared stripe) or neither (no geometry): round-robin
            # keeps the two sides balanced, which the recursion's progress check
            # depends on.
            (via if len(via) <= len(vib) else vib).append(vid)
    return (
        Clip(clip_id=clip.clip_id + "a",
             violation_ids=tuple(via),
             polygon_ids=pa,
             depth=clip.depth + 1),
        Clip(clip_id=clip.clip_id + "b",
             violation_ids=tuple(vib),
             polygon_ids=pb,
             depth=clip.depth + 1),
    )


def _compute_bbox(polygon_ids, polys_by_id) -> Tuple[int, int, int, int]:
    xs1, ys1, xs2, ys2 = [], [], [], []
    for pid in polygon_ids:
        poly = polys_by_id.get(pid)
        if poly is None:
            continue
        xs1.append(poly.bbox_dbu[0])
        ys1.append(poly.bbox_dbu[1])
        xs2.append(poly.bbox_dbu[2])
        ys2.append(poly.bbox_dbu[3])
    if not xs1:
        return (0, 0, 0, 0)
    return (min(xs1), min(ys1), max(xs2), max(ys2))


def _mark_bridges(leaves: List[Leaf],
                  polys_by_id: Dict[str, Polygon]) -> None:
    """Polygons appearing in multiple leaves are bridges."""
    counts: Dict[str, int] = {}
    for leaf in leaves:
        for pid in (list(leaf.editable_polygons)
                    + list(leaf.bridge_polygons)
                    + list(leaf.context_readonly)):
            counts[pid] = counts.get(pid, 0) + 1
    for pid, count in counts.items():
        poly = polys_by_id.get(pid)
        if poly is None:
            continue
        if count > 1 and poly.owner_kind == "editable":
            poly.owner_kind = "bridge"


def _annotate_leaves(leaves: List[Leaf], ctx: CaseContext) -> None:
    """Populate rule_families, subcell_instances, block_bounds, the net map, the
    read-only top-level neighbour channel and the cap-exempt seed set.

    Membership is computed from the leaf's focus window -- its own ``bbox_dbu``,
    with the seed set additionally keyed on the raw per-violation bboxes --
    intersected against each instance's rotation-correct world bbox.
    ``_mark_bridges`` has already run, so a candidate neighbour polygon with
    ``owner_kind == 'bridge'`` is editable elsewhere and is left to the bridge
    path, while a plain ``owner_kind == 'editable'`` neighbour that is neither
    in this leaf nor shared becomes a comment-only ``# ro`` entry. Editable-
    elsewhere geometry therefore stays visible as a potential conflict, while
    plain neighbours appear as inert context.
    """
    geom = ctx.geometry_model
    if geom is None:
        return
    block_bounds = geom.block_bounds_dbu
    viol_by_id = {v.violation_id: v for v in ctx.violations}
    inst_by_id = geom.instances
    cell_defs = geom.cell_defs

    # Precompute each instance's rotation-correct world bbox once.
    inst_bbox: Dict[str, Tuple[int, int, int, int]] = {
        iid: instance_block_bbox_dbu(inst, cell_defs)
        for iid, inst in inst_by_id.items()}

    for leaf in leaves:
        leaf.block_bounds_dbu = block_bounds
        # rule families of this leaf's violations
        fams = set()
        viols = []
        for vid in leaf.violations:
            v = viol_by_id.get(vid)
            if v is not None:
                fams.add(v.rule_family or "other")
                viols.append(v)
        leaf.rule_families = tuple(sorted(fams))

        # The leaf's own sizing bbox is the focus window; subcell and `# ro`
        # membership both key on this single bbox.
        windows = [leaf.bbox_dbu]

        # (1) Seed: the instance world bbox intersects a raw violation bbox --
        #     the via or std cell physically containing the violated geometry.
        #     This set is exempt from the instance cap.
        # (2) Pull: the instance world bbox intersects the focus window --
        #     neighbouring std cells and connecting vias.
        seen: List[str] = []
        seed_iids: List[str] = []
        for iid in sorted(inst_bbox.keys()):
            bb = inst_bbox[iid]
            hit_raw = any(_bbox_intersect(bb, v.bbox_dbu) for v in viols)
            hit_win = any(_bbox_intersect(bb, w) for w in windows)
            if hit_raw or hit_win:
                if iid not in seen:
                    seen.append(iid)
                if hit_raw and iid not in seed_iids:
                    seed_iids.append(iid)
        leaf.subcell_instances = seen
        leaf.seed_instance_ids = seed_iids

        # (3) `# ro` neighbours: top-level polygons inside the window that are
        #     plain neighbours -- owner_kind 'editable', not in this leaf and
        #     not on the die boundary. 'bridge' polygons are editable elsewhere
        #     and are left to the bridge path so the conflict stays visible.
        leaf_polyset = (set(leaf.editable_polygons)
                        | set(leaf.bridge_polygons)
                        | set(leaf.context_readonly))
        ro: List[str] = []
        for pid in sorted(geom.polygons.keys()):
            poly = geom.polygons[pid]
            if poly.layer_name in _SEED_EXCLUDE_LAYERS:
                continue
            if pid in leaf_polyset:
                continue
            if poly.owner_kind != "editable":
                continue
            if any(_bbox_intersect(poly.bbox_dbu, w) for w in windows):
                ro.append(pid)
        leaf.ro_neighbor_ids = ro

        # net_to_polygons, best effort: cluster by bbox touch within the leaf.
        leaf.net_to_polygons = _derive_net_map(leaf, geom.polygons)

        # Std-cell pin narrowing plus one hop of background, then long-stripe
        # classification (open-end flags and pass-through demotion).
        subcell_inclusion.refine(leaf, ctx)
        longstripe.classify(leaf, ctx)


# ---------------------------------------------------------------------------
# Layer band passes: editable/background layers, promotion, demotion.
# ---------------------------------------------------------------------------

def _annotate_band_layers(leaves: List[Leaf], ctx: CaseContext) -> None:
    """Set each leaf's editable_layers and background_layers from the union of
    its violations' rule layers, and stamp case_deck_layers with the raw union
    including V0, which the std-cell keep-set and the trimmed rule deck both
    read. It rewrites only these three leaf fields, so it is safe to re-run."""
    viol_by_id = {v.violation_id: v for v in ctx.violations}
    for leaf in leaves:
        ed, bg = layer_band.band_for_leaf(leaf, viol_by_id)
        leaf.editable_layers = ed
        leaf.background_layers = bg
        nset_with_v0 = set()
        for vid in leaf.violations:
            vv = viol_by_id.get(vid)
            if vv is not None:
                for lyr in layer_band.layers_of_rule(vv.rule_id):
                    nset_with_v0.add(lyr)
        leaf.case_deck_layers = tuple(sorted(nset_with_v0))


def _promote_band_editables_all(leaves: List[Leaf], ctx: CaseContext) -> None:
    """Append to each leaf's editable_polygons any top-level polygon that is on
    an editable band layer, falls inside the leaf's focus region, and is itself
    unfrozen (owner_kind 'editable').

    The per-polygon freeze is absolute: std-cell, V0 and frozen-subcell polygons
    are never promoted. Runs before _mark_bridges, so a promoted polygon that
    ends up shared between leaves still becomes a bridge and gets an owner.
    """
    geom = ctx.geometry_model
    if geom is None:
        return
    polys = geom.polygons
    viol_by_id = {v.violation_id: v for v in ctx.violations}
    for leaf in leaves:
        editable_layer_set = set(leaf.editable_layers)
        if not editable_layer_set:
            continue
        # The leaf bbox is clamped tight, so an in-band editable polygon can sit
        # just outside it; the per-violation dilated windows keep the
        # violation's own editable target reachable. The leaf window and the
        # per-violation windows are kept as separate lists: the band-constrained
        # rule uses both, while the own-violation path uses w_viol alone with no
        # band constraint, so a neighbour inside a violation window becomes a
        # lever even when its layer is out of band.
        w_leaf = [leaf.bbox_dbu]
        viol_by_id = {v.violation_id: v for v in ctx.violations}
        w_viol = []
        for vid in leaf.violations:
            vv = viol_by_id.get(vid)
            if vv is not None:
                w_viol.append(_invariant.expand(vv.bbox_dbu,
                                                _invariant.SPATIAL_MARGIN_DBU))
        existing = (set(leaf.editable_polygons) | set(leaf.bridge_polygons)
                    | set(leaf.context_readonly))
        for pid in sorted(polys.keys()):
            if pid in existing:
                continue
            poly = polys[pid]
            if poly.layer_name in _SEED_EXCLUDE_LAYERS:
                continue
            if poly.owner_kind != "editable":          # frozen stays frozen
                continue
            if is_pdn_editable_pid(pid):               # never promote a PDN
                continue                               # polygon into a non-power leaf
            bb = poly.bbox_dbu
            # Path 1: in band and intersecting either the leaf window or any
            # per-violation window. Path 2: intersecting a per-violation window,
            # with no band constraint. The guards above and the real-lever guard
            # below apply to both paths.
            hit_viol = any(_bbox_intersect(bb, w) for w in w_viol)
            band_hit = (poly.layer_name in editable_layer_set
                        and (hit_viol
                             or any(_bbox_intersect(bb, w) for w in w_leaf)))
            if not (band_hit or hit_viol):
                continue
            # The dilated per-violation window can admit an in-band polygon
            # whose body lies outside leaf.bbox_dbu, such as a full-width stripe.
            # Such a polygon clips to zero area in crop_body, so promotion is
            # limited to polygons whose clip into the leaf bbox has positive
            # area -- the ones that stay usable levers in the rendered crop.
            from .crop_body import poly_is_real_lever
            if not poly_is_real_lever(poly, leaf.bbox_dbu):
                continue
            leaf.editable_polygons.append(pid)
            existing.add(pid)


def _demote_out_of_band(leaves: List[Leaf], ctx: CaseContext) -> None:
    """Move out-of-band bridge polygons into band_background.

    Top-level editable polygons stay editable whatever their band membership;
    longstripe widens editable_layers instead. Only an out-of-band bridge
    polygon is demoted, and it becomes comment-only, with the validator's
    provenance check rejecting ops on it. One-directional, and composes with the
    per-polygon freeze."""
    geom = ctx.geometry_model
    if geom is None:
        return
    polys = geom.polygons
    for leaf in leaves:
        eset = set(leaf.editable_layers)
        if not eset:
            continue
        # Top-level editable polygons stay editable whatever their band
        # membership; longstripe widens editable_layers so the validator's
        # band gate accepts those metals, and the window-containment classifier
        # decides which crop section each one lands in. The out-of-band bridge
        # demotion below is kept, because it avoids a cross-leaf ownership
        # change.
        pass
        # Out-of-band bridges demote to band_background.
        kept_bridge = []
        for pid in leaf.bridge_polygons:
            poly = polys.get(pid)
            if poly is not None and poly.layer_name not in eset:
                if pid not in leaf.band_background:
                    leaf.band_background.append(pid)
            else:
                kept_bridge.append(pid)
        leaf.bridge_polygons = kept_bridge


def _bbox_intersect(a, b) -> bool:
    return a[0] <= b[2] and b[0] <= a[2] and a[1] <= b[3] and b[1] <= a[3]


def _derive_net_map(leaf: Leaf, polygons_by_id) -> Dict[str, List[str]]:
    pids = list(leaf.editable_polygons) + list(leaf.bridge_polygons)
    if not pids:
        return {}
    polys = [polygons_by_id[p] for p in pids if p in polygons_by_id]
    if not polys:
        return {}
    n = len(polys)
    parent = list(range(n))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for i in range(n):
        for j in range(i + 1, n):
            if _bboxes_touch(polys[i].bbox_dbu, polys[j].bbox_dbu):
                union(i, j)

    groups: Dict[int, List[str]] = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(polys[i].polygon_id)
    return {"net_{0:03d}".format(idx): members
            for idx, (_root, members) in enumerate(sorted(groups.items()))}


def _bboxes_touch(a, b) -> bool:
    return a[0] <= b[2] and b[0] <= a[2] and a[1] <= b[3] and b[1] <= a[3]


# ---------------------------------------------------------------------------
# Band polygon counting and the residual-overlap merge fixpoint.
# ---------------------------------------------------------------------------

def _build_band_layer_index(polys_by_id):
    """Map each layer name to the list of top-level polygon bboxes on it.

    Built once: geometry is immutable across split and merge, so the same index
    serves every band count."""
    idx: Dict[str, List[Tuple[int, int, int, int]]] = {}
    for poly in polys_by_id.values():
        idx.setdefault(poly.layer_name, []).append(poly.bbox_dbu)
    return idx


def _band_count(bbox, band_layers, band_index) -> int:
    """Count the top-level polygons on a layer in ``band_layers`` whose bbox
    intersects ``bbox``. A ``band_index`` of None or an empty ``band_layers``
    returns 0, so the split gate degrades to extent-only."""
    if not band_index or not band_layers:
        return 0
    x1, y1, x2, y2 = bbox
    n = 0
    for ly in band_layers:
        for a in band_index.get(ly, ()):
            if a[0] <= x2 and x1 <= a[2] and a[1] <= y2 and y1 <= a[3]:
                n += 1
    return n


def _clip_band_layers(violation_ids, violations_by_id):
    """Return the band layer set (editable layers unioned with background
    layers) for a set of violations, matching layer_band.band_for_leaf."""
    nset: set = set()
    for vid in violation_ids:
        v = violations_by_id.get(vid)
        if v is None:
            continue
        for lyr in layer_band.layers_of_rule(v.rule_id):
            nset.add(lyr)
    editable, background = layer_band.band_for_layers(nset)
    return editable | background


def _bbox_area(b) -> int:
    return max(0, b[2] - b[0]) * max(0, b[3] - b[1])


def _bbox_inter_area(a, b) -> int:
    ix = min(a[2], b[2]) - max(a[0], b[0])
    iy = min(a[3], b[3]) - max(a[1], b[1])
    return 0 if ix <= 0 or iy <= 0 else ix * iy


def _bbox_contains(big, small) -> bool:
    return (big[0] <= small[0] and big[1] <= small[1]
            and big[2] >= small[2] and big[3] >= small[3])


def _uniq_extend(dst: List[str], src) -> None:
    """Order-preserving dedup append (in place)."""
    seen = set(dst)
    for x in src:
        if x not in seen:
            dst.append(x)
            seen.add(x)


def _merge_member_leaves(members, viol_by_id, polys, insts, cdefs):
    """Fold ``members`` (two or more leaves) into ``members[0]``.

    Violations and the owned collections are unioned with an order-preserving
    dedup, so no violation appears twice and single ownership survives, and the
    bbox is recomputed over the union. Context fields that
    _annotate_band_layers and _annotate_leaves rebuild on the grown bbox are
    reset, so re-annotation fills each of them from the grown bbox alone."""
    base = members[0]
    vios: List[str] = []
    for m in members:
        _uniq_extend(vios, m.violations)
    base.violations = vios
    for attr in ("editable_polygons", "bridge_polygons", "context_readonly",
                 "subcell_instances", "band_background", "frozen_context"):
        merged = list(getattr(base, attr))
        for m in members[1:]:
            _uniq_extend(merged, getattr(m, attr))
        setattr(base, attr, merged)
    owned = list(base.owned_instances)
    for m in members[1:]:
        _uniq_extend(owned, m.owned_instances)
    base.owned_instances = tuple(owned)
    # Union the band layer sets here rather than waiting for re-annotation: the
    # fixpoint's next pass reads editable_layers and background_layers as the
    # band-cap input, so a stale members[0]-only band would under-count and let
    # an over-cap merge through. Re-annotation later recomputes both from the
    # grown bbox.
    ed: set = set(base.editable_layers)
    bg: set = set(base.background_layers)
    for m in members[1:]:
        ed |= set(m.editable_layers)
        bg |= set(m.background_layers)
    base.editable_layers = tuple(sorted(ed))
    base.background_layers = tuple(sorted(bg))
    base.depth = max(m.depth for m in members)
    base.bbox_dbu = clip_bbox_dbu(vios, viol_by_id, polys, insts, cdefs)
    # Rebuilt by re-annotation on the grown bbox; reset to avoid stale entries.
    base.net_to_polygons = {}
    base.long_open_ends = {}
    base.stdcell_pin_polys = []
    return base


def build_union_leaf(ctx, member_ids, leaf_id):
    """Build one merged union leaf out of the leaves named in ``member_ids``.

    The prompt side, the host prep step and the DRC preview all call this, so
    every caller gets the same leaf. A union carries only its members' own
    content: the members are deep-copied, folded together by
    _merge_member_leaves (which unions editable polygons, violations, owned and
    subcell instances and band background), and their own read-only context is
    unioned on top. It keeps that member-only annotation rather than recomputing
    over the merged bbox, because that recompute swept in polygons, vias and std
    cells from non-member leaves sharing the same row band. The member ids are
    recorded for the preview; ctx.leaves keeps the members, not the union."""
    import copy
    geom = ctx.geometry_model
    polys, insts, cdefs = geom.polygons, geom.instances, geom.cell_defs
    viol_by_id = {v.violation_id: v for v in ctx.violations}
    members = [copy.deepcopy(ctx.leaves[m]) for m in member_ids]
    ub = [min(m.bbox_dbu[0] for m in members),
          min(m.bbox_dbu[1] for m in members),
          max(m.bbox_dbu[2] for m in members),
          max(m.bbox_dbu[3] for m in members)]
    # Capture the read-only context each member already carries, before
    # _merge_member_leaves mutates members[0]: it resets those fields, expecting
    # a re-annotation that is deliberately skipped here. Unioning the members'
    # own context keeps the result to exactly the members' items.
    ro = []; sp = []; n2p = {}; loe = {}
    for m in members:
        _uniq_extend(ro, list(getattr(m, "ro_neighbor_ids", []) or []))
        for x in (getattr(m, "stdcell_pin_polys", []) or []):
            if x not in sp:
                sp.append(x)
        n2p.update(getattr(m, "net_to_polygons", {}) or {})
        loe.update(getattr(m, "long_open_ends", {}) or {})
    base = _merge_member_leaves(members, viol_by_id, polys, insts, cdefs)
    base.bbox_dbu = tuple(ub)                 # window spanning the members
    base.ro_neighbor_ids = ro                 # members' own read-only neighbours
    base.stdcell_pin_polys = sp               # members' own std-cell pin background
    base.net_to_polygons = n2p                # members' own net context
    base.long_open_ends = loe                 # members' own open ends
    base.leaf_id = leaf_id
    base.is_pdn = False
    base.union_members = list(member_ids)     # lets the preview rebuild this leaf
    # Re-run the open-end classification on the union window. classify is
    # idempotent by design, and the union bbox contains every member bbox, so
    # the open-end flags can only become more permissive: no lever is lost, and
    # a stripe with both ends inside the window is promoted to fully editable.
    longstripe.classify(base, ctx)
    return base


# Reserved id for the whole-design unit. It can never collide with a per-leaf
# id (leaf_%04d) or a union id (<case>_union_row%d).
WHOLE_UNIT_ID = "whole_design"


def build_whole_design_leaf(ctx, leaf_id=WHOLE_UNIT_ID):
    """Build the single leaf that covers the whole design.

    The container prompt side, the DRC preview reconstruction and the host gate,
    scorer, assemble and cu_drc all call this, so every caller sees the same
    leaf. The whole block is one unit: bbox is the block bounds, the violations
    are every input violation, and editable_polygons is every top-level polygon
    except the die boundary, PDN nets included. Std-cell and V0 protections
    still hold: std-cell internals are never top-level polygon ids and so are
    unreachable by polygon ops, the validator's add guard iterates
    leaf.subcell_instances, which here is every instance, and V0 stays out of
    the editable band. Per-instance allowed_ops still govern move and delete
    legality, so std cells remain frozen; owned_instances covering every id is
    vacuous with a single unit. long_open_ends stays empty, so the validator
    rejects every open-end resize -- that op class disappears along with the
    window borders. The leaf exists only as the returned object."""
    geom = ctx.geometry_model
    polys, insts, cdefs = geom.polygons, geom.instances, geom.cell_defs
    editable = [pid for pid in sorted(polys)
                if polys[pid].layer_name not in _SEED_EXCLUDE_LAYERS]
    all_iids = sorted(insts.keys())
    # Editable band: every layer present on a top-level polygon plus every via
    # cut and landing layer present in a via cell def, minus V0 (the std-cell
    # device floor; the validator's V0 rejections stay authoritative).
    from .crop_body import _layer_name_for_gds   # local: avoid import cycle
    layers = set()
    for pid in editable:
        layers.add(polys[pid].layer_name)
    for cd in cdefs.values():
        if cd.kind != "via":
            continue
        for (gds, _pts, _cut) in cd.shapes:
            lname = _layer_name_for_gds(gds)
            if lname:
                layers.add(lname)
    layers.discard("V0")
    # Net map: merge of the per-leaf cluster maps, prefixed with the leaf id so
    # per-leaf 'net_000' style keys never collide. Losing a cluster would only
    # make the minimum-spacing check more conservative; the block-level
    # connectivity gate is authoritative either way.
    n2p = {}
    for lid in sorted(ctx.leaves):
        for net, members in (ctx.leaves[lid].net_to_polygons or {}).items():
            n2p["%s:%s" % (lid, net)] = list(members)
    viol_by_id = {v.violation_id: v for v in ctx.violations}
    fams = set()
    for v in ctx.violations:
        fams.add(v.rule_family or "other")
    leaf = Leaf(
        leaf_id=leaf_id,
        editable_polygons=editable,
        bridge_polygons=[],
        subcell_instances=list(all_iids),
        violations=[v.violation_id for v in ctx.violations],
        net_to_polygons=n2p,
        block_bounds_dbu=tuple(geom.block_bounds_dbu),
        bbox_dbu=tuple(geom.block_bounds_dbu),
        strap_class=None,
        depth=0,
        rule_families=tuple(sorted(fams)),
        context_readonly=[],
        editable_layers=tuple(sorted(layers)),
        background_layers=(),
        owned_instances=tuple(all_iids),
        is_pdn=False,
        pdn_rail="",
    )
    leaf.whole_design = True
    # Sanity: every violation id resolves, matching the host DRC json.
    assert all(vid in viol_by_id for vid in leaf.violations)
    return leaf


def _merge_overlapping_leaves(leaves, ctx, band_index,
                              band_cap=_BAND_SPLIT_CAP):
    """Fixpoint merge of contained or heavily overlapping leaves into
    parallel-safe crops.

    Each pass recomputes overlap on the grown bboxes; an edge is merged only if
    the recomputed band count on the merged bbox stays within ``band_cap``. The
    cap binds on every edge, because even a containment merge that does not grow
    the bbox unions the two band layer sets and can inflate the count. Returns
    (leaves, passes, refused_total, merged_leaves)."""
    geom = ctx.geometry_model
    if geom is None or len(leaves) < 2:
        return leaves, 0, 0, []
    polys = geom.polygons
    insts = geom.instances
    cdefs = geom.cell_defs
    viol_by_id = {v.violation_id: v for v in ctx.violations}

    def _leaf_band(L):
        return set(L.editable_layers) | set(L.background_layers)

    merged_ids: set = set()
    refused_total = 0
    passno = 0
    while passno < _MERGE_MAX_PASSES:
        passno += 1
        n = len(leaves)
        boxes = [L.bbox_dbu for L in leaves]
        parent = list(range(n))

        def find(i):
            while parent[i] != i:
                parent[i] = parent[parent[i]]
                i = parent[i]
            return i

        edges: List[Tuple[int, int, int]] = []
        for i in range(n):
            ai = boxes[i]
            aa = _bbox_area(ai)
            for j in range(i + 1, n):
                bj = boxes[j]
                ia = _bbox_inter_area(ai, bj)
                if ia == 0:
                    continue
                ab = _bbox_area(bj)
                sm = aa if aa < ab else ab
                if sm <= 0:
                    continue
                cont = _bbox_contains(ai, bj) or _bbox_contains(bj, ai)
                # containment, or an overlap ratio (intersection over the
                # smaller area) above 0.5
                if cont or ia * 2 > sm:
                    edges.append((0 if cont else 1, i, j))
        if not edges:
            break
        edges.sort()                      # containment edges first, then partial overlap
        cv = {i: list(leaves[i].violations) for i in range(n)}
        cband = {i: _leaf_band(leaves[i]) for i in range(n)}
        pass_changed = False
        for (_kind, i, j) in edges:
            ri, rj = find(i), find(j)
            if ri == rj:
                continue
            vios = list(dict.fromkeys(cv[ri] + cv[rj]))
            mbox = clip_bbox_dbu(vios, viol_by_id, polys, insts, cdefs)
            mband = cband[ri] | cband[rj]
            if _band_count(mbox, mband, band_index) > band_cap:
                refused_total += 1        # band-cap refusal: leaves residual overlap
                continue
            parent[rj] = ri
            cv[ri] = vios
            cband[ri] = mband
            pass_changed = True
        groups: Dict[int, List[int]] = {}
        for i in range(n):
            groups.setdefault(find(i), []).append(i)
        new_leaves: List[Leaf] = []
        for _root, mem in sorted(groups.items()):
            if len(mem) == 1:
                new_leaves.append(leaves[mem[0]])
                continue
            base = _merge_member_leaves([leaves[m] for m in mem],
                                        viol_by_id, polys, insts, cdefs)
            merged_ids.add(id(base))
            new_leaves.append(base)
        leaves = new_leaves
        if not pass_changed:
            break
    merged_leaves = [L for L in leaves if id(L) in merged_ids]
    return leaves, passno, refused_total, merged_leaves
