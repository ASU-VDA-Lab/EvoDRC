## Repair Patterns Observed

**End-extension of M2 segments resolves tip-related spacing and enclosure violations without introducing new errors.** In trial:i03.ug.whole_design.00, seven M2 polygons (p2071, p2020, p2072, p2086, p1946, p1903, p1991) had their high-x ends extended by 116 or 152 dbu. The gated result showed zero new violations in-crop and zero new violations out-of-crop, and connectivity was fully preserved. The extension amounts (116 dbu ≈ 11.6 nm, 152 dbu ≈ 15.2 nm) are sub-threshold relative to M2.W.1 (minimum width 18 nm) and M2.S.1 (minimum side spacing 18 nm), confirming that these small positive deltas corrected deficient enclosure or tip-spacing without pushing any edge into a new spacing conflict on the side-to-side axis.

**Smaller resize increments (+10 dbu) on M2 polygons are sufficient for marginal violations.** In trial:i04.ug.whole_design.00, polygons p1990, p1923, and p1920 were each resized by +10 dbu in x. Together with instance repositioning across multiple layers, the result was gated_in with zero new violations and preserved connectivity. This establishes that not every M2 repair requires the 116–152 dbu extensions seen in trial:i03.ug.whole_design.00; a +10 dbu correction suffices when the underlying spacing deficit is small.

**M2 polygon moves (not just resizes) can also be part of a clean repair.** In trial:i04.ug.whole_design.00, polygon p1684 was translated +80 dbu on x without any resize. The move was applied alongside resizes of other M2 polygons and was accepted with no new violations. This confirms that rigid body translation of an M2 segment is a valid repair primitive when it does not tighten adjacent spacings.

## Instance Co-movement

**All M2 end-extension and move operations in the measured history were accompanied by co-movement of associated cell instances.** In trial:i03.ug.whole_design.00, every M2 polygon resize_end was paired with a move_instance of +96 dbu in x for the corresponding instance. In trial:i04.ug.whole_design.00, instance moves ranged from -96 dbu to +96 dbu and -48 dbu in x, matching the varied delta patterns applied to M2 and other layers. Attempting to resize or move an M2 segment without co-moving attached instances risks disconnecting vias or violating V1.M2.AUX.2 (V1 must exactly match M2 width along the perpendicular direction) and V1.M2.EN.2 (minimum enclosure of V1 by M2 on two opposite sides is 5 nm).

## Via Enclosure Interactions

**V2 reshaping that touches M2 can reduce M2-layer violation counts.** In trial:i02.cu.def:VIA_VIA23_1_3_36_36.00, a sequence of five ops on V2 (move -144 dbu x then resize +288 dbu x for the via body, plus independent moves and resizes of associated M2/M3 enclosure shapes) reduced the total violation count by 78. The touched layers included M2, confirming that V2.M2.EN.1 failures (minimum enclosure of V2 by M2 on at least two opposite sides ≥ 5 nm) can contribute substantially to the M2-layer violation tally and that centering the V2 within the M2 landing pad—via a negative move followed by symmetric positive resize—is a reliable fix pattern.

**The V2 repair in trial:i02.cu.def:VIA_VIA23_1_3_36_36.00 used a net-zero translation (move -144, net resize +288) to re-center the via.** The delta of -144 dbu followed by a +288 dbu resize achieves a symmetric 144 dbu (14.4 nm) expansion on each side of the V2 shape, which, given the V2.M2.EN.1 requirement of 5 nm enclosure on two opposite sides, implies the original layout had an enclosure deficit on at least one side that the symmetric expansion corrected.

## Spacing Rule Hazards

**Side-to-side spacing (M2.S.1, minimum 18 nm) is the binding constraint for x-axis resizes.** All accepted M2 polygon extensions in trial:i03.ug.whole_design.00 and trial:i04.ug.whole_design.00 produced zero new in-crop violations. Because M2.S.1 applies when both edges are longer than 36 nm, end-extensions that lengthen an M2 tip edge to exceed 36 nm will promote that edge into the M2.S.1 regime; the absence of new violations in these trials confirms the post-extension side spacings remained ≥ 18 nm.

**The M2.S.7 forbidden-zone rule (tip-to-tip gap of 18 nm co-located with side-to-side spacing ≤ 32 nm) creates a coupled constraint: fixing a tip spacing may expose a side spacing violation and vice versa.** The clean gate outcomes in trial:i03.ug.whole_design.00 and trial:i04.ug.whole_design.00 confirm that the specific end-extensions applied (116–152 dbu and 10 dbu respectively) successfully navigated this coupling. Repairs that extend M2 tip ends should verify that the resulting parallel-run geometry does not enter the M2.S.7 forbidden region (parallel run length < 35 nm with side spacing ≤ 32 nm).

**M2.S.6 corner-to-corner spacing (20 nm, euclidean) is distinct from the projection-based rules and must be checked independently after any move or resize.** No trial in the measured history isolated an M2.S.6 violation specifically, but all accepted trials confirmed zero new violations across the whole design, establishing that the repair magnitudes applied (10–152 dbu) did not create corner violations.

## Area Compliance

**No M2.A.1 violations (minimum area 504 nm²) were introduced by any measured trial.** The smallest resize applied to an M2 polygon was +10 dbu (trial:i04.ug.whole_design.00), and all repairs were accepted with zero new violations. This confirms that the polygons in question already exceeded the 504 nm² floor by enough margin that small positive deltas did not require separate area checks in these cases.

## Nonorthogonal Geometry

**All M2 ops in the measured history are purely orthogonal (x-axis moves and resizes only).** The GEOMETRY.NONORTHOGONAL rule applies to M2 and will fire on any edge with angle not in {0°, 90°, 180°, 270°}. No diagonal or angled edges were introduced in trial:i02.cu.def:VIA_VIA23_1_3_36_36.00, trial:i03.ug.whole_design.00, or trial:i04.ug.whole_design.00, consistent with their zero-new-violation outcomes.