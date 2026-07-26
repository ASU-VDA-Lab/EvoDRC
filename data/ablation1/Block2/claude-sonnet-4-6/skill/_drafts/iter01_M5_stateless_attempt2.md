## Width Constraints

M5.W.1 requires a minimum horizontal (x-direction) width of 24 nm. M5.W.2 caps horizontal width at 480 nm. M5.W.3 forbids horizontal widths that are exact even multiples of 24 nm: 48, 96, 144, 192, 240, 288, 336, 384, 432, and 480 nm are each prohibited. M5.W.4 additionally bans widths of 72, 168, 264, 360, and 456 nm, which cause a polygon to span an even number of minimum-width routing tracks horizontally. M5.W.5 requires a minimum vertical (y-direction) width of 44 nm.

Asymmetric resize_end operations on the x-axis — in trial:i01.ug.leaf_0012.07 the low end moved 64 dbu and the high end moved 128 dbu — produced an accepted (gated_in) result on polygon p938. Apply resize_end adjustments to both x-axis ends independently, as in trial:i01.ug.leaf_0012.07, when simultaneous satisfaction of M5.W.1, M5.W.3, and M5.W.4 requires different deltas per endpoint.

## Spacing Constraints

M5.S.1 requires a minimum horizontal spacing of 24 nm between any two M5 polygon edges (projection metric, and also absolute Euclidean). M5.S.2 requires a minimum vertical spacing of 40 nm. M5.S.3 sets a 40 nm minimum tip-to-tip spacing for M5 polygons on adjacent tracks that do not share a parallel run length. M5.S.4 applies the same 40 nm tip-to-tip minimum when a shared parallel run length exists. M5.S.5 requires that whenever two M5 polygons on adjacent tracks share a parallel run, that run length must be at least 44 nm.

## Routing Track and Grid Constraints

M5.AUX.1 requires that all M5 vertical edges lie on a 24 nm horizontal grid (x-coordinates divisible by 24 nm). M5.AUX.2 confines minimum-width (1x) M5 tracks to vertical routing tracks defined by a 192 dbu pitch with a 48 dbu offset from the origin; tracks whose centerline does not satisfy `(cl - 48) % 192 == 0` violate this rule. M5.AUX.3 forbids any bend in M5: no interior corner angle in the range 0° to 90° is permitted, meaning all M5 polygons must be strictly rectilinear single-segment wires. M5.AUX.4 forbids the outer vertical edges of wide M5 polygons (polygons wider than the 1x threshold of approximately 24 nm after the erosion/dilation test) from coinciding with any routing track edge.

The NONORTHOGONAL block fires on any M5 edge whose angle falls in 1°–89°, 91°–179°, −179°–−91°, or −89°–−1°, covering all non-axis-aligned geometry.

resize_end on the x-axis, as applied in trial:i01.ug.leaf_0012.07, moves polygon endpoints along the horizontal axis and was the sole operation class observed in this iteration. Move x-axis endpoints to values satisfying the M5.AUX.1 grid (multiples of 24 nm) and the M5.AUX.2 track-center constraint simultaneously; trial:i01.ug.leaf_0012.07 confirmed this is achievable with independent per-end deltas.

## Wide Polygon Constraints

M5.AUX.4 fires when the vertical (x-direction) edges of a wide M5 polygon align with a routing track edge. The 1x detection uses a ±13 nm erosion/dilation: polygons surviving that round-trip are classified as wide. resize_end on x-axis endpoints shifts the outer edge off the offending track-aligned position; trial:i01.ug.leaf_0012.07 applied exactly this class of operation to polygon p938 and the result was accepted.

## Via Enclosure Constraints

V4.M5.EN.2 requires M5 to enclose V4 by at least 11 nm on two opposite sides. V4.M5.AUX.2 requires V4 width to exactly match M5 width in the direction perpendicular to the M5 run direction; partial enclosure or any lateral overhang violates this rule. V5.M5.EN.1 requires M5 to enclose V5 by at least 11 nm on at least two opposite sides.