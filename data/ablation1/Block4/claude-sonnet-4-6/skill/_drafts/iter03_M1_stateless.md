## Observed Repair Strategies and Outcomes

### X-Axis Instance Moves Reliably Eliminate M1 Violations Without Introducing New Ones

Across all three iterations, positive X-axis instance moves in multiples of 36 dbu consistently resolved V1.M1.EN.1 and related enclosure violations with zero new violations introduced. Single-instance moves of +36 dbu succeeded in trial:i01.ug.Block4_union_row1.00, trial:i01.ug.leaf_0020.09, trial:i01.ug.leaf_0021.10, trial:i03.ug.leaf_0001.01, and trial:i03.ug.Block4_union_row7.00. Multi-instance moves where all instances shift by the same +36 dbu increment succeeded in trial:i01.ug.Block4_union_row6.05 (three instances) and trial:i03.ug.Block4_union_row7.00 (two instances). Larger multiples — +72 dbu (trial:i02.ug.Block4_union_row1.00), +108 dbu (trial:i01.ug.Block4_union_row2.02, trial:i02.ug.Block4_union_row7.03) — also produced zero new violations. Non-multiple-of-36 moves of +12 dbu (trial:i01.ug.Block4_union_row10.01) and −28 dbu (trial:i02.ug.Block4_union_row3.02, trial:i01.ug.Block4_union_row7.06) similarly cleared cleanly.

When multiple instances within the same locus are moved simultaneously in the same direction and by consistent increments, the assembler produces a clean result: trial:i01.ug.Block4_union_row5.04 moved four instances each by +37 dbu with no new violations, and trial:i01.ug.Block4_union_row7.06 moved two instances by −28 dbu while also moving two M1 polygons, all with zero new violations.

Apply X-axis instance moves of ±36 dbu or ±28 dbu as the first strategy when V0.M1.EN.1, V1.M1.EN.1, or M1.S.x violations appear; move all instances in the locus uniformly to avoid relative misalignment.

### M1 Polygon resize_end (High-End X Extension) Resolves Enclosure Shortfalls

Extending the high end of an M1 polygon in the X direction resolves enclosure violations without generating new spacing or area violations. In trial:i01.ug.Block4_union_row7.06, polygon p1395 was extended +172 dbu at its high X end alongside instance moves; the combined operation produced zero new violations across M1, M2, M3, M4, V1, and V2. In trial:i01.ug.leaf_0008.08, polygon p1604 was extended +92 dbu at its high end concurrent with a +36 dbu instance move, again yielding zero new violations. In trial:i02.ug.Block4_union_row10.01, polygon p1551 was extended +16 dbu at its high end as part of a four-op bundle with zero new violations. In trial:i02.ug.Block4_union_row7.03, polygon p1595 was extended at its high end alongside a +108 dbu instance move with zero new violations.

The resize_end operation (axis x, end high) extending M1 polygon coverage satisfies V0.M1.EN.1 and V1.M1.EN.1 requirements by increasing the metal overhang at the via's high-X side. Use resize_end to complement instance moves when the enclosure gap is too large to close by instance translation alone — as shown in trial:i01.ug.Block4_union_row7.06 where +172 dbu was required.

Polygon-only axis moves (not resize_end) at small deltas also work: a +16 dbu X move on polygon p1548 in trial:i01.ug.Block4_union_row2.02 produced zero new violations.

### Y-Axis Negative Moves Introduce M1.A.1, M1.S.2, and V1.M1.EN.1 Violations

Do not apply negative Y-axis moves to instances that contain small M1 segments or M1 shapes near V1 vias. In trial:i02.ug.leaf_0013.06, moving instance i0038 by [0, −36] dbu introduced 9 new violations: 2 M1.A.1, 1 M1.S.2, and 4 V1.M1.EN.1. In trial:i02.ug.leaf_0008.04, moving the same instance by [0, −44] dbu introduced 2 new violations (M2.S.2, V1.M2.EN.2), confirming that even smaller Y-axis shifts disrupt via enclosure margins. In trial:i03.ug.leaf_0004.02, a further Y-axis move of [0, −64] dbu on i0038 introduced 2 new violations. Across these three trials on the same instance, every negative Y move produced new in-crop violations.

The V1.M1.EN.1 rule requires M1 to enclose V1 by at least 5 nm on one axis and 2 nm on the other. A vertical shift that moves the M1 shape away from the V1 via in the Y direction directly erodes this margin; with a 36 dbu shift, four simultaneous V1.M1.EN.1 failures are generated (trial:i02.ug.leaf_0013.06), indicating multiple via edges fall below threshold simultaneously.

