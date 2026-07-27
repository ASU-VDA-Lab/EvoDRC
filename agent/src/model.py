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

"""Parse a KLayout layout script and a DRC report into an in-memory model.

Reads the per-case layout script and its ``drc.json``, builds the geometry
model (top-level polygons, subcell instances, per-cell shape definitions) and
the violation list, and stores both on the case context. It also inserts
``# polygon_id:`` and ``# instance_id:`` anchor comments above the insert
lines so later stages can rewrite the layout by text. The module additionally
owns the per-violation crop sizing used when selecting and rendering clips.
"""


import json
import os
import re
from typing import Dict, List, Optional, Tuple

from .logging_setup import get_logger, stage_extra
from .subcell_protection import (allowed_ops_for, detect_subcell_kind,
                                 owner_kind_for)
from .types import (CaseContext, CellDef, GeometryModel, LAYER_NUM_TO_NAME,
                    LAYER_INDEX_MAP, Polygon, SubcellInstance, Violation)


# ---------------------------------------------------------------------------
# Via-cut layers, rule thresholds, and instance transforms
# ---------------------------------------------------------------------------

# GDS cut-layer numbers for V0..V9 in the ASAP7 stack. These are raw GDS layer
# numbers, not the logical indices held in LAYER_INDEX_MAP.
_VIA_CUT_LAYER_NUMS = frozenset((18, 21, 25, 35, 45, 55, 65, 75, 85, 95))


def _is_via_cut_layer(layer_num):
    return layer_num in _VIA_CUT_LAYER_NUMS


# The layout scripts set layout.dbu = 0.00025 um, so 1 nm is 4 database units.
NM_TO_DBU = 4

_RE_RULE_NM = re.compile(r"\bis\s+([0-9]+(?:\s*&\s*[0-9]+)*)\s*nm\b")


def rule_threshold_dbu(description):
    """Conservative inclusion radius in dbu, parsed from a rule description.

    Returns None for rules that state no scalar distance, such as
    width-equality or grid rules. For an asymmetric rule like '5 & 2 nm' the
    larger number wins. The result is a search halo only; the per-side
    constraint a fix has to satisfy comes from the rule text itself.
    """
    if not description:
        return None
    matches = _RE_RULE_NM.findall(description)
    if not matches:
        return None
    last = matches[-1]                     # the last match skips '<= 36 nm' qualifiers
    nums = [int(tok) for tok in re.findall(r"[0-9]+", last)]
    if not nums:
        return None
    return NM_TO_DBU * max(nums)


def _apply_trans(rot, mirror, dx, dy, px, py):
    # Reproduces the transform the benchmark scorer applies, so world
    # coordinates computed here agree with it. The origin (dx, dy) is added
    # inside this function, not at the call site.
    stored_rot = (rot | 4) if mirror else (rot & 3)
    if stored_rot == 0:   rx, ry = px, py
    elif stored_rot == 1: rx, ry = -py, px
    elif stored_rot == 2: rx, ry = -px, -py
    elif stored_rot == 3: rx, ry = py, -px
    elif stored_rot == 4: rx, ry = px, -py
    elif stored_rot == 5: rx, ry = py, px
    elif stored_rot == 6: rx, ry = -px, py
    else:                 rx, ry = -py, -px
    return rx + dx, ry + dy


_FLAT_CACHE = {}


# Ids of the top-level polygons classed as GLOBAL: long straps and rails that
# span the block and bbox-touch many violations at once. Left unclamped such a
# polygon stretches every one of those violations' crops to the strap's full
# extent, giving a set of identical, fully overlapping crops. Its contribution
# is therefore clipped to a local window around each violation, keeping the
# merged crop tight. Clip merging fills this set in; stage_model empties it at
# the start of each case.
_GLOBAL_POLY_IDS = set()


def set_global_poly_ids(ids):
    """Replace the active GLOBAL-polygon id set in place.

    Called by clip merging once it has computed the global polygons, and with
    an empty iterable by stage_model to reset the set per case."""
    _GLOBAL_POLY_IDS.clear()
    _GLOBAL_POLY_IDS.update(ids)


