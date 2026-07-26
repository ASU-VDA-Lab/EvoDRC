## Repair Operation Patterns

All three trials in the recorded history for this layer were accepted as `gated_in` with `conn_preserved: true`. No trial produced new violations outside the crop region. This means every measured repair maintained global connectivity and did not worsen the design outside its local window.

V3 instances were never touched in isolation: every trial that touched V3 also touched M3 and M4 simultaneously (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03, trial:i03.ug.leaf_0001.00). This is consistent with V3.AUX.1, which requires V3 to lie inside the intersection of M3 and M4. Any repair that repositions a V3 instance must co-move or co-resize the enclosing M3 and M4 shapes to avoid creating a V3.AUX.1 or V3.M4.AUX.2 violation.

## Instance Move Operations

Pure `move_instance` operations applied symmetrically in pairs along the y-axis produced zero new in-crop violations (trial:i02.ug.leaf_0003.02: 6 ops, `n_new_in_crop: 0`). The paired pattern moved instances in equal and opposite directions (e.g., i0177/i0152 at −48 dbu, i0079/i0102 at +96 dbu, i0078/i0101 at +48 dbu), suggesting that symmetric spreading preserves inter-via spacing relationships captured by V3.S.1.

A single lateral (x-axis) move of −16 dbu on instance i0132 introduced 1 new in-crop violation (trial:i03.ug.leaf_0001.00: 1 op, `n_new_in_crop: 1`). Lateral displacement of a V3 instance without a paired move on its neighbor can reduce projected spacing and trigger V3.S.1 or V3.M4.AUX.2, since the width constraint (V3.M4.AUX.2) requires V3 to match M4 width exactly in the perpendicular direction.

## Polygon Resize Operations

In trial:i02.ug.leaf_0004.03, M4 polygon ends were extended (resize_end on polygons p1101–p1104 along y) in conjunction with instance moves; this introduced 2 new in-crop violations despite `conn_preserved: true`. The resize operations were asymmetric: p1104 and p1103 extended the high-y end, while p1102 and p1101 extended the low-y end. Extending M4 polygon ends shifts the effective v3_wec_mask and v3_nec_mask used in V3.S.1 and V3.S.2 checks. A resize that increases M4 end-cap coverage can change a via from the "no end-cap" (NEC) category to the "with end-cap" (WEC) category, altering which spacing threshold applies (18 nm same-track vs. 27 nm parallel tracks for V3.S.1; 30 nm corner-to-corner for V3.S.3 vs. 23 nm for V3.S.2).

## Co-movement Coupling

When M5 and V4 are also present in touched_layers alongside M3, M4, and V3 (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03), the repair bundle is larger and affects multiple via layers simultaneously. The V3-specific violations in these cases are resolved as part of a multi-layer move set; V3 repair cannot be planned in isolation when its M4 track is shared with V4.

## Enclosure and Width Constraints

V3.M3.EN.1 requires M3 to enclose V3 by at least 5 nm on two opposite sides. V3.M4.EN.2 requires M4 to enclose V3 by at least 11 nm on two opposite sides. V3.M4.AUX.2 requires V3 width to exactly match M4 width perpendicular to the M4 length direction. These three rules together mean that any resize of V3 along the M4-perpendicular axis must be matched by an equal resize of M4; any move of V3 that changes its overlap with M3 or M4 must be bounded such that both 5 nm (M3) and 11 nm (M4) enclosures are preserved. The history shows that all accepted repairs co-moved M3 and M4 with V3 rather than resizing V3 in place (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03, trial:i03.ug.leaf_0001.00), which avoids disturbing the width-match condition of V3.M4.AUX.2.

## Minimum Width

V3.W.1 sets a minimum V3 width of 18 nm along the M4 length direction. No trial records a V3 resize operation; all observed V3 modifications are `move_instance` ops. Resizing V3 below 18 nm along the M4 direction violates V3.W.1 and is not supported by any measured operation.

## Spacing Rule Geometry

V3.S.1 distinguishes three sub-cases based on track geometry: same M4 track (18 nm projected), parallel tracks not aligned (27 nm projected), and parallel tracks aligned (18 nm projected). The deck computes separate NEC and WEC masks (v3_nec_mask = sized by 5 nm; v3_wec_mask = via body plus 5 nm M4 end-cap extension) to apply these thresholds. Repairs that move V3 instances in y without changing x maintain track alignment and keep violations in the same sub-case. The x-axis move in trial:i03.ug.leaf_0001.00 could shift a via between the "not aligned" and "aligned" sub-cases, changing the applicable threshold from 27 nm to 18 nm or vice versa, which is consistent with the 1 new in-crop violation that trial introduced.

V3.S.2 and V3.S.3 govern corner-to-corner (euclidean, not projection-filtered) spacings: 23 nm between two WEC vias and 30 nm between two NEC vias respectively. V3.S.4 governs the mixed case at 27 nm. These rules fire only on violations that are in the euclidean set but not in the projection set (via the `not_interacting` filter), meaning they target diagonal neighbors. No trial explicitly targeted a diagonal spacing violation, but any repair that moves a V3 instance diagonally relative to a neighbor must respect the 23 nm (WEC–WEC), 27 nm (WEC–NEC), or 30 nm (NEC–NEC) corner clearances.