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

"""Coverage-union DRC pool: a measured gate for design-wide operations.

Some proposed operations reach beyond the window of the unit that proposed
them: edits to a via cell definition, full-edge resizes of die-spanning
polygons, or competing edits to one shared polygon. This module extracts those
operations from the per-unit patches, builds a window set covering each one's
whole footprint, measures every candidate on its own, and keeps the candidate
that removes the most violations while preserving connectivity. It writes
cu_verdicts.json and returns the decision that assemble consumes.
"""

import copy
import hashlib
import json
import os
from concurrent.futures import ThreadPoolExecutor

from ..types import Leaf
from .. import hrd_split as HRD
from ..drc_check import run_faithful_crop_drc
from ..drc_preview import _apply_ops_to_geom
from ..patch_apply import apply_patch_to_text
from ..patch_parser import parse_patch_from_file_text
from ..connectivity import is_connectivity_preserved

# Conflict keys are assemble's own core-pass target keys, including the
# resize_end end-suffix granularity. This creates no import cycle: assemble's
# module level imports only the patch primitives.
from .assemble import _op_target_key

POOLED_VIA_OPS = ("resize_via_shape", "move_via_shape")
DIE_SPAN_FRAC = 0.6          # polygon counts as die-spanning above this
BAND_HALO = 200              # dbu margin appended to synthesized windows
MAX_WORKERS = 4

# Exactly the set drc_preview._apply_ops_to_geom supports, and it has to stay
# that way. Ops outside it, such as add_polygon and add_jog, are invisible to
# window measurement, so a pooled group containing one is rejected outright
# rather than falling back to the regional path, which would let it bypass the
# measured gate. add_via belongs here because _apply_ops_to_geom registers the
# new instance and the faithful render measures it.
MEASURABLE_OPS = frozenset((
    "resize", "move", "resize_end", "delete", "move_instance",
    "delete_instance", "resize_via_shape", "move_via_shape", "add_via"))


def _log(msg):
    print("[cu_drc] %s" % msg, flush=True)


def _ov(a, b, m=0):
    return not (a[2] + m <= b[0] or b[2] <= a[0] - m
                or a[3] + m <= b[1] or b[3] <= a[1] - m)


def _cell_extent(geom, cell_name):
    cd = geom.cell_defs.get(cell_name)
    xs, ys = [], []
    for _lyr, pts, _cut in (cd.shapes if cd else []):
        for x, y in pts:
            xs.append(x)
            ys.append(y)
    if not xs:
        return None
    return (min(xs), min(ys), max(xs), max(ys))


def _canon(ops):
    """Canonical form used for strip matching: byte-exact with what assemble
    compares, so the op is serialised as submitted, ``group`` label and all."""
    return json.dumps(ops, sort_keys=True)


def _canon_content(ops):
    """Canonical form used for cross-unit dedup: ignores the ``group`` label,
    so two units proposing identical ops under different labels collapse into
    one candidate."""
    return json.dumps([{k: v for k, v in op.items() if k != "group"}
                       for op in ops], sort_keys=True)


def _sha1_12(s):
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:12]


def _conflict_key(op):
    k = _op_target_key(op)      # the same keying the core pass uses
    return None if k is None else ":".join(str(x) for x in k)


def _conflict_keys(member_ops):
    """Conflict keys over all member ops, pooled and regional alike."""
    return sorted({ck for op in member_ops
                   for ck in [_conflict_key(op)] if ck})


# ---------------------------------------------------------------------------
# 1. extraction
# ---------------------------------------------------------------------------
def _load_patch_ops(iter_dir, unit_id):
    # Every unit kind -- leaf, union and whole-design -- lives under the same
    # <iter_dir>/leaf/<unit_id> directory.
    p = os.path.join(iter_dir, "leaf", unit_id, "patch.json")
    if not os.path.isfile(p) or os.path.getsize(p) == 0:
        return []
    try:
        with open(p, "r", encoding="utf-8", errors="replace") as fh:
            d = json.load(fh)
        ops = d.get("ops")
        return ops if isinstance(ops, list) else []
    except Exception:  # noqa: BLE001
        return []


def _polygon_die_span(geom, pid):
    p = geom.polygons.get(pid)
    if p is None:
        return 0.0
    bb = geom.block_bounds_dbu
    dw = max(1, int(bb[2]) - int(bb[0]))
    dh = max(1, int(bb[3]) - int(bb[1]))
    px = p.bbox_dbu
    return max((px[2] - px[0]) / float(dw), (px[3] - px[1]) / float(dh))


