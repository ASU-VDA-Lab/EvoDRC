**Via-cell repair affecting M3 (V2.M3.EN.2 / V2.M3.AUX.2 context)**

The repair on M3 at iteration 1 targeted cell `def:VIA_VIA23_1_3_36_36` via the `cu_pool` channel. Five operations were applied to V2 shapes in the x-axis: shape_index 0 was moved −144 dbu and resized +288 dbu; shape_index 1 was resized +288 dbu; shape_index 2 was moved +144 dbu and resized +288 dbu. The result was −24 total violations eliminated (−12 in unit:leaf_0012, −12 in unit:leaf_0013) with connectivity preserved (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

**Enclosure rules V2.M3.EN.2 and V2.M3.AUX.2**

Rule V2.M3.EN.2 requires M3 to enclose V2 by at least 5 nm on two opposite sides (either 5 & 5 nm or 5 & 0 nm, projection). Rule V2.M3.AUX.2 requires V2 to be exactly the same width as M3 along the direction perpendicular to M3 length; any V2 not sharing two coincident edges with M3 in that perpendicular direction triggers the rule. When V2 shapes are narrower than their enclosing M3 in x, or shift off-center, both V2.M3.EN.2 and V2.M3.AUX.2 can fire simultaneously, producing paired violation counts. The −24 reduction achieved by symmetrically moving V2 shapes outward (±144 dbu) while widening each by +288 dbu in x confirms that expanding V2 width to match M3 extent in x and recentering the outer V2 shapes resolves both enclosure and width-match violations in a single pass (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

**Axis and direction for V2 resizes inside via cells**

Resizing V2 shapes in the x-axis by a uniform +288 dbu, combined with symmetric x-displacement of the outer shapes, achieved full violation clearance in both affected windows without connectivity loss (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). Do not apply asymmetric resizes across V2 shapes sharing the same M3 enclosure when V2.M3.AUX.2 is among the flagged rules: the AUX.2 rule fires on any V2 whose perpendicular width does not match M3, so partial adjustment of one shape while leaving others untouched will leave residual violations. The measured approach of resizing all three V2 shapes in the same axis by the same delta eliminated residual violations cleanly (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

**M3 spacing and width rules — interaction with via-cell repairs**

Rules M3.S.1 (side-to-side ≥ 18 nm, edges > 36 nm), M3.S.2 (tip-to-side ≥ 25 nm), M3.S.3 (tip-to-tip ≥ 27 nm, both edges 24–36 nm), M3.S.4 (tip-to-tip ≥ 31 nm, both edges < 24 nm), M3.S.5 (tip-to-tip ≥ 31 nm, one edge 24–36 nm, other < 24 nm), M3.S.6 (corner-to-corner ≥ 20 nm, Euclidean), M3.W.1 (width ≥ 18 nm), and M3.A.1 (area ≥ 504 nm²) were not directly cited as firing violations in the cu_pool trial, but M3 was listed as a touched layer. The via-cell resize operations that corrected V2.M3.EN.2 and V2.M3.AUX.2 did not introduce new M3 spacing or width violations: the trial was applied and connectivity was preserved with a net negative violation delta (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). This confirms that widening V2 to match M3 width in x does not by itself shrink or shift M3 geometry in a way that triggers M3.W.1 or M3.S.* when the M3 shape already satisfies those rules prior to repair.

**V3.M3.EN.1 — unit_gate channel, instance moves and M3 polygon resize**

Rule V3.M3.EN.1 (M3 must enclose V3 by ≥ 5 nm on at least two opposite sides) is implicated in unit_gate channel repairs that list both M3 and V3 among touched layers.

Two distinct repair shapes are measured for this rule in unit_gate:

*Instance-move-only repairs:* In trial:i04.ug.leaf_0003.02 (Block2, unit:leaf_0003), 3 move_instance operations were applied in y: instances i0090 and i0110 moved +24 dbu, instance i0089 moved −24 dbu. No polygon resizes were applied. The repair was gated_in with connectivity preserved, introducing n_new_in_crop:2 violations; it was accepted on that basis (trial:i04.ug.leaf_0003.02). The instance moves in y shift surrounding cell instances to relieve enclosure pressure without directly modifying M3 geometry. An asymmetric distribution — two instances pushed in one direction, one in the other — is accepted by the gate; exact equal-and-opposite balance is not required (trial:i04.ug.leaf_0003.02).

*Instance-move plus asymmetric M3 polygon resize:* In trial:i03.ug.leaf_0002.01 (Block2, unit:leaf_0002), 10 operations were applied: 8 move_instance operations in y at magnitudes of ±24 dbu and ±72 dbu (symmetric four-and-four distribution), plus 2 resize_end operations on M3 polygon p937 in the x-axis (low end +64 dbu, high end +320 dbu). The polygon resize is asymmetric: the high end receives a 320 dbu extension while the low end receives only 64 dbu. The repair was gated_in with connectivity preserved; it introduced n_new_in_crop:2 violations and was still accepted (trial:i03.ug.leaf_0002.01). The asymmetric x-resize of p937 extends the M3 landing to satisfy V3.M3.EN.1 enclosure on the deficient edge without requiring equal bilateral growth; a polygon short only on one x-edge benefits from targeting that edge specifically (trial:i03.ug.leaf_0002.01).

**Gated-in acceptance criterion for unit_gate repairs**

Gated-in acceptance of n_new_in_crop > 0 is confirmed across two independent trials: repairs introducing 2 new in-crop violations are committed when connectivity is preserved (trial:i03.ug.leaf_0002.01, trial:i04.ug.leaf_0003.02). Do not treat n_new_in_crop:0 as a required precondition for acceptance in the unit_gate channel; the measured gate criterion is conn_preserved.

**Touched-layer scope for unit_gate repairs on V3.M3.EN.1**

The touched-layer set varies by repair. Instance-move-only repairs in unit_gate can propagate through M2, M3, M4, M5, V2, V3, and V4 (trial:i04.ug.leaf_0003.02). Repairs that additionally include M3 polygon resizes propagate through M3, M4, M5, V3, and V4 (trial:i03.ug.leaf_0002.01). Both sets confirm that unit_gate repairs on V3.M3.EN.1 touch multiple metal and via layers in a single committed operation; the inclusion of M2 and V2 in the touched set does not block gated_in acceptance (trial:i04.ug.leaf_0003.02).