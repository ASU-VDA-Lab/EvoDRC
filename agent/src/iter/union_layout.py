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

"""Grouping of decomposition leaves into row-union repair units.

``group_units(ctx, case, hrd)`` converts a decomposed case context into the
unit list written to unions.json. Each unit is a dict with the keys unit_id,
kind, is_union, member_leaf_ids, bbox_dbu, violation_ids and n_viol; kind is
one of union, multi or pdn, and is_union is true when a unit has two or more
members.

Grouping follows the standard-cell rows. ``detect_rail_ys`` locates the M1
power-rail centre lines geometrically, and ``compute_row_layout`` turns the
gaps between consecutive rails into bands: a crop that crosses no rail is
single-row and merges with the other single-row crops in its band, a crop that
crosses a rail becomes its own unit, and each power-grid crop stays separate.
Union bounding boxes come from the shared builder in ``hrd_split`` so the
repaired window matches the one the rest of the pipeline reconstructs.
"""


# ---------------------------------------------------------------------------
# Row-grouping algorithm
#
# detect_rail_ys, compute_row_layout and _median together are the source of
# truth for row grouping: pure standard library, deterministic, and
# independent of hash ordering.
# ---------------------------------------------------------------------------

def _median(xs):
    """Integer median of a list, or 0 when it is empty. An even-length list
    yields the floored mean of the two middle values, so the result stays an
    integer."""
    if not xs:
        return 0
    s = sorted(xs)
    n = len(s)
    mid = n // 2
    if n % 2:
        return s[mid]
    return (s[mid - 1] + s[mid]) // 2


_RAIL_WFRAC = 0.5   # A top-level M1 polygon counts as a power rail when its
                    # x-span reaches this fraction of the die width. Real rails
                    # span most of the die; signal M1 is far shorter.


