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

"""Move violations out of leaves that have nothing editable to fix them with.

A leaf can hold violations while owning no editable polygon and no movable
instance, because the item that would repair the violation belongs to another
leaf: each item has exactly one owner. This module moves such violations to a
leaf that does own a suitable item and drops the leaf left empty. The move
rewrites leaf membership only, so the single-owner property is preserved.
Violations are matched to owners spatially, using the same per-violation
bounding box the rest of the pipeline works from.
"""

from . import _invariant
from .model import (per_violation_bbox_dbu, clip_bbox_dbu,
                    instance_block_bbox_dbu)


def relocate_pdn_owned(leaves, ctx):
    """Move violations that only a power crop can repair into that crop.

    A violation sitting in an ordinary leaf whose editable touchers are all
    owned by the power-net pre-pass -- every touching editable polygon belongs
    to a power net and every touching movable instance is a power via -- cannot
    be repaired anywhere else, so it is moved to the power leaf it touches
    most, ranked by (-contact score, leaf index). Touching is an inclusive bbox
    contact with no margin. Violations with no editable toucher at all are left
    alone.

    This runs before relocate_c2_empty, which builds its owner index from the
    ordinary leaves only and so cannot see the power leaves. The target leaf's
    violations and bbox are updated together with the context's per-net
    violation lists, and a source leaf the move empties is dropped. Returns
    (surviving_leaves, n_moved, n_dropped)."""
    from .pdn_prepass import _bbox_contact_score   # local: no import cycle
    from .clips import _SEED_EXCLUDE_LAYERS
    pdn_leaves = list(getattr(ctx, "pdn_leaves", []) or [])
    geom = ctx.geometry_model
    if not pdn_leaves or geom is None:
        return leaves, 0, 0
    polys = geom.polygons
    insts = geom.instances
    cell_defs = geom.cell_defs
    viol_by_id = {v.violation_id: v for v in ctx.violations}

    # Ownership maps, taken straight from the power leaves.
    pdn_pid_owner = {}         # power-net polygon id -> power leaf index
    pdn_via_owner = {}         # power via instance id -> power leaf index
    for k, P in enumerate(pdn_leaves):
        for pid in (P.editable_polygons or []):
            pdn_pid_owner.setdefault(pid, k)
        for iid in (getattr(P, "owned_instances", ()) or ()):
            pdn_via_owner.setdefault(iid, k)

    # Power leaf index -> net key, used to keep ctx.pdn_net_violations in sync.
    net_by_leaf = {}
    for ni, pids in (getattr(ctx, "pdn_net_pids", {}) or {}).items():
        pset = set(pids)
        for k, P in enumerate(pdn_leaves):
            if k not in net_by_leaf and pset and pset == set(
                    P.editable_polygons or []):
                net_by_leaf[k] = ni

    # Candidate editable objects, built once. Die-boundary layers are left out,
    # the same exclusion the repair-order and highlight predicates apply.
    edit_polys = []            # (pid, bbox) of top-level editable polygons
    for pid in sorted(polys.keys()):
        p = polys[pid]
        if p.owner_kind != "editable":
            continue
        if p.layer_name in _SEED_EXCLUDE_LAYERS:
            continue
        edit_polys.append((pid, p.bbox_dbu))
    mobile_insts = []          # (iid, world bbox) instances with allowed_ops
    for iid in sorted(insts.keys()):
        inst = insts[iid]
        if not inst.allowed_ops:
            continue
        mobile_insts.append((iid, instance_block_bbox_dbu(inst, cell_defs)))

    n_moved = 0
    emptied = set()
    for L in sorted(leaves, key=lambda x: x.leaf_id):
        if getattr(L, "is_pdn", False):
            continue
        moved_here = []
        for vid in list(L.violations):
            v = viol_by_id.get(vid)
            if v is None:
                continue
            vb = v.bbox_dbu
            all_pdn = True
            n_touch = 0
            scores = {}        # power leaf index -> contact score sum
            for pid, pb in edit_polys:
                s = _bbox_contact_score(vb, pb)
                if s <= 0:
                    continue
                n_touch += 1
                k = pdn_pid_owner.get(pid)
                if k is None:
                    all_pdn = False
                    break
                scores[k] = scores.get(k, 0) + s
            if all_pdn:
                for iid, ib in mobile_insts:
                    s = _bbox_contact_score(vb, ib)
                    if s <= 0:
                        continue
                    n_touch += 1
                    k = pdn_via_owner.get(iid)
                    if k is None:
                        all_pdn = False
                        break
                    scores[k] = scores.get(k, 0) + s
            if not all_pdn or n_touch == 0 or not scores:
                continue
            k = min((-s, kk) for kk, s in scores.items())[1]
            target = pdn_leaves[k]
            if vid not in target.violations:
                target.violations.append(vid)
            tb = target.bbox_dbu
            target.bbox_dbu = (min(tb[0], vb[0]), min(tb[1], vb[1]),
                               max(tb[2], vb[2]), max(tb[3], vb[3]))
            ni = net_by_leaf.get(k)
            sync = getattr(ctx, "pdn_net_violations", None)
            if ni is not None and isinstance(sync, dict) and ni in sync:
                if vid not in sync[ni]:
                    sync[ni].append(vid)
            moved_here.append(vid)
            n_moved += 1
        if not moved_here:
            continue
        gone = set(moved_here)
        L.violations = [x for x in L.violations if x not in gone]
        if L.violations:
            fams = set()
            for vid in L.violations:
                v = viol_by_id.get(vid)
                if v is not None:
                    fams.add(v.rule_family or "other")
            L.rule_families = tuple(sorted(fams))
        else:
            emptied.add(L.leaf_id)
    if not emptied:
        return leaves, n_moved, 0
    return [L for L in leaves if L.leaf_id not in emptied], \
        n_moved, len(emptied)


