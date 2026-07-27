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

"""Apply an approved patch to the text of a layout script.

A patch is a list of edit operations, and each one is a regex-anchored rewrite
of the script source. Operations find their target through the
`# polygon_id: <id>` and `# instance_id: <id>` anchor comments the model stage
writes above every `.shapes(...).insert(...)` and `.insert(CellInstArray(...))`
line. Everything here takes the script text and returns new text; nothing is
read from or written to disk.
"""


import re
from typing import Any, Dict

from .logging_setup import get_logger, stage_extra
from .types import LAYER_INDEX_MAP, Leaf, Patch


_log = None


def _wlog():
    global _log
    if _log is None:
        _log = get_logger()
    return _log


def _warn_no_anchor(kind, pid):
    """Warn that an op's polygon target could not be located in the text."""
    try:
        _wlog().warning(
            "patch_apply.%s: polygon_id=%s not found; op silently no-op",
            kind, pid, extra=stage_extra("S10"))
    except Exception:
        pass


def _warn_no_inst(kind, iid):
    try:
        _wlog().warning(
            "patch_apply.%s: instance_id=%s not found; op silently no-op",
            kind, iid, extra=stage_extra("S10"))
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Layer name to GDS layer number, for shapes this module creates
# ---------------------------------------------------------------------------
_LAYER_NAME_TO_NUM = {
    "M1": 19, "V1": 21, "M2": 20, "V2": 25, "M3": 30, "V3": 35,
    "M4": 40, "V4": 45, "M5": 50, "V5": 55, "M6": 60, "V6": 65,
    "M7": 70, "V7": 75, "M8": 80, "V8": 85, "M9": 90, "V9": 95,
}


def apply_patch_to_text(layout_text: str, patch: Patch, leaf: Leaf) -> str:
    """Apply one leaf's approved patch to layout_text and return the new text.

    Operations may carry an optional `group` metadata key used elsewhere for
    pooling; it is ignored here, since dispatch reads only the keys that belong
    to each op.
    """
    text = layout_text
    add_counter = [_max_polygon_index(text) + 1]
    for op in patch.ops:
        if not isinstance(op, dict):
            continue
        kind = op.get("op")
        if kind == "resize":
            text = _apply_resize(text, op["polygon_id"],
                                 op.get("axis", "x"),
                                 int(op.get("delta_dbu", 0)))
        elif kind == "move":
            text = _apply_move(text, op["polygon_id"],
                               op.get("axis", "x"),
                               int(op.get("delta_dbu", 0)))
        elif kind == "delete":
            text = _apply_delete(text, op["polygon_id"])
        elif kind == "resize_end":
            text = _apply_resize_end(text, op["polygon_id"],
                                     op.get("axis", "x"),
                                     op.get("end", "low"),
                                     int(op.get("delta_dbu", 0)))
        elif kind == "add_jog":
            text = _apply_add_jog(text, op["polygon_id"], op.get("jog_pts", []))
        elif kind == "add_polygon":
            text = _apply_add_polygon(text, op, add_counter)
        elif kind == "add_via":
            text = _apply_add_via(text, op)
        elif kind == "move_instance":
            iid = op.get("inst_id") or op.get("instance_id")
            text = _apply_move_instance(
                text, iid, op.get("delta_dbu", [0, 0]))
        elif kind == "delete_instance":
            iid = op.get("inst_id") or op.get("instance_id")
            text = _apply_delete_instance(text, iid)
        elif kind in ("resize_via_shape", "move_via_shape"):
            text = _apply_via_shape(text, kind, op)
        else:
            raise ValueError("Unknown op: {0!r}".format(kind))
    return text


# ---------------------------------------------------------------------------
# Anchor helpers
# ---------------------------------------------------------------------------

_RE_POLY_DEF = re.compile(
    r"^(\s*)({pid})\s*=\s*pya\.Polygon\(\[(.*?)\]\)\s*$",
    re.MULTILINE,
)


def _find_polygon_def(text, pid):
    # Returns the match object for polygon `pid`'s definition line, or None.
    pattern = _RE_POLY_DEF.pattern.replace("{pid}", re.escape(pid))
    m = re.search(pattern, text, re.MULTILINE)
    return m


def _resize_points(points: list, axis: str, delta: int) -> list:
    if not points:
        return points
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    half = delta // 2
    rem = delta - half
    out = []
    for (x, y) in points:
        if axis == "x":
            if x <= x_min:
                out.append((x - half, y))
            elif x >= x_max:
                out.append((x + rem, y))
            else:
                out.append((x, y))
        elif axis == "y":
            if y <= y_min:
                out.append((x, y - half))
            elif y >= y_max:
                out.append((x, y + rem))
            else:
                out.append((x, y))
        else:
            out.append((x, y))
    return out


