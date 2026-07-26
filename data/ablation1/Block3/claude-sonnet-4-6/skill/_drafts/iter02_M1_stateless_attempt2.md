**Operation outcomes and accepted move magnitudes**

Every trial recorded in the Block3 unit_gate channel for iteration 1 was accepted with `decision: gated_in` and zero new DRC violations in the crop (`n_new_in_crop: 0`, `n_new_out_of_crop: 0`). The full set of accepted trials is: trial:i01.ug.Block3_union_row1.00, trial:i01.ug.Block3_union_row2.01, trial:i01.ug.Block3_union_row5.02, trial:i01.ug.Block3_union_row8.03, trial:i01.ug.leaf_0006.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0008.06, trial:i01.ug.leaf_0009.07, trial:i01.ug.leaf_0012.08, trial:i01.ug.leaf_0013.09. The single iteration-2 trial trial:i02.ug.leaf_0001.00 was also accepted with the same zero-violation outcome.

The only accepted move magnitudes for `move_instance` operations are 36 dbu and 108 dbu in the x-axis. Moves of 36 dbu appeared in trial:i01.ug.Block3_union_row2.01, trial:i01.ug.Block3_union_row5.02, trial:i01.ug.leaf_0006.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0009.07, trial:i01.ug.leaf_0012.08, and trial:i01.ug.leaf_0013.09. Moves of 108 dbu appeared in trial:i01.ug.Block3_union_row1.00 and trial:i01.ug.Block3_union_row8.03. A move of 72 dbu was accepted in trial:i02.ug.leaf_0001.00 for instance i0047. All accepted moves are multiples of 36 dbu on the x-axis only; no y-axis moves appear in any record.

**Move direction polarity**

Both positive-x and negative-x moves are represented in the accepted history. Positive-x moves (delta_dbu [36,0] or [108,0]) were accepted in trial:i01.ug.Block3_union_row1.00, trial:i01.ug.Block3_union_row2.01, trial:i01.ug.Block3_union_row5.02, trial:i01.ug.Block3_union_row8.03, trial:i01.ug.leaf_0006.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0008.06, trial:i01.ug.leaf_0009.07, trial:i01.ug.leaf_0012.08, and trial:i02.ug.leaf_0001.00. A negative-x move (delta_dbu [-36,0]) was accepted in trial:i01.ug.leaf_0013.09. Both polarities preserved connectivity and introduced no new M1 violations, so neither direction is disqualified on DRC grounds alone.

**resize_end operations on M1**

Two trials used `resize_end` on axis `x`, end `high`: trial:i01.ug.leaf_0008.06 applied delta_dbu 36 to polygon p1261 alongside two `move_instance` operations and was accepted; trial:i02.ug.leaf_0001.00 applied delta_dbu 72 to the same polygon p1261 alongside a 72 dbu move of instance i0047 and was also accepted with no new M1 violations. Apply `resize_end` only on the `high` end of the x-axis at the same grid multiple (36 dbu or 72 dbu) used for co-located `move_instance` operations in the same trial, as established by trial:i01.ug.leaf_0008.06 and trial:i02.ug.leaf_0001.00.

**Connectivity preservation as a gate condition**

All 11 accepted trials carried `conn_preserved: true` and `reason: conn_preserved`. Never apply a move or resize that breaks connectivity; the gate check rejects such operations before DRC is even evaluated. Every accepted operation in this history — including moves of instances across multiple rows in trial:i01.ug.Block3_union_row1.00 (3 instances moved) and trial:i01.ug.Block3_union_row8.03 (4 instances moved) — preserved connectivity.

**Multi-instance move coordination**

Trials that moved multiple instances in a single operation used consistent or closely related delta magnitudes within the same trial. In trial:i01.ug.Block3_union_row1.00, instances i0233 moved 36 dbu while i0246 and i0205 each moved 108 dbu; all were accepted together. In trial:i01.ug.Block3_union_row8.03, three instances moved 36 dbu and one moved 108 dbu together. Do not assume all instances in a multi-move trial must share the same delta; trial:i01.ug.Block3_union_row1.00 demonstrates mixed deltas (36 and 108 dbu) are accepted when connectivity is preserved.

**Layer interaction scope**

Every trial in this history touched layers M1, M2, and V1 together. No trial touched M1 in isolation. When repairing M1 violations, treat M1, V1, and M2 as a coupled group; moves that shift M1 geometry also affect V1 enclosure (rules V0.M1.EN.1, V0.M1.AUX.3, V1.M1.EN.1) and M2 via V1. All accepted trials in this history confirm that 36 dbu and 108 dbu x-axis moves are consistent with maintaining V0 and V1 enclosure requirements simultaneously — trial:i01.ug.leaf_0008.06 and trial:i02.ug.leaf_0001.00 additionally confirm that a coordinated resize_end on M1 together with a matching instance move does not break V1.M1.EN.1.

**Revisiting a locus across iterations**

The locus [9232,5508,10080,8532] was addressed in iteration 1 (trial:i01.ug.leaf_0008.06, 36 dbu moves and resize) and again in iteration 2 (trial:i02.ug.leaf_0001.00, 72 dbu moves and resize on the same polygon p1261 and overlapping instances). Both passes were accepted. When a locus requires a second pass, apply larger deltas (double the prior step) to the same polygon and instance set as established by trial:i02.ug.leaf_0001.00 relative to trial:i01.ug.leaf_0008.06.