The MEMORY.md file doesn't exist yet; I'll proceed directly with the output.

---

## Dominant Repair Operations on M1

All 46 recorded trials carry `decision: gated_in` and `conn_preserved: true`, establishing that every operation sequence in this history was accepted by the gate. Repairs to M1 take two forms: **instance moves** (`move_instance`) and **polygon-boundary adjustments** (`resize_end` / polygon `move`). Both forms appear in the same trial and must be coordinated (trial:i01.ug.Block7_union_row9.21 combines eight instance moves with a `resize_end` on p3300 and a polygon move on p2720; trial:i01.ug.leaf_0024.25 combines two instance moves with four `resize_end` calls across two polygons).

## X-Axis Move Quantum

The most frequent single move delta on the X axis is 36 dbu, appearing across at least the following trials: trial:i01.ug.Block7_union_row11.01, trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row15.05, trial:i01.ug.Block7_union_row16.06, trial:i01.ug.Block7_union_row18.08, trial:i01.ug.Block7_union_row20.10, trial:i01.ug.Block7_union_row22.12, trial:i01.ug.Block7_union_row23.13, trial:i01.ug.Block7_union_row24.14, trial:i01.ug.leaf_0024.25, trial:i02.ug.Block7_union_row14.01, trial:i02.ug.Block7_union_row18.03, trial:i02.ug.Block7_union_row19.04, trial:i02.ug.Block7_union_row21.05, trial:i02.ug.Block7_union_row23.06, trial:i02.ug.Block7_union_row6.08, trial:i02.ug.leaf_0007.10, trial:i03.ug.Block7_union_row14.01, trial:i03.ug.Block7_union_row24.05. Use 36 dbu as the default X-axis step when selecting an instance move quantum; other quanta (4, 8, 28, 40, 44, 56, 64, 72, 108 dbu) appear but are less frequent (trial:i01.ug.Block7_union_row10.00 uses 4 dbu; trial:i01.ug.Block7_union_row7.19 uses 108 dbu; trial:i01.ug.Block7_union_row8.20 uses 64 dbu; trial:i01.ug.leaf_0002.23 uses 72 dbu).

When multiple instances are moved in the same trial they share the same delta (trial:i01.ug.Block7_union_row15.05 moves seven instances all by [36,0]; trial:i02.ug.Block7_union_row6.08 moves five instances all by [36,0]). Do not apply mixed X quanta to a group of instances unless the trial explicitly records differing deltas for members of that group (as in trial:i01.ug.Block7_union_row16.06, which uses -36 for i0407 and i0928 but +40 for i0320).

## X-Axis resize_end Deltas

`resize_end` on M1 polygon ends along X is not constrained to the 36-dbu instance grid. Observed deltas include 50 dbu (trial:i01.ug.Block7_union_row10.00, polygon p3305 axis x high), 56 dbu (trial:i01.ug.Block7_union_row12.02, polygon p3273 axis x high; trial:i01.ug.Block7_union_row9.21, polygon p2720 move), 49 dbu (trial:i01.ug.Block7_union_row3.15, polygon p3379 axis x high), 128 dbu (trial:i01.ug.leaf_0002.23, polygon p3695 axis x high), 164 dbu (trial:i01.ug.leaf_0008.24, polygon p3771 axis x high), 92 dbu (trial:i02.ug.Block7_union_row19.04, polygon p3523 axis x high), and 8 dbu (trial:i03.ug.Block7_union_row14.01, polygons p3200 and p3215 axis x high). Apply the resize delta that closes the measured enclosure shortfall rather than snapping to 36 dbu.

When an X-axis `resize_end` accompanies an instance move in the same trial, the resize is applied to the `high` end in all recorded cases where the instance moves in the positive X direction (trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row3.15, trial:i01.ug.leaf_0008.24, trial:i03.ug.Block7_union_row14.01). Apply `resize_end` to the leading edge (high end in the direction of motion) when extending M1 to recover V0.M1.EN.1 or V1.M1.EN.1 enclosure lost by an instance shift.

A single trial can resize a polygon's low end in the opposite direction from its accompanying instance moves: trial:i01.ug.Block7_union_row9.21 resizes p3300 axis x low by -36 dbu while moving instances in the positive X direction. Shrinking the trailing edge is therefore a valid companion action when spacing toward a neighbor on the low side would otherwise be violated.

## Y-Axis Instance Moves and Polygon Adjustments

