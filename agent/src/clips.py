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

"""Construction and merging of clips.

A clip is the working unit for one DRC violation: the violation itself plus
the top-level polygons and subcell instances that sit near it. The first
stage builds exactly one clip per violation. The second merges clips that
share a polygon or a subcell instance, so violations that have to be
repaired together end up in the same clip, with guards that stop a single
widely shared object from chaining most of a block into one giant clip.
"""


from typing import Dict, List, Optional, Set, Tuple

from .logging_setup import get_logger, stage_extra
from .model import clip_bbox_dbu, instance_block_bbox_dbu, set_global_poly_ids
from .types import CaseContext, Clip, Polygon, Violation


# Layers that must never seed a clip. The die-boundary polygon covers the whole
# block, so its bounding box overlaps every violation; without this exclusion it
# would be pulled into every clip and drag the rest of the block in with it.
_SEED_EXCLUDE_LAYERS = frozenset(("L235D0",))


# Limits on merge edges created by a shared subcell instance. Both are checked
# against the would-be-merged extent and violation count before the union, and
# an edge that breaks either one is refused, leaving the two clips separate.
# The extent limit is the geometric backstop and matches the maximum leaf side
# used when splitting; it is repeated here rather than imported to avoid a
# circular import. The violation-count limit stops chaining: a large shared
# standard cell or via is touched by a dozen violations at once, and union-find
# transitivity would otherwise link them all into a single clip that still fits
# inside the extent limit. Shared-polygon edges follow the rule below.
_MERGE_MAX_SIDE_DBU = 16000   # 4um, same bound as the leaf-splitting stage
_MERGE_VIOL_CAP = 4           # max violations a shared-instance edge may merge

# Limit on merge edges created by a shared top-level polygon. A long metal
# strap, a power rail or another block-spanning net overlaps dozens of violation
# clips, and transitivity through such a polygon would chain the large majority
# of a block's violations into one clip. A top-level polygon counts as global,
# and is then barred from acting as a merge edge while still appearing in every
# clip's polygon_ids, when its bounding-box span exceeds _GLOBAL_SPAN_FRAC of
# the die side and it is carried by more than _GLOBAL_FANOUT_K clips. A short or
# low-fan-out shared polygon still merges its violations unconditionally. These
# limits are independent of the shared-instance ones above.
_GLOBAL_SPAN_FRAC = 0.25      # global iff bbox span > this fraction of die side
_GLOBAL_FANOUT_K = 4          # and carried by more than K clips


def compute_global_poly_ids(clips, polys, block_bounds) -> Set[str]:
    """Return the ids of the polygons that count as global.

    A polygon is global when more than ``_GLOBAL_FANOUT_K`` clips carry it and
    its longer bounding-box side exceeds ``_GLOBAL_SPAN_FRAC`` of the longer
    side of ``block_bounds``. The result depends only on the set of clips, so
    it is stable across dict and set iteration orders. A block with missing or
    zero bounds yields the empty set, which leaves the guard inactive.
    """
    die_side = (max(block_bounds[2] - block_bounds[0],
                    block_bounds[3] - block_bounds[1])
                if block_bounds else 0)
    out: Set[str] = set()
    if die_side <= 0:
        return out
    poly_fanout: Dict[str, int] = {}
    for c in clips:
        for pid in c.polygon_ids:
            poly_fanout[pid] = poly_fanout.get(pid, 0) + 1
    span_thresh = _GLOBAL_SPAN_FRAC * die_side
    for pid, fo in poly_fanout.items():
        if fo <= _GLOBAL_FANOUT_K:
            continue
        poly = polys.get(pid)
        if poly is None:
            continue
        a = poly.bbox_dbu
        if max(a[2] - a[0], a[3] - a[1]) > span_thresh:
            out.add(pid)
    return out


