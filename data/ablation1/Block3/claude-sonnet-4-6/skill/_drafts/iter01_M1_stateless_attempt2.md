## Operation outcomes

All ten trials in this iteration were accepted as `gated_in` with `n_new_in_crop: 0` and `n_new_out_of_crop: 0` across every M1-touching locus. No trial introduced new DRC violations on M1 (trial:i01.ug.Block3_union_row1.00, trial:i01.ug.Block3_union_row2.01, trial:i01.ug.Block3_union_row5.02, trial:i01.ug.Block3_union_row8.03, trial:i01.ug.leaf_0006.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0008.06, trial:i01.ug.leaf_0009.07, trial:i01.ug.leaf_0012.08, trial:i01.ug.leaf_0013.09).

## Move deltas

All `move_instance` operations applied delta_dbu values along the X-axis only (Y component always 0). The observed X deltas are 36, -36, or 108 dbu, i.e., integer multiples of 36 dbu (trial:i01.ug.Block3_union_row1.00 uses 36 and 108; trial:i01.ug.leaf_0013.09 uses -36). Apply X-axis instance moves in multiples of 36 dbu to remain consistent with the grid that produced zero new M1 violations across all ten accepted trials (trial:i01.ug.Block3_union_row1.00 through trial:i01.ug.leaf_0013.09).

## Resize operations on M1

One `resize_end` operation was applied to M1 polygon p1261 in trial:i01.ug.leaf_0008.06: axis x, end high, delta_dbu 36. That trial was accepted with no new M1 violations. When extending an M1 polygon end along the X-axis, use a delta of 36 dbu (trial:i01.ug.leaf_0008.06) to stay within the accepted grid and avoid introducing M1.W.1, M1.S.1, M1.S.2, M1.S.3, M1.S.4, M1.S.5, M1.S.6, or M1.A.1 violations.

## Via enclosure rules (V0 and V1)

Rules V0.M1.EN.1 and V1.M1.EN.1 require M1 to enclose vias on two opposite sides. V0.M1.EN.1 requires 5 nm on at least one pair of opposite sides (with zero permitted on the complementary pair). V1.M1.EN.1 requires 5 nm on one side and at least 2 nm on the opposite. All trials that touched M1 also touched V1 (trial:i01.ug.Block3_union_row1.00 through trial:i01.ug.leaf_0013.09), and all were accepted without enclosure violations. Move instances and resize M1 ends only along the axis that preserves the enclosure margins already established by the pre-move layout; the accepted 36 dbu step size (trial:i01.ug.leaf_0008.06, trial:i01.ug.leaf_0009.07) kept all via enclosures within rule bounds.

## V0.M1.AUX.3 co-width constraint

Rule V0.M1.AUX.3 requires that V0 width matches M1 width along the direction perpendicular to the M1 run. Moves of entire instances along X (trial:i01.ug.Block3_union_row1.00 through trial:i01.ug.leaf_0013.09) preserve the relative geometry between V0 and M1 within each instance and therefore do not violate AUX.3. The single M1 polygon resize in trial:i01.ug.leaf_0008.06 extended the end of an M1 shape without disturbing perpendicular width, and was accepted with no AUX.3 violation.

## Spacing and width rules (M1.W.1, M1.S.1 through M1.S.6)

M1.W.1 sets a minimum M1 width of 18 nm. M1.S.1 sets minimum side-to-side spacing of 18 nm for edges longer than 36 nm. M1.S.2 sets tip-to-side spacing of 25 nm. M1.S.3 sets 27 nm tip-to-tip for edges 24–36 nm wide. M1.S.4 and M1.S.5 set 31 nm for tip-to-tip configurations involving edges under 24 nm. M1.S.6 sets corner-to-corner spacing of 20 nm. All accepted trials (trial:i01.ug.Block3_union_row1.00 through trial:i01.ug.leaf_0013.09) moved instances only 36 or 108 dbu along X or resized one polygon end by 36 dbu (trial:i01.ug.leaf_0008.06), and none produced spacing or width violations. Avoid moves or resizes that bring M1 edges to within the spacing minimums listed above; the 36 dbu step used across all ten trials preserved all spacing margins.

## Area rule (M1.A.1)

M1.A.1 requires a minimum M1 polygon area of 504 nm-sq. No trial produced an M1.A.1 violation. The resize_end operation in trial:i01.ug.leaf_0008.06, which increased polygon p1261 area by extending its high-X end by 36 dbu, maintained area compliance.

## Redundant island rule (M1.R.0)

M1.R.0 flags M1 islands enclosing exactly one small V0 via when near a large empty M1 region. No trial produced an M1.R.0 marker (trial:i01.ug.Block3_union_row1.00 through trial:i01.ug.leaf_0013.09). Instance moves and single-end resizes at the 36 dbu step did not create isolated single-via M1 fragments.

## Layer interaction pattern

Every accepted trial in this iteration touched M1, M2, and V1 together (trial:i01.ug.Block3_union_row1.00 through trial:i01.ug.leaf_0013.09). No trial touched M1 in isolation. Apply M1 edits together with their associated V1 and M2 context to preserve connectivity; the `conn_preserved: true` flag on all ten trials confirms that simultaneous multi-layer instance moves at 36 dbu steps hold connectivity without introducing new inter-layer violations.