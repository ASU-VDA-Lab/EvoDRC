## V4 Repair Knowledge — Iteration 4

### Cell VIA_VIA45_1_2_58_58: Equal-Delta X-Axis Resize of V4 and M4 Achieves Large Violation Reduction

Resizing both V4 shapes and the M4 shape in cell `VIA_VIA45_1_2_58_58` by the same +152 dbu x-axis delta reduces DRC violations substantially. In trial:i04.cu.def:VIA_VIA45_1_2_58_58.00 the cu_pool channel applied three ops — resize V4 shape_index:0 by +152 dbu x, resize V4 shape_index:1 by +152 dbu x, and resize M4 shape_index:0 by +152 dbu x — achieving `delta_total: −18` (window `unit:whole_design` went from 21 to 3 violations, `decision: applied`, `conn_preserved: true`). This operation is accepted and confirmed effective under design state `8a722f989fdc21cf094a3ebd8d95a2800f21586dfd35b6db34bc6c9848972add`.

The critical distinction from the failed iteration-2 attempt (trial:i02.cu.def:VIA_VIA45_1_2_58_58.00, `delta_total: 0`, rejected) is the resize delta applied to V4: iteration 2 used +76 dbu per V4 shape (half the M4 delta of +152 dbu) combined with ±38 dbu moves; iteration 4 uses +152 dbu per V4 shape equal to the M4 delta with no accompanying moves. Equal-delta resizing of V4 and M4 along x is the correct formulation; the asymmetric-delta-plus-move approach is exhausted without improvement.

Do not retry the iteration-2 combination (V4 +76 dbu with ±38 dbu moves, M4 +152 dbu) in this cell; it is recorded as producing no improvement. Apply the equal +152 dbu x-axis resize to all V4 shapes and M4 together when addressing this cell's violations.

### V4.AUX.1 and V4.M4.EN.1 Enclosure: Equal Resize Maintains Containment

The accepted trial (trial:i04.cu.def:VIA_VIA45_1_2_58_58.00) confirms that resizing V4 and M4 by the same delta (+152 dbu x-axis each) satisfies V4.AUX.1 (V4 must be inside both M4 and M5) and does not introduce new out-of-crop violations. Keeping V4 resize delta equal to the M4 resize delta preserves the relative enclosure margin required by V4.M4.EN.1 (≥11 nm on two opposite sides). The asymmetric ratio from iteration 2 (M4 = 2× each V4 resize) did not resolve violations; the 1:1 equal-delta ratio does.

### Assemble-Drop Filtering: Cu_Pool-Rejected Ops Are Excluded From Whole-Design Trials

When the cu_pool channel rejects a set of ops with `rejected_net_positive`, those ops are recorded in `assemble_drops` and excluded from subsequent whole-design assembly. Trial:i02.ug.whole_design.00 lists all five ops from trial:i02.cu.def:VIA_VIA45_1_2_58_58.00 in its `assemble_drops` array with reason `cu_pool:rejected_net_positive`. Never re-inject cu_pool-rejected V4 resize ops into a whole-design pass; they were explicitly filtered. Accepted ops (such as those from trial:i04.cu.def:VIA_VIA45_1_2_58_58.00) are eligible for whole-design assembly.

### Whole-Design X-Axis Instance and Polygon Moves Accepted for V4-Touching Shapes

The whole-design trial trial:i02.ug.whole_design.00 was accepted (`decision: gated_in`) after moving V4-layer polygons p1059 and p1060 each by +32 dbu on the x-axis, together with x-axis and y-axis moves of multiple instances (i0173, i0147, i0083, i0085, i0163, i0177, i0079, i0078, i0140, i0151, i0192, i0096, i0088, i0152, i0102, i0101). Touched layers included V4, M4, M5, M3, and V3. No new out-of-crop violations were introduced (`new_out_of_crop_bboxes: []`, `new_out_of_crop_by_rule: {}`). A +32 dbu x-axis shift of V4 polygons in a whole-design coordinated move is a viable accepted operation when connectivity is preserved.

### Spacing Rules Require 33 nm on All Metrics; Active Violations Substantially Reduced

Rules V4.S.1, V4.S.2, and V4.S.3 each enforce a 33 nm minimum (projection for S.1/S.2, Euclidean corner-to-corner for S.3). The accepted equal-delta x-axis resize (trial:i04.cu.def:VIA_VIA45_1_2_58_58.00) reduced whole-design violations from 21 to 3 (`delta_total: −18`), so the majority of spacing and enclosure violations in cell `VIA_VIA45_1_2_58_58` are resolved by that operation. Three violations remain open in the whole-design window as of iteration 4; V4.M5.AUX.2 (V4 width must match M5 width perpendicular to M5 length) has not been explicitly targeted by any accepted operation and may account for residual violations.