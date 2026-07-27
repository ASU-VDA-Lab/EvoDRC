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

"""Merge the patches of gated-in units onto the iteration input.

The input block text is threaded through every gated-in unit's patch in
ascending unit id order, so the result is deterministic, and written to the
repaired layout file. One unit's ops always apply together; when two units edit
the same target, a shared via cell definition goes to an isolated DRC
competition, identical instance edits are deduplicated while differing ones are
dropped on both sides, and other polygon targets are first-wins. Coverage-union
pool winners outrank all of that. Every dropped op is recorded.
"""

import json
import os
from collections import OrderedDict

from ..patch_apply import apply_patch_to_text
from ..patch_parser import parse_patch_from_file_text


_VIA_STRUCT_OPS = ("resize_via_shape", "move_via_shape")


def _op_target_key(op):
    """The namespaced target key an op edits, or None for a fresh add.

    ("via_cell", cell_name)            -- via-structure ops (shared cell def)
    ("polygon", pid, "low"/"high")     -- resize_end (end included)
    ("polygon", pid)                   -- other whole-polygon ops
    ("instance", iid)                  -- instance ops
    None                               -- add_polygon / add_via / malformed
    """
    if not isinstance(op, dict):
        return None
    kind = op.get("op") or op.get("type") or op.get("kind")
    if kind in ("add_polygon", "add", "add_via"):
        return None                # fresh adds are always kept
    if kind in _VIA_STRUCT_OPS:
        cell = op.get("cell_name")
        if cell is not None:
            return ("via_cell", cell)
        return None                # malformed via op: kept; apply may raise
    pid = op.get("polygon_id")
    iid = op.get("instance_id") or op.get("inst_id")
    if kind == "resize_end" and pid is not None:
        # The "low" default matches patch_apply's own default for this op.
        return ("polygon", pid, op.get("end", "low"))
    if pid is not None:
        return ("polygon", pid)
    if iid is not None:
        return ("instance", iid)
    return None


def _prescan_claims(ctx, gated_in, patch_objs):
    """Collect the via-cell and instance claims of every applicable unit.

    Only units with both a patch and a registered leaf take part, so a unit
    that could never apply cannot win a competition or block an instance.
    Returns (via_groups, inst_claims)::

      via_groups:  {cell_name: OrderedDict(unit_id -> [via ops, patch order])}
      inst_claims: {iid: OrderedDict(unit_id -> [instance ops, patch order])}
    """
    via_groups = {}
    inst_claims = {}
    for unit_id in gated_in:
        obj = patch_objs.get(unit_id)
        if obj is None or ctx.leaves.get(unit_id) is None:
            continue
        for op in (obj.get("ops", []) or []):
            key = _op_target_key(op)
            if key is None:
                continue
            if key[0] == "via_cell":
                grp = via_groups.setdefault(key[1], OrderedDict())
                grp.setdefault(unit_id, []).append(op)
            elif key[0] == "instance":
                grp = inst_claims.setdefault(key[1], OrderedDict())
                grp.setdefault(unit_id, []).append(op)
    return via_groups, inst_claims


def _resolve_via_cells(via_groups, input_layout_text, comp_cfg):
    """Resolve each via cell claimed by more than one unit to a single winner.

    Single-owner cells are left out entirely: all their ops apply and no DRC
    runs. ``comp_cfg`` is {"deck", "scratch", "case"}. Returns
    {cell_name: {"winner": uid, "scores": {uid: int|None},
                 "artifacts": scratch_dir_or_None, ...}}."""
    comp_info = {}
    for cell in sorted(via_groups.keys()):
        owners = sorted(via_groups[cell].keys())
        if len(owners) < 2:
            continue                          # single owner, nothing to resolve
        if comp_cfg is None:
            # No DRC runner configured: fail open deterministically and let the
            # lexicographically smallest owner win.
            comp_info[cell] = {"winner": owners[0],
                               "scores": dict((u, None) for u in owners),
                               "artifacts": None, "no_docker": True}
            continue
        from . import via_competition          # only on real contention
        res = via_competition.run_competition(
            input_layout_text, cell,
            dict((u, list(via_groups[cell][u])) for u in owners),
            comp_cfg["deck"], comp_cfg["scratch"], comp_cfg["case"])
        info = {"winner": res["winner"], "scores": res["scores"],
                "artifacts": comp_cfg["scratch"]}
        if res.get("no_transforms"):
            info["no_transforms"] = True
        comp_info[cell] = info
    return comp_info


def _resolve_instances(inst_claims):
    """Resolve each instance claimed by more than one unit.

    Identical op lists keep the lowest unit's copy ("dedup"); any difference
    makes every claimant drop all of its ops on that instance ("drop_all"). A
    single claimant is left untouched, multiple ops and all."""
    resolution = {}
    for iid in sorted(inst_claims.keys()):
        claimants = sorted(inst_claims[iid].keys())
        if len(claimants) < 2:
            continue
        canon = [json.dumps(inst_claims[iid][u], sort_keys=True)
                 for u in claimants]
        if all(c == canon[0] for c in canon):
            resolution[iid] = {"mode": "dedup", "winner": claimants[0],
                               "claimants": claimants}
        else:
            resolution[iid] = {"mode": "drop_all", "claimants": claimants}
    return resolution


