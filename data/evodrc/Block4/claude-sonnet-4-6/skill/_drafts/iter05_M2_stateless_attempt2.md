**Repair acceptance in the unit_gate channel**

All unit_gate repairs in this history are accepted (decision="gated_in"). Trial:i01.ug.Block4_union_row1.00 through trial:i02.ug.leaf_0001.00 all show conn_preserved=true and n_new_in_crop=0. Trial:i02.ug.leaf_0003.02 was also gated_in despite n_new_in_crop=2, with reason="conn_preserved," confirming that connectivity preservation is the primary gate condition; the unit_gate channel tolerates small numbers of new in-crop violations when connectivity is maintained.

**Primary repair: move_instance along x**

Moving instances along the x-axis is the most frequent M2 repair action. Moves of exactly 36 dbu are used when a single cell needs modest repositioning (trial:i01.ug.Block4_union_row3.03, trial:i01.ug.Block4_union_row6.05, trial:i01.ug.leaf_0008.08, trial:i01.ug.leaf_0020.09, trial:i01.ug.leaf_0021.10, trial:i02.ug.leaf_0001.00). Larger moves of 64–112 dbu are applied when coordinated repositioning of multiple instances is required (trial:i01.ug.Block4_union_row5.04, trial:i01.ug.Block4_union_row1.00, trial:i01.ug.Block4_union_row7.06). Pairs of opposing moves — one positive, one negative on adjacent instances — also appear to balance spacing from both sides (trial:i01.ug.Block4_union_row3.03). A small negative move (-28 dbu) alongside larger positive moves is used when fine adjustment is needed to satisfy spacing from one direction without overcrowding the other (trial:i01.ug.Block4_union_row7.06).

**Complementary repair: resize_end on M2 polygons**

When instance moves do not fully resolve requirements, resize_end operations extend or trim M2 polygon ends along the x-axis. Extension deltas range from 56 to 172 dbu on high ends and 64–72 dbu on low ends (trial:i01.ug.Block4_union_row10.01, trial:i01.ug.Block4_union_row2.02, trial:i01.ug.Block4_union_row7.06). A small high-end trim of -8 dbu is used in trial:i02.ug.leaf_0003.02 in combination with a matching -8 dbu instance move in the same group, preserving connectivity while accepting two new in-crop violations. Do not apply resize_end in isolation: every accepted resize_end in this history is paired with at least one move_instance in the same transaction (trial:i01.ug.Block4_union_row10.01, trial:i01.ug.Block4_union_row2.02, trial:i01.ug.Block4_union_row7.06, trial:i02.ug.leaf_0003.02).

**Adding new M2 polygons**

Insert new M2 rectangles to close gaps when connectivity would otherwise be broken. Trial:i01.ug.Block4_union_row1.00 adds two M2 shapes with 72 dbu height and widths of 192 dbu and 92 dbu respectively, alongside two move_instance operations. Both added shapes produced n_new_in_crop=0, confirming that properly sized rectangles within the track footprint do not introduce new spacing violations.

**V2/M2 enclosure: resize V2 shapes, not M2 or M3**

For the VIA_VIA23_1_3_36_36 cell, shrinking M3 in y by 40 dbu (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, rejected_net_positive, delta=0) produced no reduction in violations touching M2. The effective repair (trial:i05.cu.def:VIA_VIA23_1_3_36_36.00, applied, delta_total=-51) moved V2 shapes -144 dbu in x and widened them +288 dbu per side in x across all three via shapes, achieving a net reduction of 51 violations without modifying M2 or M3 geometry. Prefer V2 shape repositioning and widening over M2 or M3 modifications when addressing V2.M2 enclosure deficits (trial:i05.cu.def:VIA_VIA23_1_3_36_36.00).

**Observed operation axes and scope**

All M2 polygon resize_end operations in the accepted repairs use the x-axis exclusively; no y-axis resize_end is applied to M2 shapes (trial:i01.ug.Block4_union_row10.01, trial:i01.ug.Block4_union_row2.02, trial:i01.ug.Block4_union_row7.06, trial:i01.ug.Block4_union_row1.00). Instance moves are also confined to the x-direction in every accepted case across all unit_gate trials. The V2 repairs in trial:i05.cu.def:VIA_VIA23_1_3_36_36.00 exclusively use the x-axis for both moves and resizes.