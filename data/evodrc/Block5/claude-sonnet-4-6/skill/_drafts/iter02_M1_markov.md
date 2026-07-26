Now I have the full context. Let me produce the updated knowledge body incorporating both iteration 2 records.

## Observed Operation Patterns (Iterations 1–2)

All six trials recorded in iteration 1 and both trials recorded in iteration 2 share the same base design state (`c479bb9...`) and were evaluated through the `unit_gate` channel for `Block5`. All eight trials received `decision: gated_in` with `conn_preserved: true`. The `target` field is `null` in every record across both iterations; none of these trials is a targeted rule-repair.

The two iteration 2 trials diverge in their violation counts. trial:i02.ug.leaf_0001.00 introduced zero new violations (clean). trial:i02.ug.leaf_0003.02 introduced 7 new in-crop violations (4 M1.A.1, 3 V1.M1.EN.1) and was still admitted because `conn_preserved: true` overrides the new-violation penalty in this channel's gating logic. This is the first measured instance of a trial being gated in while introducing new M1 violations.

## Safe Operation Classes Confirmed

**Instance moves (X-axis, small deltas)** remain the dominant clean operation across both iterations. A single +36 dbu X-axis instance move on i0012 in leaf_0001 produced no new violations (trial:i02.ug.leaf_0001.00), consistent with the iteration 1 evidence (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05, trial:i01.ug.Block5_union_row6.01). The clean range for single-instance X moves spans at least +4 dbu to +112 dbu (trial:i01.ug.leaf_0006.05, trial:i01.ug.leaf_0005.04).

**X-axis polygon resizes (positive, outward)** paired with a co-located instance move were clean in iteration 1. Resizes of +256 dbu and +328 dbu on the X axis alongside two +108 dbu instance moves introduced no violations (trial:i01.ug.Block5_union_row6.01). The only confirmed clean resize pattern includes a co-located instance move; resize-only changes remain untested.

**Y-axis polygon resizes (negative, inward) are not confirmed clean.** The only Y-axis resize recorded, -64 dbu on polygon p893, appeared in a three-operation compound that produced 4 M1.A.1 and 3 V1.M1.EN.1 violations (trial:i02.ug.leaf_0003.02). Whether the area and enclosure violations are attributable specifically to the Y-axis shrink, the accompanying X-axis polygon move (+8 dbu on p910), or their interaction cannot be disaggregated from this single trial; but the compound containing the Y-axis inward resize is the only compound in the measured set that produced violations.

## Layer Interaction Notes

Six of eight trials report `touched_layers: ["M1","M2","V1"]`. trial:i02.ug.leaf_0003.02 additionally touches M3. The M3 contact did not suppress the M1 violations; the 4 M1.A.1 and 3 V1.M1.EN.1 violations were reported in-crop despite M3 being in scope (trial:i02.ug.leaf_0003.02).

All iteration 1 trials and trial:i02.ug.leaf_0001.00 passed the full inter-layer enclosure checks V0.M1.EN.1 (5 nm minimum enclosure of V0 by M1 on two opposite sides) and V1.M1.EN.1 (5 nm and 2 nm minimum enclosure of V1 by M1), as well as V0.M1.AUX.3 (V0 width must exactly match the perpendicular M1 width). This confirms that X-only instance moves across the measured delta range do not break via enclosure or width-matching constraints on M1 (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.Block5_union_row6.01, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05, trial:i02.ug.leaf_0001.00).

trial:i02.ug.leaf_0003.02 also records an `assemble_drops` entry: a Y-axis resize_via_shape (-88 dbu) on M5 layer cell VIA_VIA45_1_2_58_58 was dropped from the `cu_pool` during assembly. This drop is at the M5/via level and is not an M1 operation, but it indicates that compound trials can carry cross-layer side effects that are silently removed before DRC runs; the recorded M1 violations are the post-drop result.

## Rule-Specific Guidance

**M1.A.1:** A compound containing a Y-axis inward resize of -64 dbu on an M1 polygon produced 4 M1.A.1 violations (trial:i02.ug.leaf_0003.02). This is the first measured evidence that inward Y-axis resizes can drive M1 shapes below the 504 nm² minimum area threshold. Outward X-axis resizes up to +328 dbu remained clean (trial:i01.ug.Block5_union_row6.01). Do not apply negative (inward) Y-axis resizes to M1 polygons without verifying that the post-resize area of each affected shape is >= 504 nm²; the -64 dbu case in the measured set was not safe under this check.

