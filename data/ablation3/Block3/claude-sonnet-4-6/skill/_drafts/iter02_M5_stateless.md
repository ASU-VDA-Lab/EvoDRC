## Width Constraints

M5 horizontal (x-axis) width must be at least 24 nm (M5.W.1) and at most 480 nm (M5.W.2). M5 vertical (y-axis) width must be at least 44 nm (M5.W.5).

M5.W.3 forbids horizontal widths that are even integer multiples of the 24 nm minimum: 48, 96, 144, 192, 240, 288, 336, 384, 432, and 480 nm are all disallowed. M5.W.4 additionally forbids horizontal widths of 72, 168, 264, 360, and 456 nm, which correspond to polygons spanning an even number of minimum-width routing tracks. The union of W.3 and W.4 restrictions leaves odd-track-count widths in the range 24–479 nm (excluding even multiples of 24 nm) as the only legal horizontal extents.

## Spacing Constraints

M5.S.1 requires a minimum horizontal spacing of 24 nm between any two M5 polygon edges, measured by projection (parallel-edge pairs) and also by Euclidean distance (catch-all overlap detection).

M5.S.2 requires a minimum vertical spacing of 40 nm between any two M5 polygon edges.

M5.S.3 extends the 40 nm vertical spacing requirement to tip-to-tip pairs on adjacent tracks that do not share a parallel run length.

M5.S.4 extends the 40 nm tip-to-tip spacing requirement to polygon pairs on adjacent tracks that do share a parallel run length.

M5.S.5 requires a minimum parallel run length of 44 nm for any two M5 polygons routed on adjacent tracks.

## Grid and Track-Placement Requirements

M5.AUX.1 requires that all vertical edges of M5 polygons fall on a 24 nm x-grid. Repairs that reposition M5 polygons in x must land on integer multiples of 24 nm.

M5.AUX.2 requires that minimum-width M5 routing tracks (those not surviving a ±13 nm erosion-and-restore cycle) have their centerlines at positions satisfying `(cl − 48) mod 192 == 0` in database units, placing valid track centers at 48, 240, 432, 624 nm, etc. from the origin along x. Polygon moves that shift the centerline of a minimum-width track must snap to one of these positions.

M5.AUX.3 forbids any corners with interior angles between 0° and 90° (exclusive) on M5 polygons; all M5 geometry must be strictly rectilinear. No bend operations are permissible.

M5.AUX.4 prohibits the outer vertical edges of wide M5 polygons (those surviving the ±13 nm erosion-and-restore cycle) from coinciding with any minimum-width routing track edge band. When widening an M5 polygon, the resulting outer vertical edges must not fall on a track-band boundary.

## Via Enclosure Rules

V4.M5.EN.2 requires that every V4 via landing inside an M5 polygon has at least 11 nm of M5 enclosure on two opposite sides (both x and y independently).

V4.M5.AUX.2 requires that V4 via width in the direction perpendicular to M5 run length exactly matches the M5 width in that direction; V4 must not be narrower or wider than its enclosing M5 stripe transversely.

V5.M5.EN.1 requires that every V5 via landing inside an M5 polygon has at least 11 nm of M5 enclosure on at least two opposite sides.

## Geometry

The GEOMETRY.NONORTHOGONAL rule applies to M5: no edge may have an angle outside {0°, 90°, 180°, 270°}. This is redundant with M5.AUX.3 for bends but also prohibits diagonal edges introduced by any automated shape manipulation.

## Observed Repair Behavior

In trial:i02.ug.whole_design.00 (unit_gate channel, decision: gated_in), two M5 polygons (p1059 and p1060) were moved +32 dbu in x together with a coordinated set of instance moves on M3, M4, V3, and V4. The trial was accepted into the design state with connectivity preserved and no new DRC violations introduced. Moving M5 polygons in x as part of a multi-layer coordinated move is viable when the destination x-coordinates satisfy the 24 nm grid requirement (M5.AUX.1) and the track-placement constraint (M5.AUX.2), and when instance-embedded via geometry is moved consistently with the M5 polygons.

In trial:i02.cu.def:VIA_VIA45_1_2_58_58.00 (cu_pool channel, decision: rejected_net_positive), adjustments to the via cell VIA_VIA45_1_2_58_58 were attempted: V4 shape 0 was moved +38 dbu and resized +76 dbu in x; V4 shape 1 was moved −38 dbu and resized +76 dbu in x; M4 shape 0 was resized +152 dbu in x. M5 appears in the touched_layers of this cell but received no explicit polygon operations in the op list. The violation count remained at 62 before and after (delta_total: 0). Resizing V4 shapes within a via cell and expanding M4 without a corresponding adjustment to the M5 geometry did not resolve any violations; via-cell x-expansion attempts that do not modify M5 geometry are insufficient to reduce M5-related DRC counts in this cell context.