# Ids of the editable top-cell polygons that belong to a promoted power net.
# The power-grid pre-pass publishes them; leaf construction reads them so a
# power-grid polygon is editable only inside its own power crop and never in
# any other leaf. Updated in place, so an imported reference stays valid.
_PDN_EDITABLE_IDS = set()


def set_pdn_editable_pids(ids):
    """Replace the active PDN-editable polygon id set in place.

    Called by the power-grid pre-pass once it has traced the promoted power
    nets, and with an empty iterable by stage_model or when the pre-pass
    degrades."""
    _PDN_EDITABLE_IDS.clear()
    _PDN_EDITABLE_IDS.update(ids)


def is_pdn_editable_pid(pid):
    """True if ``pid`` belongs to a promoted power net, and so has to stay out
    of every non-power leaf's editable set."""
    return pid in _PDN_EDITABLE_IDS


def instance_block_polys(inst, cell_defs):
    """Return one instance's polygons in world coordinates.

    The result is a list of (gds_layer_num, world_points, is_via_cut) tuples
    and callers must treat it as read-only. Results are memoized on the cell
    name, placement and a hash of the cell's shapes, which keeps the cache
    correct across cases; polygon selection flattens every instance once per
    violation, so a large case would otherwise redo millions of transforms."""
    cdef = cell_defs.get(inst.cell_name)
    if cdef is None:
        return []
    origin = inst.origin_dbu if inst.origin_dbu else (0, 0)
    key = (inst.cell_name, origin, inst.rot_code, inst.mirror,
           hash(tuple(cdef.shapes)))
    hit = _FLAT_CACHE.get(key)
    if hit is not None:
        return hit
    ox, oy = origin[0], origin[1]
    out = []
    if inst.rot_code == 0 and not inst.mirror:
        # Identity fast-path, gated on this instance's own placement code, so
        # a rotated or mirrored instance still takes the general path below.
        for (lyr, pts, cut) in cdef.shapes:
            out.append((lyr, tuple((px + ox, py + oy) for (px, py) in pts),
                        cut))
    else:
        for (lyr, pts, cut) in cdef.shapes:
            wpts = tuple(_apply_trans(inst.rot_code, inst.mirror, ox, oy, px, py)
                         for (px, py) in pts)
            out.append((lyr, wpts, cut))
    _FLAT_CACHE[key] = out
    return out


def instance_block_bbox_dbu(inst, cell_defs):
    """World-coordinate bounding box of one instance.

    Falls back to a zero-area box at the instance origin when the cell
    definition is unknown, so callers always get a usable box."""
    polys = instance_block_polys(inst, cell_defs)
    if not polys:
        origin = inst.origin_dbu if inst.origin_dbu else (0, 0)
        ox, oy = origin[0], origin[1]
        return (ox, oy, ox, oy)
    xs = []
    ys = []
    for (_lyr, pts, _cut) in polys:
        for (x, y) in pts:
            xs.append(x)
            ys.append(y)
    return (min(xs), min(ys), max(xs), max(ys))


# ---------------------------------------------------------------------------
# Per-violation crop sizing
# ---------------------------------------------------------------------------

LONGAXIS_CAP_DBU = 8000      # 2 um cap per axis on a single violation's crop
LEAF_SIDE_CAP_DBU = 16000    # 4 um cap per side on a merged crop
# Half-width of the window a GLOBAL polygon's bbox contribution is clipped to
# around the violation. Well under the long-axis cap, so a clamped global
# polygon can never widen a single-violation crop beyond that cap.
_GLOBAL_LOCAL_HALO_DBU = LONGAXIS_CAP_DBU // 4   # = 2000


def _is_routing_via_instance(inst, cell_defs):
    """True if the instance is a routing via on V1..V9.

    Requires the cell to be of via kind and to carry at least one cut shape on
    a V1..V9 cut layer; standard cells and V0 (layer 18) are excluded."""
    if inst is None or getattr(inst, "kind", "") != "via":
        return False
    cdef = cell_defs.get(inst.cell_name)
    if cdef is None:
        return False
    for (lyr, _pts, cut) in cdef.shapes:
        if cut and lyr in _VIA_CUT_LAYER_NUMS and lyr != 18:
            return True
    return False


