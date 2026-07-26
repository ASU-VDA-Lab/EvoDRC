## M3 Width and Spacing Rules: Measured Parameters

M3.W.1 requires a minimum wire width of 18 nm. M3.S.1 sets 18 nm minimum side-to-side spacing when both edges exceed 36 nm in length. Tip edges introduce stricter requirements: M3.S.2 requires 25 nm tip-to-side clearance (one edge ≤ 36 nm, other > 36 nm); M3.S.3 requires 27 nm tip-to-tip when both edges are in the 24–36 nm range; M3.S.4 requires 31 nm tip-to-tip when both edges are < 24 nm; M3.S.5 requires 31 nm when one edge is 24–36 nm and the other is < 24 nm. M3.S.6 adds a 20 nm Euclidean corner-to-corner floor. M3.A.1 requires a minimum area of 504 nm². All M3 edges must be axis-aligned; GEOMETRY.NONORTHOGONAL is a hard violation for any non-0/90° edge.

## V2/M3 Enclosure and Width-Match Constraints

V2.M3.EN.2 requires M3 to enclose V2 by at least 5 nm on two opposite sides (acceptable configurations are 5&5 or 5&0 nm); the zero-enclosure endpoint condition is additionally checked per the deck's `v2_en2_ep_zero` pass. V2.M3.AUX.2 requires the V2 width to exactly match the M3 width in the direction perpendicular to M3's length; V2 polygons whose edges do not share coincident edges with M3 on at least two sides fail this rule. V3.M3.EN.1 requires M3 to enclose V3 by at least 5 nm on two opposite sides (horizontal or vertical pair); V3 not fully inside M3 always fails.

## Observed cu_pool Repair Strategy for VIA_VIA23_1_3_36_36

The cu_pool channel successfully resolved M3/V2 DRC violations across two iterations against target `def:VIA_VIA23_1_3_36_36`. In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, the repair applied a `resize_via_shape` shrink of −40 dbu on the y axis to the M3 shape inside the via cell, and simultaneously shrunk four M3 polygons (p894–p897) by −64 dbu each on the y axis. This group of five operations (tagged group g1) reduced the window violation total by 8 (from 25 to 17 in leaf_0009). In trial:i02.cu.def:VIA_VIA23_1_3_36_36.01, a follow-on `move_via_shape` relocated the V2 shape at index 1 by +144 dbu on the x axis within the same via cell, reducing violations by a further 7 (leaf_0002: −4, leaf_0003: −3). Both decisions were marked `applied` with `conn_preserved: true`.

The two-step pattern — first shrink M3 and the via's M3 shape in y, then reposition V2 in x — addresses both V2.M3.EN.2 (enclosure) and V2.M3.AUX.2 (width match) in sequence. Shrinking M3 in y adjusts the enclosure margin along the perpendicular axis; repositioning V2 in x corrects the lateral alignment needed for the coincident-edge check in V2.M3.AUX.2.

Resize deltas at the via-cell level (−40 dbu on M3, layer `M3`, axis y) are smaller in magnitude than the polygon-level resizes applied to the connecting M3 segments (−64 dbu per polygon, p894–p897). Apply the larger shrink to the long-segment polygons and the smaller shrink to the via-cell's internal M3 shape.

## Observed unit_gate Repair Strategy for M3-Touching Instances

The unit_gate channel repaired M3-layer violations via `move_instance` on connected cell instances in all three recorded trials. In trial:i01.ug.leaf_0010.07, six instances were moved: i0113 and i0099 each by +72 dbu in y, i0001 and i0002 each by +24 dbu in y, i0067 and i0070 each by −24 dbu in y. This produced zero new violations outside the crop window and was gated in with `conn_preserved: true`. In trial:i02.ug.leaf_0002.01, eight instances were moved (i0114, i0112, i0073, i0062 each by +32 dbu in x with varied y components; i0105, i0075, i0076 by y-axis adjustments), again with `conn_preserved: true` and zero new out-of-crop violations, despite introducing 27 new in-crop violations that were accepted because connectivity was preserved. In trial:i02.ug.leaf_0003.02, a mixed strategy was used: instance i0111 was moved +36 dbu in x, polygon p893 was resized −64 dbu on the y axis, and polygon p910 was moved +8 dbu on the x axis; this introduced 7 new in-crop violations (M1.A.1: 4, V1.M1.EN.1: 3) but preserved connectivity and was gated in.

Move-instance operations on M3-touching units consistently preserve connectivity. Direct polygon resize/move on M3 segments (p893 −64 dbu y, p910 +8 dbu x in trial:i02.ug.leaf_0003.02) introduce secondary violations in adjacent layers (M1, V1) and must be accounted for when budgeting violation debt.

## Assemble-Drop Interactions

In trial:i02.ug.leaf_0002.01, three ops were dropped at assembly: a move of p879 in x (+32 dbu) was dropped due to conflict with a cu_pool winner on leaf_0002; a y-axis resize of p879 (+96 dbu) was dropped because cu_pool had already applied; and a V2 `move_via_shape` on VIA_VIA23_1_3_36_36 (index 1, +144 dbu x) was dropped because cu_pool had already applied it. The cu_pool-applied V2 move at +144 dbu x in trial:i02.cu.def:VIA_VIA23_1_3_36_36.01 thus took precedence over the unit_gate attempt to move the same shape. When cu_pool and unit_gate both target the same VIA_VIA23_1_3_36_36 V2 shape, the cu_pool result wins at assembly.

## Enclosure-Sensitive Resize Bounds

V2.M3.EN.2 requires 5 nm enclosure. At 1 dbu = 1 nm (inferred from the 40/64/8/144 dbu deltas seen alongside nm-scale rules), a y-axis shrink of −40 dbu on the M3 via shape leaves adequate enclosure only if the original M3 shape had ≥ 45 nm extent beyond the V2 boundary on the shrunk side. The applied −64 dbu shrinks on polygon group p894–p897 (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00) resolved violations without producing new ones, confirming those polygons had sufficient length margin to absorb the reduction while keeping V2 enclosed.

V3.M3.EN.1 requires 5 nm enclosure on at least one axis pair. Any M3 polygon resize that reduces M3 extent near a V3 must keep the V3 inside M3 with at least 5 nm of inset on two opposite sides in at least one axis direction.