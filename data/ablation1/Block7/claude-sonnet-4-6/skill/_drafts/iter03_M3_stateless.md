## M3.S.2 — Tip-to-Side Spacing (25 nm minimum)

M3.S.2 fires when an M3 edge ≤ 36 nm faces an M3 edge > 36 nm with less than 25 nm projection separation. The only measured M3.S.2 generation event produced 10 new violations in a single repair: a bulk symmetric y-axis resize of −64 dbu applied to 39 M3 polygons simultaneously (trial:i02.ug.leaf_0045.20). Do not apply large symmetric resize operations (≥ 64 dbu) across many M3 polygons in one step; this approach consistently creates M3.S.2 tip-to-side violations by shortening polygon ends into tip territory (≤ 36 nm) and bringing those new tips within 25 nm of adjacent side edges that were previously compliant.

When M3 polygon height is reduced, newly shortened y-edges become tips (≤ 36 nm). Surrounding M3 side edges (> 36 nm) that previously cleared the tip-to-side rule can fall within 25 nm of the new tips, triggering M3.S.2. A −64 dbu symmetric reduction amplifies this across the design by creating many new short tips in a single operation (trial:i02.ug.leaf_0045.20).

## M3.S.4 — Narrow Tip-to-Tip Spacing (31 nm minimum)

M3.S.4 fires when two M3 edges both < 24 nm in length face each other with less than 31 nm projection separation. The same bulk y-resize of −64 dbu in trial:i02.ug.leaf_0045.20 generated 1 new M3.S.4 violation alongside the 10 M3.S.2 violations. Symmetric shrink of M3 polygon height that produces narrow tips (< 24 nm) risks M3.S.4 when neighboring narrow-tip polygons are already near the 31 nm minimum. Avoid symmetric shrinks that bring any polygon end below 24 nm in width, particularly in dense M3 regions.

## Bulk M3 Symmetric Resize — Avoid Large Negative Steps

The only multi-polygon M3-only repair in the history applied a −64 dbu symmetric y-resize to 39 polygons and produced 11 new M3 violations (10 M3.S.2, 1 M3.S.4) while also triggering a via-shape resize drop (trial:i02.ug.leaf_0045.20). This repair was accepted (gated_in) only because connectivity was preserved and no out-of-crop violations occurred; it nevertheless increased in-crop DRC count by 150 across all rules. Use individual targeted single-end adjustments instead of broad symmetric shrink when reducing M3 polygon dimensions.

A smaller targeted M3 single-end retraction of −20 dbu on one polygon (resize_end y high −20 on p2328, trial:i02.ug.leaf_0009.12) introduced only 1 new in-crop violation and was accepted. Targeted single-end moves at ≤ 20 dbu produce minimal M3 violation side effects compared to bulk symmetric operations.

## V2 Via Shape Resize on M3 — Net-Positive Risk

Shrinking the M3 shape within via cell VIA_VIA23_1_3_36_36 by −40 dbu in y was rejected by the cu_pool evaluator as net_positive — it did not reduce total DRC count across any of the five evaluated windows (delta_total: 0, trial:i02.cu.def:VIA_VIA23_1_3_36_36.00). The same resize was dropped at assembly during trial:i02.ug.leaf_0045.20 (assemble_drops, reason: cu_pool:rejected_net_positive). Do not apply y-axis M3 via shape shrinks of ≥ 40 dbu on VIA_VIA23_1_3_36_36; the V2.M3.EN.2 two-opposite-sides enclosure requirement and the V2.M3.AUX.2 width-match constraint make this direction violation-generating rather than violation-reducing.

## Instance Moves on M3/V2 — Safe at Moderate Step Sizes

Instance moves of 36–57 dbu in x or y on cells that touch M3, M2, and V2 have been accepted with zero new M3 violations across multiple trials:

- y+57 dbu whole-polygon and instance move (trial:i02.ug.Block7_union_row17.02, 0 new violations)
- y−36 dbu instance move touching M2, M3, V2 (trial:i02.ug.leaf_0010.13, 0 new violations)
- y+36 dbu instance move touching M2, M3, V2 (trial:i03.ug.leaf_0002.07, 0 new violations)

Instance moves at 36–57 dbu do not create new M3 spacing or width violations. Larger coordinated multi-instance moves in x (36–108 dbu, trials i01.ug.Block7_union_row12.02, i01.ug.Block7_union_row9.21) also completed with 0 new M3 violations when the moved group preserves relative polygon positions.

## Polygon Translation vs. Resize End

Moving M3 polygons as whole units (op: move) produces no new M3 violations in all observed cases (trials i02.ug.Block7_union_row17.02, i03.ug.Block7_union_row17.02). Resizing a single end of an M3 polygon (resize_end) at increments of 4–56 dbu on one end at a time also avoids new M3 violations across all iter 1 single-end operations (trials i01.ug.Block7_union_row12.02, i01.ug.Block7_union_row13.03, i01.ug.Block7_union_row14.04, i01.ug.leaf_0024.25, i01.ug.Block7_union_row9.21). The M3 violation risk concentrates in symmetric resize (both ends simultaneously) at large deltas, not in single-end or whole-polygon operations at comparable magnitudes.

## Oscillating Instance Positions — Violation Direction Asymmetry

Instances i0949 and i0950 moved y−52 in iter 1 (trial:i01.ug.Block7_union_row19.09, 1 new in-crop violation), y+52 in iter 2 (trial:i02.ug.leaf_0032.17, 4 new in-crop violations), then y−52 in iter 3 (trial:i03.ug.Block7_union_row19.03, 1 new in-crop violation). The y+52 direction produces 4× more new violations than the y−52 direction for this instance group. When the same instance set reverses direction across iterations, the direction that produced more violations (y+52 here) is the violation-generating direction; avoid re-applying that direction in subsequent iterations.