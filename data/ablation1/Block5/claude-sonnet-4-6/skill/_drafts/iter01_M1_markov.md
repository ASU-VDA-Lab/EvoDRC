All six iteration-1 trials for layer M1 are from Block5, channel unit_gate, and all carried a `gated_in` decision with `conn_preserved=true` and zero new in-crop or out-of-crop violations. The conclusions below are grounded exclusively in those records.

## Repair move direction and magnitude

All successful M1 repairs in this iteration used x-axis displacement only; no y-direction move appeared in any trial. Instance moves of +36 dbu in x are the dominant single-step displacement: this value appears in trials trial:i01.ug.Block5_union_row3.00, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, and trial:i01.ug.leaf_0006.05. A smaller move of +4 dbu in x was sufficient for trial:i01.ug.Block5_union_row6.01, which moved two instances by the same delta. Use x-direction displacements; do not introduce y-direction moves when repairing M1 violations of the types seen here.

## Counter-directional instance pairs

Moving two instances in opposite x-directions (+36 and -36 dbu respectively) in the same repair set resolves violations without new violations (trial:i01.ug.leaf_0002.03, ops move i0056 by +36 and i0103 by -36). This pattern is safe when connectivity is preserved across the pair.

## M1 polygon resize on high-x end

Extending the high-x end of an M1 polygon (resize_end, axis x, end high) by +36 dbu alongside a matching instance move resolves violations cleanly (trial:i01.ug.Block5_union_row3.00, polygon p967). A larger extension of +72 dbu on the high-x end of M1 polygon p974, paired with a +36 dbu instance move, is also violation-free (trial:i01.ug.leaf_0001.02). Apply resize_end on the high-x edge of the relevant M1 polygon when the enclosure or width margin requires it; do not resize the low-x end when the high-x end is the deficient side.

## Operation count

Repair sets of 1, 2, or 3 operations all achieved clean outcomes in this iteration. Single-op repairs (trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05) are viable when one instance move alone restores the required enclosure or spacing. Do not add superfluous operations beyond what the geometry requires.

## Touched-layer scope

Every trial touched M1, M2, and V1 together. M1 instance moves propagate through V1 to M2; verify V1.M1.EN.1 and V1.M1.EN.1 enclosure constraints after any M1 displacement, since M1 and V1 move together when an instance is repositioned (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.Block5_union_row6.01, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05).

## Connectivity preservation as a gate

All gated_in decisions in this iteration share `conn_preserved=true`. Repairs that break connectivity are excluded from the gated_in channel. Preserve all net connections when constructing a repair set; a topologically disconnecting move must not be submitted even if it would satisfy M1 spacing or width rules.