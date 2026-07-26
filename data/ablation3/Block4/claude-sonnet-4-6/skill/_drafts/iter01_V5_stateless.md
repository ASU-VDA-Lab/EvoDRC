## Effective Repair Pattern for V5 Enclosure Violations in VIA56 Cells

All successful V5 repairs in this iteration operated on V5 shapes within VIA_VIA56 cell definitions via the cu_pool channel. The pattern used in both applied trials is a paired move-then-resize on the y-axis: each V5 shape is first displaced outward (away from the cell's y-center) and then grown in the y dimension. In trial:i01.cu.def:VIA_VIA56_2_1_66_58.00, shape_index 0 was moved by -132 dbu then resized by +512 dbu in y, while shape_index 1 was moved by +132 dbu then resized by +512 dbu in y. The same delta magnitudes were reused for all four shapes in trial:i01.cu.def:VIA_VIA56_2_2_66_58.01, where shape indices 0 and 1 received -132 dbu moves and shape indices 2 and 3 received +132 dbu moves, each followed by +512 dbu resize in y. Both trials were accepted (decision: "applied") and preserved connectivity.

## Shape Count and Violation Budget

The number of V5 shapes per VIA56 cell directly predicts how many violations a single cu_pool trial will close. VIA_VIA56_2_1_66_58 carries 2 V5 shapes and its repair reduced the design-wide violation count by 2 (trial:i01.cu.def:VIA_VIA56_2_1_66_58.00, before: 147, after: 145). VIA_VIA56_2_2_66_58 carries 4 V5 shapes and its repair reduced the count by 4 (trial:i01.cu.def:VIA_VIA56_2_2_66_58.01, before: 147, after: 143 as measured from the original baseline). Allocate cu_pool budget proportionally: a 4-shape VIA56 cell returns twice the delta of a 2-shape cell for the same per-shape operation.

## Symmetric Outward Displacement is Required

Do not move all shapes in the same direction. The measured pattern is strictly symmetric: shapes below the cell's y-midpoint move in the negative-y direction; shapes above move in the positive-y direction. Both groups receive the same resize magnitude (+512 dbu in y). This symmetric outward shift is consistent with the two-opposite-sides requirement of V5.M5.EN.1 (minimum 11 nm enclosure by M5 on at least two opposite sides) and V5.M6.EN.2 (minimum 11 nm enclosure by M6 on two opposite sides). Asymmetric moves would resolve enclosure on one side while violating it on the other and are not supported by any applied trial in this history.

## All V5 Repairs Co-Touch M5 and M6

Every trial that modified V5 shapes listed M5, M6, and V5 together in touched_layers (trial:i01.ug.whole_design.00, trial:i01.cu.def:VIA_VIA56_2_1_66_58.00, trial:i01.cu.def:VIA_VIA56_2_2_66_58.01). This is structurally required by V5.AUX.1 (V5 must be inside both M5 and M6) and V5.M6.AUX.2 (V5 must match M6 width exactly in the direction perpendicular to M6 length). Any operation that repositions or resizes a V5 shape must simultaneously be consistent with the enclosing M5 and M6 geometries; cu_pool operations on VIA56 cells inherently satisfy this because the cell definition holds V5, M5, and M6 together.

## Unit-Gate Acceptance Does Not Imply Zero Residual V5 Violations

The unit_gate trial i01.ug.whole_design.00 was accepted (decision: "gated_in") with conn_preserved and deltas showing zero new in-crop or out-of-crop violations introduced by its three ops (move polygon p1402 +64 dbu in y, move instances i0234 and i0305 by +64 dbu in y). However, the subsequent cu_pool trials show the design still held 147 V5 violations before those cu_pool fixes were applied. Unit-gate acceptance reflects that the trigger move did not worsen the violation count, not that the design was clean. Do not treat unit_gate "gated_in" as a signal that V5 DRC is resolved; use the running violation count from cu_pool deltas as the authoritative metric.

## Connectivity is Preserved by Outward Resize Operations

All three trials in this iteration report conn_preserved: true. The outward-move-then-resize pattern on V5 shapes does not sever net connectivity because resizing a via shape in y increases its overlap with the enclosing M5 and M6 metals rather than reducing it. Apply this repair with confidence that the move delta of 132 dbu outward combined with a +512 dbu y-resize maintains the via's electrical connection on both the M5 and M6 sides, as confirmed by trial:i01.cu.def:VIA_VIA56_2_1_66_58.00 and trial:i01.cu.def:VIA_VIA56_2_2_66_58.01.

## Corner-to-Corner and Projection Spacing (V5.S.1 / V5.S.2 / V5.S.3)

No spacing violations (V5.S.1, V5.S.2, V5.S.3) were introduced by any repair in this iteration; all trials report zero new out-of-crop violations and were accepted without debt entries. The outward y-displacement of 132 dbu per shape increases inter-shape distance within the same cell only if those shapes occupy opposite sides. Within-cell spacing between shapes on the same net is governed by V5.S.1 (minimum 33 nm, projection); the measured move magnitude of 132 dbu outward from center does not collapse adjacent shapes toward each other, consistent with the zero new violations observed in trial:i01.cu.def:VIA_VIA56_2_2_66_58.01, which moved four shapes simultaneously without triggering spacing errors.