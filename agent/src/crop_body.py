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

"""Renderer for the crop body: the runnable KLayout snippet a repair agent edits.

Given one leaf and the case context, this builds the lines inside the ``python``
fence of a crop prompt -- a units line, a runnable preamble, a layer band
banner, an optional via-cell catalog, then four sections: via instances the crop
owns (A), read-only background (B), partially editable stripes (C) and fully
editable polygons (D). Three prompt-only sections built here reuse the same
editability classification, so the prompt and the crop can never disagree about
what may be edited. The snippet is display only; edits reach the real layout
through the ``# polygon_id:`` and ``# instance_id:`` anchors.
"""


import os
import re

from typing import Dict, List, Optional, Tuple  # noqa: F401

from .model import instance_block_bbox_dbu, instance_block_polys
from .types import (CaseContext, LAYER_NUM_TO_NAME, Leaf, Polygon,
                    SubcellInstance, Violation)  # noqa: F401
from .clips import _SEED_EXCLUDE_LAYERS
from .subcell_protection import detect_subcell_kind, allowed_ops_for


def _via_edit_enabled():
    """Whether via cell internals may be edited (VIA_STRUCT_EDIT, default on).

    Read at call time so both the container environment and host-side toggling
    take effect. When it is off, via internals are shown frozen and only
    whole-instance move and delete remain available."""
    return os.environ.get("VIA_STRUCT_EDIT", "1") == "1"


def _via_add_enabled():
    """Whether the add_via catalog is rendered (VIA_ADD, default on).

    Read at call time, like _via_edit_enabled but independent of it. When it is
    off the catalog is omitted, the grammar drops add_via, and the validator
    rejects the operation as well."""
    return os.environ.get("VIA_ADD", "1") == "1"


# GDS layer numbers, with V0=18 as the std-cell device via floor. Note that the
# numbering is not monotone with the physical stack: M2=20 sits below V1=21.
_GDS_BY_LAYER = {
    "V0": 18, "M1": 19, "V1": 21, "M2": 20, "V2": 25, "M3": 30, "V3": 35,
    "M4": 40, "V4": 45, "M5": 50, "V5": 55, "M6": 60, "V6": 65,
    "M7": 70, "V7": 75, "M8": 80, "V8": 85, "M9": 90, "V9": 95,
}
GDS_M1 = 19   # retained for callers outside this module
GDS_V0 = 18

# Cap on the read-only context tail (B-section neighbours, distance-ordered).
MAX_CONTEXT_STAMPS = 12

# The units line. It must be the first body line, ahead of the runnable
# preamble. Non-ASCII characters used: U+2192 arrow, U+00B5 micro, U+2260 not
# equal, U+00D7 multiplication sign.
UNITS_LINE = ("# Units: coords are dbu; layout.dbu=0.00025µm → "
              "1 dbu = 0.25 nm, 1 nm = 4 dbu. DRC rules are in nm "
              "(deck≠crop units); multiply nm×4 to compare in dbu.")

# Bridge ownership mode: "owner" gives each bridge polygon a single owning leaf.
BRIDGE_MODE = "owner"


# ---------------------------------------------------------------------------
# Pure helpers, duplicated from prompt_format to avoid a circular import
# ---------------------------------------------------------------------------

def _resolve_top_cell_var(ctx):
    """Pick the variable name for the top cell in the emitted snippet."""
    geom = getattr(ctx, "geometry_model", None)
    if geom is not None:
        tcv = getattr(geom, "top_cell_var", None)
        if tcv:
            return tcv
    case_info = getattr(ctx, "case_info", None)
    case_name = getattr(case_info, "case_name", "") if case_info else ""
    if case_name:
        return "cell_{0}".format(case_name)
    return "cell_top"


def _points_for(poly):
    """Return the list of (x, y) tuples used to construct the pya.Polygon.

    Falls back to a 4-corner bbox polygon when ``points_dbu`` is empty or
    degenerate (length < 3).
    """
    pts = tuple(poly.points_dbu) if poly.points_dbu else ()
    if len(pts) < 3:
        x1, y1, x2, y2 = poly.bbox_dbu
        return [(x1, y1), (x1, y2), (x2, y2), (x2, y1)]
    return [(int(x), int(y)) for (x, y) in pts]


def _format_points(pts):
    return ", ".join("pya.Point({0}, {1})".format(x, y) for (x, y) in pts)


def _clip_pts_to_bbox(pts, bbox):
    """Clamp every vertex of ``pts`` into ``bbox``.

    Only the C and D top-level polygons are clipped this way. B is shown whole
    and A1 is in cell-local coordinates, so neither calls this."""
    x1, y1, x2, y2 = bbox
    out = []
    for (x, y) in pts:
        cx = x1 if x < x1 else (x2 if x > x2 else x)
        cy = y1 if y < y1 else (y2 if y > y2 else y)
        out.append((int(cx), int(cy)))
    return out


def _polygon_area(pts):
    """Shoelace area (>=0) of a closed point ring; 0 for degenerate (<3 pts)."""
    if len(pts) < 3:
        return 0
    a = 0
    n = len(pts)
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        a += x1 * y2 - x2 * y1
    return abs(a) / 2.0


def clipped_is_degenerate(poly, bbox):
    """True when ``poly`` clipped to ``bbox`` has zero area, meaning it would
    render as a degenerate pya.Polygon. ``poly`` is a types.Polygon."""
    return _polygon_area(_clip_pts_to_bbox(_points_for(poly), bbox)) <= 0


def poly_is_real_lever(poly, leaf_bbox):
    """True when ``poly`` is a usable editable lever inside ``leaf_bbox``.

    It must overlap the bbox inclusively and its clip into the bbox must have
    positive area. Positive area already implies inclusive overlap for
    axis-aligned bboxes; the explicit overlap test only makes the definition
    plain. A polygon that merely touches the boundary has zero clipped area and
    is rejected by the area term."""
    if poly is None:
        return False
    bx1, by1, bx2, by2 = poly.bbox_dbu
    lx1, ly1, lx2, ly2 = leaf_bbox
    if not (bx1 <= lx2 and lx1 <= bx2 and by1 <= ly2 and ly1 <= by2):
        return False
    return not clipped_is_degenerate(poly, leaf_bbox)


# ---------------------------------------------------------------------------
# Distance helper (for clearance advisory ordering)
# ---------------------------------------------------------------------------

def _bbox_dist(a, b):
    """Manhattan gap between two bboxes; 0 if they intersect."""
    dx = 0
    if a[2] < b[0]:
        dx = b[0] - a[2]
    elif b[2] < a[0]:
        dx = a[0] - b[2]
    dy = 0
    if a[3] < b[1]:
        dy = b[1] - a[3]
    elif b[3] < a[1]:
        dy = a[1] - b[3]
    return dx + dy


def _nearest_viol_dist(bbox, viol_bboxes):
    if not viol_bboxes:
        return 0
    return min(_bbox_dist(bbox, vb) for vb in viol_bboxes)


