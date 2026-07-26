## Operation Channels and Strategy

Two distinct repair channels operate on M2: `unit_gate` and `cu_pool`. The `unit_gate` channel repairs M2 violations by moving cell instances and resizing M2 polygon endpoints within standard design units. The `cu_pool` channel repairs violations in via cell definitions by modifying via and surrounding metal shapes directly. Use `unit_gate` for instance-level M2 geometry correction and `cu_pool` for via cell enclosure violations; trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 achieved a -78 total violation reduction via V2 shape resizing within a via cell, touching M2, M3, and V2 simultaneously.

## Co-Moving M2 with Adjacent Layers

Never move M2 instances or resize M2 polygons in isolation within the `unit_gate` channel. Every unit_gate trial in the record co-touches M1, M2, and V1 together (trial:i01.ug.Block6_union_row3.00, trial:i01.ug.Block6_union_row5.01, trial:i01.ug.Block6_union_row7.02, trial:i01.ug.Block6_union_row8.03, trial:i01.ug.leaf_0001.04, trial:i01.ug.leaf_0011.05, trial:i01.ug.leaf_0015.06, trial:i01.ug.leaf_0018.07, trial:i02.ug.Block6_union_row4.00, trial:i02.ug.Block6_union_row7.01, trial:i02.ug.Block6_union_row8.02, trial:i02.ug.leaf_0004.04, trial:i03.ug.leaf_0001.00, trial:i05.ug.leaf_0001.00). Co-moving V1 with M2 satisfies V1.M2.EN.2 (minimum M2 enclosure of V1 on two opposite sides is 5 nm on each side, or 5 nm and 0 nm) by construction: when M2 translates, V1 translates by the same delta, preserving the enclosure margin without requiring a separate enclosure check after each move.

## Primary Move Direction

Apply positive x-direction (rightward) move_instance deltas as the primary M2 repair strategy. Across all unit_gate trials, x move deltas of +28, +36, +56, +72, +104, +112, and +136 dbu appear and all produce conn_preserved acceptance (trial:i01.ug.Block6_union_row3.00 at +72 dbu, trial:i01.ug.Block6_union_row5.01 at +36 dbu, trial:i01.ug.leaf_0001.04 at +112 dbu, trial:i02.ug.Block6_union_row4.00 at +56 and +112 dbu, trial:i02.ug.leaf_0004.04 at +72 dbu, trial:i05.ug.leaf_0002.01 at +136 dbu). Y-axis moves appear only in trial:i05.ug.leaf_0002.01, where two instances (i0384, i0528) each receive a +24 dbu y-delta; all other unit_gate moves are strictly x-axis. Restrict y-axis moves to cases where x-only moves cannot resolve the conflict.

## resize_end Direction and M2.S.7 Parallel Run Length

Use resize_end on the high-x end (end="high") with positive delta_dbu as the standard endpoint extension operation. Every resize_end in the record except one uses end="high" with a positive expansion: trial:i01.ug.Block6_union_row5.01 (+92 dbu, p2072), trial:i01.ug.Block6_union_row7.02 (+124 dbu, p1903), trial:i01.ug.leaf_0001.04 (+132 dbu, p2016), trial:i01.ug.leaf_0015.06 (+48 dbu, p1923), trial:i02.ug.Block6_union_row4.00 (+132 dbu, p2020), trial:i05.ug.leaf_0001.00 (+12 dbu, p2071), trial:i05.ug.leaf_0002.01 (+168 dbu p2086, +132 dbu p1946, +100 dbu p2046).

The single end="low" resize occurs in trial:i01.ug.Block6_union_row7.02 (p1920, +56 dbu) and is paired in the same trial with a -36 dbu move_instance on i0074. Do not apply end="low" resize without a compensating instance move in the same trial.

Expanding the high-x end of M2 polygons increases parallel run length, directly targeting M2.S.7: when tip-to-tip spacing is 18 nm and side-to-side spacing is <= 32 nm simultaneously, the run length must reach at least 35 nm. The large high-end expansions (92-168 dbu) observed in trials above achieve this clearance in a single operation.

## Iterative Refinement: Coarse Then Fine

