Based on the single measured record `i03.cu.def:VIA_VIA45_1_2_58_58.00`, here is the [KNOWLEDGE] section body:

---

## Co-expansion of V4 and M4 in the same axis resolves the dominant violation cluster

The only applied repair in this layer's history (trial:i03.cu.def:VIA_VIA45_1_2_58_58.00) expanded two V4 shapes and one M4 shape simultaneously along the x-axis, each by 152 dbu, inside cell `VIA_VIA45_1_2_58_58`. That single three-operation move reduced the whole-design violation count from 89 to 61, a net delta of −28, with connectivity fully preserved (conn_preserved=true). Apply co-expansion of V4 and the enclosing M4 shape by an equal delta on the same axis when targeting this cell type (trial:i03.cu.def:VIA_VIA45_1_2_58_58.00).

## Match delta_dbu across V4 shapes and the co-located M4 shape

In trial:i03.cu.def:VIA_VIA45_1_2_58_58.00, all three resize_via_shape operations used the identical delta_dbu of 152. Use equal deltas across all V4 shape indices and the companion M4 shape when operating on the same axis: mismatching deltas would shift enclosure margins asymmetrically and risk introducing new V4.M4.EN.1 violations.

## Both V4 shape indices in a multi-via cell must be resized together

The cell `VIA_VIA45_1_2_58_58` contained at least two V4 shapes (shape_index 0 and shape_index 1), both resized in trial:i03.cu.def:VIA_VIA45_1_2_58_58.00. Never resize only one shape index in a multi-shape via cell; omitting either index leaves the unmodified shape at its original width, which can re-trigger V4.W.1 or V4.M5.AUX.2 on the untouched via (trial:i03.cu.def:VIA_VIA45_1_2_58_58.00).

## x-axis expansion is the effective repair direction for this cell type

The repair channel `cu_pool` selected x-axis expansion for both the V4 and M4 shapes in trial:i03.cu.def:VIA_VIA45_1_2_58_58.00. V4.M5.AUX.2 requires that V4 width perpendicular to the M5 length direction matches M5 exactly; an x-axis expansion corrects that match when M5 runs along y. V4.M4.EN.1 requires 11 nm enclosure on at least two opposite sides; expanding M4 in x by the same delta as V4 in x maintains or grows the x-direction enclosure margin without disturbing the orthogonal edges (trial:i03.cu.def:VIA_VIA45_1_2_58_58.00).

## Whole-design locus is appropriate; no sub-region restriction is needed

Trial:i03.cu.def:VIA_VIA45_1_2_58_58.00 used locus [0, 0, 14672, 14672] (unit:whole_design) and produced a clean −28 delta with no reported secondary violations. Do not restrict the DRC window to a sub-region for repairs targeting this cell definition; the cell is instantiated across the full design footprint and a narrow locus would leave instances outside the window uncorrected.

## Spacing rules (V4.S.1 / V4.S.2 / V4.S.3) were not triggered by 152 dbu x-expansion

The net violation count dropped after expanding V4 shapes by 152 dbu in x, meaning the expansion did not push any V4 instance within 33 nm of a neighbor along the projection or Euclidean metric (trial:i03.cu.def:VIA_VIA45_1_2_58_58.00). When proposing further x-expansions to this cell, verify that the grown V4 edge does not cross the 33 nm spacing threshold to the nearest co-planar V4 on either the same or different net; the measured safe expansion was 152 dbu and conn_preserved was true.