def _is_pooled(op, geom):
    """The (kind, target) pair for ops the pool owns; None for regional ops."""
    k = op.get("op")
    if k in POOLED_VIA_OPS:
        return ("def", str(op.get("cell_name") or ""))
    if k == "resize":                       # Whole-edge resize; resize_end is
        pid = op.get("polygon_id")          # an end op and stays regional.
        if pid and _polygon_die_span(geom, pid) >= DIE_SPAN_FRAC:
            return ("poly", str(pid))
    return None


def extract_candidates(iter_dir, units, geom):
    """Collect the pooled candidates from every unit's patch.

    Returns ``(pool, strip, rejected)``::

        pool = {cand_key: {"ops": [...], "proposers": [unit...],
                           "target_keys": ["kind:name" of pooled members],
                           "conflict_keys": [target keys over ALL members],
                           "group": label_or_None}}
        strip = {unit_id: set(raw op-list canons)}
        rejected = [verdicts for pooled groups holding an op that window
                    measurement cannot see]

    A group is every op of one unit sharing a non-empty string ``group`` value,
    and the group is pooled as soon as one of its members is. Groups with no
    pooled member stay in the unit's regional stream untouched, with no strip
    and no verdict, because the per-unit gate already measures them atomically.
    Cross-unit dedup uses the content canon while the strip sets use the raw
    one that assemble matches against."""
    pool = {}
    strip = {}
    rejected = {}

    for u in units:
        uid = u["unit_id"]
        ops = _load_patch_ops(iter_dir, uid)
        grouped = {}
        solo = []
        for op in ops:
            if not isinstance(op, dict):
                continue
            label = op.get("group")
            if isinstance(label, str) and label:
                grouped.setdefault(label, []).append(op)
            else:
                solo.append(op)

        # --- ungrouped ops ---
        pooled_here = {}
        for op in solo:
            t = _is_pooled(op, geom)
            if t is None:
                continue
            pooled_here.setdefault(t, []).append(op)
        for t, t_ops in sorted(pooled_here.items()):
            s = strip.setdefault(uid, set())
            s.add(_canon([o for o in t_ops]))     # whole-list canon
            for o in t_ops:
                s.add(_canon([o]))
            tk = "%s:%s" % t
            cand_key = "%s@%s" % (tk, _sha1_12(_canon_content(t_ops)))
            slot = pool.setdefault(cand_key, {
                "ops": t_ops, "proposers": [], "target_keys": [tk],
                "conflict_keys": _conflict_keys(t_ops), "group": None})
            if uid not in slot["proposers"]:
                slot["proposers"].append(uid)

        # --- atomic groups ---
        for label in sorted(grouped):
            g_ops = grouped[label]
            pooled_targets = []
            for op in g_ops:
                t = _is_pooled(op, geom)
                if t is not None:
                    tk = "%s:%s" % t
                    if tk not in pooled_targets:
                        pooled_targets.append(tk)
            if not pooled_targets:
                # No pooled member: the group label is advisory metadata and
                # the members stay regional, with no strip and no verdict.
                continue
            ck = _canon_content(g_ops)
            bad = sorted({str(op.get("op")) for op in g_ops
                          if op.get("op") not in MEASURABLE_OPS})
            if bad:
                # A pooled group with a member that window measurement cannot
                # see: rejected outright with a recorded verdict, all members
                # stripped and nothing applied.
                s = strip.setdefault(uid, set())
                for o in g_ops:
                    s.add(_canon([o]))
                rej = rejected.setdefault(ck, {
                    "decision": "rejected_unmeasurable_group",
                    "target": sorted(pooled_targets)[0],
                    "target_keys": sorted(pooled_targets),
                    "conflict_keys": _conflict_keys(g_ops),
                    "group": label, "atomic": True, "ops": g_ops,
                    "proposers": [], "windows": [], "delta_total": 0,
                    "conn_preserved": None,
                    "reason": "unmeasurable member op kind(s): %s"
                              % ",".join(bad)})
                if uid not in rej["proposers"]:
                    rej["proposers"].append(uid)
                continue
            s = strip.setdefault(uid, set())
            for o in g_ops:              # every member op, regional included
                s.add(_canon([o]))
            cand_key = "grp:" + _sha1_12(ck)
            slot = pool.setdefault(cand_key, {
                "ops": g_ops, "proposers": [],
                "target_keys": sorted(pooled_targets),
                "conflict_keys": _conflict_keys(g_ops), "group": label})
            if uid not in slot["proposers"]:
                slot["proposers"].append(uid)

    for cand in pool.values():
        cand["proposers"].sort()
    for rej in rejected.values():
        rej["proposers"].sort()
    return pool, strip, sorted(rejected.values(),
                               key=lambda r: _canon_content(r["ops"]))


