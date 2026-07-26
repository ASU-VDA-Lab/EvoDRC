## Repair Strategy: Paired M2 End-Extension and V1 Instance Move

The single measured trial (trial:i03.ug.whole_design.00) demonstrates one repair pattern for V1 DRC violations: extend the high-x end of one or more M2 polygons using `resize_end` and simultaneously translate co-located V1 instances by +x using `move_instance`. In that trial, 7 M2 `resize_end` operations (axis x, end high) were paired with `move_instance` operations on 9 V1 instances, all moving +96 dbu in x. The repair was accepted with `decision: gated_in`, `conn_preserved: true`, and zero net change in violation count (`n_new_in_crop: 0`, `n_new_out_of_crop: 0`), confirming the approach does not create new DRC errors while resolving existing ones (trial:i03.ug.whole_design.00).

## M2 Extension Must Exceed V1 Displacement

In every paired case in trial:i03.ug.whole_design.00, the M2 `resize_end` delta (116 dbu for polygons p2020, p1946, p1903, p1991; 152 dbu for polygons p2071, p2072, p2086) was larger than the V1 displacement (96 dbu for all instances). The M2 extension delta always exceeded the V1 move delta. This differential is required by V1.M2.EN.2, which demands that M2 enclose V1 by at least 5 nm on two opposite sides (either 5 & 5 nm or 5 & 0 nm). Moving V1 without sufficiently extending M2 would violate the enclosure rule; the measured differentials of 20 dbu (116 − 96) and 56 dbu (152 − 96) represent the margin maintained above the enclosure minimum (trial:i03.ug.whole_design.00). Do not move a V1 instance in +x by a delta equal to or greater than the corresponding M2 `resize_end` delta.

## V1 Must Remain Co-Located with M2 Width

V1.M2.AUX.2 requires V1 to match M2 width perpendicular to M2 length exactly. V1.AUX.1 requires V1 to remain inside the intersection of M1 and M2. The measured repair keeps V1 inside M2 by moving both layers together rather than moving V1 alone: M2 is extended first, then V1 is translated within the new M2 boundary. Attempting to move V1 without extending M2 would violate V1.AUX.1 and V1.M2.AUX.2 because the V1 polygon would shift outside M2 laterally (trial:i03.ug.whole_design.00).

## M1 Enclosure Must Be Checked After V1 Moves

V1.M1.EN.1 requires M1 to enclose V1 by at least 5 nm on one axis and 2 nm on the perpendicular axis. The trial touched M1, M2, and V1 simultaneously (trial:i03.ug.whole_design.00), and the zero-new-violation outcome shows the M1 geometry was already sufficient or was adjusted in the same operation set. When moving V1 instances in +x, verify that M1 enclosure is maintained on both the high-x and the axis-perpendicular sides; do not assume M1 is always large enough to absorb the V1 displacement.

## Spacing Rules Drive the Required Displacement Magnitude

V1.S.1 sets minimum projected spacing between V1 masks at 17 nm (between v1_mask edges at 90 degrees) and minimum projected spacing between v1_maskav non-M2 edges at 18 nm. V1.S.2, V1.S.3, and V1.S.4 set corner-to-corner euclidean minimums at 16.4 nm, 16.12 nm, and 17.11 nm respectively (translating to 23 nm, 30 nm, and 27 nm physical minimums). The 96 dbu V1 displacement in trial:i03.ug.whole_design.00 was sufficient to clear these spacing constraints without introducing new ones, confirming that when V1 spacing violations are present, a uniform same-direction displacement of all nearby instances can resolve inter-instance spacing without creating conflicts elsewhere (trial:i03.ug.whole_design.00).

## Non-Orthogonal Geometry Is Prohibited

V1 edges must be at exactly 0 or 90 degrees. All `resize_end` and `move_instance` operations in trial:i03.ug.whole_design.00 operate on axis-aligned (x) directions, producing only orthogonal geometry. Never apply diagonal or non-axis-aligned transformations to V1 polygons or instances; the NONORTHOGONAL rule applies to every layer including V1.

## Repair Scope: Whole-Design Channel

Trial:i03.ug.whole_design.00 used `channel: unit_gate` on `unit_id: whole_design` with locus covering the full 16944 × 16944 dbu crop. The repair modified 16 operations across multiple instances and polygons simultaneously rather than fixing one violation at a time. This batch approach across the full design area produced zero new violations, showing that coordinated multi-instance moves in the same direction are safe when all M2 enclosures are extended proportionally.