## Dominant Repair Primitives

`move_instance` is the primary M2 repair operation across all three measured iterations. Every `gated_in` trial in the history uses at least one `move_instance`, and the majority of trials use only `move_instance` operations. Direct polygon edits (`resize_end`, `move` on polygon ids) appear as secondary adjustments paired with instance moves, never alone on this layer in the `unit_gate` channel (trial:i01.ug.Block7_union_row10.00, trial:i01.ug.Block7_union_row11.01, trial:i01.ug.leaf_0001.22, and all other `gated_in` records confirm this pattern).

When a `resize_end` does appear, apply it to the same polygon that connects to or terminates at the moved instance, on the axis aligned with the move direction. Do not extend polygons on axes orthogonal to the move unless a separate y-axis violation is being resolved concurrently (trial:i01.ug.Block7_union_row12.02 extended p3694 on both y ends; trial:i01.ug.Block7_union_row14.04 extended p3200 on x-high only while the y-moves were on separate instances).

## Move Magnitude Conventions

The 36 dbu step is the grid-aligned unit for horizontal instance displacement and is by far the most frequent delta in the history. It appears in trials i01.ug.Block7_union_row11.01, i01.ug.Block7_union_row12.02, i01.ug.Block7_union_row15.05, i01.ug.Block7_union_row16.06, i01.ug.Block7_union_row18.08, i01.ug.Block7_union_row20.10, i01.ug.Block7_union_row22.12, i01.ug.Block7_union_row23.13, i01.ug.Block7_union_row24.14, i01.ug.Block7_union_row5.17, i01.ug.Block7_union_row9.21, i02.ug.Block7_union_row6.08, i02.ug.Block7_union_row14.01, i02.ug.Block7_union_row18.03, i02.ug.Block7_union_row19.04, i02.ug.Block7_union_row21.05, i02.ug.Block7_union_row23.06, i02.ug.leaf_0007.10, i03.ug.Block7_union_row24.05, and others. Use 36 dbu as the default horizontal step when closing M2.S.1 (side-to-side 18 nm) or M2.S.2 (tip-to-side 25 nm) violations.

Larger horizontal steps (40, 44, 56, 64, 72, 104, 108 dbu) appear when a single 36 dbu step is insufficient to clear a spacing rule, or when multiple stacked violations require a compound offset. Trial i01.ug.Block7_union_row7.19 used a 108 dbu move for i1446 and a 40 dbu move for i1442 in the same repair, and trial i01.ug.Block7_union_row9.21 applied 108 dbu to i1117 alongside 56 dbu moves for two other instances.

Vertical (y-axis) instance moves are less frequent than horizontal and appear primarily in trials that also touch M3 or V2 layers: trial:i01.ug.Block7_union_row14.04 (y delta -12 and +64), trial:i01.ug.Block7_union_row12.02 (y delta +8), trial:i02.ug.Block7_union_row17.02 (y delta +57), trial:i03.ug.Block7_union_row17.02 (y delta -57). Vertical moves in M2 are therefore coupled to inter-layer constraint resolution, not purely to M2 spacing rules.

## resize_end Pairing with move_instance

When an instance is moved along x, resize the high end of the connecting M2 polygon if the move separates that polygon from the instance's via landing area. Failure to do so violates V1.M2.EN.2 (5 nm enclosure on opposite sides) or V1.M2.AUX.2 (V1 width matching M2 width perpendicularly). The pattern of move + resize_end on the same axis appears in trial:i01.ug.Block7_union_row3.15 (move i1623 by -36 x, then resize_end p3379 +49 on x-high), trial:i01.ug.Block7_union_row12.02 (move i1208 +36 x, then resize_end p3273 +56 on x-high), trial:i01.ug.leaf_0002.23 (move i1646 +72 x, then resize_end p3695 +128 on x-high), and trial:i01.ug.leaf_0008.24 (move i1968 +108 x, then resize_end p3771 +164 on x-high).

The resize delta on the polygon end is always equal to or greater than the instance move delta. It must be at minimum large enough to keep the V1 or V2 fully inside the extended M2 edge by 5 nm on both projected sides (V1.M2.EN.2, V2.M2.EN.1). When the move is 36 dbu, polygon resize deltas of 36, 49, 52, or 56 dbu appear across accepted trials, confirming the extension is not simply a copy of the move delta but depends on the initial enclosure margin.

## Via Enclosure Constraints on M2 Edits

V1.M2.EN.2 requires M2 to enclose V1 by at least 5 nm on two opposite sides (either both horizontal or one horizontal and one zero). V1.M2.AUX.2 requires V1 to be exactly as wide as M2 perpendicular to M2's length direction. V2.M2.EN.1 requires M2 to enclose V2 by at least 5 nm on two opposite sides.

These enclosure rules constrain the minimum amount any M2 polygon end can be recessed relative to the via it serves. When a `resize_end` sets `end: "low"` (shrinks the polygon), verify that the recessed end does not violate the 5 nm minimum enclosure. Trial:i01.ug.Block7_union_row9.21 applied a `resize_end` with delta_dbu -36 on the low end of p3300 and a separate polygon move of +56 on p2720, consistent with maintaining enclosure after the compound shift.

Trials touching only M2 and V1 (without M3 or V2) are the most common category; trials adding M3 and V2 always involve more ops and span wider locus windows (trial:i01.ug.Block7_union_row9.21 locus 3184–18288 x, trial:i01.ug.leaf_0024.25 locus 14112–15696 x crossing multiple row heights).

## M2.S.7 Interaction: Tip-to-Tip with Narrow Side Spacing

