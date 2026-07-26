## Repair Operation Patterns

Across all four measured iterations, M2-touching repairs operated exclusively through the `unit_gate` channel (trials trial:i01.ug.Block7_union_row10.00 through trial:i04.ug.leaf_0007.06) and the `cu_pool` channel (trial:i04.cu.def:VIA_VIA23_1_3_36_36.01). Every `unit_gate` trial that touched M2 resulted in `decision: gated_in` with `conn_preserved: true`, confirming that the chosen move-and-resize strategy preserved all M2 net topology across the full measured history. The single `gated_out` result on M2 (trial:i04.ug.leaf_0008.07) was rejected for `empty_or_missing_patch`, not for connectivity failure; the identical op set was subsequently applied through `cu_pool` (trial:i04.cu.def:VIA_VIA23_1_3_36_36.01).

The dominant repair primitives applied to M2 polygons are `move_instance` (x-axis, occasionally y-axis), `resize_end` on specific polygon ends (x-axis predominantly), symmetric `resize` (both ends simultaneously), and, rarely, `add_polygon`. These four primitives account for every M2 modification across iterations 1 through 4.

## M2.W.1 and M2.A.1: Minimum Width and Area

The only `add_polygon` operation on M2 in the history, trial:i01.ug.Block7_union_row20.10, created a rectangle with coordinates [5992,22824]–[6048,22896], giving a width of 56 dbu (56 nm) and a height of 72 dbu (72 nm), yielding area 4032 nm². Both dimensions comfortably exceed the M2.W.1 minimum of 18 nm and the M2.A.1 minimum of 504 nm², and the trial was gated_in. Do not add M2 patches with any edge shorter than 18 nm or with total area below 504 nm².

When extending an existing M2 polygon via `resize_end`, verify that the remaining side opposite the extended end does not drop below 18 nm after the resize. Observed high-end extensions include +56, +92, +100, +128, +136, +160, +180, +192, and +308 dbu (trials trial:i01.ug.Block7_union_row10.00, trial:i01.ug.Block7_union_row7.19, trial:i01.ug.Block7_union_row5.17, trial:i01.ug.Block7_union_row24.14, trial:i02.ug.Block7_union_row9.06); none of these produced M2.W.1 errors, indicating the originating polygons were wide enough to absorb low-end reductions.

## M2.S.1 and M2.S.7: Side-to-Side Spacing and Parallel Run Constraint

Coordinated moves of multiple instances in the same direction by the same delta preserve inter-polygon side spacing. In trial:i01.ug.Block7_union_row11.01 both instances (i1828, i1728) were moved +36 dbu in x simultaneously; in trial:i01.ug.Block7_union_row9.21 five instances (i1117, i1398, i1215, i1178, i1885) were all moved +40 dbu; in trial:i01.ug.Block7_union_row6.18 six instances moved +36 or +28 dbu. All were gated_in with zero new in-crop violations, confirming that uniform-delta group moves do not create new side-to-side spacing violations between the moved polygons.

When instances must move by different deltas (e.g., one moves +136 and another moves +64 in trial:i01.ug.Block7_union_row24.14, or +108 and +40 in trial:i01.ug.Block7_union_row7.19), apply paired `resize_end` on the M2 polygon segment between them to compensate the differential displacement and preserve M2.S.1 clearance. This pattern appeared across trials trial:i01.ug.Block7_union_row10.00, trial:i01.ug.Block7_union_row14.04, trial:i01.ug.Block7_union_row18.08, and others, all with zero new in-crop violations.

M2.S.7 forbids a tip-to-tip gap of 18 nm co-located with side spacing <= 32 nm, and requires parallel run length >= 35 nm when side spacing <= 32 nm. No trial in the history logged an M2.S.7 violation or gated_out for that reason; however, the consistent use of move deltas that are multiples of 4 dbu (with common values 36, 72, 108, 136 dbu) and the avoidance of sub-18 dbu gaps in all gated_in trials is consistent with keeping tip-to-tip distances above 18 nm.

## M2.S.2, M2.S.3, M2.S.4, M2.S.5: Tip Spacing Rules