def _move_points(points: list, axis: str, delta: int) -> list:
    if axis == "x":
        return [(x + delta, y) for (x, y) in points]
    if axis == "y":
        return [(x, y + delta) for (x, y) in points]
    return list(points)


def _resize_end_points(points: list, axis: str, end: str, delta: int) -> list:
    """Move only the vertices at one end of an axis, leaving the other end put.

      end='low'  -> vertices whose coord == min move to min - delta
      end='high' -> vertices whose coord == max move to max + delta

    A positive delta therefore pushes that end away from the centre and
    lengthens the shape; a negative delta shortens it.
    """
    if not points:
        return points
    if axis == "x":
        coords = [p[0] for p in points]
    elif axis == "y":
        coords = [p[1] for p in points]
    else:
        return list(points)
    mn, mx = min(coords), max(coords)
    out = []
    for (x, y) in points:
        if axis == "x":
            if end == "low" and x == mn:
                out.append((mn - delta, y))
            elif end == "high" and x == mx:
                out.append((mx + delta, y))
            else:
                out.append((x, y))
        else:  # axis == "y"
            if end == "low" and y == mn:
                out.append((x, mn - delta))
            elif end == "high" and y == mx:
                out.append((x, mx + delta))
            else:
                out.append((x, y))
    return out


def _format_points(points: list) -> str:
    return ", ".join("pya.Point({0}, {1})".format(int(x), int(y))
                     for (x, y) in points)


def _parse_points(body: str) -> list:
    out = []
    for m in re.finditer(r"pya\.Point\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)", body):
        out.append((int(m.group(1)), int(m.group(2))))
    return out


def _replace_polygon_def(text: str, pid: str, new_points: list) -> str:
    match = _find_polygon_def(text, pid)
    if match is None:
        return text
    indent = match.group(1) or ""
    new_body = _format_points(new_points)
    new_line = "{0}{1} = pya.Polygon([{2}])".format(indent, pid, new_body)
    return text[:match.start()] + new_line + text[match.end():]


# ---------------------------------------------------------------------------
# Per-op implementations
# ---------------------------------------------------------------------------

def _apply_resize(text: str, pid: str, axis: str, delta: int) -> str:
    match = _find_polygon_def(text, pid)
    if match is None:
        _warn_no_anchor("resize", pid)
        return text
    pts = _parse_points(match.group(3))
    new_pts = _resize_points(pts, axis, delta)
    return _replace_polygon_def(text, pid, new_pts)


def _apply_move(text: str, pid: str, axis: str, delta: int) -> str:
    match = _find_polygon_def(text, pid)
    if match is None:
        _warn_no_anchor("move", pid)
        return text
    pts = _parse_points(match.group(3))
    new_pts = _move_points(pts, axis, delta)
    return _replace_polygon_def(text, pid, new_pts)


# ---------------------------------------------------------------------------
# Via-internal shape ops (resize_via_shape / move_via_shape)
#
# These edit the shared VIA_* cell definition. The op names a (cell_name,
# layer_name, shape_index) triple, which is resolved back to the real
# `pN = pya.Polygon([...])` variable by scanning the source for the matching
#     cell_<cell>.shapes(layout.layer(pya.LayerInfo(<num>, 0))).insert(pN)
# line and then handed to the ordinary resize/move rewrite, so the definition
# line is edited in place and keeps its anchor comment. Because the shape lives
# in the shared cell definition, the edit reaches every placement of that via
# type; the cell name and the placements themselves are untouched. The
# `\.shapes` right after the escaped cell name pins the match, so VIA_VIA12
# never resolves inside VIA_VIA12_1_3_36_36.
# ---------------------------------------------------------------------------

_RE_VIA_INSERT = (
    r"^\s*cell_{cell}\.shapes\(layout\.layer\(pya\.LayerInfo\("
    r"\s*{num}\s*,\s*0\s*\)\)\)\.insert\(\s*(p\w+)\s*\)\s*$"
)


def _resolve_via_pid(text, cell_name, layer_name, shape_index):
    """Resolve (cell_name, layer_name, shape_index) to a polygon variable name.

    The index is 0-based in source order among the shapes on that layer inside
    the shared VIA_* cell definition. Returns None when the cell, layer or
    index does not exist, and also when the cell is not a VIA_* definition:
    a via op naming a standard cell would otherwise rewrite that cell's frozen
    internals at every placement in the block."""
    if not str(cell_name or "").startswith("VIA_"):
        return None
    num = _LAYER_NAME_TO_NUM.get(str(layer_name))
    if num is None or not cell_name:
        return None
    pat = _RE_VIA_INSERT.format(cell=re.escape(str(cell_name)), num=num)
    matches = list(re.finditer(pat, text, re.MULTILINE))
    try:
        k = int(shape_index or 0)
    except (TypeError, ValueError):
        return None
    if 0 <= k < len(matches):
        return matches[k].group(1)
    return None