def _nearest_clearance(pid, polys, leaf):
    """Advisory: the smallest gap from ``pid`` to a read-only or band-background
    neighbour. Returns (neighbor_pid, neighbor_layer, gap_dbu) or None."""
    src = polys.get(pid)
    if src is None:
        return None
    cands = list(getattr(leaf, "ro_neighbor_ids", []) or []) \
        + list(getattr(leaf, "band_background", []) or [])
    best = None
    for opid in cands:
        op = polys.get(opid)
        if op is None:
            continue
        gap = _bbox_dist(src.bbox_dbu, op.bbox_dbu)
        if best is None or gap < best[2]:
            best = (opid, op.layer_name, gap)
    return best


def _emit_instance_insert(inst, top_cell_var):
    """Emit the runnable A2 insert line, using the instance's real rotation and
    mirror flags."""
    origin = inst.origin_dbu if inst.origin_dbu else (0, 0)
    ox, oy = int(origin[0]), int(origin[1])
    return ("{0}.insert(pya.CellInstArray(cell_{1}.cell_index(), "
            "pya.Trans({2}, {3}, pya.Vector({4}, {5}))))".format(
                top_cell_var, inst.cell_name, inst.rot_code,
                inst.mirror, ox, oy))


def _layer_name_for_gds(lyr):
    """Map a GDS number to a friendly layer name; 18 is V0."""
    lname = LAYER_NUM_TO_NAME.get(lyr)
    if lname is None:
        if lyr == 18:
            return "V0"
        return "L{0}".format(lyr)
    return lname


# ---------------------------------------------------------------------------
# Deterministic sort and grouping helpers
#
# Every ordering below uses explicit numeric keys with an id string as the final
# tie-break, and materializes intermediate sets with sorted(), so the emitted
# prompt is byte-stable from run to run.
# ---------------------------------------------------------------------------

_METAL_RE = re.compile(r"^M(\d+)$")
_VIA_RE = re.compile(r"^V(\d+)$")
_SENTINEL_RANK = 10 ** 6      # sorts last: unknown layer, std-cell, no metal
_NO_METAL_RULE = 99           # a rule_id with no Mk token sorts last


def _rule_lowest_metal(rule_id):
    """Return the lowest metal number named in a DRC rule id.

    The dotted rule id is split into tokens; every token matching ``M<k>``
    contributes k and the minimum is returned. Via tokens (``V<k>``) are not
    metals and are ignored. When no metal token is present a large sentinel is
    returned so the violation sorts last. Examples: ``V0.M1.AUX.3`` -> 1,
    ``M1.S.2`` -> 1, ``V1.M1.EN.1`` -> 1, ``V2.M3.AUX.2`` -> 3,
    ``M4.AUX.1`` -> 4, ``V4.M5.AUX.2`` -> 5."""
    best = None
    for tok in str(rule_id or "").split("."):
        m = _METAL_RE.match(tok)
        if m:
            k = int(m.group(1))
            if best is None or k < best:
                best = k
    return best if best is not None else _NO_METAL_RULE


def _layer_rank(layer_name):
    """Return a physical-stack rank for a layer name, monotone bottom to top.

    ``M<k>`` maps to 2k-1 and ``V<k>`` to 2k, giving V0=0, M1=1, V1=2, M2=3,
    V2=4, M3=5 and so on, so metals and vias interleave in stack order even
    though the GDS numbers do not (M2=20 < V1=21). For pure metals this is
    order-equivalent to ranking M1..M6 as 1..6. An unknown layer gets a large
    sentinel."""
    if not layer_name:
        return _SENTINEL_RANK
    m = _METAL_RE.match(layer_name)
    if m:
        return 2 * int(m.group(1)) - 1
    m = _VIA_RE.match(layer_name)
    if m:
        return 2 * int(m.group(1))
    return _SENTINEL_RANK


def _lower_metal_rank_from_gds(gds_iter):
    """Lowest _layer_rank over the metal (M*) GDS layers in ``gds_iter``, or the
    sentinel when none of them is a metal. Shared by the two via helpers."""
    best = None
    for lyr in gds_iter:
        name = _layer_name_for_gds(lyr)
        if _METAL_RE.match(name):
            r = _layer_rank(name)
            if best is None or r < best:
                best = r
    return best if best is not None else _SENTINEL_RANK


def _via_lower_metal_rank(inst, cell_defs):
    """Stack rank of a via instance's lower metal land, read from its per-layer
    world lands. VIA_VIA12 -> M1 -> 1, VIA_VIA23 -> M2 -> 3, VIA_VIA34 -> M3 ->
    5, VIA_VIA45 -> M4 -> 7. Returns the sentinel when there is no metal land."""
    if inst is None:
        return _SENTINEL_RANK
    return _lower_metal_rank_from_gds(
        lyr for (lyr, _w, _c) in instance_block_polys(inst, cell_defs))


def _celldef_lower_metal_rank(cdef):
    """Same as _via_lower_metal_rank, but read from a via cell definition's
    cell-local shapes. Used to order via cell types within section A."""
    if cdef is None:
        return _SENTINEL_RANK
    return _lower_metal_rank_from_gds(lyr for (lyr, _p, _c) in cdef.shapes)


def _median(vals):
    """Median of a list of numbers, averaging the two middle values when the
    length is even. Returns 0 for an empty list."""
    s = sorted(vals)
    n = len(s)
    if n == 0:
        return 0
    mid = n // 2
    if n % 2 == 1:
        return s[mid]
    return (s[mid - 1] + s[mid]) / 2.0


def _via_size_thresholds(leaf, geom):
    """Per-axis median via-cell extent over the unique via cells this crop's
    subcell instances reference.

    The median rather than the maximum, because one wide PDN power-strap via
    would otherwise make every violation count as via-sized and collapse the
    grouping. Returns (via_w, via_h), or (0, 0) when the crop has no via cell,
    in which case nothing is via-sized and every violation stands alone."""
    cell_defs = geom.cell_defs or {}
    insts = geom.instances or {}
    seen = set()
    ws = []
    hs = []
    for iid in getattr(leaf, "subcell_instances", []) or []:
        inst = insts.get(iid)
        if inst is None or getattr(inst, "kind", "") != "via":
            continue
        cn = inst.cell_name
        if cn in seen:
            continue
        seen.add(cn)
        cdef = cell_defs.get(cn)
        if cdef is None:
            continue
        ext = getattr(cdef, "extent_dbu", (0, 0)) or (0, 0)
        if ext[0] > 0 and ext[1] > 0:
            ws.append(ext[0])
            hs.append(ext[1])
    if not ws:
        return (0, 0)
    return (_median(ws), _median(hs))


