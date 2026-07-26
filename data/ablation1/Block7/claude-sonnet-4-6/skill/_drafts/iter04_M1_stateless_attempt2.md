## Repair operation taxonomy

The complete set of operations recorded on layer M1 across all four iterations is: `move_instance`, `resize_end` (adjusting one edge of a named polygon), and `move` (translating an entire named polygon). No other operation type appears on M1 in this history. trial:i01.ug.Block7_union_row15.05 applied seven `move_instance` operations with no polygon operation at all; trial:i01.ug.Block7_union_row9.21 combined instance moves with both a `resize_end` and a polygon `move` on two separate polygons in the same transaction.

## Dominant move grid

Instance moves on M1 use a delta_dbu of exactly 36 in the x-direction in the majority of accepted trials: trial:i01.ug.Block7_union_row11.01, trial:i01.ug.Block7_union_row15.05, trial:i01.ug.Block7_union_row18.08, trial:i01.ug.Block7_union_row20.10, trial:i02.ug.Block7_union_row6.08, trial:i02.ug.Block7_union_row13.00, trial:i02.ug.Block7_union_row14.01, trial:i02.ug.Block7_union_row23.06, trial:i03.ug.Block7_union_row24.05, and others all apply [36,0]. Non-36 deltas appear for finer corrections: trial:i01.ug.Block7_union_row10.00 used [4,0] alongside a +50 resize; trial:i01.ug.Block7_union_row6.18 used [28,0]; trial:i01.ug.Block7_union_row13.03 used [40,0]. When multiple instances must be relocated in the same unit, apply the same delta to all of them in the same operation rather than splitting into separate passes, as seen in trial:i01.ug.Block7_union_row15.05 (seven instances, all [36,0]) and trial:i01.ug.Block7_union_row9.21 (four instances at [36,0] and two at [56,0]).

## Mixed-direction instance displacement for spacing violations

M1 spacing rules M1.S.1 through M1.S.6 require minimum separations ranging from 18 nm (side-to-side, edges >36 nm) up to 31 nm (tip-to-tip, edges <24 nm). When adjacent M1 wires violate spacing, moving all instances in the same direction propagates the violation to the far neighbor; instead, displace instances in opposing directions. trial:i01.ug.Block7_union_row16.06 moved i0407 and i0928 by [-36,0] while moving i0320 by [40,0], spreading the local cluster bidirectionally. trial:i01.ug.Block7_union_row8.20 moved i1405 and i1921 by [64,0] while i1891 moved by [-36,0]. trial:i01.ug.Block7_union_row9.21 moved four instances by [36,0], two by [56,0], and one by [108,0], with an opposing M1 polygon contraction at p3300 (axis=x, delta=-36, end=low) to eliminate the space at the vacated side.

## Enclosure rule V0.M1.EN.1: lateral (x-axis) repairs

V0.M1.EN.1 requires M1 to enclose V0 by at least 5 nm on two opposite sides. When an instance carrying V0 is moved along the M1 wire's long (x) axis, extend the M1 polygon's far end by at least the move magnitude. trial:i01.ug.Block7_union_row12.02 moved instance i1208 by [36,0] and extended p3273 high-x by 56 dbu. trial:i01.ug.Block7_union_row3.15 moved i1623 by [-36,0] and extended p3379 high-x by 49 dbu. trial:i01.ug.leaf_0002.23 moved i1646 by [72,0] and extended p3695 high-x by 128 dbu. trial:i01.ug.leaf_0008.24 moved i1968 by [108,0] and i1964 by [40,0] while extending p3771 high-x by 164 dbu. In all four cases the resize_end end="high" on the x-axis absorbed the via displacement.

