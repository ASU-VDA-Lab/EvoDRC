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

"""Detect the power-distribution nets and give each one its own crop.

Runs between clip building and clip merging. The power nets are derived
geometrically from the layout script: same-layer metals are merged, a
metal-to-via graph is built, and every connected component that spans most of
the block and contains a tap or decap cell counts as a power net. Each net
becomes one leaf whose editable polygons are that net's own shapes, and the
violations it captures leave the ordinary clip pool. Any degenerate input or
internal failure degrades to a no-op that leaves the clips untouched.

Two power crops may overlap in bbox, but their editable polygon and owned via
sets are disjoint, so crops worked on in parallel never touch the same shape.
"""


from collections import defaultdict
from typing import Dict, List, Set

from ._invariant import bbox_intersect
from .clips import compute_global_poly_ids
from .layer_band import layers_of_rule
from .logging_setup import get_logger, stage_extra
from .model import (set_pdn_editable_pids, _is_routing_via_instance,
                    instance_block_bbox_dbu)
from .types import LAYER_NUM_TO_NAME, Leaf


# A power net has to span more than this fraction of the longer die side and
# contain a tap or decap cell. The threshold is deliberately higher than the one
# clip merging uses for global polygons: a lower bar also picks up signal spines
# and via pillars here.
_PDN_SPAN_FRAC = 0.5

# A net's capture region -- the polygons a violation is matched against -- is
# limited to its polygons at or above this GDS layer number, that is the upper
# straps. The lower rails are excluded because their full width would capture
# unrelated signal violations.
_PDN_STRAP_MIN_LAYER_NUM = 50

# Diagnostic threshold, not a gate. A power net is usually fed by multi-cut
# power-via arrays, so a classified net attached by fewer than this many is
# logged at INFO. Classification stays purely geometric and such a net is still
# treated as power; the log line is a cheap tripwire for a future mis-pick.
_PDN_MIN_STRAP_VIAS = 4


def _bbox_inter_area(a, b) -> int:
    dx = min(a[2], b[2]) - max(a[0], b[0])
    dy = min(a[3], b[3]) - max(a[1], b[1])
    if dx < 0 or dy < 0:
        return 0
    return dx * dy


def _bbox_contact_score(a, b):
    """Bounding-box contact score that also handles degenerate boxes.

    DRC edge markers can have a zero-width or zero-height bbox. Such a marker
    can touch a power strap while having no intersection area, so an area-only
    score would drop it from the carve. Returns the overlap area for a real
    overlap, the shared edge length for edge contact, 1 for point contact and 0
    when the boxes are disjoint. Only the violation-to-net assignment uses this;
    _bbox_inter_area keeps the plain area semantics for its own callers."""
    dx = min(a[2], b[2]) - max(a[0], b[0])
    dy = min(a[3], b[3]) - max(a[1], b[1])
    if dx < 0 or dy < 0:
        return 0
    if dx > 0 and dy > 0:
        return dx * dy       # area contact
    if dx > 0:
        return dx            # horizontal edge contact
    if dy > 0:
        return dy            # vertical edge contact
    return 1                 # point contact


def _assign_net(viol, live, cap_box, lay_box):
    """Assign one violation to a power net, returning its index or None.

    The first pass scores the violation's bbox against each net's capture
    (strap) polygons. Ownership really follows the whole connected net, though,
    and the capture set only holds the top straps, so when the first pass finds
    nothing the violation is re-scored against each net's full polygon set
    restricted to the rule's own layers: a marker on a lower net shape beneath
    a strap is still owned, while a marker away from every net shape stays
    unowned. Restricting to the rule's layers is what keeps the wide lower rails
    from capturing unrelated violations. Both passes break ties on
    (-score, net index), so the owner is deterministic."""
    vb = viol.bbox_dbu
    best = None                           # (-score, net_index) total order
    for ni in live:
        score = 0
        for pid, pb in cap_box[ni].items():
            if bbox_intersect(vb, pb):
                score += _bbox_contact_score(vb, pb)
        if score <= 0:
            continue
        cand = (-score, ni)
        if best is None or cand < best:
            best = cand
    if best is not None:
        return best[1]
    # Fallback: score against the whole net geometry on the rule's layers.
    rl = layers_of_rule(getattr(viol, "rule_id", ""))
    if not rl:
        return None
    for ni in live:
        by_layer = lay_box.get(ni) or {}
        score = 0
        for ly in rl:
            for pb in by_layer.get(ly, ()):
                score += _bbox_contact_score(vb, pb)
        if score <= 0:
            continue
        cand = (-score, ni)
        if best is None or cand < best:
            best = cand
    return best[1] if best is not None else None


