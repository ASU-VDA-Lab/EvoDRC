**Repair primitive landscape**

The dominant repair primitive for M2 violations across all five iterations is `move_instance` by 36 dbu in the X direction. This step recurs in accepted `gated_in` trials throughout the entire history: trial:i01.ug.Block7_union_row10.00, trial:i01.ug.Block7_union_row11.01, trial:i01.ug.Block7_union_row15.05, trial:i01.ug.Block7_union_row16.06, trial:i01.ug.Block7_union_row18.08, trial:i01.ug.Block7_union_row20.10, trial:i01.ug.Block7_union_row22.12, trial:i01.ug.Block7_union_row23.13, trial:i01.ug.Block7_union_row24.14, trial:i02.ug.Block7_union_row13.00, trial:i02.ug.Block7_union_row14.01, trial:i02.ug.Block7_union_row6.08, trial:i05.ug.leaf_0003.03. The 36 dbu step is twice the M2.S.1 minimum side-to-side spacing of 18 nm (18 dbu) and twice the M2.W.1 minimum width of 18 nm; these are the tightest lateral spacing rules on M2, and 36 dbu provides a full double-pitch correction.

Non-36 X-moves appear when the locus is congested: trial:i01.ug.Block7_union_row7.19 used 108 and 40 dbu moves; trial:i01.ug.Block7_union_row8.20 used 64 dbu for two instances; trial:i02.ug.leaf_0001.09 used 104 dbu. These larger steps occur in narrow loci where the standard 36 dbu is insufficient to clear the spacing gap.

**resize_end operations on M2 polygons**

`resize_end` on M2 polygon high-ends in X extends a wire after an adjacent instance is moved, restoring V1 enclosure or M2 spacing that the instance move would otherwise disturb. Examples: trial:i01.ug.Block7_union_row3.15 resized p3379 high-end by +49 dbu after moving i1623 by -36 dbu X; trial:i01.ug.Block7_union_row12.02 resized p3273 high-end by +56 dbu after moving i1208 by +36 dbu X; trial:i01.ug.leaf_0002.23 resized p3695 high-end by +128 dbu after moving i1646 by +72 dbu X; trial:i02.ug.Block7_union_row19.04 resized p3523 high-end by +92 dbu after two +36 dbu X instance moves. The resize magnitude is not always equal to the instance move delta because the wire must reach a specific absolute endpoint to satisfy the enclosure requirement under V1.M2.EN.2 (minimum 5 nm enclosure on two opposite sides) or V2.M2.EN.1 (minimum 5 nm enclosure on at least two opposite sides).

`resize_end` on the low-end in X also occurs: trial:i01.ug.Block7_union_row9.21 shrunk p3300 low-end by -36 dbu. Y-axis resize_end operations appear when M2 or M3 stubs require vertical extension after instance repositioning: trial:i01.ug.Block7_union_row14.04 resized p3576 high-end in Y by +64 dbu; trial:i03.ug.Block7_union_row14.01 resized p3515 high-end in Y by +8 dbu and p3200 high-end by +8 dbu.

**V1 and V2 enclosure interactions**

All trials accepted in the `unit_gate` channel that touch M2 also co-touch M1 and V1 in the majority of records; a subset additionally modify M3 and V2. This multi-layer co-movement is required by V1.M2.EN.2 and V1.M2.AUX.2: when an M2 instance is repositioned, the V1 via and underlying M1 metal must move with it to preserve both enclosure (>= 5 nm on two opposite sides) and the width-match constraint. Trials that touch only M2, M3, and V2 — with no M1 or V1 involved — correspond to M2-to-M3 via stack adjustments subject to V2.M2.EN.1: trial:i02.ug.leaf_0010.13, trial:i03.ug.leaf_0002.07, trial:i04.ug.leaf_0002.02, trial:i05.ug.leaf_0001.01.

**Rejected via-cell shape resize**

Trial:i02.cu.def:VIA_VIA23_1_3_36_36.00 resized the M3 shape in via cell VIA_VIA23_1_3_36_36 by -40 dbu in Y. This was rejected as `rejected_net_positive` with delta_total=0. All five sampled DRC windows were unchanged: leaf_0032 (11→11), leaf_0038 (13→13), leaf_0041 (14→14), leaf_0045 (426→426), leaf_0046 (395→395). Do not apply global via-cell shape resizes through the `cu_pool` channel as a primary M2 repair strategy; this operation produced no reduction in violation count across any window in this design.

