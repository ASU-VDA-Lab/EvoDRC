**Instance-move quantum for M1-touching repairs**

All 10 accepted trials in iteration 1 use x-axis-only instance moves with delta magnitudes that are integer multiples of 36 dbu (36, 108). Moves of +36 dbu and +108 dbu on instances whose geometries touch M1, M2, and V1 produced zero new DRC violations within the crop and preserved all connectivity (trial:i01.ug.Block3_union_row1.00, trial:i01.ug.Block3_union_row2.01, trial:i01.ug.Block3_union_row5.02, trial:i01.ug.Block3_union_row8.03, trial:i01.ug.leaf_0006.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0008.06, trial:i01.ug.leaf_0009.07, trial:i01.ug.leaf_0012.08). Apply x-axis instance moves in multiples of 36 dbu when targeting M1 spacing or enclosure violations.

**Negative-x moves on M1-touching instances**

A move of -36 dbu in x on an M1/M2/V1-touching instance also produced zero new violations and preserved connectivity (trial:i01.ug.leaf_0013.09). Both positive and negative x-direction moves of 36 dbu are valid repair steps for M1.

**resize_end on M1 polygon high-x edge**

Extending the high-x end of an M1 polygon by 36 dbu (resize_end, axis x, end high) in the same move set as instance displacements produced no new DRC violations and preserved connectivity (trial:i01.ug.leaf_0008.06). Use resize_end on M1 polygon high-x edges in 36 dbu increments to resolve enclosure shortfalls on V0 or V1 when the enclosing M1 edge falls short on the positive-x side.

**Multi-instance batch moves remain clean**

Batch moves of 2, 3, and 4 instances within a single operation set, all touching M1/M2/V1, were accepted with zero new violations (trial:i01.ug.Block3_union_row1.00 with 3 ops, trial:i01.ug.Block3_union_row8.03 with 4 ops, trial:i01.ug.Block3_union_row2.01 with 2 ops). Do not limit repair sets to single-instance moves; multi-instance moves within the same locus are safe when connectivity is preserved.

**Connectivity preservation is a necessary gate condition**

Every trial accepted in iteration 1 carries conn_preserved: true and n_new_in_crop: 0. No trial with conn_preserved: false appears in the accepted set. Always verify connectivity preservation before committing a move_instance or resize_end operation on M1.