The end="low" direction is used when the polygon must be contracted on the trailing side after a via moves away. trial:i01.ug.Block7_union_row9.21 contracted p3300 low-x by 36 dbu (axis=x, delta=-36, end=low) alongside a full polygon move on p2720 of +56 dbu. trial:i04.ug.leaf_0001.01 applied resize_end (axis=x, delta=-40, end=low) on p3297 and resize_end (axis=x, delta=108, end=high) on p3696 simultaneously to reposition both M1 edges so the enclosed via satisfied V0.M1.AUX.3 and V0.M1.EN.1 simultaneously.

Not every instance move requires an accompanying resize. Many accepted trials move instances with no polygon operation at all — trial:i01.ug.Block7_union_row11.01, trial:i01.ug.Block7_union_row18.08, trial:i02.ug.Block7_union_row18.03, trial:i02.ug.Block7_union_row21.05, trial:i03.ug.Block7_union_row23.04, trial:i03.ug.Block7_union_row24.05 — indicating that a resize is needed only when the moved via would otherwise fall outside the existing M1 polygon boundary.

## Enclosure rule V0.M1.EN.1: vertical (y-axis) repairs

When a via is displaced in y, the M1 polygon's y-extent must track the move. trial:i01.ug.Block7_union_row14.04 moved instances i0894 and i0920 by [0,64] and extended p3576 high-y by 64 dbu in the same operation. trial:i01.ug.Block7_union_row12.02 moved i1356 and i1358 by [0,8] and symmetrically adjusted p3694 at both y ends (high +8, low -8). trial:i04.ug.leaf_0007.05 translated polygon p3631 by [0,68], moved i0794 and i0810 by [0,68], and resized p2596 high-y by +68 in a single transaction. The y-resize magnitude matches the y-displacement of the associated instance in each of these trials.

Y-axis resize_end also appears without an accompanying y instance move. trial:i03.ug.Block7_union_row14.01 applied resize_end (axis=y, delta=8, end=high) on p3515 while instance moves in that trial were x-only ([8,0]). trial:i04.ug.leaf_0001.01 applied resize_end (axis=y, delta=-12, end=high) on p2719 while instance moves in that trial were x-only ([108,0] and [60,0]). Both were accepted with conn_preserved, establishing that small y-end trimming to satisfy enclosure margin on a stationary via is a valid standalone operation.

## Enclosure rule V1.M1.EN.1

V1.M1.EN.1 requires M1 to enclose V1 by at least 5 nm on one side and at least 2 nm on the opposite side. The same resize_end and instance-move patterns used for V0.M1.EN.1 apply here. trial:i01.ug.leaf_0024.25 adjusted p3538 (axis=x, delta=36, end=high and axis=y, delta=44, end=high) and p2333 (axis=y, delta=20, end=high) alongside instance move i0347 by [72,44] and resize_end (axis=x, delta=52, end=low) on p3706, touching layers M1, M2, M3, and V1.

## V0.M1.AUX.3 (via width matching)

V0.M1.AUX.3 flags V0 vias whose width in the direction perpendicular to the M1 length does not exactly match the M1 wire width in that direction. Repair requires that both non-coincident via edges align with M1 edges. trial:i04.ug.leaf_0001.01 corrected this by applying resize_end (axis=x, delta=-40, end=low) on p3297 and resize_end (axis=x, delta=108, end=high) on p3696, repositioning both lateral M1 edges to be flush with the via. trial:i01.ug.Block7_union_row9.21 applied resize_end (axis=x, delta=-36, end=low) on p3300 to contract one M1 edge to the via boundary, and a full translate (axis=x, delta=56) on p2720 to reposition that polygon's edges relative to its via.

## M1.W.1 minimum width

M1.W.1 requires a minimum M1 width of 18 nm. In trial:i01.ug.Block7_union_row9.21, p3300 was contracted at its low-x end by 36 dbu and the trial was accepted, confirming p3300 was wide enough beforehand that the contraction did not violate M1.W.1. Do not apply a resize_end that shrinks an M1 dimension if the resulting width would fall below 18 nm; verify remaining width before applying a contracting resize_end to any narrow polygon.

## M1.A.1 minimum area

