## Layer M5 Routing Geometry

M5 is a horizontal routing layer. All wires run in the x-direction (horizontal edges are the wire faces; vertical edges are the wire sides). Rule M5.AUX.3 forbids any corner in the angle range 0..90 degrees, which means M5 polygons must be strictly rectilinear with no bends of any kind. Rule M5.AUX.1 places all vertical edges on a 24 nm x-grid. Together these two constraints mean every M5 polygon must be a plain rectangle whose left and right edges are both snapped to multiples of 24 nm.

Minimum-width M5 tracks (those that survive a -13 nm / +13 nm size-round-trip) must additionally satisfy M5.AUX.2: their x-centerlines must satisfy `(cl - 48) % 192 == 0` in database units, i.e., the centerline must land on the series {48, 240, 432, 624, …} dbu. Wide M5 polygons (those that survive the same erosion) are subject to M5.AUX.4: no vertical edge of a wide polygon may coincide with any of those routing-track x-positions. Placing a wide polygon such that its outer vertical edge falls on a track position violates AUX.4.

## Horizontal Width Rules (M5.W.1 – M5.W.4)

The allowed horizontal width range is [24 nm, 480 nm] (M5.W.1 lower bound, M5.W.2 upper bound). Within that range, a large set of specific widths is forbidden:

M5.W.3 forbids every even-integer multiple of the 24 nm minimum: 48, 96, 144, 192, 240, 288, 336, 384, 432, and 480 nm. M5.W.4 forbids widths that cause the polygon to span an even number of routing tracks horizontally: 72, 168, 264, 360, and 456 nm.

Combining both exclusions, the only permitted horizontal widths (up to the 480 nm cap) are the odd multiples of 24 nm that are congruent to 24 nm modulo 96 nm: **24, 120, 216, 312, and 408 nm**. Any horizontal width that is not one of these five values triggers either M5.W.1, M5.W.2, M5.W.3, or M5.W.4. When generating or adjusting M5 widths, the target must be drawn from this explicit set.

The unit-gate batch in trial:i02.ug.whole_design.00 and trial:i04.ug.whole_design.00 performed x-direction resize_end and resize operations on M5-touching polygons and introduced zero new M5 violations, confirming that width adjustments landing on grid-legal values pass the full rule set without secondary side effects.

## Vertical Width Rule (M5.W.5)

M5.W.5 sets a minimum vertical wire height of 44 nm (measured with euclidean check on horizontal edges). This is independent of the horizontal width grid. There is no stated maximum vertical height. Shrinking an M5 shape in the y-direction must not push the vertical extent below 44 nm; trial:i01.cu.def:VIA_VIA45_1_2_58_58.00 applied a y-axis shrink of -88 dbu to an M5 via shape and still closed 56 violations, showing that the pre-repair shape had excess vertical extent and the post-repair shape retained at least 44 nm vertical width.

## Horizontal Spacing Rules (M5.S.1, M5.S.3 – M5.S.5)

M5.S.1 requires at minimum 24 nm horizontal gap between any two M5 polygons, checked both with projection and with a 1 dbu general check. The projection check applies regardless of edge lengths or mask colors.

M5.S.3 covers the tip-to-tip case where two M5 polygons on adjacent tracks share no parallel run length: the minimum tip-to-tip gap is 40 nm. M5.S.4 covers the opposite case—polygons that do share a parallel run length—and sets the same 40 nm minimum for tip-to-tip separations along the shared-run region. M5.S.5 requires that when two M5 polygons on adjacent tracks are within 24 nm of each other horizontally, their parallel run length must be at least 44 nm; a parallel run shorter than 44 nm between near-adjacent wires violates M5.S.5.

The batch operations in trial:i02.ug.whole_design.00 included instance moves that repositioned M5 via cells and resize_end steps that extended M5 polygon ends horizontally (axis:x, end:high, delta_dbu:20 on polygons p1831, p1786, p1806). These passed with zero new violations, confirming that extending M5 wire ends by a moderate amount (20 dbu) in the direction away from a spacing-critical region does not induce M5.S.3 or M5.S.4 violations when the adjacent tracks are sufficiently spaced.

## Vertical Spacing Rule (M5.S.2)

M5.S.2 requires at least 40 nm vertical separation between horizontal edges of different M5 polygons. This is a symmetric rule applied to edges at 0-degree angle (horizontal). Because M5 is a horizontal routing layer, vertical spacing constrains stacking of M5 wires in the y-direction. The y-direction polygon moves in trial:i02.ug.whole_design.00 (e.g., p2106 –16, p2107 +32, p2108 +16, p2109 –64) were accepted with zero new violations, showing that vertical repositioning of M5 polygons at these magnitudes does not create M5.S.2 conflicts when the initial placement already satisfies the 40 nm floor.

## Via Enclosure – V4 (V4.M5.EN.2, V4.M5.AUX.2)

V4.M5.EN.2 requires that every V4 via inside M5 is enclosed by at least 11 nm on two opposite sides (checked independently in x and y). V4.M5.AUX.2 imposes a stricter structural constraint: V4 must be exactly the same width as M5 in the direction perpendicular to the M5 wire length (i.e., V4 width in y must match M5 width in y). A V4 that is either wider or narrower than the enclosing M5 track in the y-direction fails AUX.2; the coincident-edge count test (requiring at least 2 coincident M5 edges) enforces exact flush alignment.

trial:i01.cu.def:VIA_VIA45_1_2_58_58.00 directly addresses this pair of rules: shrinking the M5 shape in cell VIA_VIA45_1_2_58_58 by 88 dbu in the y-axis reduced the total violation count by 56. The cell name encodes a via structure coupling V4 and M5; the y-axis shrink narrows the M5 enclosure shape to match V4 geometry, resolving either over-enclosure that caused AUX.2 mismatch or a vertical spacing violation that the over-tall M5 was creating on an adjacent M5 track. Shrinking M5 in y on via cells is therefore the confirmed repair direction when these rules fire on VIA_VIA45 instances.

## Via Enclosure – V5 (V5.M5.EN.1)

V5.M5.EN.1 mirrors V4.M5.EN.2: every V5 inside M5 must be enclosed on at least two opposite sides by a minimum of 11 nm. If V5 protrudes past M5 in x or y (the two independent size checks), the rule fires.

trial:i01.cu.def:VIA_VIA56_2_2_66_58.01 repaired V5.M5.EN.1 violations by expanding four V5 shapes in cell VIA_VIA56_2_2_66_58 by +248 dbu each in the y-direction. The M5 layer is touched as a side-effect (M5 is listed in touched_layers) but the explicit ops are V5 resizes. This shows that V5.M5.EN.1 failures on VIA_VIA56 instances are resolved by growing the V5 shape in y to stay inside M5, not by moving or enlarging M5 itself. The repair closed 32 violations. Applying this pattern—resize the via rather than the metal—preserves M5 width rules while satisfying enclosure.

## Instance-Move Safety

Both trial:i02.ug.whole_design.00 and trial:i04.ug.whole_design.00 moved large numbers of via cell instances (move_instance ops) simultaneously with polygon adjustments while touching M5 in the affected layers list. Both were accepted with `n_new_in_crop: 0` and `n_new_out_of_crop: 0`, and both passed connectivity preservation checks. This establishes that coordinated bulk instance repositioning, when driven by the unit-gate channel with connectivity verification, does not induce new M5 DRC violations provided the individual polygon adjustments landing on M5 geometries remain within the legal width and spacing envelopes described above.