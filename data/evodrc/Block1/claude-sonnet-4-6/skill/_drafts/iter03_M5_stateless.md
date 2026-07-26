**M5.AUX.1 — Vertical-edge grid (24 nm)**

X-axis polygon translations of +32 dbu and −16 dbu each produced 12 new M5.AUX.1 violations (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03). Neither 32 nor 16 is an integer multiple of 24; both displacements left every moved vertical edge off the 24 nm grid. X-axis displacements applied to M5 polygons must be integer multiples of 24 dbu to avoid M5.AUX.1. A y-axis resize_end of +44 dbu on p1154 in trial:i02.ug.leaf_0002.01 and an x-axis resize_end of −32 dbu on p1187 in trial:i03.ug.leaf_0001.00 each introduced zero new M5.AUX.1 violations, confirming that y-axis changes do not affect the x-edge grid, and that the −32 dbu resize placed the high edge of p1187 at a grid-legal absolute coordinate in that specific starting state.

A resize_end delta that is not itself a multiple of 24 does not automatically cause M5.AUX.1; the absolute post-move coordinate of the affected edge is what the rule checks. When applying x-axis resize_end, verify the resulting absolute edge coordinate is a multiple of 24 dbu — do not judge legality from the delta alone (trial:i03.ug.leaf_0001.00 vs. trial:i02.ug.leaf_0003.02).

**M5.AUX.3 — No bends**

Both trial:i02.ug.leaf_0003.02 and trial:i02.ug.leaf_0004.03 introduced 38 M5.AUX.3 violations each. In leaf_0003, instance moves carried mixed x+y components — [32,−64], [32,−112], [32,−96], [−16,−64], [−16,−112], [−16,−96] — alongside y-only polygon moves on p1563 (−64y), p1562 (−112y), and p1561 (−96y). In leaf_0004, the mixed-component instance moves included [32,32], [−16,32], [32,72], [32,24], [32,−24], [32,−72], [−16,72], [−16,24], [−16,−24], [−16,−72] dbu. By contrast, the pure x-axis instance move [−76,0] in trial:i02.ug.leaf_0002.01 and [76,0] in trial:i03.ug.leaf_0001.00 produced zero M5.AUX.3 violations. M5-touching cell instances must not be translated with simultaneous non-zero x and y components; instance moves must be decomposed into single-axis steps, or M5.AUX.3 fires.

**M5.W.5 — Minimum vertical width (44 nm)**

Twelve new M5.W.5 violations appeared in both trial:i02.ug.leaf_0003.02 and trial:i02.ug.leaf_0004.03, driven by y-axis polygon body shifts (−64, −96, −112 dbu on M5 shapes) that compressed vertical extents below the 44 nm floor. The resize_end in trial:i02.ug.leaf_0002.01, which expanded the low end of p1154 by exactly +44 dbu in y, introduced zero M5.W.5 violations, establishing that 44 dbu is the exact minimum vertical extent and that expanding a low endpoint by that exact amount is safe. Do not shift M5 polygon bodies in y without confirming that neither the moved shape nor any neighbour whose spacing is affected falls below 44 nm vertical width.

**M5.S.4 — Tip-to-tip spacing with shared parallel run length (40 nm)**

Four new M5.S.4 violations appeared in each of trial:i02.ug.leaf_0003.02 and trial:i02.ug.leaf_0004.03, coinciding with the same y-axis polygon displacements that produced M5.W.5 and M5.AUX.3 violations. No M5.S.4 violations appeared in trial:i02.ug.leaf_0002.01, trial:i03.ug.leaf_0001.00, or trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, where only single-axis moves or via-shape y-resizes were applied. Y-axis shifts of M5 polygon bodies that alter tip positions relative to shapes on adjacent tracks with parallel run length must maintain 40 nm tip-to-tip clearance.

**V4.M5.AUX.2 — V4 width must exactly match M5 width perpendicular to M5 length**

Four new V4.M5.AUX.2 violations appeared in trial:i02.ug.leaf_0003.02, where M5 polygons p1145 (+32 dbu x) and p1144 (−16 dbu x) were translated laterally. These x-axis body shifts moved M5 shapes out of lateral alignment with their associated V4 vias. No V4.M5.AUX.2 violations occurred in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, where the M5 via shape was resized −88 dbu in y while x-extent was unchanged. Lateral x-axis translation of M5 polygon bodies breaks the M5-width/V4-width co-constraint; y-axis resizing of the via shape that preserves x-extent does not. When adjusting M5 shapes that enclose V4 vias, use y-axis resizing rather than x-axis translation unless the V4 shape is moved in lock-step.

**Via cell M5 y-axis resize: effective DRC reduction**

In trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, resizing the M5 shape in cell VIA_VIA45_1_2_58_58 by −88 dbu in y (axis y, shape_index 0) eliminated 26 violations in each of two windows (leaf_0034, leaf_0035), total delta −52. The operation was applied with conn_preserved=true. This is the only "applied" repair in the history and the only record showing a net M5 DRC reduction. A y-axis shrink of an M5 via shape is a confirmed DRC-reducing operation on this cell type when the starting shape is over-long in y.

**Safe vs. unsafe operation patterns on M5 (history summary)**

Operations that produced zero new M5 violations: y-axis resize_end expanding low endpoint of an M5 shape by +44 dbu (trial:i02.ug.leaf_0002.01); x-axis resize_end shrinking the high endpoint of an M5 shape by −32 dbu where the resulting edge is grid-aligned (trial:i03.ug.leaf_0001.00); y-axis shrink of an M5 via shape by −88 dbu in a via cell (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01); pure x-axis instance translation ([−76,0] and [76,0]) on M5-touching cells (trial:i02.ug.leaf_0002.01, trial:i03.ug.leaf_0001.00).

Operations that produced new M5 violations: x-axis polygon body translation by non-multiples of 24 dbu causing M5.AUX.1 (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03); instance moves with simultaneous x+y components on M5-touching cells causing M5.AUX.3, M5.W.5, and M5.S.4 (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03); lateral x-axis translation of M5 bodies co-located with V4 vias causing V4.M5.AUX.2 (trial:i02.ug.leaf_0003.02).

**Assemble conflict resolution does not prevent M5 violations in surviving ops**

When leaf_0003 and leaf_0004 competed, 26 instance-move ops from leaf_0003 were dropped before its trial ran, and 41 ops from leaf_0004 were dropped or deduplicated after leaf_0003 committed (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03). The surviving ops in each trial still fired identical M5 violation counts (M5.AUX.1: 12, M5.AUX.3: 38, M5.W.5: 12, M5.S.4: 4 in both). Conflict resolution removes duplicate or conflicting moves but does not sanitize the M5-grid or bend constraints of the retained moves; each surviving op must independently satisfy M5.AUX.1, M5.AUX.3, M5.W.5, and M5.S.4.