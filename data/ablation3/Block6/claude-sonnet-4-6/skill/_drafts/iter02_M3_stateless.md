**Active violations and rule priority**

V2.M3.EN.2 (minimum enclosure of V2 by M3, two opposite sides each at least 5 nm) is the sole M3-adjacent DRC rule recorded as generating new in-crop violations this iteration. The unit_gate trial trial:i02.ug.whole_design.00 produced 10 new V2.M3.EN.2 violations while being gated in. No new violations of M3.W.1, M3.S.1–M3.S.6, M3.A.1, V2.M3.AUX.2, V3.M3.EN.1, or the NONORTHOGONAL rule were recorded in any trial this iteration. Treat V2.M3.EN.2 as the dominant active constraint for M3 in iteration 2.

**Cu-pool via-cell widening reduces violations**

The cu_pool channel applied a move-and-resize sequence to V2 shapes inside cell definition VIA_VIA23_1_3_36_36. The sequence is: move shape_index 0 by −144 dbu in X; resize shape_index 0 and shape_index 1 each by +288 dbu in X; move shape_index 2 by +144 dbu in X; resize shape_index 2 by +288 dbu in X. This net-expands and re-centers the V2 via shapes along X within that cell. The outcome was a reduction of total violations from 159 to 81 (delta −78) across unit:whole_design (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00). Because V2.M3.EN.2 checks that M3 encloses V2 by at least 5 nm on two opposite sides, expanding the V2 shape inside a fixed M3 landing reduces the enclosure margin; however, the net violation count still dropped by 78, indicating that correcting the X-centering of V2 within M3 resolved more enclosure failures than the expansion created.

**Unit-gate moves introduce new V2.M3.EN.2 violations**

The unit_gate trial trial:i02.ug.whole_design.00 moved M3 polygons p1682, p1683, and p1685 along the X axis (delta_dbu −16, +32, and +32 respectively) and extended the high-X ends of M3 polygons p1831, p1786, and p1806 (each by +20 dbu in X, combined with Y-end adjustments of +24/−24/+24/+72 dbu). These moves, taken alongside a large set of instance moves, introduced exactly 10 new V2.M3.EN.2 violations in-crop while preserving connectivity (conn_preserved: true). The trial was accepted (decision: gated_in). When moving M3 polygons or resizing their ends in X, the resulting 10 new V2.M3.EN.2 violations confirm that lateral displacement of M3 relative to underlying V2 sites reduces enclosure on one X-side. Do not move M3 polygons laterally without verifying that each resident V2 via retains at least 5 nm enclosure on two opposite sides.

**V2.M3.AUX.2 interaction with via-cell reshaping**

V2.M3.AUX.2 requires that V2 exactly matches M3 width perpendicular to M3 length. The cu_pool operation on VIA_VIA23_1_3_36_36 resized V2 shapes in X by +288 dbu (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00). Because this operation was applied and resulted in a net violation decrease, the resized V2 footprint still satisfied V2.M3.AUX.2 after adjustment — the M3 landing in that cell accommodates the new V2 width perpendicular to M3 length. However, no V2.M3.AUX.2 violations appear in the new_in_crop_by_rule record of either trial, so the rule was not triggered by either operation this iteration.

**V3.M3.EN.1 was not triggered**

Despite the unit_gate trial touching V3 (touched_layers includes "V3"), no V3.M3.EN.1 violations were recorded in either trial this iteration (trial:i02.ug.whole_design.00, trial:i02.cu.def:VIA_VIA23_1_3_36_36.00). V3.M3.EN.1 requires M3 to enclose V3 by at least 5 nm on two opposite sides. The instance moves and M3 end-resizes in the unit_gate trial did not break V3 enclosure.

**Resize-end operations on M3**

Three M3 polygons received resize_end operations in trial:i02.ug.whole_design.00: p1831 (high-X end extended +20 dbu, low-Y end extended +24 dbu), p1786 (high-X end extended +20 dbu, high-Y end extended +72 dbu), and p1806 (high-X end extended +20 dbu, high-Y end extended +24 dbu). These extensions were accepted alongside the gated-in decision. The X extensions of 20 dbu on all three polygons did not trigger M3.W.1 (minimum width 18 nm) or M3.S.1 violations in the recorded results. Extending M3 ends along X by 20 dbu in this design context is viable when the adjoining spacing budget supports it.