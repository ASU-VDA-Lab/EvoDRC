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

"""Checks a model-proposed patch before it is applied to the layout.

A patch is a list of edit operations scoped to a single leaf. The checks run
in order and cover provenance (the patch only touches what the leaf owns),
mount feasibility (a dry application stays on grid and in bounds), a non-empty
result, in-leaf connectivity, minimum spacing, and a stricter routing grid.
All of it is pure Python against a deep copy of the leaf, so no layout tool is
invoked and nothing is written to disk. The first failing check stops the run
and returns a Verdict naming the check and the reason it rejected the patch.
"""


import copy
import os
import re
from typing import Any, Dict, List, Optional, Tuple

from .predicates import MANUFACTURING_GRID_DBU
from .types import CaseContext, Leaf, Patch, Polygon, SubcellInstance, Verdict
from . import crop_body


_POLY_OPS = ("add_polygon", "resize", "move", "delete", "add_jog", "resize_end")
_INST_OPS = ("move_instance", "delete_instance")
# Operations that edit the internals of a via cell definition. Because the
# definition is shared, every instance of that cell type changes together.
_VIA_SHAPE_OPS = ("resize_via_shape", "move_via_shape")


def _via_edit_enabled():
    """Whether editing the internals of a via cell is allowed.

    Controlled by the VIA_STRUCT_EDIT environment variable, enabled by
    default, and read on every call so it can be toggled without a restart.
    """
    return os.environ.get("VIA_STRUCT_EDIT", "1") == "1"


def _via_add_enabled():
    """Whether placing new via instances is allowed.

    Controlled by the VIA_ADD environment variable, enabled by default, and
    read on every call for the same reason as VIA_STRUCT_EDIT.
    """
    return os.environ.get("VIA_ADD", "1") == "1"


from .model import NM_TO_DBU
GRID_24NM_DBU = 24 * NM_TO_DBU              # 96 dbu: the coarse routing pitch
_GRID96_AXIS = {"M4": "y", "M5": "x"}       # the axis that pitch binds per layer


def validate(patch: Patch, leaf: Leaf, ctx: CaseContext) -> Verdict:
    """Run every check against a deep copy of the leaf; first failure wins."""
    leaf_copy = copy.deepcopy(leaf)

    v = _check_provenance(patch, leaf_copy, ctx)
    if not v.ok:
        return v

    v = _check_mount_feasibility(patch, leaf_copy, ctx)
    if not v.ok:
        return v

    v = _check_crop_not_empty(patch, leaf_copy, ctx)
    if not v.ok:
        return v

    v = _check_connectivity_intact(patch, leaf_copy, ctx)
    if not v.ok:
        return v

    v = _check_min_spacing_preserved(patch, leaf_copy, ctx)   # always on
    if not v.ok:
        return v

    v = _check_on_grid_strict(patch, leaf_copy, ctx)          # always on
    if not v.ok:
        return v

    if ctx.via_metal_coupling:                                # opt-in
        v = _check_via_metal_coupling(patch, leaf_copy, ctx)
        if not v.ok:
            return v

    return Verdict(ok=True)


# ---------------------------------------------------------------------------
# Helpers shared across checks
# ---------------------------------------------------------------------------

def _polygons_by_id(ctx: CaseContext) -> Dict[str, Polygon]:
    if ctx.geometry_model is None:
        return {}
    return ctx.geometry_model.polygons


def _instances_by_id(ctx: CaseContext) -> Dict[str, SubcellInstance]:
    if ctx.geometry_model is None:
        return {}
    return ctx.geometry_model.instances


def _bbox_within(child_bbox: Tuple[int, int, int, int],
                 parent_bbox: Tuple[int, int, int, int]) -> bool:
    cx1, cy1, cx2, cy2 = child_bbox
    px1, py1, px2, py2 = parent_bbox
    return (cx1 >= px1 and cy1 >= py1 and cx2 <= px2 and cy2 <= py2)


def _on_grid(value) -> bool:
    """True for an integer coordinate: the manufacturing grid is 1 dbu."""
    if isinstance(value, bool):
        return False
    if not isinstance(value, int):
        return False
    return (value % MANUFACTURING_GRID_DBU) == 0


# ---------------------------------------------------------------------------
# Via placement and standard-cell M1 protection helpers
# ---------------------------------------------------------------------------

def _points_bbox(pts):
    """bbox of an [[x, y], ...] list; None when empty/malformed."""
    xs = []
    ys = []
    for pt in pts or ():
        if not (isinstance(pt, (list, tuple)) and len(pt) == 2):
            return None
        try:
            xs.append(int(pt[0]))
            ys.append(int(pt[1]))
        except (TypeError, ValueError):
            return None
    if not xs:
        return None
    return (min(xs), min(ys), max(xs), max(ys))


def _celldef_world_bbox(cdef, x, y):
    """World bbox covering every shape of a cell def placed at (x, y).

    Assumes no rotation and no mirroring, the only transform a newly placed
    via uses.
    """
    xs = []
    ys = []
    for (_g, pts, _c) in cdef.shapes:
        for (px, py) in pts:
            xs.append(int(px))
            ys.append(int(py))
    if not xs:
        return (x, y, x, y)
    return (min(xs) + x, min(ys) + y, max(xs) + x, max(ys) + y)


