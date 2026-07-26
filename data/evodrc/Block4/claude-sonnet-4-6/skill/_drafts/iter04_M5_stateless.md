## Via Cell Repair: M5 y-Resize Paired with V5 Repositioning

The only two committed repairs in this layer's history both target VIA_VIA56 cell definitions through the cu_pool channel. In trial:i04.cu.def:VIA_VIA56_2_1_66_58.00 and trial:i04.cu.def:VIA_VIA56_2_2_66_58.01, the operative pattern is identical on the M5 side: a single `resize_via_shape` on the M5 shape in the via cell, axis y, delta_dbu 160. The difference between the two trials is the number of V5 shapes repositioned (two in .00, four in .01); the M5 operation is the same in both. The trial with four V5 shape edits produced a net reduction of 4 violations (trial:i04.cu.def:VIA_VIA56_2_2_66_58.01), while the trial with two V5 shape edits produced a net reduction of 2 (trial:i04.cu.def:VIA_VIA56_2_1_66_58.00). Apply y-axis M5 enlargement inside via cell definitions when repairing V5.M5.EN.1 (minimum 11 nm enclosure of V5 by M5 on two opposite sides) or V5.M5 violations that co-occur with V5 shape adjustments.

Do not apply M5 resizes in isolation from the paired V5 moves: both committed trials moved each V5 shape by ±132 dbu in y before resizing it by 512 dbu in y, then enlarged M5 by 160 dbu in y (trial:i04.cu.def:VIA_VIA56_2_1_66_58.00, trial:i04.cu.def:VIA_VIA56_2_2_66_58.01). Applying the M5 resize without the V5 repositioning is not grounded in any successful outcome in this history.

The V5 moves use symmetric ±132 dbu offsets (move shape_index 0 by −132, move shape_index 1 by +132 in trial:i04.cu.def:VIA_VIA56_2_1_66_58.00), which centers the adjusted V5 shapes relative to the pre-edit position before the 512 dbu resize. The M5 160 dbu y-resize that follows extends the M5 footprint to satisfy V5.M5.EN.1's two-sided 11 nm enclosure requirement.

## M5 Grid Alignment Corrections Require Coordinated Instance Moves

Trial trial:i04.ug.leaf_0002.01 moved M5 polygon p1341 by 32 dbu in the x-direction under the group label `m5_align`, and bundled ten instance moves in the same operation. The instance moves carry x-deltas of 32 dbu for instances in the m5_align group (i0239, i0223, i0141, i0150, i0138) and 0 x-delta for the remaining instances (i0237, i0214, i0103, i0104, i0134). This trial touched layers M3, M4, M5, V3, V4 and was accepted as gated_in with conn_preserved=true and 2 new in-crop violations.

When correcting an M5 polygon to satisfy M5.AUX.2 (minimum-width M5 tracks must lie on vertical routing tracks at pitch 192 dbu, offset 48 dbu from origin), move all instances whose geometry references that track in the same operation. Applying the M5 polygon move without the dependent instance moves is not grounded in any committed result in this history.

M5.AUX.2 requires minimum-width M5 track centerlines to fall on positions satisfying `(cl − 48) mod 192 = 0` in x (i.e., x = 48, 240, 432, 624, … dbu). The 32 dbu x-shift applied in trial:i04.ug.leaf_0002.01 is consistent with correcting a track whose centerline was 32 dbu off the required grid position.

## Gated-In Acceptance: Connectivity Preservation Overrides In-Crop Violation Count

Two trials were accepted as gated_in despite introducing new in-crop violations: trial:i01.ug.leaf_0025.11 (9 new in-crop violations, 0 out-of-crop) and trial:i04.ug.leaf_0002.01 (2 new in-crop violations, 0 out-of-crop). Both carry `conn_preserved: true` and reason `"conn_preserved"`. Neither was rejected on the basis of the newly introduced violations.

Do not treat gated_in as equivalent to applied: no gated_in trial in this history appears in a subsequent design_state as a committed change. The applied commits are exclusively from the cu_pool channel (trial:i04.cu.def:VIA_VIA56_2_1_66_58.00, trial:i04.cu.def:VIA_VIA56_2_2_66_58.01). Unit_gate trials (trial:i01.ug.leaf_0025.11, trial:i04.ug.leaf_0002.01) remained gated_in only.

