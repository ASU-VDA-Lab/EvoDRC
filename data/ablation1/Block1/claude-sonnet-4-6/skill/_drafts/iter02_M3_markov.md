**M3 y-axis polygon shrinks of -64 dbu accepted by unit_gate when connectivity is preserved**

In trial i02.ug.leaf_0014.05, a batch of 12 M3 polygon y-axis resize ops at -64 dbu each was accepted by the unit_gate channel (decision: gated_in). Connectivity was preserved across all 12 ops. The trial introduced new in-crop violations on adjacent layers (M1.A.1: 39, V1.M1.EN.1: 38, M4.W.5: 3, M4.S.4: 1, M4.S.5: 1) but zero new out-of-crop violations. The unit_gate channel accepts M3 polygon shrink ops that preserve connectivity even when they generate collateral violations on neighboring layers; those collateral counts do not block the gated_in outcome.

**resize_via_shape on M3 in cell VIA_VIA23_1_3_36_36 at -40 dbu y produces no net DRC reduction and is rejected by cu_pool**

In trial i02.cu.def:VIA_VIA23_1_3_36_36.00, a single resize_via_shape on M3 (cell VIA_VIA23_1_3_36_36, axis y, delta_dbu -40) was rejected by cu_pool with reason rejected_net_positive. Violation counts in both affected windows were unchanged (leaf_0014: 175 → 175, leaf_0015: 113 → 113; delta_total: 0). Connectivity was preserved. Do not apply resize_via_shape to M3 in VIA_VIA23_1_3_36_36 along the y-axis at -40 dbu; it does not reduce violations and will be rejected regardless of connectivity outcome.

**unit_gate drops cu_pool-rejected ops at assembly without affecting the remaining trial decision**

In trial i02.ug.leaf_0014.05, the VIA_VIA23_1_3_36_36 M3 resize_via_shape op (axis y, -40 dbu) was dropped at assembly with reason cu_pool:rejected_net_positive, referencing the rejection recorded in i02.cu.def:VIA_VIA23_1_3_36_36.00. The remaining 12 M3 polygon resize ops in the same trial were still accepted (gated_in). A cu_pool-rejected op dropped at the assemble phase does not block gated_in for the surviving ops in the same unit_gate trial.