def _shape_world_bbox(pts, org):
    """World bbox of one cell-local shape translated by org = (x, y)."""
    xs = [int(px) for (px, _py) in pts]
    ys = [int(py) for (_px, py) in pts]
    return (min(xs) + int(org[0]), min(ys) + int(org[1]),
            max(xs) + int(org[0]), max(ys) + int(org[1]))


def _stdcell_m1_shapes(leaf, ctx):
    """M1 shapes owned by the leaf's standard cells, in world coordinates.

    Returns the individual shapes rather than instance bounding boxes, since a
    cell's own M1 usually covers only part of its footprint.
    """
    from .model import instance_block_polys        # imported here: import cycle
    geom = ctx.geometry_model
    out = []
    if geom is None:
        return out
    for iid in leaf.subcell_instances:
        inst = geom.instances.get(iid)
        if inst is None or inst.kind != "stdcell":
            continue
        for (gds, wpts, _cut) in instance_block_polys(inst, geom.cell_defs):
            if gds == 19:
                out.append(wpts)
    return out


def _overlaps_stdcell_m1(new_bbox, leaf, ctx):
    """True when new_bbox overlaps a standard-cell M1 shape by positive area.

    A bounding-box comparison filters the candidates, then each survivor is
    clipped to the box and its area measured, which is exact for these
    rectilinear pins. Requiring strictly positive area keeps abutment legal:
    tying into a standard-cell pin edge-to-edge is a valid connection, and
    only a real overlap is rejected.
    """
    if new_bbox is None:
        return False
    for wpts in _stdcell_m1_shapes(leaf, ctx):
        xs = [p[0] for p in wpts]
        ys = [p[1] for p in wpts]
        if not xs:
            continue
        if (min(xs) > new_bbox[2] or new_bbox[0] > max(xs)
                or min(ys) > new_bbox[3] or new_bbox[1] > max(ys)):
            continue                                # bbox prefilter miss
        if crop_body._polygon_area(
                crop_body._clip_pts_to_bbox(list(wpts), new_bbox)) > 0:
            return True
    return False


# ---------------------------------------------------------------------------
# Check 1 - Provenance
# ---------------------------------------------------------------------------

