## Move-grid discipline

All M2-touching `move_instance` and `resize_end` operations in the measured history use x-axis deltas that are exact non-zero multiples of 36 dbu. Observed values are 36, 72, and 108 dbu (trial:i01.ug.Block3_union_row1.00, trial:i01.ug.leaf_0008.06, trial:i02.ug.leaf_0001.00). No sub-36-dbu or fractional-grid step has ever been applied to an M2-affecting operation. Do not propose a correction at any granularity finer than 36 dbu.

## Axis restriction

Every correction recorded against M2 is purely horizontal (x-axis). No y-axis `move_instance` or `resize_end` operation appears in any trial (trial:i01.ug.Block3_union_row1.00 through trial:i02.ug.leaf_0001.00). Do not propose vertical moves to resolve M2 spacing or width violations.

## Direction polarity

Positive-x movement (+36 to +108 dbu) is the standard polarity: nine of the ten iter-1 unit_gate trials use positive deltas (trial:i01.ug.Block3_union_row1.00, trial:i01.ug.Block3_union_row2.01, trial:i01.ug.Block3_union_row5.02, trial:i01.ug.Block3_union_row8.03, trial:i01.ug.leaf_0006.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0008.06, trial:i01.ug.leaf_0009.07, trial:i01.ug.leaf_0012.08). Negative-x movement (-36 dbu) was accepted once (trial:i01.ug.leaf_0013.09) and also received decision `gated_in`. Both polarities are structurally legal; positive-x is the preferred default direction.

## Paired resize_end when an M2 polygon endpoint must track its host instance

When an instance move would leave an M2 polygon endpoint stranded (decoupled from the moved geometry), a `resize_end` operation on the high-x edge of the affected polygon must accompany the move with exactly the same delta. In trial:i01.ug.leaf_0008.06, instance i0047 was moved +36 dbu and polygon p1261's high-x end was simultaneously extended +36 dbu; the trial was accepted with `conn_preserved=true` and zero new violations. In trial:i02.ug.leaf_0001.00, the same i0047 and p1261 received matching +72 dbu deltas under the same acceptance criteria. Always apply `resize_end` with a matching delta whenever the corrected instance carries an M2 segment whose far endpoint is not anchored by another instance in the same op-set.

## Iteration escalation on residual violations

A +36 dbu correction applied to i0047 and p1261 in iter 1 (trial:i01.ug.leaf_0008.06) did not fully resolve the underlying violation; the same objects required a +72 dbu correction in iter 2 (trial:i02.ug.leaf_0001.00). When a prior iteration's correction to a specific instance or polygon was insufficient, double the delta on the subsequent attempt rather than repeating the same step size.

## Multi-instance ops within a unit crop

Unit_gate trials routinely bundle two to four `move_instance` operations inside a single trial. Multi-instance ops with mixed deltas (e.g., 36 and 108 dbu on different instances within the same unit, trial:i01.ug.Block3_union_row1.00; 36 and 108 on four instances, trial:i01.ug.Block3_union_row8.03) are accepted by the gating check provided each instance's M2 geometry remains internally consistent. Group all logically coupled instances into a single trial rather than issuing separate single-instance trials.

## Gating acceptance criterion for unit_gate channel

Every unit_gate trial in the measured history received decision `gated_in`. The invariant present in all accepted trials is: `conn_preserved=true`, `n_new_in_crop=0`, and `n_new_out_of_crop=0` (trial:i01.ug.Block3_union_row1.00 through trial:i02.ug.leaf_0001.00). Any proposed M2 correction must satisfy all three conditions simultaneously; introducing even one new violation anywhere in the crop, or breaking connectivity, causes rejection. The gating check is crop-local but connectivity-global.

## Via enclosure repairs belong to the cu_pool channel, not unit_gate

V2.M2.EN.1 violations (minimum 5 nm M2 enclosure of V2 on two opposite sides) are repaired exclusively through the cu_pool channel by editing via cell shapes directly. Trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 eliminated 27 violations across two units (leaf_0018: -15, leaf_0019: -12) by applying a combination of `move_via_shape` and `resize_via_shape` operations to three shapes inside the VIA_VIA23_1_3_36_36 cell, using x-axis deltas of 144 dbu (move) and 288 dbu (resize). Do not attempt to repair V2.M2.EN.1 through unit_gate instance moves; the cu_pool via-shape path is the proven mechanism (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

## Layer stack separation by channel

Unit_gate operations always touch exactly the set {M1, M2, V1} (all ten unit_gate trials, iter 1 and iter 2). The cu_pool operation touched {M2, M3, V2} (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). These two layer stacks are mutually exclusive per trial. Do not construct a trial that mixes unit_gate instance moves with via-cell edits; they must be issued through their respective channels.

## Design state and inter-iteration commitment

The design_state hash changed from `fa7319eece0a9b26b444e9a0d864a3703ec997046c6414b63de8e4f61d0e7958` (all iter-1 trials) to `8472bfa7592d4d7776dfe2bc755ed7dd066cdb7858088beb48f31019b83ef43f` (iter-2 trial:i02.ug.leaf_0001.00), confirming that all iter-1 results were committed to the layout before iter-2 trials ran. Each iteration operates on the cumulative post-commit state of all prior iterations; corrections applied in earlier iterations are permanent and not re-evaluated from the original baseline.