Y-axis moves appear across both iteration 1 and iterations 2 and 3. Observed Y instance-move deltas include +64 and -12 (trial:i01.ug.Block7_union_row14.04), +44 (trial:i01.ug.leaf_0024.25; trial:i03.ug.leaf_0010.08), -52 (trial:i01.ug.Block7_union_row19.09; trial:i03.ug.Block7_union_row19.03), +57 (trial:i02.ug.Block7_union_row17.02), -64 (trial:i02.ug.leaf_0021.14), -44 (trial:i02.ug.leaf_0022.15; trial:i02.ug.leaf_0041.19), +52 (trial:i02.ug.leaf_0032.17), -48 (trial:i02.ug.leaf_0035.18), -88 (trial:i03.ug.Block7_union_row13.00), +48 (trial:i03.ug.leaf_0020.09), +72 (trial:i03.ug.Block7_union_row23.04).

Y-axis polygon moves track the accompanying instance moves: trial:i02.ug.Block7_union_row17.02 moves polygon p3631 by +57 on Y alongside instances i0794 and i0810 by the same delta; trial:i03.ug.Block7_union_row17.02 reverses this by moving p3631 by -57 and the same instances by -57. Move the M1 polygon by the same Y delta as the instances it contains so that via enclosure (V0.M1.EN.1, V1.M1.EN.1) is preserved after the shift.

Y `resize_end` operations occur on both `high` and `low` ends. trial:i01.ug.leaf_0024.25 resizes p3538 axis y high by +44; trial:i03.ug.Block7_union_row13.00 resizes p3538 axis y high by -44 (a reversal on the same polygon). trial:i03.ug.Block7_union_row17.02 resizes p2594 axis y low by +20. Do not assume the direction of a Y `resize_end` from a prior iteration: measure the current shortfall and apply the sign that closes it (trial:i03.ug.Block7_union_row13.00 demonstrates that the correct repair in iteration 3 directly reverses the iteration-1 expansion of the same polygon p3538).

## Iterative Direction Reversal on the Same Instance or Polygon

Several instances and polygons are operated on in multiple iterations with opposite-sign deltas.

- Instance i0347: moved +72X +44Y in trial:i01.ug.leaf_0024.25 (iter 1); moved +0X +44Y in trial:i02.ug.Block7_union_row13.00 (iter 2); moved +0X -88Y in trial:i03.ug.Block7_union_row13.00 (iter 3).
- Instance i0949: moved Y-52 in trial:i01.ug.Block7_union_row19.09 (iter 1); moved Y+52 in trial:i02.ug.leaf_0032.17 (iter 2); moved Y-52 in trial:i03.ug.Block7_union_row19.03 (iter 3).
- Instance i0950: same pattern as i0949 across trial:i01.ug.Block7_union_row19.09, trial:i02.ug.leaf_0032.17, trial:i03.ug.Block7_union_row19.03.
- Instance i0041: moved Y-44 in trial:i02.ug.leaf_0041.19 (iter 2); moved Y+72 in trial:i03.ug.Block7_union_row23.04 (iter 3).
- Instance i0235: moved Y-48 in trial:i02.ug.leaf_0035.18 (iter 2); moved Y+48 in trial:i03.ug.leaf_0020.09 (iter 3).
- Polygon p3538: Y-high extended +44 in trial:i01.ug.leaf_0024.25; Y-high retracted -44 in trial:i03.ug.Block7_union_row13.00.

Do not carry the sign of a prior-iteration move forward as the expected sign for the same instance or polygon in the current iteration. Recheck the current violation direction before assigning the delta sign.

## Multi-Layer Coupling

Trials that touch M1 frequently also touch V1 and M2; a subset additionally touch M3 and V2. The following trials record M1+M2+M3+V1+V2 as touched layers: trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row13.03, trial:i01.ug.Block7_union_row14.04, trial:i01.ug.Block7_union_row19.09, trial:i01.ug.Block7_union_row9.21, trial:i01.ug.leaf_0024.25, trial:i02.ug.Block7_union_row17.02, trial:i02.ug.leaf_0023.16, trial:i02.ug.leaf_0032.17, trial:i03.ug.Block7_union_row17.02, trial:i03.ug.Block7_union_row19.03. When an M1 repair moves an instance that also carries V1 or V2 geometry, apply the enclosure check for both V0.M1.EN.1 and V1.M1.EN.1 before committing the delta, since both rules become active simultaneously.

## n_new_in_crop and Acceptance

All 46 trials were accepted (`gated_in`). Trials with `n_new_in_crop > 0` were still accepted provided `conn_preserved: true`. The highest observed `n_new_in_crop` for an accepted trial is 9 (trial:i01.ug.Block7_union_row21.11, a single 4-dbu X instance move). Do not abort a repair solely because `n_new_in_crop` is nonzero; connectivity preservation (`conn_preserved: true`) is the binding constraint in all recorded cases.