def _check_provenance(patch: Patch, leaf: Leaf, ctx: CaseContext) -> Verdict:
    editable_ids = set(leaf.editable_polygons)
    bridge_self_ids = set(leaf.bridge_polygons)
    inst_map = _instances_by_id(ctx)
    leaf_inst_set = set(leaf.subcell_instances)

    for op in patch.ops:
        if not isinstance(op, dict):
            return Verdict(False, "provenance", "op is not a dict")
        kind = op.get("op")
        # Rejected here, ahead of the accept path below, so that with the
        # feature off no edit to a shared cell definition can get through.
        if kind in _VIA_SHAPE_OPS and not _via_edit_enabled():
            return Verdict(False, "provenance",
                           "via-structure editing is DISABLED "
                           "(VIA_STRUCT_EDIT=0); use move_instance/delete_instance")
        if kind == "add_via":
            # Places one instance of a via cell that already exists somewhere
            # in the design. Any integer origin is accepted, provided the whole
            # instance fits inside the leaf and clears standard-cell M1.
            if not _via_add_enabled():
                return Verdict(False, "provenance",
                               "via adding is DISABLED (VIA_ADD=0)")
            cn = op.get("cell_name")
            cdefs = (ctx.geometry_model.cell_defs
                     if ctx.geometry_model is not None else {})
            cdef = cdefs.get(cn)
            if cdef is None or cdef.kind != "via":  # design-present defs only
                return Verdict(False, "provenance",
                               "unknown or non-via cell {0}".format(cn))
            if any(s[0] == 18 for s in cdef.shapes):
                # Layer 18 is standard-cell device geometry; never place it.
                return Verdict(False, "provenance",
                               "via {0} carries V0 device geometry".format(cn))
            cuts = {crop_body._layer_name_for_gds(s[0])
                    for s in cdef.shapes if s[2]}
            band = set(leaf.editable_layers or ())
            if not cuts or not all(re.match(r"^V[1-9]$", c or "") and c in band
                                   for c in cuts):
                return Verdict(False, "provenance",
                               "via {0} cut {1} not a via layer in the leaf "
                               "editable band"
                               .format(cn, sorted(c or "?" for c in cuts)))
            org = op.get("origin_dbu") or [op.get("x"), op.get("y")]
            if (not isinstance(org, (list, tuple)) or len(org) != 2
                    or not all(isinstance(v, int) for v in org)):
                return Verdict(False, "provenance",
                               "add_via origin_dbu must be two ints")
            wb = _celldef_world_bbox(cdef, int(org[0]), int(org[1]))
            if not _bbox_within(wb, leaf.bbox_dbu):
                # The whole instance has to fit inside the leaf's own region.
                return Verdict(False, "provenance",
                               "add_via {0} outside the leaf editable region"
                               .format(cn))
            # Every M1 land of the new via is checked against standard-cell M1.
            for (g, pts, _c) in cdef.shapes:
                if g == 19 and _overlaps_stdcell_m1(
                        _shape_world_bbox(pts, org), leaf, ctx):
                    return Verdict(False, "provenance",
                                   "add_via {0} M1 land overlaps std-cell M1"
                                   .format(cn))
            continue
        if kind == "add_polygon":
            # A new polygon gets a fresh id, so only the leaf has to be editable.
            if not editable_ids and not bridge_self_ids:
                return Verdict(False, "provenance",
                               "leaf has no editable region for add_polygon")
            lname = op.get("layer_name") or op.get("layer")
            if lname == "V0":
                # V0 is standard-cell device geometry. Applying such an op
                # would silently do nothing, so reject it explicitly.
                return Verdict(False, "provenance",
                               "add_polygon on V0 (std-cell device layer) "
                               "is not allowed")
            if lname == "M1":
                # New M1 must not overlap the M1 owned by a standard cell.
                bb = _points_bbox(op.get("points")
                                  or op.get("polygon_points") or [])
                if bb is not None and _overlaps_stdcell_m1(bb, leaf, ctx):
                    return Verdict(False, "provenance",
                                   "add_polygon M1 overlaps std-cell M1")
            continue
        if kind in ("resize", "move", "delete", "add_jog", "resize_end"):
            pid = op.get("polygon_id")
            if pid not in editable_ids and pid not in bridge_self_ids:
                return Verdict(False, "provenance",
                               "polygon_id {0} not in editable/bridge-self".format(pid))
            poly_obj = _polygons_by_id(ctx).get(pid)
            if (poly_obj is not None and leaf.editable_layers
                    and poly_obj.layer_name not in set(leaf.editable_layers)):
                return Verdict(False, "provenance",
                               "polygon {0} layer {1} not in leaf editable band"
                               .format(pid, poly_obj.layer_name))
            # Polygons listed in long_open_ends are stripes that continue past
            # the edge of the crop. If an end is open, resize_end on that end
            # is the only accepted edit; if neither end is open, the stripe may
            # only be resized perpendicular to its long axis.
            partial = getattr(leaf, "long_open_ends", {}) or {}
            if pid in partial:
                oe = partial[pid]
                if not (oe.get("open_low") or oe.get("open_high")):
                    # Both ends are cut off by the crop, so the only edit that
                    # can be judged from inside the crop is a width change.
                    if kind != "resize":
                        return Verdict(False, "provenance",
                                       "WIDTH-ONLY C-section stripe {0} accepts "
                                       "perpendicular resize only".format(pid))
                elif kind != "resize_end":
                    return Verdict(False, "provenance",
                                   "C-section stripe {0} accepts resize_end only"
                                   .format(pid))
                else:
                    end = op.get("end")
                    if end not in ("low", "high"):
                        return Verdict(False, "provenance",
                                       "resize_end end must be low|high")
                    if op.get("axis", "x") != oe.get("axis"):
                        return Verdict(False, "provenance",
                                       "resize_end axis must be stripe long axis")
                    open_ok = oe.get("open_low") if end == "low" else oe.get("open_high")
                    if not open_ok:
                        return Verdict(False, "provenance",
                                       "resize_end on frozen (display-cut) end of {0}"
                                       .format(pid))
            elif kind == "resize_end":
                return Verdict(False, "provenance",
                               "resize_end only valid on a C-section stripe")
            if (kind == "add_jog" and poly_obj is not None
                    and poly_obj.layer_name == "M1"):
                # Jog vertices on an M1 target must not overlap standard-cell
                # M1; abutting it remains legal.
                bb = _points_bbox(op.get("jog_pts") or [])
                if bb is not None and _overlaps_stdcell_m1(bb, leaf, ctx):
                    return Verdict(False, "provenance",
                                   "add_jog M1 overlaps std-cell M1")
            continue
        if kind in ("move_instance", "delete_instance"):
            iid = op.get("inst_id") or op.get("instance_id")
            if iid not in leaf_inst_set:
                return Verdict(False, "provenance",
                               "instance {0} not in leaf".format(iid))
            inst = inst_map.get(iid)
            if inst is None:
                return Verdict(False, "provenance",
                               "unknown inst_id {0}".format(iid))
            if kind not in inst.allowed_ops:
                return Verdict(False, "provenance",
                               "op {0} not in allowed_ops for {1}".format(
                                   kind, inst.cell_name))
            # When leaves are dispatched in parallel, a movable via that
            # several leaves can see has one owning leaf, and only that leaf
            # may move or delete it. In co-edit mode the instance is shared, so
            # every leaf that can see it may move or delete it.
            if crop_body.BRIDGE_MODE == "owner" \
                    and iid not in set(leaf.owned_instances):
                return Verdict(False, "provenance",
                               "instance {0} not owned by this leaf".format(iid))
            continue
        if kind in ("resize_via_shape", "move_via_shape"):
            # Rewrites a via cell definition, which changes every instance of
            # that cell type at once. Allowed only on a via cell this leaf
            # owns a movable instance of.
            cn = op.get("cell_name")
            cdefs = (ctx.geometry_model.cell_defs
                     if ctx.geometry_model is not None else {})
            cdef = cdefs.get(cn)
            if cdef is None:
                return Verdict(False, "provenance",
                               "unknown via cell {0}".format(cn))
            if cdef.kind != "via":
                return Verdict(False, "provenance",
                               "via-shape edit only on via cells (got kind {0} "
                               "for {1})".format(cdef.kind, cn))
            owned_cells = {inst_map[i].cell_name
                           for i in leaf.owned_instances if i in inst_map}
            if cn not in owned_cells:
                return Verdict(False, "provenance",
                               "via {0} not owned/movable in this leaf".format(cn))
            lname = op.get("layer_name")
            if crop_body._GDS_BY_LAYER.get(lname) is None:
                return Verdict(False, "provenance",
                               "unknown layer {0}".format(lname))
            # V0 is the standard-cell device via layer, not a routing via cut
            # or land. Mounting such an op would silently do nothing, so it is
            # rejected here to keep validation, mounting and preview agreeing
            # that V0 is not editable.
            if crop_body._GDS_BY_LAYER.get(lname) == crop_body.GDS_V0:
                return Verdict(False, "provenance",
                               "layer V0 is a std-cell device layer, not a "
                               "routing via cut; not editable via a via-shape op")
            on_layer = [s for s in cdef.shapes
                        if crop_body._layer_name_for_gds(s[0]) == lname]
            if not on_layer:
                return Verdict(False, "provenance",
                               "via {0} has no {1} shape".format(cn, lname))
            si = op.get("shape_index", 0)
            if (not isinstance(si, int) or isinstance(si, bool)
                    or si < 0 or si >= len(on_layer)):
                return Verdict(False, "provenance",
                               "shape_index {0} out of range for {1} {2}".format(
                                   si, cn, lname))
            if op.get("axis") not in ("x", "y"):
                return Verdict(False, "provenance",
                               "axis must be x|y")
            dd = op.get("delta_dbu")
            if not isinstance(dd, int) or isinstance(dd, bool):
                return Verdict(False, "provenance",
                               "delta_dbu must be int")
            continue
        # Anything not handled above, including ops from an older grammar.
        return Verdict(False, "provenance",
                       "unknown or deprecated op {0!r}".format(kind))
    return Verdict(True)


