## Successful Repair Patterns

**Horizontal end-extension of M4 runlength.**
In trial:i01.ug.Block1_union_row12.02, extending the high-x ends of two M4 polygons (p1211: +456 dbu, p1216: +240 dbu) was gated in with zero new violations in the crop window and full connectivity preserved. Apply x-axis end-resizes on M4 when increasing tip separation or parallel run length is needed; the measured result in trial:i01.ug.Block1_union_row12.02 confirms this class of operation carries no observable violation cost when executed in isolation on M4.

**Y-axis reduction of V4 via shapes to satisfy M4 enclosure.**
In trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, shrinking the y-extent of via cell VIA_VIA45_1_2_58_58 by 88 dbu eliminated 52 total violations (−26 in leaf_0034, −26 in leaf_0035) without breaking connectivity. The touched layers were M4, M5, and V4. Use y-axis via shrinks to address over-extended via shapes that violate V4.M4.EN.1 (minimum 11 nm enclosure of V4 by M4 on two opposite sides), as this approach is confirmed effective in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01.

## Failed Pattern

**Mixed multi-layer combinatorial operations that include M4 edge trims.**
Trial:i01.ug.leaf_0034.12 bundled 10 simultaneous operations across M1, M2, M3, M4, V1, and V2 — including a −4 dbu right-edge trim of M4 polygon p1214 and a +192 dbu right-edge extension of p1178, combined with five instance moves and an M3 via reshape. The result was 89 new violations in the crop window and broken connectivity; the trial was gated out. Do not bundle M4 edge trims with large-displacement multi-layer perturbations in the same operation set; trial:i01.ug.Block1_union_row12.02 demonstrates that M4-only resizes applied in isolation succeed without side effects, while the mixed 10-op set in trial:i01.ug.leaf_0034.12 failed.

## Width Rule Constraints

Vertical (y-axis) width must be ≥ 24 nm (M4.W.1) and ≤ 480 nm (M4.W.2). Within that range, widths that are even integer multiples of 24 nm — specifically 48, 96, 144, 192, 240, 288, 336, 384, 432, and 480 nm — are forbidden by M4.W.3. Widths of 72, 168, 264, 360, and 456 nm are additionally forbidden by M4.W.4 because they span an even number of minimum-width routing tracks. Minimum horizontal (x-axis) width is 44 nm (M4.W.5).

When resizing M4 polygon endpoints on the x-axis, avoid producing a vertical height that lands on any of the M4.W.3 or M4.W.4 forbidden values; trial:i01.ug.Block1_union_row12.02 confirms that x-axis resizes (+456 dbu and +240 dbu) can be applied cleanly when they do not alter the y-dimension.

## Grid and Topology Constraints

Minimum-width (24 nm) M4 segments must be centered on horizontal routing tracks at y-positions satisfying (centerline − 48 dbu) mod 192 dbu = 0, with the polygon base on a 96 dbu grid (M4.AUX.2). All M4 horizontal edges must lie on a 24 nm vertical grid (M4.AUX.1). M4 polygons must be fully orthogonal (GEOMETRY.NONORTHOGONAL) and must not contain right-angle bends within a single polygon (M4.AUX.3). The outer horizontal edges of wide M4 polygons may not coincide with routing track edges (M4.AUX.4). None of the trials in the current history record a violation of these geometric constraints, but resize operations must keep adjusted edges on the 24 nm grid to avoid introducing M4.AUX.1 errors.

## Spacing Constraints

Minimum vertical spacing between M4 polygon edges is 24 nm (M4.S.1). Minimum horizontal spacing between vertical M4 edges is 40 nm (M4.S.2). Tip-to-tip spacing on adjacent tracks for polygons that do not share a parallel run length is ≥ 40 nm (M4.S.3); for polygons that do share a parallel run length the same 40 nm tip-to-tip floor applies (M4.S.4). When two M4 polygons on adjacent tracks share a parallel run length, that run length must be ≥ 44 nm (M4.S.5). X-axis end-resizes that increase tip separation or runlength address M4.S.3, M4.S.4, and M4.S.5 without introducing new violations, as measured in trial:i01.ug.Block1_union_row12.02.

## Via Enclosure

V3 must be enclosed by M4 by ≥ 11 nm on at least two opposite sides (V3.M4.EN.2). The width of V3 must exactly match the width of M4 in the direction perpendicular to the M4 run direction — no overhang or underhang is permitted (V3.M4.AUX.2). V4 must be enclosed by M4 by ≥ 11 nm on at least two opposite sides (V4.M4.EN.1). Shrink via y-extent to resolve V4.M4.EN.1 violations caused by over-extended via shapes; trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 confirms this reduces violations at scale (−52 net) with no connectivity loss. Avoid resizing M4 itself to fix enclosure unless the via shape cannot be reduced, because M4 polygon mutations in multi-layer contexts have broken connectivity (trial:i01.ug.leaf_0034.12).