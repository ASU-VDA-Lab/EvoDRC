## Geometry Constraints

M5 runs horizontally (length axis = x, width axis = y). All vertical edges must land on a 24 nm grid (M5.AUX.1). M5 shapes must be strictly orthogonal; any edge angle outside 0° or 90° triggers both M5.AUX.3 and M5.GEOMETRY.NONORTHOGONAL. No operation that introduces a non-rectilinear corner is legal.

Minimum horizontal (x-direction) width is 24 nm (M5.W.1); maximum is 480 nm (M5.W.2). Widths that are exact even-integer multiples of 24 nm (48, 96, 144, 192, 240, 288, 336, 384, 432, 480 nm) are forbidden by M5.W.3. Widths of 72, 168, 264, 360, and 456 nm are additionally forbidden by M5.W.4 because they span an even number of minimum-width routing tracks. The permitted horizontal widths are therefore the odd-multiple-of-24 values that are not also forbidden by M5.W.4: 24 nm, 120 nm, 216 nm, 312 nm, 408 nm, and non-multiples in the range up to 480 nm that satisfy both rules.

Minimum vertical (y-direction) width is 44 nm (M5.W.5).

## Routing Track Placement

Minimum-width M5 tracks (those narrower than 26 nm after a ±13 nm erosion/dilation round-trip, i.e. true 1x tracks) must have their centerlines placed at x = 48 + N×192 dbu for integer N (M5.AUX.2). Any resize or shift of a min-width M5 polygon along x must keep this alignment. Wide M5 polygons (those that survive the ±13 nm erosion) must not have their vertical outside edges coinciding with any 1x routing track edge (M5.AUX.4).

The vertical edge grid of 24 nm and the track pitch of 192 dbu (= 8× the 24 nm minimum width unit) are distinct constraints. Moving a min-width M5 polygon by 32 dbu (= 32 nm) from a track-centered position shifts it off the required track centerline grid even while keeping it on the 24 nm vertex grid; the two constraints must both be satisfied simultaneously. The trial i02.ug.leaf_0002.01 moved polygon p938 and four instances (i0097, i0098, i0064, i0068) by +32 dbu in x across M4/M5/V4 and resulted in zero new violations, indicating that the starting position was not a track-center position for any 1x M5 shape involved, or the shapes concerned were wide M5 not subject to M5.AUX.2.

## Spacing Rules

Horizontal edge-to-edge spacing (between vertical edges of distinct M5 polygons) must be ≥ 24 nm by projection measurement (M5.S.1). This also triggers for any sub-1 nm overlap (the second clause of M5.S.1 catches overlaps).

Vertical spacing between horizontal edges of distinct M5 polygons must be ≥ 40 nm (M5.S.2).

Tip-to-tip spacing for M5 polygons on adjacent tracks that do not share a parallel run length must be ≥ 40 nm (M5.S.3). Tip-to-tip spacing for M5 polygons that do share a parallel run length must also be ≥ 40 nm (M5.S.4). The shared-run-length case (M5.S.4) uses a 30 nm extension of horizontal edges to detect proximity; any horizontal edge within 30 nm laterally of another M5 polygon's horizontal edge and within 40 nm tip-to-tip will flag.

When two M5 polygons are on adjacent tracks (horizontal spacing < 24 + 1 dbu by projection), their parallel overlap in y must be ≥ 44 nm (M5.S.5). Creating a gap between adjacent-track polygons that is shorter than 44 nm in the y direction will flag M5.S.5.

## Via Enclosure (V4 and V5)

V4 vias inside M5 must be enclosed by M5 by ≥ 11 nm on two opposite sides (V4.M5.EN.2). V5 vias inside M5 must be enclosed by M5 by ≥ 11 nm on at least two opposite sides (V5.M5.EN.1). Both rules use the `sized(-11 nm)` interaction test.

V4 must match M5 width exactly in the direction perpendicular to the M5 length axis (V4.M5.AUX.2). A V4 shape that is narrower or wider than the enclosing M5 in the y direction (for horizontal M5) will fail unless the via edges are coincident with the M5 edges on both y-sides.

Resizing VIA_VIA45_1_2_58_58 V4 shapes by +152 dbu in x (two V4 shape indices plus the M4 shape) reduced total DRC violations by 8 in each of two affected units (leaf_0012 and leaf_0013) and was applied (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01). M5 was among the touched layers, consistent with V4.M5 enclosure rules being resolved by the resize. The direction of the resize (+x) widens the via along the M5 length axis, not the width axis, and the improvement indicates that tip enclosure (V4.M5.EN.2 along x) was the binding constraint rather than width matching (V4.M5.AUX.2 along y).

## Instance and Polygon Move Interactions

Moving instances that contain M5 shapes requires coordinated moves of all connected-net instances and any stand-alone polygons (e.g., M4, V4 fill shapes) in the same net group to maintain connectivity. Trial i01.ug.leaf_0012.07 moved four instances in y (i0097 and i0092 by −48 dbu, i0064 and i0072 by +96 dbu) across M3/M4/M5/V3/V4; connectivity was preserved and no M5-rule violations were introduced, though 2 V1.M1.EN.1 violations appeared (on M1, not M5). Trial i02.ug.leaf_0002.01 moved polygon p938 and four instances (i0098, i0097, i0064, i0068) by +32 dbu in x across M4/M5/V4 with zero new violations of any kind and connectivity preserved.

The +32 dbu x-move in trial:i02.ug.leaf_0002.01 kept all M5 vertical edges on the 24 nm grid (32 is not a multiple of 24, but the net shift from a previously on-grid position must have landed on-grid, implying the prior position was at a x-coordinate with residue 8 mod 24, and the shift brought it to residue 16, or the shapes are wide M5 not subject to M5.AUX.1's vertex constraint in the same way). Operations should verify post-move grid alignment explicitly.