def _bbox_touch(a, b):
    return a[0] <= b[2] and b[0] <= a[2] and a[1] <= b[3] and b[1] <= a[3]


def _clamp_long_axis(bbox, viol_bbox):
    """Clamp a bbox to LONGAXIS_CAP_DBU on each axis whose span exceeds it.

    The kept window is centred on the violation's midpoint and then slid to lie
    inside the original extent on that axis, so the crop stays over the
    selected polygon while still covering the violation. The result is at most
    the cap wide on both axes by construction."""
    x1, y1, x2, y2 = bbox
    vx1, vy1, vx2, vy2 = viol_bbox
    cap = LONGAXIS_CAP_DBU
    half = cap // 2
    if (x2 - x1) > cap:
        cx = (vx1 + vx2) // 2
        lo, hi = cx - half, cx + half
        if lo < x1:
            lo, hi = x1, x1 + cap
        elif hi > x2:
            lo, hi = x2 - cap, x2
        x1, x2 = lo, hi
    if (y2 - y1) > cap:
        cy = (vy1 + vy2) // 2
        lo, hi = cy - half, cy + half
        if lo < y1:
            lo, hi = y1, y1 + cap
        elif hi > y2:
            lo, hi = y2 - cap, y2
        y1, y2 = lo, hi
    return (x1, y1, x2, y2)


def _select_world_polys_for_violation(viol, polygons, instances, cell_defs):
    """Select the polygons that a violation's crop has to cover.

    Flattens subcell instances and top-level polygons to world coordinates and
    keeps those that sit on one of the rule's layers and whose bbox touches the
    violation bbox. Returns a list of (bbox, layer_name, is_via_member,
    owning_instance_id). The rule's layer set comes from ``layer_band``, which
    is imported inside the function because it depends on nothing here."""
    from . import layer_band
    n_layers = set(layer_band.layers_of_rule(viol.rule_id))
    vb = viol.bbox_dbu
    out = []
    # Local neighbourhood a GLOBAL polygon's contribution is clipped to.
    h = _GLOBAL_LOCAL_HALO_DBU
    win = (vb[0] - h, vb[1] - h, vb[2] + h, vb[3] + h)
    # Top-level polygons are already in world coordinates.
    for pid, poly in polygons.items():
        if poly.layer_name in n_layers and _bbox_touch(poly.bbox_dbu, vb):
            bb = poly.bbox_dbu
            if pid in _GLOBAL_POLY_IDS:
                # A strap or rail contributes only its intersection with the
                # local window. That window contains the violation bbox and the
                # polygon already touches it, so the result is never empty.
                bb = (max(bb[0], win[0]), max(bb[1], win[1]),
                      min(bb[2], win[2]), min(bb[3], win[3]))
            out.append((bb, poly.layer_name, False, None))
    # Subcell instances, flattened to world coordinates.
    for iid, inst in instances.items():
        for (lyr, wpts, _cut) in instance_block_polys(inst, cell_defs):
            lname = LAYER_NUM_TO_NAME.get(lyr)
            if lname is None and lyr == 18:
                lname = "V0"
            if lname in n_layers and wpts:
                xs = [p[0] for p in wpts]
                ys = [p[1] for p in wpts]
                bb = (min(xs), min(ys), max(xs), max(ys))
                if _bbox_touch(bb, vb):
                    is_via = _is_routing_via_instance(inst, cell_defs)
                    out.append((bb, lname, is_via, iid))
    return out


def _via_full_bbox(iid, instances, cell_defs):
    """World bbox of the whole via instance ``iid``, covering all its shapes."""
    inst = instances.get(iid)
    if inst is None:
        return None
    return instance_block_bbox_dbu(inst, cell_defs)


