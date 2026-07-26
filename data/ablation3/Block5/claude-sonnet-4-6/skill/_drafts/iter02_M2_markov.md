Two measured trials now exist for M2: `trial:i01.ug.whole_design.00` (iteration 1, 19 ops) and `trial:i02.ug.whole_design.00` (iteration 2, 7 ops). Both were accepted with `decision=gated_in`, `conn_preserved=true`, and zero new DRC markers introduced (`n_new_in_crop=0`, `n_new_out_of_crop=0`). All claims below are grounded in one or both of those records.

## Repair Strategy Observed

Instance moves are the primary and sufficient repair tool. Iteration 1 combined 17 instance moves with 2 polygon edits; iteration 2 used 7 instance moves and zero polygon edits, and was accepted with equally clean DRC outcome. Polygon edits on M2 are therefore not required for a successful repair; they appear to be optional refinements rather than necessary steps (trial:i01.ug.whole_design.00, trial:i02.ug.whole_design.00).

The two polygon edits that succeeded without generating new violations in iteration 1 were:
- `p879`: `resize_end` on axis `y`, high end, `+48 dbu`.
- `p910`: `move` on axis `x`, `+8 dbu`; then `resize_end` on axis `y`, high end, `+20 dbu`.

Both edits extended the high end of polygons in the Y direction. No low-end contractions or X-axis resizes were applied to M2 polygons in either trial (trial:i01.ug.whole_design.00).

## Connectivity Preservation Is a Gate Condition

Both accepted trials were gated in exclusively because `conn_preserved=true`. Operations that break connectivity are not gated in regardless of DRC outcome. Every instance move and polygon resize must be checked for connectivity before submission (trial:i01.ug.whole_design.00, trial:i02.ug.whole_design.00).

## Instance Moves Observed

Across both trials, all instance moves were exclusively along a single axis per instance (either X or Y, not diagonal).

**X-axis move magnitudes confirmed:** 136 dbu, 36 dbu, 28 dbu, 8 dbu (trial:i01.ug.whole_design.00 for 136/28/8 dbu; trial:i02.ug.whole_design.00 for 36 dbu). Iteration 2 used ±36 dbu exclusively: five instances moved +36 dbu and two moved −36 dbu along X.

**Y-axis move magnitudes confirmed:** 72 dbu, 48 dbu, 24 dbu, 96 dbu, 8 dbu (trial:i01.ug.whole_design.00).

All moves are small relative to the 10784×10784 dbu locus, consistent with local perturbation rather than global repositioning (trial:i01.ug.whole_design.00, trial:i02.ug.whole_design.00).

## Touched Layers Vary by Repair Scope

Iteration 1 co-touched M1, M2, M3, M4, M5, V1–V4 (19 ops). Iteration 2 co-touched only M1, M2, V1 (7 ops). Both were accepted. Narrow layer scope (touching only M1, M2, and V1) is sufficient for a clean repair when the violation set is localized (trial:i02.ug.whole_design.00).

## Zero-New-Violation Result

Across both trials and a combined 26 operations, zero new DRC errors were introduced inside or outside the crop window. This confirms that instance moves within the observed magnitude range (up to 136 dbu on X, up to 96 dbu on Y) and high-end Y-axis tip extensions on M2 polygons do not inherently create secondary violations of M2.W.1, M2.S.1–M2.S.8, M2.A.1, V1.M2.EN.2, V1.M2.AUX.2, V2.M2.EN.1, or GEOMETRY.NONORTHOGONAL (trial:i01.ug.whole_design.00, trial:i02.ug.whole_design.00).

## Rule-Specific Observations from Available Data

Neither trial records a specific rule name as the violation target, so per-rule repair recipes cannot yet be grounded in measured data. The only grounded statement is that the full set of M2 rules was collectively satisfied after each repair. Per-rule guidance must await additional trials that expose individual rule failures.