Apply large x-direction move deltas in early iterations and small correction deltas in later iterations for the same unit. Iter 1 uses deltas of 28-112 dbu across all unit_gate trials. Iter 2 applies fine corrections of +4 dbu (trial:i02.ug.Block6_union_row7.01) and +8 dbu (trial:i02.ug.Block6_union_row8.02) to units Block6_union_row7 and Block6_union_row8, which were already adjusted in iter 1 at larger deltas (trial:i01.ug.Block6_union_row7.02 at +104/-36 dbu, trial:i01.ug.Block6_union_row8.03 at +36 dbu). Apply coarse moves first to resolve dominant spacing violations (M2.S.1 side-to-side 18 nm, M2.S.2 tip-to-side 25 nm), then apply small delta corrections to close remaining margin gaps.

## Gating: Connectivity Preservation Overrides New In-Crop Violations

The gating criterion accepts an operation when connectivity is preserved (conn_preserved=true), even when the operation introduces new in-crop DRC violations. Iter 5 trials accepted with n_new_in_crop=12 (trial:i05.ug.leaf_0001.00) and n_new_in_crop=22 (trial:i05.ug.leaf_0002.01) despite nonzero new violations, both gated_in with reason "conn_preserved". All iters 1-3 unit_gate trials achieved n_new_in_crop=0 (trial:i01.ug.Block6_union_row3.00 through trial:i03.ug.leaf_0001.00). Do not treat a gated_in decision as proof of zero new violations in later iterations; read the n_new_in_crop field directly from the delta record to determine whether secondary cleanup is needed.

## Via Cell Enclosure Repair (V2.M2.EN.1)

For V2.M2.EN.1 violations (V2 must be enclosed by M2 by at least 5 nm on at least two opposite sides), use the cu_pool channel to resize via cell shapes directly rather than moving instances. Trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 moved and resized three V2 shape indices within cell VIA_VIA23_1_3_36_36 (x-deltas: -144 dbu move shape_index 0, +264 dbu resize shape_index 0, +288 dbu resize shape_index 1, +144 dbu move shape_index 2, +264 dbu resize shape_index 2), reducing total violations by 78 across two windows (leaf_0019: 139→97, leaf_0020: 154→118). The fix simultaneously touches M2 and M3 alongside V2, confirming that via cell enclosure repair must modify both the via layer and its enclosing metal layers together.

## M2 Width and Area Preservation

All resize_end operations in the record expand M2 polygons or apply low-end shrinks paired with compensating instance moves, maintaining M2 widths above the 18 nm minimum (M2.W.1) and areas above the 504 nm² minimum (M2.A.1). The one low-end shrink (trial:i01.ug.Block6_union_row7.02, p1920 +56 dbu from low) is paired in the same trial with a -36 dbu move_instance on i0074. Apply end="low" shrinks only when a same-trial instance move compensates to prevent width reduction below 18 nm.

## Orthogonality Requirement

All M2 geometry modifications must remain strictly orthogonal (0° and 90° edges only). Every move_instance and resize_end in the record is axis-aligned: move deltas specify only x or y (not both nonzero for diagonal translation), and resize_end specifies axis="x" exclusively in the record. This is required by the NONORTHOGONAL block, which flags any edge on M2 with angle outside {0°, 90°, 180°, 270°}. All clean iters 1-3 results (trial:i01.ug.Block6_union_row3.00 through trial:i03.ug.leaf_0001.00) demonstrate that purely axis-aligned operations satisfy this constraint.

## Operation Count Relative to Locus Size

Single-unit small-locus trials use one operation and produce zero new violations (trial:i01.ug.leaf_0011.05, trial:i01.ug.leaf_0018.07, trial:i02.ug.Block6_union_row7.01, trial:i03.ug.leaf_0001.00). Trials with larger loci or multi-unit scope use more operations: trial:i05.ug.leaf_0002.01 covers a near-full-design locus and includes 7 operations (3 resize_end, 4 move_instance across x and y) and introduces n_new_in_crop=22. Do not expand operation count beyond what the locus geometry requires; clean zero-new-violation outcomes correlate with targeted single- or two-operation trials in iters 1-3.