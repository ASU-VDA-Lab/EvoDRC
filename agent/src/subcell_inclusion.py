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

"""Selection of the subcell geometry a leaf shows.

A crop shows a standard cell only through its pins. This pass picks out the
individual V0 and M1 pin polygons of every standard-cell instance in the leaf
that either falls inside the leaf window or touches editable geometry, and
records them on the leaf as frozen context, dropping repeats of the same pin.
For a power-net leaf it does the opposite, narrowing the leaf to the vias that
net owns and clearing the standard-cell and background channels. The leaf is
modified in place and nothing becomes editable as a result.
"""


from .model import instance_block_polys


# GDS layer numbers for the std-cell pin keep candidates.
_GDS_M1 = 19
_GDS_V0 = 18


def _bbox_of_points(pts):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return (min(xs), min(ys), max(xs), max(ys))


def _touch(a, b):
    return a[0] <= b[2] and b[0] <= a[2] and a[1] <= b[3] and b[1] <= a[3]


def refine(leaf, ctx):
    """Fill leaf.stdcell_pin_polys with the frozen V0 and M1 pins of the leaf.

    For a power-net leaf it instead narrows subcell_instances to the vias that
    net owns and clears the standard-cell and background channels. These pins
    are all a standard cell contributes; routing vias are stamped by the crop
    renderer. Nothing in this pass changes editable_polygons."""
    geom = ctx.geometry_model
    if geom is None:
        return
    insts = geom.instances
    if getattr(leaf, "is_pdn", False):
        # A power-net crop shows only that net's own geometry and the vias it
        # owns. Standard cells and vias belonging to anything else are dropped,
        # and the background channels, which would otherwise carry the other
        # power net and all the signal routing, are emptied.
        owned = set(getattr(leaf, "owned_instances", ()) or ())
        leaf.subcell_instances = [iid for iid in leaf.subcell_instances if iid in owned]
        leaf.stdcell_pin_polys = []
        leaf.ro_neighbor_ids = []
        leaf.band_background = []
        return
    cell_defs = geom.cell_defs
    polys = geom.polygons
    lb = leaf.bbox_dbu
    # World bounding boxes of the editable geometry, for the touch test below.
    edit_bboxes = []
    for pid in leaf.editable_polygons:
        p = polys.get(pid)
        if p is not None:
            edit_bboxes.append(p.bbox_dbu)
    keep_gds = _keep_gds_for_leaf(leaf)
    seen_pin = set()      # dedup key: (cell name, first point, layer)
    pins = []
    for iid in leaf.subcell_instances:
        inst = insts.get(iid)
        if inst is None or inst.kind != "stdcell":
            continue
        for (lyr, wpts, _cut) in instance_block_polys(inst, cell_defs):
            if lyr not in keep_gds:
                continue
            bb = _bbox_of_points(wpts)
            in_leaf = _touch(bb, lb)
            touches_edit = any(_touch(bb, eb) for eb in edit_bboxes)
            if not (in_leaf or touches_edit):
                continue
            key = (inst.cell_name, wpts[0] if wpts else (0, 0), lyr)
            if key in seen_pin:
                continue
            seen_pin.add(key)
            pins.append((inst.cell_name, lyr, tuple(wpts)))
    leaf.stdcell_pin_polys = pins


def _keep_gds_for_leaf(leaf):
    """Return the GDS layer numbers whose standard-cell polygons to keep.

    M1 is kept whenever it is in the leaf's layer band, since standard cells
    contribute their M1 pins, and V0 is added when the leaf's rule deck
    mentions it. M1 alone is the floor if neither applies."""
    keep = set()
    band_names = set(leaf.editable_layers) | set(leaf.background_layers)
    if "M1" in band_names:
        keep.add(_GDS_M1)
    # V0 is dropped from the editable band, so the layers the leaf's own rules
    # name -- kept whole in case_deck_layers, V0 included -- are what identify a
    # leaf whose rule couples V0 to M1 and therefore has to show the
    # standard-cell V0 pin.
    if "V0" in set(getattr(leaf, "case_deck_layers", ()) or ()):
        keep.add(_GDS_V0)
    if not keep:
        keep.add(_GDS_M1)        # conservative floor
    return keep