# ---------------------------------------------------------------------------
# 2. coverage windows
# ---------------------------------------------------------------------------
def _rail_bands(ctx):
    """Die-clamped (lo, hi) M1 rail bands, using the same geometric pass as
    union_layout.detect_rail_ys."""
    from . import union_layout
    geom = ctx.geometry_model
    bb = geom.block_bounds_dbu
    all_m1 = [list(p.bbox_dbu) for p in geom.polygons.values()
              if p.layer_name == "M1"]
    rails = union_layout.detect_rail_ys([], all_m1, bb)
    edges = [int(bb[1])] + sorted(int(r) for r in rails) + [int(bb[3])]
    return [(edges[i], edges[i + 1]) for i in range(len(edges) - 1)]


def _footprint_items(ctx, kind, name):
    """List of (item_id, bbox). For a cell definition item_id is the instance
    id, since coverage is content-aware; for a polygon it is a pseudo id."""
    geom = ctx.geometry_model
    if kind == "def":
        ex = _cell_extent(geom, name)
        if ex is None:
            return []
        out = []
        for iid, ins in sorted(geom.instances.items()):
            if ins.cell_name != name:
                continue
            ox, oy = ins.origin_dbu
            out.append((iid, (ox + ex[0], oy + ex[1],
                              ox + ex[2], oy + ex[3])))
        return out
    p = geom.polygons.get(name)
    return [("poly:%s" % name, tuple(p.bbox_dbu))] if p is not None else []


def _unit_leaf_cached(ctx, cache, u):
    uid = u["unit_id"]
    if uid not in cache:
        if u.get("is_union"):
            cache[uid] = HRD.build_union_leaf(ctx, u["member_leaf_ids"], uid)
        else:
            cache[uid] = ctx.leaves[u["member_leaf_ids"][0]]
    return cache[uid]


def coverage_windows(ctx, units, kind, name, conflict_units=None,
                     leaf_cache=None):
    """The window set covering a footprint, as a list of ``("unit", unit)`` and
    ``("synth", bbox, wid)`` entries.

    Coverage is content-aware: a unit window covers a placement only when that
    instance id appears in the window leaf's subcell_instances, meaning the crop
    actually renders it. Geometric containment is not enough, because a PDN
    window spans nearly the whole die yet renders only its own net and so
    cannot see damage in the signal rows. Placements that no unit window
    renders get synthesized rail-band windows, whose pseudo leaf includes every
    piece of geometry overlapping the band and is therefore complete by
    construction."""
    if leaf_cache is None:
        leaf_cache = {}
    if kind == "conflict":
        return [("unit", u) for u in units
                if u["unit_id"] in (conflict_units or [])]
    items = _footprint_items(ctx, kind, name)
    win = []
    covered = dict((iid, False) for iid, _ in items)
    if kind == "def":
        for u in units:
            leaf = _unit_leaf_cached(ctx, leaf_cache, u)
            subs = set(leaf.subcell_instances or [])
            hits = [iid for iid, _ in items if iid in subs]
            if hits:
                win.append(("unit", u))
                for iid in hits:
                    covered[iid] = True
    else:
        # Polygon footprint: a unit window helps only when the polygon is part
        # of its rendered content, so editable, bridge or context of the leaf.
        for u in units:
            leaf = _unit_leaf_cached(ctx, leaf_cache, u)
            pool_ids = set(leaf.editable_polygons or []) \
                | set(leaf.bridge_polygons or []) \
                | set(getattr(leaf, "context_readonly", []) or [])
            if name in pool_ids:
                win.append(("unit", u))
        # The polygon's full strip still needs band coverage below.
    left = [(iid, b) for iid, b in items if not covered[iid]]
    if kind != "def" and items:
        left = items                     # cover the whole strip with bands
    if left:
        bands = _rail_bands(ctx)
        bb = ctx.geometry_model.block_bounds_dbu
        k = 0
        for lo, hi in bands:
            inband = [(iid, b) for iid, b in left
                      if not (b[3] <= lo or b[1] >= hi)]
            if not inband:
                continue
            x0 = max(int(bb[0]), min(b[0] for _, b in inband) - BAND_HALO)
            x1 = min(int(bb[2]), max(b[2] for _, b in inband) + BAND_HALO)
            y0 = max(int(bb[1]), lo - BAND_HALO)
            y1 = min(int(bb[3]), hi + BAND_HALO)
            k += 1
            win.append(("synth", (x0, y0, x1, y1), "cuwin_%04d" % k))
            for iid, _ in inband:
                covered[iid] = True
    n_uncov = sum(1 for v in covered.values() if not v)
    if n_uncov:
        _log("WARNING: %d footprint items of %s:%s not covered by any window"
             % (n_uncov, kind, name))
    return win


