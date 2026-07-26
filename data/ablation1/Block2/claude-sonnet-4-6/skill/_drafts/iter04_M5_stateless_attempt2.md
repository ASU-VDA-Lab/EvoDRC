## Horizontal Width Constraints (M5.W.1 – M5.W.4, M5.AUX.1, M5.AUX.2)

M5 horizontal width must be at least 24 nm (M5.W.1) and no more than 480 nm (M5.W.2). The forbidden widths are precisely those that are exact even-integer multiples of 24 nm (M5.W.3) or that cause a polygon to span an even number of minimum-width routing tracks horizontally—specifically widths whose projection gap equals 72, 168, 264, 360, or 456 nm (M5.W.4). Vertical edges must land on a 24 nm grid (M5.AUX.1), and minimum-width M5 tracks must be centered on vertical routing tracks with pitch 192 dbu and offset 48 dbu from the base-96-dbu grid (M5.AUX.2).

When resizing an M5 polygon end in x, the resulting width must avoid the M5.W.3 and M5.W.4 forbidden values in addition to satisfying M5.W.1 and M5.W.2. Resize operations on p938 (trial:i01.ug.leaf_0012.07, trial:i02.ug.leaf_0003.02) and p937 (trial:i03.ug.leaf_0002.01) each introduced new in-crop violations despite preserving connectivity, confirming that naive resize deltas in x routinely violate M5.W.3, M5.W.4, or M5.AUX.1 even when the target end displacement appears modest. Do not apply x-axis resize deltas without verifying that the resulting edge position is 24 nm grid-aligned and that the resulting width is not 48, 96, 144, 192, 240, 288, 336, 384, or 432 nm (trial:i01.ug.leaf_0012.07, trial:i02.ug.leaf_0003.02).

For minimum-width M5 polygons (width ≤ 24 nm + 2×13 nm = 50 nm effective limit before the sized erosion used in AUX.2 removes them), the polygon centerline in x must satisfy `(cl - 48) % 192 == 0` relative to the base-96-dbu grid. Resize operations that shift one end without recentering will displace the centerline and can violate M5.AUX.2 (trial:i01.ug.leaf_0012.07, trial:i02.ug.leaf_0003.02).

## Vertical Width and Spacing Constraints (M5.W.5, M5.S.2 – M5.S.5)

M5 minimum vertical width is 44 nm (M5.W.5). Minimum vertical spacing between M5 edges is 40 nm (M5.S.2). Tip-to-tip spacing between M5 polygons on adjacent tracks is 40 nm whether or not they share a parallel run length (M5.S.3, M5.S.4). Where two M5 polygons do run in parallel on adjacent tracks, the minimum parallel run length is 44 nm (M5.S.5).

Instance moves in y propagate M5 edge positions across multiple layers simultaneously. Moves of 24 dbu and 72 dbu on instances i0090, i0110, i0061, i0066, i0069, i0098, i0094, i0070 (trial:i03.ug.leaf_0002.01) and moves of 24 dbu on i0090, i0110, i0089 (trial:i04.ug.leaf_0003.02) each introduced two new in-crop violations on M5. Do not treat instance move deltas as safe with respect to M5.S.2 or M5.W.5 without post-move DRC verification, even when connectivity is preserved (trial:i03.ug.leaf_0002.01, trial:i04.ug.leaf_0003.02).

## No-Bend and No-Offtrack-Wide-Edge Constraints (M5.AUX.3, M5.AUX.4)

M5 may not bend: any corner between 0° and 90° is a violation of M5.AUX.3. Resize operations that shift only one end in x (trial:i01.ug.leaf_0012.07 low-end −64 dbu, trial:i02.ug.leaf_0003.02 low-end −192 dbu, trial:i03.ug.leaf_0002.01 low-end −64 dbu) preserve the rectangular shape of the polygon as long as the polygon itself is already rectangular, which is the only form compatible with M5.AUX.3. Never apply a partial-edge resize that would produce a non-rectangular M5 shape.

For wide M5 polygons (those that survive the `sized(-13 nm, 0).sized(13 nm, 0)` erosion-regrow in AUX.4), the vertical edges of the polygon must not coincide with any vertical routing track edge occupied by a minimum-width M5 polygon on an adjacent track. Instance moves that shift wide M5 features in y do not themselves displace x-position of wide-polygon vertical edges, but must still be verified for M5.AUX.4 because adjacent minimum-width tracks may shift relative to the wide polygon (trial:i03.ug.leaf_0002.01, trial:i04.ug.leaf_0003.02).

## Via Enclosure Rules (V4.M5.EN.2, V4.M5.AUX.2, V5.M5.EN.1)

V4 must be enclosed by M5 by at least 11 nm on two opposite sides (V4.M5.EN.2). V4 must also exactly match the M5 width in the direction perpendicular to M5's length (V4.M5.AUX.2): V4 vertical edges must be coincident with M5 vertical edges, with no overhanging or recessed M5 margin in that direction.

Via shape resizes that adjust the M5 extent in y directly affect V4 enclosure compliance. Reducing the M5 via-cell shape in y by 88 dbu (trial:i04.cu.def:VIA_VIA45_1_2_58_58.00) reduced total in-crop M5 violations from 23 to 15 on leaf_0002 and from 14 to 6 on leaf_0003, for a combined delta of −16, and was applied via the cu_pool channel against via cell `VIA_VIA45_1_2_58_58`. This confirms that M5 extents defined inside via cells are a significant source of M5 DRC violations and that resizing the M5 shape within the via cell in y is an effective repair avenue (trial:i04.cu.def:VIA_VIA45_1_2_58_58.00).

When resizing an M5 via-shape in y, the touched layers include M4 and V4 (trial:i04.cu.def:VIA_VIA45_1_2_58_58.00). Verify V4.M5.EN.2 and V4.M5.AUX.2 after every such resize to confirm that V4 enclosure by M5 in y remains ≥ 11 nm on both sides and that V4 width perpendicular to M5 length still exactly matches M5 (trial:i04.cu.def:VIA_VIA45_1_2_58_58.00).

V5.M5.EN.1 requires V5 to be enclosed by M5 by at least 11 nm on two opposite sides. No trial in the measured history records a V5 interaction on M5, so no repair-specific guidance for V5 can be grounded from the available records.

## Decision Gating Behavior

All four unit-gate channel trials (trial:i01.ug.leaf_0012.07, trial:i02.ug.leaf_0003.02, trial:i03.ug.leaf_0002.01, trial:i04.ug.leaf_0003.02) were accepted with `decision: gated_in` despite introducing new in-crop violations (2, 4, 2, and 2 respectively), because `conn_preserved` was true and `n_new_out_of_crop` was 0 in each case. The cu_pool trial (trial:i04.cu.def:VIA_VIA45_1_2_58_58.00) was accepted with `decision: applied` because it produced a net reduction of 16 violations. Operations that create out-of-crop violations will not satisfy the gated_in acceptance condition and must be avoided; operations bounded to in-crop effects with preserved connectivity are accepted even when they introduce new in-crop violations (trial:i01.ug.leaf_0012.07, trial:i02.ug.leaf_0003.02, trial:i03.ug.leaf_0002.01, trial:i04.ug.leaf_0003.02).