## V2.M3.AUX.2 — Width-match between V2 and M3 perpendicular to M3 length

V2.M3.AUX.2 requires that V2 exactly matches the M3 width along the direction perpendicular to M3 length. Oversized M3 in that perpendicular axis causes violations. The successful repair in trial:i04.cu.def:VIA_VIA23_1_3_36_36.00 applied the fix group `v2m3aux2_fix`, which simultaneously shrunk the M3 shape inside the via cell `VIA_VIA23_1_3_36_36` by -40 dbu along the y-axis and shrunk seven surrounding M3 polygons (p891–p897) by -64 dbu each along the y-axis. This coordinated resize reduced the total violation count from 30 to 22 (delta -8), and the trial was accepted (decision: applied).

When the via cell itself contains an M3 shape that participates in V2.M3.AUX.2, resize both the via-cell M3 shape and all interacting M3 polygons together along the same axis. Applying the via-cell resize alone or the polygon resize alone leaves the constraint unsatisfied, as the fix group in trial:i04.cu.def:VIA_VIA23_1_3_36_36.00 bundled all eight operations into a single atomic apply.

The -40 dbu correction on the via-cell M3 shape and -64 dbu correction on the surrounding polygons were not equal, indicating the via cell and the freeform M3 polygons started at different offsets from the V2 boundary. Do not assume a uniform delta across the two shape classes; derive each correction from the actual enclosure violation measured.

## V3.M3.EN.1 — Enclosure of V3 by M3

No V3.M3.EN.1 violations were repaired in the recorded history. The rule requires M3 to enclose V3 by at least 5 nm on at least one pair of opposite sides (either left+right via `m3.sized(-5,0)` or top+bottom via `m3.sized(0,-5)`). In trial:i05.ug.whole_design.00 (decision: gated_in, conn_preserved), seven `VIA_VIA34` instances were added at specific locations ([2200,2160], [2200,4272], [2200,6576], [2200,8688], [2968,3312], [2968,5424], [2968,7536]), and the touched layers include M3 and V3. The trial was accepted with zero new violations in or out of crop, establishing that those via placements satisfied V3.M3.EN.1 without additional M3 edits. When placing VIA_VIA34, the existing M3 geometry at those coordinates was sufficient to provide the required 5 nm bilateral enclosure.

## V2.M3.EN.2 — Enclosure of V2 by M3

V2.M3.EN.2 requires M3 to enclose V2 by at least 5 nm on two opposite sides (5 & 5 nm, or 5 & 0 nm with exact flush on the opposite side). The repair in trial:i04.cu.def:VIA_VIA23_1_3_36_36.00 targeted the `v2m3aux2_fix` group, not V2.M3.EN.2 explicitly, but the y-axis shrink of M3 shapes (both via-cell and freeform) in a V2-containing region affects EN.2 enclosure margins simultaneously. The net violation count fell by 8 after the fix, consistent with both AUX.2 and EN.2 violations being resolved together by the same resize operation.

## M3 polygon resizes and axis discipline

All M3 resizes recorded in the repair history operate along a single axis per operation. In trial:i04.cu.def:VIA_VIA23_1_3_36_36.00, every resize in the `v2m3aux2_fix` group used `axis: y`. In trial:i01.ug.whole_design.00, polygon p879 received a y-axis `resize_end` (+48 dbu, end: high) and polygon p910 received an x-axis `move` (+8 dbu) followed by a y-axis `resize_end` (+20 dbu, end: high). In trial:i05.ug.whole_design.00, polygons p951 and p955 each received an x-axis `resize_end` (+128 dbu, end: high). No diagonal or simultaneous two-axis resize operations appear in any accepted trial. Apply single-axis corrections and verify both spacing and width rules after each axis independently.

## Instance moves and M3 connectivity preservation

Trials accepted via the `unit_gate` channel (trial:i01.ug.whole_design.00, trial:i05.ug.whole_design.00) both recorded `conn_preserved: true` and zero new violations entering or leaving the crop window. The instance moves in those trials ranged from -36 dbu to +136 dbu in x and -48 dbu to +96 dbu in y, and none triggered M3.W.1, M3.S.1, M3.S.2, M3.S.3, M3.S.4, M3.S.5, M3.S.6, or M3.A.1 violations. Moving instances within those magnitude bounds, while preserving connectivity, does not itself create new M3 DRC violations in this design.

Deleting instances does not automatically clear associated M3 violations. In trial:i05.ug.whole_design.00, seven instances (i0098, i0105, i0075, i0076, i0099, i0002, i0070) were deleted alongside polygon resizes and via additions; the trial was accepted, but the deletion and the geometric changes were bundled. Do not assume instance deletion alone resolves an M3 spacing or width error without accompanying M3 geometry correction.

## M3.W.1 — Minimum width 18 nm

No M3.W.1 violations appear as explicit repair targets in any recorded trial. All accepted polygon resize operations shrank or expanded M3 shapes without triggering a minimum-width failure, establishing that the polygons involved remained at or above 18 nm width after the applied deltas (trial:i04.cu.def:VIA_VIA23_1_3_36_36.00, trial:i01.ug.whole_design.00, trial:i05.ug.whole_design.00).

## M3.A.1 — Minimum area 504 nm²

No M3.A.1 violations appear as repair targets in the recorded history. The shrinks applied in trial:i04.cu.def:VIA_VIA23_1_3_36_36.00 (-64 dbu per polygon across seven shapes) were accepted without triggering area violations, indicating those shapes retained area above 504 nm² after the correction. When applying large y-axis shrinks to M3 polygons, confirm residual area remains above 504 nm² — the accepted shrink magnitude in trial:i04.cu.def:VIA_VIA23_1_3_36_36.00 provides a reference upper bound on safe delta for similarly sized polygons in this block.

## GEOMETRY.NONORTHOGONAL

All accepted M3 operations in the recorded history (trial:i01.ug.whole_design.00, trial:i04.cu.def:VIA_VIA23_1_3_36_36.00, trial:i05.ug.whole_design.00) use orthogonal axis moves and resize_end operations. No non-orthogonal edges were introduced. Restrict all M3 edits to horizontal and vertical operations to avoid triggering the GEOMETRY.NONORTHOGONAL rule, which fires on any M3 edge with angle outside {0°, 90°, 180°, 270°}.