def _synth_leaf(ctx, bbox, wid):
    """A window-only pseudo leaf holding read-only context; the faithful
    renderer needs no more than its instances, polygon ids and bbox."""
    geom = ctx.geometry_model
    ctxt = [pid for pid, p in geom.polygons.items()
            if _ov(p.bbox_dbu, bbox)]
    insts = []
    for iid, ins in geom.instances.items():
        ex = _cell_extent(geom, ins.cell_name)
        if ex is None:
            continue
        ox, oy = ins.origin_dbu
        if _ov((ox + ex[0], oy + ex[1], ox + ex[2], oy + ex[3]), bbox):
            insts.append(iid)
    viols = [v.violation_id for v in (ctx.violations or [])
             if _ov(v.bbox_dbu, bbox)]
    return Leaf(leaf_id=wid, editable_polygons=[], bridge_polygons=[],
                subcell_instances=sorted(insts), violations=sorted(viols),
                block_bounds_dbu=geom.block_bounds_dbu,
                bbox_dbu=tuple(bbox), context_readonly=sorted(ctxt))


def _win_leaf(ctx, unions_map, w, leaf_cache=None):
    if w[0] == "synth":
        key = "synth:%s" % (w[2],)
        if leaf_cache is not None and key in leaf_cache:
            return leaf_cache[key]
        leaf = _synth_leaf(ctx, w[1], w[2])
        if leaf_cache is not None:
            leaf_cache[key] = leaf
        return leaf
    return _unit_leaf_cached(ctx, leaf_cache if leaf_cache is not None
                             else {}, w[1])


def _win_key(w):
    if w[0] == "synth":
        return "synth:%d,%d,%d,%d" % tuple(w[1])
    return "unit:%s" % w[1]["unit_id"]


def _components(pool):
    """Group the candidates into conflict components with a union-find over
    their conflict keys, so candidates sharing any target of any kind land in
    one component and at most one of them can win.

    The order is deterministic: components by their lexicographically smallest
    member conflict key, candidates within a component by content canon.
    Returns a list of candidate lists."""
    keys = sorted(pool)
    parent = {k: k for k in keys}

    def _find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def _union(a, b):
        ra, rb = _find(a), _find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)

    by_ck = {}
    for k in keys:
        for ck in pool[k]["conflict_keys"]:
            by_ck.setdefault(ck, []).append(k)
    for ck in sorted(by_ck):
        members = by_ck[ck]
        for m in members[1:]:
            _union(members[0], m)
    groups = {}
    for k in keys:
        groups.setdefault(_find(k), []).append(k)
    comps = []
    for members in groups.values():
        cands = sorted((pool[m] for m in members),
                       key=lambda c: _canon_content(c["ops"]))
        cks = sorted({ck for c in cands for ck in c["conflict_keys"]})
        comps.append((cks[0] if cks else "\uffff",
                      _canon_content(cands[0]["ops"]), cands))
    comps.sort(key=lambda t: (t[0], t[1]))
    return [c for _, _, c in comps]


def _component_windows(ctx, units, comp, leaf_cache):
    """The coverage-window set for one conflict component.

    It is the union of ``coverage_windows`` over the component's pooled targets
    and, for every candidate holding a regional member op, the proposer units'
    own windows: a regional member edits geometry the proposer's crop renders,
    so that window prices its collateral where it occurs. Windows are
    deduplicated by ``_win_key`` in order. Collateral falling strictly outside
    both sets stays invisible to delta_total; only the full-design connectivity
    check sees it there."""
    geom = ctx.geometry_model
    wins = []
    seen = set()

    def _add(ws):
        for w in ws:
            k = _win_key(w)
            if k not in seen:
                seen.add(k)
                wins.append(w)

    conflict_units = sorted({p for c in comp for p in c["proposers"]})
    for tk in sorted({t for c in comp for t in c["target_keys"]}):
        kind, name = tk.split(":", 1)
        _add(coverage_windows(ctx, units, kind, name,
                              conflict_units=conflict_units,
                              leaf_cache=leaf_cache))
    for cand in comp:
        if any(_is_pooled(op, geom) is None for op in cand["ops"]):
            pset = set(cand["proposers"])
            _add([("unit", u) for u in units if u["unit_id"] in pset])
    return wins


