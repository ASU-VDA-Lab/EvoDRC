## Via-Cell Operations That Indirectly Modify M6

Both recorded trials operated exclusively on V5 and M5 shapes inside VIA_VIA56 cell definitions; M6 appears in `touched_layers` as a passive participant whose DRC violations were reduced as a consequence of those shape changes. No direct M6 geometry edits were issued in either trial (trial:i04.cu.def:VIA_VIA56_2_1_66_58.00, trial:i04.cu.def:VIA_VIA56_2_2_66_58.01).

## V5.M6.EN.2 and V5.M6.AUX.2: Enclosure and Width-Match Violations Resolved by V5 Resizing

V5.M6.EN.2 requires M6 to enclose V5 by at least 11 nm on two opposite sides in both X and Y. V5.M6.AUX.2 requires V5 to be exactly as wide as M6 in the direction perpendicular to M6's length. Both rules are violated when a V5 shape protrudes past or falls short of the M6 boundary. The successful repair pattern — confirmed in trial:i04.cu.def:VIA_VIA56_2_1_66_58.00 and trial:i04.cu.def:VIA_VIA56_2_2_66_58.01 — is to expand V5 shapes in Y via `resize_via_shape` (delta_dbu=512 per shape) combined with compensating `move_via_shape` adjustments (delta_dbu=±132 in Y) so that V5 remains centered within M6 and the 11 nm enclosure margin is satisfied on both the top and bottom edges simultaneously. Do not resize V5 in X when the violation axis is Y; the enclosure check is two-sided and the AUX.2 width-match check is directional.

In trial:i04.cu.def:VIA_VIA56_2_1_66_58.00 (2 V5 shapes, 5 ops, delta_total=-2) and trial:i04.cu.def:VIA_VIA56_2_2_66_58.01 (4 V5 shapes, 9 ops, delta_total=-4), the pattern scales linearly: each additional V5 shape requires one move and one resize op, and the DRC reduction scales proportionally with shape count.

## M5 Resize Accompanies V5 Changes

Both trials also issued a Y-axis `resize_via_shape` on the M5 shape (delta_dbu=248) within the same via cell before modifying V5 (trial:i04.cu.def:VIA_VIA56_2_1_66_58.00, trial:i04.cu.def:VIA_VIA56_2_2_66_58.01). Although M5 is not governed by M6 DRC rules, this M5 resize appears to be a prerequisite step that creates room for the V5 expansion without introducing M5-side violations. Do not omit the M5 resize when applying the V5 expansion pattern to VIA_VIA56_2_x cells.

## Op Ordering Within a Via Cell

Both successful trials apply ops in this fixed order: (1) resize M5 in Y, (2) move V5 shape 0 in Y, (3) resize V5 shape 0 in Y, then repeat move+resize for each additional V5 shape in ascending shape_index order, alternating move direction (−132 for even-indexed shapes, +132 for odd-indexed shapes) (trial:i04.cu.def:VIA_VIA56_2_1_66_58.00, trial:i04.cu.def:VIA_VIA56_2_2_66_58.01). Applying resizes before the centering move, or interleaving shapes out of order, is not validated by the recorded history.

## M6 Grid and Width Rules Are Not the Active Failure Mode Here

M6.AUX.1 (horizontal edges on 32 nm grid), M6.W.1 (min vertical width 32 nm), M6.W.2 (max vertical width 640 nm), M6.W.3/W.4 (forbidden even-multiple widths), M6.W.5 (min horizontal width 44 nm), M6.S.1–S.5 (spacing), M6.AUX.2 (track centering), M6.AUX.3 (no bends), M6.AUX.4 (wide polygon track edge constraint), and V6.M6.EN.1 (V6 enclosure) are not cited as the source of the violations reduced in these trials. The recorded delta_total reductions (trial:i04.cu.def:VIA_VIA56_2_1_66_58.00, trial:i04.cu.def:VIA_VIA56_2_2_66_58.01) are attributable to V5.M6.EN.2 and V5.M6.AUX.2 resolution. No repair guidance for these other M6 rules is grounded in this iteration's measured history.

## Connection Preservation

Both trials report `conn_preserved=true`, confirming that the V5 expansion strategy does not break electrical connectivity (trial:i04.cu.def:VIA_VIA56_2_1_66_58.00, trial:i04.cu.def:VIA_VIA56_2_2_66_58.01). Expanding V5 fully within an already-enclosing M6 keeps the via electrically valid.