def _pdn_strips(leaf, geom):
    """The editable M5/M6 straps of a PDN leaf, each with its orientation,
    cross-axis match interval and anchor.

    A strap is vertical, meaning it runs in y, when it is taller than it is
    wide. A group matches a vertical strap by its centre x against [x1, x2] and
    a horizontal strap by its centre y against [y1, y2]. Sorted by
    (anchor_x, anchor_y, pid) so strip indices are stable. Returns [] when the
    leaf has no editable M5/M6 polygon, which makes the caller fall back to via
    groups."""
    polys = geom.polygons or {}
    strips = []
    for pid in getattr(leaf, "editable_polygons", []) or []:
        poly = polys.get(pid)
        if poly is None or poly.layer_name not in ("M5", "M6"):
            continue
        x1, y1, x2, y2 = poly.bbox_dbu
        vertical = (x2 - x1) < (y2 - y1)
        if vertical:
            lo, hi = x1, x2
        else:
            lo, hi = y1, y2
        strips.append({"pid": pid, "vertical": vertical, "lo": lo, "hi": hi,
                       "anchor": (x1, y1)})
    strips.sort(key=lambda s: (s["anchor"][0], s["anchor"][1], s["pid"]))
    return strips


def _assign_group_to_strip(group, meta, strips):
    """Index of the strip whose cross-axis match interval contains the group's
    mean centre, or failing that the nearest one by interval distance. Ties
    break on the smaller strip lower bound, then the strip index. ``strips`` is
    assumed non-empty."""
    n = float(len(group))
    mcx = sum(meta[vid][1] for vid in group) / n
    mcy = sum(meta[vid][2] for vid in group) / n
    best = None
    for si, s in enumerate(strips):
        val = mcx if s["vertical"] else mcy
        lo, hi = s["lo"], s["hi"]
        if lo <= val <= hi:
            dist = 0
        elif val < lo:
            dist = lo - val
        else:
            dist = val - hi
        key = (dist, s["lo"], si)
        if best is None or key < best[0]:
            best = (key, si)
    return best[1]


def _ordered_violations(leaf, ctx):
    """The single source of truth for the violation order, shared by the
    "violations to fix" list and the per-violation object list.

    Returns the leaf's violation ids reordered:

      * the per-violation key is (lowest_metal(rule), cx, cy, vid);
      * via groups are the connected components of via-sized violations whose
        DRC bboxes overlap inclusively; a violation that is not via-sized, or
        that is isolated, forms its own group, and inside a group the
        per-violation key applies;
      * a PDN leaf with an editable M5/M6 strap adds an outer strip level
        (strip -> via group -> violation); each group nests under the strip
        nearest its mean centre, and both the strips and the groups within a
        strip are ordered by (min lowest_metal, min cx, min cy);
      * every other leaf uses via groups alone, ordered by that same group key;
      * violation ids that do not resolve to a Violation are appended last, in
        their original order.
    """
    geom = getattr(ctx, "geometry_model", None)
    viol_ids = list(getattr(leaf, "violations", []) or [])
    if geom is None or not viol_ids:
        return viol_ids
    viol_by_id = {v.violation_id: v for v in (ctx.violations or [])}
    resolved = []
    missing = []
    for vid in viol_ids:
        v = viol_by_id.get(vid)
        if v is None:
            missing.append(vid)
        else:
            resolved.append((vid, v))
    if not resolved:
        return viol_ids

    meta = {}   # vid -> (metal, cx, cy, w, h, bbox)
    for (vid, v) in resolved:
        bbox = v.bbox_dbu if v.bbox_dbu else (0, 0, 0, 0)
        cx = (bbox[0] + bbox[2]) / 2.0
        cy = (bbox[1] + bbox[3]) / 2.0
        metal = _rule_lowest_metal(getattr(v, "rule_id", ""))
        meta[vid] = (metal, cx, cy, bbox[2] - bbox[0], bbox[3] - bbox[1], bbox)

    via_w, via_h = _via_size_thresholds(leaf, geom)
    thr_w = 3 * via_w / 2.0
    thr_h = 3 * via_h / 2.0

    def _via_sized(vid):
        (_m, _cx, _cy, w, h, _b) = meta[vid]
        return via_w > 0 and via_h > 0 and w <= thr_w and h <= thr_h

    ids = [vid for (vid, _v) in resolved]
    n = len(ids)
    parent = list(range(n))

    def _find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def _union(a, b):
        ra, rb = _find(a), _find(b)
        if ra == rb:
            return
        if ra < rb:
            parent[rb] = ra
        else:
            parent[ra] = rb

    for i in range(n):
        if not _via_sized(ids[i]):
            continue
        for j in range(i + 1, n):
            if not _via_sized(ids[j]):
                continue
            if _bbox_touch_inclusive(meta[ids[i]][5], meta[ids[j]][5]):
                _union(i, j)

    comp = {}
    for i in range(n):
        comp.setdefault(_find(i), []).append(ids[i])

    def _viol_key(vid):
        (metal, cx, cy, _w, _h, _b) = meta[vid]
        return (metal, cx, cy, vid)

    groups = [sorted(members, key=_viol_key) for members in comp.values()]

    def _group_key(g):
        ms = [meta[vid] for vid in g]
        return (min(m[0] for m in ms), min(m[1] for m in ms),
                min(m[2] for m in ms))

    groups.sort(key=_group_key)

    strips = _pdn_strips(leaf, geom) if getattr(leaf, "is_pdn", False) else []
    if not strips:
        out = []
        for g in groups:
            out.extend(g)
        out.extend(missing)
        return out

    strip_groups = dict((si, []) for si in range(len(strips)))
    for g in groups:
        strip_groups[_assign_group_to_strip(g, meta, strips)].append(g)

    def _strip_key(si):
        gs = strip_groups[si]
        if not gs:
            s = strips[si]
            return (_SENTINEL_RANK, s["anchor"][0], s["anchor"][1])
        keys = [_group_key(g) for g in gs]
        return (min(k[0] for k in keys), min(k[1] for k in keys),
                min(k[2] for k in keys))

    out = []
    for si in sorted(range(len(strips)), key=_strip_key):
        for g in sorted(strip_groups[si], key=_group_key):
            out.extend(g)
    out.extend(missing)
    return out


# ---------------------------------------------------------------------------
# The crop body: units line, preamble, layer-band banner, then sections A to D
# ---------------------------------------------------------------------------

