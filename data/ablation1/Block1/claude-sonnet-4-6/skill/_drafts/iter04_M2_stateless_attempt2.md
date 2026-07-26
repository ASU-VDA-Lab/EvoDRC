## Geometry constraints

M2 polygons require a minimum width of 18 nm (M2.W.1) and a minimum area of 504 nm² (M2.A.1). All M2 edges must be orthogonal per the GEOMETRY.NONORTHOGONAL rule. No trial in this history introduced non-orthogonal M2 geometry.

## Spacing rule hierarchy

Spacing requirements between M2 polygons depend on the length of the interacting edges:

- **Side-to-side (M2.S.1):** 18 nm between edges both longer than 36 nm.
- **Tip-to-side (M2.S.2):** 25 nm (projection) when one edge is ≤36 nm and the other is >36 nm.
- **Wide-tip-to-tip (M2.S.3):** 27 nm (projection) when both edges are 24–36 nm.
- **Mixed-tip (M2.S.5):** 31 nm (projection) when one edge is 24–36 nm and the other is <24 nm.
- **Narrow-tip-to-tip (M2.S.4):** 31 nm (projection) when both edges are <24 nm.
- **Corner-to-corner (M2.S.6):** 20 nm Euclidean.

## Forbidden co-location pattern (M2.S.7)

A tip-to-tip gap of 18 nm between M2 polygons is forbidden when the co-located side-to-side spacing is ≤32 nm and the parallel run length is <35 nm. The resize_end operations recorded in trial:i01.ug.Block1_union_row1.00 (x +128 dbu high end and x +92 dbu high end on two separate polygons) and trial:i01.ug.Block1_union_row3.03 (x +92 dbu high end) increased run length along affected M2 segments; both trials were accepted with n_new_in_crop of 4 and 0 respectively, and zero out-of-crop violations.

## Diagonal gap spacing (M2.S.8)

Tip-to-tip gaps on separate M2 tracks must have Euclidean center-to-center distance ≥80 nm, where gap centers are derived by shrinking each 18 nm gap region by 8.5 nm per side. Operations that extend or eliminate tip-to-tip gaps—such as the resize_end steps in trial:i01.ug.Block1_union_row3.03 and trial:i01.ug.Block1_union_row1.00—reduce the number of gap centers subject to M2.S.8 evaluation.

## Via enclosure by M2: V1 (V1.M2.EN.2, V1.M2.AUX.2)

Every V1 must be enclosed by M2 on two opposite sides with ≥5 nm each, or ≥5 nm on one side and flush (0 nm) on the other. Additionally, V1 width must match M2 width perpendicular to M2 length (V1.M2.AUX.2). All unit_gate trials that touch M2 also touch V1 in this history; all were accepted with conn_preserved=true, including trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row9.08, trial:i02.ug.Block1_union_row6.01, and trial:i04.ug.leaf_0001.00. An add_via inserting a VIA_VIA12 cell (replacing a deleted instance) in trial:i02.ug.leaf_0004.02 was accepted with zero new violations, confirming that via insertion at a properly placed origin satisfies both V1.M2.EN.2 and V1.M2.AUX.2.

## Via enclosure by M2: V2 (V2.M2.EN.1)

V2 must be enclosed by M2 by ≥5 nm on at least two opposite sides. A whole-instance move of [−36, 0] dbu in trial:i04.ug.leaf_0002.01 (touching M2, M3, V2) was accepted with zero new violations. A cu_pool resize_via_shape operation (y −40 dbu on the M3 shape of cell VIA_VIA23_1_3_36_36) in trial:i02.cu.def:VIA_VIA23_1_3_36_36.00 was rejected with decision=rejected_net_positive and delta_total=0 across both sampled windows; shrinking the M3 shape of that via cell produced no net reduction in M2-layer violations.

## Instance move steps and new-violation counts

Unit_gate instance moves in this history use multiples of 36 dbu along x or y. Accepted displacements include 36, 72, and 108 dbu in trials trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row8.07, trial:i03.ug.Block1_union_row3.00, trial:i03.ug.leaf_0004.01, and trial:i03.ug.leaf_0005.02; and −32 dbu in trial:i01.ug.Block1_union_row6.06 and trial:i01.ug.Block1_union_row8.07. A move with delta 4 dbu (x) applied to instance i0060 in trial:i04.ug.leaf_0004.03 was accepted (gated_in, conn_preserved=true) but introduced 80 new in-crop violations across a locus spanning (1728,2068)–(14256,13680), the largest new-violation count in this history; no other single trial in this history produced more than 4 new in-crop violations.

## Polygon resize operations on M2

resize_end operations on M2 polygon endpoints adjust segment length. Accepted high-end resize_end deltas: x +36 dbu (trial:i01.ug.Block1_union_row5.05, trial:i01.ug.leaf_0020.10), x +52 dbu (trial:i01.ug.Block1_union_row4.04), x +72 dbu (trial:i03.ug.leaf_0004.01), x +92 dbu (trial:i01.ug.Block1_union_row3.03), x +128 dbu (trial:i01.ug.Block1_union_row1.00). Accepted low-end resize_end delta: x +36 dbu (trial:i01.ug.Block1_union_row5.05). A symmetric resize of +36 dbu on both ends of polygon p1390 in trial:i01.ug.leaf_0031.11 was accepted with 4 new in-crop violations. All resize trials listed above were accepted as gated_in with conn_preserved=true.