def relocate_c2_empty(leaves, ctx, margin=None):
    """Move the violations of every leaf with nothing to edit to a leaf that
    does own an editable item able to fix them, dropping the emptied leaves.

    Only a leaf's violations, bbox and rule families change; owned instances,
    editable polygon lists and the geometry itself are never touched. Returns
    the surviving leaves plus the relocated, unrelocatable and grown counts."""
    if margin is None:
        margin = _invariant.SPATIAL_MARGIN_DBU
    geom = ctx.geometry_model
    if geom is None:
        return leaves, 0, 0, 0
    polys = geom.polygons
    insts = geom.instances
    cell_defs = geom.cell_defs
    viol_by_id = {v.violation_id: v for v in ctx.violations}
    inst_bbox = {iid: instance_block_bbox_dbu(inst, cell_defs)
                 for iid, inst in insts.items()}

    def vbox(vid):
        v = viol_by_id.get(vid)
        return None if v is None else per_violation_bbox_dbu(
            v, polys, insts, cell_defs)

    # Index the editable items by the leaves that own them.
    from .crop_body import poly_is_real_lever          # local: no import cycle
    poly_holders = {}          # editable polygon_id -> [leaf,...]
    inst_owner_leaf = {}       # owned mobile instance_id -> leaf
    for L in leaves:
        for pid in L.editable_polygons:
            if poly_is_real_lever(polys.get(pid), L.bbox_dbu):
                poly_holders.setdefault(pid, []).append(L)
        for iid in getattr(L, "owned_instances", ()):
            inst_owner_leaf[iid] = L
    by_id = {L.leaf_id: L for L in leaves}

    def find_owner(L):
        cand = {}
        for vid in L.violations:
            vb = vbox(vid)
            if vb is None:
                continue
            vbm = _invariant.expand(vb, margin)
            # (a) a leaf owning an editable polygon overlapping the violation
            for pid, holders in poly_holders.items():
                p = polys.get(pid)
                if p is None or not _invariant.bbox_intersect(p.bbox_dbu, vbm):
                    continue
                for O in holders:
                    if O.leaf_id != L.leaf_id:
                        cand.setdefault(O.leaf_id, set()).add("poly")
            # (b) a leaf owning the movable instance the violation sits on
            for iid, ib in inst_bbox.items():
                inst = insts.get(iid)
                if inst is None or not inst.allowed_ops:
                    continue
                if not _invariant.bbox_intersect(ib, vbm):
                    continue
                O = inst_owner_leaf.get(iid)
                if O is not None and O.leaf_id != L.leaf_id:
                    cand.setdefault(O.leaf_id, set()).add("inst")
        if not cand:
            return None
        # Deterministic ranking: prefer a destination that already contains all
        # of L's violation bboxes, so it need not grow, then the smaller leaf,
        # then the leaf id.
        def contains_all(O):
            return 1 if all(
                vbox(vid) is None or _invariant.bbox_contains(O.bbox_dbu, vbox(vid))
                for vid in L.violations) else 0
        ranked = sorted(cand.keys(), key=lambda lid: (
            -contains_all(by_id[lid]),
            max(by_id[lid].bbox_dbu[2] - by_id[lid].bbox_dbu[0],
                by_id[lid].bbox_dbu[3] - by_id[lid].bbox_dbu[1]),
            lid))
        return by_id[ranked[0]]

    n_reloc = n_unreloc = growth = 0
    dropped = set()
    targets = [L for L in leaves
               if len(L.violations) > 0 and _invariant.leaf_editable_count(L) == 0]
    for L in sorted(targets, key=lambda x: x.leaf_id):
        O = find_owner(L)
        if O is None or O.leaf_id in dropped:
            n_unreloc += 1
            continue
        old_box = O.bbox_dbu
        O.violations = list(dict.fromkeys(list(O.violations) + list(L.violations)))
        O.bbox_dbu = clip_bbox_dbu(O.violations, viol_by_id, polys,
                                   insts, cell_defs)
        if O.bbox_dbu != old_box:
            growth += 1
        fams = set(O.rule_families)
        for vid in L.violations:
            v = viol_by_id.get(vid)
            if v is not None:
                fams.add(v.rule_family or "other")
        O.rule_families = tuple(sorted(fams))
        L.violations = []
        dropped.add(L.leaf_id)
        n_reloc += 1

    return [L for L in leaves if L.leaf_id not in dropped], \
        n_reloc, n_unreloc, growth
