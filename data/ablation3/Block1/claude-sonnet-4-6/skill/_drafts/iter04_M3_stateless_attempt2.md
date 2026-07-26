## Spacing Rules

**M3.S.1** enforces 18 nm minimum side-to-side spacing between edges longer than 36 nm. **M3.S.2** enforces 25 nm tip-to-side spacing when one edge is ≤ 36 nm and the other is > 36 nm. **M3.S.3** enforces 27 nm tip-to-tip spacing when both edges are in the 24–36 nm range. **M3.S.4** enforces 31 nm tip-to-tip spacing when both edges are < 24 nm. **M3.S.5** enforces 31 nm tip-to-tip spacing when one edge is in the 24–36 nm range and the other is < 24 nm. **M3.S.6** enforces 20 nm corner-to-corner spacing using Euclidean measurement, independently of projection-based checks.

Extending the high end of M3 polygons along the x-axis by values ranging from 128 to 192 dbu, and along the y-axis by 9 dbu, was accepted with zero new in-crop violations (trial:i04.ug.whole_design.00). Moving M3 polygons along both axes produced zero new M3-layer violations (trial:i02.ug.whole_design.00). These results confirm that end-resizing and repositioning are viable repair strategies when the adjusted geometry satisfies the applicable spacing rule thresholds.

## Width and Area Rules

**M3.W.1** requires a minimum width of 18 nm. **M3.A.1** requires a minimum area of 504 nm². Any resize that contracts a polygon's width or shortens its run length risks triggering one or both of these rules; end-extensions accepted in trial:i04.ug.whole_design.00 increased polygon length without narrowing width, which kept both rules satisfied.

## Via Enclosure and Auxiliary Rules

**V2.M3.EN.2** requires M3 to enclose V2 by at least 5 nm on two opposite sides (either 5 & 5 nm or 5 & 0 nm in projection). **V2.M3.AUX.2** requires V2 to be exactly the same width as M3 in the direction perpendicular to the M3 run; V2 must have at least two edges coincident with M3 edges on that axis to satisfy the deck's interacting-coincident-edge test.

Shrinking M3 in the y-axis by 40 dbu inside cell VIA_VIA23_1_3_36_36 left the total violation count unchanged at 122 and was rejected (trial:i04.cu.def:VIA_VIA23_1_3_36_36.00). Do not apply negative y-axis resize_via_shape operations to M3 shapes inside via cells when the enclosure budget on that axis is already at or near the 5 nm minimum: trial:i04.cu.def:VIA_VIA23_1_3_36_36.00 demonstrates this produces no net reduction in V2.M3 violations.

**V3.M3.EN.1** requires M3 to enclose V3 by at least 5 nm on at least two opposite sides (either the left/right pair or the top/bottom pair). The small y-axis end-extensions accepted in trial:i04.ug.whole_design.00 (+9 dbu on polygons p1543 and p1458) are consistent with increasing M3 run length to satisfy V3.M3.EN.1 enclosure on the top/bottom pair.

## Geometry

The NONORTHOGONAL rule applies to M3: all M3 edges must be strictly horizontal or vertical. Moves and end-resizes recorded in trial:i02.ug.whole_design.00 and trial:i04.ug.whole_design.00 involved only axis-aligned deltas and produced no NONORTHOGONAL violations, confirming that operations restricted to x-axis or y-axis deltas preserve orthogonality.

## Repair Operation Outcomes

The cu_pool channel rejected the resize_via_shape on VIA_VIA23_1_3_36_36 M3 before assembly because the delta was net positive (trial:i04.cu.def:VIA_VIA23_1_3_36_36.00); the unit_gate channel's assembled plan dropped that op and the remaining six end-resizes on M3/M2/M4 polygons were accepted with zero new in-crop violations (trial:i04.ug.whole_design.00). This confirms that assemble_drops from cu_pool rejection do not prevent the parent unit_gate trial from being gated in, provided the retained ops themselves introduce no new violations.