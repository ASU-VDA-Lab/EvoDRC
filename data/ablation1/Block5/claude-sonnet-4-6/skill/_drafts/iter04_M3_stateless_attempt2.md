## M3 Via-Shape Resize: Single-Operation Context Dependence

Resizing a single M3 via shape (VIA_VIA23_1_3_36_36, shape_index 0, -40 dbu on y) produced opposite outcomes across two design states. At design_state c5292a..., the operation yielded delta_total=0 and was rejected by cu_pool as not net-positive (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00). At design_state d7ef52f..., the identical operation reduced violations by 8 (delta_total=-8) and was applied (trial:i03.cu.def:VIA_VIA23_1_3_36_36.00). Do not treat a M3 via-shape resize as permanently blocked after a single-state rejection; the same operation becomes viable when the surrounding design state changes.

## Compound Multi-Layer Bundles Touching M3 Produce Net-Positive Results

A compound bundle combining an M3 via-shape resize, V3 via-shape resizes, and bidirectional end resizes on three standalone M3 polygons (p891/p892/p893), all under the V2M3_corrected group, produced delta_total=+5 and was rejected as net-positive (trial:i02.cu.def:VIA_VIA23_1_3_36_36.01). The single-op subset of that same bundle — the M3 via-shape resize of -40 dbu y in isolation — was applied at delta_total=-8 in a subsequent iteration (trial:i03.cu.def:VIA_VIA23_1_3_36_36.00). Do not apply compound bundles that mix M3 via-shape resizes with standalone M3 polygon end resizes when a narrower single-op alternative exists; the compound form increases the total violation count while the isolated via-shape op reduces it.

## Standalone M3 Polygon Y-Axis Resize (-64 dbu) Introduces New In-Crop Violations

Applying -64 dbu y-axis resizes to groups of standalone M3 polygons introduced 2 new in-crop violations in each case: p897/p896/p895/p894 in trial:i02.ug.leaf_0005.03 and p893/p892/p891 in trial:i04.ug.leaf_0002.01. Both were accepted by unit_gate under the conn_preserved gating criterion. The new violations recorded in trial:i02.ug.leaf_0005.03 were attributed to rule V1.M1.EN.1, not to any M3 rule. Do not expect groups of -64 dbu y resizes on M3 polygons to be violation-free; each such operation has consistently introduced exactly 2 new in-crop violations before acceptance.

## Polygon-Level X-Axis Moves on M3 Carry Higher Violation Risk Than Instance-Level Moves

Moving a single M3 polygon (p910) by +8 dbu on the x-axis introduced 3 new in-crop violations (trial:i01.ug.leaf_0010.07); the trial was gated_in due to conn_preserved, not because the violations were absent. Moving instances that touch M3 by the same +8 dbu on x (instances i0104 and i0061) introduced zero new in-crop violations (trial:i02.ug.leaf_0001.01). At this displacement magnitude, instance-level moves have produced clean results while polygon-level moves have not.

## Via-Chain M3 Shape Resize: Apply Only Within Coordinated Chain-Fix Groups

In trial:i01.cu.def:VIA_VIA34_1_2_58_52.00, resizing the M3 shape in cell VIA_VIA34_1_2_58_52 by +48 dbu on y was co-applied under the chain_fix group alongside V3 shape resizes, V4 shape resizes, and an M4 shape resize, reducing the total violation count by 13 (delta_total=-13). Resize the M3 via shape in a via-chain cell only within the coordinated chain_fix group that simultaneously adjusts the adjacent via and metal shapes; doing so preserved the enclosure relationships governed by V2.M3.EN.2, V2.M3.AUX.2, and V3.M3.EN.1, and the trial was applied without connectivity loss.

## Assembly Drops M3 Via-Shape Ops When the Corresponding Cu-Pool Trial Was Rejected

The assembly step for trial:i02.ug.leaf_0005.03 dropped a planned M3 via-shape resize (VIA_VIA23_1_3_36_36, shape_index 0, -40 dbu y) with reason cu_pool:rejected_net_positive, because the standalone cu_pool trial for that op (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00) had been rejected in the same iteration. The unit_gate assembly channel enforces cu_pool rejection decisions for M3 via-shape operations before committing the assembled fix.