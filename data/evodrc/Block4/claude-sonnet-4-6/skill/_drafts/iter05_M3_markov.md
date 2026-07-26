Reading the new record and updating the knowledge body now.

The new record (trial:i05.cu.def:VIA_VIA23_1_3_36_36.00) is an x-axis V2 reshape in VIA_VIA23_1_3_36_36 accepted with delta_total = -51. No existing claim is contradicted — prior rejected trials targeted y-axis M3 shrinks, not x-axis V2 ops. I'll add a new section capturing the x-axis V2 result and leave existing sections intact.

## M3 Via-Cell Shape Shrinks (Y-Axis)

Shrinking the M3 enclosure shape inside via-cell definitions on the y-axis was rejected by the cu_pool channel in both measured attempts. A -40 dbu y-resize on the M3 shape in VIA_VIA23_1_3_36_36 produced delta_total = 0 (no net improvement) and was marked `rejected_net_positive` (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). A -64 dbu y-resize on the M3 shape in VIA_VIA34_1_2_58_52, taken together with concurrent V3 shrinks of -24 dbu on both V3 shapes in that cell, produced delta_total = +34 — a net increase in violation count — and was likewise rejected (trial:i01.cu.def:VIA_VIA34_1_2_58_52.01). Do not apply `resize_via_shape` y-shrinks to M3 in either VIA_VIA23 or VIA_VIA34 cell types when operating through the cu_pool channel; both measured outcomes worsened or did not improve the DRC count (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, trial:i01.cu.def:VIA_VIA34_1_2_58_52.01).

The assemble_drops mechanism correctly excluded all four rejected via-cell ops (the M3 resize in VIA_VIA23_1_3_36_36 and the M3 + both V3 resizes in VIA_VIA34_1_2_58_52) when assembling the unit_gate trial. The assembled unit_gate trial that omitted those drops was accepted as `gated_in` (trial:i01.ug.leaf_0026.12). This confirms that the assemble_drops filter on `cu_pool:rejected_net_positive` is the correct gate before escalating via-cell ops to the unit channel (trial:i01.ug.leaf_0026.12).

## X-Axis V2 Reshape in VIA_VIA23_1_3_36_36

A five-operation x-axis V2 reshape bundle targeting VIA_VIA23_1_3_36_36 was applied by the cu_pool channel with delta_total = -51 and conn_preserved = true (trial:i05.cu.def:VIA_VIA23_1_3_36_36.00). The five ops were: move V2 shape 0 by -144 dbu on x; resize V2 shapes 0, 1, and 2 each by +288 dbu on x; move V2 shape 2 by +144 dbu on x. Touched layers were M2, M3, and V2; M3 was passively affected, not directly operated on. Violation reduction was distributed across two windows: leaf_0001 (-36, from 74 to 38) and leaf_0002 (-15, from 29 to 14) (trial:i05.cu.def:VIA_VIA23_1_3_36_36.00).

The x-axis V2 reshape in VIA_VIA23_1_3_36_36 succeeded where the y-axis M3 shrink in the same cell type failed. The productive repair direction in VIA_VIA23_1_3_36_36 is x-axis repositioning and widening of V2 shapes, not y-axis reduction of the M3 enclosure shape (trial:i05.cu.def:VIA_VIA23_1_3_36_36.00 vs. trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

## M3 Polygon Y-Axis Bulk Shrink in Unit Gate Context

A bulk y-axis resize of -64 dbu applied simultaneously to five M3 polygons (p1406 through p1410) in the unit_gate channel passed with decision `gated_in`, reason `conn_preserved` (trial:i01.ug.leaf_0026.12). The two new in-crop violations introduced were M1.A.1 and V1.M1.EN.1 — neither is an M3 rule — and zero new out-of-crop violations were created. A -64 dbu y-shrink on M3 bulk shapes in the unit_gate channel produced zero new M3-rule violations in this context (trial:i01.ug.leaf_0026.12).

## M3 End Resize (X-Axis) Combined with Instance Moves

Resizing the high-x end of a single M3 polygon (p1410, group_D) by -8 dbu on the x-axis, combined with a -8 dbu x-move of instance i0238 and a -36 dbu x-move of instance i0213, was accepted as `gated_in`, reason `conn_preserved` (trial:i02.ug.leaf_0003.02). Touched layers were M1, M2, M3, V1, and V2. Two new in-crop violations were introduced but neither was an M3 rule. A small end-trim of -8 dbu on M3 in the x-direction paired with coordinated instance repositioning does not, on its own, trigger M3 width, spacing, or enclosure violations in the measured case (trial:i02.ug.leaf_0003.02).

## M3 Polygon X-Axis Translation in Unit Gate Context (M5-Align Group)

Moving M3 polygon p1341 by +32 dbu on the x-axis, as part of a coordinated m5_align group that also repositioned ten instances with x-offsets of +32 dbu and y-offsets ranging from -24 to +72 dbu, was accepted as `gated_in`, reason `conn_preserved` (trial:i04.ug.leaf_0002.01). Touched layers were M3, M4, M5, V3, and V4. Two new in-crop violations were introduced and zero new out-of-crop violations were created. A +32 dbu x-axis translation of an M3 polygon paired with coordinated multi-instance repositioning produced zero new M3-rule violations in the measured case (trial:i04.ug.leaf_0002.01).

## V2.M3.EN.2 and V2.M3.AUX.2 Interaction with Via-Cell Ops

Rules V2.M3.EN.2 (minimum two-sided enclosure of V2 by M3 ≥ 5 nm on opposite sides) and V2.M3.AUX.2 (V2 width must match M3 width perpendicular to M3 length) are both sensitive to changes in the M3/V2 relationship inside VIA_VIA23_1_3_36_36 cells.

A y-axis M3 shrink of -40 dbu in VIA_VIA23_1_3_36_36 produced delta_total = 0 — zero net improvement — confirming it is a zero-benefit operation for these rules (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

An x-axis V2 reshape bundle (move + resize totaling net +144 dbu on x for shapes 0 and 2, +288 dbu resize for shape 1) in the same cell produced delta_total = -51, applied by cu_pool with conn_preserved (trial:i05.cu.def:VIA_VIA23_1_3_36_36.00). X-axis V2 repositioning and widening in VIA_VIA23_1_3_36_36 is an effective repair path; y-axis M3 shrinking in the same cell is not (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, trial:i05.cu.def:VIA_VIA23_1_3_36_36.00).

## V3.M3.EN.1 Interaction with Via-Cell Shrinks

The rejected ops in trial:i01.cu.def:VIA_VIA34_1_2_58_52.01 touched M3, M4, and V3. Rule V3.M3.EN.1 requires M3 to enclose V3 by ≥ 5 nm on at least two opposite sides. A -64 dbu y-shrink of the M3 shape in VIA_VIA34_1_2_58_52 combined with -24 dbu y-shrinks of both V3 shapes produced a net +34 violation increase (trial:i01.cu.def:VIA_VIA34_1_2_58_52.01). Do not shrink M3 in the y-direction in VIA_VIA34 cells; even when accompanied by proportional V3 shrinks, this combination increases total violation count rather than reducing it (trial:i01.cu.def:VIA_VIA34_1_2_58_52.01).