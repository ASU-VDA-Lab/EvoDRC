## M5 Horizontal Width Constraints (M5.W.1 – M5.W.4)

M5.W.1 sets the minimum horizontal width at 24 nm. M5.W.2 caps the maximum at 480 nm. M5.W.3 prohibits widths that are exact even-integer multiples of 24 nm (48, 96, 144, 192, 240, 288, 336, 384, 432, 480 nm). M5.W.4 adds a complementary prohibition on widths that cause a polygon to span an even number of minimum-width routing tracks horizontally, detected at gap distances of 72, 168, 264, 360, and 456 nm. Via-cell repairs resize M5 only in the y axis; trial:i04.cu.def:VIA_VIA56_2_1_66_58.00 and trial:i04.cu.def:VIA_VIA56_2_2_66_58.01 both resize the M5 shape exclusively in y (+160 dbu), leaving the horizontal extent unchanged and thereby avoiding interaction with M5.W.3 and M5.W.4.

## M5 Vertical Width Constraint (M5.W.5)

M5.W.5 requires a minimum vertical width of 44 nm. Both accepted via-cell repairs apply a +160 dbu y-resize to the M5 shape (trial:i04.cu.def:VIA_VIA56_2_1_66_58.00, trial:i04.cu.def:VIA_VIA56_2_2_66_58.01); both trials resulted in decision: applied, confirming that this resize increment satisfies M5.W.5 in the context of VIA_VIA56 cell geometry.

## M5 Spacing Constraints (M5.S.1 – M5.S.5)

M5.S.1 requires 24 nm minimum horizontal spacing (projection and Euclidean). M5.S.2 requires 40 nm minimum vertical spacing. M5.S.3 and M5.S.4 each enforce 40 nm tip-to-tip spacing on adjacent tracks, covering both the non-parallel-run and parallel-run cases respectively. M5.S.5 requires a minimum parallel run length of 44 nm when two M5 polygons occupy adjacent tracks.

Vertical instance moves that are not multiples of the vertical routing pitch risk tightening M5.S.2, M5.S.3, or M5.S.5 gaps. The purely vertical move of +64 dbu applied to instances i0234 and i0305 in trial:i01.ug.leaf_0025.11 introduced 9 new in-crop violations (decision: gated_in, not applied), demonstrating that vertical displacements must be validated against spacing rules before acceptance.

## Vertical Routing Track Alignment (M5.AUX.2)

M5.AUX.2 requires that minimum-width M5 tracks — those whose horizontal extent is not fully eroded by 13 nm on each side — have their x-axis centerlines at positions satisfying (centerline − 48) mod 192 = 0 in dbu. Correct AUX.2 violations by moving the affected M5 polygon and any co-located instances by the signed x delta needed to reach the nearest compliant track. In trial:i04.ug.leaf_0002.01, the operation group labeled "m5_align" applied a +32 dbu x correction to polygon p1341 and instances i0239, i0223, i0141, i0150, and i0138; instances not participating in that group (i0237, i0214, i0103, i0104, i0134) received y-only adjustments, confirming that AUX.2 x corrections are applied selectively to the geometries that violate the track-center constraint.

## M5 Vertical-Edge Grid (M5.AUX.1)

M5.AUX.1 requires every M5 vertical edge to lie on a 24 nm grid. All horizontal moves and resizes applied to M5 must use x deltas that, when added to the current edge position, yield a coordinate divisible by 24 dbu. The horizontal correction in trial:i04.ug.leaf_0002.01 (+32 dbu x shift for the "m5_align" group) was applied to M5-touching geometries targeting grid compliance under M5.AUX.1.

## M5 Must Not Bend (M5.AUX.3)

