## Repair Pattern: Always adjust M1, M2, and V1 together

All accepted repairs in this layer's history touch M1 and M2 simultaneously with V1 (trial:i01.ug.Block4_union_row1.00, trial:i01.ug.Block4_union_row2.02, trial:i01.ug.Block4_union_row3.03, trial:i01.ug.leaf_0008.08, trial:i01.ug.leaf_0020.09, trial:i01.ug.leaf_0021.10, trial:i02.ug.leaf_0001.00). Do not adjust V1 position without simultaneously updating the M2 polygon that must enclose it; isolated V1 moves violate V1.AUX.1, V1.M2.EN.2, and V1.M2.AUX.2.

## V1.M2.AUX.2: Keep M2 width coincident with V1 after every instance move

V1.M2.AUX.2 requires V1 to match M2 width exactly along the axis perpendicular to M2 length. In trial:i01.ug.Block4_union_row2.02, each move_instance was paired with a resize_end on the enclosing M2 polygon (p1548 high-end +56dbu with instance +36dbu; p1569 high-end +92dbu with instance +36dbu). In trial:i01.ug.Block4_union_row7.06, five resize_end operations on M2 polygons accompanied three instance moves. Always resize the relevant M2 polygon endpoint(s) when moving an instance so that M2 and V1 remain co-extensive in width (trial:i01.ug.Block4_union_row2.02, trial:i01.ug.Block4_union_row7.06).

## Dominant repair: +X instance move with M2 high-end extension

The primary repair mode across all rows is moving an instance in the +X direction and extending the high-end of the covering M2 polygon. In trial:i01.ug.Block4_union_row7.06, instance i0153 moved +108dbu while M2 polygon p1595 extended +164dbu at its high end. In trial:i01.ug.Block4_union_row2.02, M2 polygon p1569 extended +92dbu for a +36dbu instance move. The M2 extension must be at least as large as the instance delta to maintain V1.M2.EN.2 enclosure; in practice the extension exceeds the instance delta to re-establish the 5nm minimum enclosure margin (trial:i01.ug.Block4_union_row2.02, trial:i01.ug.Block4_union_row7.06).

## Negative-X moves: extend M2 low-end toward the new V1 position

Negative-direction instance moves are valid when the low-side spacing budget permits. In trial:i01.ug.Block4_union_row10.01, instance i0041 moved -108dbu while M2 polygon p1589 low-end extended +72dbu (toward the new V1 low-X edge). In trial:i01.ug.Block4_union_row7.06, instance i0158 moved -28dbu. In trial:i02.ug.leaf_0003.02, instance i0213 moved -36dbu with a group_D M2 polygon high-end resize of -8dbu. When an instance moves in -X, extend the M2 low-end toward the shifted V1 to restore V1.M2.EN.2 and V1.M2.AUX.2 compliance (trial:i01.ug.Block4_union_row10.01, trial:i02.ug.leaf_0003.02).

## M2 polygon addition as an alternative enclosure repair

In trial:i01.ug.Block4_union_row1.00, two new M2 polygons were added (bounding boxes [9252,3024]-[9444,3096] and [12132,3024]-[12224,3096]) alongside two instance moves, achieving n_new_in_crop=0. Adding a new M2 stub to cover a V1 is a valid repair for V1.M2.EN.2 and V1.AUX.1 when no existing M2 polygon can be extended without introducing V1.S.1 or V1.S.2 spacing violations (trial:i01.ug.Block4_union_row1.00).

## Cohort moves preserve inter-V1 spacing

When multiple instances on the same row share a spacing violation against a neighbor, moving all of them by a uniform delta maintains their mutual V1 spacings per V1.S.1 while displacing the group away from the violating neighbor. In trial:i01.ug.Block4_union_row5.04, four instances each moved +64dbu with two M2 resize_end operations. In trial:i01.ug.Block4_union_row6.05, three instances each moved +36dbu. Use uniform group moves for row-level spacing corrections rather than moving individual instances inside a packed row (trial:i01.ug.Block4_union_row5.04, trial:i01.ug.Block4_union_row6.05).

## Opposite-direction pair moves for symmetric spacing violations

In trial:i01.ug.Block4_union_row3.03, two instances were moved in opposite directions (i0170 at -36dbu, i0292 at +36dbu), resolving the violation with no new errors. Use symmetric pair moves when a V1.S.1 violation sits between two instances and the available movement budget on each side is approximately equal (trial:i01.ug.Block4_union_row3.03).

## Multi-layer upper-metal adjustment in complex rows

Several repairs required adjustments to M4 in addition to M1/M2/V1 (trial:i01.ug.Block4_union_row10.01, trial:i01.ug.Block4_union_row7.06), and trial:i02.ug.leaf_0003.02 required M3/V2 adjustments as well. When moving instances in a row that carries upper routing, extend the affected upper-metal polygons by at least the instance delta to preserve routing continuity; failure to do so risks creating new violations on M3, M4, V2, or higher (trial:i01.ug.Block4_union_row7.06, trial:i02.ug.leaf_0003.02).

## Enclosure rules V1.M1.EN.1 and V1.M2.EN.2: opposite-side minimums

V1.M1.EN.1 requires M1 to enclose V1 by 5nm on one side and 2nm on the opposite side. V1.M2.EN.2 requires M2 to enclose V1 by 5nm on one side and either 5nm or 0nm on the opposite side. All accepted trials that moved instances also adjusted the enclosing M2 polygon to maintain these margins; none introduced enclosure violations. When computing the required M2 resize_end delta, account for both the minimum 5nm enclosure on the primary end and the 0nm-or-5nm constraint on the secondary end (trial:i01.ug.Block4_union_row2.02, trial:i01.ug.Block4_union_row7.06, trial:i01.ug.Block4_union_row10.01).

## n_new_in_crop tolerance: target zero but gating allows nonzero when conn_preserved

Trial trial:i02.ug.leaf_0003.02 introduced n_new_in_crop=2 new in-crop violations and was still accepted because conn_preserved=true. All other trials achieved n_new_in_crop=0. Target zero new in-crop violations; accept nonzero only when connectivity is fully preserved and the new violations are on out-of-crop geometry that will be repaired by a later iteration (trial:i02.ug.leaf_0003.02).

## GEOMETRY.NONORTHOGONAL: all operations must produce axis-aligned edges

Every polygon operation in the recorded history — move_instance, resize_end, and add_polygon — produces exclusively horizontal (0-degree) or vertical (90-degree) edges. Do not introduce diagonal or off-axis V1 edges; the GEOMETRY.NONORTHOGONAL rule fires on any edge at 1–89, 91–179, -179 to -91, or -89 to -1 degrees. Verify that all resize_end delta values and new polygon coordinates produce strictly orthogonal boundaries (trial:i01.ug.Block4_union_row1.00, trial:i01.ug.Block4_union_row2.02, trial:i01.ug.Block4_union_row7.06).