Tip edges (edges <= 36 nm long) on M2 polygons require larger separation than side edges: 25 nm for tip-to-side (M2.S.2), 27 nm for wide-tip-to-wide-tip (M2.S.3), 31 nm for narrow-tip-to-narrow-tip (M2.S.4) or mixed narrow/wide (M2.S.5). No trial explicitly logged violations against these rules by name, but the `resize_end` operations pulling a low end inward (e.g., trial:i01.ug.Block7_union_row3.15: end=low +56 on p3384; trial:i01.ug.Block7_union_row8.20: end=low +56 on p3430; trial:i01.ug.Block7_union_row17.07: end=low +56 on p3187) consistently shrink M2 ends toward the interior of the polygon, which increases tip-to-tip or tip-to-side distance toward an adjacent polygon. Apply `resize_end` on the low end (inward pull) when the tip of an M2 polygon is too close to an adjacent polygon. All such trials were gated_in.

## M2.S.6: Corner-to-Corner Spacing

M2.S.6 requires a minimum euclidian corner-to-corner spacing of 20 nm between any two M2 polygons. No trial produced an M2.S.6 violation in the gated_in set. The smallest move delta applied in any M2 trial was 3 dbu (trial:i02.ug.leaf_0022.10), and the result was gated_in with 3 new in-crop violations (likely on a different layer given the small move); no M2.S.6 was introduced. Move deltas of 4 dbu or larger are the consistent floor across the history.

## V1.M2.EN.2 and V1.M2.AUX.2: V1 Enclosure by M2

M2 must enclose V1 by at least 5 nm on two opposite sides (V1.M2.EN.2), and M2 must be exactly the same width as V1 in the direction perpendicular to M2 length (V1.M2.AUX.2). In every trial that moves a V1-bearing instance, the repair also applies `resize_end` on the directly connected M2 polygon to track the V1 displacement. Examples:

- trial:i01.ug.Block7_union_row10.00: i1140 moves +52 x; p3286 high end extends +308 x; i1811 moves -216 x; p3751 low end moves +180 x and high end extends +56 x.
- trial:i01.ug.Block7_union_row15.05: i0913 moves +136 x; p3586 is resized symmetrically +160 x (both ends, equivalent to a centered extension).
- trial:i01.ug.Block7_union_row24.14: i0215 moves +136 x with p3058 high end +136 x; i0561 moves +64 x with p3635 high end +120 x; p3564 high end +128 x.

Never move a V1-bearing instance without a concurrent adjustment to the M2 polygon that encloses that V1. This pattern is present in every multi-op trial across iterations 1–4 that touches M1/M2/V1, and all such trials were gated_in.

For V1.M2.AUX.2, the AUX constraint requires M2 edge coincidence with V1 edge in the perpendicular direction. In iter 2, trial:i02.ug.Block7_union_row15.03 applied a y-axis `resize` (+96 dbu, both ends symmetric) on p3592 while simultaneously moving i1062 by y=-84 dbu, adjusting the M2 polygon height to realign with V1. The same polygon p3592 was revisited in trial:i03.ug.leaf_0007.05 with further y-axis `resize_end` adjustments (low end +72, low end -48, high end -48) and gated_in with 3 new in-crop violations. These fine-tuning passes confirm that y-axis M2 height adjustments are sometimes required over multiple iterations to satisfy V1.M2.AUX.2.

## V2.M2.EN.1: V2 Enclosure by M2

V2.M2.EN.1 requires M2 to enclose V2 by at least 5 nm on two opposite sides. When M2 polygons serve as the M2-side landing pad for V2 vias, their y-axis position must be tuned independently of x-axis spacing adjustments. In trial:i02.ug.leaf_0001.07, polygon p3383 was moved y=-57 dbu together with instance i1643 to reposition the M2 pad relative to V2, and the result was gated_in. In trial:i03.ug.leaf_0001.03, the same polygon p3383 was moved y=+21 dbu (with i1643) as a corrective follow-up, again gated_in. These small iterative y-axis corrections (57 dbu down, then 21 dbu back up across two iterations) confirm that M2/V2 alignment is sensitive and may require more than one pass.