def stage_build_clips(ctx: CaseContext) -> None:
    """Build one clip per violation.

    A clip carries the polygons the violation names, or the polygons whose
    bounding box overlaps it when the report names none, together with the
    subcell instances whose world bounding box touches the violation. The
    stage always produces as many clips as there are violations.
    """
    log = get_logger()
    log.info("start", extra=stage_extra("S4"))
    clips: List[Clip] = []
    geom = ctx.geometry_model
    polys = geom.polygons if geom else {}
    block_bounds = geom.block_bounds_dbu if geom else None
    # Compute each instance's transformed world bounding box once here, rather
    # than repeating the work for every violation.
    inst_bbox_by_id: Dict[str, Tuple[int, int, int, int]] = {}
    if geom is not None:
        for iid, inst in geom.instances.items():
            inst_bbox_by_id[iid] = instance_block_bbox_dbu(inst, geom.cell_defs)
    for idx, viol in enumerate(ctx.violations):
        polygon_ids = tuple(pid for pid in viol.involves if pid in polys)
        if not polygon_ids:
            # The report named none, so fall back to bounding-box overlap.
            polygon_ids = tuple(
                _find_polys_by_bbox(viol.bbox_dbu, polys, block_bounds))
        instance_ids = _instances_touching_bbox(viol.bbox_dbu, inst_bbox_by_id)
        clips.append(Clip(
            clip_id="c{0:04d}".format(idx),
            violation_ids=(viol.violation_id,),
            polygon_ids=polygon_ids,
            instance_ids=instance_ids,
        ))
    ctx.clips = clips
    log.info("built %d clips", len(clips), extra=stage_extra("S4"))


