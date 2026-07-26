**Operation types observed on M1**

All operations recorded for M1 are either `move_instance` or `resize_end` (axis `x`, end `high`). Every `move_instance` delta carries a zero Y component; no vertical instance displacement appears in any trial (trial:i01.ug.Block3_union_row1.00, trial:i01.ug.Block3_union_row2.01, trial:i01.ug.Block3_union_row5.02, trial:i01.ug.Block3_union_row8.03, trial:i01.ug.leaf_0006.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0008.06, trial:i01.ug.leaf_0009.07, trial:i01.ug.leaf_0012.08, trial:i01.ug.leaf_0013.09, trial:i02.ug.leaf_0001.00). Do not apply Y-axis displacements to M1 instances to repair spacing or enclosure violations.

**Grid discipline**

Every delta magnitude is a non-zero multiple of 36 dbu. Values of 36, 72, and 108 dbu all appear and are all accepted: trial:i01.ug.Block3_union_row1.00 and trial:i01.ug.Block3_union_row8.03 include 108 dbu moves; trial:i02.ug.leaf_0001.00 uses 72 dbu; the remaining iter-1 trials use 36 dbu. Snap all M1 instance moves and polygon end adjustments to the 36 dbu grid.

**Move direction polarity**

Both positive and negative X displacements are accepted. trial:i01.ug.leaf_0013.09 applied a [-36, 0] delta and was accepted with `conn_preserved` and zero new violations. Do not restrict moves to one direction; choose the polarity that closes the specific spacing or enclosure gap.

**Connectivity preservation is the acceptance gate**

Every accepted trial carries `conn_preserved: true` and `reason: conn_preserved`. In every case `n_new_in_crop` and `n_new_out_of_crop` are both 0 (trial:i01.ug.Block3_union_row1.00 through trial:i02.ug.leaf_0001.00). An operation that preserves connectivity and introduces zero new crop violations is gated in. Any move that would sever a net connection must not be applied.

**Multi-instance batching within a locus**

A single trial may move between one and four instances simultaneously. trial:i01.ug.Block3_union_row8.03 moved four instances in one operation; trial:i01.ug.Block3_union_row1.00 moved three. All instances within the same locus window that share a root DRC violation can be corrected in one batched operation without creating secondary violations, as confirmed by zero new violations across all multi-instance trials.

**resize_end on M1 polygons**

Two trials include a `resize_end` on polygon p1261 (axis `x`, end `high`) alongside move_instance steps: trial:i01.ug.leaf_0008.06 (delta 36 dbu, iter 1) and trial:i02.ug.leaf_0001.00 (delta 72 dbu, iter 2, same locus). Both were accepted with zero new violations and connectivity preserved. Use resize_end on the high-x end of an M1 polygon when the enclosure shortfall is on the polygon boundary and cannot be resolved by instance movement alone. V0.M1.EN.1 requires ≥5 nm enclosure of V0 by M1 on two opposite sides; V1.M1.EN.1 requires ≥5 nm and ≥2 nm on opposite sides. A resize_end that extends the relevant M1 edge is the direct repair for either enclosure deficit at that boundary.

**Iter-2 delta scaling on revisited loci**

trial:i02.ug.leaf_0001.00 revisits locus [9232, 5508, 10080, 8532] — the same window as trial:i01.ug.leaf_0008.06 — under a new design_state reflecting committed iter-1 changes. The delta applied in iter 2 is 72 dbu versus 36 dbu in iter 1, a 2× increase. When a locus is revisited in a subsequent iteration because the prior fix was insufficient, increase the move and resize delta proportionally rather than repeating the same magnitude.

**Layer co-movement**

Every trial touches exactly the set {M1, M2, V1}. No trial touches M1 in isolation. When correcting an M1 violation by moving an instance, the associated V1 and M2 geometry moves with the instance automatically; the fix applies across all three layers in one operation.

**No secondary violations introduced**

All eleven trials concluded with `n_new_in_crop: 0` and `n_new_out_of_crop: 0`. The operations as applied never triggered M1.W.1 (18 nm min width), M1.S.1 (18 nm side-to-side spacing), M1.S.2 (25 nm tip-to-side), M1.S.3 (27 nm wide-tip-to-tip), M1.A.1 (504 nm² min area), V0.M1.AUX.3 (V0 width must match M1 perpendicular width), or GEOMETRY.NONORTHOGONAL as secondary violations. The recorded resize_end operations are axis-aligned (trial:i01.ug.leaf_0008.06, trial:i02.ug.leaf_0001.00) and produce no diagonal M1 edges. Maintain orthogonal-only geometry on M1; any edit that would produce a non-axis-aligned edge violates GEOMETRY.NONORTHOGONAL.