def build_body(leaf, ctx):
    """Build the runnable KLayout body -- the lines inside the ```python fence.

    Emitted in order: the units line, the preamble, the band banner, then
    sections A, B(i), B(ii), C and D. Display only; the round trip back to the
    real layout uses the anchors described in the module docstring."""
    geom = getattr(ctx, "geometry_model", None)
    polys = geom.polygons if geom else {}
    insts = geom.instances if geom else {}
    cell_defs = geom.cell_defs if geom else {}
    top = _resolve_top_cell_var(ctx)
    case = top[5:] if top.startswith("cell_") else top

    lines = []

    # (1) units line; it has to be the first body line.
    lines.append(UNITS_LINE)

    # (2) runnable preamble.
    lines.append("layout = pya.Layout()")
    lines.append("layout.dbu = 0.00025")
    lines.append('{0} = layout.create_cell("{1}")'.format(top, case))

    # (3) layer band banner: a header, not one of the sections.
    el = ", ".join(getattr(leaf, "editable_layers", ()) or ()) or "(none)"
    bl = ", ".join(getattr(leaf, "background_layers", ()) or ()) or "(none)"
    lines.append("# === layer band ===")
    lines.append("# editable layers: {0}".format(el))
    lines.append("# background layers: {0} (view-only; do NOT edit)".format(bl))

    # (3b) add_via catalog: a comment-only header, not a section. It lists every
    # via cell definition present in the design that add_via can place in this
    # crop -- kind "via" and every cut layer name inside the editable band,
    # which is exactly the validator's admissibility test, so the catalog and
    # the accept-set cannot disagree. Types with no instance are included on
    # purpose, and each shape is printed with its full point list.
    if _via_add_enabled():
        band_ed = set(getattr(leaf, "editable_layers", ()) or ())
        cat = []
        for cn in sorted(cell_defs, key=lambda c: (
                _celldef_lower_metal_rank(cell_defs.get(c)), c)):
            cdef = cell_defs.get(cn)
            if cdef is None or cdef.kind != "via":
                continue
            cuts = {_layer_name_for_gds(s[0]) for s in cdef.shapes if s[2]}
            if not cuts or not all(
                    re.match(r"^V[1-9]$", c or "") and c in band_ed
                    for c in cuts):
                continue
            n_inst = sum(1 for i in insts.values() if i.cell_name == cn)
            cat.append("# {0} -- cut {1}; {2} instance(s) design-wide".format(
                cn, ",".join(sorted(cuts)), n_inst))
            for (lyr, pts, cut) in cdef.shapes:
                cat.append("#   layer: {0} (GDS {1}) -- {2}: [{3}]".format(
                    _layer_name_for_gds(lyr), lyr,
                    "via cut" if cut else "via land",
                    _format_points([(int(x), int(y)) for (x, y) in pts])))
        if cat:
            lines.append("# --- via cell types placeable with add_via "
                         "(design-present defs; cut layer in this crop's "
                         "editable band) ---")
            lines.extend(cat)

    # Split subcell instances by editability: mobile (allowed_ops non-empty)
    # versus frozen. In single-owner mode, mobile additionally requires that
    # this leaf owns the instance.
    owned = set(getattr(leaf, "owned_instances", ()) or ())
    mobile_ids = []
    frozen_ids = []
    for iid in leaf.subcell_instances:
        inst = insts.get(iid)
        is_mobile = inst is not None and bool(inst.allowed_ops)
        if BRIDGE_MODE == "owner":
            is_mobile = is_mobile and (iid in owned)
        if is_mobile:
            mobile_ids.append(iid)
        else:
            frozen_ids.append(iid)

    partial = getattr(leaf, "long_open_ends", {}) or {}

    # --- A. via instances (this crop OWNS these) ---
    if mobile_ids:
        lines.append("")
        if _via_edit_enabled():
            lines.append("# --- A. via instances (this crop OWNS these). Editable TWO ways:")
            lines.append("#   (1) whole instance -> move_instance / delete_instance;")
            lines.append("#   (2) SHARED via cell structure -> resize_via_shape / move_via_shape on its")
            lines.append("#       internal metal LANDS (M*) and V-CUT (V*). This edits the ONE shared")
            lines.append("#       VIA_* cell definition, so EVERY instance of that via type changes")
            lines.append("#       together (cell name + all placements unchanged). ---")
        else:
            lines.append("# --- A. via instances (this crop OWNS these). Editable as a WHOLE")
            lines.append("#   instance -> move_instance / delete_instance; the via cell INTERNAL")
            lines.append("#   structure (metal lands M*, V-cut V*) is FROZEN. ---")
        # Group mobile instances by cell type, order the types by their lower
        # metal (VIA_VIA12 before VIA_VIA23 and so on), and order each type's
        # instances by (origin_x, origin_y, iid). This keeps the
        # declare-once-then-place structure runnable: every instance of a cell
        # type sits contiguously right after its single A1 declaration.
        a_groups = {}   # cell_name -> [iid, ...]; insertion order, re-sorted
        for iid in mobile_ids:
            inst = insts.get(iid)
            if inst is None:
                continue
            a_groups.setdefault(inst.cell_name, []).append(iid)

        def _a_cell_key(cn):
            return (_celldef_lower_metal_rank(cell_defs.get(cn)), cn)

        def _a_inst_key(iid):
            inst = insts.get(iid)
            origin = inst.origin_dbu if (inst and inst.origin_dbu) else (0, 0)
            return (int(origin[0]), int(origin[1]), iid)

        for cn in sorted(a_groups, key=_a_cell_key):
            cdef = cell_defs.get(cn)
            # A1 structure: declared once per cell type, with every cut shape.
            if cdef is not None:
                if _via_edit_enabled():
                    lines.append("# A1 structure: cell {0} (declared once; all cut "
                                 "shapes shown, never truncated) -- lands/cut EDITABLE "
                                 "via resize_via_shape/move_via_shape (shared cell def; "
                                 "all same-type instances change together)".format(cn))
                else:
                    lines.append("# A1 structure: cell {0} (declared once; all cut "
                                 "shapes shown, never truncated) -- via cell internals "
                                 "are FROZEN (whole-instance move/delete only)".format(cn))
                lines.append('cell_{0} = layout.create_cell("{0}")'.format(cn))
                k = 0
                layer_occ = {}   # per-layer occurrence -> shape_index, in source order
                for (lyr, pts, cut) in cdef.shapes:      # cell-local coords
                    lname = _layer_name_for_gds(lyr)
                    tag = "via cut" if cut else "via land"
                    pid_local = "p{0}".format(k)
                    k += 1
                    sidx = layer_occ.get(lname, 0)
                    layer_occ[lname] = sidx + 1
                    # Shapes are addressed by shape_index in both modes; only
                    # the comment handle differs.
                    if _via_edit_enabled():
                        lines.append(
                            "# layer: {0} (GDS {1}) -- {2} [editable: "
                            "resize_via_shape/move_via_shape  cell_name={3} "
                            "layer_name={0} shape_index={4}]".format(
                                lname, lyr, tag, cn, sidx))
                    else:
                        lines.append(
                            "# layer: {0} (GDS {1}) -- {2} [frozen: via internal "
                            "shape]".format(lname, lyr, tag))
                    lines.append("{0} = pya.Polygon([{1}])".format(
                        pid_local,
                        _format_points([(int(x), int(y)) for (x, y) in pts])))
                    lines.append("cell_{0}.shapes(layout.layer(pya.LayerInfo"
                                 "({1}, 0))).insert({2})".format(
                                     cn, lyr, pid_local))
            # A2 placement: one CellInstArray per instance, with its real anchor.
            for iid in sorted(a_groups[cn], key=_a_inst_key):
                lines.append("# instance_id: {0}".format(iid))
                lines.append(_emit_instance_insert(insts.get(iid), top))

    # --- B. background (read-only; runnable; do NOT edit) ---
    # B is emitted only when there is at least one background item to show.
    band_set = set(getattr(leaf, "editable_layers", ()) or ()) \
        | set(getattr(leaf, "background_layers", ()) or ())
    stdcell_pins = list(getattr(leaf, "stdcell_pin_polys", []) or [])

    # Order B(i) std-cell pins by (metal, min_x, min_y). The _ptemp_ names are
    # throwaway and carry no anchor, so the counter just follows the emission
    # order.
    def _stdpin_key(entry):
        _cell_name, lyr, wpts = entry
        xs = [x for (x, _y) in wpts]
        ys = [y for (_x, y) in wpts]
        return (_layer_rank(_layer_name_for_gds(lyr)),
                min(xs) if xs else 0, min(ys) if ys else 0, _cell_name)
    stdcell_pins.sort(key=_stdpin_key)

    # B(ii) real top-level pids (out-of-band demoted + read-only neighbours).
    bg_real = []
    for pid in (list(getattr(leaf, "band_background", []) or [])
                + list(getattr(leaf, "ro_neighbor_ids", []) or [])):
        if pid not in bg_real:
            bg_real.append(pid)

    # Order B(ii) real background polygons by (metal, x, y).
    def _bg_real_key(pid):
        poly = polys.get(pid)
        if poly is None:
            return (_SENTINEL_RANK, 0, 0, pid)
        return (_layer_rank(poly.layer_name),
                poly.bbox_dbu[0], poly.bbox_dbu[1], pid)
    bg_real.sort(key=_bg_real_key)

    # Decide whether any B content will be emitted; frozen vias may filter out.
    frozen_via_polys = []   # (iid, cell_name, [(gds, lname, wpts), ...])
    for iid in frozen_ids:
        inst = insts.get(iid)
        if inst is None or inst.kind != "via":
            continue
        emitted = []
        for (lyr, wpts, _cut) in instance_block_polys(inst, cell_defs):
            lname = _layer_name_for_gds(lyr)
            if lname not in band_set:
                continue                         # keep only in-band layers
            emitted.append((lyr, lname, wpts))
        if emitted:
            frozen_via_polys.append((iid, inst.cell_name, emitted))

    # Order B(i) frozen vias by (lower metal, min_x, min_y) so they interleave
    # with the std-cell pins by stack position.
    def _fvia_key(entry):
        f_iid, _cell_name, emitted = entry
        xs = [x for (_g, _l, wpts) in emitted for (x, _y) in wpts]
        ys = [y for (_g, _l, wpts) in emitted for (_x, y) in wpts]
        return (_via_lower_metal_rank(insts.get(f_iid), cell_defs),
                min(xs) if xs else 0, min(ys) if ys else 0, f_iid)
    frozen_via_polys.sort(key=_fvia_key)

    has_b = bool(stdcell_pins) or bool(frozen_via_polys) or bool(bg_real)
    if has_b:
        lines.append("")
        lines.append("# --- B. background (read-only; runnable; do NOT edit) ---")

        ptemp_counter = [0]   # running index across the whole leaf

        def _emit_ptemp(world_pts, gds, lname, source):
            idx = ptemp_counter[0]
            ptemp_counter[0] += 1
            name = "_ptemp_{0}".format(idx)
            lines.append("# layer: {0} (GDS {1})  source: {2}".format(
                lname, gds, source))
            lines.append("{0} = pya.Polygon([{1}])".format(
                name,
                _format_points([(int(x), int(y)) for (x, y) in world_pts])))
            lines.append("{0}.shapes(layout.layer(pya.LayerInfo({1}, 0)))"
                         ".insert({2})".format(top, gds, name))
            # Deliberately no "# polygon_id:" anchor, so a patch that targets
            # this shape is a no-op.

        # B(i)-1: std-cell V0/M1 pins. Always background, emitted under a
        # throwaway _ptemp_ name, and the only std-cell geometry in the snippet.
        if stdcell_pins:
            lines.append("# B(i) std-cell V0/M1 pin flattened to world coords "
                         "(ALWAYS background; std-cell internals NEVER disclosed)")
        for (cell_name, lyr, wpts) in stdcell_pins:
            lname = _layer_name_for_gds(lyr)
            _emit_ptemp(wpts, lyr, lname,
                        "std-cell {0} pin (frozen; placement fixed by P&R)"
                        .format(cell_name))

        # B(i)-2: routing vias owned by another leaf, flattened to world
        # coordinates, keeping only the layers inside the band.
        for (iid, cell_name, emitted) in frozen_via_polys:
            for (gds, lname, wpts) in emitted:
                _emit_ptemp(wpts, gds, lname,
                            "via {0} owned by another leaf; view-only here"
                            .format(cell_name))

        # B(ii): real top-level polygons -- out-of-band demoted ones plus
        # read-only neighbours. They keep their real pid so a clearance note can
        # refer to them, and carry no "# editable" marker. Because they do have
        # a real anchor, their read-only status rests entirely on the validator.
        for pid in bg_real:
            poly = polys.get(pid)
            if poly is None:
                continue
            gds = _GDS_BY_LAYER.get(poly.layer_name)
            if gds is None:
                continue
            lines.append("# background (out-of-band / read-only neighbour; "
                         "not editable here)")
            lines.append("# layer: {0}".format(poly.layer_name))
            pts = _points_for(poly)              # full shape, not clipped
            lines.append("{0} = pya.Polygon([{1}])".format(
                pid, _format_points(pts)))
            lines.append("{0}.shapes(layout.layer(pya.LayerInfo({1}, 0)))"
                         ".insert({2})".format(top, gds, pid))

    # Order the C and D top-level polygons by (metal, x, y). Each pid's whole
    # block -- comment, layer, polygon, insert, clearance note -- stays
    # contiguous, so only the pid order changes and the snippet stays runnable,
    # with each declaration still ahead of its single insert.
    def _pid_key(pid):
        poly = polys.get(pid)
        if poly is None:
            return (_SENTINEL_RANK, 0, 0, pid)
        return (_layer_rank(poly.layer_name),
                poly.bbox_dbu[0], poly.bbox_dbu[1], pid)

    # --- C. partially editable (stripe cut at 2um; clipped to crop bbox) ---
    c_pids = sorted((pid for pid in leaf.editable_polygons if pid in partial),
                    key=_pid_key)
    if c_pids:
        lines.append("")
        lines.append("# --- C. partially editable (stripe cut at 2um; clipped to "
                     "crop bbox; per-entry rule: only the marked real end(s) / "
                     "width may change) ---")
        for pid in c_pids:
            poly = polys.get(pid)
            if poly is None:
                continue
            oe = partial[pid]
            axis = oe.get("axis")
            gds = _GDS_BY_LAYER.get(poly.layer_name)
            if gds is None:
                continue
            # Never emit a zero-area degenerate clip. pts is computed before the
            # comment block so a skip leaves no orphan comments behind.
            pts = _clip_pts_to_bbox(_points_for(poly), leaf.bbox_dbu)
            if _polygon_area(pts) <= 0:
                continue
            # The whole comment block is driven by the (open_low, open_high)
            # flag pair.
            ol = bool(oe.get("open_low"))
            oh = bool(oe.get("open_high"))
            if ol and oh:
                # both ends real and inside the crop
                lines.append("# editable (BOTH ENDS, may SHORTEN/ELONGATE either "
                             "end along {0} via resize_end, must NOT cross leaf "
                             "border)".format(axis))
            elif not (ol or oh):
                # neither end is real: width changes only
                lines.append("# editable (WIDTH ONLY: perpendicular resize; "
                             "both ends frozen)")
            else:
                lines.append("# editable (END ONLY, may SHORTEN/ELONGATE the near real "
                             "end along {0} via resize_end, must NOT cross leaf border)"
                             .format(axis))
            lines.append("# polygon_id: {0}".format(pid))   # real anchor
            lines.append("# layer: {0}".format(poly.layer_name))
            if ol and oh:
                lines.append("# both ends real & inside crop (editable via "
                             "resize_end end=low or end=high); no display-cut end")
            elif not (ol or oh):
                lines.append("# both ends display-cut/FROZEN (wire continues past "
                             "the crop on both sides); end-length edits "
                             "unavailable; only perpendicular (width) resize per "
                             "grammar")
            else:
                near = "LOW" if ol else "HIGH"
                far = "HIGH" if ol else "LOW"
                lines.append("# near real end = {0} {1} (inside crop, editable); "
                             "far end = {2} (clipped at crop bbox, FROZEN display-cut, "
                             "not a real edge)".format(near, axis, far))
            lines.append("{0} = pya.Polygon([{1}])".format(
                pid, _format_points(pts)))
            lines.append("{0}.shapes(layout.layer(pya.LayerInfo({1}, 0)))"
                         ".insert({2})".format(top, gds, pid))
            nb = _nearest_clearance(pid, polys, leaf)
            if nb is not None:
                (npid, nlayer, gap) = nb
                lines.append("# min clearance to {0} on {1}: {2} dbu -- keep "
                             ">= rule".format(npid, nlayer, gap))

    # --- D. editable (top-level editable polygons + owned-via connecting
    # metal in [N]+/-1) ---
    d_pids = [pid for pid in leaf.editable_polygons if pid not in partial]
    # A bridge renders as a plain editable polygon, carrying just its layer and
    # polygon id. A bridge with an in-crop open end already carries a
    # long_open_ends record and renders in C only, so the loop below appends to
    # D exactly the bridges C left out. Bridges with no open end were removed
    # from bridge_polygons by longstripe.classify.
    for pid in list(leaf.bridge_polygons):
        if pid not in d_pids and pid not in partial:
            d_pids.append(pid)
    # Bridge pids are appended first, then the combined list is sorted by the
    # same key section C uses.
    d_pids = sorted(d_pids, key=_pid_key)
    if d_pids:
        lines.append("")
        lines.append("# --- D. editable (top-level editable polygons + owned-via "
                     "connecting metal in [N]+/-1) ---")
        for pid in d_pids:
            poly = polys.get(pid)
            if poly is None:
                continue
            gds = _GDS_BY_LAYER.get(poly.layer_name)
            if gds is None:
                continue
            # Never emit a zero-area degenerate clip.
            pts = _clip_pts_to_bbox(_points_for(poly), leaf.bbox_dbu)
            if _polygon_area(pts) <= 0:
                continue
            lines.append("# editable")
            lines.append("# polygon_id: {0}".format(pid))
            lines.append("# layer: {0}".format(poly.layer_name))
            lines.append("{0} = pya.Polygon([{1}])".format(
                pid, _format_points(pts)))
            lines.append("{0}.shapes(layout.layer(pya.LayerInfo({1}, 0)))"
                         ".insert({2})".format(top, gds, pid))
            nb = _nearest_clearance(pid, polys, leaf)
            if nb is not None:
                (npid, nlayer, gap) = nb
                lines.append("# min clearance to {0} on {1}: {2} dbu -- keep "
                             ">= rule".format(npid, nlayer, gap))

    return lines