def per_violation_bbox_dbu(viol, polygons, instances, cell_defs):
    """Crop bbox for one violation, before any merging with its neighbours.

    Unions the bboxes of the polygons selected for the violation, grows the
    result to contain any whole routing via involved, and clamps each axis to
    LONGAXIS_CAP_DBU."""
    sel = _select_world_polys_for_violation(viol, polygons, instances, cell_defs)
    if not sel:
        # Nothing selected: fall back to the violation's own bbox.
        return _clamp_long_axis(tuple(viol.bbox_dbu), viol.bbox_dbu)
    xs1 = [s[0][0] for s in sel]
    ys1 = [s[0][1] for s in sel]
    xs2 = [s[0][2] for s in sel]
    ys2 = [s[0][3] for s in sel]
    bbox = (min(xs1), min(ys1), max(xs2), max(ys2))
    # If a routing via took part, grow the box to contain the whole via, so a
    # fix is never shown only part of it.
    for (_bb, _ln, is_via, iid) in sel:
        if is_via and iid is not None:
            full = _via_full_bbox(iid, instances, cell_defs)
            if full is not None:
                bbox = (min(bbox[0], full[0]), min(bbox[1], full[1]),
                        max(bbox[2], full[2]), max(bbox[3], full[3]))
    # Final clamp, applied to the union.
    return _clamp_long_axis(bbox, viol.bbox_dbu)


def clip_bbox_dbu(violation_ids, violations_by_id, polygons, instances,
                  cell_defs):
    """Union of per_violation_bbox_dbu over all violations in a clip.

    The same function backs the crop-size gate, a leaf's own bbox and the bbox
    printed in the prompt header, so all three always agree."""
    boxes = []
    for vid in violation_ids:
        v = violations_by_id.get(vid)
        if v is None:
            continue
        boxes.append(per_violation_bbox_dbu(v, polygons, instances, cell_defs))
    if not boxes:
        return (0, 0, 0, 0)
    return (min(b[0] for b in boxes), min(b[1] for b in boxes),
            max(b[2] for b in boxes), max(b[3] for b in boxes))


# ---------------------------------------------------------------------------
# Layout-script regexes, matched against the source text line by line
# ---------------------------------------------------------------------------

_RE_CREATE_CELL = re.compile(
    r"^\s*(\w+)\s*=\s*layout\.create_cell\(\s*\"([^\"]+)\"\s*\)\s*$")
_RE_POLY = re.compile(
    r"^\s*(p\d+)\s*=\s*pya\.Polygon\(\[(.*?)\]\)\s*$")
_RE_POINT = re.compile(
    r"pya\.Point\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)")
_RE_SHAPE_INSERT = re.compile(
    r"^(\s*)(\w+)\.shapes\(layout\.layer\(pya\.LayerInfo\("
    r"\s*(\d+)\s*,\s*(\d+)\s*\)\)\)\.insert\((\w+)\)\s*$")
_RE_CELL_INST = re.compile(
    r"^(\s*)(\w+)\.insert\(\s*pya\.CellInstArray\(\s*(\w+)\.cell_index\(\)"
    r"\s*,\s*pya\.Trans\(\s*(\d+)\s*,\s*(True|False)\s*,\s*"
    r"pya\.Vector\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)\s*\)\s*\)\s*\)\s*$")

_RE_POLYGON_ANCHOR = re.compile(r"^\s*#\s*polygon_id\s*:")
_RE_INSTANCE_ANCHOR = re.compile(r"^\s*#\s*instance_id\s*:")


# ---------------------------------------------------------------------------
# Frozen-input guard
#
# stage_model annotates the layout script in place, so it must never be handed
# a benchmark input directly: that would permanently add anchor comments to a
# file the benchmark expects to stay unchanged. The controller copies each
# layout into a per-iteration directory before decomposing it, so the guard
# costs nothing in normal operation and turns an accidental in-place write into
# an error raised in the offending caller's frame.
# ---------------------------------------------------------------------------

_FROZEN_COMPONENT = "testcase"


