## Observed Repair Patterns

All three recorded trials were accepted (`gated_in`, `conn_preserved=true`, `n_new_in_crop=0`, `n_new_out_of_crop=0`). V1 appears in the `touched_layers` list for every trial (trial:i02.ug.whole_design.00, trial:i03.ug.whole_design.00, trial:i04.ug.whole_design.00). No direct V1 polygon resize or move operations appear in any trial; V1 geometry is modified exclusively through instance placement moves that reposition entire via cells.

## Coordinated Instance Movement and M2 High-End Extension

The established repair pattern for V1 is simultaneous x-axis instance displacement combined with M2 polygon extension on the high-x end. This pattern was applied in all three trials and cleared DRC in each case (trial:i02.ug.whole_design.00, trial:i03.ug.whole_design.00, trial:i04.ug.whole_design.00).

V1.AUX.1 requires V1 to lie inside both M1 and M2. V1.M2.AUX.2 requires V1 to match M2's width in the direction perpendicular to M2's length. Moving a via instance in +x without extending the enclosing M2 polygon displaces V1 toward or beyond the M2 boundary, which violates V1.AUX.1. All accepted trials extended the M2 high-x end by at least as much as the corresponding instance displacement. In trial:i04, eleven via-cell instances were moved +72 dbu in x and the corresponding M2 polygons (p1065, p1045, p1026, p1052, p1053, p1040, p1063, p1034, p1057, p1059, p1060) were each extended +72 dbu on the high-x end, producing an exact-match co-movement (trial:i04.ug.whole_design.00). In trial:i03, instance i0063 was moved +36 dbu in x while polygon p1036 was extended +84 dbu on the high-x end, a surplus of 48 dbu, which also passed DRC (trial:i03.ug.whole_design.00).

Do not move a via instance in x without simultaneously extending its enclosing M2 polygon on the same end by at least the instance displacement magnitude. Equal-magnitude co-extension (trial:i04.ug.whole_design.00) and larger-magnitude M2 extension (trial:i03.ug.whole_design.00) both yielded accepted outcomes. No trial in this history tested an M2 extension smaller than the instance displacement.

## M2 Extension Amounts Across Trials

In trial:i02, instance i0086 was moved +72 dbu and polygon p1065 was extended +116 dbu on the high-x end; instance i0063 was moved +72 dbu and polygon p1036 was extended +80 dbu on the high-x end (trial:i02.ug.whole_design.00). In trial:i03, i0063 was moved an additional +36 dbu and p1036 was extended a further +84 dbu (trial:i03.ug.whole_design.00). In trial:i04, all eleven instance moves of +72 dbu were matched by exactly +72 dbu M2 extensions (trial:i04.ug.whole_design.00). The cumulative x-displacement of i0063 across these three trials is +72 + 36 = +108 dbu, and the cumulative M2 high-x extension of p1036 is +80 + 84 = +164 dbu. These multi-step adjustments to the same instance and polygon across sequential trials all remained DRC-clean at each step.

## Multi-Row Y-Displacement in a Single Trial

Trial:i02 applied distinct y-offsets to groups of via-containing instances within one accepted trial: instances i0080, i0073, i0068 moved +48 dbu in y; i0107, i0092, i0097 moved −48 dbu; i0088, i0095, i0099, i0059, i0070, i0061 moved +72 dbu; i0090, i0091, i0111, i0076, i0069, i0066 moved −72 dbu; i0079, i0072, i0064 moved −96 dbu; all also received a +32 dbu x-displacement (trial:i02.ug.whole_design.00). The simultaneous repositioning of via rows with differing y-offsets, spanning ±48, ±72, and −96 dbu, did not introduce V1.S.1 through V1.S.4 spacing violations in that trial (trial:i02.ug.whole_design.00). Additionally, two instances (i0086 and i0063) received +72 dbu x-displacements in the same trial (trial:i02.ug.whole_design.00), larger than the +32 dbu applied to the bulk of the via instances.

## Spacing Rules V1.S.1 Through V1.S.4

V1.S.1 requires minimum 17 nm projected spacing between V1 mask regions and 18 nm projected spacing between via active edges not coincident with M2 edges. V1.S.2 requires minimum 16.4 nm Euclidean corner-to-corner spacing between WEC (with-end-cap) via mask regions. V1.S.3 requires minimum 16.12 nm Euclidean corner-to-corner spacing between NEC (no-end-cap) via mask regions in the non-projection direction. V1.S.4 requires minimum 17.11 nm Euclidean separation between a WEC mask and a NEC mask in the non-projection direction. No spacing violations in these rules were introduced by any trial in this history. The mixed y-displacement pattern across multiple via rows in trial:i02.ug.whole_design.00 and the uniform +72 dbu x-only shifts in trial:i04.ug.whole_design.00 both left all spacing rules clean.

## M1 Enclosure (V1.M1.EN.1)

V1.M1.EN.1 requires M1 to enclose V1 on two opposite sides by at least 5 nm in projection on one axis and 2 nm on the other. M1 appears in `touched_layers` for all three trials (trial:i02.ug.whole_design.00, trial:i03.ug.whole_design.00, trial:i04.ug.whole_design.00). Because V1 is repositioned through instance moves and M1 context is co-located within the same instances, the M1 enclosure geometry moves with the via and V1.M1.EN.1 is maintained without separate M1 polygon adjustments. No M1 polygon resize operations appear in the history; M1 involvement in each trial is a consequence of instance-level co-movement.

## Width Rule V1.W.1

V1.W.1 requires a minimum via width of 18 nm along the M2 length direction. No V1 polygon resize operations appear in any trial. Instance moves reposition via cells without changing the cell's internal via dimensions. V1.W.1 was not perturbed by any recorded operation (trial:i02.ug.whole_design.00, trial:i03.ug.whole_design.00, trial:i04.ug.whole_design.00).

## Orthogonality (GEOMETRY.NONORTHOGONAL)

The NONORTHOGONAL rule fires on any edge whose angle deviates from 0° or 90°. All instance displacements and polygon extensions in the recorded history use integer-dbu axis-aligned deltas (x only or y only, never diagonal) with no fractional-dbu values. No NONORTHOGONAL violations were introduced in any trial (trial:i02.ug.whole_design.00, trial:i03.ug.whole_design.00, trial:i04.ug.whole_design.00). Apply only axis-aligned moves and extensions to V1 instances and their enclosing M2 polygons.