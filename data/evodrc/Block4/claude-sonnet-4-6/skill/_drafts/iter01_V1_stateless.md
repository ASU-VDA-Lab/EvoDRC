## Operation Vocabulary Observed in Iteration 1

All ten accepted repairs in this iteration used three operation types on V1-touching units: `move_instance` (horizontal displacement only), `add_polygon` on M2, and `resize_end` on M2 polygon boundaries. Every `move_instance` delta had a zero y-component; no vertical instance displacement occurred in any trial (trial:i01.ug.Block4_union_row1.00, trial:i01.ug.Block4_union_row3.03, trial:i01.ug.Block4_union_row5.04, trial:i01.ug.Block4_union_row6.05, trial:i01.ug.leaf_0008.08, trial:i01.ug.leaf_0020.09, trial:i01.ug.leaf_0021.10). Do not apply vertical moves to resolve V1 DRC violations; the measured record contains no successful y-axis displacements.

## Instance Move Magnitudes

The most frequent single-step horizontal displacement is 36 dbu, appearing as the sole or one of several move operations in trial:i01.ug.Block4_union_row2.02, trial:i01.ug.Block4_union_row3.03, trial:i01.ug.Block4_union_row5.04 (one of four moves), trial:i01.ug.Block4_union_row6.05, trial:i01.ug.Block4_union_row7.06 (two of four moves), trial:i01.ug.leaf_0008.08, trial:i01.ug.leaf_0020.09, trial:i01.ug.leaf_0021.10. Larger displacements (64, 108, 112, -28 dbu) appear in trials with higher op-counts, such as trial:i01.ug.Block4_union_row1.00 (112 and 36 dbu), trial:i01.ug.Block4_union_row10.01 (108, -108, 36 dbu), and trial:i01.ug.Block4_union_row7.06 (108, -28, 36, 36 dbu). Prefer 36 dbu as the starting move quantum; use larger steps only when multiple instances must be separated beyond what a single 36 dbu step achieves.

## Bidirectional Instance Moves to Create Symmetric Separation

When two adjacent V1-hosting instances violate spacing, move them in opposite horizontal directions rather than moving only one. trial:i01.ug.Block4_union_row3.03 moved i0170 by [-36,0] and i0292 by [36,0], sharing the separation burden symmetrically. trial:i01.ug.Block4_union_row10.01 moved i0025 by [108,0] and i0041 by [-108,0], again in opposite directions. Both trials were accepted with zero new violations. Avoid moving a single instance by the full required gap when a symmetric split is geometrically feasible; the measured record shows symmetric splits succeed without generating new enclosure or spacing violations on the non-moved neighbor.

## M2 Polygon Additions Required After Instance Moves

Moving a V1-bearing instance horizontally can leave a gap in M2 coverage, violating V1.M2.EN.2 (minimum enclosure of V1 by M2 on two opposite sides is 5 & 5 nm or 5 & 0 nm) or V1.AUX.1 (V1 must be inside M2). In trial:i01.ug.Block4_union_row1.00, after moving i0265 by 112 dbu and i0325 by 36 dbu, two M2 patches were added: [[9252,3024],[9444,3024],[9444,3096],[9252,3096]] (192 dbu wide, 72 dbu tall) and [[12132,3024],[12224,3024],[12224,3096],[12132,3096]] (92 dbu wide, 72 dbu tall). Always add or extend M2 to re-cover V1 instances that have been displaced beyond the original M2 boundary.

## M2 resize_end Operations Accompany Instance Moves

Several accepted trials combined instance moves with `resize_end` operations on M2 polygon ends (x axis, high or low end) rather than adding entirely new polygons. trial:i01.ug.Block4_union_row10.01 extended p1551 high-end by 128 dbu, p1589 low-end by 72 dbu, p1605 high-end by 92 dbu, and p1379 low-end by 64 dbu alongside the instance moves. trial:i01.ug.Block4_union_row2.02 extended p1548 high-end by 56 dbu and p1569 high-end by 92 dbu. trial:i01.ug.Block4_union_row7.06 extended four M2 polygons (56 to 172 dbu). All resize_end operations were on the x axis and always extended (positive delta_dbu) rather than contracted a polygon end. Do not shrink M2 polygon ends when repairing V1 violations; the measured record contains only extensions.

## All Iteration-1 Repairs Were Accepted with Zero New Violations

Every trial in this iteration received decision `gated_in` with `conn_preserved: true` and `n_new_in_crop: 0`, `n_new_out_of_crop: 0` (trial:i01.ug.Block4_union_row1.00 through trial:i01.ug.leaf_0021.10). The repair strategy of combining horizontal instance moves with M2 extension or M2 patch insertion consistently avoided introducing new DRC markers both inside and outside the repair crop window. Use this compound strategy—move then extend/patch M2—as the baseline approach for V1 repairs.

## Layer Touch Pattern: M1 and M2 Always Co-Touched with V1

Every trial that touched V1 also touched M1 and M2 (trial:i01.ug.Block4_union_row1.00 through trial:i01.ug.leaf_0021.10). Four trials additionally touched M4 (trial:i01.ug.Block4_union_row10.01, trial:i01.ug.Block4_union_row7.06). V1 moves propagate enclosure constraints upward to M2 and downward to M1; repairs that touch V1 must always verify V1.M1.EN.1 (minimum enclosure of V1 by M1 on two opposite sides is 5 & 2 nm) and V1.M2.EN.2 in the same operation set. Never treat a V1 move as a single-layer edit.

## Connectivity Is Preserved Through Move-Plus-Extend Strategy

The `conn_preserved: true` flag and `reason: "conn_preserved"` gating condition held for all ten trials. The combination of instance moves with M2 polygon extensions (resize_end) or new M2 patches maintains the electrical connections that V1 instances bridge between M1 and M2. Do not move a V1-hosting instance without simultaneously ensuring M2 still covers that instance on two opposite sides (satisfying V1.M2.AUX.2: V1 must be exactly the same width as M2 along the direction perpendicular to M2 length), as disconnection would cause the repair to be rejected by the connectivity gate.

## Op-Count Scales with Locus Width

Single-instance, narrow-locus units required only one operation: trial:i01.ug.leaf_0008.08 (locus width ~848 dbu, 1 op), trial:i01.ug.leaf_0020.09 (locus width ~200 dbu, 1 op), trial:i01.ug.leaf_0021.10 (locus width ~848 dbu, 1 op). Wider multi-instance loci required more operations: trial:i01.ug.Block4_union_row1.00 (locus width ~3656 dbu, 4 ops), trial:i01.ug.Block4_union_row10.01 (locus width ~7112 dbu, 7 ops), trial:i01.ug.Block4_union_row7.06 (locus width ~8668 dbu, 8 ops). Allocate op budget proportionally to locus width; narrow single-V1 cases resolve with one move, while wide rows with multiple V1 instances require coordinated move-and-extend sequences across several polygons.