def _frozen_roots():
    """Extra frozen roots, os.pathsep-separated, from EVODRC_FROZEN_ROOTS.

    Returns a tuple of realpath'd absolute directories. Blank entries are
    dropped so a trailing separator is harmless.
    """
    raw = os.environ.get("EVODRC_FROZEN_ROOTS", "") or ""
    roots = []
    for part in raw.split(os.pathsep):
        part = part.strip()
        if not part:
            continue
        roots.append(os.path.realpath(part))
    return tuple(roots)


def _is_under(path, root):
    """True if `path` lies under `root` on a path-component boundary.

    Both arguments must already be resolved with realpath. A plain startswith()
    would match /a/rootery against /a/root, so the separator is joined on first.
    """
    if path == root:
        return True
    return path.startswith(root.rstrip(os.sep) + os.sep)


def is_frozen_layout(path):
    """True if `path` names a frozen benchmark input.

    A path counts as frozen when the resolved path has a component named
    exactly ``testcase``, which is how the benchmark lays its inputs out, or
    when it lies under one of the EVODRC_FROZEN_ROOTS entries.

    The decision is taken on os.path.realpath, so a symlink, a ``..``-laden
    path or a relative path cannot dodge it, and it compares whole path
    components, so a file merely named ``my_testcase_backup.py`` is not frozen.
    """
    if not path:
        return False
    real = os.path.realpath(path)
    parts = real.split(os.sep)
    if _FROZEN_COMPONENT in parts:
        return True
    for root in _frozen_roots():
        if _is_under(real, root):
            return True
    return False


def assert_layout_not_frozen(path, why):
    """Raise RuntimeError if `path` is a frozen benchmark input.

    `why` names the calling context so the message points at the real caller.
    This fails rather than warning or redirecting the write to a copy, because
    a redirect would hide the caller's mistake and would also change the
    layout path recorded verbatim in the context JSON files the model reads.
    """
    if not is_frozen_layout(path):
        return
    raise RuntimeError(
        "{0}: refusing to annotate a FROZEN benchmark input: {1}. "
        "Copy the layout to a writable per-iteration path first (the "
        "controller does this at controller.py:184-188) and decompose the "
        "copy. Set EVODRC_FROZEN_ROOTS to extend the frozen set.".format(
            why, os.path.realpath(path)))


def stage_model(ctx: CaseContext) -> None:
    """Parse the layout script and DRC report into the case context.

    Populates ctx.geometry_model and ctx.violations, writes anchor comments
    back to the layout file when they are missing so patch application can find
    the right line, and loads the skill text when one is configured.
    Annotating a frozen benchmark input raises; see assert_layout_not_frozen.
    """
    log = get_logger()
    log.info("start", extra=stage_extra("S2"))
    _FLAT_CACHE.clear()   # drop instance flattens memoized for the last case
    set_global_poly_ids(())   # reset; clip merging reloads it
    set_pdn_editable_pids(())  # reset; the power-grid pre-pass reloads it
    info = ctx.case_info
    if not info.layout_path or not os.path.isfile(info.layout_path):
        raise FileNotFoundError(
            "layout_path missing: {0}".format(info.layout_path))

    text = _read_text(info.layout_path)
    text = _ensure_anchor_comments(text)
    # Write back so patch application finds the anchors.
    if text != _read_text(info.layout_path):
        # Guard the write, not the read: parsing a frozen layout is harmless,
        # and re-running on an already-annotated copy writes nothing.
        assert_layout_not_frozen(info.layout_path, "model.stage_model")
        _write_text(info.layout_path, text)

    # Pass the per-case top cell name so top-level routing polygons land on
    # the flat polygon map rather than being taken for subcell internals.
    geom = _build_geometry_model(
        text, top_cell_name=getattr(info, "case_name", "") or None)
    ctx.geometry_model = geom
    log.info("parsed layout: polys=%d instances=%d",
             len(geom.polygons), len(geom.instances),
             extra=stage_extra("S2"))

    violations = _parse_drc_violations(info.drc_path)
    ctx.violations = violations
    log.info("parsed drc: violations=%d", len(violations),
             extra=stage_extra("S2"))

    if info.skill_path and os.path.isfile(info.skill_path):
        try:
            with open(info.skill_path, encoding="utf-8") as fh:
                ctx.skill_excerpt = fh.read()
        except OSError:
            ctx.skill_excerpt = ""

    log.info("end", extra=stage_extra("S2"))


