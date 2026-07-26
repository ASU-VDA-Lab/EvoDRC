## Via Enclosure and Shape Repair (V2 on M3)

The only cu_pool trial in this layer's history reshaped V2 shapes to satisfy V2.M3.EN.2 and V2.M3.AUX.2 without moving the M3 polygons themselves. In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, five ops were applied on cell VIA_VIA23_1_3_36_36: an initial x-axis move of the first V2 shape by -144 dbu, followed by x-axis resizes of +264 dbu and +288 dbu on the first two shapes, then a +144 dbu move and +264 dbu resize on the third shape. This sequence yielded a net reduction of 78 violations across windows leaf_0019 (-42) and leaf_0020 (-36), with connectivity preserved. The approach of repositioning the via center and then widening the via shape along the enclosure-deficient axis addresses both the projection-check (V2.M3.EN.2) and the width-match requirement (V2.M3.AUX.2) in a single coordinated set of ops.

When V2 shapes are involved, correct the enclosure deficit by first translating the via to reduce the asymmetry, then resizing the via shape outward on the under-enclosed side. Trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 confirms that resizing V2 shapes in x by hundreds of dbu while keeping M3 fixed clears enclosure violations without introducing new M3 spacing or width errors.

## Instance-Move Repairs Touching M3 (unit_gate Channel)

All four unit_gate trials (trial:i02.ug.leaf_0003.03, trial:i02.ug.leaf_0010.06, trial:i03.ug.leaf_0002.01, trial:i04.ug.leaf_0001.00) were accepted with decision gated_in and conn_preserved true, and none introduced violations outside the crop window (n_new_out_of_crop was 0 in every case). This means move_instance operations that shift M3-bearing instances are safe to gate in when connectivity is preserved and no new out-of-crop errors are introduced.

Move magnitudes observed on the y-axis across unit_gate trials are ±24, ±48, ±72, and ±96 dbu (trial:i02.ug.leaf_0010.06, trial:i03.ug.leaf_0002.01). On the x-axis, small moves of -16 dbu were used in trial:i02.ug.leaf_0003.03 and trial:i04.ug.leaf_0001.00. No x-axis moves larger than 16 dbu appear in the unit_gate record for M3.

For large multi-instance repairs, y-axis moves cluster at multiples of 24 dbu (24, 48, 72, 96). Trial:i02.ug.leaf_0010.06 moved 24 instances simultaneously with displacements of ±24 and ±72 dbu and resolved 26 in-crop violations. Trial:i03.ug.leaf_0002.01 moved 20 instances with ±48 and ±96 dbu displacements and resolved 35 in-crop violations. Prefer coordinated multi-instance moves in the y direction when the violation cluster spans multiple adjacent units; trial:i03.ug.leaf_0002.01 demonstrates that moving groups of instances in opposite directions (some +48/+96, some -48/-96) clears spacing violations between neighboring M3 features.

## M3 Polygon End Resizing

Trial:i02.ug.leaf_0010.06 included twelve resize_end operations on M3 polygons (polygons p1826, p1833, p1831, p1792, p1786, p1806, p1845, p1844, p1857, p1734, p1757, p1749), all on the y-axis, with deltas of +72 dbu (high end) or +24 dbu (high end) or +24 dbu (low end) or +72 dbu (low end). These resize_end ops were applied concurrently with the matching move_instance ops in the same trial, and the combined set resolved 26 in-crop violations. Resizing M3 polygon ends in y by 24 or 72 dbu, paired with instance moves of the same magnitude, maintains V3.M3.EN.1 enclosure (minimum 5 nm on two opposite sides) as the via moves with the metal.

Never apply resize_end to an M3 polygon end in isolation if the associated via (V3) is not also moved or if the resulting M3 tip length would fall below 36 nm: tips shorter than 36 nm are subject to M3.S.2 (tip-to-side 25 nm minimum) and M3.S.3/M3.S.4/M3.S.5 (tip-to-tip 27-31 nm minimum), which are stricter than the side-to-side M3.S.1 rule (18 nm). Trial:i02.ug.leaf_0010.06 confirmed that coordinated resize_end plus move_instance avoids new M3 spacing errors (n_new_out_of_crop = 0).

## Spacing Rule Sensitivity by Edge Classification

M3.S.1 (18 nm side-to-side) applies only when both opposing edges are longer than 36 nm. M3.S.2 (25 nm tip-to-side) triggers when one edge is 36 nm or shorter and the other is longer than 36 nm. M3.S.3 (27 nm tip-to-tip) applies when both edges are between 24 nm and 36 nm inclusive. M3.S.4 (31 nm tip-to-tip) applies when both edges are shorter than 24 nm. M3.S.5 (31 nm tip-to-tip) applies when one edge is in [24,36] nm and the other is below 24 nm. M3.S.6 adds a 20 nm euclidean corner-to-corner floor.

The graduated spacing requirements mean that shortening an M3 tip from side-class (>36 nm) to wide-tip-class (24-36 nm) changes the applicable spacing from M3.S.1 (18 nm) to M3.S.2 or M3.S.3 (25-27 nm). Because trial:i02.ug.leaf_0010.06 performed resize_end ops of 24 and 72 dbu without introducing new spacing violations, those resizes did not push any tip into a narrower class in a context where the neighbor was too close to satisfy the stricter rule.

## Area Rule

M3.A.1 requires minimum M3 area of 504 nm-sq. No trial in this history recorded an M3.A.1 violation introduced by a repair, but resize_end operations that shrink an M3 polygon end (negative delta_dbu not observed in the record for M3 resizes) could reduce area below threshold. All measured M3 resize_end operations in trial:i02.ug.leaf_0010.06 were positive (expanding the polygon end), which is consistent with avoiding area underrun.

## Connectivity Preservation Requirement

All five trials in this history preserved connectivity (conn_preserved true in every record). The gated_in decision in unit_gate trials requires conn_preserved. Do not commit any repair that breaks a net on M3 or on via layers V2/V3 that land on M3. Trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 (cu_pool) and all four unit_gate trials confirm that the repair engine gates out trials that would disconnect nets, so every accepted result in this history is connectivity-safe.

## Out-of-Crop Violation Budget

All unit_gate trials in this history report n_new_out_of_crop of 0. Repairs applied to M3 via instance moves or polygon resizes must not push violations outside the repair crop window. Trial:i02.ug.leaf_0010.06 (26 in-crop resolutions, 0 out-of-crop) and trial:i03.ug.leaf_0002.01 (35 in-crop resolutions, 0 out-of-crop) demonstrate that large coordinated move sets can resolve many violations simultaneously without exporting new errors to neighboring regions.