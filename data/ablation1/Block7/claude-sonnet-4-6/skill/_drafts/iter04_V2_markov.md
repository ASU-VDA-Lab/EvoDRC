## Operation anatomy

Every accepted repair touching V2 co-moves or co-resizes M2 and M3 within the same operation set. The smallest observed touch set is {M2, M3, V2}, confirmed in trial:i02.ug.leaf_0010.13, trial:i03.ug.leaf_0002.07, and trial:i04.ug.leaf_0002.02, all single-instance translations of i1358. Accepted trials may additionally touch M1 and V1 (trial:i04.ug.Block7_union_row13.00, trial:i04.ug.leaf_0001.01, trial:i04.ug.leaf_0007.05, trial:i04.ug.leaf_0008.06); the {M2, M3, V2} minimum holds only when the repair scope is confined to a single via instance and its direct enclosing metals. This is structurally required by V2.AUX.1 (V2 must lie inside both M2 and M3) and V2.M3.AUX.2 (V2 width must equal M3 width perpendicular to the M3 length): translating V2 without co-translating its enclosing metal layers would immediately violate containment and the width-match constraint.

## Primary repair operation: move_instance

The dominant V2 repair operation is `move_instance`, used to translate cell instances bodily within their M2/M3 context. The smallest accepted trials each consist of a single `move_instance` operation: trial:i02.ug.leaf_0010.13 (instance i1358, delta [0, -36] dbu), trial:i03.ug.leaf_0002.07 (instance i1358, delta [0, +36] dbu), and trial:i04.ug.leaf_0002.02 (instance i1358, delta [-36, 0] dbu), all touching only M2/M3/V2. Larger repair loci involve batches of 3–9 instances moved together, often mixing x- and y-direction deltas in the same trial (trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row9.21, trial:i04.ug.leaf_0001.01).

`resize_end` operations on polygon endpoints appear as secondary adjustments and are never the sole operation in a V2-touching trial. Observed secondary `resize_end` patterns include: extending the high x-end of a polygon by +56 dbu alongside instance moves (trial:i01.ug.Block7_union_row12.02, trial:i04.ug.leaf_0008.06); shrinking the low x-end (trial:i01.ug.Block7_union_row9.21, -36 dbu; trial:i04.ug.leaf_0001.01, -40 dbu); extending the high x-end by +108 dbu (trial:i04.ug.leaf_0001.01, polygon p3696); raising or lowering y-ends by ±12–20 dbu (trial:i01.ug.Block7_union_row9.21, trial:i03.ug.Block7_union_row17.02, trial:i04.ug.leaf_0001.01); and moving or resizing polygon y-position by ±57–68 dbu alongside instance moves (trial:i02.ug.Block7_union_row17.02, trial:i03.ug.Block7_union_row17.02, trial:i04.ug.leaf_0007.05). The iter-4 trial:i04.ug.leaf_0007.05 introduced a resize_end on the high-y end of p2596 by +68 dbu coincident with y+68 moves on i0794, i0810, and p3631, confirming that polygon endpoint adjustments accompany even y-direction polygon translations when the enclosing metal boundary also shifts.

## Displacement magnitudes

Observed y-axis deltas for V2-touching instance and polygon moves across accepted trials:
- ±12 dbu: trial:i01.ug.Block7_union_row14.04 (instances i0519, i0524 moved y-12); trial:i04.ug.leaf_0001.01 (resize_end p2719 high-y, -12)
- ±16 dbu: trial:i02.ug.leaf_0023.16 (instances i0336, i0308, polygon p3516 moved y-16)
- ±36 dbu: trial:i02.ug.leaf_0010.13 (i1358 y-36); trial:i03.ug.leaf_0002.07 (i1358 y+36)
- ±52 dbu: trial:i01.ug.Block7_union_row19.09, trial:i02.ug.leaf_0032.17, trial:i03.ug.Block7_union_row19.03, trial:i04.ug.leaf_0008.06 (instances i0949, i0950)
- ±57 dbu: trial:i02.ug.Block7_union_row17.02 (polygon p3631 and instances i0794, i0810 y+57); trial:i03.ug.Block7_union_row17.02 (same objects y-57); trial:i04.ug.Block7_union_row13.00 (instances i0507, i0520 and polygon p3526 y-57)
- +64 dbu: trial:i01.ug.Block7_union_row14.04 (instances i0894, i0920)
- +68 dbu: trial:i04.ug.leaf_0007.05 (instances i0794, i0810, polygon p3631, resize_end p2596 high-y)