def _assemble_core(ctx, gated_in_ids, patch_objs, input_layout_text, out_py,
                   comp_cfg=None, reserved=None):
    """Thread the patches, resolve cross-unit conflicts and write ``out_py``.

    ``comp_cfg`` is {"deck", "scratch", "case"} for the via-cell DRC
    competition; None fails open in-process to the lowest-sorting claimant.
    ``reserved`` maps a target key to ``"cu_pool:<attributed_to>"`` for every
    pool winner, so a colliding regional op is dropped whatever order the units
    are processed in: the measured pool winner outranks an unmeasured regional
    op on the same target. The ``"cu_pool:"`` prefix marks an owner apart from
    every real unit id, so the proposing unit's own leftover op is dropped too.

    Returns {repaired_py, gated_in, drops: {unit_id: rec}}, where each rec holds
    {leaf_id, ops_total, ops_applied, ops_dropped[], had_drop} and optionally
    via_competitions."""
    text = input_layout_text
    op_target_owner = {}
    records = {}
    gated_in = sorted(gated_in_ids)

    # First pass: resolve the via-cell competitions and instance conflicts.
    via_groups, inst_claims = _prescan_claims(ctx, gated_in, patch_objs)
    via_comp_info = _resolve_via_cells(via_groups, input_layout_text,
                                       comp_cfg)
    inst_resolution = _resolve_instances(inst_claims)

    # Second pass: apply in order, honouring those keep and drop decisions.
    for unit_id in gated_in:
        obj = patch_objs.get(unit_id)
        leaf = ctx.leaves.get(unit_id)
        rec = {"leaf_id": unit_id, "ops_total": 0, "ops_applied": 0,
               "ops_dropped": [], "had_drop": False}
        if obj is None or leaf is None:
            records[unit_id] = rec
            continue
        ops = obj.get("ops", []) or []
        rec["ops_total"] = len(ops)
        kept = []
        for op in ops:
            key = _op_target_key(op)
            # Pool winner targets are reserved; this covers every key kind
            # ahead of the branches below.
            if key is not None and reserved and key in reserved:
                rec["ops_dropped"].append(
                    {"op": op, "conflict_with_leaf": reserved[key],
                     "reason": "reserved_by_cu_pool_winner"})
                continue
            if key is None:
                kept.append(op)
                continue
            if key[0] == "via_cell":
                info = via_comp_info.get(key[1])
                if info is not None and unit_id != info["winner"]:
                    rec["ops_dropped"].append(
                        {"op": op, "conflict_with_leaf": info["winner"],
                         "reason": "via_competition_lost_to:%s"
                                   % info["winner"]})
                    continue
                kept.append(op)
                continue
            if key[0] == "instance":
                resn = inst_resolution.get(key[1])
                if resn is not None:
                    if resn["mode"] == "dedup":
                        if unit_id != resn["winner"]:
                            rec["ops_dropped"].append(
                                {"op": op,
                                 "conflict_with_leaf": resn["winner"],
                                 "reason": "external_duplicate",
                                 "claimants": resn["claimants"]})
                            continue
                    else:                                  # drop_all
                        others = [u for u in resn["claimants"]
                                  if u != unit_id]
                        rec["ops_dropped"].append(
                            {"op": op,
                             "conflict_with_leaf":
                                 others[0] if others else unit_id,
                             "reason": "external_conflict_dropped",
                             "claimants": resn["claimants"]})
                        continue
                kept.append(op)
                continue
            # Polygon keys are first-wins, but only across different units:
            # one unit's ops on a target are a single composed edit.
            owner = op_target_owner.get(key)
            if owner is not None and owner != unit_id:
                rec["ops_dropped"].append(
                    {"op": op, "conflict_with_leaf": owner,
                     "reason": "cross_crop_first_wins"})
                continue
            op_target_owner.setdefault(key, unit_id)
            kept.append(op)
        rec["ops_applied"] = len(kept)
        rec["had_drop"] = len(rec["ops_dropped"]) > 0
        # Record the competition outcome on every participant, not just winners.
        for cell in sorted(via_comp_info.keys()):
            if unit_id in via_groups.get(cell, {}):
                rec.setdefault("via_competitions", {})[cell] = \
                    via_comp_info[cell]
        if kept:
            patch = parse_patch_from_file_text(
                json.dumps({"leaf_id": unit_id, "ops": kept,
                            "explanation": obj.get("explanation", "")}),
                unit_id)
            if patch is not None:
                try:
                    text = apply_patch_to_text(text, patch, leaf)
                except Exception:                         # noqa: BLE001
                    rec["had_drop"] = True
        records[unit_id] = rec

    os.makedirs(os.path.dirname(os.path.abspath(out_py)), exist_ok=True)
    with open(out_py, "w", encoding="utf-8") as fh:
        fh.write(text)
    return {"repaired_py": out_py, "gated_in": gated_in, "drops": records}


