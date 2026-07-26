## Operation Patterns

The dominant corrective operation across all 13 trials is `move_instance` in the +x direction by 36 dbu. This step appears in trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row10.01, trial:i01.ug.Block1_union_row3.03, trial:i01.ug.Block1_union_row4.04, trial:i01.ug.Block1_union_row5.05, trial:i01.ug.Block1_union_row8.07, trial:i01.ug.Block1_union_row9.08, trial:i01.ug.leaf_0004.09, and trial:i02.ug.Block1_union_row6.01. No trial moves instances exclusively in the y direction; all observed y-component deltas are incidental to x-primary moves (trial:i01.ug.Block1_union_row4.04 includes a delta of [36, -36] for instance i0300 alongside three pure-x moves).

`resize_end` on the x-axis (end:high or end:low) accompanies `move_instance` in multi-op trials. Observed resize deltas on the high end: 128 dbu and 92 dbu (trial:i01.ug.Block1_union_row1.00), 92 dbu (trial:i01.ug.Block1_union_row3.03), 52 dbu (trial:i01.ug.Block1_union_row4.04), 36 dbu (trial:i01.ug.Block1_union_row5.05). Observed resize deltas on the low end: 36 dbu (trial:i01.ug.Block1_union_row5.05, trial:i01.ug.leaf_0020.10). A symmetric `resize` (no end qualifier) of 36 dbu appears in trial:i01.ug.leaf_0031.11. No trial applies `resize_end` as the sole operation without any accompanying `move_instance`.

A `delete_instance` + `add_via` pair appears in trial:i02.ug.leaf_0004.02, where a via instance was deleted and a replacement via was inserted at a new origin within the same locus. This pattern was not used in any iteration-1 trial and represents the only non-move, non-resize corrective operation in the recorded history.

## Gating and New-Violation Tolerance

Every trial in this history received decision:gated_in. Trials that introduced new in-crop DRC violations were accepted when conn_preserved:true:

- trial:i01.ug.Block1_union_row1.00: n_new_in_crop=4, gated_in
- trial:i01.ug.Block1_union_row6.06: n_new_in_crop=1, gated_in
- trial:i01.ug.leaf_0031.11: n_new_in_crop=4, gated_in
- trial:i02.ug.Block1_union_row6.01: n_new_in_crop=1, gated_in

The stated reason in all four cases is "conn_preserved". No trial with conn_preserved:true was rejected in these records. No trial produced out-of-crop violations (n_new_out_of_crop=0 across all 13 trials).

## Layer Co-modification

Every trial lists touched_layers as ["M1","M2","V1"]. M1 is never modified in isolation from V1 and M2 in this history (trial:i01.ug.Block1_union_row1.00 through trial:i02.ug.leaf_0004.02). When M1 geometry is extended or an instance moved, V1 and M2 change in the same trial. Repair operations that adjust M1 must account for the V1 enclosure constraints (V0.M1.EN.1, V1.M1.EN.1) and the co-planarity constraint (V0.M1.AUX.3), which require coordinated adjustment of the via layers.

## Move Delta Grid

Observed x-axis move_instance deltas: +36 dbu (most frequent, trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row10.01, trial:i01.ug.Block1_union_row3.03, trial:i01.ug.Block1_union_row4.04, trial:i01.ug.Block1_union_row5.05, trial:i01.ug.Block1_union_row8.07, trial:i01.ug.Block1_union_row9.08, trial:i01.ug.leaf_0004.09, trial:i02.ug.Block1_union_row6.01); +108 dbu (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row8.07); -36 dbu (trial:i01.ug.Block1_union_row5.05, trial:i01.ug.Block1_union_row8.07); -32 dbu (trial:i01.ug.Block1_union_row6.06, trial:i01.ug.Block1_union_row8.07). The value 108 dbu equals 3 × 36 dbu. The value -32 dbu departs from the 36-dbu step and is the only non-multiple-of-36 observed.

## Persistent Locus: Block1_union_row6

Locus [8152, 7668, 13752, 8532] was targeted in both iterations. In iteration 1, trial:i01.ug.Block1_union_row6.06 moved instance i0455 by [-32, 0] in a single operation and produced 1 new in-crop violation. In iteration 2, trial:i02.ug.Block1_union_row6.01 applied 5 move_instance operations across instances i0097, i0434, i0455, i0436, and i0116 and still produced 1 new in-crop violation. Two iterations of repair at this locus have not eliminated new in-crop violations. The iter2 trial operated on a new design_state (45ca183...) distinct from the iter1 state (796a626...), confirming the iter2 attempt incorporated all iter1 changes before retrying.

## Operation Count and Violation Count Relationship

Trial op counts range from 1 (trial:i01.ug.Block1_union_row6.06, trial:i01.ug.leaf_0004.09) to 5 (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row5.05, trial:i01.ug.Block1_union_row8.07, trial:i02.ug.Block1_union_row6.01). Single-op trials produce either 0 new violations (trial:i01.ug.leaf_0004.09) or 1 new violation (trial:i01.ug.Block1_union_row6.06). Higher op counts do not guarantee fewer new violations: the 5-op trial:i01.ug.Block1_union_row1.00 introduced 4 new in-crop violations; the 5-op trial:i02.ug.Block1_union_row6.01 introduced 1. The 5-op trial:i01.ug.Block1_union_row5.05, trial:i01.ug.Block1_union_row8.07 both produced 0 new violations.

## Design State Transitions Between Iterations

All iteration-1 trials share design_state "796a62668ac7e368d71fcb67038c38c1b27a9a85bb6eda7a3ee1f1ebd18ab3b3" (trial:i01.ug.Block1_union_row1.00 through trial:i01.ug.leaf_0031.11). Both iteration-2 trials share design_state "45ca183ccc1fc881ea2e08566a587dc0ed38475ce80051eafe6d0dd3fc5024e7" (trial:i02.ug.Block1_union_row6.01, trial:i02.ug.leaf_0004.02). The state change between iterations confirms that iteration-1 operations collectively modified the layout before iteration-2 trials began.