## Operation repertoire

All ten accepted trials in this iteration resolved V1 DRC violations exclusively through X-axis (horizontal) operations on surrounding layers: `move_instance` to reposition V1-hosting cells, `add_polygon` on M2 to insert new M2 coverage segments, and `resize_end` on M2 polygon edges to extend existing M2 wire ends. No Y-axis displacements, no direct V1 polygon edits, and no M1 geometry modifications were used to repair V1 errors across trial:i01.ug.Block4_union_row1.00 through trial:i01.ug.leaf_0021.10.

## Instance moves and simultaneous M2 coverage repair

Moving a V1-hosting instance along X displaces V1 relative to the fixed M2 wires, which risks breaking V1.AUX.1 (V1 must be inside M1 ∩ M2), V1.M2.EN.2 (M2 must enclose V1 on two opposite sides by ≥5 nm each, or 5 nm and 0 nm), and V1.M2.AUX.2 (V1 must be exactly the same width as M2 perpendicular to M2 length). When the existing M2 geometry no longer covers the post-move V1 position, a corrective M2 add or extend must appear in the same compound operation set as the move itself—not in a subsequent pass.

In trial:i01.ug.Block4_union_row1.00 instance i0265 was moved +112 dbu and a new M2 polygon was added in the same op list; instance i0325 was moved +36 dbu and a second M2 polygon was added. In trial:i01.ug.Block4_union_row7.06 instance i0153 was moved +108 dbu and the high-end of M2 polygon p1595 was extended +164 dbu in the same set. In trial:i01.ug.Block4_union_row10.01 instance i0025 was moved +108 dbu and the high-end of M2 polygon p1551 was extended +128 dbu simultaneously. In trial:i01.ug.Block4_union_row2.02 instance i0250 was moved +36 dbu and p1548 high-end was extended +56 dbu; instance i0163 was moved +36 dbu and p1569 high-end was extended +92 dbu. In trial:i01.ug.Block4_union_row5.04 instances i0220 and i0198 were both moved +64 dbu and M2 polygons p1608 and p1593 had their high-ends extended +120 dbu each; instance i0341 was moved −36 dbu without an M2 change in that same trial.

Trials trial:i01.ug.Block4_union_row3.03, trial:i01.ug.Block4_union_row6.05, trial:i01.ug.leaf_0008.08, trial:i01.ug.leaf_0020.09, and trial:i01.ug.leaf_0021.10 used only `move_instance` operations (displacements of ±36 dbu) and produced zero new violations (n_new_in_crop = 0, conn_preserved = true in every case). This demonstrates that moves within pre-existing M2 slack pass all M2 enclosure and containment rules without any M2 edit; M2 repair is needed only when the move exhausts that slack.

## Paired-diverge and unidirectional move patterns for V1 spacing

V1.S.1, V1.S.2, V1.S.3, and V1.S.4 govern spacings between V1 instances. Two move geometries appear in the accepted repairs.

Paired-diverge: two neighboring V1-hosting instances are moved apart to open spacing. In trial:i01.ug.Block4_union_row3.03 instance i0170 was moved −36 dbu and i0292 was moved +36 dbu (net separation increase 72 dbu), with no M2 modification—used when both instances have adequate M2 slack in their respective directions.

Unidirectional or asymmetric: one instance is moved while an adjacent one stays fixed or moves by a different amount. In trial:i01.ug.Block4_union_row5.04 i0220 and i0198 were both moved +64 dbu (same direction, opening spacing toward a fixed neighbor on one side). In trial:i01.ug.Block4_union_row6.05 three instances—i0139, i0043, and i0028—were each moved +36 dbu in the same direction to uniformly shift a row of V1 instances away from a constraint on the low-X side.

## M2 extension method selection

Two distinct M2 extension mechanisms appear. `add_polygon` inserts an entirely new rectangular M2 segment and is used when the moved V1 lands at a location not covered by any existing M2 wire: trial:i01.ug.Block4_union_row1.00 added two polygons, each 72 dbu tall (one M2 track height), to cover the post-move V1 positions of i0265 and i0325.

`resize_end` extends the high-end or low-end of an existing M2 polygon's edge along X and is used when V1 moves to a position still on the same M2 wire but beyond its current terminus: trial:i01.ug.Block4_union_row2.02 applied high-end extensions of +56 dbu (p1548) and +92 dbu (p1569); trial:i01.ug.Block4_union_row7.06 applied high-end extensions of +164 dbu (p1595), +92 dbu (p1577), +56 dbu (p1556), and +172 dbu (p1395); trial:i01.ug.Block4_union_row10.01 extended p1551 high-end +128 dbu, p1589 low-end +72 dbu, p1605 high-end +92 dbu, and p1379 low-end +64 dbu.

## V1 geometry is controlled through instance placement, not direct polygon edits

No trial directly edited V1 polygon vertices. V1 shape, width, and position in every trial are determined entirely by the parent cell instance's placement. V1.W.1 (minimum width 18 nm along M2 length) and V1.M2.AUX.2 (V1 exactly flush with M2 perpendicular to M2 length) are therefore satisfied by selecting an instance whose V1 has the correct width and by choosing an instance whose V1 aligns with the M2 track width—not by reshaping V1 directly. This pattern holds across all ten accepted trials (trial:i01.ug.Block4_union_row1.00 through trial:i01.ug.leaf_0021.10).

## Connectivity and out-of-crop cleanliness

Every accepted trial carried conn_preserved = true and n_new_out_of_crop = 0. All M2 additions and extensions are purely additive (no M2 removal), which is consistent with zero connectivity loss. In trial:i01.ug.Block4_union_row7.06 and trial:i01.ug.Block4_union_row10.01 M4 also appears in touched_layers, indicating that extending M2 upward in those loci required corresponding M4 adjustments to preserve upper-layer connectivity, and those compound edits still produced zero new violations.