## Enclosure Rules: Operation Patterns

V0.M1.EN.1 requires M1 to enclose V0 by at least 5 nm on two opposite sides (or 5 & 0 nm with the zero-enclosure side fully flush). V1.M1.EN.1 requires M1 to enclose V1 by at least 5 nm on one pair of opposite sides and at least 2 nm on the other pair. Resize operations extending the M1 `high` end in X by 36-164 dbu (trial:i01.ug.Block7_union_row24.14 at 36; trial:i01.ug.leaf_0002.23 at 128; trial:i01.ug.leaf_0008.24 at 164) establish that the enclosure shortfall can be large and that `resize_end` is the corrective tool when the M1 boundary rather than via position is the repair target. When the via is inside M1 but the enclosure margin is insufficient, extend the M1 boundary with `resize_end` rather than moving the via instance.

V0.M1.AUX.3 requires V0 width to exactly match M1 width along the perpendicular direction. Trials that resize M1 in X while simultaneously moving instances containing V0 (trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row14.04, trial:i01.ug.Block7_union_row9.21) show that both the M1 polygon and the cell containing V0 must be repositioned together to keep V0 flush with M1 edges on both sides. Apply instance moves and polygon resizes in the same trial when AUX.3 is active.

## Spacing Rules: Edge Length and Tip Classification

M1.S.1 applies only when both interacting edges are longer than 36 nm (18 nm minimum spacing). M1.S.2 applies when one edge is ≤ 36 nm and the other is > 36 nm (25 nm tip-to-side). M1.S.3 applies when both edges are in the 24-36 nm range (27 nm tip-to-tip). Because `resize_end` changes an edge length, a resize that extends a short (tip) edge past 36 nm can upgrade the applicable rule from M1.S.2 to M1.S.1, reducing the required spacing from 25 nm to 18 nm. Conversely, a resize that shrinks an edge below 24 nm can upgrade from M1.S.3 to M1.S.4/M1.S.5, increasing the required spacing from 27 nm to 31 nm. Verify the post-resize edge length against the thresholds 24 nm and 36 nm before accepting any `resize_end` delta (trials with resize_end in trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row14.04, trial:i01.ug.leaf_0002.23 all touch M1 and were accepted, confirming that resize-end operations can pass spacing checks when the resulting geometry satisfies the applicable rule).

M1.S.6 (corner-to-corner spacing 20 nm) is distinct from side-to-side and tip-to-side rules. Large X instance moves such as 108 dbu (trial:i01.ug.Block7_union_row9.21, instance i1117; trial:i01.ug.Block7_union_row7.19, instance i1446) move M1 well clear of corner proximity. Use moves of this magnitude when a corner-to-corner violation requires significant separation.

## M1.A.1 (Minimum Area 504 nm²) and M1.W.1 (Minimum Width 18 nm)

No trial records a `resize_end` that reduces M1 polygon size to a level triggering M1.A.1 or M1.W.1, and all trials were accepted. When applying a shrink-direction `resize_end` (e.g., trial:i01.ug.Block7_union_row9.21, axis x low, delta -36 on polygon p3300), verify that the resulting polygon area remains above 504 nm² and that no resulting edge-to-edge width falls below 18 nm before committing.

## M1.R.0 (Redundant Island)

M1.R.0 flags M1 polygons that contain exactly one small V0 via and lie near a large empty M1 region (≥ 500 nm wide, area > 2.5 µm², expanded by 400 nm). No trial records an operation explicitly targeting an M1.R.0 violation; however, trial:i01.ug.Block7_union_row21.11 introduces 9 new in-crop violations with a single 4-dbu X move (trial:i01.ug.Block7_union_row21.11, n_new_in_crop = 9), which is the largest violation increase in the history. Treat a large `n_new_in_crop` spike from a small positional delta as a signal that the move has brought an M1 island into proximity with a large empty region.

## NONORTHOGONAL Rule

The NONORTHOGONAL rule fires on any M1 edge whose angle is not exactly 0°, 90°, 180°, or 270°. All resize_end operations in the history adjust axis-aligned endpoints (axis x or axis y), and all instance moves use integer dbu deltas on a single axis or both axes simultaneously. No non-orthogonal edge is introduced by any recorded operation. Apply only axis-aligned `resize_end` and rectilinear `move_instance` deltas to M1 polygons to avoid triggering NONORTHOGONAL.