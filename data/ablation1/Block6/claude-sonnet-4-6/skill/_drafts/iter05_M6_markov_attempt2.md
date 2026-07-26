## V5.M6.AUX.2 Violations

**Fix by Y-axis resize of V5 shapes, not X-axis repositioning.** Rule V5.M6.AUX.2 requires V5 to exactly match M6's width in the direction perpendicular to M6 length. In trial:i01.cu.def:VIA_VIA56_2_2_66_58.02, resizing all four V5 shapes by +248 dbu on the Y axis (group `v5_m6_aux2_fix`) removed 32 total violations (−16 in leaf_0019, −16 in leaf_0020) and was applied. X-axis move/resize of the same V5 shapes in trial:i01.cu.def:VIA_VIA56_2_2_66_58.01 (±116 dbu moves, +320 dbu resizes) reduced violations by only 16 total and lost the tournament, indicating that lateral repositioning of V5 is a weaker repair path for this rule class.

When a via cell touching both M5 and M6 generates V5.M6.AUX.2 violations, apply Y-axis resizes to the V5 shapes rather than X-axis moves. Trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 demonstrates that symmetric Y-axis expansion of all shapes in the via cell (all four shapes receiving the same +248 dbu delta) achieves the full enclosure correction without disrupting connectivity. Trial:i01.cu.def:VIA_VIA56_2_2_66_58.01 confirms that X-axis adjustments to V5 shapes in the same cell are a competing but inferior repair path for violations scored in the M6 window.

## Via Cell Repair Scope

Both trials operated on `VIA_VIA56_2_2_66_58` and touched layers M5, M6, and V5 together. The applied fix (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02) preserved connectivity (`conn_preserved: true`) while achieving the larger violation delta. Do not treat M6 violation windows in this locus as requiring direct M6 shape edits; the root cause was V5 undersize relative to M6 width, and V5 Y-axis resize is the effective repair.

## V5.M6.EN.2 Interaction

V5.M6.EN.2 requires 11 nm enclosure of V5 by M6 on two opposite sides. The Y-axis expansion of V5 by +248 dbu applied in trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 was the dominant fix; no separate M6 resizing was needed to satisfy enclosure in this case. When both V5.M6.AUX.2 and V5.M6.EN.2 are failing together in the same via cell, prioritize the AUX.2 Y-axis resize, as trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 shows that single action yielded the maximum per-window delta (−16 each window) and was tournament-winning.

## M6 Polygon Moves in unit_gate Channel

Do not issue M6 Y-axis polygon moves in the unit_gate channel when the same repair window also requires large instance displacements. Trial:i05.ug.leaf_0003.01 applied M6 Y-axis polygon moves (p2107 +32 dbu, p2106 −16 dbu, group `m6_fix`) alongside 16 instance moves in the unit_gate channel and was gated_in rather than applied, introducing 68 new in-crop violations (M1.A.1: +27, V1.M1.EN.1: +39, M4.W.5: +2) with zero net reduction in the M6 window. The combination of direct polygon moves on M6 and simultaneous large instance displacements produces cascading violations on layers far from M6 (M1, V1, M4), making this repair path net-negative for the design window.

## M5 X-axis Moves and Via Shape Resize in cu_pool Channel

X-axis moves of M5 polygons combined with X-axis resize of M5 via shapes in the cu_pool channel are an effective narrow-delta repair path. Trial:i05.cu.def:VIA_VIA45_1_2_58_58.00 moved p1683 by +32 dbu and p1682 by −16 dbu on the X axis, and resized the M5 shape at index 0 in both VIA_VIA45_1_2_58_58 and VIA_VIA56_2_2_66_58 by −64 dbu on X; this was applied with `conn_preserved: true` and achieved a delta of −2 (all improvement in leaf_0003, zero change in leaf_0002). The touched layers were M4, M5, M6, V4, and V5, confirming that X-axis M5 correction in the via cell propagates through the via stack without introducing M6-rule violations at the window boundary.