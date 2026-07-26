## Repair operation patterns for M1

All 18 trials in the measured history carry `"decision": "gated_in"` and touch M1 together with M2 and V1. Every operation in the history is one of: `move_instance`, `move` (polygon), or `resize_end` (polygon). No trial introduces a new M1 polygon or deletes an existing one.

## X-axis instance moves

X-axis instance moves at +36 dbu produce zero new in-crop violations across every clean trial where they appear. Single-instance moves at +36 dbu cleared in trial:i01.ug.Block4_union_row1.00 (i0265), trial:i01.ug.leaf_0020.09 (i0101), trial:i03.ug.leaf_0001.01 (i0292), and trial:i03.ug.Block4_union_row7.00 (i0040 and i0026 simultaneously). Three instances moved at +36 dbu simultaneously also cleared in trial:i01.ug.Block4_union_row6.05 (i0139, i0043, i0028). Apply X-axis instance moves at +36 dbu as the primary single-instance step when adjusting M1/V1 co-located cells.

Negative X-axis moves at -28 dbu also produce zero new violations: trial:i01.ug.Block4_union_row7.06 applied -28 dbu to i0158 and i0124 simultaneously; trial:i02.ug.Block4_union_row3.02 applied -28 dbu to i0170 alone. Use -28 dbu X-axis moves when a positive displacement would create a spacing conflict on the other side of the moved instance.

Larger X-axis displacements clear without new violations when the enclosure gap exceeds one grid step. Trial:i02.ug.Block4_union_row1.00 applied +72 dbu to i0265 and +36 dbu to i0325. Trial:i02.ug.Block4_union_row7.03 applied +108 dbu to i0153. Trial:i02.ug.Block4_union_row10.01 applied +96 dbu to i0025 and -108 dbu to i0041 in the same operation set, all with zero new violations. Scale X-axis displacement beyond 36 dbu when the measured enclosure shortfall exceeds the per-side minimum of 5 nm.

Mixed-sign X-axis moves on multiple instances in one trial are viable: trial:i01.ug.Block4_union_row5.04 moved i0220, i0198, and i0271 each at +37 dbu and i0341 at -36 dbu, producing zero new violations.

## Y-axis moves

Y-axis negative moves on instance i0038 introduce new in-crop M1 and V1 violations in every trial where they appear. Trial:i02.ug.leaf_0008.04 applied [0,-44] to i0038 and recorded 2 new in-crop violations (M2.S.2 and V1.M2.EN.2). Trial:i02.ug.leaf_0013.06 applied [0,-36] to i0038 and recorded 9 new in-crop violations including V1.M1.EN.1:4, M1.A.1:2, and M1.S.2:1. Trial:i03.ug.leaf_0004.02 applied [0,-64] to i0038 and recorded 2 new in-crop violations. Do not use Y-axis negative moves on M1/V1 instances as a repair strategy; all three measured Y-axis negative moves on i0038 (trial:i02.ug.leaf_0008.04, trial:i02.ug.leaf_0013.06, trial:i03.ug.leaf_0004.02) generated new rule violations and none eliminated them.

By contrast, a 2D move of [+36, +44] on the same instance i0038 in trial:i01.ug.leaf_0021.10 produced zero new violations in the iteration-1 design state. The distinction between that result and the Y-axis negative outcomes in iterations 2 and 3 is the sign and design-state context; positive Y-axis displacement on i0038 did not introduce violations in the one trial where it was applied.

## Conflict-dropped operations and per-rule violation counts

When `assemble_drops` is present in a trial record, one or more ops were removed during assembly due to external conflicts, and the `deltas.per_rule` counts reflect the partial or opposing assembly rather than the intended repair. Trial:i02.ug.leaf_0008.04 records that the op moving i0038 by [0,-44] was dropped because both leaf_0008 and leaf_0013 claimed that instance; the 2 violations reported (M2.S.2, V1.M2.EN.2) result from the remaining partial layout, not from the dropped move. Trial:i02.ug.leaf_0013.06 records the inverse conflict drop and reports 9 violations. Do not use the per-rule counts from trials with assemble_drops to calibrate the magnitude or direction of the dropped operation; the counts in trial:i02.ug.leaf_0008.04 and trial:i02.ug.leaf_0013.06 are both artifacts of the incomplete conflict-affected assembly, not signals about what the intended move would have produced.

## Polygon resize_end operations

`resize_end` operations on M1 polygons alongside instance moves produce zero new violations in every trial where they appear. Trial:i01.ug.Block4_union_row7.06 applied resize_end on p1395 at x+172 combined with -28 dbu instance moves. Trial:i01.ug.leaf_0008.08 applied resize_end on p1604 at x+92 combined with a +36 dbu instance move. Trial:i02.ug.Block4_union_row7.03 applied resize_end on p1595 at x+52 combined with a +108 dbu instance move. Trial:i02.ug.Block4_union_row10.01 applied resize_end on p1551 at x+16 combined with instance moves. Apply resize_end on the high-x end of an M1 polygon when an instance move would otherwise open a gap that fails V0.M1.EN.1 or V1.M1.EN.1 enclosure.

## Polygon move operations

Direct polygon moves (`"op": "move"`) appear alongside instance moves in two trials with zero new violations. Trial:i01.ug.Block4_union_row2.02 moved polygon p1548 by x+16 together with instance moves on i0250 and i0163. Trial:i01.ug.Block4_union_row7.06 moved p1596 and p1477 each by x-28 together with instance moves. Apply direct polygon moves when an instance move repositions the via stack but leaves an M1 segment that requires independent adjustment to maintain enclosure.

## Multi-operation trials

Trials with the largest operation counts clear without new violations. Trial:i01.ug.Block4_union_row7.06 applied five distinct operations (two instance moves, two polygon moves, one resize_end) across M1, M2, M3, M4, V1, and V2 simultaneously. Trial:i01.ug.Block4_union_row5.04 applied four instance moves with mixed sign. Trial:i02.ug.Block4_union_row10.01 applied four operations including a resize_end. Use multi-operation sets when spacing or enclosure constraints on adjacent M1 structures are co-dependent and cannot be resolved by repositioning a single instance.

## V1.M1.EN.1 violations

V1.M1.EN.1:4 appears in the violation count of trial:i02.ug.leaf_0013.06, which applied a Y-axis negative move to i0038 under a conflict-affected assembly. No V1.M1.EN.1 violations appear in any trial that uses only X-axis moves. The V1.M1.EN.1 violations in trial:i02.ug.leaf_0013.06 co-occur with M1.A.1:2 and M1.S.2:1, indicating that a Y-axis misalignment of an instance carrying V1 vias simultaneously fails enclosure, area, and spacing checks for M1.

## M1.A.1 (minimum area 504 nm-sq)

M1.A.1 violations appear only in trial:i02.ug.leaf_0013.06, which is conflict-affected (assemble_drops present) and uses a Y-axis negative move. No M1.A.1 violations appear in any clean X-axis move trial. Avoid Y-axis negative moves on instances co-located with M1 polygons near the 504 nm-sq minimum; the evidence is that such moves produce M1.A.1 failures (trial:i02.ug.leaf_0013.06).