# ---------------------------------------------------------------------------
# Per-violation highlight section (prompt-only)
# ---------------------------------------------------------------------------

def _bbox_touch_inclusive(a, b):
    """Inclusive bbox touch: a single shared vertex or edge counts."""
    return (a and b and a[0] <= b[2] and b[0] <= a[2]
            and a[1] <= b[3] and b[1] <= a[3])


def _hl_poly_flag(pid, poly, leaf_bbox, editable_ids, bridge_ids, partial):
    """Editability of a top-level polygon, matching what the validator allows
    and how build_body renders it. Tested in order:
      * a polygon whose clip into the crop has zero area is 'frozen', because
        build_body drops it from the snippet. This also catches a degenerate
        polygon that the long-stripe pass recorded in long_open_ends.
      * a polygon in long_open_ends that is editable or a bridge is 'C
        partial-editable' when it has at least one open end, since the validator
        accepts resize_end there, and 'C partial-editable (width only)' when it
        has none, since only a perpendicular resize is accepted.
      * any other editable or bridge polygon is 'D editable'; everything else is
        'frozen'."""
    if poly is not None and not poly_is_real_lever(poly, leaf_bbox):
        return "frozen"                              # degenerate clip
    if pid in partial and (pid in editable_ids or pid in bridge_ids):
        oe = partial.get(pid) or {}
        if oe.get("open_low") or oe.get("open_high"):
            return "C partial-editable"
        return "C partial-editable (width only)"
    if pid in editable_ids or pid in bridge_ids:
        return "D editable"
    return "frozen"