M5.AUX.3 prohibits M5 corners with interior angles in the range 0°–90°; all M5 polygon shapes must be strictly rectilinear (only 90° corners). Moving an instance with a combined [x, y] translation vector does not alter the shape of M5 polygons within that instance and does not violate AUX.3; trial:i04.ug.leaf_0002.01 moved instance i0239 by [32, 72] dbu without creating bent M5 geometry. Direct shape operations (move_via_shape, resize_via_shape) each specify a single axis, leaving the perpendicular extent fixed, as seen in all five shape operations in trial:i04.cu.def:VIA_VIA56_2_1_66_58.00 and all nine in trial:i04.cu.def:VIA_VIA56_2_2_66_58.01 (all carry "axis":"y").

## Wide M5 and Routing Track Edges (M5.AUX.4)

M5.AUX.4 prohibits the vertical (90°) edges of wide M5 polygons (those wider than the 26 nm threshold implied by the bilateral 13 nm erosion test) from coinciding with the edge of a minimum-width routing track as defined by M5.AUX.2. Resizing a wide M5 shape in the y axis only leaves its vertical edges stationary and avoids displacing them into a track-edge conflict; trial:i04.cu.def:VIA_VIA56_2_1_66_58.00 and trial:i04.cu.def:VIA_VIA56_2_2_66_58.01 both resize the M5 shape exclusively in y, consistent with this requirement.

## V5 Enclosure of M5 (V5.M5.EN.1) and Via-Cell Repair Pattern

V5.M5.EN.1 requires M5 to enclose every V5 via by at least 11 nm on two opposite sides. When a VIA_VIA56 cell carries V5.M5.EN.1 violations, apply the following repair sequence: (1) move each V5 shape by −132 dbu in y, (2) resize it by +512 dbu in y, (3) move the paired V5 shape by +132 dbu in y, (4) resize it by +512 dbu in y, then (5) resize the M5 shape by +160 dbu in y (trial:i04.cu.def:VIA_VIA56_2_1_66_58.00, trial:i04.cu.def:VIA_VIA56_2_2_66_58.01). This pattern reduced violations by −2 in trial:i04.cu.def:VIA_VIA56_2_1_66_58.00 (single V5 column, two shapes) and by −4 in trial:i04.cu.def:VIA_VIA56_2_2_66_58.01 (two V5 columns, four shapes processed in two ±132 dbu / +512 dbu pairs plus one M5 +160 dbu y-resize). Both trials resulted in decision: applied.

## V4 Enclosure and Width-Match Rules (V4.M5.EN.2, V4.M5.AUX.2)

V4.M5.EN.2 requires M5 to enclose V4 by at least 11 nm on two opposite sides. V4.M5.AUX.2 requires that V4 match M5 exactly in width along the direction perpendicular to the M5 length. Instance moves in trial:i04.ug.leaf_0002.01 touched both V4 and M5 layers (touched_layers includes V4); those moves are instance-level translations that preserve the relative V4-to-M5 geometry established within each cell definition, leaving the enclosure and width-match relationships intact.

## Multi-Layer Impact of Instance Moves

All four trials touching M5 also affect other layers. trial:i01.ug.leaf_0025.11 (y-only instance moves, +64 dbu) touches M5, M6, and V5. trial:i04.ug.leaf_0002.01 (combined x+y instance moves) touches M3, M4, M5, V3, and V4. Whenever an instance move is applied to resolve an M5 violation, validate the resulting state on all touched layers; the 9 new in-crop violations introduced by trial:i01.ug.leaf_0025.11 (decision: gated_in) illustrate that a move which satisfies an M5 target rule can simultaneously produce new violations on co-touched layers.

## Non-Orthogonal Geometry (GEOMETRY.NONORTHOGONAL)

The GEOMETRY.NONORTHOGONAL rule rejects any M5 edge with an angle outside {0°, 90°, 180°, 270°}. All shape operations in the measured history use strictly axis-aligned deltas and single-axis resizes, consistent with this requirement (trial:i04.cu.def:VIA_VIA56_2_1_66_58.00, trial:i04.cu.def:VIA_VIA56_2_2_66_58.01, trial:i04.ug.leaf_0002.01, trial:i01.ug.leaf_0025.11).