# ---------------------------------------------------------------------------
# Check 2 - Mount feasibility
# ---------------------------------------------------------------------------

def _check_mount_feasibility(patch: Patch, leaf: Leaf,
                             ctx: CaseContext) -> Verdict:
    polys = _clone_leaf_polys(leaf, ctx)
    insts = _clone_leaf_insts(leaf, ctx)
    bounds = leaf.block_bounds_dbu

    for op in patch.ops:
        kind = op.get("op")
        if kind == "resize":
            poly = polys.get(op.get("polygon_id"))
            if poly is None:
                return Verdict(False, "mount_feasibility",
                               "resize target not found")
            delta = op.get("delta_dbu", 0)
            if not _on_grid(delta):
                return Verdict(False, "mount_feasibility",
                               "delta_dbu {0} not on grid".format(delta))
            axis = op.get("axis", "x")
            new_bbox = _apply_resize_bbox(poly.bbox_dbu, axis, delta)
            if not _bbox_within(new_bbox, bounds):
                return Verdict(False, "mount_feasibility",
                               "resize on {0} out of bounds".format(poly.polygon_id))
            poly.bbox_dbu = new_bbox
        elif kind == "move":
            poly = polys.get(op.get("polygon_id"))
            if poly is None:
                return Verdict(False, "mount_feasibility",
                               "move target not found")
            delta = op.get("delta_dbu", 0)
            if not _on_grid(delta):
                return Verdict(False, "mount_feasibility",
                               "delta_dbu {0} not on grid".format(delta))
            axis = op.get("axis", "x")
            new_bbox = _apply_move_bbox(poly.bbox_dbu, axis, delta)
            if not _bbox_within(new_bbox, bounds):
                return Verdict(False, "mount_feasibility",
                               "move on {0} out of bounds".format(poly.polygon_id))
            poly.bbox_dbu = new_bbox
        elif kind == "resize_end":
            poly = polys.get(op.get("polygon_id"))
            if poly is None:
                return Verdict(False, "mount_feasibility",
                               "resize_end target not found")
            delta = op.get("delta_dbu", 0)
            if not _on_grid(delta):
                return Verdict(False, "mount_feasibility",
                               "delta_dbu {0} not on grid".format(delta))
            axis = op.get("axis", "x")
            end = op.get("end", "low")
            new_bbox = _apply_resize_end_bbox(poly.bbox_dbu, axis, end, delta)
            if not (new_bbox[0] <= new_bbox[2] and new_bbox[1] <= new_bbox[3]):
                return Verdict(False, "mount_feasibility",
                               "resize_end on {0} degenerate (over-shorten)"
                               .format(poly.polygon_id))
            if not _bbox_within(new_bbox, bounds):
                return Verdict(False, "mount_feasibility",
                               "resize_end on {0} out of bounds".format(poly.polygon_id))
            poly.bbox_dbu = new_bbox
        elif kind == "delete":
            pid = op.get("polygon_id")
            if pid not in polys:
                return Verdict(False, "mount_feasibility",
                               "delete target {0} not found".format(pid))
            polys.pop(pid, None)
            if pid in leaf.editable_polygons:
                leaf.editable_polygons.remove(pid)
            if pid in leaf.bridge_polygons:
                leaf.bridge_polygons.remove(pid)
        elif kind == "add_jog":
            poly = polys.get(op.get("polygon_id"))
            if poly is None:
                return Verdict(False, "mount_feasibility",
                               "add_jog target not found")
            jog_pts = op.get("jog_pts") or []
            if not isinstance(jog_pts, list) or len(jog_pts) < 1:
                return Verdict(False, "mount_feasibility",
                               "add_jog has no jog points")
            # Each jog point must be on grid and inside bounds.
            for pt in jog_pts:
                if (not isinstance(pt, (list, tuple))) or len(pt) != 2:
                    return Verdict(False, "mount_feasibility",
                                   "add_jog point malformed")
                px, py = pt
                if not (_on_grid(px) and _on_grid(py)):
                    return Verdict(False, "mount_feasibility",
                                   "add_jog point off grid")
                if not (bounds[0] <= px <= bounds[2] and
                        bounds[1] <= py <= bounds[3]):
                    return Verdict(False, "mount_feasibility",
                                   "add_jog point out of bounds")
        elif kind == "add_polygon":
            points = op.get("points") or op.get("polygon_points") or []
            if not isinstance(points, list) or len(points) < 3:
                return Verdict(False, "mount_feasibility",
                               "add_polygon requires >=3 points")
            xs = []
            ys = []
            for pt in points:
                if (not isinstance(pt, (list, tuple))) or len(pt) != 2:
                    return Verdict(False, "mount_feasibility",
                                   "add_polygon point malformed")
                if not (_on_grid(pt[0]) and _on_grid(pt[1])):
                    return Verdict(False, "mount_feasibility",
                                   "add_polygon vertex off grid")
                xs.append(pt[0])
                ys.append(pt[1])
            new_bbox = (min(xs), min(ys), max(xs), max(ys))
            if not _bbox_within(new_bbox, bounds):
                return Verdict(False, "mount_feasibility",
                               "add_polygon out of bounds")
        elif kind == "move_instance":
            iid = op.get("inst_id") or op.get("instance_id")
            inst = insts.get(iid)
            if inst is None:
                return Verdict(False, "mount_feasibility",
                               "move_instance target not found")
            delta = op.get("delta_dbu", [0, 0])
            if not (isinstance(delta, (list, tuple)) and len(delta) == 2):
                return Verdict(False, "mount_feasibility",
                               "move_instance delta_dbu must be [dx, dy]")
            if not (_on_grid(delta[0]) and _on_grid(delta[1])):
                return Verdict(False, "mount_feasibility",
                               "move_instance delta_dbu not on grid")
            new_pos = (inst.origin_dbu[0] + int(delta[0]),
                       inst.origin_dbu[1] + int(delta[1]))
            inst.origin_dbu = new_pos
        elif kind == "delete_instance":
            iid = op.get("inst_id") or op.get("instance_id")
            if iid not in insts:
                return Verdict(False, "mount_feasibility",
                               "delete_instance target not found")
            insts.pop(iid, None)
        elif kind in ("resize_via_shape", "move_via_shape"):
            # Cell-local edit: the delta must be on grid and a resize must not
            # collapse the shape it targets. There is no block-bounds check,
            # because these coordinates are cell-local rather than world.
            delta = op.get("delta_dbu", 0)
            if not _on_grid(delta):
                return Verdict(False, "mount_feasibility",
                               "delta_dbu {0} not on grid".format(delta))
            if kind == "resize_via_shape":
                cdefs = (ctx.geometry_model.cell_defs
                         if ctx.geometry_model is not None else {})
                cdef = cdefs.get(op.get("cell_name"))
                lname = op.get("layer_name")
                si = int(op.get("shape_index", 0) or 0)
                on_layer = ([s for s in cdef.shapes
                             if crop_body._layer_name_for_gds(s[0]) == lname]
                            if cdef is not None else [])
                if 0 <= si < len(on_layer):
                    pts = on_layer[si][1]
                    xs = [p[0] for p in pts]
                    ys = [p[1] for p in pts]
                    bb = (min(xs), min(ys), max(xs), max(ys))
                    nb = _apply_resize_bbox(bb, op.get("axis", "x"), int(delta))
                    if nb[0] >= nb[2] or nb[1] >= nb[3]:
                        return Verdict(False, "mount_feasibility",
                                       "resize_via_shape collapses {0} {1} shape"
                                       .format(op.get("cell_name"), lname))
        elif kind == "add_via":
            # Treated like move_instance: an integer origin whose world bbox
            # lands inside the block. Provenance has already pinned down the
            # cell definition, its cut layer and the leaf window.
            cdefs = (ctx.geometry_model.cell_defs
                     if ctx.geometry_model is not None else {})
            cdef = cdefs.get(op.get("cell_name"))
            if cdef is None:
                return Verdict(False, "mount_feasibility",
                               "add_via cell def not found")
            org = op.get("origin_dbu") or [op.get("x"), op.get("y")]
            if (not isinstance(org, (list, tuple)) or len(org) != 2
                    or not all(isinstance(v, int) for v in org)):
                return Verdict(False, "mount_feasibility",
                               "add_via origin_dbu must be two ints")
            wb = _celldef_world_bbox(cdef, int(org[0]), int(org[1]))
            if not _bbox_within(wb, bounds):
                return Verdict(False, "mount_feasibility",
                               "add_via {0} out of block bounds"
                               .format(op.get("cell_name")))
        else:
            return Verdict(False, "mount_feasibility",
                           "unknown op {0!r}".format(kind))

    # --- Long stripes: judge all ops on one polygon by their combined effect ---
    oe_map = getattr(leaf, "long_open_ends", {}) or {}
    if oe_map:
        poly_map = _polygons_by_id(ctx)
        for pid, oe in oe_map.items():
            axis = oe.get("axis")
            base = poly_map.get(pid)
            if base is None:
                continue
            bb = base.bbox_dbu
            cur = bb
            touched = False
            for op in patch.ops:
                if op.get("polygon_id") != pid:
                    continue
                kind = op.get("op")
                if kind in ("move", "resize", "resize_end"):
                    oax = op.get("axis", "x")
                    if oax != axis:
                        if not (kind == "resize" and
                                not (oe.get("open_low") or oe.get("open_high"))):
                            return Verdict(False, "mount_feasibility",
                                           "stripe {0} edit axis must be long axis {1}"
                                           .format(pid, axis))
                        # Width-only stripe: a perpendicular resize is fine.
                        cur = _apply_resize_bbox(cur, oax, op.get("delta_dbu", 0))
                        touched = True
                        continue
                    if kind == "move":
                        cur = _apply_move_bbox(cur, axis, op.get("delta_dbu", 0))
                    elif kind == "resize":
                        cur = _apply_resize_bbox(cur, axis, op.get("delta_dbu", 0))
                    else:  # resize_end
                        cur = _apply_resize_end_bbox(cur, axis,
                                                     op.get("end", "low"),
                                                     op.get("delta_dbu", 0))
                    touched = True
                elif kind == "add_jog":
                    for pt in (op.get("jog_pts") or []):
                        if len(pt) == 2 and not (
                                leaf.bbox_dbu[0] <= pt[0] <= leaf.bbox_dbu[2]
                                and leaf.bbox_dbu[1] <= pt[1] <= leaf.bbox_dbu[3]):
                            return Verdict(False, "mount_feasibility",
                                           "stripe {0} jog vertex crosses leaf border"
                                           .format(pid))
                    touched = True
                elif kind == "delete":
                    touched = False        # deleting the stripe is fine here
                    cur = bb
            if not touched:
                continue
            # The closed far end must finish exactly where it started.
            if axis == "x":
                if not oe.get("open_low") and cur[0] != bb[0]:
                    return Verdict(False, "mount_feasibility",
                                   "stripe {0} closed end (low x) moved".format(pid))
                if not oe.get("open_high") and cur[2] != bb[2]:
                    return Verdict(False, "mount_feasibility",
                                   "stripe {0} closed end (high x) moved".format(pid))
            else:
                if not oe.get("open_low") and cur[1] != bb[1]:
                    return Verdict(False, "mount_feasibility",
                                   "stripe {0} closed end (low y) moved".format(pid))
                if not oe.get("open_high") and cur[3] != bb[3]:
                    return Verdict(False, "mount_feasibility",
                                   "stripe {0} closed end (high y) moved".format(pid))
            # A stripe that crosses the crop window sticks out past the leaf by
            # definition, since its frozen far end lies outside it. The far end
            # is already pinned by the check above, so only the moved near edge
            # is bounded here; testing the whole bbox would reject every
            # crossing stripe regardless of the edit.
            lb = leaf.bbox_dbu
            if axis == "x":
                if oe.get("open_low") and not (lb[0] <= cur[0] <= lb[2]):
                    return Verdict(False, "mount_feasibility",
                                   "stripe {0} near end crosses leaf border".format(pid))
                if oe.get("open_high") and not (lb[0] <= cur[2] <= lb[2]):
                    return Verdict(False, "mount_feasibility",
                                   "stripe {0} near end crosses leaf border".format(pid))
            else:
                if oe.get("open_low") and not (lb[1] <= cur[1] <= lb[3]):
                    return Verdict(False, "mount_feasibility",
                                   "stripe {0} near end crosses leaf border".format(pid))
                if oe.get("open_high") and not (lb[1] <= cur[3] <= lb[3]):
                    return Verdict(False, "mount_feasibility",
                                   "stripe {0} near end crosses leaf border".format(pid))
    return Verdict(True)


