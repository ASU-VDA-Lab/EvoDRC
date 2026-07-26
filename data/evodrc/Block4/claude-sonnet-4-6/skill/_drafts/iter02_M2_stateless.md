**Move Quantum and Direction**

Instance moves that resolve M2 violations use multiples of 36 dbu along the x-axis exclusively; no y-axis instance moves appear in any accepted M2 repair (trial:i01.ug.leaf_0008.08, trial:i01.ug.leaf_0020.09, trial:i01.ug.leaf_0021.10, trial:i02.ug.leaf_0001.00, trial:i01.ug.Block4_union_row3.03, trial:i01.ug.Block4_union_row6.05). The minimum observed displacement is 36 dbu; 72 dbu (trial:i02.ug.leaf_0001.00), 108 dbu (trial:i01.ug.Block4_union_row1.00, trial:i01.ug.Block4_union_row7.06), and 64 dbu (trial:i01.ug.Block4_union_row5.04) are also accepted. Use 36 dbu as the atomic candidate step when searching for valid positions.

**Polygon Resize Strategy**

Extend M2 polygon ends along the x-axis high end to increase parallel run length; accepted high-end extension amounts span 56 to 172 dbu across row-level repairs (trial:i01.ug.Block4_union_row2.02, trial:i01.ug.Block4_union_row5.04, trial:i01.ug.Block4_union_row7.06, trial:i01.ug.Block4_union_row10.01). M2.S.7 requires parallel run length ≥ 35 nm when side-to-side spacing is ≤ 32 nm; extensions in the 56–172 dbu range address that constraint. A low-end resize is also accepted: trial:i01.ug.Block4_union_row10.01 includes one end="low" resize of 72 dbu alongside multiple high-end resizes. Shrinking the high end by 8 dbu paired with a matching -8 dbu instance move is accepted (trial:i02.ug.leaf_0003.02), but that combination introduced n_new_in_crop=2 new violations in the local crop window while still passing because connectivity was preserved.

**Adding Bridge Polygons**

When instance moves alone cannot close a connectivity gap, add a new rectangular M2 polygon to bridge. In trial:i01.ug.Block4_union_row1.00 two M2 polygons were added: [[9252,3024],[9444,3024],[9444,3096],[9252,3096]] (192×72 dbu, area 13,824 dbu²) and [[12132,3024],[12224,3024],[12224,3096],[12132,3096]] (92×72 dbu, area 6,624 dbu²). Both satisfy M2.W.1 (minimum dimension 72 dbu >> 18 nm) and M2.A.1 (both areas >> 504 nm²). Both polygons share the same y-range (3024–3096), which keeps their long edges co-planar with adjacent M2 segments and avoids introducing new tip-to-side violations under M2.S.2.

**Multi-Operation Row Repairs**

Row-level units require coordinated sequences of move_instance and resize_end applied together to maintain alignment and preserve connectivity. trial:i01.ug.Block4_union_row7.06 used 8 ops (four instance moves + four resize_end calls) across layers M1, M2, M4, V1 and was accepted. trial:i01.ug.Block4_union_row10.01 used 7 ops across M1, M2, M4, V1 and was accepted. trial:i01.ug.Block4_union_row5.04 used 6 ops and was accepted. In all cases conn_preserved=true and decision=gated_in. Never issue resize_end without the companion instance move when multiple instances share the same M2 segment, or relative positions will skew and create new spacing violations.

**Cu Pool Via Resize**

A y-axis shrink of -40 dbu on a via cell shape (touching M2, M3, V2 layers) was rejected because the net DRC delta was zero (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, delta_total=0, decision=rejected_net_positive). The cu_pool channel requires a strictly positive net reduction in violation count; do not apply via shape resizes as M2 repair operations unless they produce a measurable decrease in total violations. The unit_gate channel does not apply this net-improvement criterion.

**Gating Criterion and Violation Budget**

The unit_gate channel gates on connectivity preservation, not DRC cleanliness. trial:i02.ug.leaf_0003.02 was accepted (decision=gated_in) despite introducing n_new_in_crop=2 new violations in the crop window, because conn_preserved=true. All other accepted trials produced n_new_in_crop=0. Repairs that introduce new violations are still accepted by the unit_gate channel, but the residual violations remain in the design state for the next iteration. The cu_pool channel applies a stricter net-improvement gate, as confirmed by the rejection in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00.

**V1/M2 Enclosure Maintenance**

All accepted unit_gate trials that touch both V1 and M2 move the containing instance as a rigid body, preserving the internal V1-to-M2 enclosure without requiring explicit via shape edits (trial:i01.ug.leaf_0008.08, trial:i01.ug.leaf_0020.09, trial:i01.ug.leaf_0021.10, trial:i02.ug.leaf_0001.00, trial:i01.ug.Block4_union_row3.03, trial:i01.ug.Block4_union_row6.05). V1.M2.EN.2 (≥5 nm enclosure on two opposite sides) and V1.M2.AUX.2 (V1 width matches M2 width perpendicular to M2 length) are satisfied by rigid instance moves without separate via adjustments. When a new M2 polygon is added to bridge a gap (trial:i01.ug.Block4_union_row1.00), no corresponding V1 is added, confirming that bridge polygons function as connectivity extensions only and need not host vias.

**Design State Transition**

All iteration-1 trials operate on design state d279330...; both iteration-2 trials operate on design state d63aa6..., confirming that the gated-in iter-1 repairs committed a new design state before iter-2 began. Repair logic must query the current design state rather than assuming continuity from a prior iteration.