def _apply_via_shape(text: str, kind: str, op: dict) -> str:
    """Apply a via-internal resize or move to the shared VIA_* cell definition.

    A target that cannot be resolved leaves the text unchanged; the mount stage
    then sees an unmodified file and records the leaf as a no-op."""
    pid = _resolve_via_pid(text, op.get("cell_name"), op.get("layer_name"),
                           op.get("shape_index", 0))
    if pid is None:
        _warn_no_anchor(kind, op.get("cell_name"))
        return text
    axis = op.get("axis", "x")
    delta = int(op.get("delta_dbu", 0))
    if kind == "resize_via_shape":
        return _apply_resize(text, pid, axis, delta)
    return _apply_move(text, pid, axis, delta)


def _apply_resize_end(text: str, pid: str, axis: str, end: str,
                      delta: int) -> str:
    match = _find_polygon_def(text, pid)
    if match is None:
        _warn_no_anchor("resize_end", pid)
        return text
    pts = _parse_points(match.group(3))
    new_pts = _resize_end_points(pts, axis, end, delta)
    return _replace_polygon_def(text, pid, new_pts)


def _apply_delete(text: str, pid: str) -> str:
    """Comment out a polygon's definition line and its insert line."""
    # Comment out the polygon definition.
    match = _find_polygon_def(text, pid)
    if match is not None:
        deleted = "# DELETED: {0}".format(match.group(0).lstrip())
        text = text[:match.start()] + deleted + text[match.end():]
    # Comment out any shapes(...).insert(<pid>) line.
    insert_re = re.compile(
        r"^(\s*)(\w+)\.shapes\(layout\.layer\(pya\.LayerInfo\("
        r"\s*\d+\s*,\s*\d+\s*\)\)\)\.insert\({0}\)\s*$".format(re.escape(pid)),
        re.MULTILINE,
    )
    text = insert_re.sub(
        lambda m: "{0}# DELETED INSERT: {1}".format(m.group(1), pid),
        text,
    )
    return text


def _apply_add_jog(text: str, pid: str, jog_pts: list) -> str:
    """Append the jog points to the polygon's vertex list."""
    match = _find_polygon_def(text, pid)
    if match is None:
        _warn_no_anchor("add_jog", pid)
        return text
    pts = _parse_points(match.group(3))
    extra = [(int(p[0]), int(p[1])) for p in jog_pts if len(p) >= 2]
    return _replace_polygon_def(text, pid, pts + extra)


def _detect_top_cell_var(text, op):
    """Return the variable name of the top cell to insert new shapes into.

    An explicit `cell_var` on the op wins. Otherwise the top cell is detected
    from the script: it is the one carrying a `<var>.name = "..."` assignment,
    because via and standard-cell subcells never have their name reassigned.
    Failing that, the last `create_cell` variable is used, since the top cell is
    declared after all subcells, and a fixed name is the final fallback."""
    cell_var = op.get("cell_var")
    if not cell_var:
        m_top = re.search(
            r"^\s*(cell_\w+)\s*\.name\s*=", text, re.MULTILINE)
        if m_top:
            cell_var = m_top.group(1)
        else:
            cells = re.findall(
                r"^\s*(cell_\w+)\s*=\s*layout\.create_cell\(", text, re.MULTILINE)
            cell_var = cells[-1] if cells else "cell_Block5"
    return cell_var


def _apply_add_via(text: str, op: dict) -> str:
    """Insert one new instance of a via cell definition the layout declares.

    1. The cell definition must already be declared in the layout text. An
       undeclared cell is warned about and leaves the text byte-identical,
       which the mount stage records as a no-op.
    2. The new instance id is one past the highest `# instance_id: iNNNN`
       anchor, or one past the number of CellInstArray lines when the file
       carries no anchors. The model stage re-anchors it on the next parse.
    3. The block goes in just before `layout.write`, in the byte format the
       instance ops, the connectivity parser and the model stage all read."""
    cn = str(op.get("cell_name") or "")
    org = op.get("origin_dbu") or [op.get("x"), op.get("y")]
    try:
        x, y = int(org[0]), int(org[1])
    except (TypeError, ValueError, IndexError):
        _warn_no_anchor("add_via", cn)
        return text
    if not re.search(
            r'^\s*cell_%s\s*=\s*layout\.create_cell\("%s"\)'
            % (re.escape(cn), re.escape(cn)), text, re.M):
        _warn_no_anchor("add_via", cn)
        return text
    ids = [int(n) for n in re.findall(r"#\s*instance_id\s*:\s*i(\d+)", text)]
    if ids:
        iid = "i%04d" % (max(ids) + 1)
    else:
        iid = "i%04d" % (len(re.findall(r"pya\.CellInstArray\(", text)) + 1)
    top = _detect_top_cell_var(text, op)
    insert_block = (
        "\n# instance_id: {iid}\n"
        "{top}.insert(pya.CellInstArray(cell_{cn}.cell_index(), "
        "pya.Trans(0, False, pya.Vector({x}, {y}))))\n"
    ).format(iid=iid, top=top, cn=cn, x=x, y=y)
    m = re.search(r"^\s*layout\.write\(", text, re.MULTILINE)
    if m is not None:
        return text[:m.start()] + insert_block + text[m.start():]
    return text + insert_block


