## Repair Patterns Observed

### X-axis Via Resize Reduces Violations

The only confirmed repair pattern for V4 in this iteration is a co-resize of V4 and M4 shapes along the x-axis inside the via cell `VIA_VIA45_1_2_58_58`. Both V4 shape indices (0 and 1) and the corresponding M4 shape (index 0) were each grown by +152 dbu on the x-axis. This single operation reduced the aggregate DRC violation count by 16 (unit `leaf_0012` dropped from 27 to 19; unit `leaf_0013` dropped from 28 to 20) and connectivity was preserved (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, trial:i01.ug.leaf_0012.07).

### Co-resize V4 and M4 Together on the Same Axis

Growing a V4 shape on axis x without a matching M4 resize risks violating V4.M4.EN.1 (minimum 11 nm enclosure on two opposite sides). In trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 both layers received the identical +152 dbu x-delta, confirming that V4 and the bounding M4 shape must move together to maintain enclosure compliance. Never apply a unilateral V4 x-resize without resizing the enclosing M4 shape by the same delta on the same axis.

### Apply the Resize to All V4 Shapes in the Cell

The repair in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 targeted both shape_index 0 and shape_index 1 of V4 within the same via cell. Resizing only one shape index while leaving the other unchanged would create asymmetry that can expose V4.S.1, V4.S.2, or V4.S.3 violations (minimum 33 nm projection and corner-to-corner spacing). Always apply the x-axis resize uniformly across all V4 shape indices within a given cell.

### Via Cell VIA_VIA45_1_2_58_58 Is the Confirmed Target

The measured repair operated on the cell definition `VIA_VIA45_1_2_58_58` (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01). Because the repair was applied at the cell-definition level (target field `def:VIA_VIA45_1_2_58_58`), it propagates to all instances of that cell. Instance-level moves (as seen for M3/V3 in trial:i01.ug.leaf_0012.07) were not the primary V4 repair mechanism; the effective V4 fix was the definition-level resize.

### Instance Moves Do Not Directly Fix V4

The unit-gate trial (trial:i01.ug.leaf_0012.07) moved four instances (i0097, i0092, i0064, i0072) on the y-axis, touching V4 among other layers. That trial was gated in and reported V1.M1.EN.1 as the new in-crop rule hit, not any V4 rule. The V4 fix credited in that trial's `assemble_drops` originated from the cu_pool x-resize already applied to `VIA_VIA45_1_2_58_58`. Do not rely on y-axis instance moves to resolve V4 width, spacing, or enclosure violations; the confirmed mechanism is the x-axis via shape resize.