**Persistent violations requiring multi-iteration repair**

Several units required fresh repair operations in three or more consecutive iterations:

Block7_union_row13 was modified in iter1 (trial:i01.ug.Block7_union_row13.03), iter2 (trial:i02.ug.Block7_union_row13.00), iter3 (trial:i03.ug.Block7_union_row13.00), and iter4 (trial:i04.ug.Block7_union_row13.00). Each iteration applied a different combination of ops and a different set of instance IDs, confirming the locus contains interacting violations that a single-pass repair does not eliminate.

Block7_union_row14 was modified in iter1 (trial:i01.ug.Block7_union_row14.04, 8 ops), iter2 (trial:i02.ug.Block7_union_row14.01, 5 ops), and iter3 (trial:i03.ug.Block7_union_row14.01, 6 ops). The op count did not decrease monotonically, ruling out a simple residual-cleanup pattern; new violations within the locus were introduced at each pass.

Block7_union_row17 was repaired in iter2 with a Y+57 dbu move of polygon p3631 and instances i0794 and i0810 (trial:i02.ug.Block7_union_row17.02), then in iter3 the same polygon was moved Y-57 dbu and those instances returned to their previous positions, while five additional instances were moved +36 dbu X (trial:i03.ug.Block7_union_row17.02). The Y displacement was fully reversed, and the accepted repair was the addition of X-axis spreading. Apply X-axis instance moves to Block7_union_row17 before attempting Y displacement; the Y displacement alone was not net positive.

Block7_union_row19 was modified in iter1 (trial:i01.ug.Block7_union_row19.09), iter2 (trial:i02.ug.Block7_union_row19.04), and iter3 (trial:i03.ug.Block7_union_row19.03). Block7_union_row23 was modified in iter1 (trial:i01.ug.Block7_union_row23.13), iter2 (trial:i02.ug.Block7_union_row23.06), and iter3 (trial:i03.ug.Block7_union_row23.04).

**Oscillating instance positions**

Instance pair i0949/i0950 moved [0,-52] in iter1 (trial:i01.ug.Block7_union_row19.09), then [0,+52] in iter2 (trial:i02.ug.leaf_0032.17), then [0,-52] again in iter3 (trial:i03.ug.Block7_union_row19.03), then [0,+52] again in iter4 (trial:i04.ug.leaf_0008.06). This pair oscillates Y by exactly 52 dbu with a period of two iterations and shows no net convergence through four iterations. Do not apply a Y-axis move of 52 dbu to i0949/i0950 without simultaneously addressing the neighbor unit that generates the counter-violation; the unit_gate channel accepts each individual pass because conn_preserved=true, but the pair oscillation persists.

Instance i0920 moved [0,-12] in iter1 (trial:i01.ug.Block7_union_row14.04), [0,-64] in iter2 (trial:i02.ug.leaf_0021.14), [0,+64] in iter3 (trial:i03.ug.Block7_union_row14.01), and [0,+64] in iter5 (trial:i05.ug.leaf_0004.04). The net Y displacement from iter1 to iter5 is +52 dbu, but the path through iter2-3 included a full +64/-64 reversal.

Instance i1062 moved [0,-44] in iter2 (trial:i02.ug.leaf_0022.15), [4,+44] in iter3 (trial:i03.ug.leaf_0010.08), and [0,-44] in iter4 (trial:i04.ug.leaf_0006.04). Instance i0235 moved [0,-48] in iter2 (trial:i02.ug.leaf_0035.18), [0,+48] in iter3 (trial:i03.ug.leaf_0020.09), and [0,-44] in iter4 (trial:i04.ug.leaf_0009.07).

When an instance is at a Y position already visited in a prior iteration, do not apply a Y-axis move of the same magnitude and direction used in the earlier iteration; the gate will accept it but the next iteration will reverse it.

**Instance i1358 trajectory (M2/M3/V2 via structure)**

Instance i1358 appears exclusively in trials touching M2, M3, and V2 with no M1 or V1 involvement, classifying it as part of an M2-to-M3 via stack. Its five-iteration sequence: Y+8 (trial:i01.ug.Block7_union_row12.02), Y-36 (trial:i02.ug.leaf_0010.13), Y+36 (trial:i03.ug.leaf_0002.07), X-36 (trial:i04.ug.leaf_0002.02), X+36 (trial:i05.ug.leaf_0001.01). The first three moves are Y-axis adjustments that cancel to a net +8 dbu; iterations 4-5 switched to X-axis moves that also cancel. As of iter5 the net displacement from the iter1 baseline is Y+8, X+0. The axis switch in iter4 broke the Y oscillation. For M2/M3/V2-only via stacks that exhibit Y oscillation, switching to an X-axis adjust is the path that advances the repair beyond the oscillation.

