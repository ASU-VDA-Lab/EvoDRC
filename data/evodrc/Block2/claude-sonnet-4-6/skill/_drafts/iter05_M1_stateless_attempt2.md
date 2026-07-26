**Resize operations on M1 polygons are confined to axis-aligned end extensions**

Every resize_end operation recorded in this layer's history targeted axis:x, with either end:high or end:low. In trial:i01.ug.Block2_union_row3.01, polygon p1040 received axis:x, end:high, delta_dbu:36. In trial:i01.ug.Block2_union_row5.02, polygons p1059 and p1057 each received axis:x, end:high extensions of 64 dbu. In trial:i01.ug.leaf_0001.03, polygon p1065 received axis:x, end:high extension of 184 dbu and polygon p957 received axis:x, end:low extension of 176 dbu. In trial:i01.ug.leaf_0011.06, polygon p1052 received axis:x, end:high extension of 36 dbu. In trial:i05.ug.leaf_0002.01, polygon p1036 received axis:x, end:high extension of 56 dbu. No axis:y resize_end appears in any record.

**Move deltas are strictly axis-aligned (X or Y only)**

Every move_instance and polygon-move delta in this history is either purely horizontal or purely vertical. Horizontal moves used delta_dbu [36,0] in trial:i01.ug.Block2_union_row1.00, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.leaf_0004.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0011.06, and trial:i05.ug.leaf_0002.01; [64,0] in trial:i01.ug.Block2_union_row5.02; [128,0] in trial:i01.ug.leaf_0001.03; and [-64,0] in trial:i04.ug.leaf_0002.01. Vertical moves used delta_dbu [0,36] in trial:i04.ug.leaf_0002.01 and trial:i05.ug.leaf_0002.01. No diagonal (mixed X and Y) delta appears in any record. The NONORTHOGONAL rule requires all M1 edges to be at exactly 0 or 90 degrees; the exclusively axis-aligned deltas observed across all nine trials are consistent with that constraint.

**All nine trials were accepted**

Every trial in this history carries decision:gated_in and conn_preserved:true. Zero trials in this dataset were rejected. New in-crop violations were introduced in two cases: trial:i04.ug.leaf_0002.01 (n_new_in_crop:1) and trial:i05.ug.leaf_0002.01 (n_new_in_crop:1, specifically rule M1.A.1). Both were accepted because conn_preserved:true satisfied the gating condition.

**M1.A.1 (minimum area 504 nm-sq) can be introduced and still pass gating when connectivity is preserved**

In trial:i05.ug.leaf_0002.01, the operation set (move_instance i0071 by [0,36], move_instance i0063 by [36,0], resize_end on p1036 axis:x end:high delta:56) produced exactly one new M1.A.1 violation in crop. The trial was nonetheless accepted. This shows that a single new M1.A.1 in-crop error does not block acceptance when conn_preserved is true. However, the violation remains in the design state advancing to the next iteration.

**V0.M1.EN.1 and V0.M1.AUX.3: enclosure and width constraints pass after moderate moves**

V0.M1.EN.1 requires M1 to enclose V0 by at least 5 nm on two opposite sides (5 & 5 or 5 & 0 pattern). V0.M1.AUX.3 requires V0 to exactly match M1 width perpendicular to the M1 run direction. All trials that touched M1 and V1 — trial:i01.ug.Block2_union_row1.00, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0001.03, trial:i01.ug.leaf_0004.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0011.06, trial:i04.ug.leaf_0002.01, trial:i05.ug.leaf_0002.01 — passed with n_new_out_of_crop:0, indicating no new V0 or V1 enclosure violations were introduced out of crop by any of these move or resize operations.

**V1.M1.EN.1: asymmetric enclosure (5 nm and 2 nm opposite sides)**

V1.M1.EN.1 requires M1 to enclose V1 with at least 5 nm on one side and at least 2 nm on the opposite side. This is less restrictive than V0.M1.EN.1. All nine trials touching V1 were accepted with n_new_out_of_crop:0, consistent with the move and resize magnitudes applied maintaining the required asymmetric clearances.

**Multi-layer coupling scales with move magnitude**

Move deltas of 36 dbu coupled M1 with M2 and V1 only, as seen in trial:i01.ug.Block2_union_row1.00 (touched_layers: M1, M2, V1), trial:i01.ug.leaf_0004.04, and trial:i01.ug.leaf_0007.05. Larger deltas expanded the coupled layer set: 64 dbu in trial:i01.ug.Block2_union_row5.02 still touched only M1, M2, V1; 128 dbu with 176–184 dbu resize offsets in trial:i01.ug.leaf_0001.03 pulled in M4 (touched_layers: M1, M2, M4, V1); the mixed-axis move set of 64 dbu (X) and 36 dbu (Y) in trial:i04.ug.leaf_0002.01 coupled M1, M2, M4, M5, V1, V4; and the 36+56 dbu mixed operation in trial:i05.ug.leaf_0002.01 additionally engaged M3 and V2.

**Assemble drops on non-M1 layers do not block M1 repair acceptance**

In trial:i05.ug.leaf_0002.01, one assembled operation was dropped: a resize_via_shape on the M3 layer with reason cu_pool:rejected_net_positive. The trial was accepted and conn_preserved remained true. Drops confined to layers other than M1 do not prevent the M1-layer repair from being gated in.

**Accepted delta magnitudes observed in this history**

The following resize_end and move delta magnitudes have each been observed in at least one accepted trial on M1: 36 dbu (trial:i01.ug.Block2_union_row3.01, trial:i01.ug.leaf_0011.06, trial:i05.ug.leaf_0002.01 move ops), 56 dbu resize (trial:i05.ug.leaf_0002.01), 64 dbu move and resize (trial:i01.ug.Block2_union_row5.02, trial:i04.ug.leaf_0002.01), 128 dbu move with 176–184 dbu resize (trial:i01.ug.leaf_0001.03). The full range 36–184 dbu has been exercised on M1 polygon resize_end operations without producing out-of-crop violations.

**M1.S.1, M1.S.2, M1.S.3, M1.S.4, M1.S.5, M1.S.6 spacing rules**

No new M1.S.* violations appear in any trial's per_rule or new_in_crop records. The spacing rules (18 nm side-to-side M1.S.1, 25 nm tip-to-side M1.S.2, 27 nm tip-to-tip M1.S.3, 31 nm tip-to-tip M1.S.4 and M1.S.5, 20 nm corner-to-corner M1.S.6) were not violated by any of the axis-aligned move and end-extension operations recorded in trial:i01.ug.Block2_union_row1.00 through trial:i05.ug.leaf_0002.01.

**M1.W.1 (minimum width 18 nm)**

No new M1.W.1 violations appear in any trial record. End-extension operations in this history (trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0001.03, trial:i01.ug.leaf_0011.06, trial:i05.ug.leaf_0002.01) extend along the polygon run axis and do not reduce M1 width.

**M1.R.0 (redundant M1 island)**

No M1.R.0 violations appear in any trial's violation records. The rule targets M1 polygons enclosing exactly one small V0 via when located near a large empty M1 region. No trial in this history introduced a new M1.R.0 flag in crop or out of crop.