def _clone_leaf_polys(leaf: Leaf, ctx: CaseContext) -> Dict[str, Polygon]:
    src = _polygons_by_id(ctx)
    out: Dict[str, Polygon] = {}
    for pid in (list(leaf.editable_polygons) + list(leaf.bridge_polygons)
                + list(leaf.context_readonly)):
        if pid in src:
            out[pid] = copy.deepcopy(src[pid])
    return out


def _clone_leaf_insts(leaf: Leaf, ctx: CaseContext) -> Dict[str, SubcellInstance]:
    src = _instances_by_id(ctx)
    out: Dict[str, SubcellInstance] = {}
    for iid in leaf.subcell_instances:
        if iid in src:
            out[iid] = copy.deepcopy(src[iid])
    return out


def _apply_resize_bbox(bbox: Tuple[int, int, int, int], axis: str,
                       delta: int) -> Tuple[int, int, int, int]:
    """Resize a bbox along one axis by delta, split evenly on both sides."""
    x1, y1, x2, y2 = bbox
    half = int(delta) // 2
    rem = int(delta) - half
    if axis == "x":
        return (x1 - half, y1, x2 + rem, y2)
    if axis == "y":
        return (x1, y1 - half, x2, y2 + rem)
    # treat unknown axis as no-op
    return bbox