def _union_bbox(boxes):
    x0 = min(b[0] for b in boxes)
    y0 = min(b[1] for b in boxes)
    x1 = max(b[2] for b in boxes)
    y1 = max(b[3] for b in boxes)
    return (x0, y0, x1, y1)


def _reset_pdn_state(ctx, full_global) -> None:
    """Reset every pdn_* field on the context to its empty value.

    ctx.pdn_global_polys is still set to the full pre-carve global-polygon set,
    so clip merging behaves exactly as it would without this pre-pass."""
    ctx.pdn_global_polys = full_global
    ctx.pdn_leaves = []
    ctx.pdn_net_pids = {}
    ctx.pdn_net_violations = {}
    ctx.pdn_editable_pids = set()
    ctx.pdn_net_vias = {}
    ctx.pdn_owned_via_iids = set()
    ctx.pdn_detect_report = []
    set_pdn_editable_pids(())


def stage_pdn_prepass(ctx) -> None:
    """Run the power-net pre-pass on a case; idempotent via ctx.pdn_done."""
    log = get_logger()
    if getattr(ctx, "pdn_done", False):
        return

    geom = ctx.geometry_model
    polys = geom.polygons if geom else {}
    bb = geom.block_bounds_dbu if geom else None

    # Freeze the global-polygon set on the full, pre-carve clips before anything
    # is removed. Both the detection below and clip merging read this one set,
    # and it is stashed even when the pre-pass degrades to a no-op.
    full_global = compute_global_poly_ids(ctx.clips, polys, bb)
    _reset_pdn_state(ctx, full_global)
    ctx.pdn_done = True

    case_name = ctx.case_info.case_name if ctx.case_info else ""
    layout_path = ctx.case_info.layout_path if ctx.case_info else ""
    instances = geom.instances if geom else {}
    # Detection needs both the layout script and the parsed geometry model.
    if not polys or not bb or not case_name or not instances:
        log.info("S4.5 no-op (degenerate inputs)", extra=stage_extra("S4.5"))
        return
    if not layout_path:
        log.info("S4.5 no-op (no layout path)", extra=stage_extra("S4.5"))
        return

    # Imported here rather than at module scope: conn_check pulls in shapely,
    # and a missing shapely has to degrade instead of failing the whole run.
    try:
        from . import conn_check as cc
    except ImportError as exc:               # pragma: no cover (image ships shapely)
        log.warning("S4.5 no-op: conn_check/shapely import failed (%s)",
                    exc, extra=stage_extra("S4.5"))
        return

    if case_name not in cc.BLOCK_HIGHEST_LAYER:
        log.info("S4.5 no-op (unknown case %s)", case_name,
                 extra=stage_extra("S4.5"))
        return

    try:
        _run(ctx, cc, polys, case_name, layout_path, full_global, log)
    except Exception as exc:                 # pragma: no cover (fail-soft)
        # Degrade to the ordinary flow, resetting any partial state so the
        # clips are never left half-carved.
        log.warning("S4.5 failed (%s); no-op carve, current method unchanged",
                    exc, extra=stage_extra("S4.5"))
        _reset_pdn_state(ctx, full_global)


