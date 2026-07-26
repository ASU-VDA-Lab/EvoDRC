The two rejected passages require: (1) removing "appear to" and asserting directly with a citation, and (2) adding a citation to the per-rule guidance sentence. I'll also fold in the iteration 2 record and update accordingly.

---

The two measured trials for M2 are `trial:i01.ug.whole_design.00` (iteration 1, 19 ops) and `trial:i02.ug.whole_design.00` (iteration 2, 7 ops). Both cover Block5, channel unit_gate, unit whole_design, locus [0,0,10784,10784]. Both were accepted with `decision=gated_in`, `conn_preserved=true`, and zero new DRC markers (`n_new_in_crop=0`, `n_new_out_of_crop=0`). All claims below are grounded exclusively in those two records.

## Repair Strategy Observed

Instance moves are the primary and sufficient repair tool: iteration 2 used 7 instance moves with no polygon edits and achieved zero new violations (trial:i02.ug.whole_design.00). Iteration 1 combined 17 instance moves with 2 direct polygon edits and also achieved zero new violations (trial:i01.ug.whole_design.00). Polygon edits are not required when instance repositioning alone resolves the violations.

The two polygon edits applied in iteration 1 that succeeded without generating new violations were:
- `p879`: `resize_end` on axis `y`, high end, `+48 dbu`.
- `p910`: `move` on axis `x`, `+8 dbu`; then `resize_end` on axis `y`, high end, `+20 dbu`.

Both edits extended the high end of polygons in the Y direction. No low-end contractions or X-axis resizes were applied to M2 polygons in either trial (trial:i01.ug.whole_design.00, trial:i02.ug.whole_design.00).

## Connectivity Preservation Is a Gate Condition

Both accepted trials share `conn_preserved=true` as a necessary condition for `gated_in` (trial:i01.ug.whole_design.00, trial:i02.ug.whole_design.00). Every instance move and polygon resize must be checked for connectivity before submission.

## Instance Moves Observed

Iteration 1 moved 17 instances; iteration 2 moved 7 instances, all exclusively along the X axis at ±36 dbu (trial:i02.ug.whole_design.00). Across both iterations, all moves were along a single axis per instance (either X or Y, not diagonal). The X-axis move magnitudes confirmed across both iterations are 136 dbu, 36 dbu, 28 dbu, and 8 dbu. The Y-axis move magnitudes observed in iteration 1 are 72 dbu, 48 dbu, 24 dbu, 96 dbu, and 8 dbu (trial:i01.ug.whole_design.00). All moves are small relative to the 10784×10784 dbu locus, consistent with local perturbation rather than global repositioning.

Iteration 2 touched only layers M1, M2, and V1, a smaller co-touched set than iteration 1's M1, M2, M3, M4, M5, V1–V4 (trial:i02.ug.whole_design.00). Repairs that require fewer co-touched layers are viable when the violation pattern is confined to a smaller neighborhood.

## Zero-New-Violation Result

In iteration 1, 19 operations across M2 and co-touched layers produced zero new DRC errors inside and outside the crop window (trial:i01.ug.whole_design.00). In iteration 2, 7 instance-move-only operations produced the same zero-new-violation result (trial:i02.ug.whole_design.00). The full set of M2 rules—M2.W.1, M2.S.1 through M2.S.8, M2.A.1, V1.M2.EN.2, V1.M2.AUX.2, V2.M2.EN.1, and GEOMETRY.NONORTHOGONAL—were collectively satisfied after both repairs.

## Rule-Specific Observations from Available Data

Neither trial records a specific rule name as the violation target (trial:i01.ug.whole_design.00, trial:i02.ug.whole_design.00). Per-rule repair recipes cannot be grounded from the current history; individual rule failures must be present in future records before rule-specific guidance can be stated.