def _apply_move_bbox(bbox: Tuple[int, int, int, int], axis: str,
                     delta: int) -> Tuple[int, int, int, int]:
    x1, y1, x2, y2 = bbox
    if axis == "x":
        return (x1 + int(delta), y1, x2 + int(delta), y2)
    if axis == "y":
        return (x1, y1 + int(delta), x2, y2 + int(delta))
    return bbox


def _apply_resize_end_bbox(bbox: Tuple[int, int, int, int], axis: str,
                           end: str, delta: int) -> Tuple[int, int, int, int]:
    """Move one edge of a bbox and leave the opposite edge where it is.

    "low" shifts the minimum edge out by delta and "high" shifts the maximum
    edge out by delta, matching how the same op is applied to real points.
    """
    x1, y1, x2, y2 = bbox
    d = int(delta)
    if axis == "x":
        if end == "low":
            return (x1 - d, y1, x2, y2)
        if end == "high":
            return (x1, y1, x2 + d, y2)
    elif axis == "y":
        if end == "low":
            return (x1, y1 - d, x2, y2)
        if end == "high":
            return (x1, y1, x2, y2 + d)
    return bbox


# ---------------------------------------------------------------------------
# Check 3 - Crop not empty
# ---------------------------------------------------------------------------

def _check_crop_not_empty(patch: Patch, leaf: Leaf, ctx: CaseContext) -> Verdict:
    """At least one editable polygon must survive the patch.

    A newly placed via does not count towards this, because it contributes an
    instance rather than an editable polygon.
    """
    remaining = set(leaf.editable_polygons)
    for op in patch.ops:
        if op.get("op") == "delete":
            remaining.discard(op.get("polygon_id"))
        elif op.get("op") == "add_polygon":
            remaining.add("__new_{0}".format(len(remaining)))
    if len(remaining) < 1:
        return Verdict(False, "crop_not_empty",
                       "patch deleted all editable polygons")
    return Verdict(True)


