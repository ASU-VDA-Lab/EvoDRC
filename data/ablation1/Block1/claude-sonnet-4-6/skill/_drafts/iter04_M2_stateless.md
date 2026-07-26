## Operation patterns and channel decisions

All trials through the `unit_gate` channel were accepted (`gated_in`) whenever `conn_preserved=true`, across all four iterations. The sole rejection came from the `cu_pool` channel (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00). No `unit_gate` trial was rejected.

## Move step quantization

Instance moves in the x-direction dominate the repair history. The base step is 36 dbu; accepted moves use 36, 72 (2×36), or 108 (3×36) dbu in the majority of operations (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row3.03, trial:i01.ug.Block1_union_row4.04, trial:i01.ug.Block1_union_row5.05, trial:i01.ug.Block1_union_row8.07, trial:i01.ug.Block1_union_row9.08, trial:i01.ug.leaf_0004.09, trial:i01.ug.leaf_0020.10, trial:i03.ug.Block1_union_row3.00, trial:i03.ug.leaf_0004.01, trial:i03.ug.leaf_0005.02, trial:i04.ug.leaf_0001.00, trial:i04.ug.leaf_0002.01). Non-multiples of 36 also appear in accepted trials: −32 dbu (trial:i01.ug.Block1_union_row6.06, trial:i01.ug.Block1_union_row8.07), 52 dbu (trial:i01.ug.Block1_union_row4.04), 92 dbu (trial:i01.ug.Block1_union_row3.03), and 128 dbu (trial:i01.ug.Block1_union_row1.00). A very small delta of 4 dbu in x was used in trial:i04.ug.leaf_0004.03, which produced 80 new in-crop violations but was still accepted because connectivity was preserved. Y-axis moves of −36 dbu appear in compound operations (trial:i01.ug.Block1_union_row4.04).

## Connectivity preservation overrides in-crop violations

The `gated_in` decision is granted whenever `conn_preserved=true`, regardless of `n_new_in_crop`. Trials with n_new_in_crop values of 1 (trial:i01.ug.Block1_union_row6.06, trial:i02.ug.Block1_union_row6.01), 4 (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.leaf_0031.11), and 80 (trial:i04.ug.leaf_0004.03) were all accepted. Do not reject or avoid operations solely because they introduce new in-crop violations, provided connectivity is preserved.

## M2 polygon end resizing (resize_end)

`resize_end` operations extend one end of an M2 polygon along the x-axis. Accepted resize_end deltas at the `high` end: 36 dbu (trial:i01.ug.Block1_union_row5.05), 52 dbu (trial:i01.ug.Block1_union_row4.04), 72 dbu (trial:i03.ug.leaf_0004.01), 92 dbu (trial:i01.ug.Block1_union_row3.03), 128 dbu (trial:i01.ug.Block1_union_row1.00). Resize_end at the `low` end of 36 dbu was accepted in trial:i01.ug.Block1_union_row5.05 and trial:i01.ug.leaf_0020.10. All confirmed resize_end operations act on the x-axis; no y-axis resize_end appears in the history. A symmetric `resize` (both ends simultaneously) of 36 dbu in x on polygon p1390 was accepted in trial:i01.ug.leaf_0031.11. Resize_end is consistently co-applied with move_instance operations in the same trial rather than applied in isolation (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row3.03, trial:i01.ug.Block1_union_row4.04, trial:i01.ug.Block1_union_row5.05, trial:i03.ug.leaf_0004.01).

## Via replacement via delete_instance + add_via

In trial:i02.ug.leaf_0004.02, an existing instance (i0300) was deleted and replaced by a new VIA_VIA12 cell placed at [5904, 6300] dbu using `add_via`. The operation touched M1/M2/V1 and was accepted with zero new in-crop violations. This pattern is valid for M2 enclosure or V1.M2.EN.2 / V1.M2.AUX.2 violations where the via placement alone, correctly positioned, satisfies the enclosure requirement on two opposite sides.

## V2.M2 via shape shrink in the cu_pool channel

In trial:i02.cu.def:VIA_VIA23_1_3_36_36.00, a `resize_via_shape` operation shrunk the M3 shape of cell `VIA_VIA23_1_3_36_36` by 40 dbu in the y-axis (delta_dbu=−40), affecting layers M2/M3/V2. The operation was rejected with decision `rejected_net_positive` and `delta_total=0`. The cu_pool channel requires a strictly positive net DRC improvement to accept; a zero-delta operation on via shape sizing does not qualify. Do not apply via-shape y-axis shrinks on VIA_VIA23 cells when the operation produces no net reduction in violation count.

## M2/M3/V2 instance moves in the unit_gate channel

A move of [−36, 0] dbu on instance i0452, touching M2/M3/V2 (not M1/M2/V1), was accepted with zero new in-crop violations in trial:i04.ug.leaf_0002.01. This confirms that instance moves affecting V2.M2.EN.1 geometry are handled through unit_gate with the same conn_preserved gating criterion as M1/M2/V1 repairs.

## Compound multi-instance operations

Trials combining up to five `move_instance` operations, or mixing `move_instance` with `resize_end` in a single trial, are consistently accepted when conn_preserved=true (trial:i01.ug.Block1_union_row1.00 with 3 moves + 2 resize_end; trial:i01.ug.Block1_union_row5.05 with 3 moves + 2 resize_end; trial:i01.ug.Block1_union_row8.07 with 5 moves; trial:i02.ug.Block1_union_row6.01 with 5 moves; trial:i03.ug.Block1_union_row3.00 with 3 moves + 1 resize_end). Compound operations that address multiple instances simultaneously are a reliable repair strategy for M2 spacing and enclosure violations when connectivity is not broken.

## Orthogonality constraint

All accepted move and resize operations produce axis-aligned M2 geometry: delta_dbu values are always in the x or y direction exclusively, with no diagonal components. The GEOMETRY.NONORTHOGONAL rule fires on any edge with angle outside {0, 90, 180, 270} degrees on every drawing layer including M2. All operations in the history respect this: maintain Manhattan geometry on all M2 modifications.

## Iteration convergence pattern

Across four iterations the per-trial n_new_in_crop counts at acceptance were predominantly 0 (15 of 20 trials), with non-zero counts appearing at iterations 1, 2, and 4 (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row6.06, trial:i01.ug.leaf_0031.11, trial:i02.ug.Block1_union_row6.01, trial:i04.ug.leaf_0004.03). The high in-crop count of 80 at trial:i04.ug.leaf_0004.03 indicates that a late-iteration move with very small x-delta (4 dbu) can displace many M2 segments relative to their spacing context without breaking connectivity; such operations are gated in but may require subsequent correction trials to resolve the introduced violations.