# ---------------------------------------------------------------------------
# Anchor emission
# ---------------------------------------------------------------------------

def _ensure_anchor_comments(text: str) -> str:
    """Insert `# polygon_id: <id>` and `# instance_id: <id>` anchor comments.

    One anchor goes above every shapes(...).insert(...) and
    cell.insert(CellInstArray(...)) line that does not already have one.
    """
    lines = text.split("\n")
    out: List[str] = []
    poly_counter = 0
    inst_counter = 0
    prev_line = ""
    for line in lines:
        m_shape = _RE_SHAPE_INSERT.match(line)
        m_inst = _RE_CELL_INST.match(line)
        if m_shape and not _RE_POLYGON_ANCHOR.match(prev_line or ""):
            indent = m_shape.group(1) or ""
            poly_var = m_shape.group(5)
            anchor = "{0}# polygon_id: {1}".format(indent, poly_var)
            out.append(anchor)
            poly_counter += 1
        elif m_inst and not _RE_INSTANCE_ANCHOR.match(prev_line or ""):
            indent = m_inst.group(1) or ""
            inst_counter += 1
            inst_id = "i{0:04d}".format(inst_counter)
            anchor = "{0}# instance_id: {1}".format(indent, inst_id)
            out.append(anchor)
        out.append(line)
        prev_line = line
    return "\n".join(out)


