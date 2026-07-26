## Observed Repair (iter 2)

Trial trial:i02.ug.leaf_0001.00 (Block2, unit_gate channel) achieved a gated-in decision with connectivity preserved. The four operations were: deleting polygon p1101, deleting instance i0086, inserting a VIA_VIA12 via at (5472, 2340) dbu, and resizing the low-x end of polygon p957 by +172 dbu along the x-axis. Touched layers were M1, M2, M4, and V1. A horizontal resize at one end of an M4 polygon was therefore part of a successful, connectivity-preserving repair in trial:i02.ug.leaf_0001.00.

## Vertical Width Rules (M4.W.1–M4.W.4)

M4.W.1 requires a minimum vertical width of 24 nm. M4.W.2 caps the maximum at 480 nm. M4.W.3 flags widths that are exact even-integer multiples of 24 nm as violations: 48, 96, 144, 192, 240, 288, 336, 384, 432, and 480 nm are all forbidden. M4.W.4 additionally flags 72, 168, 264, 360, and 456 nm because each of those values spans an even number of minimum-width routing tracks vertically. The smallest compliant vertical width is 24 nm; the next compliant widths above that are 120 nm (5×24), 216 nm (9×24), and so on, skipping all values enumerated by M4.W.3 and M4.W.4.

## Horizontal Width (M4.W.5)

M4.W.5 requires a minimum horizontal width of 44 nm. In trial:i02.ug.leaf_0001.00, a +172 dbu end-resize along the x-axis was applied to p957, extending its horizontal span without producing a reported M4.W.5 violation, consistent with the minimum being satisfied after the operation.

## Spacing Rules (M4.S.1–M4.S.5)

M4.S.1 requires a minimum vertical spacing of 24 nm between M4 edges (checked via projection and Euclidian fallback). M4.S.2 requires a minimum horizontal spacing of 40 nm between vertical M4 edges. M4.S.3 and M4.S.4 each require a 40 nm tip-to-tip separation between M4 polygons on adjacent tracks: M4.S.3 applies where the two polygons share no parallel run length; M4.S.4 applies where they do share a parallel run. M4.S.5 requires that adjacent-track M4 polygons sharing a parallel run have a parallel run length of at least 44 nm.

## Grid and Track Placement (M4.AUX.1, M4.AUX.2)

M4.AUX.1 requires all M4 horizontal edges to lie on a 24 nm grid. M4.AUX.2 constrains minimum-width (1×, i.e., vertical width ≤ 24 nm after erosion of 13 nm per side) M4 tracks to lie on routing tracks spaced at a 192 dbu pitch with a 48 dbu offset from the origin; the centerline of each such track must satisfy `(cl − 48) mod 192 == 0` in database units.

## Bend Prohibition and Wide-Shape Restriction (M4.AUX.3, M4.AUX.4)

M4.AUX.3 flags any M4 polygon corner where the interior angle is between 0° and 90° (exclusive); M4 shapes must be strictly rectilinear with no bends. M4.AUX.4 prohibits the outer horizontal edges of wide M4 polygons from coinciding with a routing track edge; wide shapes must not have their bounding horizontal edges land exactly on a track centerline.

## Via Enclosure (V3.M4.EN.2, V3.M4.AUX.2, V4.M4.EN.1)

V3.M4.EN.2 requires M4 to enclose each V3 via by at least 11 nm on at least two opposite sides. V4.M4.EN.1 imposes the same 11 nm two-sided enclosure requirement for V4 within M4. V3.M4.AUX.2 requires the V3 width in the direction perpendicular to the M4 length to exactly equal the M4 width in that same direction; V3 must not be narrower or wider than M4 in that axis.

## Non-Orthogonal Geometry

The GEOMETRY.NONORTHOGONAL rule flags any M4 edge whose angle is not a multiple of 90°; all M4 polygon edges must be strictly horizontal or strictly vertical.