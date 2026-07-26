## Via Geometry Repair for V2 Enclosure Rules (V2.M3.EN.2, V2.M3.AUX.2)

Resizing V2 shapes along the x-axis within a VIA cell, paired with compensating x-axis moves to maintain alignment, directly reduces M3-layer DRC error counts. In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, five operations on the cu_pool channel (three x-axis resize_via_shape at +264, +288, and +264 dbu; two x-axis move_via_shape at -144 and +144 dbu) applied to cell VIA_VIA23_1_3_36_36 reduced violations across two windows by 78 in total (139→97 in unit:leaf_0019, 154→118 in unit:leaf_0020), with connectivity preserved. The pattern is: move the via shape inward on the approaching edge, then resize both the resized shape and adjacent shapes outward to satisfy the 5 nm projection enclosure required by V2.M3.EN.2 and the coincidence condition of V2.M3.AUX.2. Apply positive x-resizes of at least 264 dbu to the shapes requiring enclosure extension before issuing compensating moves; the move-then-resize sequence keeps net centroid displacement small while expanding coverage.

Never resize only one side of a V2 shape when V2.M3.AUX.2 is the active rule: that rule requires the via to share M3 edges on the sides perpendicular to M3 length (two coincident edges required). A one-sided resize produces asymmetric enclosure and fails the coincident-edge count, as indicated by the rule's `interacting(v2_aux2_coinc, 2)` check. trial:i01 addressed this by resizing multiple indexed shapes (shape_index 0, 1, and 2) in a coordinated sequence rather than touching a single shape.

## Instance-Level Moves for M3 Spacing Violations

Small x-axis instance moves clear M3 spacing violations when the offending geometry belongs to a cell that can be shifted without dragging out-of-crop errors. trial:i02.ug.leaf_0003.03 moved instance i0358 by [-16, 0] dbu on the unit_gate channel, which introduced 2 new in-crop DRC reductions (n_new_in_crop: 2) with zero new out-of-crop violations and conn_preserved true. Use moves of this magnitude (-16 dbu, i.e., approximately 1.6 nm at 1 dbu = 0.1 nm) as a minimum step size when M3 tip-to-side (M3.S.2) or corner spacing (M3.S.6) shortfalls are small.

For violations distributed across many instances in a larger region, coordinated y-axis instance moves are effective. trial:i02.ug.leaf_0010.06 moved 24 instances along y at four discrete deltas (+72, +24, -24, -72 dbu), which cleared 26 in-crop violations with no out-of-crop introductions across M3, M4, M5, V3, and V4. trial:i03.ug.leaf_0002.01 moved 20 instances along y at three deltas (-48, -48, -96, -96 dbu per repeated pair, and +48 in two instances), clearing 35 in-crop violations under the same connectivity-preserved condition. The ±96 dbu (≈9.6 nm) moves are the largest single-axis displacement confirmed to resolve M3 spacing violations without introducing new ones, making 96 dbu a safe upper-bound step for y-axis instance moves targeting M3.S.1 or M3.S.2 side-to-side and tip-to-side spacing shortfalls.

Do not apply x-axis instance moves to fix y-axis spacing violations or vice versa: trial:i02.ug.leaf_0003.03 used an x-move for an x-axis spacing context; trial:i02.ug.leaf_0010.06 and trial:i03.ug.leaf_0002.01 used y-moves for y-axis spacing contexts. Mixing axes for these correction types was not demonstrated to succeed in any measured record.

## Polygon End Resizes for M3 Width and Spacing Compliance

When instance moves alone do not close all spacing gaps—particularly where M3 polygon ends are misaligned relative to shifted neighbor instances—resize_end operations on specific polygon ids supply the remaining correction. trial:i02.ug.leaf_0010.06 included 12 resize_end operations on y-axis polygon ends (six at +72 or -72 dbu, six at +24 or -24 dbu), matching the same discrete steps used for instance moves in that same trial. Apply resize_end at matching magnitudes to the endpoints that face the moved instance so that the M3 edge-to-edge relationship is maintained. Resize the high end upward and the low end downward at matching magnitudes; the pairing of +72/−72 and +24/−24 dbu per trial:i02.ug.leaf_0010.06 confirmed zero new out-of-crop violations.

Ensure that any polygon end resize keeps M3 width at or above 18 nm (M3.W.1) and that polygon area does not drop below 504 nm² (M3.A.1). The minimum width rule binds first: a resize_end shrinking a polygon end into a width violation will produce a new M3.W.1 error even if it resolves a spacing error. No resize_end operation in the measured history reduced polygon dimensions; all measured resize_end deltas were positive or outward, which is consistent with avoiding M3.W.1 and M3.A.1 regressions.

## V3 Enclosure Integrity During Multi-Instance Moves

Trials touching M3 together with V3 (trial:i02.ug.leaf_0003.03, trial:i02.ug.leaf_0010.06, trial:i03.ug.leaf_0002.01) all preserved connectivity and introduced no out-of-crop V3.M3.EN.1 violations. V3.M3.EN.1 requires 5 nm enclosure on at least one pair of opposite sides. When moving M3-connected instances along y, move all instances and associated polygon ends by the same delta so that V3 via positions remain centered inside M3 relative to the movement. In trial:i02.ug.leaf_0010.06, the polygon end resizes at +72 and -72 dbu matched the outer instance moves at ±72 dbu, preserving the enclosure margin on both sides simultaneously. Mismatched resize and move magnitudes on opposite ends would break this symmetry and risk a V3.M3.EN.1 shortfall.

## Channel Routing and Decision Outcomes

The cu_pool channel (trial:i01) operates directly on via cell geometry and produces `decision: applied` outcomes that commit the fix unconditionally after DRC count reduction is confirmed. The unit_gate channel (trials i02, i03) produces `decision: gated_in` outcomes gated on conn_preserved and n_new_out_of_crop = 0; moves that introduce any new violation outside the crop window are rejected by this gate. Prefer the unit_gate channel for instance-level moves on M3 since it provides a built-in connectivity and out-of-crop guard. Use the cu_pool channel only when the repair targets a named via cell (e.g., VIA_VIA23_1_3_36_36) and the fix is a direct geometric reshape of V2 within that cell.

## Quantitative DRC Reduction Reference

| Trial | Channel | Ops | Layers | In-crop reduction |
|---|---|---|---|---|
| i01.cu.def:VIA_VIA23_1_3_36_36.00 | cu_pool | 5 (resize+move V2, x-axis) | M2, M3, V2 | 78 total (42 + 36) |
| i02.ug.leaf_0003.03 | unit_gate | 1 (move_instance, x=-16) | M3, M4, V3 | 2 |
| i02.ug.leaf_0010.06 | unit_gate | 36 (24 move_instance + 12 resize_end, y-axis) | M3, M4, M5, V3, V4 | 26 |
| i03.ug.leaf_0002.01 | unit_gate | 20 (move_instance, y-axis) | M3, M4, M5, V3, V4 | 35 |

The largest single-trial in-crop reduction on M3 came from the 20-instance y-axis move set in trial:i03.ug.leaf_0002.01 (35 violations cleared). The highest ops-to-reduction efficiency was trial:i02.ug.leaf_0003.03 (1 op, 2 violations). Scale op count proportionally to locus area and violation density: trial:i02.ug.leaf_0010.06's 36-op batch covered a locus of approximately 13608×11648 dbu with 26 violations; trial:i03.ug.leaf_0002.01's 20-op batch covered approximately 13608×13148 dbu with 35 violations, both within Block6.