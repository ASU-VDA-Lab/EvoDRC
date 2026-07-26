## Horizontal Width (M5.W.1, M5.W.2, M5.W.3, M5.W.4)

M5 horizontal width must be at least 24 nm (M5.W.1) and at most 480 nm (M5.W.2). Widths that are exact even-integer multiples of 24 nm — specifically 48, 96, 144, 192, 240, 288, 336, 384, 432, and 480 nm — are forbidden by M5.W.3. Widths of 72, 168, 264, 360, and 456 nm are additionally forbidden by M5.W.4 because they span an even number of minimum-width routing tracks horizontally.

In trial:i05.ug.leaf_0001.00, polygon p879 received a low-end x-axis extension of 352 dbu and a high-end x-axis extension of 32 dbu. The trial was gated in with n_new_in_crop: 0 and n_new_out_of_crop: 0, confirming the post-resize horizontal width avoided all M5.W.1, M5.W.2, M5.W.3, and M5.W.4 forbidden values.

## Vertical Width (M5.W.5)

Minimum vertical width is 44 nm (M5.W.5). The resize operations in trial:i05.ug.leaf_0001.00 operated exclusively on the x-axis and did not alter the vertical extent of p879; no M5.W.5 violation was introduced.

## Horizontal Spacing (M5.S.1, M5.S.3, M5.S.4, M5.S.5)

Minimum horizontal spacing between M5 polygon edges is 24 nm (M5.S.1). Tip-to-tip spacing on adjacent tracks is 40 nm regardless of whether the polygons share a parallel run length (M5.S.3, M5.S.4). Minimum parallel run length between M5 polygons on adjacent tracks is 44 nm (M5.S.5).

The low-end extension of 352 dbu and high-end extension of 32 dbu on p879 in trial:i05.ug.leaf_0001.00 produced zero new violations, confirming all horizontal spacing constraints were satisfied after the resize.

## Vertical Spacing (M5.S.2)

Minimum vertical spacing between M5 polygon edges is 40 nm (M5.S.2). No operation in either recorded trial moved M5 geometry along the y-axis, and no M5.S.2 violation was introduced.

## Routing Track Alignment (M5.AUX.1, M5.AUX.2)

M5 vertical edges must land on a 24 nm x-grid (M5.AUX.1). Minimum-width M5 tracks must be centered on vertical routing tracks at a pitch of 192 dbu with a 48 dbu offset from the origin (M5.AUX.2).

The x-axis edge moves applied to p879 in trial:i05.ug.leaf_0001.00 introduced no M5.AUX.1 or M5.AUX.2 violations (n_new_in_crop: 0), confirming that the resulting edge positions landed on legal grid locations.

## No-Bend Rule (M5.AUX.3)

M5 polygons may not bend; all geometry must be purely rectilinear (M5.AUX.3). The two resize_end operations on p879 in trial:i05.ug.leaf_0001.00 extended horizontal ends along the x-axis only, introducing no corners and no M5.AUX.3 violations.

## Wide Metal Restriction (M5.AUX.4)

Outside edges of wide M5 polygons may not touch a routing track edge (M5.AUX.4). No op in the measured history targeted a wide M5 polygon directly.

## Via Enclosure (V4.M5.EN.2, V4.M5.AUX.2, V5.M5.EN.1)

V4 must be enclosed by M5 by at least 11 nm on two opposite sides (V4.M5.EN.2), and V4 must exactly match the M5 width along the direction perpendicular to the M5 run direction (V4.M5.AUX.2). V5 carries the same 11 nm two-side enclosure requirement against M5 (V5.M5.EN.1).

In trial:i01.cu.def:VIA_VIA34_1_2_58_52.00, M5 appears in touched_layers alongside V4. All direct ops in that trial applied y-axis resize_via_shape changes to M3, M4, V3, and V4; no op targeted M5 geometry directly. The trial was accepted (decision: "applied") and reduced the total violation count by 13. The inclusion of M5 in touched_layers alongside V4 in trial:i01.cu.def:VIA_VIA34_1_2_58_52.00 establishes that resizing V4 triggers re-evaluation of M5 enclosure rules; enclosure compliance on M5 must therefore be verified whenever V4 dimensions change.