The M1.A.1 rule requires minimum M1 area of 504 nm-sq. A −36 dbu Y shift on i0038 caused two M1.A.1 violations (trial:i02.ug.leaf_0013.06), meaning the shift caused at least two M1 shapes to fall below minimum area — an outcome consistent with a Y move that clips M1 fragments out of the active region or narrows them below minimum dimensions.

Never use a Y-axis negative move as a repair strategy for M1 DRC violations on instances known to carry V1 vias or short M1 segments. If a Y-axis move is required by connectivity, extend M1 coverage using resize_end to restore V1.M1.EN.1 margins after the move.

### Instance Conflict Drops Invalidate Assembled Operations

When two units within the same iteration claim conflicting operations on the same instance, the assembler drops one of the conflicting ops and marks it `external_conflict_dropped`. In iteration 2, both unit leaf_0008 and unit leaf_0013 attempted Y-axis moves on instance i0038 in opposite-priority order; the assembler dropped the leaf_0013-perspective op for trial:i02.ug.leaf_0008.04 (trial:i02.ug.leaf_0008.04 assemble_drops) and dropped the leaf_0008-perspective op for trial:i02.ug.leaf_0013.06 (trial:i02.ug.leaf_0013.06 assemble_drops). Each trial therefore ran a subset of the intended operations, and violations still appeared.

When a trial reports assemble_drops, the resulting violation count reflects only the surviving ops. Do not rely on the per-rule violation counts of conflict-affected trials to calibrate move magnitude for the dropped operation — the surviving op and the dropped op act on the same instance and their violation footprints may overlap or cancel.

### V1.M1.EN.1 Repair: Enclosure on Two Opposite Sides

V1.M1.EN.1 requires M1 to enclose V1 by 5 nm on one pair of opposite edges and 2 nm on the other (the asymmetric 5&2 nm rule). When this rule fires for multiple vias simultaneously — as seen with 4 violations from a single move in trial:i02.ug.leaf_0013.06 — the root cause is a shift in the instance that moves M1 collectively away from all enclosed vias. Repair by moving the instance back toward the via stack (positive X or Y correction) or by extending the M1 polygon's high end to cover the deficient enclosure side. The successful +36 dbu instance moves in trials such as trial:i03.ug.Block4_union_row7.00 and trial:i03.ug.leaf_0001.01 each touched M1, M2, and V1 layers and produced zero new V1.M1.EN.1 violations, confirming that correctly-sized X moves restore enclosure on both the V0 and V1 via stacks simultaneously.

### M1.S.2 Tip-to-Side Spacing Exposure from Y Moves

M1.S.2 flags a tip-to-side spacing violation when an M1 tip edge (length ≤ 36 nm) is separated from a side edge of a neighboring M1 shape by less than 25 nm. In trial:i02.ug.leaf_0013.06, a single −36 dbu Y-axis instance move produced one M1.S.2 violation, demonstrating that Y displacement of an M1 shape can expose a previously-clear tip toward a neighboring M1 side. X-axis moves as large as +108 dbu produced zero M1.S.2 violations across multiple trials including trial:i01.ug.Block4_union_row2.02 and trial:i02.ug.Block4_union_row7.03, indicating that horizontal moves along the M1 wire direction do not create new tip exposures when the routing is orthogonal and the grid is maintained.

### M1.A.1 Exposure from Y Moves; Not Triggered by X Moves

M1.A.1 (minimum M1 area 504 nm-sq) appeared only in trial:i02.ug.leaf_0013.06, triggered by a −36 dbu Y instance move, producing 2 violations. No X-axis instance or polygon move in any trial generated an M1.A.1 violation. When repairing M1 enclosure or spacing violations, prefer X-axis moves and resize_end operations to avoid inadvertently shrinking M1 shape area below 504 nm-sq.

### Connectivity Preservation Gates Acceptance Irrespective of New Violations

All trials in this history were accepted with `decision: gated_in` and `conn_preserved: true`, including trials that introduced new violations (trial:i02.ug.leaf_0008.04 with 2 new violations, trial:i02.ug.leaf_0013.06 with 9 new violations, trial:i03.ug.leaf_0004.02 with 2 new violations). The gating criterion is connection preservation, not violation count. Repair operations that preserve connectivity are accepted even when they introduce new in-crop M1 violations. This means M1 violations introduced as side effects of connectivity-preserving moves accumulate across iterations and require separate resolution passes.