def assemble(ctx, gated_in_leaf_ids, patch_objs, input_layout_text, out_py,
             comp_cfg=None, pool=None, records_dir=None):
    """Assemble the gated-in patches onto ``input_layout_text`` and write
    ``out_py``.

    ``patch_objs`` maps unit_id to a normalized {leaf_id, ops, explanation}.
    ``comp_cfg`` is {"deck", "scratch", "case"} and enables the via-cell DRC
    competition; None keeps the deterministic fail-open. ``pool``, the result
    of ``cu_drc.run_pool``, routes design-wide ops through the measured
    coverage-union gate: pooled ops are stripped from their unit's patch before
    core assembly, leaving the isolated-cell via competition the rest, and each
    winner's op list is applied once afterwards, attributed to its
    lexicographically first proposer. ``pool=None`` runs core assembly alone.
    ``records_dir``, when given, receives one
    ``<records_dir>/<unit_id>.assembled.json`` per gated unit.

    Returns {repaired_py, gated_in, drops: {unit_id: record}}.
    """
    gated_in_ids = list(gated_in_leaf_ids or [])

    # --- pool pre-filter: pooled ops leave the per-unit stream --------------
    pool_dropped = {}
    if pool and pool.get("strip"):
        decision_of = {}
        for v in pool.get("verdicts", []):
            for op in v.get("ops", []):
                for u in v.get("proposers", []):
                    decision_of[(u, json.dumps([op], sort_keys=True))] = \
                        v.get("decision", "pooled")
        for unit_id, canon_set in pool["strip"].items():
            obj = patch_objs.get(unit_id)
            if not obj:
                continue
            keep = []
            taken = []
            for op in (obj.get("ops") or []):
                c = json.dumps([op], sort_keys=True)
                if c in canon_set:
                    taken.append(
                        {"op": op,
                         "reason": "cu_pool:%s" % decision_of.get(
                             (unit_id, c), "pooled")})
                else:
                    keep.append(op)
            if taken:
                obj["ops"] = keep
                pool_dropped[unit_id] = taken

    # Pre-register every pool winner target so the core pass drops colliding
    # regional ops. The assertion checks that no two winners share a target,
    # which cu_drc's one-winner-per-component tournament guarantees.
    reserved = {}
    if pool and pool.get("winners"):
        for w in pool["winners"]:
            owner = "cu_pool:%s" % (w.get("attributed_to") or "cu_pool")
            for op in (w.get("ops") or []):
                k = _op_target_key(op)
                if k is None:
                    continue
                assert reserved.get(k, owner) == owner, \
                    "two pool winners share target %r -- component " \
                    "invariant broken" % (k,)
                reserved[k] = owner

    res = _assemble_core(ctx, gated_in_ids, patch_objs, input_layout_text,
                         out_py, comp_cfg=comp_cfg, reserved=reserved)

    # --- pool post-pass: apply the winners once and merge their records ----
    if pool:
        if pool.get("winners"):
            with open(res["repaired_py"], "r", encoding="utf-8") as fh:
                text = fh.read()
            for w in pool["winners"]:
                uid = w.get("attributed_to") or "cu_pool"
                try:
                    patch = parse_patch_from_file_text(
                        json.dumps({"leaf_id": uid, "ops": w["ops"],
                                    "explanation": "cu_pool winner"}), uid)
                    leaf = ctx.leaves.get(uid)
                    text = apply_patch_to_text(text, patch, leaf)
                    rec = res["drops"].setdefault(
                        uid, {"leaf_id": uid, "ops_total": 0,
                              "ops_applied": 0, "ops_dropped": [],
                              "had_drop": False})
                    rec["ops_applied"] = rec.get("ops_applied", 0) + \
                        len(w["ops"])
                    rec.setdefault("cu_pool", []).append(
                        {"target": w["target"], "role": "winner",
                         "ops": w["ops"]})
                except Exception as exc:                  # noqa: BLE001
                    rec = res["drops"].setdefault(uid, {"leaf_id": uid})
                    rec.setdefault("cu_pool", []).append(
                        {"target": w.get("target"),
                         "role": "winner_apply_failed", "error": repr(exc)})
            with open(res["repaired_py"], "w", encoding="utf-8") as fh:
                fh.write(text)
        for unit_id in sorted(pool_dropped.keys()):
            rec = res["drops"].setdefault(
                unit_id, {"leaf_id": unit_id, "ops_total": 0,
                          "ops_applied": 0, "ops_dropped": [],
                          "had_drop": False})
            rec.setdefault("ops_dropped", []).extend(pool_dropped[unit_id])
            rec["had_drop"] = True

    # One assembled record per gated unit, holding leaf_id, ops_total,
    # ops_applied, ops_dropped[] and had_drop.
    if records_dir:
        if not os.path.isdir(records_dir):
            os.makedirs(records_dir)
        for unit_id in sorted(res["drops"].keys()):
            p = os.path.join(records_dir, "%s.assembled.json" % unit_id)
            with open(p, "w", encoding="utf-8") as fh:
                json.dump(res["drops"][unit_id], fh, indent=2)

    return res
