**V2-in-M3 enclosure: resize and redistribute V2 shapes within via cells**

When V2.M3.EN.2 or V2.M3.AUX.2 violations occur inside a via cell, resize V2 shapes on the axis of the violation and redistribute their positions within the cell (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). In that trial, three V2 shapes in cell VIA_VIA23_1_3_36_36 were adjusted on x: shape_index 0 moved −144 dbu, shape_index 2 moved +144 dbu, and all three shapes were widened by +288 dbu in x. The repair was applied and reduced total violations by 24 (leaf_0012: −12, leaf_0013: −12). Touched layers were M2, M3, and V2.

V2.M3.EN.2 requires that V2 be enclosed by M3 by at least 5 nm on two opposite sides (either 5 & 5 nm, or 5 & 0 nm). V2.M3.AUX.2 requires that V2 match the M3 width perpendicular to the M3 length. Widening V2 shapes in x by +288 dbu while symmetrically repositioning them (−144 dbu / +144 dbu) within the cell addresses both constraints together, as confirmed by the applied result in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00. Do not adjust V2 position alone without also resizing to match M3 width; trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 shows that both the move and resize operations were required in the same repair.

**M3 polygon asymmetric x-extension in unit-gate channel**

In trial:i03.ug.leaf_0002.01 (channel `unit_gate`, iter 3), M3 polygon p937 was extended asymmetrically on x: low end +64 dbu, high end +320 dbu, for a net shift of +192 dbu at the polygon center with 256 dbu of additional length on the high side relative to the low side. The trial was gated_in with 2 new violations within the crop window, 0 new violations outside the crop window, and connectivity preserved. Simultaneously, eight instances were moved in y by ±24 or ±72 dbu. Apply asymmetric resize on M3 polygons when the required extension differs between the two ends (trial:i03.ug.leaf_0002.01); there is no requirement that both ends be extended equally.

**Instance y-moves propagate to M3**

In trial:i04.ug.leaf_0003.02 (channel `unit_gate`, iter 4), instance moves of ±24 dbu in y (i0090: +24 dbu, i0110: +24 dbu, i0089: −24 dbu) produced changes on M3 among layers M2, M3, M4, M5, V2, V3, V4. The trial was gated_in with 2 new in-crop violations and connectivity preserved. Evaluate instance moves in y for their effect on M3 spacing rules (M3.S.1, M3.S.2, M3.S.3, M3.S.4, M3.S.5, M3.S.6) and on M3 enclosure of V3 (V3.M3.EN.1) whenever the moved instances carry M3 geometry, as confirmed by trial:i04.ug.leaf_0003.02.

**Gated-in decisions with new in-crop violations**

Both trial:i03.ug.leaf_0002.01 and trial:i04.ug.leaf_0003.02 were gated_in with exactly 2 new violations within the crop window and 0 new violations outside the crop, with connectivity preserved in both cases. Repairs accepted under `gated_in` with new in-crop violations and zero new out-of-crop violations represent a net improvement over the crop as a whole; the introduced in-crop violations become targets for subsequent repair iterations.

**M3 width, area, and spacing constraints: interaction with resize operations**

M3.W.1 sets the minimum M3 width at 18 nm. M3.A.1 sets the minimum M3 polygon area at 504 nm². When resizing M3 polygons—as performed in trial:i03.ug.leaf_0002.01—verify that the resized polygon still satisfies M3.W.1 and M3.A.1, and that neither the moved low edge nor the extended high edge creates new M3.S.* violations against adjacent M3 geometry.

M3.S.1 requires 18 nm side-to-side spacing when both opposing edges exceed 36 nm in length. M3.S.2 requires 25 nm tip-to-side spacing (projection) when one edge is ≤ 36 nm and the other is > 36 nm. M3.S.3 requires 27 nm tip-to-tip spacing (projection) when both edges fall between 24 nm and 36 nm. M3.S.5 requires 31 nm tip-to-tip spacing when one edge is between 24 nm and 36 nm and the other is < 24 nm. M3.S.4 requires 31 nm tip-to-tip spacing when both edges are < 24 nm. M3.S.6 requires 20 nm corner-to-corner Euclidean spacing between M3 polygons. The asymmetric extension of p937 in trial:i03.ug.leaf_0002.01 introduced 2 new in-crop violations, confirming that M3 polygon resizes must be checked against all M3.S.* rules on all four sides of the modified polygon.

**V3.M3.EN.1 enclosure: M3 must enclose V3 by 5 nm on at least two opposite sides**

V3.M3.EN.1 requires that V3 be inside an M3 region sized inward by 5 nm on either the x-pair or the y-pair of sides. Instance moves that shift M3 relative to V3 can create or repair V3.M3.EN.1 violations; both trial:i03.ug.leaf_0002.01 and trial:i04.ug.leaf_0003.02 touch V3 and M3 together, and both were gated_in rather than rejected, confirming that the enclosure remained satisfiable after the moves. Never move M3 or V3 instances in y without checking V3.M3.EN.1 on both the moved and stationary V3/M3 pairs (trial:i03.ug.leaf_0002.01, trial:i04.ug.leaf_0003.02).