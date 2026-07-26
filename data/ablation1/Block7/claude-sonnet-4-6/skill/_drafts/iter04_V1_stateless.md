## Repair Mechanism

V1 violations are repaired exclusively through indirect geometry changes: `move_instance` operations that relocate cell instances carrying V1 vias, and `resize_end` or `move` operations on enclosing M1 or M2 polygons. No trial in the history directly modifies V1 polygon geometry. All 45 recorded trials across iterations 1–4 resulted in `decision: gated_in` with `conn_preserved: true`, confirming that every accepted strategy preserved connectivity (trial:i01.ug.Block7_union_row10.00 through trial:i04.ug.leaf_0009.07).

## V1.S.1 — Same-Track and Parallel-Track Spacing

V1.S.1 spacing violations are resolved primarily by X-direction instance moves. The most frequently applied X displacements are ±28, ±36, ±40, ±72, and ±108 dbu. Moves of ±36 dbu appear in the majority of multi-instance spacing-fix trials, including trial:i01.ug.Block7_union_row15.05 (seven instances each moved +36 dbu), trial:i02.ug.Block7_union_row6.08 (five instances each +36 dbu), and trial:i01.ug.Block7_union_row23.13 (mixed ±36 and +72 dbu moves). Larger displacements appear when the spacing deficit is substantially larger: trial:i01.ug.Block7_union_row9.21 moves one instance +108 dbu and trial:i04.ug.leaf_0001.01 likewise applies a +108 dbu X move paired with M2 polygon resizing.

When a V1.S.1 violation involves instances on both sides of a via, moves in opposite X directions are applied simultaneously: trial:i02.ug.Block7_union_row18.03 moves i0942 by +36 dbu and i0428 by -36 dbu; trial:i01.ug.Block7_union_row16.06 moves i0407 and i0928 by -36 dbu while i0320 moves +40 dbu.

## V1.S.1 — Cross-Axis Corrections with Y Moves

For V1 instances on adjacent M2 tracks where a spacing violation has a Y-component, Y-direction instance moves are applied alongside or instead of X moves. trial:i01.ug.Block7_union_row19.09 moves instances i0949 and i0950 by [0,-52] dbu and moves i0771, i0026, i0294 by ±37 dbu in X. trial:i03.ug.Block7_union_row19.03 applies the same [0,-52] dbu Y move to i0949 and i0950, confirming the violation recurred. trial:i02.ug.leaf_0032.17 moves i0949 and i0950 by [0,+52] dbu, and trial:i04.ug.leaf_0008.06 repeats the [0,+52] dbu move on the same instances, indicating this via pair oscillates between two Y positions across iterations due to competing violations from both sides.

## V1.M2.EN.2 — M2 Enclosure Fixes

V1.M2.EN.2 violations (M2 must enclose V1 by 5 & 5 nm or 5 & 0 nm on opposite sides) are resolved by extending M2 polygon ends via `resize_end` on the x or y axis. Extensions to the high end of M2 polygons in the X direction are consistently applied:

- trial:i01.ug.Block7_union_row10.00: M2 polygon p3305 extended +50 dbu at the high-x end.
- trial:i01.ug.Block7_union_row3.15: M2 polygon p3379 extended +49 dbu at the high-x end.
- trial:i01.ug.leaf_0002.23: M2 polygon p3695 extended +128 dbu at the high-x end, paired with a +72 dbu instance move.
- trial:i01.ug.leaf_0008.24: M2 polygon p3771 extended +164 dbu at the high-x end, paired with +40 dbu and +108 dbu instance moves.
- trial:i04.ug.leaf_0001.01: M2 polygon p3696 extended +108 dbu at the high-x end while p3297 was trimmed -40 dbu at the low-x end, with simultaneous M3 and M1 resizing.

When M2 is extended to improve enclosure on one side, a paired instance move in the same direction accompanies the resize to keep the V1 via correctly positioned within the extended M2 region (trial:i01.ug.leaf_0002.23, trial:i01.ug.leaf_0008.24).

## V1.M1.EN.1 — M1 Enclosure Fixes

V1.M1.EN.1 requires M1 to enclose V1 by 5 nm on one pair of opposite sides and 2 nm on the other. M1 polygon `resize_end` operations appear alongside instance moves when M1 enclosure is deficient. trial:i01.ug.Block7_union_row12.02 resizes an M2/M1 polygon by +56 dbu at the high-x end while also adjusting Y positions of multiple instances. trial:i01.ug.Block7_union_row9.21 resizes M1 polygon p3300 by -36 dbu at the low-x end and applies a +56 dbu X move to M2 polygon p2720, simultaneously extending M2 coverage in the region vacated by the M1 trim.

