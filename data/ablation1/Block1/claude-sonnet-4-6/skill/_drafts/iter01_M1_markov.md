**Gating criterion and acceptance pattern**

In iteration 1, all 11 trials were accepted (decision: gated_in) solely on the basis of conn_preserved=true. DRC cleanliness within the crop window is not a gating condition: trials i01.ug.Block1_union_row1.00 (n_new_in_crop=4), i01.ug.Block1_union_row6.06 (n_new_in_crop=1), and i01.ug.leaf_0031.11 (n_new_in_crop=4) were all accepted despite introducing new violations inside the crop. Across all 11 trials, n_new_out_of_crop=0 — repair operations do not push M1 violations outside the crop boundary.

**Move step sizes on M1**

The dominant move step is 36 dbu on the x-axis, applied successfully across every row unit tested: trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row3.03, trial:i01.ug.Block1_union_row4.04, trial:i01.ug.Block1_union_row5.05, trial:i01.ug.Block1_union_row8.07, trial:i01.ug.Block1_union_row9.08, trial:i01.ug.leaf_0004.09. Negative x moves at -36 dbu are also accepted when connectivity is preserved (trial:i01.ug.Block1_union_row5.05, trial:i01.ug.Block1_union_row8.07, trial:i01.ug.leaf_0020.10). Larger moves are accepted in the same channel: 108 dbu (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row8.07) and -32 dbu (trial:i01.ug.Block1_union_row6.06, trial:i01.ug.Block1_union_row8.07). One trial used a combined x+y move ([36,-36] dbu) and was accepted (trial:i01.ug.Block1_union_row4.04).

**resize_end operations on M1**

X-axis resize_end on the high end is accepted at multiple delta values: 128 dbu (trial:i01.ug.Block1_union_row1.00), 92 dbu (trial:i01.ug.Block1_union_row3.03), 52 dbu (trial:i01.ug.Block1_union_row4.04), and 36 dbu (trial:i01.ug.Block1_union_row5.05). Resize_end on the low end at 36 dbu x is also accepted (trial:i01.ug.Block1_union_row5.05, trial:i01.ug.leaf_0020.10). A symmetric resize (axis unspecified, delta 36 dbu) on polygon p1390 was accepted (trial:i01.ug.leaf_0031.11). Resize_end and move_instance operations on M1 are freely combined within a single trial: see trial:i01.ug.Block1_union_row1.00 (2 moves + 2 resize_ends), trial:i01.ug.Block1_union_row5.05 (3 moves + 2 resize_ends), trial:i01.ug.leaf_0020.10 (1 move + 1 resize_end).

**Layer co-movement**

All 11 accepted trials touched layers M1, M2, and V1 together. No trial in this iteration modified M1 in isolation. This indicates that M1 instance moves and polygon resizes are performed as part of multi-layer operations that include V1 and M2, maintaining via enclosure relationships (rules V0.M1.EN.1 and V1.M1.EN.1) across the move.

**Op count**

Accepted trials range from 1 op (trial:i01.ug.Block1_union_row6.06, trial:i01.ug.leaf_0004.09) to 5 ops (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row5.05, trial:i01.ug.Block1_union_row8.07). There is no op-count ceiling observed at iteration 1.