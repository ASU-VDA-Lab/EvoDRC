**High-yield operation: M5 y-shrink in via cell VIA_VIA45_1_2_58_58**

Shrinking the M5 shape (shape_index 0) in cell `VIA_VIA45_1_2_58_58` by 88 dbu on the y-axis reduced the total violation count from 47 to 32, eliminating 15 violations in a single cu_pool operation (trial:i03.cu.def:VIA_VIA45_1_2_58_58.00). No other single-operation M5 change in the recorded history matches this yield. Apply this y-shrink to `VIA_VIA45_1_2_58_58` shape_index 0 whenever the cell is present and has not already received this reduction (trial:i03.cu.def:VIA_VIA45_1_2_58_58.00).

**Deduplication between cu_pool and unit_gate: assemble_drop reason `cu_pool:applied` is not an error**

When cu_pool commits an operation to a via cell definition, the unit_gate assembler drops the identical op with reason `cu_pool:applied` (trial:i03.ug.whole_design.00). In iter 3, the unit_gate run dropped the `VIA_VIA45_1_2_58_58` M5 y-resize for exactly this reason; the design state `68104886e25dfbd12e0678a2ceab563e72350b564c21e8ca83a16267697fff38` already incorporated the cu_pool change before unit_gate assembled (trial:i03.ug.whole_design.00, trial:i03.cu.def:VIA_VIA45_1_2_58_58.00). Never re-issue to unit_gate an operation that cu_pool has already committed; treat the assemble_drop as confirmation of success (trial:i03.ug.whole_design.00).

**x-axis shifts of +32 dbu on M5 polygons p878 and p879: accepted with zero new violations**

Moving p878 and p879 each by +32 dbu in x, together with [32, 0] moves on seven instances (i0001, i0062, i0067, i0073, i0112, i0113, i0114), introduced zero new in-crop violations and preserved all connectivity in iter 3 (trial:i03.ug.whole_design.00). These polygons share their vertical stack with M4 and V4 (the touched_layers record confirms all three were moved together); move M5 polygons in x only when the co-located M4 and V4 geometry moves by the same delta (trial:i03.ug.whole_design.00).

**Polygon p879 corrected across two iterations: y high-end resize first, then x repositioning**

p879 received a +48 dbu y high-end resize in iter 1 (trial:i01.ug.whole_design.00) and a +32 dbu x move in iter 3 (trial:i03.ug.whole_design.00). Both operations were gated in with connectivity preserved. The iter 1 y-resize did not preclude the iter 3 x-move; applying edge resizes and lateral repositioning to the same polygon in separate iterations is safe when each iteration preserves connectivity.

**Iter 1 multi-layer repair: y high-end resizes and small x moves on M5 accepted**

A 19-operation repair in iter 1 gated in with connectivity preserved across M1–M5 and V1–V4 simultaneously (trial:i01.ug.whole_design.00). M5-touching operations within that repair included: +48 dbu y high-end resize on p879; +8 dbu x move and +20 dbu y high-end resize on p910; [8, 0] instance moves on i0061 and i0104. Y high-end resizes of +20 dbu and +48 dbu on M5 polygons are both accepted amounts when the surrounding multi-layer context remains connectivity-safe (trial:i01.ug.whole_design.00).

**M5.AUX.2 routing track constraint: pitch 192 dbu, offset 48 dbu, base grid 96 dbu**

M5.AUX.2 requires minimum-width M5 track centerlines at x positions satisfying `(cl_x - 48) % 192 == 0`, with vertical edges also on the base grid of 96 dbu. The x-move amounts of +8 dbu (trial:i01.ug.whole_design.00) and +32 dbu (trial:i03.ug.whole_design.00) were both accepted without introducing new M5 violations, confirming these amounts moved polygons from off-track to on-track positions within the 192 dbu pitch. When correcting M5.AUX.2 violations, use x deltas that restore `(cl_x - 48) % 192 == 0` for the affected polygon centerlines; the recorded deltas of 8 and 32 dbu bracket the minimum useful correction range (trial:i01.ug.whole_design.00, trial:i03.ug.whole_design.00).

**M5.AUX.1 vertical edge grid: x-move corrections must land on 24 dbu boundaries**

M5.AUX.1 requires all M5 vertical edges at a 24 dbu grid. The x-moves of +8 dbu and +32 dbu applied in iter 1 and iter 3 respectively (trial:i01.ug.whole_design.00, trial:i03.ug.whole_design.00) were accepted without new M5.AUX.1 violations, confirming that the resulting edge positions after each move remained on the 24 dbu grid. Apply x corrections only in amounts that keep all M5 vertical edges at multiples of 24 dbu after the move (trial:i01.ug.whole_design.00, trial:i03.ug.whole_design.00).

**Instance and polygon moves must be co-applied for connected stacks**

In both accepted repairs, instance moves and direct polygon ops were issued together within the same operation set rather than split across separate trials: iter 1 combined 14 instance moves with 5 polygon ops in one 19-op trial (trial:i01.ug.whole_design.00); iter 3 combined 7 instance moves with 2 polygon moves in one 9-op trial (trial:i03.ug.whole_design.00). Apply all geometric corrections for a connected M4/M5/V4 stack within a single operation set to avoid intermediate connectivity breaks.