def _hl_inst_flag(iid, inst, owned_ids):
    """Editability of a via or std-cell, using the same mobile/frozen split as
    build_body. Returns (flag, label, sort_order)."""
    try:
        movable = bool(allowed_ops_for(detect_subcell_kind(inst.cell_name)))
    except ValueError:
        movable = False
    kind = getattr(inst, "kind", "?")
    label = "via" if kind == "via" else ("std-cell" if kind == "stdcell" else kind)
    order = 1 if kind == "via" else 2
    if movable:
        if BRIDGE_MODE == "owner" and iid not in owned_ids:
            return "movable via (owned by another leaf)", label, order
        return ("movable, owned" if iid in owned_ids else "movable"), label, order
    return "frozen", label, order


def build_highlight_section(leaf, ctx):
    """Per-violation list of every top-level polygon, via and std-cell whose
    bbox inclusively touches that violation's raw DRC bbox, regardless of
    editability.

    Each item carries its editability from the same classification the crop
    itself uses, so the two cannot disagree. Die boundary layers are excluded.
    Returns '' when the leaf has no violations. Prompt-only: never called from
    build_body, so the crop files written to disk are unaffected."""
    geom = getattr(ctx, "geometry_model", None)
    if geom is None or not getattr(leaf, "violations", None):
        return ""
    polys = geom.polygons
    insts = geom.instances
    cell_defs = geom.cell_defs
    viol_by_id = {v.violation_id: v for v in (ctx.violations or [])}
    partial = getattr(leaf, "long_open_ends", {}) or {}
    edit = set(leaf.editable_polygons or [])
    bridge = set(leaf.bridge_polygons or [])
    own = set(getattr(leaf, "owned_instances", ()) or ())
    lines = [
        "## Objects physically at each violation (bbox touches the violation's DRC bbox)",
        "For EACH violation below: EVERY top-level polygon / via / std-cell whose",
        "bounding box touches that violation's DRC bbox (inclusive -- even one",
        "vertex/edge). Vias / std-cells are listed as WHOLE instances, not inner",
        "shapes. The [flag] is this object's editability in THIS crop, identical to",
        "the Crop above: [C partial-editable] / [D editable] = you MAY edit it (see",
        "that section); [movable...] = you MAY move/delete it, OR resize/move its",
        "lands/cut via resize_via_shape/move_via_shape (section A); [frozen]",
        "= you may NOT. This section grants NO new permissions; it only shows what",
        "geometry is physically at each violation so you do not miss the culprit.",
        "",
    ]
    # Iterate the violations in the shared hierarchical order, the same one the
    # "violations to fix" list uses.
    for vid in _ordered_violations(leaf, ctx):
        v = viol_by_id.get(vid)
        if v is None:
            continue
        rb = v.bbox_dbu
        lines.append("* {0} {1} @ bbox {2}".format(
            vid, getattr(v, "rule_id", "?"), tuple(rb)))
        # Order the objects inside this bullet by (metal, x, y), a via keying on
        # its lower metal and a std-cell on a large sentinel so std-cells sort
        # last. Polygons and vias therefore interleave by stack position.
        items = []
        for pid, p in polys.items():
            if p.layer_name in _SEED_EXCLUDE_LAYERS:
                continue
            if not _bbox_touch_inclusive(p.bbox_dbu, rb):
                continue
            flag = _hl_poly_flag(pid, p, leaf.bbox_dbu, edit, bridge, partial)
            key = (_layer_rank(p.layer_name), p.bbox_dbu[0], p.bbox_dbu[1], pid)
            items.append((key, "  - top-level polygon {0}  layer={1}  bbox={2}  [{3}]"
                          .format(pid, p.layer_name, tuple(p.bbox_dbu), flag)))
        for iid, inst in insts.items():
            ib = instance_block_bbox_dbu(inst, cell_defs)
            if not _bbox_touch_inclusive(ib, rb):
                continue
            flag, label, _order = _hl_inst_flag(iid, inst, own)
            if getattr(inst, "kind", "") == "via":
                rank = _via_lower_metal_rank(inst, cell_defs)
            else:
                rank = _SENTINEL_RANK          # std-cell or unknown sorts last
            key = (rank, ib[0], ib[1], iid)
            items.append((key, "  - {0} {1}  cell={2}  bbox={3}  [{4}]"
                          .format(label, iid, inst.cell_name, tuple(ib), flag)))
        if items:
            for _k, txt in sorted(items, key=lambda x: x[0]):
                lines.append(txt)
        else:
            lines.append("  (no top-level polygon / via / std-cell touches this bbox)")
        lines.append("")
    out = "\n".join(lines)
    # With via structure editing off, the legend drops the via-shape phrasing
    # and offers whole-instance move and delete only.
    if not _via_edit_enabled():
        out = out.replace(
            "you MAY move/delete it, OR resize/move its\n"
            "lands/cut via resize_via_shape/move_via_shape (section A); [frozen]",
            "you MAY move/delete it (whole instance); [frozen]")
    return out