**V1.M1.EN.1:** The same compound that violated M1.A.1 also produced 3 V1.M1.EN.1 violations (trial:i02.ug.leaf_0003.02). V1.M1.EN.1 requires M1 to enclose V1 by at least 5 nm on one axis and 2 nm on the perpendicular axis. An inward Y-axis shrink of M1 directly reduces the vertical enclosure margin of any V1 vias landing on the affected polygon. Do not apply negative Y-axis resizes to M1 polygons that carry V1 vias without verifying that the post-resize enclosure satisfies the 5 nm / 2 nm requirement on both axis pairs.

**M1.W.1 / M1.A.1 (outward resizes):** Positive (outward) X-axis resize operations as large as +328 dbu on a single polygon edge did not shrink any M1 shape below the 18 nm minimum width or 504 nm² minimum area threshold (trial:i01.ug.Block5_union_row6.01). When resizing M1 polygons outward on a single axis, the evidence shows these are safe in the observed range; verify that the perpendicular dimension remains >= 18 nm and area >= 504 nm² when applying negative-delta resizes.

**M1.S.1 through M1.S.6:** No trial across either iteration introduced a spacing violation. Instance moves in the +4 to +112 dbu X range and polygon resizes up to +328 dbu on X did not push any M1 edge into violation of the side-to-side (18 nm, M1.S.1), tip-to-side (25 nm, M1.S.2), wide-tip-to-tip (27 nm, M1.S.3), or corner-to-corner (20 nm, M1.S.6) spacing rules (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.Block5_union_row6.01, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05, trial:i02.ug.leaf_0001.00, trial:i02.ug.leaf_0003.02). M1.S.4 and M1.S.5 are stub rules (empty result set by construction in the deck); no action is needed for those checks.

**M1.R.0:** No redundant-island flag was raised by any trial across both iterations. Operations in the confirmed set move or resize existing connected M1 shapes rather than creating isolated single-via islands (trial:i01.ug.Block5_union_row3.00 through trial:i02.ug.leaf_0003.02).

**V0.M1.EN.1 / V0.M1.AUX.3:** No trial across either iteration raised a V0 enclosure or width-match violation. X-axis instance moves and X-axis polygon resizes leave the V0/M1 enclosure geometry intact in the observed range (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.Block5_union_row6.01, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05, trial:i02.ug.leaf_0001.00, trial:i02.ug.leaf_0003.02). The Y-axis resize in trial:i02.ug.leaf_0003.02 did not trigger V0.M1.EN.1 or V0.M1.AUX.3 flags; only V1.M1.EN.1 was violated, indicating V0 vias were not present on the affected polygon or their enclosure margins were not compromised by the -64 dbu Y shrink.

**GEOMETRY.NONORTHOGONAL:** All operations across both iterations were axis-aligned. No nonorthogonal M1 edges were introduced in any trial. Maintain strict X/Y axis alignment for all M1 move and resize operations to avoid GEOMETRY.NONORTHOGONAL flags (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.Block5_union_row6.01, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05, trial:i02.ug.leaf_0001.00, trial:i02.ug.leaf_0003.02).

## Gating Behavior Under New Violations

trial:i02.ug.leaf_0003.02 establishes that the `unit_gate` channel admits trials with new in-crop violations when `conn_preserved: true`. The 7 new violations (4 M1.A.1, 3 V1.M1.EN.1) did not prevent gating. The `debt` field records `new_out_of_crop_bboxes: []` and `new_out_of_crop_by_rule: {}`, confirming zero out-of-crop spread; only in-crop violations were introduced. This means compound operations that preserve connectivity and contain violations only within the crop boundary will be admitted, but they leave behind unresolved M1 violations that accumulate as design debt.

## Coverage Gaps

No trial across either iteration targeted a specific M1 DRC rule; all `target` fields are `null`. The iteration 2 records provide the first measured evidence of violation-generating operations (trial:i02.ug.leaf_0003.02), but they do not establish which operations resolve those violations when violations are already present. Specifically, there is no measured evidence for: (a) repair moves that correct existing M1.A.1 area violations, (b) repair moves that correct existing V1.M1.EN.1 enclosure violations, (c) the effect of positive Y-axis resizes on M1 area or V1 enclosure, or (d) the effect of polygon moves without a co-located instance move. These remain untested in the recorded history.