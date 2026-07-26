**Observed operation types and step sizes**

All 11 accepted trials used `move_instance` on the x-axis with delta values drawn from the set {-36, 36, 108} dbu (trial:i01.ug.Block3_union_row1.00, trial:i01.ug.leaf_0013.09, trial:i01.ug.Block3_union_row8.03). Every trial returned `n_new_in_crop: 0` and `n_new_out_of_crop: 0`, meaning no new violations entered the crop window under these step choices. Use x-axis `move_instance` in multiples of 36 dbu to keep V1 geometry aligned with the M2 track grid and satisfy V1.W.1's 18 nm minimum width together with the projection-based spacing thresholds in V1.S.1 (trial:i01.ug.leaf_0009.07, trial:i01.ug.leaf_0012.08, trial:i02.ug.leaf_0001.00).

The minimum step of 36 dbu suffices for single-instance corrections (trial:i01.ug.leaf_0009.07, trial:i01.ug.leaf_0012.08, trial:i01.ug.leaf_0013.09). Use 108 dbu (3× the minimum) when two or more instances within the same unit require differential x-offsets — in trial:i01.ug.Block3_union_row1.00, instance i0233 moved 36 dbu while i0246 and i0205 each moved 108 dbu within the same crop window, and the trial was accepted with zero new violations.

No y-axis deltas appear in any accepted record across all 11 trials (trial:i01.ug.Block3_union_row1.00 through trial:i02.ug.leaf_0001.00). Apply moves on the x-axis only; V1.S.1's projection-based spacing check operates along the M2 track direction, and y-axis displacement would risk introducing new cross-track spacing violations without benefit to the V1.S.1 projection metric.

**Co-modification of M1, M2, and V1**

Every accepted trial touched layers M1, M2, and V1 together; no trial modified V1 without simultaneously touching M1 and M2 (trial:i01.ug.Block3_union_row1.00, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0008.06, trial:i02.ug.leaf_0001.00). V1.AUX.1 requires V1 to reside inside both M1 and M2; V1.M2.AUX.2 requires V1 width to match M2 width along the direction perpendicular to M2 length. Moving a V1-bearing instance therefore repositions all three layers as a unit. Apply repairs at the instance level rather than by editing V1 geometry in isolation, so that M1 and M2 enclosure constraints (V1.M1.EN.1, V1.M2.EN.2) remain satisfied after the move.

**Resize-end operations**

Two trials combined `move_instance` with a `resize_end` on the high x-end of polygon p1261 (axis x, end high): trial:i01.ug.leaf_0008.06 (resize delta 36 dbu) and trial:i02.ug.leaf_0001.00 (resize delta 72 dbu). Both were accepted with `conn_preserved: true` and zero new crop violations. Apply `resize_end` at the high x-end when instance moves alone do not close the M2 end-cap gap required by V1.M2.EN.2 or the width-match required by V1.M2.AUX.2. Match the resize delta to the same 36 dbu grid used for move deltas (trial:i01.ug.leaf_0008.06, trial:i02.ug.leaf_0001.00).

**Iter-2 step doubling at the same locus**

Trial:i02.ug.leaf_0001.00 targeted the same spatial locus [9232, 5508, 10080, 8532] as trial:i01.ug.leaf_0008.06 and applied doubled deltas: 72 dbu for the `move_instance` and 72 dbu for the `resize_end`, versus 36 dbu each in iteration 1. The iter-2 trial was accepted with zero new violations and `conn_preserved: true`. When a locus recurs in a later iteration, double the previous step size for both the move and the accompanying resize rather than repeating the same delta.

**Connectivity preservation**

All 11 trials preserved connectivity (`conn_preserved: true`, trial:i01.ug.Block3_union_row1.00 through trial:i02.ug.leaf_0001.00). Restricting moves to the x-axis and keeping resize operations to the high x-end of polygons that already carry V1 instances maintains the net topology. Do not resize the low x-end or move on the y-axis; no accepted trial applied either, and both would risk disconnecting M2 segments that bridge adjacent V1 instances.