## VIA_VIA45 cells: coordinated V4 x-axis + M5 x-resize outperforms M5 y-shrink alone

Two competing strategies were evaluated for violations in `def:VIA_VIA45_1_2_58_58`. The applied fix (trial:i01.cu.def:VIA_VIA45_1_2_58_58.00) used five operations: four on V4 (two x-axis moves of −116 dbu and +116 dbu on shape indices 0 and 1, each paired with an x-axis resize of +232 dbu) plus one M5 x-axis resize of −152 dbu on shape index 0. This delivered a total violation delta of −156, clearing 81 violations from `unit:leaf_0103` and 75 from `unit:leaf_0104`. The competing single-operation strategy—a −88 dbu y-axis resize of the same M5 shape (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01)—projected the identical delta_total of −156 across the same windows but lost the tournament. Never apply an isolated M5 vertical shrink when a coordinated V4 x-reposition plus M5 x-shrink is available; the multi-operation approach wins the tournament even when the projected violation counts are equal (trial:i01.cu.def:VIA_VIA45_1_2_58_58.00 vs trial:i01.cu.def:VIA_VIA45_1_2_58_58.01).

The −152 dbu M5 horizontal shrink in trial:i01.cu.def:VIA_VIA45_1_2_58_58.00 is a large reduction. Apply it only in concert with the matching V4 x-axis expansion (+232 dbu resize on each V4 shape) so that V4.M5.EN.2 enclosure (minimum 11 nm on two opposite sides) and V4.M5.AUX.2 (V4 must span exactly the M5 width perpendicular to the M5 run direction) are maintained. The V4 +232 dbu resize offsets the tightened M5 envelope and keeps both via enclosure rules satisfied (trial:i01.cu.def:VIA_VIA45_1_2_58_58.00, `conn_preserved: true`).

## VIA_VIA56 cells: V5 y-axis adjustments clear M5-region violations without touching M5 geometry

For `def:VIA_VIA56_2_2_66_58`, the applied fix (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02) used eight operations entirely on V5 shapes (four pairs of y-axis move ±132 dbu and y-axis resize +512 dbu across shape indices 0–3), with no direct modification of M5. M5 appeared in `touched_layers` because the V5.M5.EN.1 rule (minimum 11 nm enclosure of V5 by M5 on two opposite sides) was evaluated against the revised V5 positions. The fix reduced violations in four windows: `unit:Block7_union_row21` (−6), `unit:Block7_union_row22` (−2), `unit:leaf_0103` (−36), `unit:leaf_0104` (−36), for a total delta of −80. When M5 appears in `touched_layers` for a VIA_VIA56 target but all ops are on V5, do not modify M5 geometry; the V5 repositioning alone resolves the enclosure check (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02, `conn_preserved: true`).

The large V5 y-resize value (+512 dbu) paired with moves of ±132 dbu on each of the four V5 shapes is consistent with satisfying V5.M5.EN.1: the combined move-then-resize operation repositions the via while expanding its footprint to maintain the required two-sided 11 nm enclosure margin within the M5 envelope (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02).

## M5 horizontal width constraints (M5.W.1–M5.W.4)

No trial in this iteration directly targeted M5.W.1 (minimum horizontal width 24 nm), M5.W.2 (maximum horizontal width 480 nm), M5.W.3 (width must not be an even integer multiple of 24 nm: 48, 96, 144, … 480 nm), or M5.W.4 (width must not span an even number of minimum-width routing tracks: 72, 168, 264, 360, 456 nm). The −152 dbu M5 x-resize in trial:i01.cu.def:VIA_VIA45_1_2_58_58.00 was measured to be safe (conn_preserved, no new violations introduced), confirming that this particular resize did not cross any M5.W.3 or M5.W.4 forbidden width. When sizing M5 in x, verify that the resulting width is not 48, 96, 144, 192, 240, 288, 336, 384, or 432 nm (M5.W.3) and not 72, 168, 264, 360, or 456 nm (M5.W.4). The minimum of 24 nm (M5.W.1) and maximum of 480 nm (M5.W.2) are hard bounds on every horizontal resize.

## M5 vertical width constraint (M5.W.5)

