## Operation grid and step sizes

All accepted trials in this iteration used move_instance deltas that are integer multiples of 36 dbu on the x-axis, with no y component: 36, 72 (not observed), and 108 dbu steps appear across trial:i01.ug.Block3_union_row1.00 (36 and 108 dbu moves), trial:i01.ug.Block3_union_row2.01 (36 dbu), trial:i01.ug.Block3_union_row5.02 (36 dbu), trial:i01.ug.Block3_union_row8.03 (36 and 108 dbu), and the leaf-unit trials (trial:i01.ug.leaf_0006.04 through trial:i01.ug.leaf_0013.09). Do not use sub-36 dbu deltas for M1 move operations; every accepted move in the full history snaps to this grid.

Negative x moves are safe when connectivity is preserved: trial:i01.ug.leaf_0013.09 used delta_dbu [-36, 0] on a single instance and was accepted with zero new violations.

## Resize operations on M1

A resize_end operation extending the high-x end of an M1 polygon by 36 dbu (axis x, end high, delta_dbu 36, polygon p1261) was accepted without introducing any new crop violations in trial:i01.ug.leaf_0008.06. This trial combined two move_instance ops with one M1 resize and still achieved n_new_in_crop=0, n_new_out_of_crop=0. Do not resize M1 ends by amounts smaller than 36 dbu; no sub-grid resize was accepted in any trial.

## Multi-instance moves and layer co-movement

All accepted trials touch layers M1, M2, and V1 together; no trial moved M1 in isolation. When moving instances to repair M1 rules, the enclosing V1 and the M2 above must move with the instance to avoid introducing new V1.M1.EN.1 or M1 spacing violations. Trial:i01.ug.Block3_union_row1.00 (3 instances, M1+M2+V1), trial:i01.ug.Block3_union_row8.03 (4 instances, M1+M2+V1), and trial:i01.ug.leaf_0008.06 (2 instances + 1 resize, M1+M2+V1) all confirm this pattern.

## Zero-violation acceptance criterion

Every trial in this iteration was accepted under the gated_in decision with n_new_in_crop=0 and n_new_out_of_crop=0, covering a range of 1 to 4 simultaneous instance moves per trial (trial:i01.ug.leaf_0009.07 and trial:i01.ug.leaf_0012.08 used single-instance moves; trial:i01.ug.Block3_union_row8.03 used four). No trial in this history was rejected. Connectivity was preserved in every case (conn_preserved: true for trial:i01.ug.Block3_union_row1.00 through trial:i01.ug.leaf_0013.09). Do not accept a move that breaks connectivity even if it clears a DRC violation; the gated_in decision in all recorded trials required conn_preserved=true.

## Rule applicability notes (V0/V1 enclosure)

V0.M1.EN.1 requires M1 to enclose V0 by 5 nm on two opposite sides in projection (the 5&5 or 5&0 case). V1.M1.EN.1 requires M1 to enclose V1 by 5 nm and 2 nm on opposite sides. Because all accepted trials co-move M1 with V1 geometry, the relative enclosure between M1 and the via does not change under a pure instance translation. The resize_end operation in trial:i01.ug.leaf_0008.06 extended M1 in x by 36 dbu, which can increase enclosure on the extended side without reducing it on the opposite side, and this was accepted cleanly.

V0.M1.AUX.3 flags V0 whose horizontal or vertical edges are not coincident with M1 edges. Pure instance moves that shift both V0 and M1 together do not alter this coincidence relationship; all accepted move_instance trials confirm this.

## M1 spacing and width rules

M1.W.1 sets a minimum width of 18 nm. M1.S.1 sets minimum side-to-side spacing of 18 nm for edges longer than 36 nm. M1.S.2 sets tip-to-side spacing of 25 nm. M1.S.3 sets tip-to-tip spacing of 27 nm for edges in the 24–36 nm range. M1.S.4 and M1.S.5 set 31 nm tip-to-tip spacing for narrower tips. M1.S.6 sets 20 nm corner-to-corner spacing. M1.A.1 sets a 504 nm² minimum area. No trial in this history was accepted with n_new_in_crop > 0, so every accepted move confirmed that the resulting M1 geometry did not create new violations of any of these rules within the cropped evaluation region. When moving instances by 36 dbu in x, the relative spacing between M1 wires within the same instance remains unchanged; only M1-to-M1 spacing between different instances is affected, and all inter-instance gaps after the moves remained clean.