# ---------------------------------------------------------------------------
# Check 4 - In-leaf connectivity intact
# ---------------------------------------------------------------------------

def _check_connectivity_intact(patch: Patch, leaf: Leaf,
                               ctx: CaseContext) -> Verdict:
    """Every net in the leaf must still be a single connected component.

    Connectivity is approximated by bounding-box adjacency, which is enough to
    catch a patch that visibly cuts a net in two. The authoritative
    whole-block connectivity check runs later, at mount time.
    """
    deleted_pids = {op.get("polygon_id") for op in patch.ops
                    if op.get("op") == "delete"}
    poly_map = _polygons_by_id(ctx)

    for net_id, pids in leaf.net_to_polygons.items():
        live = [pid for pid in pids if pid not in deleted_pids]
        if len(live) <= 1:
            continue
        polys = [poly_map.get(pid) for pid in live]
        polys = [p for p in polys if p is not None]
        if len(polys) <= 1:
            continue
        if not _is_single_connected_component(polys):
            return Verdict(False, "connectivity_intact",
                           "net {0} fragmented after patch".format(net_id))
    return Verdict(True)


def _is_single_connected_component(polys: List[Polygon]) -> bool:
    """True when every polygon is reachable from the first one.

    Two polygons count as adjacent when their bounding boxes touch or overlap.
    """
    if not polys:
        return True
    n = len(polys)
    adj: List[List[int]] = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if _bboxes_touch_or_overlap(polys[i].bbox_dbu, polys[j].bbox_dbu):
                adj[i].append(j)
                adj[j].append(i)
    seen = {0}
    stack = [0]
    while stack:
        u = stack.pop()
        for w in adj[u]:
            if w not in seen:
                seen.add(w)
                stack.append(w)
    return len(seen) == n


def _bboxes_touch_or_overlap(a: Tuple[int, int, int, int],
                             b: Tuple[int, int, int, int]) -> bool:
    return a[0] <= b[2] and b[0] <= a[2] and a[1] <= b[3] and b[1] <= a[3]


# ---------------------------------------------------------------------------
# Checks 5 to 7 - spacing, routing grid, via-metal coupling
# ---------------------------------------------------------------------------

def _same_net(leaf, pid_a, pid_b):
    """True when both polygons appear in the same net cluster of the leaf.

    The clusters in ``leaf.net_to_polygons`` are the signal that is actually
    populated during a run; individual ``Polygon.net_id`` values are usually
    None, and callers that want them apply that comparison themselves.
    """
    n2p = getattr(leaf, "net_to_polygons", None) or {}
    for _net, members in n2p.items():
        ms = set(members)
        if pid_a in ms and pid_b in ms:
            return True
    return False


def _check_min_spacing_preserved(patch, leaf, ctx):
    """No edit may create a new touch or overlap with a different net.

    Each moved or resized polygon is compared against every other polygon in
    the leaf: a pair whose bounding boxes did not touch before must not touch
    afterwards. This is a coarse proxy for the spacing rules -- it catches a
    shape driven into its neighbour, but not a gap that is merely too narrow.
    Polygons on the same net are exempt.
    """
    poly_map = _polygons_by_id(ctx)
    # Snapshot the original bboxes of every polygon visible in the leaf.
    leaf_pids = (list(leaf.editable_polygons) + list(leaf.bridge_polygons)
                 + list(leaf.context_readonly) + list(getattr(leaf, "band_background", [])))
    orig = {pid: poly_map[pid].bbox_dbu for pid in leaf_pids if pid in poly_map}
    # Work out where each edited polygon would end up.
    moved = {}
    for op in patch.ops:
        kind = op.get("op")
        pid = op.get("polygon_id")
        if pid not in orig:
            continue
        if kind == "move":
            moved[pid] = _apply_move_bbox(orig[pid], op.get("axis", "x"),
                                          op.get("delta_dbu", 0))
        elif kind == "resize":
            moved[pid] = _apply_resize_bbox(orig[pid], op.get("axis", "x"),
                                            op.get("delta_dbu", 0))
        elif kind == "resize_end":
            moved[pid] = _apply_resize_end_bbox(orig[pid], op.get("axis", "x"),
                                                op.get("end", "low"),
                                                op.get("delta_dbu", 0))
        elif kind == "add_jog":
            xs = [p[0] for p in (op.get("jog_pts") or []) if len(p) == 2]
            ys = [p[1] for p in (op.get("jog_pts") or []) if len(p) == 2]
            if xs and ys:
                ob = orig[pid]
                moved[pid] = (min(ob[0], min(xs)), min(ob[1], min(ys)),
                              max(ob[2], max(xs)), max(ob[3], max(ys)))
    for pid, new_bb in moved.items():
        p = poly_map.get(pid)
        if p is None:
            continue
        for other_pid, other_bb in orig.items():
            if other_pid == pid:
                continue
            q = poly_map.get(other_pid)
            if q is None:
                continue
            # Polygons on the same net are allowed to touch each other.
            if _same_net(leaf, pid, other_pid) or (
                    p.net_id is not None and q.net_id is not None
                    and p.net_id == q.net_id):
                continue
            was = _bboxes_touch_or_overlap(orig[pid], other_bb)
            now = _bboxes_touch_or_overlap(new_bb, other_bb)
            if now and not was:
                return Verdict(False, "min_spacing_preserved",
                               "op on {0} creates new abut with {1}".format(pid, other_pid))
    return Verdict(True)


