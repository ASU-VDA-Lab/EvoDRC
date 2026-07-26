**Move increment granularity on M2**

All 10 unit_gate trials in iteration 1 used x-axis move deltas that are multiples of 36 dbu (values observed: 36, 108, and −36 dbu). Every such trial produced n_new_in_crop=0 and n_new_out_of_crop=0 for M2, with conn_preserved=true and decision=gated_in (trial:i01.ug.Block3_union_row1.00, trial:i01.ug.Block3_union_row2.01, trial:i01.ug.Block3_union_row5.02, trial:i01.ug.Block3_union_row8.03, trial:i01.ug.leaf_0006.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0008.06, trial:i01.ug.leaf_0009.07, trial:i01.ug.leaf_0012.08, trial:i01.ug.leaf_0013.09). Use multiples of 36 dbu as the move step when repositioning instances to avoid introducing new M2 violations.

**Negative x-axis moves are safe at the 36 dbu step**

A negative x move of −36 dbu (trial:i01.ug.leaf_0013.09) produced zero new M2 violations with conn_preserved=true. Move direction (positive or negative x) does not determine M2 DRC outcome at 36 dbu step granularity.

**Mixed per-instance deltas within a single operation do not cause M2 violations**

Trial:i01.ug.Block3_union_row1.00 moved three instances with deltas of 36, 108, and 108 dbu on the x-axis in one operation; trial:i01.ug.Block3_union_row8.03 moved four instances with deltas of 36, 108, 36, and 36 dbu. Both produced n_new_in_crop=0 and n_new_out_of_crop=0. Applying non-uniform move amounts across instances within one repair does not introduce M2 violations provided every individual delta is a multiple of 36 dbu and connectivity is preserved.

**Single-polygon resize_end on M2 combined with instance moves**

In trial:i01.ug.leaf_0008.06, a resize_end on M2 polygon p1261 (axis x, high end, +36 dbu) was applied alongside two move_instance ops (each +36 dbu x), touching M1, M2, and V1. The result was n_new_in_crop=0 and n_new_out_of_crop=0. Extending the high-x end of an M2 polygon by 36 dbu in combination with instance moves does not introduce new M2 violations when connectivity is preserved.

**V2 via widening by 288 dbu reduces V2.M2.EN.1 violations**

Trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 applied x-axis resizes of +288 dbu per V2 shape on cell VIA_VIA23_1_3_36_36 together with asymmetric repositioning moves (−144 dbu and +144 dbu on separate shapes), touching M2, M3, and V2. The operation reduced total DRC violations by 27 (leaf_0018: 32→17; leaf_0019: 35→23) and was applied with conn_preserved=true. Widening V2 via shapes on the x-axis by 288 dbu with repositioning moves of ±144 dbu is an effective repair for V2.M2.EN.1 violations arising from insufficient M2 enclosure of V2 on two opposite sides.