def detect_rail_ys(pdn_m1_bboxes, all_m1_top_bboxes, block_bounds, tol=None):
    """Detect the centre-Y of every horizontal M1 power rail in a block.

    A standard-cell row is bounded by two consecutive M1 power rails, which
    alternate between the two supply nets at the cell-row pitch. Rails are
    found geometrically from every top-level M1 bounding box: those that are
    wider than they are tall and span at least ``_RAIL_WFRAC`` of the die width
    are kept, and their centre-Ys are clustered. The per-net list
    ``pdn_m1_bboxes`` serves only as the fallback for a block with no wide
    horizontal M1: one net's editable M1 exposes only every other rail and
    would merge two cell rows into one.

    Centre-Ys within ``tol`` of each other -- by default the larger of 40 dbu
    and a fifth of the median gap -- collapse into one rail at their rounded
    mean. Returns a sorted list of unique rail centre-Ys, empty when there is
    no M1 at all.
    """
    x0, _y0, x1, _y1 = block_bounds
    diew = int(x1) - int(x0)
    rails_src = [b for b in all_m1_top_bboxes
                 if (int(b[2]) - int(b[0])) > (int(b[3]) - int(b[1]))
                 and diew > 0 and (int(b[2]) - int(b[0])) >= _RAIL_WFRAC * diew]
    if not rails_src:                     # no wide horizontal M1 found
        rails_src = list(pdn_m1_bboxes) or list(all_m1_top_bboxes)
    ys = sorted((int(b[1]) + int(b[3])) // 2 for b in rails_src)
    if not ys:
        return []
    if tol is None:
        # Rail-to-rail gaps; duplicates within one rail share a centre and give
        # a zero gap, so they are dropped. The median gap approximates the row
        # pitch, and a fifth of it is too small to merge two real rails but
        # large enough to absorb jitter between coincident rail polygons.
        gaps = [ys[i + 1] - ys[i] for i in range(len(ys) - 1) if ys[i + 1] - ys[i] > 0]
        median_gap = _median(gaps)
        tol = max(40, int(round(0.20 * median_gap)))
    clusters = [[ys[0]]]
    for y in ys[1:]:
        if y - clusters[-1][-1] <= tol:
            clusters[-1].append(y)
        else:
            clusters.append([y])
    rails = sorted(set(int(round(sum(c) / float(len(c)))) for c in clusters))
    return rails


def compute_row_layout(leaves, rail_ys, block_bounds, cross_margin=20):
    """Assign leaves to standard-cell row bands and group them into units.

    ``leaves`` is a list of dicts with the keys idx, id, bbox and is_pdn.

    Bands are the intervals between consecutive rails, clamped to the die
    edges, so the edge list is ``[ymin] + sorted(rail_ys) + [ymax]``.

    For each non-power-grid crop, a rail counts as crossed only when it lies
    strictly inside the crop by more than ``cross_margin``; that margin stops a
    crop that merely abuts a rail -- crops are cut at rail Ys -- from counting
    as crossing. A crop that crosses no rail is single-row and is assigned to
    the band containing its y-centre; one that crosses at least one rail is
    multi-row and forms its own unit. Power-grid crops always stand alone.

    All single-row crops sharing a band become one union. The unit order is
    unions by ascending band, then multi-row crops, then power-grid crops.
    Returns a dict describing the rails, bands, pitch, per-crop assignment and
    the resulting units.
    """
    ymin, ymax = int(block_bounds[1]), int(block_bounds[3])
    rails = sorted(int(r) for r in rail_ys)
    edges = [ymin] + rails + [ymax]
    row_bands = [(edges[i], edges[i + 1]) for i in range(len(edges) - 1)]
    if len(rails) >= 2:                       # row pitch = median rail-to-rail gap
        gaps = [rails[i + 1] - rails[i] for i in range(len(rails) - 1)]
    else:                                     # too few rails: use band heights
        gaps = [hi - lo for (lo, hi) in row_bands]
    row_pitch = _median(gaps)

    def _band_of_ycenter(yc):
        for i, (lo, hi) in enumerate(row_bands):
            if lo <= yc < hi:
                return i
        if yc >= row_bands[-1][1]:            # at or above ymax -> last band
            return len(row_bands) - 1
        return 0                              # below ymin -> first band

    crop_row = {}
    single_row = []
    multi_row = []
    pdn = []
    for lf in leaves:
        idx = lf["idx"]
        if lf.get("is_pdn"):
            pdn.append(idx)
            crop_row[idx] = None
            continue
        x0, y0, x1, y1 = lf["bbox"]
        n_cross = sum(1 for r in rails if y0 + cross_margin < r < y1 - cross_margin)
        if n_cross == 0:
            b = _band_of_ycenter((int(y0) + int(y1)) // 2)
            crop_row[idx] = b
            single_row.append(idx)
        else:
            crop_row[idx] = None
            multi_row.append(idx)

    by_band = {}                              # single-row crops keyed by band index
    for idx in single_row:
        by_band.setdefault(crop_row[idx], []).append(idx)
    unions = []
    for b in sorted(by_band.keys()):
        unions.append({"row": b, "y_band": list(row_bands[b]),
                       "members": sorted(by_band[b])})

    units = []                                # stable order: unions, multi, pdn
    for u in sorted(unions, key=lambda uu: row_bands[uu["row"]][0]):
        units.append({"kind": "union", "row": u["row"],
                      "members": list(u["members"])})
    for idx in sorted(multi_row):
        units.append({"kind": "multi", "row": None, "members": [idx]})
    for idx in sorted(pdn):
        units.append({"kind": "pdn", "row": None, "members": [idx]})

    return {
        "rail_ys": rails,
        "row_bands": [list(b) for b in row_bands],
        "row_pitch": row_pitch,
        "crop_row": crop_row,
        "single_row": sorted(single_row),
        "multi_row": sorted(multi_row),
        "pdn": sorted(pdn),
        "unions": unions,
        "units": units,
        "n_single": len(single_row),
        "n_multi": len(multi_row),
        "n_pdn": len(pdn),
    }


# ---------------------------------------------------------------------------
# Deriving the row-grouping inputs from a case context
# ---------------------------------------------------------------------------

def _leaf_idx(leaf_id):
    """Numeric index of a leaf id: 'leaf_0012' and 'Block7_leaf_0012' both
    give 12, and an unrecognised id gives -1."""
    try:
        return int(leaf_id.rsplit("leaf_", 1)[-1])
    except (ValueError, IndexError):
        return -1


def _design_bbox(geom):
    """Overall design extent: the block bounds unioned with every top-level
    polygon bounding box and every flattened instance bounding box.

    The instance-bbox helper is imported lazily so this module stays importable
    without a geometry model."""
    from ..model import instance_block_bbox_dbu
    INF = 10 ** 18
    acc = [INF, INF, -INF, -INF]

    def upd(b):
        acc[0] = min(acc[0], b[0]); acc[1] = min(acc[1], b[1])
        acc[2] = max(acc[2], b[2]); acc[3] = max(acc[3], b[3])

    try:
        upd(geom.block_bounds_dbu)
    except Exception:
        pass
    for p in geom.polygons.values():
        upd(p.bbox_dbu)
    for inst in geom.instances.values():
        try:
            upd(instance_block_bbox_dbu(inst, geom.cell_defs))
        except Exception:
            pass
    return list(acc)


def group_units(ctx, case, hrd):
    """Group ``ctx.leaves`` into the list of unit dicts described in the module
    docstring."""
    geom = ctx.geometry_model

    # --- leaf records in sorted leaf id order ---------------------------------
    recs = []
    for leaf_id in sorted(ctx.leaves.keys()):
        L = ctx.leaves[leaf_id]
        recs.append({
            "idx": _leaf_idx(leaf_id),
            "id": leaf_id,
            "bbox": list(L.bbox_dbu),
            "is_pdn": bool(getattr(L, "is_pdn", False)),
            "viol": list(L.violations or []),
            "edit": list(getattr(L, "editable_polygons", []) or []),
        })
    by_idx = {r["idx"]: r for r in recs}

    # --- inputs to the row-grouping algorithm ---------------------------------
    design = _design_bbox(geom)
    pdn_m1 = [list(geom.polygons[pid].bbox_dbu)
              for r in recs if r["is_pdn"]
              for pid in r["edit"]
              if geom.polygons.get(pid) is not None
              and geom.polygons[pid].layer_name == "M1"]
    all_m1 = [list(p.bbox_dbu) for p in geom.polygons.values()
              if p.layer_name == "M1"]
    rail_ys = detect_rail_ys(pdn_m1, all_m1, design)
    layout = compute_row_layout(
        [{"idx": r["idx"], "id": r["id"], "bbox": r["bbox"],
          "is_pdn": r["is_pdn"]} for r in recs], rail_ys, design)

    # --- convert the grouped rows into unit dicts, preserving their order -----
    units = []
    for u in layout["units"]:
        members = [by_idx[i] for i in u["members"]]
        if u["kind"] == "union" and len(members) >= 2:
            member_ids = [m["id"] for m in members]        # ascending leaf index
            unit_id = "%s_union_row%d" % (case, u["row"])
            bbox_dbu = list(hrd.build_union_leaf(ctx, member_ids,
                                                 unit_id).bbox_dbu)
            viol_ids = []
            for m in members:                              # kept in member order
                viol_ids.extend(m["viol"])
            units.append({
                "unit_id": unit_id,
                "kind": "union",
                "is_union": True,
                "member_leaf_ids": member_ids,
                "bbox_dbu": bbox_dbu,
                "violation_ids": viol_ids,
                "n_viol": len(viol_ids),
            })
        else:                                              # singleton: keep leaf id
            m = members[0]
            units.append({
                "unit_id": m["id"],
                "kind": u["kind"],
                "is_union": False,
                "member_leaf_ids": [m["id"]],
                "bbox_dbu": list(m["bbox"]),
                "violation_ids": m["viol"],
                "n_viol": len(m["viol"]),
            })
    return units
