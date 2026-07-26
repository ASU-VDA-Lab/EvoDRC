## Width Rules

M6.W.1 sets the minimum vertical (y-direction) width at 32 nm. M6.W.2 caps vertical width at 640 nm. M6.W.3 prohibits vertical widths that are even integer multiples of 32 nm: 64, 128, 192, 256, 320, 384, 448, 512, 576, and 640 nm are all forbidden. M6.W.4 additionally prohibits widths of 96, 224, 352, 480, and 608 nm, which correspond to polygons that would vertically span an even number of minimum-width routing tracks. M6.W.5 sets the minimum horizontal (x-direction) width at 44 nm.

The smallest compliant vertical width is exactly 32 nm (1x). The smallest compliant wide width above 32 nm is 48 nm, because 64 nm is blocked by W.3. All candidate repair widths above 32 nm must be checked against both W.3 and W.4 before application.

## Spacing Rules

M6.S.1 requires at least 32 nm vertical spacing between any two M6 polygon edges, regardless of edge length or mask color. M6.S.2 requires at least 40 nm horizontal spacing between M6 polygon edges. M6.S.3 applies a 40 nm tip-to-tip spacing constraint when two M6 polygons on adjacent tracks share no parallel run length. M6.S.4 applies the same 40 nm tip-to-tip spacing when the two polygons do share a parallel run length. M6.S.5 requires a minimum parallel run length of 44 nm for M6 polygons on adjacent tracks.

## Grid and Track Alignment

M6.AUX.1 requires all M6 horizontal edges (angle 0°) to lie on a 32 nm vertical grid, meaning every y-coordinate of a horizontal M6 edge must be divisible by 32 nm. Off-grid horizontal edges on any M6 polygon trigger this violation regardless of polygon width.

M6.AUX.2 constrains minimum-width (1x) M6 tracks. The rule isolates 1x polygons as those surviving `m6 - m6.sized(0, -17.nm).sized(0, 17.nm)`, i.e., polygons whose vertical extent collapses under a 17 nm inward sizing on each side (vertical width ≤ 34 nm, effectively 32 nm tracks). For these 1x polygons whose top and bottom edges are both divisible by 128 dbu (base_dbu check), their centerline must satisfy `(cl - 64) % 256 == 0` in dbu. Valid centerlines for 1x tracks are therefore y = 64 + N × 256 dbu for integer N ≥ 0.

M6.AUX.3 prohibits bends: any M6 polygon with a 0°–90° internal corner triggers a violation. M6 polygons must be strictly rectilinear without L-shapes, T-shapes, or any non-convex corner transitions.

M6.AUX.4 prohibits wide M6 polygon horizontal edges from coinciding with a 1x routing track edge. The rule detects horizontal edges of wide polygons (`m6_wide`) that fall within the horizontal band of any 1x track (`m6_1x_separate`). Wide polygon horizontal edges must not be co-linear with any 1x track's top or bottom edge.

## Via Enclosure Rules

V5.M6.EN.2 requires M6 to enclose each V5 via by at least 11 nm on two opposite sides: the via must not protrude beyond `m6.sized(-11.nm, 0)` (horizontal enclosure) and must not protrude beyond `m6.sized(0, -11.nm)` (vertical enclosure) simultaneously. Both conditions must be satisfied.

V5.M6.AUX.2 requires each V5 via to share at least two edges with M6, meaning the V5 width in the direction perpendicular to M6 length must exactly match the M6 width at that location. Vias not inside M6, and vias inside M6 with fewer than two coincident edges, both trigger the violation.

V6.M6.EN.1 requires M6 to enclose each V6 via by at least 11 nm on at least two opposite sides, with the same horizontal and vertical enclosure checks as V5.M6.EN.2.

## Geometry Constraint

The GEOMETRY.NONORTHOGONAL rule prohibits any M6 edge with an angle outside 0° and 90°. All M6 polygon edges must be exactly horizontal or exactly vertical.

## Repair Strategy: Y-Axis Snap with Co-Movement of Instances

In trial:i01.ug.whole_design.00, the repair engine resolved M6 violations over the full design locus ([0, 0, 30440, 30440]) using 24 operations, all in the group "m6_snap", touching layers M5, M6, and V5. The repair was accepted (decision: gated_in) with connectivity preserved (conn_preserved: true).

Six M6 polygons were moved along the y-axis with the following deltas: p3806 by −64 dbu, p3803 by +32 dbu, p3805 by +16 dbu, p3802 by −16 dbu, p3804 by −32 dbu, p3801 by −64 dbu. All deltas are multiples of 16 dbu. Snap M6 polygons along y by the minimum delta (in multiples of 16 dbu) needed to place horizontal edges on the 32 nm AUX.1 grid and, for 1x tracks, align the centerline to y = 64 + N × 256 dbu per AUX.2 (trial:i01.ug.whole_design.00).

For every M6 polygon snap, move all associated V5 and M5 instances by the identical y-delta. In trial:i01.ug.whole_design.00, each of the six polygon deltas was replicated exactly across three instances: the −64 dbu move applied to p3806 and p3801 was mirrored on instances i1469/i1666/i2012 and i0726/i0664/i0121 respectively; the +32 dbu move on p3803 was mirrored on i1524/i1693/i2026; the +16 dbu move on p3805 on i1362/i1139/i1765; the −16 dbu move on p3802 on i1336/i1124/i1762; and the −32 dbu move on p3804 on i0723/i0656/i0123. Omitting co-movement of V5 and M5 instances would violate V5.M6.EN.2, V5.M6.AUX.2, and connectivity. Apply the same delta to all dependent instances in the same atomic operation group (trial:i01.ug.whole_design.00).

The snap deltas of ±16, ±32, and ±64 dbu used in trial:i01.ug.whole_design.00 were sufficient to correct all M6 AUX.1/AUX.2 violations in the design without introducing new M6.W, M6.S, or enclosure violations, as confirmed by the gated_in acceptance.