## Iteration 1 — M1 Operation Summary

All seven trials in this iteration were accepted (`decision: gated_in`) with no new violations introduced in crop and no new violations outside crop (`n_new_in_crop: 0`, `n_new_out_of_crop: 0`). Connectivity was preserved in every case (`conn_preserved: true`). The full set of accepted trial IDs is: trial:i01.ug.Block2_union_row1.00, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0001.03, trial:i01.ug.leaf_0004.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0011.06.

## Operation Classes Observed on M1

**move_instance.** Instance moves along the x-axis (delta_dbu in the x direction, zero y-component) on M1-touching units were accepted in every trial where they appeared. Single-instance moves of 36 dbu were accepted in trial:i01.ug.leaf_0004.04 and trial:i01.ug.leaf_0007.05. Multi-instance moves of 36 dbu (two instances simultaneously) were accepted in trial:i01.ug.Block2_union_row1.00 and trial:i01.ug.leaf_0011.06. A multi-instance move of 64 dbu (three instances) was accepted in trial:i01.ug.Block2_union_row5.02. A multi-instance move of 128 dbu (one instance, combined with resize) was accepted in trial:i01.ug.leaf_0001.03. Apply instance moves at a granularity consistent with the site grid — the 36 dbu and 64 dbu steps used in trials trial:i01.ug.Block2_union_row1.00 through trial:i01.ug.leaf_0011.06 all satisfied M1.W.1, M1.S.1, and via enclosure rules without introducing new errors.

**resize_end.** Polygon-end resizes along the x-axis (`axis: x`) on M1 polygons were accepted when paired with corresponding instance moves in trial:i01.ug.Block2_union_row3.01 (one resize, +36 dbu on the high end of p1040), trial:i01.ug.Block2_union_row5.02 (two resizes, +64 dbu on the high ends of p1059 and p1057), trial:i01.ug.leaf_0001.03 (two resizes: +184 dbu on high end of p1065 and +176 dbu on the low end of p957), and trial:i01.ug.leaf_0011.06 (one resize, +36 dbu on the high end of p1052). Always pair a resize_end with the associated instance move that shifts the via stack, as done in trial:i01.ug.Block2_union_row3.01 and trial:i01.ug.leaf_0011.06; unpaired resizes were not tested and are not in the accepted record.

## M1 Enclosure of V0 and V1

V0 enclosure (rule V0.M1.EN.1) and V1 enclosure (rule V1.M1.EN.1) require enclosure on two opposite sides. All accepted trials touched both M1 and V1 layers simultaneously. When resizing an M1 polygon end in the direction of a via move, extend the M1 high end by at least the instance move delta, as demonstrated in trial:i01.ug.Block2_union_row3.01 (resize +36 dbu matches move +36 dbu) and trial:i01.ug.Block2_union_row5.02 (resize +64 dbu matches move +64 dbu). This preserves enclosure on the side that would otherwise be exposed by the move. In trial:i01.ug.leaf_0001.03, the asymmetric resizes (+184 dbu high, +176 dbu low) together with the 128 dbu instance move were accepted, confirming that the resize deltas can exceed the move delta when additional enclosure margin is needed.

## M1 Width and Spacing

No trial introduced a new M1.W.1 (minimum width 18 nm) or M1.S.1/M1.S.2/M1.S.3 spacing violation. Use resize_end magnitudes that maintain the existing M1 wire width — all resize operations in the accepted trials extended rather than contracted M1 polygon ends (all delta_dbu values on resize_end were positive), as seen in trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0001.03, and trial:i01.ug.leaf_0011.06.

## V0.M1.AUX.3 (M1-Width-Matched Vias)

V0 must be exactly the same width as M1 in the direction perpendicular to M1 length. All accepted trials preserved this relationship by moving instances rather than independently resizing the via polygon — the via and surrounding M1 moved together in trial:i01.ug.Block2_union_row1.00, trial:i01.ug.leaf_0004.04, and trial:i01.ug.leaf_0007.05 (move_instance only, no resize). Do not resize M1 in the direction perpendicular to its length without a matching via resize; no such perpendicular resize appeared in any accepted trial.

## Multi-Layer Coupling

M1 changes consistently co-touched M2 and V1 (all seven trials). trial:i01.ug.leaf_0001.03 additionally touched M4, showing that instance moves propagate up the via stack. When moving an instance that spans multiple metal layers, include all relevant polygon resizes on M1 to maintain enclosure at the M1-V0 and M1-V1 interfaces, as done in trial:i01.ug.leaf_0001.03 and trial:i01.ug.Block2_union_row5.02.

## M1.A.1 (Minimum Area 504 nm-sq) and M1.R.0 (Redundant Island)

No M1.A.1 or M1.R.0 violations were introduced in any accepted trial. Resize_end operations that increase M1 polygon length (as in all accepted resize trials) increase area and move away from minimum-area risk. Avoid resize_end operations that shorten M1 polygons below the area threshold; no such contraction was performed in any accepted trial.

## NONORTHOGONAL Constraint

All accepted operations were axis-aligned (x-axis moves and resizes only; zero y-delta on all move_instance ops). Do not introduce diagonal polygon edges on M1. Every accepted operation in this iteration — trial:i01.ug.Block2_union_row1.00 through trial:i01.ug.leaf_0011.06 — used orthogonal-only geometry, consistent with the NONORTHOGONAL block that applies to M1.