## Operation Granularity

X-axis instance moves across all accepted trials use multiples of 36 dbu. Values of 36, 72, and 108 dbu appear in trial:i01.ug.Block3_union_row1.00, trial:i01.ug.Block3_union_row2.01, trial:i01.ug.leaf_0006.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0008.06, trial:i01.ug.leaf_0009.07, and trial:i01.ug.leaf_0012.08; a negative move of -36 dbu also follows this granularity (trial:i01.ug.leaf_0013.09). Y-axis instance moves use 96 dbu increments (trial:i03.ug.leaf_0003.02, deltas [0,-96] for i0085 and i0088).

One x-axis displacement of 73 dbu (not a multiple of 36) appears for instance i0239 in trial:i03.ug.leaf_0001.00; that trial was accepted with conn_preserved=true and 0 new violations in crop.

## Resize-End Pairing with Instance Moves

Apply a resize_end operation (axis=x, end=high) to the M2 polygon associated with a moved V1-carrying instance whenever that polygon must be extended in the +x direction to maintain V1.M2.AUX.2 compliance and V1.M2.EN.2 enclosure. Trial:i01.ug.leaf_0008.06 paired two instance moves of +36 dbu (i0239 and i0047) with resize_end delta=36 on polygon p1261. Trial:i02.ug.leaf_0001.00 paired a +72 dbu move of i0047 with resize_end delta=72 on p1261. Trial:i03.ug.leaf_0001.00 paired a +73 dbu move of i0239 with resize_end delta=130 on polygon p1226; the resize delta exceeded the instance displacement by 57 dbu to satisfy the 5 nm end-enclosure that V1.M2.EN.2 requires beyond the new V1 edge position.

Do not apply resize_end to M2 polygons when instance moves alone keep all V1 enclosure and spacing rules satisfied. Trials without any resize_end operation — trial:i01.ug.Block3_union_row1.00, trial:i01.ug.Block3_union_row2.01, trial:i01.ug.Block3_union_row5.02, trial:i01.ug.Block3_union_row8.03, trial:i01.ug.leaf_0006.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0009.07, trial:i01.ug.leaf_0012.08, trial:i01.ug.leaf_0013.09 — all achieved 0 new violations in crop and were accepted.

## V1.AUX.1: Containment Inside M1 and M2

V1.AUX.1 flags any V1 shape not fully inside M1 ∩ M2. Every gated-in trial reports conn_preserved=true with 0 new out-of-crop violations, confirming that no accepted move ejected a V1 shape from M1 or M2 (trial:i01.ug.Block3_union_row1.00 through trial:i03.ug.leaf_0003.02). In the three trials that also applied resize_end (trial:i01.ug.leaf_0008.06, trial:i02.ug.leaf_0001.00, trial:i03.ug.leaf_0001.00), extending the M2 polygon's high-x end was the mechanism that preserved this containment after the instance displacement.

## V1.M2.AUX.2: V1 Width Must Match M2 Width

V1.M2.AUX.2 requires V1 to be exactly the same width as M2 in the direction perpendicular to M2 length. Moves in the x-direction (along the M2 run) do not alter the perpendicular-width relationship and were accepted without any resize operation in the majority of trials (trial:i01.ug.Block3_union_row1.00, trial:i01.ug.leaf_0006.04, trial:i01.ug.leaf_0009.07, and others). Apply resize_end only to the longitudinal end of M2 (axis=x, end=high), not to its transverse edges, so that V1.M2.AUX.2 compliance is preserved; all three resize_end operations in the history (trial:i01.ug.leaf_0008.06, trial:i02.ug.leaf_0001.00, trial:i03.ug.leaf_0001.00) use axis=x, end=high exclusively.

## V1.M2.EN.2: M2 Enclosure of V1

V1.M2.EN.2 requires M2 to enclose V1 by at least 5 nm on two opposite sides (5&5 nm or 5&0 nm depending on end-cap geometry). When resize_end delta exceeds the corresponding instance move delta, the surplus accounts for this end-enclosure. In trial:i03.ug.leaf_0001.00, instance i0239 moved +73 dbu in x while polygon p1226 was extended +130 dbu; the 57 dbu difference maintains the 5 nm M2 enclosure margin beyond the new V1 edge. In trial:i02.ug.leaf_0001.00 and trial:i01.ug.leaf_0008.06, instance move and resize deltas were equal (72 and 36 dbu respectively), indicating the existing M2 end already provided sufficient enclosure margin on the far side at those displacement sizes.

## V1.M1.EN.1: M1 Enclosure of V1

V1.M1.EN.1 requires M1 to enclose V1 by 5 nm and 2 nm on two opposite sides. Move V1-carrying instances only to positions where M1 continues to provide these enclosure margins; every accepted trial in the history (trial:i01.ug.Block3_union_row1.00 through trial:i03.ug.leaf_0003.02) confirms that all displacement amounts used left M1 enclosure intact, as evidenced by conn_preserved=true and 0 new out-of-crop violations in each case.

## V1.W.1: Minimum Width

V1.W.1 requires each V1 instance to be at least 18 nm wide along the M2 length direction. No trial in the history applied a resize operation directly to V1 shapes; all repairs used instance placement moves that preserved existing V1 dimensions (trial:i01.ug.leaf_0009.07 and trial:i01.ug.leaf_0012.08 each achieved repair with a single move_instance, leaving V1 width unchanged). Do not apply resize operations to V1 shapes directly; the repair record shows only move_instance and M2 resize_end as effective V1-area operations (trial:i01.ug.leaf_0008.06, trial:i02.ug.leaf_0001.00, trial:i03.ug.leaf_0001.00).

## V1.S.1 / V1.S.2 / V1.S.3 / V1.S.4: Spacing Rules

The V1 spacing rules differentiate vias with a 5 nm M2 end-cap (wec, minimum mask-space 16.4 nm euclidean under V1.S.2) from those without (nec, minimum 30 nm euclidean under V1.S.3), with the mixed case governed by V1.S.4 (minimum 27 nm euclidean). All iter-1 and iter-2 trials report n_new_in_crop=0, confirming that the displacements applied did not introduce new V1-to-V1 spacing violations. Trial:i03.ug.leaf_0003.02 reports n_new_in_crop=10 on a large multi-layer locus and was still accepted because conn_preserved=true; this establishes that a trial with new in-crop violations is accepted when connectivity is preserved. When moving a V1-carrying instance toward a neighboring V1, verify that the resulting projected separation of the V1 masks satisfies the applicable minimum before committing the move.

## Multi-Layer Loci and Co-Movement

Every trial touching V1 also touches M1 and M2 (trial:i01.ug.Block3_union_row1.00 through trial:i03.ug.leaf_0001.00). Trial:i03.ug.leaf_0003.02 additionally touches M3, M4, M5, V3, and V4 within a locus spanning [1728,3148] to [11016,9840]. Multi-instance op sets moving two or more instances in the same trial are consistently accepted when all moved instances shift by amounts that jointly satisfy the V1 containment and enclosure rules (trial:i01.ug.Block3_union_row1.00 with 3 ops, trial:i01.ug.Block3_union_row8.03 with 4 ops, trial:i01.ug.leaf_0008.06 with 2 moves and 1 resize).