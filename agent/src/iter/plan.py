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

"""Per-iteration planning of the repair units that get dispatched.

Decomposition splits a block into ``leaf_%04d`` crops, but a repair unit can
span several of them: ``union_layout.group_units`` merges the single-row
crops that share a standard-cell row band into one row union, while multi-row
crops and power-grid crops stay standalone.

This module sits between decomposition and dispatch. ``plan_units`` does the
grouping for the normal configurations; ``plan_whole`` treats the entire block
as one unit for ablation 3. Both return the same dict of units, the subset
worth repairing, the union membership map and any quarantined units, and both
register non-leaf units into ``ctx.leaves``, since the gating, assembly and
tournament stages all resolve units through it.
"""

import json
import os

from ..logging_setup import get_logger, stage_extra
from . import union_layout


def _log(msg):
    get_logger().info("%s", msg, extra=stage_extra("S0"))


def assert_predispatch_touch(ctx, units):
    """Check, before dispatch, that every violation can actually be repaired by
    the unit that carries it.

    For each repairable unit, every one of its violations must be touched by at
    least one of the unit's own editable objects -- an editable polygon or an
    owned movable instance. A violation with no such toucher makes the unit
    unrepairable: it would dispatch and then fail on the in-crop repair-order
    check, so it is caught here instead.

    By default such a unit is quarantined: it is logged, dropped from dispatch
    and returned in the quarantined set, while the other units still run.
    Setting ``FIX4_HARD_FAIL=1`` turns this into a hard failure instead. That
    failure raises RuntimeError rather than SystemExit, which the top-level
    handler would read as a clean shutdown.

    Returns the set of quarantined unit ids.
    """
    from .. import _invariant as _inv
    from .. import hrd_split as _hrd

    fails = []
    bad_units = set()
    for u in units:
        if u.get("n_viol", 0) <= 0:
            continue
        uid = u["unit_id"]
        if u.get("is_union"):
            leaf = _hrd.build_union_leaf(ctx, list(u["member_leaf_ids"]), uid)
        else:
            leaf = ctx.leaves.get(uid)
        if leaf is None:
            fails.append("unit %s: leaf object missing from ctx.leaves" % uid)
            bad_units.add(uid)
            continue
        for f in _inv.unit_touch_failures(ctx, leaf):
            fails.append(
                "unit %s (members=%s): violation %s rule=%s bbox=%s has NO "
                "editable C/D-polygon or owned-movable-instance toucher in "
                "this unit; objects touching it: %s"
                % (uid, u.get("member_leaf_ids"), f["violation_id"],
                   f["rule_id"], list(f["bbox"]),
                   f["touchers"] or "(nothing touches this bbox)"))
            bad_units.add(uid)
    if fails:
        msg = ("PRE-DISPATCH INVARIANT: %d violation(s) have no editable "
               "toucher inside their repairable unit:\n  %s"
               % (len(fails), "\n  ".join(fails)))
        if str(os.environ.get("FIX4_HARD_FAIL", "")).strip() == "1":
            raise RuntimeError(msg + "\n(FIX4_HARD_FAIL=1 -> abort)")
        _log(msg)
        _log("FIX-4 QUARANTINE: unit(s) %s dropped from dispatch this "
             "iteration (their violations stay in the design for later "
             "iterations); all other units proceed" % sorted(bad_units))
    return bad_units


def plan_units(ctx, case, iter_dir, hrd):
    """Group ``ctx.leaves`` into repair units and stage the dispatch inputs.

    Writes ``<iter_dir>/unions.json`` and, for each repairable union unit,
    ``<iter_dir>/input/host_union.<unit_id>.json``. Every union unit is
    registered into ``ctx.leaves``."""
    in_dir = os.path.join(iter_dir, "input")
    if not os.path.isdir(in_dir):
        os.makedirs(in_dir)

    units = union_layout.group_units(ctx, case, hrd)

    # Every violation of every repairable unit must have an editable toucher
    # inside that unit; failing units are quarantined by default.
    quarantined = assert_predispatch_touch(ctx, units)

    with open(os.path.join(iter_dir, "unions.json"), "w",
              encoding="utf-8") as fh:
        json.dump({"iter": _iter_of(iter_dir), "case": case, "units": units,
                   "n_union": sum(1 for u in units if u["is_union"]),
                   "quarantined": sorted(quarantined),
                   "count": len(units)}, fh, indent=2)

    # Repair every unit that carries violations, of any kind: row unions,
    # multi-row crops, single-member bands and the power-grid crops alike.
    # Quarantined units are excluded and their violations persist.
    repairable = [u["unit_id"] for u in units
                  if u["n_viol"] > 0 and u["unit_id"] not in quarantined]
    unions_map = dict((u["unit_id"], u["member_leaf_ids"])
                      for u in units if u["is_union"])

    # Register the union units so gating, assembly and the DRC tournament can
    # resolve them.
    for unit_id in sorted(unions_map.keys()):
        ctx.leaves[unit_id] = hrd.build_union_leaf(
            ctx, list(unions_map[unit_id]), unit_id)

    # Per-union crop metadata visible to the model, containing no solution
    # information. One file per union unit, so several union units in the same
    # iteration cannot collide. leaf_runner._pick_union_leaf checks these keys
    # against its own view of the unit.
    for u in units:
        if u["is_union"] and u["n_viol"] > 0:
            hu = {"leaf_id": u["unit_id"], "case": case,
                  "member_leaf_ids": u["member_leaf_ids"],
                  "bbox_dbu": u["bbox_dbu"],
                  "violation_ids": u["violation_ids"]}
            hu_path = os.path.join(in_dir,
                                   "host_union.%s.json" % u["unit_id"])
            with open(hu_path, "w", encoding="utf-8") as fh:
                json.dump(hu, fh, indent=2)

    # The same projection for plain leaves. Nothing reads these files -- the
    # parity check covers union files only -- but the published tree carries
    # one per repairable plain leaf as a record.
    for u in units:
        if (not u["is_union"]) and u["n_viol"] > 0 \
                and u["unit_id"] not in quarantined:
            hl = {"leaf_id": u["unit_id"], "case": case,
                  "member_leaf_ids": u["member_leaf_ids"],
                  "bbox_dbu": u["bbox_dbu"],
                  "violation_ids": u["violation_ids"]}
            hl_path = os.path.join(in_dir,
                                   "host_leaf.%s.json" % u["unit_id"])
            with open(hl_path, "w", encoding="utf-8") as fh:
                json.dump(hl, fh, indent=2)

    _log("grouped: %d leaves -> %d units (%d union, %d repairable, "
         "%d quarantined)" % (len(ctx.leaves) - len(unions_map), len(units),
                              len(unions_map), len(repairable),
                              len(quarantined)))
    return {"units": units, "repairable": repairable,
            "unions_map": unions_map, "quarantined": sorted(quarantined)}


