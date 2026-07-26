**X-direction instance moves on M2-connected cells**

All unit_gate trials in iteration 1 that moved instances along x by 36 dbu or 64 dbu were accepted with zero new M2 violations (trial:i01.ug.Block2_union_row1.00, trial:i01.ug.leaf_0004.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0011.06, trial:i01.ug.Block2_union_row5.02). When moving M2-connected instances in the x-direction, use multiples of 36 dbu; these increments have produced clean results across five distinct unit and row contexts.

**resize_end on the high x-end of M2 polygons**

Extending M2 polygons at their high x-end by 36 dbu or 64 dbu did not introduce new M2 violations in any trial where this operation appeared (trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0011.06). Pair each resize_end(axis=x, end=high) with the corresponding instance move for the same delta; all three cited trials applied this paired pattern and preserved connectivity.

In iteration 5, a resize_end(axis=x, end=high, delta=56 dbu) paired with a 36 dbu instance move also produced a gated_in result on M2 (trial:i05.ug.leaf_0002.01). Mixed-magnitude pairings (instance move at 36 dbu, polygon extension at 56 dbu) are therefore viable when the net assembly eliminates more violations than it introduces.

**Y-direction M2 shrinks via the VIA_VIA23_1_3_36_36 cu_pool adjustment**

Shrinking M2 polygons by 64 dbu along y as part of the VIA_VIA23_1_3_36_36 via cell adjustment reduced total DRC violation count by 8 per application, confirmed in two successive iterations across two distinct design states (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, trial:i02.cu.def:VIA_VIA23_1_3_36_36.00). Apply this y-shrink adjustment to the four M2 polygons associated with each via23 instance when M2 or V2 violations cluster around those instances.

**Avoid y-direction expansion of VIA_VIA23_1_3_36_36 shapes touching M2**

The reverse operation -- expanding the via shape along y by +40 dbu -- was rejected as net_positive with delta_total=0 in iteration 5 (trial:i05.cu.def:VIA_VIA23_1_3_36_36.00). Do not apply y-expansion to VIA_VIA23_1_3_36_36 when targeting M2 violations; the measured result is no net reduction.

**Assemble_drops: dropped cu_pool operations in unit_gate assembly**

The iteration 5 unit_gate trial for leaf_0002 dropped a via y-expansion (+40 dbu on the VIA_VIA23_1_3_36_36 M3 shape) from its assembled operation set, citing cu_pool:rejected_net_positive (trial:i05.ug.leaf_0002.01). When the cu_pool has already rejected an operation as net_positive in the current design state, the assembler omits it. Do not resubmit that operation in the same design state; resubmission in a changed design state after further repairs is the correct path.

**Gating on connectivity, not zero new violations**

The unit_gate channel accepted trials that introduced one new in-crop violation when connectivity was preserved (trial:i04.ug.leaf_0002.01, trial:i05.ug.leaf_0002.01). A single new violation entering the crop window does not block acceptance when conn_preserved=true. Prioritize operations that maintain electrical connectivity even if they incidentally introduce one new in-crop marker; the repair iterator will address residual violations in subsequent passes.

**Multi-layer operations and M2 interaction**

Several accepted trials touched M2 alongside other layers (M1, V1, M4, M5, V4) within the same operation set (trial:i01.ug.leaf_0001.03, trial:i04.ug.leaf_0002.01, trial:i05.ug.leaf_0002.01). Co-moving M2 with adjacent-layer polygons and vias in a single atomic step is consistent with gated_in outcomes, provided all M2 polygons in the locus remain within the crop window after the move.