## Instance Y-Moves on M5-Touching Instances

Trial trial:i01.ug.leaf_0025.11 moved two instances (i0234, i0305) each by [0, 64] dbu, touching M5, M6, and V5. This trial was accepted gated_in with 9 new in-crop violations and is the only recorded unit_gate action from iter 1. The 64 dbu y-shift is not a multiple of the M5.S.2 minimum vertical spacing (40 nm) but is a multiple of 8 dbu (the implied grid resolution present throughout the history).

When moving instances that touch M5, ensure the resulting M5 geometry satisfies M5.W.5 (minimum vertical width 44 nm), M5.S.2 (minimum vertical spacing 40 nm), M5.S.3 and M5.S.4 (tip-to-tip spacing 40 nm on adjacent tracks), and M5.S.5 (minimum parallel run length 44 nm on adjacent tracks). The gated_in outcome of trial:i01.ug.leaf_0025.11 with 9 new in-crop violations indicates these constraints were not fully satisfied after the move, which is consistent with the trial never advancing to applied status in the recorded history.

## M5 Shape Constraints: Forbidden Width Values

M5.W.3 prohibits horizontal widths that are even-integer multiples of 24 nm: 48, 96, 144, 192, 240, 288, 336, 384, 432, 480 nm. M5.W.4 additionally prohibits widths of 72, 168, 264, 360, and 456 nm (widths that place a polygon across an even number of minimum-width routing tracks). When resizing M5 shapes horizontally — including the inside-cell resize operations in trial:i04.cu.def:VIA_VIA56_2_1_66_58.00 and trial:i04.cu.def:VIA_VIA56_2_2_66_58.01 — verify the resulting x-extent does not land on any of these forbidden values. The committed M5 resizes in this history are exclusively y-axis (delta_dbu=160 in y), which does not directly engage M5.W.3 or M5.W.4; however, any x-direction modification must avoid those forbidden widths.

M5.W.1 sets the minimum horizontal width at 24 nm and M5.W.2 sets the maximum at 480 nm. M5.W.5 sets the minimum vertical width at 44 nm. No trial in this history violates these absolute bounds in its committed ops.

## M5 Must Remain Rectilinear and Non-Bending

M5.AUX.3 prohibits any M5 corner with interior angle between 0 and 90 degrees (the `corners(0..90)` check). M5.GEOMETRY.NONORTHOGONAL prohibits any M5 edge at a non-orthogonal angle. All moves and resizes across all four trials in this history produce strictly rectilinear geometry (axis-aligned moves in x or y only, with no diagonal components). Never introduce diagonal offsets or non-right-angle corners when editing M5 shapes or moving instances that place M5 geometry.

## VIA Cell M5 Enclosure for V4

V4.M5.EN.2 requires V4 to be enclosed by M5 by at least 11 nm on two opposite sides; V4.M5.AUX.2 requires V4 to be exactly the same width as M5 along the direction perpendicular to M5 length. No trial in this history directly repairs a V4.M5 violation, but trial:i04.ug.leaf_0002.01 touches V4 alongside M5 and V3 through instance moves. When instance moves shift M5 geometry relative to V4, verify both V4.M5.EN.2 and V4.M5.AUX.2 post-move; trial:i04.ug.leaf_0002.01 introduced 2 new in-crop violations after its instance repositioning, consistent with a residual enclosure or width-match error on one of these rules.

## M5.AUX.1: Vertical Edge Grid

M5.AUX.1 requires all M5 vertical edges to lie on a 24 nm grid. The x-shift of 32 dbu applied to p1341 in trial:i04.ug.leaf_0002.01 implies the pre-edit position was off-grid if the post-edit position lands on the 24 nm grid. Snap all M5 vertical edge x-coordinates to multiples of 24 nm (in dbu units matching the deck's 1 dbu = 1 nm mapping implied by the 24.nm / 24 dbu correspondence in the rule deck) before committing any x-direction M5 move.