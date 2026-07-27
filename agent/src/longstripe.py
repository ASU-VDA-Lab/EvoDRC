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

"""Classification of long metal stripes inside a leaf crop.

A leaf shows only a window onto the layout, so a wire running past the window
edge is cut off in the view and must not be resized from that side. This
module inspects the editable polygons of a leaf, records which ends of a long
stripe actually lie inside the crop, and demotes stripes that merely pass
through to read-only background. It mutates the leaf in place and reads
nothing beyond the leaf and the geometry model it belongs to.
"""


from typing import Dict, List


# A top-level metal polygon counts as a long stripe when its long axis exceeds
# the 2um per-violation window (8000 dbu), the same bound the geometry model
# applies when it clamps a polygon's long axis.
LONGAXIS_CAP_DBU = 8000


def classify(leaf, ctx):
    """Flag long stripes, record their open ends, and demote pass-throughs.

    A top-level editable polygon is long when its longer side exceeds
    LONGAXIS_CAP_DBU. For each long stripe, the ends lying inside or on the
    leaf bounding box are located:
      - no end visible in the crop: the stripe only passes through, so it
        leaves editable_polygons and is rendered as background;
      - at least one end visible: the stripe stays editable and an entry
        {axis, open_low, open_high} goes into long_open_ends, which limits
        the allowed edit to changing the length at that end.
    """
    geom = ctx.geometry_model
    if geom is None:
        return
    polys = geom.polygons
    lx1, ly1, lx2, ly2 = leaf.bbox_dbu
    if not (lx2 > lx1 and ly2 > ly1):
        return                         # degenerate bbox: nothing to classify
    from . import _invariant
    viol_by_id = {v.violation_id: v for v in (ctx.violations or [])}
    el = set(getattr(leaf, "editable_layers", ()) or ())
    own_target = set()
    for vid in leaf.violations:
        v = viol_by_id.get(vid)
        if v is None:
            continue
        vb = _invariant.expand(v.bbox_dbu, _invariant.SPATIAL_MARGIN_DBU)
        for pid in list(leaf.editable_polygons):
            p = polys.get(pid)
            if (p is not None and p.layer_name in el
                    and _invariant.bbox_intersect(p.bbox_dbu, vb)):
                own_target.add(pid)
    # Bridge polygons are routed here, ahead of the stripe loops, and the
    # routing is idempotent so it can be redone on a merged or relocated leaf
    # with a grown bounding box; earlier stages treat bridge membership as
    # provisional and this block settles it. A bridge is only partially
    # editable in this crop when the crop contains at least one real end of the
    # wire: a long-axis end strictly inside the leaf interior, positive overlap
    # on the short axis, and a clip with positive area. The single allowed edit
    # is then resizing that visible end, while the far end and the middle stay
    # fixed. A bridge with no real end in the crop becomes read-only context
    # instead. When leaves are unioned their open-end records are combined with
    # a plain dict update, so one member's entry can overwrite another's; that
    # can only withdraw a permission, never grant one.
    from .model import is_pdn_editable_pid
    from .crop_body import poly_is_real_lever        # local: no import cycle
    # A second set of polygons overlapping this leaf's own violations, used
    # only by the bridge branch below. It dilates the violation window exactly
    # as own_target does, but also scans bridge polygons and drops the
    # editable-layer restriction, since a polygon a violation actually targets
    # can sit outside the rule's layer band.
    own_target_wide = set()
    for vid in leaf.violations:
        v = viol_by_id.get(vid)
        if v is None:
            continue
        vb = _invariant.expand(v.bbox_dbu, _invariant.SPATIAL_MARGIN_DBU)
        for pid in dict.fromkeys(list(leaf.editable_polygons)
                                 + list(leaf.bridge_polygons)):
            p = polys.get(pid)
            if p is not None and _invariant.bbox_intersect(p.bbox_dbu, vb):
                own_target_wide.add(pid)
    _bridge_routed = set()
    _demoted_bridge_layers = set()
    if not getattr(leaf, "is_pdn", False):
        for pid in dict.fromkeys(list(leaf.editable_polygons)
                                 + list(leaf.bridge_polygons)):
            p = polys.get(pid)
            if p is None or p.owner_kind != "bridge":
                continue
            if is_pdn_editable_pid(pid):
                continue          # power-net polygon: its power crop owns it
            bx1, by1, bx2, by2 = p.bbox_dbu
            fully_inside = (bx1 >= lx1 and by1 >= ly1
                            and bx2 <= lx2 and by2 <= ly2)
            if pid in own_target_wide and fully_inside \
                    and poly_is_real_lever(p, leaf.bbox_dbu):
                # A polygon that one of this leaf's own violations targets, and
                # whose whole bounding box fits in the window, is fully
                # editable: no end restriction and no demotion. It stays listed
                # as a bridge so the validator still admits edits to it.
                leaf.long_open_ends.pop(pid, None)
                if pid not in leaf.editable_polygons:
                    leaf.editable_polygons.append(pid)
                leaf.context_readonly = [q for q in leaf.context_readonly
                                         if q != pid]
                leaf.band_background = [q for q in leaf.band_background
                                        if q != pid]
                _bridge_routed.add(pid)
                continue
            bw = bx2 - bx1
            bh = by2 - by1
            baxis = "x" if bw >= bh else "y"
            if baxis == "x":
                # Positive overlap on the short axis, with an end either inside
                # the interior or exactly on the border. An end on the border is
                # still fully visible; only a polygon reaching past the border
                # is cut off by the view.
                b_short = (by1 < ly2 and ly1 < by2)
                b_low = b_short and (lx1 <= bx1 < lx2)
                b_high = b_short and (lx1 < bx2 <= lx2)
            else:
                b_short = (bx1 < lx2 and lx1 < bx2)
                b_low = b_short and (ly1 <= by1 < ly2)
                b_high = b_short and (ly1 < by2 <= ly2)
            if (b_low or b_high) and poly_is_real_lever(p, leaf.bbox_dbu):
                # Stays editable, but only at the end or ends inside the crop.
                leaf.long_open_ends[pid] = {"axis": baxis, "open_low": b_low,
                                            "open_high": b_high}
                if pid not in leaf.editable_polygons:
                    leaf.editable_polygons.append(pid)
                if pid not in leaf.bridge_polygons:
                    leaf.bridge_polygons.append(pid)
                leaf.context_readonly = [q for q in leaf.context_readonly
                                         if q != pid]
                leaf.band_background = [q for q in leaf.band_background
                                        if q != pid]
            else:
                # No real end inside the crop, so it becomes read-only context.
                leaf.long_open_ends.pop(pid, None)
                leaf.editable_polygons = [q for q in leaf.editable_polygons
                                          if q != pid]
                leaf.bridge_polygons = [q for q in leaf.bridge_polygons
                                        if q != pid]
                if pid not in leaf.context_readonly:
                    leaf.context_readonly.append(pid)
                if pid not in leaf.band_background:
                    leaf.band_background.append(pid)
                _demoted_bridge_layers.add(p.layer_name)
            _bridge_routed.add(pid)

    thr = LONGAXIS_CAP_DBU
    kept = []
    for pid in list(leaf.editable_polygons):
        if pid in _bridge_routed:
            # Bridges were already routed above, so the stripe path keeps each
            # one exactly as that pass left it: same listing, same open-end
            # record.
            kept.append(pid)
            continue
        poly = polys.get(pid)
        if poly is None:
            kept.append(pid)
            continue
        x1, y1, x2, y2 = poly.bbox_dbu
        w = x2 - x1
        h = y2 - y1
        if max(w, h) <= thr:
            kept.append(pid)
            continue
        axis = "x" if w >= h else "y"
        if axis == "x":
            # An end exactly on the crop border is still fully visible and can
            # be resized; only a polygon reaching strictly past the border is
            # cut off by the view.
            open_low = x1 >= lx1           # left end inside or on the border
            open_high = x2 <= lx2          # right end inside or on the border
        else:
            open_low = y1 >= ly1
            open_high = y2 <= ly2
        if not (open_low or open_high):
            if pid in own_target:
                # A pass-through stripe that one of this leaf's own violations
                # targets stays editable, with both ends recorded as closed.
                leaf.long_open_ends[pid] = {"axis": axis, "open_low": open_low,
                                            "open_high": open_high}
                kept.append(pid)
            elif pid not in leaf.band_background:
                leaf.band_background.append(pid)
        elif open_low and open_high:
            # Both ends lie inside or on the crop border, so the whole wire is
            # visible and this is an ordinary fully editable polygon with no
            # open-end record. Any stale entry is dropped first: this function
            # mutates long_open_ends in place, and a leaf can arrive already
            # carrying entries from its members or from an earlier, smaller
            # window. Leaving one in place would render the wire as though one
            # end were frozen. Only windows wider than the 8000-dbu clamp reach
            # this branch, so it applies to unioned, merged and power-net crops
            # but never to a single-violation window.
            leaf.long_open_ends.pop(pid, None)
            kept.append(pid)
        else:
            # Exactly one end is visible: record it as the only editable end.
            leaf.long_open_ends[pid] = {"axis": axis,
                                        "open_low": open_low,
                                        "open_high": open_high}
            kept.append(pid)
    leaf.editable_polygons = kept

    # Widen editable_layers to every layer carried by a top-level editable or
    # bridge polygon now in this leaf, so the validator's layer-band check
    # accepts them. This only ever adds layers to the rule's own band.
    _ext = set(leaf.editable_layers)
    for _pid in (list(leaf.editable_polygons) + list(leaf.bridge_polygons)):
        _p = polys.get(_pid)
        if _p is not None:
            _ext.add(_p.layer_name)
    # Layers of demoted bridges stay in editable_layers, so that demoting a
    # bridge leaves the leaf's layer sets unchanged, and with them the later
    # merge decisions and the validator's layer-band check.
    _ext |= _demoted_bridge_layers
    leaf.editable_layers = tuple(sorted(_ext))

    # Second pass: decide from window containment alone which of the remaining
    # editable polygons may be resized at one end only.
    #   * entirely inside the window: fully editable, nothing recorded here.
    #   * extending past any leaf edge: restricted to one end, but only if at
    #     least one long-axis end lies strictly inside the interior. That end is
    #     the near end and may be resized; the protruding far end is frozen.
    #   * crossing both long-axis borders, or touching a border with no end
    #     strictly inside: there is no near end, so the polygon stays fully
    #     editable. Its clip still has positive area and remains a usable
    #     handle, and advertising a resize the validator would later reject
    #     would be worse than leaving it unrestricted.
    #   * clipping to zero area inside the leaf: skipped, as it offers no
    #     handle at all.
    from .crop_body import poly_is_real_lever            # local: no import cycle
    for pid in list(leaf.editable_polygons):
        if pid in leaf.long_open_ends:                   # already restricted
            continue
        poly = polys.get(pid)
        if poly is None:
            continue
        bx1, by1, bx2, by2 = poly.bbox_dbu
        crosses = (bx1 < lx1 or bx2 > lx2 or by1 < ly1 or by2 > ly2)
        if not crosses:
            continue                                     # entirely in-window
        if not poly_is_real_lever(poly, leaf.bbox_dbu):  # clips to zero area
            continue
        w = bx2 - bx1
        h = by2 - by1
        axis = "x" if w >= h else "y"
        if axis == "x":
            open_low = (lx1 < bx1 < lx2)                 # strictly inside
            open_high = (lx1 < bx2 < lx2)
        else:
            open_low = (ly1 < by1 < ly2)
            open_high = (ly1 < by2 < ly2)
        if not (open_low or open_high):
            continue                                     # no near end; stays full
        leaf.long_open_ends[pid] = {"axis": axis, "open_low": open_low,
                                    "open_high": open_high}

    # A layer must never be listed as both editable and view-only.
    leaf.background_layers = tuple(
        sorted(set(leaf.background_layers) - set(leaf.editable_layers)))
