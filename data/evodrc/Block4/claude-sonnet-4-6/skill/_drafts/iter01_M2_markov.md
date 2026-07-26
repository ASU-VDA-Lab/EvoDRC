**Effective M2 DRC repair strategies — iteration 1**

**Lateral instance translation clears M2 spacing violations**

Horizontal (x-axis) instance moves are the primary repair primitive for M2 spacing and tip-to-side violations. All ten unit_gate trials accepted in this iteration used only x-axis deltas (y-delta = 0 in every op), and all produced zero new violations in or out of crop (trial:i01.ug.leaf_0008.08, trial:i01.ug.leaf_0020.09, trial:i01.ug.leaf_0021.10, trial:i01.ug.Block4_union_row1.00, trial:i01.ug.Block4_union_row2.02, trial:i01.ug.Block4_union_row3.03, trial:i01.ug.Block4_union_row5.04, trial:i01.ug.Block4_union_row6.05, trial:i01.ug.Block4_union_row7.06, trial:i01.ug.Block4_union_row10.01). Applied deltas ranged from -108 to +112 dbu; +36 dbu is the most frequently used single-step increment. Never apply y-axis instance moves for M2 spacing repair; no accepted trial used a non-zero y-delta.

**Balance paired moves to avoid displacing violations to the far side**

When one instance is shifted in the positive x-direction, assign a compensating negative shift (-36 dbu) to the neighboring instance on the opposing side of the gap, or leave it stationary. This distributes the spacing correction and avoids introducing a new M2.S.1 or M2.S.2 violation on the far edge. Accepted examples: trial:i01.ug.Block4_union_row3.03 (i0170 at -36, i0292 at +36) and trial:i01.ug.Block4_union_row5.04 (three instances at +64, one at -36).

**Always accompany instance moves with resize_end on affected M2 polygon ends**

When an instance move elongates or contracts the gap between an M2 polygon and its neighbor, a resize_end op on the high or low x-end of the affected M2 polygon is required to restore connectivity without creating a minimum-width or area violation. All accepted multi-op repairs that included a resize_end used high-end extensions of +56 to +172 dbu and low-end extensions of +64 to +72 dbu on axis x (trial:i01.ug.Block4_union_row2.02, trial:i01.ug.Block4_union_row5.04, trial:i01.ug.Block4_union_row7.06, trial:i01.ug.Block4_union_row10.01). Do not leave an M2 polygon end floating after a move without a matching resize_end.

**Insert a bridge M2 polygon when a large translation breaks net continuity**

When a large instance translation (≥112 dbu) opens a gap that a resize_end cannot close without violating M2.S.1/M2.S.2, insert a new rectangular M2 polygon to bridge the break. In trial:i01.ug.Block4_union_row1.00 two bridge polygons were added (192×72 dbu and 92×72 dbu); both satisfy M2.W.1 (minimum width 18 nm) and M2.A.1 (minimum area 504 nm²) with large margin. Ensure every added polygon's narrower dimension is ≥ 18 dbu and its area ≥ 504 dbu² before committing.

**Co-move M1 and V1 with every M2 repair**

Every accepted M2 repair simultaneously touched M1 and V1; two also touched M4 (trial:i01.ug.Block4_union_row7.06, trial:i01.ug.Block4_union_row10.01). M2 spacing corrections must move the full vertical via stack (M1, V1, M2) together to preserve V1.M2.EN.2 and V1.M2.AUX.2 enclosure. Do not shift an M2 segment without issuing the corresponding move_instance (or resize_end) on the connected M1 and V1 geometry in the same operation set.

**Via shape resize on upper-metal layers does not repair M2 DRC**

Resizing a V2/M3 via shape that incidentally intersects the M2 bounding box produces no net improvement in M2 violation count. The one cu_pool trial that applied a resize_via_shape to M3/V2 was rejected with delta_total = 0 across all measured windows (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). Do not use upper-via resize ops as a substitute for direct M2 instance moves or polygon edits when the root violation is on M2.