def _check_on_grid_strict(patch, leaf, ctx):
    """M4 y-edges and M5 x-edges must land on the 96-dbu routing grid.

    Only edges the patch actually moves are checked, so geometry that was
    already off-grid does not block an unrelated edit. The perpendicular axis
    is left to the 1-dbu manufacturing grid check.
    """
    poly_map = _polygons_by_id(ctx)
    for op in patch.ops:
        kind = op.get("op")
        if kind in ("move", "resize", "resize_end"):
            pid = op.get("polygon_id")
            poly = poly_map.get(pid)
            if poly is None or poly.layer_name not in _GRID96_AXIS:
                continue
            caxis = _GRID96_AXIS[poly.layer_name]
            if op.get("axis", "x") != caxis:
                continue                       # edit on the free axis -> skip
            bb = poly.bbox_dbu
            if kind == "move":
                new_bb = _apply_move_bbox(bb, caxis, op.get("delta_dbu", 0))
            elif kind == "resize":
                new_bb = _apply_resize_bbox(bb, caxis, op.get("delta_dbu", 0))
            else:  # resize_end
                new_bb = _apply_resize_end_bbox(bb, caxis,
                                                op.get("end", "low"),
                                                op.get("delta_dbu", 0))
            # Pick out the two edges on the constrained axis.
            if caxis == "y":
                old_lo, old_hi, new_lo, new_hi = bb[1], bb[3], new_bb[1], new_bb[3]
            else:
                old_lo, old_hi, new_lo, new_hi = bb[0], bb[2], new_bb[0], new_bb[2]
            for (oldv, newv) in ((old_lo, new_lo), (old_hi, new_hi)):
                if newv != oldv and (oldv % GRID_24NM_DBU == 0) \
                        and (newv % GRID_24NM_DBU != 0):
                    return Verdict(False, "on_grid_strict",
                                   "{0} new {1}-edge {2} off 96-dbu grid".format(
                                       pid, caxis, newv))
        elif kind in ("add_jog", "add_polygon"):
            # add_polygon names its own layer; add_jog inherits the layer of
            # the polygon it targets.
            if kind == "add_polygon":
                lname = op.get("layer_name") or op.get("layer")
            else:
                p = poly_map.get(op.get("polygon_id"))
                lname = p.layer_name if p is not None else None
            if lname not in _GRID96_AXIS:
                continue                       # unknown / not M4,M5 -> skip
            caxis = _GRID96_AXIS[lname]
            pts = op.get("jog_pts") if kind == "add_jog" else \
                (op.get("points") or op.get("polygon_points") or [])
            for pt in (pts or []):
                if len(pt) != 2:
                    continue
                coord = pt[1] if caxis == "y" else pt[0]
                if coord % GRID_24NM_DBU != 0:
                    return Verdict(False, "on_grid_strict",
                                   "new {0} vertex {1} off 96-dbu grid".format(caxis, coord))
    return Verdict(True)


def _check_via_metal_coupling(patch, leaf, ctx):
    """Refuse to move or delete a via on a leaf with an enclosure violation.

    Shifting a via away from the metal land that encloses it tends to make an
    enclosure violation worse. This check is deliberately blunt -- the presence
    of such an op is enough to reject the patch, whatever the resulting overlap
    would be -- so it is off unless explicitly enabled.
    """
    # Any non-zero move, or any deletion, is enough to reject.
    for op in patch.ops:
        if op.get("op") in ("move_instance", "delete_instance"):
            delta = op.get("delta_dbu", [0, 0])
            if op.get("op") == "delete_instance" or (
                    isinstance(delta, (list, tuple)) and any(int(d) for d in delta)):
                # Does any violation in this leaf name an enclosure rule?
                viol = {vv.violation_id: vv for vv in (ctx.violations or [])}
                aux_en = any(("AUX" in str(viol.get(vid).rule_id or "")
                              or "EN" in str(viol.get(vid).rule_id or ""))
                             for vid in leaf.violations if viol.get(vid))
                if aux_en:
                    return Verdict(False, "via_metal_coupling",
                                   "via move/delete on AUX/EN coupling leaf (L2)")
    return Verdict(True)
