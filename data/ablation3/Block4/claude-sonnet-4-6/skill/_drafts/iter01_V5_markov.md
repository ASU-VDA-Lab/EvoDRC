**V5 enclosure repair via cu_pool: move-then-resize on y-axis**

The cu_pool channel repaired V5 enclosure violations by applying a paired move-then-resize sequence on individual V5 shapes within via cell definitions along the y-axis. In cell VIA_VIA56_2_1_66_58 (2-shape via), shape_index 0 was moved −132 dbu on y then resized +512 dbu on y, and shape_index 1 was moved +132 dbu on y then resized +512 dbu on y (trial:i01.cu.def:VIA_VIA56_2_1_66_58.00). The moves are antisymmetric (each shape moves inward toward the array center) while the resize is identical for both. This repair reduced the violation count by 2 (147 → 145).

In cell VIA_VIA56_2_2_66_58 (4-shape via), the same paired pattern was applied to all four shapes as two antisymmetric pairs: shapes at indices 0 and 1 each moved −132 dbu y and resized +512 dbu y; shapes at indices 2 and 3 each moved +132 dbu y and resized +512 dbu y (trial:i01.cu.def:VIA_VIA56_2_2_66_58.01). This repair reduced the violation count by 4 (147 → 143). Connectivity was preserved in both cases.

The 512 dbu resize magnitude and 132 dbu inward move are the measured correction quanta for y-axis enclosure deficits in VIA_VIA56_2_x_66_58 cell families (trial:i01.cu.def:VIA_VIA56_2_1_66_58.00, trial:i01.cu.def:VIA_VIA56_2_2_66_58.01). Apply both operations together per shape; neither alone is sufficient as only the combination was observed to reach the applied decision.

**V5 shapes are modified jointly with M5 and M6**

All three repairs in this iteration touched layers M5, M6, and V5 together (trial:i01.ug.whole_design.00, trial:i01.cu.def:VIA_VIA56_2_1_66_58.00, trial:i01.cu.def:VIA_VIA56_2_2_66_58.01). Do not modify V5 shapes in isolation from their enclosing M5/M6 geometry; the repair operations span all three layers in each applied fix.

**unit_gate whole-design move gated in without new violations**

A y-axis move of +64 dbu applied to polygon p1402 and two instances (i0234, i0305) was accepted by the unit_gate channel with decision gated_in, zero new in-crop violations, and connectivity preserved (trial:i01.ug.whole_design.00). The cu_pool enclosure fixes to VIA_VIA56_2_1_66_58 and VIA_VIA56_2_2_66_58 were assembled and carried forward as drops within this unit_gate trial without introducing out-of-crop debt.

**Scaling and cell-family context**

VIA_VIA56_2_1_66_58 and VIA_VIA56_2_2_66_58 are two members of the VIA_VIA56_2_x_66_58 family, differing in shape count (2 vs. 4). The 4-shape cell produced twice as many enclosure violations per instance as the 2-shape cell, consistent with each shape contributing independently to V5.M5.EN.1 or V5.M6.EN.2 violation count (trial:i01.cu.def:VIA_VIA56_2_1_66_58.00, trial:i01.cu.def:VIA_VIA56_2_2_66_58.01).