The losing trial trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 proposed shrinking M5 in y by −88 dbu. This trial was rejected by the tournament, not by a DRC error (conn_preserved is true for that record), indicating the resulting vertical dimension still exceeded the 44 nm minimum (M5.W.5). Nevertheless, do not use an isolated M5 y-shrink when a better coordinated fix is available (trial:i01.cu.def:VIA_VIA45_1_2_58_58.00 vs trial:i01.cu.def:VIA_VIA45_1_2_58_58.01).

## M5.AUX.1: vertical edge grid alignment

M5.AUX.1 requires all M5 vertical edges to lie on a 24 nm grid. The −152 dbu M5 x-resize in trial:i01.cu.def:VIA_VIA45_1_2_58_58.00 was applied without introducing new violations, confirming that a resize of 152 dbu (not a multiple of 24) is grid-safe only when the original edge positions are already on-grid and the resize shifts both edges symmetrically or from a grid-aligned baseline. Always verify that post-resize left and right M5 edge x-coordinates are divisible by 24 dbu before committing an x-axis resize.

## M5.AUX.2: minimum-width track centerline alignment

M5.AUX.2 requires minimum-width M5 tracks (identified by the erosion test: width < 26 nm after a −13/+13 dbu x-sized round-trip) to have their x-centerlines at positions satisfying `(cl − 48) mod 192 == 0` (pitch 192 dbu, offset 48 dbu from origin). No trial in this iteration targeted M5.AUX.2 directly, but the M5 x-resize in trial:i01.cu.def:VIA_VIA45_1_2_58_58.00 preserved connectivity and introduced no new violations, confirming the post-resize centerline remained on a legal track position.

## M5.AUX.3: no bends

M5.AUX.3 prohibits any corner with angle 0°–90° (i.e., M5 must be a straight rectangle with no L-shape). No bend-introducing ops appeared in this iteration. All M5 shapes remained rectangles (trial:i01.cu.def:VIA_VIA45_1_2_58_58.00, trial:i01.cu.def:VIA_VIA56_2_2_66_58.02). Never apply a move or resize that creates a non-rectilinear M5 outline.

## M5.AUX.4: wide M5 outside edge must not align with a routing track edge

M5.AUX.4 flags any wide M5 polygon (surviving the erosion/dilation test) whose vertical edges fall on the x-band of a nearby minimum-width M5 track. The applied M5 x-resize of −152 dbu in trial:i01.cu.def:VIA_VIA45_1_2_58_58.00 passed without triggering this rule (conn_preserved, no new violations), establishing that the shrunken M5 did not land its outside vertical edges on an adjacent routing track edge.

## Spacing rules (M5.S.1–M5.S.5)

No trial in this iteration targeted M5.S.1 (minimum horizontal spacing 24 nm), M5.S.2 (minimum vertical spacing 40 nm), M5.S.3 (tip-to-tip on adjacent tracks without shared parallel run 40 nm), M5.S.4 (tip-to-tip with shared parallel run 40 nm), or M5.S.5 (minimum parallel run length 44 nm). The M5 x-resize of −152 dbu in trial:i01.cu.def:VIA_VIA45_1_2_58_58.00 did not introduce new spacing violations, confirming that shrinking M5 in x moves its edges inward, which can only increase spacing to neighbors, not decrease it.

## Op ordering for VIA_VIA45 fixes

The applied five-op sequence in trial:i01.cu.def:VIA_VIA45_1_2_58_58.00 follows this pattern:
1. Move V4 shape 0 in x by −116 dbu (repositioning toward target edge).
2. Resize V4 shape 0 in x by +232 dbu (expanding to restore enclosure).
3. Move V4 shape 1 in x by +116 dbu (symmetric move on opposing side).
4. Resize V4 shape 1 in x by +232 dbu (expanding to restore enclosure).
5. Resize M5 shape 0 in x by −152 dbu (trimming M5 to eliminate the DRC violation).

Apply V4 repositioning and expansion before M5 trimming so that at no intermediate point do V4 shapes violate V4.M5.EN.2 or V4.M5.AUX.2 with respect to the still-untrimmed M5. The final M5 shrink then tightens the envelope around the already-repositioned V4 geometry (trial:i01.cu.def:VIA_VIA45_1_2_58_58.00).