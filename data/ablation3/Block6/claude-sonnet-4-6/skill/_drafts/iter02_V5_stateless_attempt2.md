## Repair History Summary

Two trials touching layer V5 exist in Block6 iteration history. Trial `i01.cu.def:VIA_VIA56_2_2_66_58.01` is the only record with direct V5 shape operations; trial `i02.ug.whole_design.00` touched V5 as a side effect of large-scale instance moves and metal polygon adjustments.

## Via Shape Resize on Y-Axis

The sole confirmed repair targeting V5 shapes directly resized all four via shapes in cell `VIA_VIA56_2_2_66_58` on the y-axis by +248 dbu each, using four `resize_via_shape` operations (trial:`i01.cu.def:VIA_VIA56_2_2_66_58.01`). The decision field is `applied` and `conn_preserved` is `true`, confirming the change was committed without breaking connectivity (trial:`i01.cu.def:VIA_VIA56_2_2_66_58.01`). The whole-design violation count dropped from 247 to 215, a reduction of 32 (trial:`i01.cu.def:VIA_VIA56_2_2_66_58.01`). The touched layers for this repair are M5, M6, and V5, consistent with enclosure rules V5.M5.EN.1 and V5.M6.EN.2 being the likely violation source resolved by increasing y-extent of the via shapes (trial:`i01.cu.def:VIA_VIA56_2_2_66_58.01`).

Resizing V5 via shapes symmetrically on the y-axis while keeping `conn_preserved=true` produced a net reduction of 32 violations at the whole-design scope (trial:`i01.cu.def:VIA_VIA56_2_2_66_58.01`). Do not resize V5 shapes in a way that breaks connectivity; the only committed V5 resize in this history maintained `conn_preserved=true` (trial:`i01.cu.def:VIA_VIA56_2_2_66_58.01`).

## Instance Moves Touching V5

Trial `i02.ug.whole_design.00` was decided `gated_in` with `conn_preserved=true` and introduced zero new in-crop or out-of-crop violations for V5 (trial:`i02.ug.whole_design.00`). The per-rule delta table lists only `V2.M3.EN.2` as gaining 10 new in-crop violations; no V5 rule appears in the new-violation list (trial:`i02.ug.whole_design.00`). The assemble_drops for trial `i02.ug.whole_design.00` contain exclusively V2-layer operations, confirming no V5 ops were dropped at assembly (trial:`i02.ug.whole_design.00`). Instance moves that touch V5 among many other layers can be accepted under `unit_gate` channel when connectivity is preserved and no new V5 violations are introduced (trial:`i02.ug.whole_design.00`).

## Rule-Specific Observations

**V5.W.1 (minimum width 24 nm):** No violation of V5.W.1 appears in either trial's delta tables. The y-axis resize of +248 dbu per side increases via height, moving away from a minimum-width violation in that axis (trial:`i01.cu.def:VIA_VIA56_2_2_66_58.01`).

**V5.M5.EN.1 and V5.M6.EN.2 (11 nm enclosure on two opposite sides):** The repair in trial `i01.cu.def:VIA_VIA56_2_2_66_58.01` modified V5 shapes on the y-axis and touched both M5 and M6, consistent with enclosure deficiencies along the y-direction. Increasing via shape extent along y resolves enclosure shortfalls on the axis perpendicular to the direction already satisfying the two-opposite-sides requirement (trial:`i01.cu.def:VIA_VIA56_2_2_66_58.01`).

**V5.M6.AUX.2 (V5 width must match M6 width perpendicular to M6 length):** No violation of V5.M6.AUX.2 is recorded as new or resolved in either trial. The y-axis resize in trial `i01.cu.def:VIA_VIA56_2_2_66_58.01` did not produce any V5.M6.AUX.2 regressions, and the repair was applied cleanly (trial:`i01.cu.def:VIA_VIA56_2_2_66_58.01`).

**V5.AUX.1 (V5 must be inside M5 and M6):** Neither trial records a V5.AUX.1 violation. The `resize_via_shape` repair touched M5, M6, and V5 together, keeping the via inside both metal layers (trial:`i01.cu.def:VIA_VIA56_2_2_66_58.01`).

**V5.S.1, V5.S.2, V5.S.3 (spacing 33 nm):** No spacing violations for V5 appear in either trial's delta records (trial:`i01.cu.def:VIA_VIA56_2_2_66_58.01`, trial:`i02.ug.whole_design.00`).

**NONORTHOGONAL:** No nonorthogonal violations are recorded for V5 in either trial (trial:`i01.cu.def:VIA_VIA56_2_2_66_58.01`, trial:`i02.ug.whole_design.00`).

## Operation Patterns

The only V5 operation type with a committed, applied outcome in this history is `resize_via_shape` on the y-axis (trial:`i01.cu.def:VIA_VIA56_2_2_66_58.01`). All four shapes in the target cell received the same delta (+248 dbu), indicating uniform per-cell resize applied to every shape index rather than selective adjustment (trial:`i01.cu.def:VIA_VIA56_2_2_66_58.01`). The `cu_pool` channel was used for the direct via repair; the `unit_gate` channel was used for the broader instance-move sweep that incidentally touched V5 (trial:`i01.cu.def:VIA_VIA56_2_2_66_58.01`, trial:`i02.ug.whole_design.00`).