**n_new_in_crop and acceptance criterion**

The `gated_in` decision is driven by `conn_preserved=true`, not by the absence of new in-crop violations. Trial:i01.ug.Block7_union_row21.11 introduced 9 new in-crop violations and was accepted; trial:i01.ug.Block7_union_row19.09, trial:i01.ug.Block7_union_row4.16, trial:i01.ug.Block7_union_row5.17, trial:i01.ug.leaf_0002.23, and trial:i01.ug.leaf_0024.25 each introduced 1-2 new violations and were accepted; trial:i02.ug.leaf_0032.17 introduced 4 and was accepted; trial:i03.ug.leaf_0010.08 introduced 4 and was accepted. Every gated_in trial in the full history has n_new_out_of_crop=0. The engine does not reject on-crop violation growth as long as connectivity is preserved; residual new violations are addressed in subsequent iterations.

**Multi-op repairs**

The largest single-iteration repairs involve 8-9 ops: trial:i01.ug.Block7_union_row14.04 (8 ops, M1/M2/M3/V1/V2), trial:i01.ug.Block7_union_row9.21 (9 ops, M1/M2/M3/V1/V2), trial:i03.ug.Block7_union_row17.02 (9 ops, M1/M2/M3/V1/V2). These all involve simultaneous instance moves and polygon resize operations, and all three were accepted with n_new_in_crop=0. Multi-layer multi-op repairs on M2 are accepted by the gate and produce zero new violations when the instance moves and wire extensions are jointly planned within a single trial.

**M2.S.7 side-to-side coupling**

M2.S.7 forbids a tip-to-tip gap of 18 nm when a co-located side-to-side spacing is <= 32 nm, and requires parallel run length >= 35 nm when side spacing is <= 32 nm. The standard +36 dbu X-axis instance move applied throughout this dataset directly widens side-to-side spacing and removes the co-location condition that triggers M2.S.7. This mechanism is active in every trial that applies the 36 dbu X move to wires that were previously within 32 nm side-to-side, including trial:i01.ug.Block7_union_row15.05, trial:i01.ug.Block7_union_row16.06, trial:i01.ug.Block7_union_row18.08, trial:i02.ug.Block7_union_row6.08.

**M2.S.8 diagonal gap center rule**

M2.S.8 requires euclidean center-to-center distance >= 80 nm between tip-to-tip gaps on different M2 tracks, measured after shrinking each 18 nm gap by 8.5 nm per side. Trial:i02.ug.Block7_union_row17.02 applied a 57 dbu Y move to shift an entire M2 row; trial:i03.ug.Block7_union_row17.02 reversed that Y move and instead added +36 dbu X moves to five instances. The Y-only displacement was insufficient and was reversed; the repair that cleared the violations used X-axis spreading. When tip-to-tip gap centers on adjacent M2 tracks violate M2.S.8, use X-axis moves to separate the gap positions along the track direction rather than Y-axis moves that shift rows as a unit.

**General repair ordering**

The complete history establishes the following ordering of repair strategies for M2:

1. X-axis `move_instance` by 36 dbu (or larger multiple when locus is congested): applied and accepted first across all iterations (trial:i01.ug.Block7_union_row10.00 through trial:i05.ug.leaf_0003.03).

2. Accompanying `resize_end` on M2 polygon high-end in X to restore V1.M2.EN.2 enclosure after an instance move: applied jointly with step 1 (trial:i01.ug.Block7_union_row3.15, trial:i01.ug.Block7_union_row12.02, trial:i02.ug.Block7_union_row19.04).

3. Y-axis `move_instance` when X movement is constrained: applied when the locus spans a full row or when X-spacing is already clear (trial:i01.ug.Block7_union_row14.04, trial:i02.ug.leaf_0021.14). Avoid repeating a Y move that was reversed in the prior iteration.

4. Y-axis `resize_end` to adjust M2 tip positions and satisfy M2.S.2, M2.S.3, M2.S.4, M2.S.5 tip spacing rules: trial:i03.ug.Block7_union_row14.01.

5. `cu_pool` via-cell shape resize: not effective for M2 in this design (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00, rejected).