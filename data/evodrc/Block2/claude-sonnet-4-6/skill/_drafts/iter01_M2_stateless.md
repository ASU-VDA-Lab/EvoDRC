## Effective Repair Patterns Observed on M2

### X-Direction Instance Moves — Safe Minimum Delta

All seven unit_gate trials applied only x-axis motion and produced zero new M2 violations (n_new_in_crop: 0, n_new_out_of_crop: 0 across trials i01.ug.Block2_union_row1.00, i01.ug.Block2_union_row3.01, i01.ug.Block2_union_row5.02, i01.ug.leaf_0001.03, i01.ug.leaf_0004.04, i01.ug.leaf_0007.05, i01.ug.leaf_0011.06). The smallest x-shift applied was 36 dbu. Trials i01.ug.Block2_union_row1.00, i01.ug.leaf_0004.04, and i01.ug.leaf_0007.05 used only move_instance with delta_dbu [36,0] and achieved conn_preserved: true with no new violations. Larger shifts of 64 dbu (i01.ug.Block2_union_row5.02) and 128 dbu (i01.ug.leaf_0001.03) were also applied cleanly. Do not apply y-direction motion during unit_gate repairs targeting M2; no y-axis delta appears in any of the seven unit_gate trials that touched M2, and all seven closed without new M2 violations.

### Pairing resize_end with move_instance

When a move_instance would shorten or strand an M2 polygon endpoint, pair it with resize_end on the affected polygon. In trial i01.ug.Block2_union_row3.01, move_instance delta [36,0] was paired with resize_end axis:x end:high delta:36 on p1040 — zero new violations. In trial i01.ug.Block2_union_row5.02, move_instance delta [64,0] was paired with resize_end axis:x end:high delta:64 on both p1059 and p1057 — zero new violations. In trial i01.ug.leaf_0011.06, move_instance delta [36,0] was paired with resize_end axis:x end:high delta:36 on p1052 — zero new violations.

The resize_end delta matched or exceeded the move_instance delta in every successful trial. In trial i01.ug.leaf_0001.03, move_instance delta was 128 dbu but resize_end end:high on p1065 used delta 184 dbu and resize_end end:low on p957 used delta 176 dbu; both polygon ends were extended outward to cover shifted connection points, and no new M2 violations were introduced. Never apply a negative (shrinking) resize_end on an M2 polygon in the x-direction during a unit_gate repair; all resize_end operations in trials i01.ug.Block2_union_row3.01, i01.ug.Block2_union_row5.02, i01.ug.leaf_0001.03, and i01.ug.leaf_0011.06 used positive deltas (extensions) on axis:x.

### No New Compound Rule Violations from X-Moves ≥ 36 dbu

The compound rules M2.S.7 and M2.S.8 are triggered by specific combinations of tip-to-tip gap position and side-to-side spacing. X-axis moves of 36 dbu and above did not introduce new M2.S.7 or M2.S.8 violations in any of the unit_gate loci tested (trials i01.ug.Block2_union_row1.00 through i01.ug.leaf_0011.06). Increasing tip-to-tip distance by moving instances in x resolves the colocation condition that M2.S.7 forbids.

### Y-Direction M2 Shrink for V2 Enclosure Repair

Trial i01.cu.def:VIA_VIA23_1_3_36_36.00 (channel: cu_pool, decision: applied) reduced total violations by 8 (delta_total: -8) by shrinking M2 polygons in y. The four M2 polygons p962, p963, p964, and p965 were each resized by -64 dbu on the y-axis; simultaneously the via shape for cell VIA_VIA23_1_3_36_36 was resized by -40 dbu on y. The touched layers were M2, M3, and V2. Shrinking M2 in y by 64 dbu while shrinking the co-located V2 via shape by 40 dbu on the same axis resolved the enclosure violations without introducing new M2 spacing violations, as confirmed by the applied outcome in trial i01.cu.def:VIA_VIA23_1_3_36_36.00.

### Connectivity Preservation Across All Trials

Every trial that moved instances and stretched M2 polygon endpoints in x preserved connectivity (conn_preserved: true in all eight trials). The pattern — move_instance in x paired with resize_end axis:x on the downstream M2 polygon end — is the consistent repair structure. No trial that followed this pattern introduced new violations on M2, M1, or V1 (trials i01.ug.Block2_union_row1.00 through i01.ug.leaf_0011.06 all touch M1, M2, and V1 together).