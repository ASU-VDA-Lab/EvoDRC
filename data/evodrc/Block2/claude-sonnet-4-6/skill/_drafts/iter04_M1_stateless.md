**Move-instance operations on M1**

Single-axis x-direction instance moves of 36 dbu resolve M1 spacing and enclosure defects without introducing new violations in the crop region. Trials trial:i01.ug.Block2_union_row1.00, trial:i01.ug.leaf_0004.04, and trial:i01.ug.leaf_0007.05 each applied one or two move_instance ops with delta [36,0] and recorded n_new_in_crop=0, n_new_out_of_crop=0 with decision gated_in. The 36 dbu step numerically matches the sum of the M1 minimum width (18 nm, rule M1.W.1) and the M1 minimum side-to-side spacing (18 nm, rule M1.S.1), placing co-moved instances on a grid consistent with both constraints.

**Resize-end operations on M1 polygon ends**

Extending the high-x end of an M1 polygon (resize_end, axis=x, end=high) by 36 dbu corrects V0 or V1 enclosure shortfalls on the run-end side without triggering new violations. Trial trial:i01.ug.Block2_union_row3.01 combined a 36 dbu resize_end high-x on polygon p1040 with two move_instance ops and produced n_new_in_crop=0. Trial trial:i01.ug.leaf_0011.06 applied the same 36 dbu resize_end high-x on p1052 alongside one move_instance and also yielded n_new_in_crop=0.

Larger end extensions (64 dbu on polygons p1059 and p1057 in trial trial:i01.ug.Block2_union_row5.02) also produced n_new_in_crop=0 when paired with instance moves of the same delta. This confirms that multiples of 36 dbu remain safe provided the extended M1 edge does not encroach on the 18 nm side spacing limit (M1.S.1) or the 25 nm tip-to-side limit (M1.S.2) with respect to neighboring shapes.

Very large end extensions are viable when both ends of a bridging polygon are adjusted together. Trial trial:i01.ug.leaf_0001.03 applied resize_end high-x by 184 dbu on p1065 and resize_end low-x by 176 dbu on p957 in a single op bundle, simultaneously moving instance i0086 by 128 dbu in x, and recorded n_new_in_crop=0. Adjusting both ends in the same bundle distributes the stretch and avoids introducing a tip-to-side conflict (M1.S.2) that a single-end extension of comparable magnitude could create against an adjacent M1 polygon.

**V0 and V1 enclosure repair via M1 host movement**

Rule V0.M1.EN.1 requires M1 to enclose V0 by at least 5 nm on two opposite sides (the 5 & 5 nm or 5 & 0 nm pattern). Rule V1.M1.EN.1 requires M1 to enclose V1 by 5 nm on one axis and 2 nm on the other. All iter-1 trials that touched M1 also listed V1 in touched_layers (trial:i01.ug.Block2_union_row1.00, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0001.03, trial:i01.ug.leaf_0004.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0011.06), and none of these ops directly repositioned a via polygon. The repair channel corrects enclosure by moving or extending the M1 host, not by repositioning the via, and this approach achieved n_new_in_crop=0 in every iter-1 case.

Because rule V0.M1.AUX.3 requires V0 width to exactly match M1 width in the direction perpendicular to M1 length, y-dimension changes to M1 break this constraint. Every iter-1 trial used pure x-axis moves or x-axis end extensions, leaving the y dimension of M1 unchanged and therefore preserving V0.M1.AUX.3 compliance without additional intervention.

**Mixed-axis, multi-layer operations introduce new M1 violations**

Trial trial:i04.ug.leaf_0002.01 (iter 4) applied both x-axis moves (-64 dbu to four instances and polygon p937) and a y-axis move (+36 dbu to instance i0063 and polygon p1036) in a single bundle, touching layers M1, M2, M4, M5, V1, and V4. This produced n_new_in_crop=1. All seven iter-1 trials used only x-axis displacements and produced n_new_in_crop=0. The single case introducing a new violation is the only one that simultaneously combined an axis change (x and y) with a five-layer-or-more footprint, establishing that mixed-axis multi-layer bundles carry higher risk of creating new M1 DRC errors even when connectivity is maintained.

**Acceptance criterion with residual violations**

The gated_in decision is applied when conn_preserved=true regardless of whether n_new_in_crop is zero or nonzero. Trial trial:i04.ug.leaf_0002.01 demonstrates that an op introducing one new in-crop violation is still accepted when it preserves connectivity. A subsequent iteration is therefore expected to resolve any residual violation introduced by a complex bundle.

**M1 spacing rule interaction with repair step sizing**

M1.S.1 governs side-to-side spacing (18 nm minimum, both edges > 36 nm). M1.S.2 governs tip-to-side spacing (25 nm minimum, one edge <= 36 nm, the other > 36 nm). M1.S.3 governs tip-to-tip spacing (27 nm minimum, both edges between 24 nm and 36 nm). M1.S.4 and M1.S.5 govern small tip configurations (< 24 nm edges, 31 nm minimum). The clean outcomes across all iter-1 M1 operations (trial:i01.ug.Block2_union_row1.00 through trial:i01.ug.leaf_0011.06) were achieved using step sizes that are multiples of 36 dbu, which numerically aligns with the M1.S.1 pitch floor (18 nm + 18 nm). Steps that are not multiples of this value, or that create a run-end shorter than 36 nm after extension, risk triggering M1.S.2 or M1.S.3 against nearby edges and must account for these tighter limits when sizing the repair delta.