Observed x-axis deltas:
- -40 dbu: trial:i04.ug.leaf_0001.01 (resize_end p3297 low-x)
- -37 dbu: trial:i01.ug.Block7_union_row19.09 (instances i0026, i0294)
- -36 dbu: trial:i04.ug.leaf_0002.02 (instance i1358)
- +28 dbu: trial:i01.ug.Block7_union_row14.04 (instance i0874)
- +36 dbu: trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row9.21, trial:i03.ug.Block7_union_row17.02 (multiple instances)
- +37 dbu: trial:i01.ug.Block7_union_row19.09 (instance i0771); trial:i03.ug.Block7_union_row19.03 (instance i0294)
- +40 dbu: trial:i01.ug.Block7_union_row13.03
- +56 dbu: trial:i01.ug.Block7_union_row12.02 (resize_end); trial:i01.ug.Block7_union_row9.21; trial:i04.ug.leaf_0008.06 (resize_end p3608 high-x)
- +60 dbu: trial:i04.ug.leaf_0001.01 (instance i1144)
- +108 dbu: trial:i01.ug.Block7_union_row9.21 (instance i1117); trial:i04.ug.leaf_0001.01 (instance i1140, resize_end p3696 high-x)

The 36 dbu x-direction step recurs across multiple trials (trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row9.21, trial:i03.ug.Block7_union_row17.02, trial:i04.ug.leaf_0002.02) and matches the 18 nm minimum width from V2.W.1 and the 18 nm same-track minimum spacing from V2.S.1 at the implied 2 dbu/nm grid resolution.

## Oscillating instances and competing constraints

Instances i0949 and i0950 exhibit a four-iteration oscillation: moved y-52 dbu in trial:i01.ug.Block7_union_row19.09 (iter 1), moved y+52 dbu in trial:i02.ug.leaf_0032.17 (iter 2), moved y-52 dbu in trial:i03.ug.Block7_union_row19.03 (iter 3), and moved y+52 dbu again in trial:i04.ug.leaf_0008.06 (iter 4). All four were accepted with conn_preserved=true. The iter-4 trial additionally applied resize_end +56 dbu on the high-x end of polygon p3608, a secondary adjustment absent from the prior three iterations. The net y-displacement of i0949 and i0950 after four iterations remains zero relative to their iter-1 starting position. The periodic reintroduction of n_new_in_crop=4 (iter 2 and iter 4 both) confirms that the two competing DRC windows remain unresolved; each y-move closes one while reopening the other.

Do not apply an isolated y-direction move to i0949 or i0950 without simultaneously resolving the opposing-direction DRC window; the four-iteration history (trial:i01.ug.Block7_union_row19.09, trial:i02.ug.leaf_0032.17, trial:i03.ug.Block7_union_row19.03, trial:i04.ug.leaf_0008.06) shows such moves are individually accepted but reversed in the next iteration, producing non-converging oscillation.

Instance i1358 has accumulated moves across all four iterations: y+8 in iter 1 (trial:i01.ug.Block7_union_row12.02), y-36 in iter 2 (trial:i02.ug.leaf_0010.13), y+36 in iter 3 (trial:i03.ug.leaf_0002.07), and x-36 in iter 4 (trial:i04.ug.leaf_0002.02). The iter-4 move is purely x-direction (delta [-36, 0]), touching only M2/M3/V2, with n_new_in_crop=0. This indicates that after the y-oscillation resolved (iter-3 revert produced n_new_in_crop=0), a residual x-direction V2 spacing or width violation remained, addressed by the iter-4 x-36 move. The -36 dbu x-step aligns with the 18 nm grid spacing established by V2.W.1 and V2.S.1.