def _read_text(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _write_text(path: str, text: str) -> None:
    tmp = path + ".tmp_anchor"
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(text)
    os.replace(tmp, path)


# ---------------------------------------------------------------------------
# Geometry parse
# ---------------------------------------------------------------------------

def _detect_top_cell_name(var_to_cell):
    # type: (Dict[str, str]) -> Optional[str]
    """Return the layout's top cell name, taken from the `create_cell` table.

    Every subcell name matches either the via pattern (`^VIA_.*`) or the
    standard-cell pattern (`^.*_ASAP7_.*`), so `detect_subcell_kind` succeeds
    on them and raises ``ValueError`` only on the top cell. The top cell is
    therefore the one declared name that `detect_subcell_kind` rejects. Returns
    the first such name, or ``None`` when every declared cell looks like a
    subcell, in which case the caller falls back.
    """
    for cell_name in var_to_cell.values():
        try:
            detect_subcell_kind(cell_name)
        except ValueError:
            return cell_name
    return None


def _build_geometry_model(text, top_cell_name=None):
    # type: (str, Optional[str]) -> GeometryModel
    var_to_cell: Dict[str, str] = {}
    polys_raw: Dict[str, List[Tuple[int, int]]] = {}
    polygons: Dict[str, Polygon] = {}
    instances: Dict[str, SubcellInstance] = {}
    cell_defs: Dict[str, CellDef] = {}
    overall_bounds: Optional[Tuple[int, int, int, int]] = None
    inst_counter = 0

    # Resolve the per-case top cell: prefer the name the caller passed, and
    # otherwise detect it from the parsed create_cell table. It must not be
    # hardcoded, because a wrong top cell classifies every top-level routing
    # polygon as subcell-internal, leaving an empty flat polygon map, no clips
    # and no editable metal.
    top_cell = top_cell_name or None

    lines = text.split("\n")
    for line in lines:
        m = _RE_CREATE_CELL.match(line)
        if m:
            var_to_cell[m.group(1)] = m.group(2)
            continue
        m = _RE_POLY.match(line)
        if m:
            body = m.group(2)
            pts = [(int(px), int(py)) for px, py in _RE_POINT.findall(body)]
            if pts:
                polys_raw[m.group(1)] = pts
            continue
        m = _RE_SHAPE_INSERT.match(line)
        if m:
            cell_var = m.group(2)
            layer_num = int(m.group(3))
            datatype = int(m.group(4))
            poly_var = m.group(5)
            pts = polys_raw.get(poly_var)
            if pts is None:
                continue
            if datatype != 0:
                # Skip non-routing (pins live on datatype 251).
                continue
            # All create_cell lines precede the inserts in a valid KLayout
            # script, so var_to_cell is complete by the time we get here.
            if top_cell is None:
                top_cell = _detect_top_cell_name(var_to_cell)
            cell_name = var_to_cell.get(cell_var, cell_var)
            if cell_name and cell_name != top_cell:
                # Subcell-internal shape: store it per cell type in cell-local
                # coordinates and keep it off the flat top-level map. The only
                # cell receiving top-level inserts is the top cell, so this
                # test separates the two exactly, and a subcell polygon can
                # never seed a clip on its own.
                cdef = cell_defs.get(cell_name)
                if cdef is None:
                    try:
                        ckind = detect_subcell_kind(cell_name)
                    except ValueError:
                        ckind = "stdcell"   # permissive: kind only drives rendering
                    cdef = CellDef(cell_name=cell_name, kind=ckind)
                    cell_defs[cell_name] = cdef
                cdef.shapes.append(
                    (layer_num, tuple(pts), _is_via_cut_layer(layer_num)))
                continue
            layer_name = LAYER_NUM_TO_NAME.get(layer_num)
            if layer_name is None:
                # Unknown layer: keep as-is for context but mark layer_index 0.
                layer_name = "L{0}D{1}".format(layer_num, datatype)
            layer_index = LAYER_INDEX_MAP.get(layer_name, -1)
            xs = [pt[0] for pt in pts]
            ys = [pt[1] for pt in pts]
            bbox = (min(xs), min(ys), max(xs), max(ys))

            owner_kind = "editable"
            if cell_name and cell_name != top_cell:
                try:
                    kind = detect_subcell_kind(cell_name)
                    owner_kind = owner_kind_for(kind)
                except ValueError:
                    # Matches neither subcell pattern; treat it as editable.
                    owner_kind = "editable"

            poly = Polygon(
                polygon_id=poly_var,
                layer_name=layer_name,
                layer_index=layer_index if layer_index >= 0 else 0,
                bbox_dbu=bbox,
                points_dbu=tuple(pts),
                net_id=None,
                owner_kind=owner_kind,
            )
            polygons[poly_var] = poly
            if overall_bounds is None:
                overall_bounds = bbox
            else:
                overall_bounds = (
                    min(overall_bounds[0], bbox[0]),
                    min(overall_bounds[1], bbox[1]),
                    max(overall_bounds[2], bbox[2]),
                    max(overall_bounds[3], bbox[3]),
                )
            continue
        m = _RE_CELL_INST.match(line)
        if m:
            child_var = m.group(3)
            cell_name = var_to_cell.get(child_var, child_var)
            try:
                kind = detect_subcell_kind(cell_name)
            except ValueError:
                # Unknown subcell kind: propagate to the caller.
                raise
            inst_counter += 1
            iid = "i{0:04d}".format(inst_counter)
            dx, dy = int(m.group(6)), int(m.group(7))
            rot_code = int(m.group(4))
            mirror = (m.group(5) == "True")
            inst = SubcellInstance(
                instance_id=iid,
                cell_name=cell_name,
                kind=kind,
                allowed_ops=allowed_ops_for(kind),
                origin_dbu=(dx, dy),
                rot_code=rot_code,
                mirror=mirror,
            )
            instances[iid] = inst
            continue

    # Finalize per-type CellDef metadata (cut count / strap flag / extent).
    for cdef in cell_defs.values():
        cuts = sum(1 for (_lyr, _p, cut) in cdef.shapes if cut)
        cdef.via_cut_count = cuts
        # Gated on via kind: a standard cell can hold dozens of V0 cut-layer
        # shapes and must not be mistaken for a strap.
        cdef.is_strap = (cdef.kind == "via" and cuts >= 4)
        xs = []
        ys = []
        for (_lyr, pts, _cut) in cdef.shapes:
            for (x, y) in pts:
                xs.append(x)
                ys.append(y)
        if xs:
            cdef.extent_dbu = ((max(xs) - min(xs)), (max(ys) - min(ys)))
        else:
            cdef.extent_dbu = (0, 0)

    if overall_bounds is None:
        overall_bounds = (0, 0, 0, 0)
    return GeometryModel(
        polygons=polygons,
        instances=instances,
        block_bounds_dbu=overall_bounds,
        cell_defs=cell_defs,
    )


# ---------------------------------------------------------------------------
# DRC parse
# ---------------------------------------------------------------------------

def _parse_drc_violations(drc_path: str) -> List[Violation]:
    if not drc_path or not os.path.isfile(drc_path):
        return []
    try:
        with open(drc_path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        return []

    rules = data.get("rules") or {}
    out: List[Violation] = []
    idx = 0
    for rule_name, body in rules.items():
        if not isinstance(body, dict):
            continue
        count = int(body.get("violation_count", 0) or 0)
        if count <= 0:
            continue
        viols = body.get("violations") or []
        family = _classify_family(rule_name)
        # Rule-level text, identical for all of this rule's violations; the
        # inclusion radius is parsed out of it.
        desc = str(body.get("description") or "")
        if not isinstance(viols, list):
            continue
        for v in viols:
            idx += 1
            vid = "v{0:04d}".format(idx)
            bbox = _extract_bbox(v)
            if not bbox:
                continue
            involves = tuple(_normalise_involves(v.get("involves")))
            out.append(Violation(
                violation_id=vid,
                rule_id=str(rule_name),
                rule_family=family,
                bbox_dbu=bbox,
                involves=involves,
                description=desc,
            ))
    return out


def _classify_family(rule_name: str) -> str:
    if not rule_name:
        return "unknown"
    parts = str(rule_name).split(".")
    for part in parts:
        p = part.upper()
        if p in ("S", "SPACE", "SPACING"):
            return "spacing"
        if p in ("W", "WIDTH"):
            return "width"
        if p in ("EN", "ENC", "ENCLOSURE"):
            return "enclosure"
        if p in ("A", "AREA"):
            return "area"
        if p == "EOL":
            return "eol"
        if p in ("MIN", "SIZE"):
            return "min_size"
    return "other"


def _extract_bbox(v: dict) -> Optional[Tuple[int, int, int, int]]:
    raw_bbox = v.get("bbox")
    if isinstance(raw_bbox, list) and len(raw_bbox) == 4:
        try:
            return tuple(int(x) for x in raw_bbox)  # type: ignore
        except (TypeError, ValueError):
            return None
    vertices = v.get("vertices") or []
    if isinstance(vertices, list) and vertices:
        try:
            xs = [int(pt[0]) for pt in vertices if len(pt) >= 2]
            ys = [int(pt[1]) for pt in vertices if len(pt) >= 2]
            if xs and ys:
                return (min(xs), min(ys), max(xs), max(ys))
        except (TypeError, IndexError, ValueError):
            return None
    edges = []
    for ek in ("edge1", "edge2"):
        e = v.get(ek)
        if isinstance(e, list):
            edges.extend(e)
    if edges:
        try:
            xs = [int(pt[0]) for pt in edges if len(pt) >= 2]
            ys = [int(pt[1]) for pt in edges if len(pt) >= 2]
            if xs and ys:
                return (min(xs), min(ys), max(xs), max(ys))
        except (TypeError, IndexError, ValueError):
            return None
    return None


def _normalise_involves(field) -> List[str]:
    if not field:
        return []
    if isinstance(field, str):
        return [field]
    if isinstance(field, list):
        out = []
        for item in field:
            if isinstance(item, str):
                out.append(item)
            elif isinstance(item, dict):
                pid = item.get("polygon_id") or item.get("id")
                if pid:
                    out.append(str(pid))
        return out
    return []
