**Width Constraints (M5.W.1 – M5.W.5)**

M5.W.1 sets a 24 nm minimum horizontal width measured by projection. M5.W.5 sets a 44 nm minimum vertical width measured by Euclidean distance. M5.W.2 sets a 480 nm maximum horizontal width; the deck implements this as a ±240 nm horizontal erosion-dilation check. M5.W.3 excludes exact even-integer-multiple horizontal widths (48, 96, 144, 192, 240, 288, 336, 384, 432, 480 nm). M5.W.4 further excludes horizontal widths that cause the polygon to span an even number of minimum-width routing tracks (72, 168, 264, 360, 456 nm distances). The combined effect of M5.W.3 and M5.W.4 is that permitted horizontal widths are odd-multiple-of-24 nm values that are not simultaneously spacing-track-even.

**Spacing Constraints (M5.S.1 – M5.S.5)**

M5.S.1 sets a 24 nm minimum horizontal projection-space between vertical edges of distinct M5 polygons; a second 1 nm Euclidean check catches any overlap. M5.S.2 sets a 40 nm minimum vertical spacing between horizontal edges of distinct M5 polygons. M5.S.3 applies the 40 nm tip-to-tip floor specifically to adjacent-track M5 polygons that do not share a parallel run length. M5.S.4 applies the same 40 nm tip-to-tip floor to adjacent-track M5 polygons that do share a parallel run length, detected via 30 nm horizontal extensions of tip edges. M5.S.5 requires that when two M5 polygons are horizontally closer than 25 dbu (≤ 24 nm by projection), their overlap in the y-direction must be ≥ 44 nm.

**Geometry and Routing-Grid Constraints (M5.AUX.1 – M5.AUX.4)**

M5.AUX.1 requires every vertical M5 edge to fall on a 24 nm horizontal grid (1 dbu vertical grid), checked via `ongrid(24.nm, 1.dbu)` on the merged M5 layer. M5.AUX.2 constrains minimum-width (1x) M5 tracks — those polygons that do not survive a ±13 nm horizontal erosion — to have their centerlines at x = 48 + N×192 dbu, and only for shapes whose bounding-box top and bottom are each multiples of 96 dbu (the `base_dbu` filter). M5.AUX.3 prohibits any corner with an interior angle strictly between 0° and 90°; M5 shapes must be purely rectilinear horizontal wires with no bends. M5.AUX.4 prohibits the vertical edges of wide M5 polygons from coinciding with vertical routing-track edges belonging to separately located 1x segments; wide polygons are those that survive the ±13 nm horizontal erosion.

**V4–M5 Enclosure and Width Matching (V4.M5.EN.2, V4.M5.AUX.2)**

V4.M5.EN.2 requires that every V4 via contained inside M5 is enclosed by ≥ 11 nm on two opposite sides, tested independently in x (`m5.sized(-11.nm, 0)`) and y (`m5.sized(0, -11.nm)`). V4.M5.AUX.2 requires V4 to match M5 width exactly in the direction perpendicular to M5 length, verified by checking that each V4 inside M5 has at least two edges coincident with the enclosing M5 boundary.

In trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, both V4 shapes (shape_index 0 and 1) in cell VIA_VIA45_1_2_58_58 were resized by +152 dbu along x, and the paired M4 shape (shape_index 0) received the same x-resize; this single operation, which also touches M5 via the cell geometry, reduced violation totals from 27 to 19 in leaf_0012 and from 28 to 20 in leaf_0013 and was committed with conn_preserved=true. Resize both V4 via shapes and the matched M4 shape in cell VIA_VIA45_1_2_58_58 together along x when V4.M5.EN.2 or V4.M5.AUX.2 violations are flagged against that cell (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01).

**V5–M5 Enclosure (V5.M5.EN.1)**

V5.M5.EN.1 requires M5 to enclose every contained V5 via by ≥ 11 nm on at least two opposite sides, using the same two-axis sizing check as V4.M5.EN.2.

**Observed Operation Outcomes**

In trial:i02.ug.leaf_0002.01, M5-touching polygon p938 was translated +32 dbu in x together with instances i0098, i0097, i0064, and i0068 (all +32 dbu in x); the result was zero new in-crop and zero new out-of-crop violations across M4, M5, and V4. In trial:i01.ug.leaf_0012.07, instances i0097 and i0092 moved −48 dbu in y while i0064 and i0072 moved +96 dbu in y, touching M3, M4, M5, V3, and V4; M5-specific violations were not introduced (n_new_out_of_crop=0 for M5-touching rules), though two V1.M1.EN.1 violations were introduced on unrelated layers. The assemble_drops record attached to that trial confirms the V4 x-resize of +152 dbu on VIA_VIA45_1_2_58_58 was folded in from the cu_pool before gating (trial:i01.ug.leaf_0012.07, trial:i01.cu.def:VIA_VIA45_1_2_58_58.01).