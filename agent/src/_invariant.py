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

"""Decide whether a leaf is worth dispatching, plus small bbox helpers.

A leaf is only useful when it holds at least one DRC violation and at least one
editable item, that is an editable polygon or an instance it owns and may move.
A leaf failing either condition is an empty crop: it is marked as skipped and
never dispatched. The DRC reports name no shapes for a violation, so a
violation is coupled to shapes spatially, by bounding-box intersection, the
same way the leaf-splitting stage does it.
"""

SKIP_STATUS = "skipped_empty_crop"
# Dilation applied to a violation bbox when searching for the editable shape
# that could fix it. Bridge co-editing deliberately ignores this margin.
SPATIAL_MARGIN_DBU = 500


def bbox_intersect(a, b):
    # Inclusive: boxes sharing only an edge or a corner still count as touching.
    return a[0] <= b[2] and b[0] <= a[2] and a[1] <= b[3] and b[1] <= a[3]


def bbox_contains(outer, inner):
    return (outer[0] <= inner[0] and outer[1] <= inner[1]
            and outer[2] >= inner[2] and outer[3] >= inner[3])


def expand(b, m):
    return (b[0] - m, b[1] - m, b[2] + m, b[3] + m)


# The current case's polygons, published once per case by the leaf-splitting
# stage. A polygon id missing from this map is counted as a usable lever rather
# than discarded, so a caller that never published anything still gets a count.
_POLYS_FOR_LEVER = {}          # polygon_id -> types.Polygon

def set_polys_for_lever(polys):
    """Publish the current case's polygons, so the lever count below can clip
    editable polygons against a leaf's bbox."""
    global _POLYS_FOR_LEVER
    _POLYS_FOR_LEVER = polys or {}

def leaf_editable_count(leaf):
    """Count the levers a leaf actually has to work with.

    An editable polygon counts only when it overlaps the leaf's bbox and clips
    into it with positive area, so the count is the number of polygons this
    leaf can really edit and an otherwise empty leaf still reads as empty.
    Owned movable instances are added to the count. A polygon id that was never
    published through set_polys_for_lever is counted rather than dropped."""
    from .crop_body import poly_is_real_lever      # local import: no cycle
    polys = _POLYS_FOR_LEVER
    bbox = getattr(leaf, "bbox_dbu", (0, 0, 0, 0))
    n = 0
    for pid in (getattr(leaf, "editable_polygons", []) or []):
        if pid not in polys:                       # no polygon map published
            n += 1
            continue
        if poly_is_real_lever(polys.get(pid), bbox):
            n += 1
    return n + len(getattr(leaf, "owned_instances", ()) or [])


def leaf_passes_invariant(leaf):
    return (len(getattr(leaf, "violations", []) or []) >= 1
            and leaf_editable_count(leaf) >= 1)


def mark_invariant_skips(leaves):
    """Stamp leaf.skip_status on every leaf that fails the invariant.

    Returns (kept, skipped). Idempotent, and only sets a flag: no geometry is
    changed."""
    kept, skipped = [], []
    for leaf in leaves:
        if leaf_passes_invariant(leaf):
            leaf.skip_status = None
            kept.append(leaf)
        else:
            leaf.skip_status = SKIP_STATUS
            skipped.append(leaf)
    return kept, skipped


def unit_touch_failures(ctx, leaf):
    """Report the violations of a unit that nothing in that unit could fix.

    A unit is a final leaf or a union of leaves. For each of its violations it
    must own at least one editable object whose bbox touches the violation
    bbox, where touching includes a shared edge or vertex so that zero-area
    edge markers still register: either an editable top-level polygon flagged
    as directly repairable, or an owned movable instance. This is the same
    predicate the crop's repair-order section is built from.

    Returns a list of failure dicts::

        {"violation_id", "rule_id", "bbox", "touchers"}

    where "touchers" names every object that does touch the failing violation,
    each with its editability flag inside this unit, for the diagnostic
    message. An empty list means the unit passes. The function is pure and
    read-only; deciding what to do about a failure is the caller's job."""
    from .pdn_prepass import _bbox_contact_score   # local: no import cycle
    from .crop_body import _hl_poly_flag, _hl_inst_flag
    from .clips import _SEED_EXCLUDE_LAYERS
    from .model import instance_block_bbox_dbu
    geom = getattr(ctx, "geometry_model", None)
    if geom is None:
        return []
    polys = geom.polygons
    insts = geom.instances
    cell_defs = geom.cell_defs
    viol_by_id = {v.violation_id: v
                  for v in (getattr(ctx, "violations", []) or [])}
    partial = getattr(leaf, "long_open_ends", {}) or {}
    edit = set(leaf.editable_polygons or [])
    bridge = set(leaf.bridge_polygons or [])
    own = set(getattr(leaf, "owned_instances", ()) or ())
    bbox = getattr(leaf, "bbox_dbu", (0, 0, 0, 0))

    # The unit's candidate editable objects, resolved once with the same flags
    # the repair-order section prints.
    poly_cands = []            # (pid, bbox) flagged 'C ' / 'D '
    for pid in sorted(edit | bridge):
        p = polys.get(pid)
        if p is None or p.layer_name in _SEED_EXCLUDE_LAYERS:
            continue
        flag = _hl_poly_flag(pid, p, bbox, edit, bridge, partial)
        if flag.startswith("C ") or flag.startswith("D "):
            poly_cands.append((pid, p.bbox_dbu))
    inst_cands = []            # (iid, world bbox) of owned movable instances
    for iid in sorted(own):
        inst = insts.get(iid)
        if inst is None:
            continue
        flag, _lbl, _o = _hl_inst_flag(iid, inst, own)
        if flag.startswith("movable"):
            inst_cands.append((iid, instance_block_bbox_dbu(inst, cell_defs)))

    failures = []
    for vid in (leaf.violations or []):
        v = viol_by_id.get(vid)
        if v is None:
            continue
        vb = v.bbox_dbu
        hit = any(_bbox_contact_score(vb, pb) > 0 for _pid, pb in poly_cands)
        if not hit:
            hit = any(_bbox_contact_score(vb, ib) > 0
                      for _iid, ib in inst_cands)
        if hit:
            continue
        # Diagnostics: every object touching the violation, with its flag.
        touch = []
        for pid in sorted(polys.keys()):
            p = polys[pid]
            if p.layer_name in _SEED_EXCLUDE_LAYERS:
                continue
            if _bbox_contact_score(vb, p.bbox_dbu) > 0:
                touch.append("%s[%s,%s]" % (
                    pid, p.layer_name,
                    _hl_poly_flag(pid, p, bbox, edit, bridge, partial)))
        for iid in sorted(insts.keys()):
            inst = insts[iid]
            ib = instance_block_bbox_dbu(inst, cell_defs)
            if _bbox_contact_score(vb, ib) > 0:
                fl, _lbl, _o = _hl_inst_flag(iid, inst, own)
                touch.append("%s[%s,%s]" % (iid, inst.cell_name, fl))
        failures.append({"violation_id": vid,
                         "rule_id": getattr(v, "rule_id", "?"),
                         "bbox": tuple(vb),
                         "touchers": touch})
    return failures