# ---------------------------------------------------------------------------
# Static repair-order-by-DRC-degree section (prompt-only)
# ---------------------------------------------------------------------------

def _via_layer_token(inst, cell_defs):
    """A '+'-joined token of the sorted unique layer names on a via's lands and
    cuts, for example 'M1+M2+V1'. instance_block_polys is used only to read the
    GDS layer numbers. Falls back to 'via' when the cell definition is unknown
    and therefore has no shapes."""
    names = set()
    for (lyr, _wpts, _cut) in instance_block_polys(inst, cell_defs):
        names.add(_layer_name_for_gds(lyr))
    if not names:
        return "via"
    return "+".join(sorted(names))


def build_repair_order_section(leaf, ctx, max_rows=None, max_touch_ids=None):
    """Build the static "Repair order by DRC degree" section.

    Ranks this leaf's editable objects -- the editable top-level polygons in
    sections C and D, plus the movable vias this leaf owns in section A -- by
    DRC degree, the number of the leaf's target violation bboxes the object's
    bbox inclusively touches, using the same touch predicate as
    build_highlight_section. Objects with degree 0 are omitted. Ranked by
    descending degree, then by ascending object id.

    Editability comes from exactly the same gates the highlight section uses:
      * a top-level polygon is kept when _hl_poly_flag starts with 'C ' or
        'D ', so frozen, degenerate and background polygons are excluded;
      * a via or std-cell is kept when _hl_inst_flag reports it movable and this
        leaf owns it.

    Returns '' when there is no geometry model, the leaf has no violations, or
    no object reaches degree 1, so the section appears exactly when there is
    something to order. Prompt-only.

    ``max_rows`` and ``max_touch_ids`` cap the size of the table. Rows are
    ranked first and then truncated to ``max_rows``, followed by a line telling
    the reader how to derive the rest; each row's touched-violation cell is cut
    to ``max_touch_ids`` ids with a '(+N more)' tail. Both default to None,
    meaning no cap.
    """
    geom = getattr(ctx, "geometry_model", None)
    if geom is None or not getattr(leaf, "violations", None):
        return ""
    polys = geom.polygons
    insts = geom.instances
    cell_defs = geom.cell_defs
    viol_by_id = {v.violation_id: v for v in (ctx.violations or [])}
    partial = getattr(leaf, "long_open_ends", {}) or {}
    edit = set(leaf.editable_polygons or [])
    bridge = set(leaf.bridge_polygons or [])
    own = set(getattr(leaf, "owned_instances", ()) or ())

    # This leaf's target violations, resolved as build_highlight_section does.
    targets = []
    for vid in leaf.violations:
        v = viol_by_id.get(vid)
        if v is not None:
            targets.append(v)
    if not targets:
        return ""

    def _degree_for(obj_bbox):
        touched = []
        for v in targets:
            if _bbox_touch_inclusive(obj_bbox, v.bbox_dbu):
                touched.append(v.violation_id)
        return touched

    rows = []
    # 1) editable top-level polygons (C partial-editable / D editable only).
    for pid in sorted(set(edit) | set(bridge)):
        p = polys.get(pid)
        if p is None:
            continue
        if p.layer_name in _SEED_EXCLUDE_LAYERS:
            continue
        flag = _hl_poly_flag(pid, p, leaf.bbox_dbu, edit, bridge, partial)
        if not (flag.startswith("C ") or flag.startswith("D ")):
            continue
        touched = _degree_for(p.bbox_dbu)
        if not touched:
            continue
        rows.append({"id": pid, "layer": p.layer_name, "kind": "polygon",
                     "degree": len(touched), "editability": flag,
                     "touched": touched})
    # 2) movable vias this leaf owns (section A).
    for iid in sorted(insts):
        inst = insts.get(iid)
        if inst is None:
            continue
        flag, _label, _order = _hl_inst_flag(iid, inst, own)
        if not (flag.startswith("movable") and iid in own):
            continue
        ib = instance_block_bbox_dbu(inst, cell_defs)
        touched = _degree_for(ib)
        if not touched:
            continue
        rows.append({"id": iid, "layer": _via_layer_token(inst, cell_defs),
                     "kind": "via", "degree": len(touched),
                     "editability": flag, "touched": touched})

    if not rows:
        return ""
    rows.sort(key=lambda r: (-r["degree"], r["id"]))
    n_truncated = 0
    if max_rows is not None and len(rows) > max_rows:
        n_truncated = len(rows) - max_rows
        rows = rows[:max_rows]

    lines = [
        "## Repair order by DRC degree (STATIC -- computed once; do NOT recompute)",
        "",
        "This fixed order ranks THIS leaf's EDITABLE objects (the editable top-level",
        "polygons in sections C/D above + the movable/owned vias in section A) by DRC",
        "DEGREE = how many of this leaf's TARGET violations the object's bounding box",
        "touches (inclusive -- a shared edge/vertex counts), highest first. Objects that",
        "touch NO target violation are omitted. Editability is identical to the sections",
        "above and to \"Objects physically at each violation\": [C partial-editable] /",
        "[D editable] = you MAY edit it; [movable, owned] = you MAY move/delete it OR",
        "resize/move its lands/cut (resize_via_shape/move_via_shape, section A); anything",
        "else is frozen and only here for context.",
        "",
        "Work the order TOP-DOWN: edit/move/delete the HIGHEST-degree object first. AFTER",
        "each fix, run the DRC-preview tool (## DRC preview below) to refresh which",
        "targets are CLEARED vs REMAINING; then move to the next object DOWN this list.",
        "Introducing a NEW in-window violation mid-way is acceptable ONLY if you clear it",
        "before you finish (the DRC preview's \"new_in_window\" must be empty in your final",
        "check). Do NOT recompute this ranking -- it is fixed for the whole repair.",
        "",
        "| # | object id | layer | kind | degree | editability | touched violation ids |",
        "|---|-----------|-------|------|--------|-------------|-----------------------|",
    ]
    rank = 0
    for r in rows:
        rank += 1
        touched = r["touched"]
        if max_touch_ids is not None and len(touched) > max_touch_ids:
            shown = (", ".join(touched[:max_touch_ids])
                     + " (+{0} more)".format(len(touched) - max_touch_ids))
        else:
            shown = ", ".join(touched)
        lines.append("| {0} | {1} | {2} | {3} | {4} | {5} | {6} |".format(
            rank, r["id"], r["layer"], r["kind"], r["degree"],
            r["editability"], shown))
    if n_truncated:
        _case = getattr(getattr(ctx, "case_info", None), "case_name", "") \
            or "<CASE>"
        lines.append("")
        lines.append("(+{0} more editable objects with degree>=1 -- derive "
                     "from /work/in/{1}.drc.json; ranking rule identical)"
                     .format(n_truncated, _case))
    out = "\n".join(lines)
    # With via structure editing off, the legend drops the via-shape phrasing
    # and offers whole-instance move and delete only.
    if not _via_edit_enabled():
        out = out.replace(
            "you MAY move/delete it OR\n"
            "resize/move its lands/cut (resize_via_shape/move_via_shape, section A); anything",
            "you MAY move/delete it (whole instance); anything")
    return out


