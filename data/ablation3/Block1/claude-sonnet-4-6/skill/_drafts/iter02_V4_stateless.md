## Repair Strategy Summary

Two trials touch V4 in this iteration window. Trial `i01.cu.def:VIA_VIA45_1_2_58_58.00` operated directly on the via cell by resizing M5 along the y-axis (−88 dbu), reducing total violations by 52 across the whole design with connectivity preserved. Trial `i02.ug.whole_design.00` applied 57 move-instance and polygon-move operations across M3–M6/V3–V5 and was gated in by the unit gate with no net new in-crop V4 violations.

## Enclosure and Containment (V4.AUX.1, V4.M4.EN.1, V4.M5.EN.2)

V4 must be fully inside the intersection of M4 and M5 (V4.AUX.1). Violations of V4.AUX.1 arise when M4 or M5 boundaries do not cover the via. In trial `i01.cu.def:VIA_VIA45_1_2_58_58.00`, shrinking M5 along the y-axis by 88 dbu on shape_index 0 of cell VIA_VIA45_1_2_58_58 was the applied fix and produced a net −52 violation reduction. This confirms that resizing M5 within the via cell—rather than moving the V4 shape itself—is a viable and effective path for enclosure-class violations when the via cell is the DRC target.

V4.M4.EN.1 requires M4 to enclose V4 by at least 11 nm on at least two opposite sides. V4.M5.EN.2 requires M5 to enclose V4 by at least 11 nm on two opposite sides. Because the M5 resize in trial `i01.cu.def:VIA_VIA45_1_2_58_58.00` was applied along y (−88 dbu) and cleared violations, the prior M5 extent was excessive and creating a geometric conflict rather than an under-enclosure problem. Shrinking M5 back toward the V4 boundary resolved the enclosure geometry without violating the 11 nm minimum on the remaining sides.

Never resize M5 in a direction that would reduce the two-opposite-side enclosure below 11 nm. The safe direction established by trial `i01.cu.def:VIA_VIA45_1_2_58_58.00` is a y-axis shrink on the cell-level M5 shape; the result preserved connectivity and reduced violations, indicating the enclosure constraint on the surviving sides remained satisfied.

## Width Matching (V4.M5.AUX.2)

V4.M5.AUX.2 requires that the V4 shape exactly matches M5 width in the direction perpendicular to M5's length. Any M5 resize that changes the perpendicular dimension must be accompanied by a matching V4 resize or the rule fires. Trial `i01.cu.def:VIA_VIA45_1_2_58_58.00` resized M5 along y; M5 and V4 are both listed in touched_layers, which is consistent with the harness adjusting V4 to maintain exact perpendicular width matching after the M5 y-shrink. Always treat M5 y-resizes in via cells as also touching the V4 perpendicular-width constraint.

## Spacing (V4.S.1, V4.S.2, V4.S.3)

All three spacing rules share a 33 nm threshold. V4.S.1 and V4.S.2 use projection-based spacing; V4.S.3 uses Euclidean (corner-to-corner). No spacing violations on V4 were directly attributed in either trial's per-rule breakdown. The 57-operation move-instance pass in trial `i02.ug.whole_design.00` touched V4 as part of a multi-layer shift and introduced zero new in-crop V4 violations, confirming that grid-aligned instance moves (multiples of 8 dbu observed: 16, 24, 32, 48, 64, 72, 96 dbu) do not degrade V4 projection spacing when the shift is uniform across neighboring instances on the same net.

Do not move a single via instance without also moving adjacent instances on the same M4/M5 segment if projection spacing is tight. Trial `i02.ug.whole_design.00` moved clusters of instances together (57 ops, coordinated x/y deltas across many inst_ids), which preserved V4.S.1 and V4.S.2.

## Minimum Width (V4.W.1)

V4.W.1 sets a 24 nm minimum width along the M5 length direction. No V4.W.1 violations appeared in either trial's output records. The via cell VIA_VIA45_1_2_58_58 has a nominal shape that satisfies 24 nm width; the M5 y-shrink in trial `i01.cu.def:VIA_VIA45_1_2_58_58.00` affected the perpendicular dimension, not the length direction, leaving V4.W.1 unaffected.

## Operation Scope and Gating

The cu_pool channel (trial `i01.cu.def:VIA_VIA45_1_2_58_58.00`) targets a single via cell definition and applies one resize op; it is the appropriate channel when a specific via cell is the DRC source. The unit_gate channel (trial `i02.ug.whole_design.00`) applies broad instance-move sweeps across the whole design; V4 is incidentally touched but is not the primary target. Gating logic accepted the unit_gate trial on the basis of conn_preserved and no new out-of-crop violations, despite introducing 48 new V1.M2.AUX.2 in-crop violations on a different layer. V4 itself incurred no new violations from the unit_gate pass.

## Non-Orthogonal Geometry

All V4 shapes must have only orthogonal edges (0° and 90°). No GEOMETRY.NONORTHOGONAL violations on V4 appear in either trial's records. Both applied operations—y-axis resize and axis-aligned instance moves—are inherently orthogonal. Maintain strictly rectilinear V4 shapes in all repair operations.