## Repair Operation Patterns on M2

All unit_gate trials that touched M2 used horizontal instance moves (x-axis, y-component zero) as the primary repair primitive. Observed horizontal deltas on M2-touching instances included 12, 16, 28, 36, 37, 72, 96, and 108 dbu across trials trial:i01.ug.Block4_union_row1.00, trial:i01.ug.Block4_union_row2.02, trial:i01.ug.Block4_union_row5.04, trial:i01.ug.Block4_union_row6.05, trial:i01.ug.Block4_union_row7.06, trial:i01.ug.Block4_union_row10.01, trial:i02.ug.Block4_union_row1.00, trial:i02.ug.Block4_union_row3.02, trial:i02.ug.Block4_union_row7.03, and trial:i02.ug.Block4_union_row10.01. Every one of these trials achieved gated_in with n_new_in_crop:0 and n_new_out_of_crop:0 (conn_preserved path). Vertical displacements on M2-touching instances—tested in trial:i02.ug.leaf_0008.04 and trial:i02.ug.leaf_0013.06—introduced new in-crop violations, establishing that horizontal moves are the safe axis for M2 instance repositioning.

## Polygon resize_end Operations on M2

Several trials combined move_instance with resize_end operations targeting M2 polygons. Observed M2 resize_end deltas and their associated trials:

- p1548 axis:x delta:16 (trial:i01.ug.Block4_union_row2.02)
- p1604 axis:x end:high delta:92 (trial:i01.ug.leaf_0008.08)
- p1551 axis:x end:high delta:16 (trial:i02.ug.Block4_union_row10.01)
- p1595 axis:x end:high delta:52 (trial:i02.ug.Block4_union_row7.03)
- p1395 axis:x end:high delta:172 (trial:i01.ug.Block4_union_row7.06)

All five trials gated_in with zero new violations. The resize_end operations extend the high end of an M2 polygon in the horizontal direction, consistently used in conjunction with instance moves rather than in isolation. The combination of instance repositioning and wire-end extension appears to maintain enclosure requirements (V1.M2.EN.2, V2.M2.EN.1) when an instance is displaced.

## M2.S.2 Violation From Vertical Instance Movement

Trial:i02.ug.leaf_0008.04 moved instance i0038 by [0, -44] dbu and introduced exactly 1 new M2.S.2 violation (tip-to-side spacing below the 25 nm minimum). The same move also introduced 1 new V1.M2.EN.2 violation. The trial was gated_in only because conn_preserved suppressed the new_in_crop count from blocking acceptance; violations were nonetheless introduced. M2.S.2 governs the interaction between a short tip edge (<=36 nm) and a long side edge (>36 nm) with a projection-measured spacing requirement of 25 nm. A -44 dbu vertical shift can compress this tip-to-side clearance below the threshold when M2 wires on different tracks share overlapping horizontal spans.

## M2.S.7 Violation From Vertical Instance Movement

Trial:i02.ug.leaf_0013.06 moved instance i0038 by [0, -36] dbu and introduced 1 new M2.S.7 violation among 9 total new in-crop violations. M2.S.7 fires when an 18 nm tip-to-tip gap (horizontal separation between vertical M2 edges) is co-located with a side-to-side spacing of <=32 nm on the same track pair, while the parallel run length is below 35 nm. A 36 dbu vertical shift is sufficient to place tip edges from two tracks into the forbidden co-location geometry. Trial:i02.ug.leaf_0013.06 also demonstrates that a vertical move that creates M2.S.7 simultaneously creates multiple other violations on adjacent layers (M1.A.1:2, M1.S.2:1, V1.M1.EN.1:4), reflecting the tight coupling between M2 position and M1/V1 geometry.

## External Conflict Dropping When Multiple Units Target the Same Instance

In trial:i02.ug.leaf_0008.04, the assembler dropped the planned op [0,-44] on i0038 because leaf_0013 also claimed that instance; the drop reason was external_conflict_dropped. In trial:i02.ug.leaf_0013.06, the symmetric conflict dropped [0,-36] on i0038 in favor of leaf_0008. Despite the drop, each trial executed its remaining op and both were gated_in. The conflict resolution selects at most one claimant per instance per assembly; the losing unit proceeds without that op. When a unit's M2-touching repair is conflict-dropped, the unit still accumulates the in-crop violation count from its surviving ops—trial:i02.ug.leaf_0013.06 accumulated 9 new in-crop violations despite the vertical move having been dropped for the conflicting case.

## cu_pool Channel: Grouped M2 Polygon Resize for Via Shape Compatibility

Trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 fixed violations by combining a via shape resize (VIA_VIA23_1_3_36_36 axis:y delta:-40 in M3) with 12 simultaneous M2 polygon resizes (p1411 through p1422, each axis:y delta:-64), achieving decision:applied with delta_total:-24 (net reduction of 24 violations across windows). Trial:i01.cu.def:VIA_VIA23_1_3_36_36.01 attempted only the via shape resize without the M2 polygon group and scored decision:lost_tournament with delta_total:0 (no improvement). The contrast establishes that adjusting the via shape alone is insufficient when V2.M2.EN.1 or V1.M2.EN.2 enclosure constraints depend on the M2 polygon extent; the M2 wires bounding the via must be co-resized. The 12-polygon group targets M2 wires on a shared y-dimension, each shrunk by 64 dbu in y, coordinated with a 40 dbu reduction in the via shape's y extent.

## Enclosure Rules: V1.M2.EN.2 and V2.M2.EN.1

V1.M2.EN.2 requires M2 to enclose V1 by at least 5 nm on two opposite sides (both sides 5 nm, or one side 5 nm and the opposite side 0 nm via the edge-point-zero exception). Trial:i02.ug.leaf_0008.04 demonstrated that a -44 dbu vertical displacement of an M2-carrying instance introduces a V1.M2.EN.2 violation in the same move that introduces M2.S.2, confirming that vertical shifts affecting M2-to-V1 overlap geometry can simultaneously violate both tip-to-side spacing and via enclosure. V2.M2.EN.1 requires M2 to enclose V2 by at least 5 nm on at least two opposite sides; trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 addressed V2.M2.EN.1-class violations by the grouped M2 resize described above.

## Move Magnitude Reference

Observed instance move deltas on M2-touching trials cluster at multiples of the 18 nm (36 dbu at 0.5 nm/dbu) rule pitch: 36, 72, 108 dbu appear repeatedly in trials trial:i01.ug.Block4_union_row1.00, trial:i01.ug.Block4_union_row6.05, trial:i02.ug.Block4_union_row1.00, trial:i02.ug.Block4_union_row7.03, trial:i02.ug.Block4_union_row10.01. The 28 dbu value (trial:i01.ug.Block4_union_row7.06, trial:i02.ug.Block4_union_row3.02) and 37 dbu value (trial:i01.ug.Block4_union_row5.04) appear as non-multiple adjustments, indicating that not all repairs snap to a 36 dbu grid—sub-pitch moves are applied when instance geometry requires finer alignment. The 12 dbu move in trial:i01.ug.Block4_union_row10.01 is the smallest observed horizontal instance displacement that achieved a clean gated_in result.