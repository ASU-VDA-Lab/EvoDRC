## Repair Strategy for V4

### Effective Fix Pattern: Joint X-Axis Resize of V4 and M4

The sole confirmed effective repair recorded for this layer expands V4 via shapes and their enclosing M4 metal together along the X axis. In trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, three simultaneous `resize_via_shape` operations were applied to cell `VIA_VIA45_1_2_58_58`: V4 shape_index 0 and shape_index 1 were each grown +152 dbu on the X axis, and M4 shape_index 0 was grown +152 dbu on the X axis in the same commit. This group (`V4M5_fix`) reduced whole-design violations from 68 to 52, a net delta of −16, with connectivity preserved (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01).

**Coordination requirement.** Apply M4 resize in the same operation group as the V4 resize. The history contains no successful single-layer V4 resize; the only applied fix touched M4 and V4 simultaneously (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01). Resizing V4 without the coordinated M4 adjustment risks introducing or leaving V4.M4.EN.1 failures (minimum 11 nm enclosure of V4 by M4 on at least two opposite sides), since enlarging the via without enlarging its metal cover reduces enclosure margins.

**Resize magnitude.** A step of 152 dbu on the X axis was sufficient to eliminate violations in the target cell while preserving connectivity (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01). No smaller step has been measured for this layer.

**Axis selection.** The single measured fix operated exclusively on the X axis for both V4 and M4 shapes (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01). Rule V4.W.1 requires minimum width of 24 nm along the length of M5; rule V4.M5.AUX.2 requires V4 width to exactly match M5 width in the direction perpendicular to M5 length. An X-axis resize therefore addresses the axis relevant to these width-matching and enclosure constraints when M5 runs along Y.

**Scope and connectivity.** Resizing multiple V4 shapes within the same cell in a single group is safe: trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 resized two V4 shapes and one M4 shape together with `conn_preserved: true` and no negative delta.

### Rules With No Recorded Repair Data

Rules V4.S.1, V4.S.2, V4.S.3, and V4.AUX.1 have no repair operations recorded in the current history. Do not apply spacing-motivated moves or via deletions for those rules without further measured evidence.