def _run(ctx, cc, polys, case_name, layout_path, full_global, log) -> None:
    geom = ctx.geometry_model
    cell_defs = geom.cell_defs
    instances = geom.instances
    bb = geom.block_bounds_dbu

    # Canonical integer key for a polygon: independent of hash seed and of
    # winding, so a shape parsed from the script matches the same shape in the
    # model even when the two list its points differently.
    def _canon_key(points):
        pts = [[int(x), int(y)] for (x, y) in points]
        return cc.points_key(cc.canonicalize_points(pts))

    # --- 1. Net detection ----------------------------------------------------
    # Parse the script, merge same-layer metals, build the metal/via graph, then
    # union the metal nodes a via bridges; each component is one net.
    polys_by_layer = cc.parse_block_script(layout_path)
    if not polys_by_layer:
        log.info("S4.5 no-op (empty parsed layout)", extra=stage_extra("S4.5"))
        return
    merged = cc.merge_same_layer_metals(polys_by_layer, cc.BLOCK_METAL_LAYERS)
    _adj, vias = cc.build_graph(merged, polys_by_layer, cc.BLOCK_VIA_LAYERS,
                                cc.BLOCK_VIA_TO_BELOW_ABOVE)

    # Deterministic key order: layers sorted, and the super-shapes inside a
    # layer are already sorted by bbox when they are merged.
    keys: List[tuple] = []
    for l in sorted(merged.keys()):
        for sp in merged[l]:
            keys.append((l, sp["super_id"]))
    if not keys:
        log.info("S4.5 no-op (no merged metals)", extra=stage_extra("S4.5"))
        return
    key_idx = {k: i for i, k in enumerate(keys)}
    uf = cc.UnionFind(len(keys))
    for v in vias:                            # list -> deterministic order
        am = v["all_metals"]                  # sorted list of (layer, super_id)
        if len(am) < 2:
            continue
        a0 = am[0]
        if a0 not in key_idx:
            continue
        for j in range(1, len(am)):
            aj = am[j]
            if aj in key_idx:
                uf.union(key_idx[a0], key_idx[aj])

    comps: Dict[int, List[tuple]] = defaultdict(list)
    for k in keys:
        comps[uf.find(key_idx[k])].append(k)

    die_side = max(bb[2] - bb[0], bb[3] - bb[1]) if bb else 0
    if die_side <= 0:
        log.info("S4.5 no-op (degenerate die)", extra=stage_extra("S4.5"))
        return

    # A component is a power net when it spans the block and holds a tap cell.
    power_comps = []                          # (comp_bbox, [metal_key,...])
    for root in sorted(comps.keys()):
        ks = comps[root]
        boxes = [merged[l][s]["merged_bounds"] for (l, s) in ks]
        comp_bbox = _union_bbox(boxes)
        span = max(comp_bbox[2] - comp_bbox[0],
                   comp_bbox[3] - comp_bbox[1]) / float(die_side)
        if span <= _PDN_SPAN_FRAC:
            continue
        has_tap = False
        for (l, s) in ks:
            for o in merged[l][s]["originals"]:
                sc = (o.get("source_cell") or "").upper()
                if "TAP" in sc or "DECAP" in sc:
                    has_tap = True
                    break
            if has_tap:
                break
        if not has_tap:
            continue
        power_comps.append((comp_bbox, ks))

    if not power_comps:
        log.info("S4.5: 0 power nets (span^tap); no-op carve",
                 extra=stage_extra("S4.5"))
        return
    if len(power_comps) != 2:
        log.warning("S4.5: expected 2 power nets, found %d (proceeding)",
                    len(power_comps), extra=stage_extra("S4.5"))

    # Order the nets by bounding box, so net indices are stable across runs.
    power_comps.sort(key=lambda t: t[0])
    n_nets = len(power_comps)

    # --- 2. Map the parsed shapes back to model polygon ids ------------------
    # Only top-cell (editable) polygons count as power-grid material. On a key
    # collision the smallest id wins, which keeps the mapping deterministic.
    key2pid: Dict[tuple, str] = {}
    bbox2pid: Dict[tuple, str] = {}
    for pid in sorted(polys.keys()):
        p = polys[pid]
        if p.owner_kind != "editable":
            continue
        k = _canon_key(p.points_dbu)
        if k not in key2pid:
            key2pid[k] = pid
        fk = (p.layer_name, tuple(p.bbox_dbu))
        if fk not in bbox2pid:
            bbox2pid[fk] = pid

    def _orig_to_pid(o, layer_num):
        # Only shapes sourced from the top cell are editable; standard-cell
        # pins stay part of the frozen background. Match on canonical points
        # first, then fall back to (layer name, bbox).
        if o.get("source_cell") != case_name:
            return None
        pid = key2pid.get(_canon_key(o["points"]))
        if pid is not None:
            return pid
        lname = LAYER_NUM_TO_NAME.get(layer_num)
        if lname is None:
            return None
        return bbox2pid.get((lname, tuple(cc.compute_bbox(o["points"]))))

    # --- 3. Per-net editable and capture polygon sets -------------------------
    # Collect each net's mapped polygon ids, noting for each one whether it is
    # an upper strap (part of the capture region) or a lower rail.
    raw_e: List[List[str]] = []               # net_index -> ordered e_pids
    raw_is_cap: List[Dict[str, bool]] = []    # net_index -> pid -> is strap
    for (_cb, ks) in power_comps:
        e_order: List[str] = []
        seen: Set[str] = set()
        is_cap: Dict[str, bool] = {}
        for (l, s) in sorted(ks):
            for o in merged[l][s]["originals"]:
                pid = _orig_to_pid(o, l)
                if pid is None or pid in seen:
                    continue
                seen.add(pid)
                e_order.append(pid)
                is_cap[pid] = (l >= _PDN_STRAP_MIN_LAYER_NUM)
        raw_e.append(e_order)
        raw_is_cap.append(is_cap)

    # --- Keep the nets' editable sets disjoint --------------------------------
    # The nets share no shapes by construction, but should a polygon be claimed
    # by more than one, it goes to the lowest net index. The editable sets then
    # stay pairwise disjoint and two crops can be worked on in parallel.
    pid_owner: Dict[str, int] = {}
    for ni in range(n_nets):
        for pid in raw_e[ni]:
            if pid not in pid_owner:
                pid_owner[pid] = ni
            elif pid_owner[pid] != ni:
                log.warning("S4.5: PDN pid %s claimed by nets %d and %d; "
                            "keeping %d", pid, pid_owner[pid], ni,
                            pid_owner[pid], extra=stage_extra("S4.5"))

    e_pids: List[List[str]] = []              # net_index -> kept e_pids
    cap_pids: List[List[str]] = []            # net_index -> kept capture pids
    for ni in range(n_nets):
        ep: List[str] = []
        cp: List[str] = []
        for pid in raw_e[ni]:
            if pid_owner.get(pid) != ni:
                continue
            ep.append(pid)
            if raw_is_cap[ni].get(pid):
                cp.append(pid)
        e_pids.append(ep)
        cap_pids.append(cp)

    # A net with no editable strap has no capture region and can own no
    # violations, so it is dropped here.
    live = [ni for ni in range(n_nets) if cap_pids[ni]]
    if not live:
        log.info("S4.5: no net has an editable capture strap; no-op carve",
                 extra=stage_extra("S4.5"))
        return

    # --- 4. Assign the violations to nets ------------------------------------
    # Precompute what _assign_net scores against: each net's capture straps, and
    # its full polygon set indexed by layer for the fallback pass.
    cap_box = {ni: {pid: polys[pid].bbox_dbu for pid in cap_pids[ni]
                    if pid in polys} for ni in live}
    lay_box: Dict[int, Dict[str, List[tuple]]] = {}
    for ni in live:
        by_layer: Dict[str, List[tuple]] = {}
        for pid in e_pids[ni]:                # kept (disjoint) net pids
            p = polys.get(pid)
            if p is None:
                continue
            by_layer.setdefault(p.layer_name, []).append(p.bbox_dbu)
        lay_box[ni] = by_layer

    viols = ctx.violations
    viol_by_id = {v.violation_id: v for v in viols}
    net_violations: Dict[int, List[str]] = {ni: [] for ni in live}
    carved_vids: Set[str] = set()
    for v in viols:                           # ctx.violations order (stable)
        ni = _assign_net(v, live, cap_box, lay_box)
        if ni is not None:
            net_violations[ni].append(v.violation_id)
            carved_vids.add(v.violation_id)

    live_nets = [ni for ni in live if net_violations[ni]]
    if not live_nets:
        log.info("S4.5: power nets captured no violations; no-op carve",
                 extra=stage_extra("S4.5"))
        return

    # --- 5. Attach the connecting vias ---------------------------------------
    # A routing via belongs to a net when its world bbox touches both that net's
    # strap region and one of its rails. Ties break on (-score, net index), so
    # every via ends up owned by exactly one net.
    strap_box: Dict[int, tuple] = {}
    rail_boxes: Dict[int, List[tuple]] = {}
    for ni in live_nets:
        sboxes = [polys[pid].bbox_dbu for pid in cap_pids[ni] if pid in polys]
        strap_box[ni] = _union_bbox(sboxes)
        rb = [polys[pid].bbox_dbu for pid in e_pids[ni]
              if pid in polys and pid not in set(cap_pids[ni])]
        rail_boxes[ni] = rb

    pdn_net_vias: Dict[int, List[str]] = {ni: [] for ni in live_nets}
    via_owner: Dict[str, int] = {}
    for iid in sorted(instances.keys()):
        inst = instances[iid]
        if not _is_routing_via_instance(inst, cell_defs):
            continue
        vbb = instance_block_bbox_dbu(inst, cell_defs)
        best = None                           # (-score, net_index) total order
        for ni in live_nets:
            sb = strap_box[ni]
            if not bbox_intersect(vbb, sb):
                continue
            rscore = 0
            rtouch = False
            for rbx in rail_boxes[ni]:
                if bbox_intersect(vbb, rbx):
                    rtouch = True
                    rscore += _bbox_inter_area(vbb, rbx)
            if not rtouch:
                continue
            score = _bbox_inter_area(vbb, sb) + rscore
            cand = (-score, ni)
            if best is None or cand < best:
                best = cand
        if best is not None:
            ni = best[1]
            pdn_net_vias[ni].append(iid)
            via_owner[iid] = ni
    pdn_owned_via_iids: Set[str] = set(via_owner.keys())

    # --- 6. Union of every net's editable polygon ids -------------------------
    live_pdn_pids: Set[str] = set()
    for ni in live_nets:
        for pid in e_pids[ni]:
            live_pdn_pids.add(pid)

    # --- 7. Keep the carved straps marked global ------------------------------
    # The carved straps counted as global on the pre-carve clips, and clip
    # merging has to keep treating them that way, so they are unioned into the
    # frozen global set. A strap new to that set is logged and kept.
    carved_strap_pids: Set[str] = set()
    for ni in live_nets:
        carved_strap_pids.update(cap_pids[ni])
    not_global = carved_strap_pids - full_global
    if not_global:
        log.warning("S4.5: %d carved strap pid(s) not in full_global: %s",
                    len(not_global), sorted(not_global)[:20],
                    extra=stage_extra("S4.5"))
    ctx.pdn_global_polys = full_global | carved_strap_pids

    # --- 8. Per-net diagnostics ----------------------------------------------
    report_lines = []
    for ni in live_nets:
        n_strap = 0
        for iid in pdn_net_vias[ni]:
            cd = cell_defs.get(instances[iid].cell_name)
            if cd is not None and cd.is_strap:
                n_strap += 1
        sb = strap_box[ni]
        top_layer = max((LAYER_NAME_NUM(polys[pid].layer_name)
                         for pid in cap_pids[ni] if pid in polys), default=0)
        report_lines.append(
            "net top=%s strap=%s edit_pids=%d cap_pids=%d vias=%d strapvias=%d "
            "viol=%d -> PDN"
            % (top_layer, sb, len(e_pids[ni]), len(cap_pids[ni]),
               len(pdn_net_vias[ni]), n_strap, len(net_violations[ni])))
        if n_strap < _PDN_MIN_STRAP_VIAS:
            # Informational only. The net is classified from its geometry
            # alone, whatever its strap-via count.
            log.info("S4.5 PDN net attached by %d < %d multi-cut strap vias "
                     "(span^tap power; informational): strap=%s",
                     n_strap, _PDN_MIN_STRAP_VIAS, sb,
                     extra=stage_extra("S4.5"))
    ctx.pdn_detect_report = report_lines

    # --- 9. One leaf per power net, editable only on that net's polygons ------
    pdn_leaves: List[Leaf] = []
    for i, ni in enumerate(live_nets):
        ep = e_pids[ni]
        vids = net_violations[ni]
        via_iids = pdn_net_vias[ni]
        boxes = [polys[pid].bbox_dbu for pid in ep if pid in polys]
        boxes += [viol_by_id[v].bbox_dbu for v in vids if v in viol_by_id]
        x0, y0, x1, y1 = _union_bbox(boxes)
        layers = tuple(sorted({polys[pid].layer_name for pid in ep
                               if pid in polys}))
        leaf = Leaf(
            leaf_id="leaf_pdn_{0:04d}".format(i),
            editable_polygons=list(ep),
            bridge_polygons=[],
            subcell_instances=list(via_iids),
            owned_instances=tuple(via_iids),
            violations=list(vids),
            bbox_dbu=(x0, y0, x1, y1),
            block_bounds_dbu=geom.block_bounds_dbu,
            editable_layers=layers,
            is_pdn=True,
        )
        pdn_leaves.append(leaf)

    ctx.pdn_leaves = pdn_leaves
    ctx.pdn_net_pids = {ni: list(e_pids[ni]) for ni in live_nets}
    ctx.pdn_net_violations = {ni: list(net_violations[ni]) for ni in live_nets}
    ctx.pdn_net_vias = {ni: list(pdn_net_vias[ni]) for ni in live_nets}
    ctx.pdn_owned_via_iids = pdn_owned_via_iids
    ctx.pdn_editable_pids = live_pdn_pids
    set_pdn_editable_pids(live_pdn_pids)

    # --- 10. Carve last: drop the owned violations from the clip pool ---------
    # An order-preserving filter. At this point every clip still holds exactly
    # one violation, so testing the first id is enough.
    ctx.clips = [c for c in ctx.clips
                 if not (c.violation_ids and c.violation_ids[0] in carved_vids)]

    log.info("S4.5: %d PDN net crops, %d violations carved, %d remain; "
             "nets=%s", len(pdn_leaves), len(carved_vids), len(ctx.clips),
             [(strap_box[ni], len(net_violations[ni]), len(e_pids[ni]))
              for ni in live_nets], extra=stage_extra("S4.5"))


# Reverse of LAYER_NUM_TO_NAME, used only by the diagnostic report above. Some
# names map from more than one number, and any representative one will do here.
_LAYER_NAME_TO_NUM = {}
for _num, _name in LAYER_NUM_TO_NAME.items():
    _LAYER_NAME_TO_NUM.setdefault(_name, _num)


def LAYER_NAME_NUM(layer_name):
    return _LAYER_NAME_TO_NUM.get(layer_name, 0)
