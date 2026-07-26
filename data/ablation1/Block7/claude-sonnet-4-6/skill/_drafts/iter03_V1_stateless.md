## Operation Profile

Every trial in this layer's history across all three iterations carries `decision: "gated_in"` and `conn_preserved: true`. The repair channel consistently produces accepted solutions; no trial was rejected on connectivity grounds in the recorded data (trial:i01.ug.Block7_union_row10.00 through trial:i03.ug.leaf_0020.09, 47 entries total).

The dominant primitive is `move_instance`. `resize_end` operations on M1 and M2 polygons appear as secondary operations coordinated with instance moves, never in isolation on V1 shapes. Direct polygon geometry operations on V1 shapes themselves do not appear in the history; V1 geometry changes occur as a side-effect of moving the instances that contain them.

## Horizontal Step Quantization

The 36 dbu horizontal step is by far the most common move quantum. It appears as the sole delta value in the majority of x-axis `move_instance` ops across all rows and leaf units: trial:i01.ug.Block7_union_row11.01 (both instances +36), trial:i01.ug.Block7_union_row15.05 (seven instances, each +36), trial:i01.ug.Block7_union_row20.10 (three of four instances ±36 or +40), trial:i02.ug.Block7_union_row6.08 (five instances each +36), trial:i02.ug.Block7_union_row21.05 (two instances each +36), trial:i03.ug.Block7_union_row24.05 (two instances each +36).

Integer multiples of 36 dbu also appear without remainder: 72 dbu in trial:i01.ug.leaf_0002.23 and trial:i01.ug.leaf_0095.26; 108 dbu in trial:i01.ug.Block7_union_row7.19, trial:i01.ug.Block7_union_row9.21, and trial:i01.ug.leaf_0008.24. Non-multiples-of-36 do appear in a minority of ops (e.g., +28 in trial:i01.ug.Block7_union_row12.02, +40 in trial:i01.ug.Block7_union_row7.19, +4 in trial:i01.ug.Block7_union_row10.00), typically accompanying a 36 dbu move on a different instance within the same trial, suggesting they are fine-tuning adjustments to reach the exact spacing clearance required by V1.S.1 (18 nm on-track, 27 nm cross-track) or V1.M1.EN.1/V1.M2.EN.2 enclosure minimums.

Use 36 dbu as the first-try horizontal step for V1 spacing violations. Apply multiples (72, 108) when the clearance deficit exceeds one grid step.

## Multi-Instance Coordination

When a V1 spacing or enclosure violation involves a cluster of instances on the same M2 track, move all members of the cluster by the same delta. Single-instance moves that leave neighbors unmoved create asymmetric spacing that can generate new violations. The successful patterns uniformly move entire logical groups: trial:i01.ug.Block7_union_row15.05 moved seven instances each by +36 dbu x; trial:i02.ug.Block7_union_row6.08 moved five instances each by +36 dbu x; trial:i01.ug.Block7_union_row9.21 applied two distinct deltas (+36 and +56 and +108) to seven instances in sub-groups, adjusting each sub-group as a unit.

Do not move a single instance when the DRC marker spans two or more adjacent V1 shapes on the same M2 track; move the full set that shares the violating edge.

## Enclosure Rule Maintenance (V1.M1.EN.1, V1.M2.EN.2, V1.AUX.1)

Every instance move that changes V1 position relative to M1 or M2 requires a coordinated `resize_end` on the affected M1 or M2 polygon to restore the enclosure margin. This pattern is confirmed across multiple trials: trial:i01.ug.Block7_union_row3.15 combined a -36 dbu instance move with a +49 dbu `resize_end` on polygon p3379 (x high end); trial:i01.ug.leaf_0002.23 combined a +72 dbu instance move with a +128 dbu `resize_end` on M2 polygon p3695 (x high end); trial:i01.ug.leaf_0008.24 combined +40 and +108 dbu instance moves with a +164 dbu `resize_end` on p3771 (x high end); trial:i01.ug.Block7_union_row24.14 combined a +36 dbu instance move with a +36 dbu `resize_end` on p3058 (x high end).

The resize delta is not always equal to the move delta (trial:i01.ug.Block7_union_row3.15: move -36, resize +49; trial:i01.ug.leaf_0002.23: move +72, resize +128), indicating the resize must absorb both the displacement and any pre-existing enclosure deficit. Always pair a V1-bearing instance move with a resize of the enclosing M1/M2 polygon end on the side toward which the instance moved; resize the opposite end only when the post-move overlap on that side would violate V1.M2.AUX.2 (V1 width must match M2 width perpendicular to M2 length).

## Y-Axis Adjustments for Parallel-Track and AUX.2 Violations