def plan_whole(ctx, case, iter_dir, hrd):
    """Plan ablation 3, where the whole block forms a single repair unit.

    The analysis pass still runs, since it supplies the geometry model and
    power-grid ownership; what this configuration removes is the unit
    structure, not the parsing. Writes a single-unit ``unions.json`` and, when
    the block has violations, one ``host_leaf`` record."""
    in_dir = os.path.join(iter_dir, "input")
    if not os.path.isdir(in_dir):
        os.makedirs(in_dir)

    whole = hrd.build_whole_design_leaf(ctx)
    # The gating, assembly and tournament stages resolve units through
    # ctx.leaves, so the whole-design unit is registered there below.
    ctx.leaves[whole.leaf_id] = whole

    # The touch check only logs here and leaves the unit in dispatch: with one
    # unit, a violation touched solely by frozen standard cells is unrepairable
    # and persists, whereas dropping the sole unit would end the iteration.
    try:
        from .. import _invariant as _inv
        for f in _inv.unit_touch_failures(ctx, whole):
            _log("WHOLE-DESIGN TOUCH WARNING: violation %s rule=%s bbox=%s "
                 "has NO editable toucher in the whole design (repair-"
                 "impossible; persists); objects touching it: %s"
                 % (f["violation_id"], f["rule_id"], list(f["bbox"]),
                    f["touchers"] or "(nothing touches this bbox)"))
    except Exception as exc:                              # noqa: BLE001
        _log("WARNING: whole-design touch check failed: %r" % (exc,))

    n_viol = len(whole.violations or [])
    unit = {"unit_id": whole.leaf_id, "kind": "whole", "is_union": False,
            "member_leaf_ids": [whole.leaf_id],
            "bbox_dbu": list(whole.bbox_dbu),
            "violation_ids": list(whole.violations or []),
            "n_viol": n_viol}
    with open(os.path.join(iter_dir, "unions.json"), "w",
              encoding="utf-8") as fh:
        json.dump({"iter": _iter_of(iter_dir), "case": case, "units": [unit],
                   "n_union": 0, "quarantined": [], "count": 1}, fh, indent=2)

    repairable = [whole.leaf_id] if n_viol > 0 else []
    # The same record-only projection plan_units writes for plain leaves. The
    # whole-design unit is not a union, so it gets a host_leaf file only.
    if repairable:
        hl = {"leaf_id": unit["unit_id"], "case": case,
              "member_leaf_ids": unit["member_leaf_ids"],
              "bbox_dbu": unit["bbox_dbu"],
              "violation_ids": unit["violation_ids"]}
        with open(os.path.join(in_dir, "host_leaf.%s.json" % unit["unit_id"]),
                  "w", encoding="utf-8") as fh:
            json.dump(hl, fh, indent=2)
    _log("whole-design plan: 1 unit (%s), %d violation(s)"
         % (whole.leaf_id, n_viol))
    return {"units": [unit], "repairable": repairable,
            "unions_map": {}, "quarantined": []}


def _iter_of(iter_dir):
    """Extract the iteration index from a ``.../iter<N>`` directory name.

    The value only labels the written record, so an unparsable name yields 0
    rather than raising."""
    base = os.path.basename(os.path.normpath(iter_dir or ""))
    if base.startswith("iter"):
        try:
            return int(base[4:])
        except (TypeError, ValueError):
            return 0
    return 0
