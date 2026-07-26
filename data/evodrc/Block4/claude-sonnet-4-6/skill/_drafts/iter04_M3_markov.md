## M3 Via-Cell Shape Shrinks (Y-Axis)

Shrinking the M3 enclosure shape inside via-cell definitions on the y-axis was rejected by the cu_pool channel in both measured attempts. A -40 dbu y-resize on the M3 shape in VIA_VIA23_1_3_36_36 produced delta_total = 0 (no net improvement) and was marked `rejected_net_positive` (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). A -64 dbu y-resize on the M3 shape in VIA_VIA34_1_2_58_52, taken together with concurrent V3 shrinks of -24 dbu on both V3 shapes in that cell, produced delta_total = +34 — a net increase in violation count — and was likewise rejected (trial:i01.cu.def:VIA_VIA34_1_2_58_52.01). Do not apply `resize_via_shape` y-shrinks to M3 in either VIA_VIA23 or VIA_VIA34 cell types when operating through the cu_pool channel; both measured outcomes worsened or did not improve the DRC count.

The assemble_drops mechanism correctly excluded all four rejected via-cell ops (the M3 resize in VIA_VIA23_1_3_36_36 and the M3 + both V3 resizes in VIA_VIA34_1_2_58_52) when assembling the unit_gate trial. The assembled unit_gate trial that omitted those drops was accepted as `gated_in` (trial:i01.ug.leaf_0026.12). This confirms that the assemble_drops filter on `cu_pool:rejected_net_positive` is the correct gate before escalating via-cell ops to the unit channel.

## M3 Polygon Y-Axis Bulk Shrink in Unit Gate Context

A bulk y-axis resize of -64 dbu applied simultaneously to five M3 polygons (p1406 through p1410) in the unit_gate channel passed with decision `gated_in`, reason `conn_preserved` (trial:i01.ug.leaf_0026.12). The two new in-crop violations introduced by this move were M1.A.1 and V1.M1.EN.1 — neither is an M3 rule — and zero new out-of-crop violations were created. A -64 dbu y-shrink on M3 bulk shapes in the unit_gate channel is therefore compatible with M3 DRC compliance in this context, though it can generate downstream M1 and V1 area/enclosure violations that must be tracked separately.

## M3 Polygon X-Axis Moves and End Resizes Combined with Instance Moves

Moving a single M3 polygon on the x-axis, coordinated with multi-instance repositioning, is accepted by the unit_gate channel without introducing M3-rule violations. Two measured cases confirm this pattern:

A +32 dbu x-move of M3 polygon p1341 (group m5_align), combined with ten instance moves spanning M3, M4, M5, V3, and V4 (instances i0239, i0223, i0141, i0150, i0138, i0237, i0214, i0103, i0104, i0134 with x-deltas of +32 or 0 and y-deltas ranging from -24 to +72 dbu), was accepted as `gated_in`, reason `conn_preserved` (trial:i04.ug.leaf_0002.01). Two new in-crop violations were introduced and zero new out-of-crop violations; neither new violation was an M3 rule.

Resizing the high-x end of a single M3 polygon (p1410, group_D) by -8 dbu on the x-axis, combined with a -8 dbu x-move of instance i0238 and a -36 dbu x-move of instance i0213, was accepted as `gated_in`, reason `conn_preserved` (trial:i02.ug.leaf_0003.02). Touched layers were M1, M2, M3, V1, and V2. Two new in-crop violations were introduced but neither was an M3 rule.

In both measured cases, x-axis M3 polygon displacement or end-trimming paired with coordinated instance repositioning does not trigger M3 width, spacing, or enclosure violations. New in-crop violations in such ops fall on other layers (M1, V1, or none observed on M3) and must be tracked in those layers' knowledge records.

## V2.M3.EN.2 and V2.M3.AUX.2 Interaction with Via-Cell Shrinks

The rejected via-cell ops in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 touched layers M2, M3, and V2. Rules V2.M3.EN.2 (minimum two-sided enclosure of V2 by M3 ≥ 5 nm on opposite sides) and V2.M3.AUX.2 (V2 width must match M3 width perpendicular to M3 length) are both sensitive to y-axis M3 shrinks over V2 vias. The cu_pool rejection at delta_total = 0 for a -40 dbu y-shrink on the M3 shape in VIA_VIA23_1_3_36_36 (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00) shows that such a shrink neither fixes nor worsens the M3/V2 enclosure or AUX situation in net terms, making it a zero-benefit operation not worth applying. Avoid y-shrinks on M3 via-enclosure shapes in VIA_VIA23 cells when the expected delta is zero.

## V3.M3.EN.1 Interaction with Via-Cell Shrinks

The rejected ops in trial:i01.cu.def:VIA_VIA34_1_2_58_52.01 touched M3, M4, and V3. Rule V3.M3.EN.1 requires M3 to enclose V3 by ≥ 5 nm on at least two opposite sides. A -64 dbu y-shrink of the M3 shape in VIA_VIA34_1_2_58_52 combined with -24 dbu y-shrinks of both V3 shapes produced a net +34 violation increase (trial:i01.cu.def:VIA_VIA34_1_2_58_52.01). Do not shrink M3 in the y-direction in VIA_VIA34 cells; even when accompanied by proportional V3 shrinks, this combination increases total violation count rather than reducing it.