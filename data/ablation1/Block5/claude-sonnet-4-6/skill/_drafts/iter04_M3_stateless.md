## Via Cell M3 Shape Sizing Is the Primary M3 Repair Action

All cu_pool trials touching M3 operated on via cell M3 shapes via resize_via_shape. A +48 dbu y-axis expansion on the M3 shape in cell VIA_VIA34_1_2_58_52, executed as part of a multi-layer chain_fix bundle (M3, V3, V4), produced delta_total=-13 across leaf_0009 and leaf_0010 and was applied (trial:i01.cu.def:VIA_VIA34_1_2_58_52.00). A -40 dbu y-axis shrink on the M3 shape in cell VIA_VIA23_1_3_36_36 produced delta_total=-8 in leaf_0001 and was applied (trial:i03.cu.def:VIA_VIA23_1_3_36_36.00).

## Design-State Dependency of Via Cell M3 Resize Effectiveness

Do not discard a via cell M3 resize based on a single cu_pool rejection; re-evaluate after the design state advances. The identical resize_via_shape on VIA_VIA23_1_3_36_36 (axis=y, delta=-40 dbu) produced delta_total=0 in design state c5292a2 and was rejected as not net positive (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00). In the successor design state d7ef52f the same operation produced delta_total=-8 and was applied (trial:i03.cu.def:VIA_VIA23_1_3_36_36.00).

## Avoid Compound Bundles of M3 Via Resize Combined with Standalone Polygon End Resizes

Do not combine resize_via_shape on multiple via cells with simultaneous bidirectional resize_end operations on standalone M3 polygons. Trial:i02.cu.def:VIA_VIA23_1_3_36_36.01 bundled resize_via_shape on both VIA_VIA34_1_2_58_52 and VIA_VIA23_1_3_36_36 with six resize_end ops (both "low" and "high" ends of p891, p892, and p893, each -32 dbu), totaling 10 ops on M3, and produced delta_total=+5 — a net increase in violations. By contrast, the isolated chain_fix resize_via_shape on VIA_VIA34_1_2_58_52 alone produced delta_total=-13 (trial:i01.cu.def:VIA_VIA34_1_2_58_52.00), and the isolated resize_via_shape on VIA_VIA23_1_3_36_36 alone produced delta_total=-8 (trial:i03.cu.def:VIA_VIA23_1_3_36_36.00).

## Standalone M3 Polygon Y-Axis Shrinks: Unit_Gate Acceptance Pattern

Unit_gate accepted simultaneous y-axis shrinks of -64 dbu across groups of M3 polygons in two separate trials. Four polygons (p894, p895, p896, p897) in leaf_0005 were each shrunk -64 dbu on y and gated_in with conn_preserved=true (trial:i02.ug.leaf_0005.03). Three polygons (p891, p892, p893) in leaf_0002 were each shrunk -64 dbu on y and gated_in with conn_preserved=true (trial:i04.ug.leaf_0002.01). Both decisions registered 2 new in-crop violations attributable to V1.M1.EN.1, not to any M3 rule; no new M3-layer DRC violations appeared in either crop window after these shrinks.

## Assemble-Drop Behavior: Dropped Cu_Pool Op in a Unit_Gate Trial

Trial:i02.ug.leaf_0005.03 records an assemble_drop of a resize_via_shape on the M3 layer of VIA_VIA23_1_3_36_36 (axis=y, delta=-40 dbu), dropped with reason "cu_pool:rejected_net_positive." The drop corresponds directly to trial:i02.cu.def:VIA_VIA23_1_3_36_36.00, which had been rejected with delta_total=0 in the same design state. The unit_gate trial proceeded with only the four standalone polygon shrinks and was gated_in. When a cu_pool op is dropped at assembly due to prior rejection, the remaining standalone M3 polygon ops are still eligible for gated_in acceptance.

## Small X-Axis Instance Moves and Single M3 Polygon X-Axis Moves

Moving instances by 8 dbu along x is safe for M3. Trial:i02.ug.leaf_0001.01 moved instances i0104 and i0061 each +8 dbu on x, touching M2, M3, and V2, and introduced zero new in-crop violations, gated_in on conn_preserved grounds. Moving a single M3 polygon (p910) by +8 dbu on x (trial:i01.ug.leaf_0010.07) was accepted with 3 new in-crop violations; the delta record does not attribute those violations to any M3 rule, and the decision was gated_in on conn_preserved grounds at iter 1 before any prior M3 state reduction.

## V2.M3.EN.2, V2.M3.AUX.2, and V3.M3.EN.1: No New Violations from Applied Resizes

None of the applied M3 via cell resizes introduced violations under V2.M3.EN.2, V2.M3.AUX.2, or V3.M3.EN.1. The +48 dbu y-axis M3 resize on VIA_VIA34_1_2_58_52 — a cell containing V3 shapes — did not trigger V3.M3.EN.1 failures (trial:i01.cu.def:VIA_VIA34_1_2_58_52.00). The -40 dbu y-axis M3 resize on VIA_VIA23_1_3_36_36 — a cell containing V2 shapes — did not trigger V2.M3.EN.2 or V2.M3.AUX.2 failures (trial:i03.cu.def:VIA_VIA23_1_3_36_36.00). Use these resize magnitudes and directions as the baseline for enclosure-safe adjustments on their respective via cell types.