M1.A.1 requires each M1 polygon to have area at least 504 nm² (0.000504 µm²). All resize_end operations that extend an M1 polygon end increase area. trial:i01.ug.leaf_0008.24 extended p3771 high-x by 164 dbu; trial:i01.ug.leaf_0002.23 extended p3695 high-x by 128 dbu; trial:i01.ug.Block7_union_row12.02 extended p3273 high-x by 56 dbu. These are all area-increasing operations. When a resize_end contracts an M1 edge, verify the reduced polygon area remains above 504 nm²; the contraction in trial:i01.ug.Block7_union_row9.21 (low-x, -36 dbu) on p3300 was accepted without an M1.A.1 marker, confirming that polygon was already well above the minimum before the shrink.

## M1.R.0 redundant island

M1.R.0 flags an M1 polygon that encloses exactly one small V0 and sits within 400 nm of a large empty M1 region (>=500 nm wide, area >2.5 µm²). No trial in this history produces an M1.R.0 violation. When moving an instance that carries a V0 to a new location, the destination M1 context must not be an isolated single-via island near a large open region. The rule is geometrically sensitive: a 400 nm expansion of any qualifying empty zone will capture nearby single-via islands.

## Non-orthogonal geometry

The NONORTHOGONAL rule flags any M1 edge not at 0° or 90°. All operations in this history apply integer dbu deltas exclusively on x or y axes, producing only rectilinear geometry. Apply all M1 polygon operations — resize_end, move, and the x/y components of instance moves — on pure x or y axes only. Never introduce a diagonal offset on any M1 polygon edge.

## Multi-iteration convergence

Several units required repair across more than one iteration with distinct operation sets each time, all accepted with conn_preserved.

Block7_union_row13: trial:i01.ug.Block7_union_row13.03 (iter 1, five ops including instance moves [40,0] and resize_end x+4) → trial:i02.ug.Block7_union_row13.00 (iter 2, three ops) → trial:i03.ug.Block7_union_row13.00 (iter 3, two ops including instance move [0,-88] and y-axis resize_end -44) → trial:i04.ug.Block7_union_row13.00 (iter 4, three ops with y-axis polygon move).

Block7_union_row14: trial:i01.ug.Block7_union_row14.04 (iter 1, eight ops) → trial:i02.ug.Block7_union_row14.01 (iter 2, five ops) → trial:i03.ug.Block7_union_row14.01 (iter 3, six ops including small +8 adjustments on three polygons).

leaf_0001: trial:i01.ug.leaf_0001.22 (iter 1, single instance move [4,0]) → trial:i02.ug.leaf_0001.09 (iter 2, single instance move [104,0]) → trial:i04.ug.leaf_0001.01 (iter 4, five ops including two resize_end x and one resize_end y).

The pattern shows that small moves in early iterations leave residual violations that require further correction. When the first move fully resolves the violation, the unit does not reappear in subsequent iterations: trial:i01.ug.Block7_union_row11.01 (two instances, [36,0]) and trial:i01.ug.Block7_union_row18.08 (four instances, [36,0]) both achieved zero new violations (n_new_in_crop=0) and did not recur.

## Connectivity preservation under mixed-delta operations

Every trial records conn_preserved=true. Trials that move some instances in one direction and others in the opposing direction — such as trial:i01.ug.Block7_union_row16.06 ([-36,0] for two instances, [40,0] for one) and trial:i01.ug.Block7_union_row8.20 ([-36,0] for one, [64,0] for two) — preserve connectivity because the opposing moves separate adjacent wires without severing any via-to-metal overlap. Trials with n_new_in_crop > 0 (e.g., trial:i01.ug.Block7_union_row13.03 with n_new_in_crop=1, trial:i01.ug.Block7_union_row19.09 with n_new_in_crop=1, trial:i02.ug.leaf_0041.19 with n_new_in_crop=5) are still accepted as long as conn_preserved=true, establishing that introducing a small number of new in-crop violations is tolerable provided connectivity is maintained.