def stage_merge_clips(ctx: CaseContext) -> None:
    """Merge clips that share a top-level polygon or a subcell instance.

    Clips are joined with union-find. Sharing a polygon merges unconditionally,
    unless that polygon counts as global. Sharing a subcell instance merges only
    if both limits hold for the result of the union, checked before it is
    applied: the merged extent must stay within ``_MERGE_MAX_SIDE_DBU`` on both
    axes, and the merged violation count within ``_MERGE_VIOL_CAP``. A refused
    edge is skipped and the two clips stay separate, though another shared
    instance may still join them later. Edges are visited in a fixed order, so
    repeated runs produce the same merges.
    """
    log = get_logger()
    log.info("start", extra=stage_extra("S5"))
    # The power-distribution pre-pass has to run before the merge: it freezes
    # the global-polygon set over the complete set of clips and then removes
    # power-net violations from ctx.clips. Callers that drive the stages one by
    # one never invoke it, so it runs itself here; ctx.pdn_done makes that a
    # no-op when it already ran.
    if not getattr(ctx, "pdn_done", False):
        from .pdn_prepass import stage_pdn_prepass
        stage_pdn_prepass(ctx)
    clips = ctx.clips
    if not clips:
        ctx.merged_clips = []
        log.info("no clips to merge", extra=stage_extra("S5"))
        return

    geom = ctx.geometry_model
    polys = geom.polygons if geom else {}
    insts = geom.instances if geom else {}
    cdefs = geom.cell_defs if geom else {}
    viol_by_id = {v.violation_id: v for v in ctx.violations}

    bb = geom.block_bounds_dbu if geom else None
    # Reuse the global-polygon set the pre-pass computed over the complete set
    # of clips, instead of recomputing it here. Recomputing after the power-net
    # violations have been removed would lower the fan-out of block-spanning
    # rails, drop them out of the set and let them act as merge edges again.
    # The fallback covers callers that bypass the pre-pass.
    global_polys: Set[str] = (
        ctx.pdn_global_polys
        if getattr(ctx, "pdn_global_polys", None) is not None
        else compute_global_poly_ids(clips, polys, bb))

    parent = list(range(len(clips)))
    # Violation count and extent carried along for each union-find root.
    root_count = [len(c.violation_ids) for c in clips]
    # A clip's extent is the union of its violations' bounding boxes.
    def _clip_extent(c):
        return clip_bbox_dbu(c.violation_ids, viol_by_id, polys, insts, cdefs)
    root_bbox = [_clip_extent(c) for c in clips]

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union_poly(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        parent[rb] = ra
        root_count[ra] += root_count[rb]
        ba, bb = root_bbox[ra], root_bbox[rb]
        root_bbox[ra] = (min(ba[0], bb[0]), min(ba[1], bb[1]),
                         max(ba[2], bb[2]), max(ba[3], bb[3]))

    def union_instance_guarded(a: int, b: int) -> bool:
        """Union two clips only if both limits hold for the merged result.

        Returns True when the union was applied."""
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        if root_count[ra] + root_count[rb] > _MERGE_VIOL_CAP:        # count
            return False
        ba, bb = root_bbox[ra], root_bbox[rb]
        merged = (min(ba[0], bb[0]), min(ba[1], bb[1]),
                  max(ba[2], bb[2]), max(ba[3], bb[3]))
        if (merged[2] - merged[0] > _MERGE_MAX_SIDE_DBU
                or merged[3] - merged[1] > _MERGE_MAX_SIDE_DBU):     # extent
            return False
        parent[rb] = ra
        root_count[ra] += root_count[rb]
        root_bbox[ra] = merged
        return True

    # Clips that share a top-level polygon are joined unconditionally.
    poly_to_clip: Dict[str, int] = {}
    for idx, clip in enumerate(clips):
        for pid in clip.polygon_ids:
            if pid in global_polys:      # merge only on non-global polygons
                continue
            if pid in poly_to_clip:
                union_poly(idx, poly_to_clip[pid])
            else:
                poly_to_clip[pid] = idx

    # Clips that share a subcell instance are joined only if the limits allow
    # it. For each instance the clips touching it are connected to the one with
    # the lowest index, in ascending order. No instance needs to be excluded the
    # way boundary layers do: every instance is a real cell with a real extent,
    # and there is no instance covering the whole block.
    instance_to_clips: Dict[str, List[int]] = {}
    for idx, clip in enumerate(clips):
        for iid in clip.instance_ids:
            instance_to_clips.setdefault(iid, []).append(idx)
    n_applied = n_refused = 0
    for iid in sorted(instance_to_clips.keys()):
        members = instance_to_clips[iid]          # already in ascending order
        anchor = members[0]
        for other in members[1:]:
            if find(anchor) == find(other):
                continue
            if union_instance_guarded(anchor, other):
                n_applied += 1
            else:
                n_refused += 1

    groups: Dict[int, List[int]] = {}
    for idx in range(len(clips)):
        groups.setdefault(find(idx), []).append(idx)

    merged: List[Clip] = []
    for gid, members in sorted(groups.items()):
        viol_ids: List[str] = []
        poly_ids: List[str] = []
        inst_ids: List[str] = []
        for m in members:
            viol_ids.extend(clips[m].violation_ids)
            for pid in clips[m].polygon_ids:
                if pid not in poly_ids:
                    poly_ids.append(pid)
            for iid in clips[m].instance_ids:
                if iid not in inst_ids:
                    inst_ids.append(iid)
        merged.append(Clip(
            clip_id="mc{0:04d}".format(len(merged)),
            violation_ids=tuple(viol_ids),
            polygon_ids=tuple(poly_ids),
            instance_ids=tuple(inst_ids),
            depth=0,
        ))
    ctx.merged_clips = merged
    # Publish the global-polygon set so that clip extents clamp each global
    # strap or rail to a local window around the violation rather than taking
    # its full length. The clips' polygon_ids are unchanged, so the strap is
    # still shown as surrounding context.
    set_global_poly_ids(global_polys)
    log.info("merged %d clips into %d (instance edges: applied=%d refused=%d) "
             "global_polys=%d",
             len(clips), len(merged), n_applied, n_refused, len(global_polys),
             extra=stage_extra("S5"))


def _find_polys_by_bbox(viol_bbox: Tuple[int, int, int, int],
                        polys: Dict[str, Polygon],
                        block_bounds=None) -> List[str]:
    """Return the polygons whose bounding box intersects the violation's.

    Used only when the DRC report does not list the polygons a violation
    involves. Boundary layers and any polygon spanning the whole block are
    skipped, since they overlap every violation and would bloat every clip.
    """
    out: List[str] = []
    for pid, poly in polys.items():
        if poly.layer_name in _SEED_EXCLUDE_LAYERS:
            continue
        a = poly.bbox_dbu
        if block_bounds is not None and tuple(a) == tuple(block_bounds):
            # A polygon covering the whole block, such as the die boundary or
            # a fill frame, is never a genuine neighbour.
            continue
        if (a[0] <= viol_bbox[2] and viol_bbox[0] <= a[2]
                and a[1] <= viol_bbox[3] and viol_bbox[1] <= a[3]):
            out.append(pid)
    return out


def _instances_touching_bbox(viol_bbox, inst_bbox_by_id):
    """Return the subcell instance ids whose world bbox touches `viol_bbox`.

    Touching is inclusive, so contact along an edge or at a single corner
    counts; this is the same test used for polygons. `inst_bbox_by_id` maps
    each instance id to its transformed world bounding box and is precomputed
    by the caller. The result is sorted so later merges are deterministic.
    """
    out = []
    vb = viol_bbox
    for iid, a in inst_bbox_by_id.items():
        if (a[0] <= vb[2] and vb[0] <= a[2]
                and a[1] <= vb[3] and vb[1] <= a[3]):
            out.append(iid)
    return tuple(sorted(out))