## V1.M2.AUX.2 — Width Matching with M2

V1.M2.AUX.2 requires V1 width perpendicular to the M2 length direction to exactly match M2 width. When instance moves shift V1 in the Y direction, the associated M2 polygon must be moved or resized by the same Y delta to maintain this constraint. In trial:i01.ug.Block7_union_row12.02, Y-axis `resize_end` operations on polygon p3694 (+8 dbu high end, -8 dbu low end) bracket instance Y moves of +8 dbu, preserving the V1/M2 width match. In trial:i03.ug.Block7_union_row17.02, polygon p3631 is moved -57 dbu in Y synchronously with instance moves of [0,-57] dbu for i0794 and i0810, maintaining exact width alignment. In trial:i04.ug.leaf_0007.05, polygon p3631 is moved +68 dbu in Y with instances i0794 and i0810 each moved +68 dbu.

## V1.AUX.1 — V1 Must Remain Inside M1 and M2

All accepted trials report zero `n_new_out_of_crop`, confirming that no repair operation displaced a V1 instance outside its enclosing M1 or M2. When instance moves shift V1 by large amounts (e.g., +108 dbu in trial:i01.ug.Block7_union_row9.21, +108 dbu in trial:i04.ug.leaf_0001.01), M2 polygon resizing accompanies the move to maintain containment. The `resize_end` operations that extend M2 in the direction of instance movement directly enforce V1.AUX.1 compliance after large displacements.

## Multi-Iteration Recurrence

Several unit_ids required V1-related repair in three or more consecutive iterations, indicating that fixing one crop's violations reintroduces violations in adjacent crops:

- `Block7_union_row13` required repair in all four iterations: trial:i01.ug.Block7_union_row13.03, trial:i02.ug.Block7_union_row13.00, trial:i03.ug.Block7_union_row13.00, trial:i04.ug.Block7_union_row13.00.
- `Block7_union_row14` required repair across three iterations: trial:i01.ug.Block7_union_row14.04, trial:i02.ug.Block7_union_row14.01, trial:i03.ug.Block7_union_row14.01.
- `Block7_union_row23` required repair across three iterations: trial:i01.ug.Block7_union_row23.13, trial:i02.ug.Block7_union_row23.06, trial:i03.ug.Block7_union_row23.04.
- `leaf_0001` required repair in three iterations: trial:i01.ug.leaf_0001.22, trial:i02.ug.leaf_0001.09, trial:i04.ug.leaf_0001.01.

Instance i0920 received an identical -64 dbu Y move in both trial:i02.ug.leaf_0021.14 and trial:i04.ug.leaf_0005.03. Instance i1062 received an identical -44 dbu Y move in both trial:i02.ug.leaf_0022.15 and trial:i04.ug.leaf_0006.04. These repeated identical corrections on the same instances across non-consecutive iterations confirm that repairs in neighboring units displace these vias out of compliance and the same fix must reapply. Instance i0235 oscillated: -48 dbu Y in trial:i02.ug.leaf_0035.18, +48 dbu Y in trial:i03.ug.leaf_0020.09, and -44 dbu Y in trial:i04.ug.leaf_0009.07, reflecting competing violations from both sides of the via in alternating iterations.

## Multi-Layer Coupling

V1 repairs frequently co-occur with M3 and V2 modifications. When an instance carrying a V1 via is moved in Y to fix a V1 spacing or enclosure violation, the same instance carries V2 vias and M3 connections that require simultaneous adjustment. Trials that touch M3 and V2 alongside V1 include trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row13.03, trial:i01.ug.Block7_union_row14.04, trial:i02.ug.Block7_union_row17.02, trial:i03.ug.Block7_union_row17.02, trial:i04.ug.Block7_union_row13.00, trial:i04.ug.leaf_0007.05, and trial:i04.ug.leaf_0008.06. In all these cases the multi-layer ops are co-issued within the same trial, not as separate subsequent steps.

## New Violations Introduced by Accepted Repairs

Several accepted trials introduce new in-crop violations (`n_new_in_crop > 0`) while resolving the target violation. The largest count is 9 new violations in trial:i01.ug.Block7_union_row21.11, produced by a single +4 dbu X instance move. All were accepted because `conn_preserved: true`. This establishes that small X displacements in densely packed rows can simultaneously create multiple new V1.S.1 violations, and that the gating criterion for acceptance is connectivity preservation rather than zero new violations. Crops with high initial `n_new_in_crop` counts subsequently recur in later iterations for further repair.