The Block7_union_row17 locus (instances i0794, i0810, polygon p3631) has oscillated across three iterations with escalating magnitudes: y+57 in iter 2 (trial:i02.ug.Block7_union_row17.02), y-57 with x+36 supplemental adjustments in iter 3 (trial:i03.ug.Block7_union_row17.02), and y+68 in iter 4 (trial:i04.ug.leaf_0007.05, logged under unit leaf_0007). The iter-4 displacement (+68 dbu) differs from the iter-2 displacement (+57 dbu) at the same locus objects, and was accompanied by resize_end +68 dbu on the high-y end of p2596. The unit_id change (Block7_union_row17 → leaf_0007) across iterations reflects that the same physical objects may be assigned to different scheduling units depending on the incoming design state; repair decisions at this locus must account for the full cumulative history of y-translations applied to i0794, i0810, and p3631, not just the most recent.

Block7_union_row13 reappeared in iter 4 (trial:i04.ug.Block7_union_row13.00) with a y-57 move on instances i0507 and i0520 and polygon p3526 (different objects from the iter-1 n_new_in_crop=1 trial at that unit), producing n_new_in_crop=0. This indicates the iter-4 repair at this locus achieved a clean closure, in contrast to the iter-1 trial that introduced one new in-crop violation.

## cu_pool resize_via_shape rejection

A `resize_via_shape` operation on the M3 shape of cell VIA_VIA23_1_3_36_36 (delta_y = -40 dbu on shape_index 0 of layer M3, shrinking the M3 end-cap) was rejected in trial:i02.cu.def:VIA_VIA23_1_3_36_36.00 with decision=rejected_net_positive and delta_total=0. Every measured window showed identical before- and after-violation counts. Do not attempt to fix V2.M3.EN.2 or V2.S.1 spacing violations for this via cell type by shrinking the M3 end-cap in the cu_pool channel; trial:i02.cu.def:VIA_VIA23_1_3_36_36.00 confirms this produces no measurable improvement.

## n_new_in_crop acceptance policy

The unit_gate channel accepts trials with conn_preserved=true regardless of n_new_in_crop count. Trials introducing 0, 1, or 4 new in-crop violations were all accepted and committed to the design state across all four iterations. Trials with n_new_in_crop=4 were accepted in iter 2 (trial:i02.ug.leaf_0032.17) and iter 4 (trial:i04.ug.leaf_0008.06), both involving i0949 and i0950; both are part of the oscillating-instance pattern. The iter-4 Block7_union_row13 trial (trial:i04.ug.Block7_union_row13.00) achieved n_new_in_crop=0, showing that loci previously carrying non-zero crop violations can be cleanly resolved in later iterations. New in-crop violations introduced by an accepted move persist as open DRC items for subsequent iterations.

## Design-state progression and inter-iteration interaction

Each iteration begins from the cumulative design state produced by all changes accepted in the prior iteration: iter 1 from state `8f6ee40c...`, iter 2 from `dfcb1ce2...`, iter 3 from `88d7f05b...`, iter 4 from `8895583b...`. Accepted instance moves in one iteration can directly contradict fixes applied in a prior iteration (as with i0949/i0950 and the Block7_union_row17 locus), because each iteration's unit windows are evaluated against the incoming state and may independently arrive at conflicting optima. When a locus reappears across multiple iterations, the iter-N repair should account for what all prior iterations committed at that locus rather than applying the same displacement again; the Block7_union_row17 locus shifted from ±57 dbu (iters 2–3) to +68 dbu (iter 4) on the same objects, indicating the optimizer converged on a different offset once x-direction adjustments from iter 3 were included in the incoming state.