def _apply_add_polygon(text: str, op: dict, counter_box: list) -> str:
    """Append a new polygon definition and its insert line to the script.

    Both go in just before the final ``layout.write`` line when there is one,
    and at the end of the file otherwise.
    """
    points = op.get("points") or op.get("polygon_points") or []
    layer_name = op.get("layer_name") or op.get("layer")
    layer_num = _LAYER_NAME_TO_NUM.get(str(layer_name))
    if layer_num is None or not points:
        return text
    counter_box[0] += 1
    new_pid = "p{0}".format(counter_box[0])
    pts_text = _format_points([(int(p[0]), int(p[1])) for p in points])
    cell_var = _detect_top_cell_var(text, op)
    insert_block = (
        "\n# polygon_id: {pid}\n"
        "{pid} = pya.Polygon([{pts}])\n"
        "# polygon_id: {pid}\n"
        "{cell}.shapes(layout.layer(pya.LayerInfo({lyr}, 0))).insert({pid})\n"
    ).format(pid=new_pid, pts=pts_text, cell=cell_var, lyr=layer_num)
    # Try to insert before layout.write(...).
    m = re.search(r"^\s*layout\.write\(", text, re.MULTILINE)
    if m is not None:
        return text[:m.start()] + insert_block + text[m.start():]
    return text + insert_block


def _apply_move_instance(text: str, iid: str, delta) -> str:
    if iid is None:
        return text
    dx, dy = int(delta[0]), int(delta[1])
    anchor = re.compile(
        r"^(\s*)#\s*instance_id\s*:\s*{0}\s*$".format(re.escape(iid)),
        re.MULTILINE,
    )
    m = anchor.search(text)
    if m is None:
        _warn_no_inst("move_instance", iid)
        return text
    after = text[m.end():]
    inst_re = re.compile(
        r"(\w+)\.insert\(\s*pya\.CellInstArray\(\s*(\w+)\.cell_index\(\)"
        r"\s*,\s*pya\.Trans\(\s*(\d+)\s*,\s*(True|False)\s*,\s*"
        r"pya\.Vector\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)\s*\)\s*\)\s*\)",
    )
    im = inst_re.search(after)
    if im is None:
        return text
    new_vx = int(im.group(5)) + dx
    new_vy = int(im.group(6)) + dy
    new_call = ("{0}.insert(pya.CellInstArray({1}.cell_index(), "
                "pya.Trans({2}, {3}, pya.Vector({4}, {5}))))").format(
        im.group(1), im.group(2), im.group(3), im.group(4), new_vx, new_vy)
    abs_start = m.end() + im.start()
    abs_end = m.end() + im.end()
    return text[:abs_start] + new_call + text[abs_end:]


def _apply_delete_instance(text: str, iid: str) -> str:
    if iid is None:
        return text
    anchor = re.compile(
        r"^(\s*)#\s*instance_id\s*:\s*{0}\s*$".format(re.escape(iid)),
        re.MULTILINE,
    )
    m = anchor.search(text)
    if m is None:
        _warn_no_inst("delete_instance", iid)
        return text
    after = text[m.end():]
    inst_re = re.compile(
        r"^(\s*)(\w+)\.insert\(\s*pya\.CellInstArray\(.*?\)\)\s*$",
        re.MULTILINE | re.DOTALL,
    )
    im = inst_re.search(after)
    if im is None:
        return text
    abs_start = m.end() + im.start()
    abs_end = m.end() + im.end()
    replacement = "{0}# DELETED INSTANCE: {1}".format(im.group(1), iid)
    return text[:abs_start] + replacement + text[abs_end:]


def _max_polygon_index(text: str) -> int:
    """Largest existing `pNNNN` polygon variable; new shapes are numbered from
    one above it, giving each a fresh name."""
    nums = re.findall(r"\bp(\d+)\s*=\s*pya\.Polygon", text)
    if not nums:
        return -1
    try:
        return max(int(n) for n in nums)
    except (TypeError, ValueError):
        return -1
