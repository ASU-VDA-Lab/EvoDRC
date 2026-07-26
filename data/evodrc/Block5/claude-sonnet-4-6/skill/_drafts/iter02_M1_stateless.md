## M1 Violation Fingerprints

### M1.A.1 — Minimum area 504 nm²

The only trial to produce new M1.A.1 violations is trial:i02.ug.leaf_0003.02, which introduced 4 new in-crop M1.A.1 errors. That trial combined a y-axis resize of -64 dbu on polygon p893 with an x-axis polygon move of +8 dbu on polygon p910. The shrink along the y-axis directly reduces polygon area; a -64 dbu y-delta is sufficient to push at least 4 M1 shapes below the 504 nm² floor. No trial that used only move_instance operations — trial:i01.ug.Block5_union_row3.00, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05, trial:i02.ug.leaf_0001.00 — produced any M1.A.1 violations.

Avoid negative y-axis resize operations on M1 polygons unless the resulting height is verified to keep each affected shape above 504 nm². The co-occurrence of M1.A.1 with V1.M1.EN.1 violations in trial:i02.ug.leaf_0003.02 indicates that the same y-shrink that reduces area simultaneously erodes M1 enclosure of V1, so these two rules fail together under y-axis compression.

### V1.M1.EN.1 — M1 enclosure of V1 (5 nm & 2 nm on opposite sides)

trial:i02.ug.leaf_0003.02 introduced 3 new in-crop V1.M1.EN.1 violations alongside the 4 M1.A.1 violations. The rule requires M1 to enclose V1 by at least 5 nm on one pair of opposite sides and at least 2 nm on the other pair. A y-axis resize of -64 dbu on p893 pulls an M1 edge toward an enclosed V1, reducing the enclosure margin. The concurrent +8 dbu x-move on p910 can shift an M1 polygon laterally relative to V1 centroid, reducing horizontal enclosure on one side. Together these two sub-operations are sufficient to generate V1.M1.EN.1 failures in at least 3 locations.

All six move_instance-only trials produced zero V1.M1.EN.1 violations, confirming that rigid instance translation preserves the M1-to-V1 enclosure relationship intact. Mixed operations that alter polygon shape or position independently of instance translation are the source of enclosure failures observed in trial:i02.ug.leaf_0003.02.

### V0.M1.EN.1 — M1 enclosure of V0 (5 nm & 5 nm or 5 nm & 0 nm)

No trial in the recorded history produced new V0.M1.EN.1 violations. The enclosure geometry for V0 was preserved across all eight trials, including the mixed-op trial:i02.ug.leaf_0003.02. This distinguishes V0 enclosure behavior from V1 enclosure under the same operations.

### V0.M1.AUX.3 — V0 width must match M1 width perpendicular to M1 length

No trial produced V0.M1.AUX.3 violations. The move_instance operations that dominate the history preserve the M1/V0 width relationship. The x-axis resize operations in trial:i01.ug.Block5_union_row6.01 (polygon p955, +256 dbu; polygon p971, +328 dbu) also avoided triggering this rule, indicating that the expanded M1 widths remained consistent with the enclosed V0 widths in that crop.

### M1.W.1 — Minimum M1 width 18 nm

No trial produced M1.W.1 violations. The y-axis shrink of -64 dbu in trial:i02.ug.leaf_0003.02 did not narrow M1 widths below 18 nm in the affected shapes, though it was sufficient to violate M1.A.1, which constrains the area product of width and length.

### M1.S.1 / M1.S.2 / M1.S.3 / M1.S.4 / M1.S.5 / M1.S.6 — Spacing rules

No M1 spacing rule produced new violations in any trial. The x-axis move operations — including the +8 dbu polygon move on p910 in trial:i02.ug.leaf_0003.02 and the instance moves ranging from +4 dbu (trial:i01.ug.leaf_0006.05) to +112 dbu (trial:i01.ug.leaf_0005.04) and instance pairs moving in opposite directions (trial:i01.ug.leaf_0002.03, ±36 dbu) — did not close any M1-to-M1 spacing below any threshold. This holds for side-to-side (M1.S.1), tip-to-side (M1.S.2), tip-to-tip between wide-tip edges (M1.S.3), narrow tip-to-tip (M1.S.4 and M1.S.5), and corner-to-corner (M1.S.6) checks.

### M1.R.0 — Redundant M1 island

No trial produced M1.R.0 violations. Existing single-via M1 islands, if any, are not located in the large-empty-M1 regions that would trigger the rule in the crop windows used across all eight trials.

## Operation Patterns and Violation Risk

Move-instance-only operations produced zero new M1 violations across six trials (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05, trial:i02.ug.leaf_0001.00). Instance moves ranging from +4 dbu to +112 dbu in x, including a pair of opposing moves (±36 dbu), all resulted in `n_new_in_crop: 0` for M1.

Mixed operations combining move_instance, polygon resize, and polygon move in a single trial produced new M1 violations. trial:i02.ug.leaf_0003.02 (3 ops: 1 move_instance + 1 y-resize + 1 x-move-polygon) yielded 7 new in-crop violations (M1.A.1: 4, V1.M1.EN.1: 3).

The x-axis resize operations in trial:i01.ug.Block5_union_row6.01 (+256 dbu on p955, +328 dbu on p971) avoided M1 violations. Expansion of M1 along x does not compress area or enclosure margins, explaining the clean outcome versus the y-axis shrink in trial:i02.ug.leaf_0003.02.

## Gating Behavior Observed

All eight trials received a `gated_in` decision. trial:i02.ug.leaf_0003.02 was accepted with 7 new in-crop violations because `conn_preserved: true` and `n_new_out_of_crop: 0`. The `debt.new_out_of_crop_by_rule` field was empty for that trial. This confirms that the gating criterion for M1 trials with `conn_preserved` allows new in-crop violations when no violations appear outside the crop window.

Trials from iter 1 operated on design state `ef66d47d...`; trials from iter 2 (trial:i02.ug.leaf_0001.00, trial:i02.ug.leaf_0003.02) operated on design state `c479bb91...`, indicating a design-state transition between iterations. The new M1.A.1 and V1.M1.EN.1 violations in trial:i02.ug.leaf_0003.02 arose in the iter-2 design state, not in any iter-1 trial, even though both iter-1 and iter-2 included resize operations (trial:i01.ug.Block5_union_row6.01 used x-axis resizes cleanly). The difference is axis direction: x-axis expansion is safe; y-axis compression is the violation source seen in trial:i02.ug.leaf_0003.02.