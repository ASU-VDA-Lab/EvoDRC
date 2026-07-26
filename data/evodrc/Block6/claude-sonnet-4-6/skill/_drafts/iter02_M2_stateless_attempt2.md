## Operation Axis

All M2-touching move_instance operations in this history carry delta_dbu of the form `[X, 0]`; no Y-component appears in any accepted trial (trial:i01.ug.Block6_union_row3.00, trial:i01.ug.Block6_union_row5.01, trial:i01.ug.Block6_union_row7.02, trial:i01.ug.Block6_union_row8.03, trial:i01.ug.leaf_0001.04, trial:i01.ug.leaf_0011.05, trial:i01.ug.leaf_0015.06, trial:i01.ug.leaf_0018.07, trial:i02.ug.Block6_union_row4.00, trial:i02.ug.Block6_union_row7.01, trial:i02.ug.Block6_union_row8.02, trial:i02.ug.leaf_0004.04). Apply X-axis instance moves when targeting M2 violations; every such move was accepted with zero new violations in the crop window.

## Accepted Move Step Sizes

Move deltas along X that were accepted range from 4 dbu to 112 dbu. Specific accepted values: 4 dbu (trial:i02.ug.Block6_union_row7.01), 8 dbu (trial:i02.ug.Block6_union_row8.02), 28 dbu (trial:i01.ug.leaf_0015.06), 36 dbu (trial:i01.ug.Block6_union_row5.01, trial:i01.ug.Block6_union_row8.03, trial:i01.ug.leaf_0011.05, trial:i01.ug.leaf_0018.07, trial:i02.ug.Block6_union_row8.02), 56 dbu (trial:i02.ug.Block6_union_row4.00), 72 dbu (trial:i01.ug.Block6_union_row3.00, trial:i02.ug.leaf_0004.04), 104 dbu (trial:i01.ug.Block6_union_row7.02), 112 dbu (trial:i01.ug.leaf_0001.04, trial:i02.ug.Block6_union_row4.00). A negative-direction move of -36 dbu was also accepted within the same trial as a +104 dbu move on a different instance (trial:i01.ug.Block6_union_row7.02).

## Polygon End Resizing

When instance moves are paired with polygon end extensions, apply resize_end on axis:x. Accepted end:high extension deltas: 48 dbu (trial:i01.ug.leaf_0015.06), 92 dbu (trial:i01.ug.Block6_union_row5.01), 124 dbu (trial:i01.ug.Block6_union_row7.02), 132 dbu (trial:i01.ug.leaf_0001.04, trial:i02.ug.Block6_union_row4.00). A concurrent end:low shrink of 56 dbu on a separate polygon alongside a 124 dbu end:high extension on another polygon was accepted in the same trial (trial:i01.ug.Block6_union_row7.02). All resize_end operations in this history act on axis:x only. Pair resize_end with the move_instance in the same trial; every trial combining both op types was accepted with zero new violations in crop (trial:i01.ug.Block6_union_row5.01, trial:i01.ug.Block6_union_row7.02, trial:i01.ug.leaf_0001.04, trial:i01.ug.leaf_0015.06, trial:i02.ug.Block6_union_row4.00).

## Multi-Instance Grouping

Move multiple instances in a single trial when they occupy the same locus. Up to five move_instance operations appear together in one accepted trial (trial:i01.ug.Block6_union_row5.01). Trials combining three move_instance ops were accepted in trial:i01.ug.Block6_union_row3.00 and trial:i01.ug.leaf_0015.06; two move_instance ops together were accepted in trial:i01.ug.Block6_union_row4.00 and trial:i02.ug.Block6_union_row8.02. In every multi-instance trial, conn_preserved remained true and n_new_in_crop was zero.

## V1 Co-movement

Every unit_gate trial touching M2 also touches V1 in touched_layers (trial:i01.ug.Block6_union_row3.00 through trial:i02.ug.leaf_0004.04). No separate via adjustment was needed in any of these trials; the V1 via moves with its parent instance and stays inside the M2 segment. Every such trial was accepted with conn_preserved:true and zero new violations, confirming that co-moving instance-embedded V1 vias with M2 satisfies V1.M2.EN.2 and V1.M2.AUX.2 without additional intervention.

## Via Cell Reshaping (cu_pool Channel)

The cu_pool trial (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00) reduced total violations by 78 (leaf_0019: -42, leaf_0020: -36) by reshaping V2 shapes inside via cell VIA_VIA23_1_3_36_36, touching M2, M3, and V2. Operations: move_via_shape on V2 by -144 dbu and +144 dbu along X, combined with resize_via_shape on V2 by +264 dbu, +288 dbu, and +264 dbu along X. Use move_via_shape and resize_via_shape on V2 within the via cell definition when M2/V2 enclosure violations cluster across multiple instances of the same via cell; this propagates the fix globally to all placements.

## Iteration-to-Iteration Residuals

Iter-2 trials revisit units that were already addressed in iter-1 (Block6_union_row7 in trial:i01.ug.Block6_union_row7.02 and again in trial:i02.ug.Block6_union_row7.01; Block6_union_row8 in trial:i01.ug.Block6_union_row8.03 and again in trial:i02.ug.Block6_union_row8.02). The iter-2 residual moves are smaller (4 dbu and 8 dbu respectively) than the iter-1 moves (104/-36 dbu and 36 dbu). Apply a second, smaller correction to units with residual violations after the first iteration rather than treating them as already clean.