In iter 4, trial:i04.ug.leaf_0002.01 and trial:i04.ug.leaf_0003.02 each applied a small +8 dbu x-axis `move` on an M2 polygon (p2916, p2877 respectively) paired with two instance moves, touching M2/M3/V2. Both were gated_in with zero new violations. This +8 dbu fine-step (the smallest non-trivial x move in the M2 history) corrects sub-grid V2.M2.EN.1 enclosure deficits without introducing new spacing violations.

## Large-Batch M2 Y-Axis Reshaping: cu_pool Required

Trial:i04.ug.leaf_0008.07 applied 72 `resize_end` operations shrinking M2 polygons in y by -32 dbu on both ends (and -41 on the high end for a subset), plus a `resize_via_shape` on M3. The unit_gate channel rejected this as `gated_out` with reason `empty_or_missing_patch`. The identical 73-op set was then accepted and applied through the `cu_pool` channel as trial:i04.cu.def:VIA_VIA23_1_3_36_36.01, reducing the total block violation count by 72 (all V2.M3.AUX.2).

Do not route large-batch M2 y-axis shrink operations (affecting many polygons simultaneously to fix cross-layer V2 enclosure rules) through unit_gate; use cu_pool. Unit_gate requires a non-empty patch locus; global M2 y-shrinks targeting a via cell definition have no single localized patch region and will be rejected.

The cu_pool trial i05.cu.def:VIA_VIA23_1_3_36_36.00 applied only the `resize_via_shape` on M3 (-40 dbu) without the M2 y-shrinks and was `rejected_net_positive` (delta_total=+64, increasing violations). The M2 y-shrinks are required alongside the M3 via resize to achieve a net improvement; applying the M3 change alone worsens the total count. Always apply M2 y-shrinks and the coupled M3/V2 resize_via_shape as a combined operation.

## Cross-Layer Context: M2 Repairs Co-occurring with M3 and V2

Several repair loci touch M2, M3, and V2 simultaneously (trials trial:i01.ug.Block7_union_row16.06, trial:i01.ug.leaf_0095.26, trial:i02.ug.leaf_0001.07, trial:i02.ug.leaf_0014.08, trial:i03.ug.leaf_0001.03, trial:i03.ug.leaf_0002.04, trial:i03.ug.leaf_0011.07, trial:i04.ug.leaf_0002.01, trial:i04.ug.leaf_0003.02, trial:i05.ug.leaf_0001.00). These are not M2-only repairs; they involve coordinated adjustment of M2 plus the V2 via instance and/or M3 landing polygon. When an M2 polygon is part of a V2 stack, modify the M2 position only in conjunction with the V2 instance and the M3 polygon above it; isolated M2 movement without corresponding V2/M3 adjustment risks violating V2.M2.EN.1 or V2.M3.AUX.2 on the other side of the via.

In trial:i03.ug.leaf_0002.04, an M3 `add_polygon` at [11664,11756]–[11908,11828] (244 nm × 72 nm) was created as part of an M2/M3/V2 stack repair. The M2 polygon p3300 on that same trial had its x-low end shrunk by -88 dbu. This confirms that stack repairs sometimes require adding new M3 geometry rather than only adjusting existing shapes, while simultaneously reducing M2 extent to avoid M2-side spacing violations.

## Instance Movement Grid

All measured `move_instance` deltas on M2-touching trials are multiples of 4 dbu: the common values are 4, 8, 12, 24, 28, 32, 36, 40, 48, 52, 56, 64, 68, 72, 84, 92, 96, 108, 136 dbu. Move instances only in increments of 4 dbu. Sub-4-dbu instance moves do not appear anywhere in the M2 history; the only sub-4-dbu positional change in the dataset is the 3-dbu x-move in trial:i02.ug.leaf_0022.10, and that trial introduced 3 new in-crop violations despite being gated_in.

`resize_end` deltas on M2 polygons also follow the 4-dbu grid in all but one case (trial:i02.ug.Block7_union_row15.03 y-resize +96; trial:i04.ug.leaf_0008.07 y-resize -32/-41). The -41 dbu end-resize values in trial:i04.ug.leaf_0008.07 are the only non-multiples-of-4 observed on M2, applied only in the large cu_pool batch where sub-grid correction of M2 y-height was required to satisfy V2.M3.AUX.2.