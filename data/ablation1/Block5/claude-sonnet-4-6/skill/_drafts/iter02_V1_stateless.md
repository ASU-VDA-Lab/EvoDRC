## Observed Repair Patterns

All eight accepted trials across iterations 1 and 2 carry `decision=gated_in`, `conn_preserved=true`, `n_new_in_crop=0`, and `n_new_out_of_crop=0`. Every operation that touched V1 also touched M1 and M2 in the same trial (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.Block5_union_row6.01, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05, trial:i02.ug.Block5_union_row6.00, trial:i02.ug.leaf_0002.02). V1 DRC violations in the `unit_gate` channel are therefore never isolated to V1 geometry alone; M1 and M2 must be adjusted concurrently.

## Effective Operation Types

Two operation kinds account for all successful repairs.

**Instance moves in X only.** Every trial used one or more `move_instance` ops with a non-zero X delta and a zero Y delta. No Y-direction moves appear anywhere in the history. Do not apply Y-direction moves to repair V1 violations; all measured successful repairs used X-only translation (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.Block5_union_row6.01, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05, trial:i02.ug.Block5_union_row6.00, trial:i02.ug.leaf_0002.02).

**M2 polygon resize on the X-axis high end.** Three of the eight trials supplemented instance moves with a `resize_end` op on an M2 polygon, always specifying `axis=x` and `end=high` (trial:i01.ug.Block5_union_row3.00 resized p967 by +36 dbu; trial:i01.ug.leaf_0001.02 resized p974 by +72 dbu; trial:i02.ug.Block5_union_row6.00 resized p955 by +20 dbu). No low-end, Y-axis, or shrink (`resize_end` with a negative delta) operations appear in any accepted trial. Apply `resize_end` only to the high end of the X-axis of M2 polygons when supplementing an instance move.

## Move Magnitude Selection

The accepted X-direction move deltas are 4 dbu (trial:i01.ug.Block5_union_row6.01), 36 dbu (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05), 72 dbu (trial:i02.ug.leaf_0002.02), and 104 dbu (trial:i02.ug.Block5_union_row6.00). The most frequently applied single-instance move magnitude is 36 dbu.

A 4 dbu correction applied to unit Block5_union_row6 in iteration 1 (trial:i01.ug.Block5_union_row6.01) proved insufficient: the same unit required re-repair in iteration 2 with a 104 dbu move plus a 20 dbu M2 end resize (trial:i02.ug.Block5_union_row6.00). Do not use a 4 dbu correction for Block5_union_row6; apply at minimum 104 dbu in X with a corresponding M2 high-end resize.

## Bidirectional (Spread) Moves for Inter-Instance Spacing

When two nearby instances contribute to the same spacing violation, moving them in opposite X directions resolves the violation without introducing new ones. In trial:i01.ug.leaf_0002.03, instance i0056 moved +36 dbu and instance i0103 moved -36 dbu within the same locus; the result was gated in with zero new violations. Use bidirectional symmetric moves when the locus contains two instances that need to be separated.

## Multi-Instance Co-Move

Several trials moved two or more instances by the same delta in the same direction. In trial:i01.ug.Block5_union_row3.00, i0117 and i0131 both moved +36 dbu in X. In trial:i01.ug.Block5_union_row6.01, i0025 and i0019 both moved +4 dbu. In trial:i02.ug.Block5_union_row6.00, i0025 and i0019 both moved +104 dbu. Moving all instances in a locus by the same delta preserves their relative spacing and is confirmed safe by these accepted trials.

## M2 End-Resize Magnitude

Accepted M2 high-end resize deltas are 20 dbu (trial:i02.ug.Block5_union_row6.00), 36 dbu (trial:i01.ug.Block5_union_row3.00), and 72 dbu (trial:i01.ug.leaf_0001.02). In each case the resize accompanied an instance move on the same trial; no standalone resize without an instance move appears in the history. Always pair an M2 high-end resize with at least one instance move in the same operation set.

## Connectivity Safety

All eight trials preserved connectivity (`conn_preserved=true`). The combination of X-direction instance moves and M2 high-end resize does not break net connections in any measured case, provided the instance moves are co-applied with any necessary M2 polygon adjustments in the same atomic trial.

## Rule Mapping from Repair Shape

Because all moves are in X and all M2 resizes extend the high end along X, the violations being resolved correspond to rules that govern spacing and enclosure along the M2 length direction. V1.M2.EN.2 (minimum M2 enclosure on two opposite sides is 5 & 5 nm or 5 & 0 nm) and V1.S.1 (minimum spacing between V1 instances on the same or parallel M2 tracks) are the most geometrically consistent with X-direction corrections. V1.AUX.1 (V1 must be inside M1 and M2) and V1.M2.AUX.2 (V1 width must match M2 width perpendicular to M2 length) require that any instance move or M2 resize maintains complete overlap; the zero new-violation count across all trials confirms the accepted repair magnitudes satisfy these containment constraints.