Y-axis `move_instance` operations address V1.S.1 violations between V1 instances on parallel M2 tracks and V1.M2.AUX.2 width-matching failures. Confirmed patterns: trial:i01.ug.Block7_union_row14.04 moved two instances by +64 dbu y while also applying x-moves to other instances; trial:i01.ug.Block7_union_row19.09 moved two instances by -52 dbu y; trial:i02.ug.leaf_0021.14 moved one instance by -64 dbu y; trial:i02.ug.leaf_0022.15 moved one instance by -44 dbu y; trial:i02.ug.leaf_0032.17 moved two instances by +52 dbu y; trial:i03.ug.leaf_0020.09 moved one instance by +48 dbu y.

Y-step values in the recorded data: 8, 12, 16, 44, 48, 52, 57, 64, 72, 88 dbu. The 44 and 52 dbu steps appear repeatedly for resolving parallel-track spacing violations on specific row geometries. When the V1.S.1 check reports a parallel-track (cross-track projection) failure, apply a y-move to the V1 instance on the nearer track; use the minimum step that clears the 17 nm (projection) or 27 nm (Euclidean corner) threshold as required.

For the case where y-axis `resize_end` accompanies y-axis moves: trial:i01.ug.Block7_union_row12.02 applied +8 and -8 dbu y resizes to polygon p3694 (both ends), netting zero y-length change while shifting the center; trial:i03.ug.Block7_union_row14.01 applied a +8 dbu y `resize_end` to polygon p3515 alongside y-axis instance moves. Maintain M2 polygon y-extent when moving V1 instances vertically; resize the trailing edge of the M2 polygon to track the instance rather than leaving a gap that would violate V1.AUX.1 (V1 must be inside M1 and M2).

## Diagonal Moves

Some trials use a single `move_instance` op with nonzero x and y components simultaneously: trial:i01.ug.Block7_union_row23.13 moved instance i0041 by [-36, +44] dbu; trial:i01.ug.Block7_union_row22.12 moved i0132 by [+36, -48] dbu; trial:i03.ug.leaf_0010.08 moved i1062 by [+4, +44] dbu. These diagonal moves resolve compound violations where both x-spacing (V1.S.1 on-track or V1.M1.EN.1 x-side) and y-spacing (V1.S.1 parallel-track or V1.M2.EN.2 y-side) are simultaneously out of spec. Use a diagonal move rather than two sequential single-axis moves when both axes have independent clearance deficits; the result in all three cited cases was gated_in with conn_preserved.

## Polygon Move vs. Resize

Two mechanisms extend M2 polygon reach: `resize_end` (moves one edge, changes polygon size) and `op: move` on the whole polygon (translates without resizing). Both appear in the history. Polygon-level `move` is used when the entire M2 wire segment must shift to follow a V1 cluster, not just one edge: trial:i01.ug.Block7_union_row9.21 applied `op: move` to polygon p2720 (x +56 dbu); trial:i02.ug.Block7_union_row17.02 and trial:i03.ug.Block7_union_row17.02 both applied `op: move` to polygon p3631 in the y direction (+57 then -57 dbu respectively). Use `resize_end` when only the enclosure margin on one side is insufficient; use polygon `move` when the M2 segment and its V1 must shift together as a rigid body.

## Tolerance for New In-Crop Violations

Trials with `n_new_in_crop > 0` were still accepted when connectivity was preserved. Trial:i01.ug.Block7_union_row21.11 introduced 9 new in-crop violations and was gated_in; trial:i02.ug.leaf_0041.19 introduced 5; trial:i03.ug.leaf_0010.08 introduced 4; trial:i03.ug.leaf_0020.09 introduced 5. The gating criterion is conn_preserved, not zero new violations. Do not reject or revert a candidate operation solely because it increases the local violation count within the crop window; evaluate only whether connectivity is preserved. Downstream iterations address the newly introduced violations in subsequent passes (as confirmed by the pattern of the same units appearing across iter 1, iter 2, and iter 3 with shrinking or shifting loci).

## Iteration Convergence Pattern

The same unit IDs recur across iterations with modified loci, confirming iterative narrowing: Block7_union_row13 appears in iter 1 (trial:i01.ug.Block7_union_row13.03), iter 2 (trial:i02.ug.Block7_union_row13.00), and iter 3 (trial:i03.ug.Block7_union_row13.00) with loci shifting from [3520,15228,26640,16092] to [3520,15228,19692,16092] to [14200,15228,26516,16092], indicating the violation region migrated rightward after each partial fix. Block7_union_row14 and Block7_union_row17 follow the same multi-iteration pattern. Expect recurring units to need progressively smaller absolute-delta corrections as the design state converges; the iter 3 ops on these units use smaller or more targeted move sets than their iter 1 equivalents.

## NONORTHOGONAL Constraint

No `resize_end` or polygon `move` operation in the history produces a non-90-degree edge. All recorded deltas are applied exclusively to x or y axis endpoints or as axis-aligned translations. Do not apply diagonal polygon resizes; use only axis-aligned `resize_end` operations. Diagonal instance moves (compound x+y deltas on `move_instance`) are valid because they translate the entire cell rigidly and do not alter the angles of any drawn polygon edge.