# ---------------------------------------------------------------------------
# 3-5. measurement + decision
# ---------------------------------------------------------------------------
def _crop_count(leaf, ctx):
    return sum(run_faithful_crop_drc(leaf, ctx).values())


def _write_verdicts(iter_dir, out):
    """Serialise the pool decision to ``<iter_dir>/cu_verdicts.json``."""
    with open(os.path.join(iter_dir, "cu_verdicts.json"), "w",
              encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)


def run_pool(iter_dir, case, unions_map, units, ctx, golden_conn_path,
             *, work_dir):
    """Run the pool for one iteration.

    Returns ``{"strip": {unit: [canon, ...]}, "winners": [...],
    "verdicts": [...]}`` and writes ``<iter_dir>/cu_verdicts.json``.

    ``units`` and ``ctx`` are required rather than reconstructed, because
    rebuilding them here would diverge from the context the gate already used.
    ``golden_conn_path`` is the case connectivity JSON, passed in because the
    iteration directory holds no copy of it. ``work_dir`` is keyword-only and
    receives the per-candidate scratch layouts, which never enter the published
    iteration record."""
    if os.environ.get("CU_DRC", "1") != "1":
        _log("CU_DRC disabled by env -- pool skipped (legacy path)")
        return None
    # Create the scratch directory once at entry, outside the per-candidate
    # try. An unusable work_dir then raises here, where the controller can log
    # it and fall back; inside the per-candidate handler below it would be
    # absorbed silently and mark every candidate as connectivity-broken.
    os.makedirs(work_dir, exist_ok=True)
    # Only gated-in units contribute ops, so a connectivity-broken or empty
    # unit cannot seed a winner; the coverage windows below still use the full
    # unit list. Scanning for the .verdict extension rather than "*.json" also
    # skips the <leaf_id>.assembled.json files assemble writes to the same dir.
    _EXT = ".verdict"
    gated = set()
    gdir = os.path.join(iter_dir, "gated")
    if os.path.isdir(gdir):
        for f in os.listdir(gdir):
            if f.endswith(_EXT):
                try:
                    with open(os.path.join(gdir, f), "r",
                              encoding="utf-8") as fh:
                        v = json.load(fh)
                    if v.get("gated_in") is True:
                        gated.add(v.get("leaf_id") or f[:-len(_EXT)])
                except Exception:  # noqa: BLE001
                    pass
    units_for_extract = [u for u in units if u["unit_id"] in gated] \
        if gated else units
    # Whole-design mode: the single unit's member_leaf_ids resolve through
    # ctx.leaves in _unit_leaf_cached, so the whole-design leaf is registered
    # once here. With one unit owning every instance, coverage_windows
    # collapses to exactly one whole-block window.
    _wid = getattr(HRD, "WHOLE_UNIT_ID", "whole_design")
    if _wid not in ctx.leaves \
            and any(u.get("unit_id") == _wid for u in units):
        ctx.leaves[_wid] = HRD.build_whole_design_leaf(ctx, _wid)
    geom = ctx.geometry_model

    pool, strip, pre_rejected = extract_candidates(
        iter_dir, units_for_extract, geom)
    verdicts = list(pre_rejected)     # pooled groups nothing can measure
    winners = []
    if not pool and not verdicts:
        _log("no pooled candidates this iteration")
        out = {"strip": {}, "winners": [], "verdicts": []}
        _write_verdicts(iter_dir, out)
        return out
    _log("pool: %d candidate(s) after dedup, %d unmeasurable group(s) "
         "pre-rejected" % (len(pool), len(pre_rejected)))

    in_layout = os.path.join(iter_dir, "input", "%s.py" % case)
    golden_conn = golden_conn_path
    with open(in_layout, "r", encoding="utf-8") as fh:
        input_text = fh.read()

    before_cache = {}
    leaf_cache = {}

    def _before(w):
        key = _win_key(w)
        if key not in before_cache:
            before_cache[key] = _crop_count(
                _win_leaf(ctx, unions_map, w, leaf_cache), ctx)
        return before_cache[key]

    # One tournament per conflict component: candidates sharing any target,
    # pooled or regional, compete for a single winner.
    for comp in _components(pool):
        comp_id = ",".join(sorted({t for c in comp for t in c["target_keys"]}))
        wins = _component_windows(ctx, units, comp, leaf_cache)
        if not wins:
            _log("component %s: no coverage windows -- rejecting all by "
                 "policy" % comp_id)
        # prime the before-cache in parallel
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
            list(ex.map(_before, wins))

        scored = []
        for cand in comp:
            snap = copy.deepcopy(geom)
            try:
                anchor = _win_leaf(ctx, unions_map, wins[0], leaf_cache) \
                if wins else None
                # The whole group is applied atomically, regional members
                # included.
                _apply_ops_to_geom(ctx, anchor, cand["ops"])
                with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
                    afters = list(ex.map(
                        lambda w: _crop_count(
                            _win_leaf(ctx, unions_map, w, leaf_cache),
                            ctx), wins))
            finally:
                ctx.geometry_model = snap
                geom = ctx.geometry_model
            per_win = []
            delta = 0
            for w, a in zip(wins, afters):
                b = before_cache[_win_key(w)]
                per_win.append({"window": _win_key(w), "before": b,
                                "after": a, "delta": a - b})
                delta += a - b
            # Full-design connectivity from a text-level apply of the whole
            # op list on its own.
            conn_ok = False
            # Initialised outside the try so the finally clause always sees it.
            tmp = None
            try:
                patch = parse_patch_from_file_text(
                    json.dumps({"leaf_id": "cu_pool", "ops": cand["ops"],
                                "explanation": "cu"}), "cu_pool")
                txt = apply_patch_to_text(input_text, patch, anchor)
                tmp = os.path.join(work_dir, "_cu_tmp_%s.py"
                                   % _sha1_12(_canon_content(cand["ops"])))
                with open(tmp, "w", encoding="utf-8") as fh:
                    fh.write(txt)
                conn_ok = bool(is_connectivity_preserved(
                    golden_conn, tmp, "block"))
            except Exception as exc:  # noqa: BLE001
                _log("cu_scratch_or_conn_failed: conn check failed for "
                     "%s: %r -> treated broken" % (comp_id, exc))
            finally:
                # Removal has to happen here rather than after the
                # connectivity call: if that call raises, the scratch file
                # would otherwise survive into the persisted iteration record.
                if tmp and os.path.isfile(tmp):
                    try:
                        os.remove(tmp)
                    except OSError:
                        pass
            scored.append({"target": (cand["target_keys"] or [None])[0],
                           "target_keys": cand["target_keys"],
                           "conflict_keys": cand["conflict_keys"],
                           "group": cand["group"],
                           "atomic": cand["group"] is not None,
                           "ops": cand["ops"],
                           "proposers": cand["proposers"],
                           "windows": per_win, "delta_total": delta,
                           "conn_preserved": conn_ok})
            _log("candidate %s (by %s): delta_total=%+d conn=%s over %d "
                 "windows" % (scored[-1]["target"],
                              ",".join(cand["proposers"]), delta,
                              conn_ok, len(per_win)))

        _le0 = os.environ.get("CU_DELTA_LE0", "") == "1"
        ok = [s for s in scored
              if (s["delta_total"] <= 0 if _le0 else s["delta_total"] < 0)
              and s["conn_preserved"]]
        if ok:
            best = sorted(ok, key=lambda s: (s["delta_total"],
                                             s["proposers"][0],
                                             _canon_content(s["ops"])))[0]
            best["decision"] = "applied"
            winners.append({"target": best["target"],
                            "target_keys": best["target_keys"],
                            "ops": best["ops"],
                            "attributed_to": best["proposers"][0]})
            for s in scored:
                if s is not best:
                    s["decision"] = "lost_tournament"
        else:
            for s in scored:
                s["decision"] = ("rejected_net_positive"
                                 if not s["conn_preserved"]
                                 or s["delta_total"] >= 0 else "rejected")
        verdicts.extend(scored)

    out = {"strip": dict((u, sorted(s)) for u, s in strip.items()),
           "winners": winners, "verdicts": verdicts}
    _write_verdicts(iter_dir, out)
    _log("pool done: %d winner(s), %d verdict(s) -> cu_verdicts.json"
         % (len(winners), len(verdicts)))
    return out
