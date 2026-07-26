**M2 instance-move operations introduce no new M2 violations**

All unit_gate trials that touched M2 produced zero new in-crop or out-of-crop M2 violations. Single-instance x-shifts of 4 dbu (trial:i01.ug.leaf_0006.05), 36 dbu (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.leaf_0001.02, trial:i02.ug.leaf_0001.00), 108 dbu (trial:i01.ug.Block5_union_row6.01), and 112 dbu (trial:i01.ug.leaf_0005.04) all cleared without M2 geometry errors. Opposing-direction moves—i0056 shifted +36 dbu and i0103 shifted -36 dbu simultaneously—also introduced no M2 violations (trial:i01.ug.leaf_0002.03). These trials co-touched M1 and V1 but left M2 clean across loci ranging from single-unit crops to multi-unit spans.

**Polygon x-resizes alongside instance moves remain safe for M2**

trial:i01.ug.Block5_union_row6.01 combined two instance x-shifts of +108 dbu with x-axis polygon resizes of +256 dbu (p955) and +328 dbu (p971) on layers including M2, and produced zero new in-crop or out-of-crop violations. Widening M2-touching polygons by up to +328 dbu in x alongside co-moving instances did not trigger M2.S.7 (tip-to-tip/side-to-side co-location) or M2.W.1 (minimum width) or M2.S.1 (side-to-side spacing) violations. The resulting geometries satisfied the ≥35 nm parallel run-length requirement imposed by M2.S.7 when side spacing is ≤32 nm.

**cu_pool y-shrink on M2-touching polygons reduces violations**

trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 applied a -64 dbu y-axis resize to each of four polygons (p894, p895, p896, p897) touching M2, M3, and V2, paired with a -40 dbu y-axis resize of the M3 via shape in cell VIA_VIA23_1_3_36_36. The operation was accepted (decision: applied) and reduced violations in unit leaf_0009 from 25 to 17, a delta of -8 across the full crop window [1728,2068,9072,8732]. No new M2 violations were introduced by this shrink sequence.

**V2 lateral repositioning further reduces violations in the same cell**

trial:i02.cu.def:VIA_VIA23_1_3_36_36.01 moved V2 shape (shape_index 1) in cell VIA_VIA23_1_3_36_36 by +144 dbu along the x-axis, touching M2, M3, and V2. The operation was accepted (decision: applied) and reduced violations by -4 in leaf_0002 (17→13) and -3 in leaf_0003 (25→22), totaling -7. Combined with the prior iteration's y-shrink (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00), the two successive cu_pool operations on VIA_VIA23_1_3_36_36 removed 15 violations from units interacting with M2/V2 geometry without introducing any new M2 violations.

**cu_pool operations must precede unit_gate assembly for the same via cell**

trial:i02.ug.leaf_0003.02 recorded an assemble_drop: the assembler discarded a resize_via_shape op on M5 for cell VIA_VIA45_1_2_58_58 with reason "cu_pool:applied". This confirms that when cu_pool has committed a shape modification to a via cell, unit_gate assembly skips conflicting operations on that cell. Repair sequencing must apply cu_pool passes before unit_gate passes that reference the same via cell to avoid silently dropped ops.

**New in-crop violations on co-touched layers do not block M2-touching gated_in decisions**

trial:i02.ug.leaf_0003.02 introduced 7 new in-crop violations—M1.A.1 (4 instances) and V1.M1.EN.1 (3 instances)—while touching M2, M3, and V1, yet the decision was gated_in because conn_preserved=true. M2 itself received no new violations in that trial. The gating criterion for unit_gate is connectivity preservation, not a zero-new-violation condition on co-touched layers. M2 violations specifically must be held to zero new in-crop and zero new out-of-crop, while M1 and V1 violations may be accepted by the gating engine when connectivity is preserved.

**M2.A.1 was not triggered by any recorded operation**

No trial reported M2.A.1 (minimum area 504 nm²) as a new violation. The most aggressive area-reducing operation observed on M2-touching polygons was the -64 dbu y-axis shrink applied to p894–p897 (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00), which passed without a minimum-area violation. When shrinking M2 polygon dimensions on a single axis, post-operation area remained above the 504 nm² floor across all measured trials.

**M2.S.7 and M2.S.8 were not triggered by any recorded operation**

No trial produced M2.S.7 (tip-to-tip 18 nm gap co-located with side-to-side spacing ≤32 nm, with parallel run length <35 nm) or M2.S.8 (diagonal center-to-center spacing between tip-to-tip gaps <80 nm euclidian) violations. The x-direction instance moves and polygon resizes in trials trial:i01.ug.Block5_union_row3.00, trial:i01.ug.Block5_union_row6.01, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05, and trial:i02.ug.leaf_0001.00 were all performed laterally (x-axis only), and none produced the vertical-gap adjacency patterns that M2.S.7 and M2.S.8 govern.