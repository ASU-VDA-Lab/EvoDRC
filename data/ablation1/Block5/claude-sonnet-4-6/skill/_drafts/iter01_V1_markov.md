## Repair Patterns Observed (Iteration 1)

All six iteration-1 trials on layer V1 were accepted by the unit_gate channel with zero new violations introduced (n_new_in_crop=0, n_new_out_of_crop=0) and full connectivity preservation. Every accepted repair operated exclusively along the x-axis via `move_instance` and/or `resize_end` (x, high end) operations touching M1, M2, and V1 simultaneously (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.Block5_union_row6.01, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05).

## Instance Move Deltas

Accepted x-axis instance move deltas include +36 dbu (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05), -36 dbu (trial:i01.ug.leaf_0002.03), and +4 dbu (trial:i01.ug.Block5_union_row6.01). A single-instance move of +36 dbu with no accompanying resize is sufficient to resolve a violation without creating new ones (trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05).

## Co-Move and Resize Combinations

When a resize_end on the x high end accompanies a move_instance, the resize delta may differ from the move delta: trial:i01.ug.leaf_0001.02 used move +36 dbu with resize +72 dbu on polygon p974 and was accepted clean. trial:i01.ug.Block5_union_row3.00 used move +36 dbu paired with resize +36 dbu on polygon p967 and two separate instance moves, also accepted clean.

Moving two instances in opposite directions (trial:i01.ug.leaf_0002.03: i0056 at +36 dbu, i0103 at -36 dbu) preserves V1 connectivity and introduces no new violations, indicating that symmetric diverging moves are a valid pattern for spacing repair between adjacent units.

Moving two instances in the same direction with equal small deltas (trial:i01.ug.Block5_union_row6.01: i0025 and i0019 both +4 dbu) also preserves V1 compliance, confirming that co-directional translation of a pair maintains relative V1 geometry.

## Multi-Instance Repair Scope

Repairs touching up to three instances in a single trial (trial:i01.ug.Block5_union_row3.00: i0117, i0131 moved, p967 resized) were accepted without new V1 violations, showing that coordinated multi-instance x-shifts do not inherently stress V1 spacing or enclosure rules when the moved group is internally consistent.

## Layer Interaction

All accepted repairs touched M1, M2, and V1 together. No trial in this iteration touched V1 in isolation. This is consistent with V1.AUX.1 (V1 must be inside M1 and M2) and V1.M2.AUX.2 (V1 width must match M2 width perpendicular to M2 length): repairs that shift M2 and its enclosing M1 together keep V1 correctly enclosed on both layers.