# ---------------------------------------------------------------------------
# Whole-block geometry by layer, with leaf-relative editability
# ---------------------------------------------------------------------------

def object_geometries_by_layer(leaf, ctx):
    """Whole-block list of objects with per-layer world rings and leaf-relative
    editability, for the connectivity-impact context writer.

    Returns a list of dicts::

        {"id", "kind", "layers": {layer_name: [ring_as_list_of_[x,y]]},
         "editability": <flag string>}

    Built for the whole block rather than just the leaf, because the
    connectivity-impact tool lists every other object as well. Rings are emitted
    as integer coordinates only, so this module needs no geometry library; the
    caller converts them and performs the overlap test. Editability is
    leaf-relative and uses the same gates as the repair-order and highlight
    sections, so a std-cell reads 'frozen' and a via owned elsewhere reads
    'movable via (owned by another leaf)'. Top-level polygons on a die-boundary
    layer are skipped. Returns [] when there is no geometry model.
    """
    geom = getattr(ctx, "geometry_model", None)
    if geom is None:
        return []
    polys = geom.polygons
    insts = geom.instances
    cell_defs = geom.cell_defs
    partial = getattr(leaf, "long_open_ends", {}) or {}
    edit = set(leaf.editable_polygons or [])
    bridge = set(leaf.bridge_polygons or [])
    own = set(getattr(leaf, "owned_instances", ()) or ())

    out = []
    # Top-level polygons: a single layer, poly.layer_name, and a ring from
    # _points_for, which falls back to the 4-corner bbox when points degenerate.
    for pid in sorted(polys):
        p = polys[pid]
        if p.layer_name in _SEED_EXCLUDE_LAYERS:
            continue
        ring = [[int(x), int(y)] for (x, y) in _points_for(p)]
        flag = _hl_poly_flag(pid, p, leaf.bbox_dbu, edit, bridge, partial)
        out.append({"id": pid, "kind": "polygon",
                    "layers": {p.layer_name: [ring]},
                    "editability": flag})
    # Instances (vias and std-cells): per-layer world rings from
    # instance_block_polys; kind is 'via' for vias, otherwise inst.kind.
    for iid in sorted(insts):
        inst = insts[iid]
        layers = {}
        for (lyr, wpts, _cut) in instance_block_polys(inst, cell_defs):
            lname = _layer_name_for_gds(lyr)
            ring = [[int(x), int(y)] for (x, y) in wpts]
            layers.setdefault(lname, []).append(ring)
        kind = "via" if getattr(inst, "kind", "") == "via" else \
            getattr(inst, "kind", "?")
        flag, _label, _order = _hl_inst_flag(iid, inst, own)
        out.append({"id": iid, "kind": kind, "layers": layers,
                    "editability": flag})
    return out
