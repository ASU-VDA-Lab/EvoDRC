## Geometry Constraints

M6 is a horizontal routing layer. Polygon edges must be strictly orthogonal; any non-orthogonal edge triggers GEOMETRY.NONORTHOGONAL. M6 may not bend: rule M6.AUX.3 fires on any corner whose interior angle is between 0° and 90°, meaning every M6 shape must be a simple axis-aligned rectangle. Do not introduce L-shaped or T-shaped M6 polygons.

Horizontal edges must be placed on a 32 nm grid (M6.AUX.1). Vertical edges are constrained indirectly through width and spacing rules.

## Width Rules

Vertical (y-direction) width has a minimum of 32 nm (M6.W.1) and a maximum of 640 nm (M6.W.2). The vertical width must not be an even integer multiple of 32 nm: prohibited exact widths include 64, 128, 192, 256, 320, 384, 448, 512, 576, and 640 nm (M6.W.3). An additional set of widths is also prohibited where the shape would span an even number of minimum-width routing tracks: 96, 224, 352, 480, and 608 nm are explicitly excluded (M6.W.4). When sizing M6 vertically, choose widths such as 32, 160, 288, or 416 nm — odd multiples of 32 nm that fall outside the M6.W.4 set.

Horizontal (x-direction) width has a minimum of 44 nm (M6.W.5); there is no stated maximum for horizontal width.

## Track Placement (AUX.2 and AUX.4)

Minimum-width M6 tracks (those not surviving a ±17 nm vertical erosion/expansion cycle) must have their centerlines at y-positions satisfying: `(y_center - 64) mod 256 == 0`, evaluated only on shapes whose bottom and top edges are multiples of 128 nm (M6.AUX.2). Wide M6 polygons (those surviving the ±17 nm erosion) must not have their horizontal outside edges touching a routing track edge defined by those same minimum-width track bands (M6.AUX.4). Do not place wide M6 shapes whose top or bottom edge coincides with a 1x track centerline.

## Spacing Rules

Minimum vertical spacing (between horizontal edges) is 32 nm (M6.S.1). Minimum horizontal spacing (between vertical edges) is 40 nm (M6.S.2).

Tip-to-tip spacing on adjacent tracks depends on whether the two polygons share any parallel run length. Where no parallel run length exists, a 40 nm tip-to-tip gap is required (M6.S.3). Where a parallel run length is shared, tip-to-tip spacing is also 40 nm (M6.S.4), and the minimum parallel run length itself must be at least 44 nm (M6.S.5). These three rules interact: when placing M6 ends near each other on adjacent horizontal tracks, ensure both the gap and any overlapping run length clear their respective thresholds simultaneously.

## Via Enclosure

V5 inside M6 must be enclosed by M6 on at least two opposite sides by a minimum of 11 nm in both the x and y directions (V5.M6.EN.2). Furthermore, V5 must be exactly the same width as M6 along the direction perpendicular to the M6 length (V5.M6.AUX.2): a V5 whose horizontal extent does not flush with the enclosing M6's vertical edges violates this rule. V6 inside M6 requires enclosure of at least 11 nm on at least two opposite sides (V6.M6.EN.1).

## Observed Operation Outcomes

A `resize_via_shape` of -96 dbu in x on the cell VIA_VIA56_2_2_66_58, touching M5, M6, and V5, produced a net delta of zero and was rejected as `rejected_net_positive` (trial:i01.cu.def:VIA_VIA56_2_2_66_58.01). Shrinking a via cell's M5 shape horizontally by 96 dbu in a VIA_VIA56 context did not reduce any M6-touching violations, indicating that enclosure and width violations on M6 in this cell are not addressable by x-axis M5 resizing alone.

A large whole-design move batch (57 ops spanning M3–M6 and V3–V5) was accepted by the unit gate on connectivity grounds (trial:i02.ug.whole_design.00). This move introduced 48 new V1.M2.AUX.2 violations on a different layer but zero new in-crop M6 violations. The gate accepted because `conn_preserved` was true and `n_new_in_crop` and `n_new_out_of_crop` were both zero for all M6 rules. Moves that preserve connectivity and do not add in-crop M6 violations will pass the unit gate even when they introduce violations on other layers.