M2.S.7 forbids an 18 nm tip-to-tip gap when the co-located side-to-side spacing is ≤32 nm, and requires parallel run length ≥35 nm whenever side spacing is ≤32 nm. This rule fires on vertical M2 edges (90°) that are 18 nm apart while horizontal edges (0°) of the same polygons are also close. The repair for M2.S.7 is horizontal separation of the instances that generate the conflicting vertical-edge pair. The 36 dbu step is sufficient to open the tip-to-tip from 18 nm to ≥19 nm, but the side spacing constraint requires the full parallel run to extend ≥35 nm if side spacing remains ≤32 nm. A combined move + x-high resize_end pattern (as in trial:i01.ug.Block7_union_row12.02 and trial:i01.ug.leaf_0002.23) addresses both: the move shifts the tip gap, and the polygon extension increases the parallel run length.

## Oscillatory Instance Behavior Across Iterations

Several instances revisit the same locus across iterations with opposing y-direction moves, indicating their optimal vertical position has not converged:

- Instances i0949 and i0950: moved [0,-52] in trial:i01.ug.Block7_union_row19.09, then [0,+52] in trial:i02.ug.leaf_0032.17 (net zero), then [0,-52] again in trial:i03.ug.Block7_union_row19.03.
- Instances i0794 and i0810: moved [0,+57] in trial:i02.ug.Block7_union_row17.02, then [0,-57] in trial:i03.ug.Block7_union_row17.02 (net zero across two iterations).
- Instance i0041: moved [-36,+44] in trial:i01.ug.Block7_union_row23.13, then [0,-44] in trial:i02.ug.leaf_0041.19, then [0,+72] in trial:i03.ug.Block7_union_row23.04 (net y = +72 over three iterations, oscillating path).
- Instance i0920: moved [0,-12] in trial:i01.ug.Block7_union_row14.04, then [0,-64] in trial:i02.ug.leaf_0021.14, then [0,+64] in trial:i03.ug.Block7_union_row14.01.

When an instance appears in locus records across multiple iterations with opposing deltas on the same axis, the underlying M2 DRC root cause is not yet resolved. Prefer a larger displacement that definitively clears the minimum rule margin (e.g., at least 2x the rule limit beyond the current violation gap) rather than incremental steps that allow re-violation in subsequent iterations.

## cu_pool Channel: Via Shape Resize Rejection

The only `rejected_net_positive` record in the history is trial:i02.cu.def:VIA_VIA23_1_3_36_36.00, from the `cu_pool` channel. It attempted a `resize_via_shape` on the M3 layer of cell VIA_VIA23_1_3_36_36 with delta_dbu -40 in y. The per-window DRC counts were unchanged (delta=0 in all five windows), producing a delta_total of 0, which triggered rejection. This trial touched M2 and V2 as secondary layers.

Do not apply `resize_via_shape` operations that produce a net-zero DRC delta. A y-shrink of the via-shape that does not change any M2 spacing or enclosure count fails both from the M2 side (no spacing margin is opened) and from the M3/V2 side (enclosure can worsen). The `cu_pool` channel evaluates net DRC across the full design window, not just the local locus.

## Connectivity Preservation as a Gate Condition

Every `gated_in` trial has `conn_preserved: true`. Trials that would break connectivity are not accepted regardless of DRC improvement. When composing multi-instance moves, verify that every V1 and V2 center remains within the M2 polygon that serves it after the move, satisfying V1.M2.EN.2 and V2.M2.EN.1. The resize_end steps accompanying instance moves in trials such as trial:i01.ug.Block7_union_row3.15 and trial:i01.ug.leaf_0008.24 exist specifically to prevent the polygon end from receding past the via, which would break the connection.

## n_new_in_crop Does Not Block Acceptance

Several `gated_in` trials accept operations that introduce new in-crop violations (n_new_in_crop > 0): trial:i01.ug.Block7_union_row13.03 (1 new), trial:i01.ug.Block7_union_row19.09 (1 new), trial:i01.ug.Block7_union_row21.11 (9 new), trial:i01.ug.Block7_union_row22.12 (2 new), trial:i01.ug.Block7_union_row24.14 (2 new), trial:i01.ug.Block7_union_row4.16 (1 new), trial:i01.ug.Block7_union_row5.17 (1 new), trial:i02.ug.Block7_union_row21.05 (2 new), trial:i02.ug.leaf_0032.17 (4 new), trial:i02.ug.leaf_0041.19 (5 new), trial:i03.ug.Block7_union_row19.03 (1 new), trial:i03.ug.leaf_0010.08 (4 new), trial:i03.ug.leaf_0020.09 (5 new). All have n_new_out_of_crop = 0. The gate condition is conn_preserved=true and no out-of-crop new violations, not zero new in-crop violations. New in-crop violations are expected as the optimizer trades local DRC state across loci.

## Multi-Layer Repair Complexity

Trials touching M1, M2, M3, V1, and V2 together require more operations (7–9 ops) and wider locus windows than trials limited to M1, M2, V1 (1–5 ops, narrower loci). When the repair locus for a unit overlaps both V1 and V2 enclosure zones on M2, expect that the polygon moves must simultaneously satisfy V1.M2.EN.2 (5 nm lateral enclosure for V1) and V2.M2.EN.1 (5 nm enclosure for V2). Trials i01.ug.Block7_union_row9.21, i01.ug.Block7_union_row12.02, and i03.ug.Block7_union_row17.02 demonstrate this multi-via coordination pattern, each requiring concurrent move and polygon-resize steps on both x and y axes.