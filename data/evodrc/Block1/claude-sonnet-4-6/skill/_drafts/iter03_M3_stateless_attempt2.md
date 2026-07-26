## M3.S.2 — Tip-to-Side Spacing (25 nm minimum)

M3.S.2 requires a minimum 25 nm projection separation between a tip edge (length ≤ 36 nm) and a side edge (length > 36 nm) on distinct M3 polygons.

Uniform y-axis shrinks of 64 dbu (16 nm) applied to 12 M3 polygons introduced 2 new M3.S.2 violations (trial:i01.ug.leaf_0035.13). Lateral x-axis moves of M3 polygons combined with multi-layer instance translations also introduced 2 new M3.S.2 violations (trial:i02.ug.leaf_0004.03). Both outcomes confirm that operations reducing the projection gap between an M3 tip edge and a neighboring M3 side edge produce M3.S.2 errors.

To clear M3.S.2, shrink the violating polygon's offending end edge using resize_end by the amount needed to restore the 100 dbu (25 nm) projection gap. When the resized polygon shares a VIA23 M3 land, move the VIA23 instance by the same displacement to maintain land alignment. This two-part approach cleared both M3.S.2 v0014 (p1543, resize_end −8 dbu on high-x edge) and M3.S.2 v0015 (p1458 resize_end −8 dbu + instance i0180 moved −40 dbu in x) in a single gated_in trial (trial:i03.ug.leaf_0003.02).

When applying resize_end to clear M3.S.2, verify that V2 cut edges inside the resized polygon remain within the new M3 boundary to preserve V2.M3.AUX.2. In trial:i03.ug.leaf_0003.02, shrinking p1543's right edge from 13876 to 13868 dbu left V2 cut rightmost edges at 13860 dbu inside the new extent; V2.M3.AUX.2 was preserved. A resize_end that would move an M3 boundary edge past an embedded V2 cut edge requires corrective action beyond the resize alone (trial:i03.ug.leaf_0003.02).

## V2.M3.EN.2 — Enclosure of V2 by M3 on Two Opposite Sides (5 nm)

V2.M3.EN.2 requires M3 to enclose V2 by at least 5 nm on two opposite sides (either 5 & 5 nm or 5 & 0 nm).

Moving M3 polygons in x and y as part of multi-layer trials generated 6 new V2.M3.EN.2 violations in trial:i02.ug.leaf_0003.02 and 6 additional V2.M3.EN.2 violations in trial:i02.ug.leaf_0004.03. Lateral and vertical translations that reduce M3 enclosure margins around embedded V2 cuts produce V2.M3.EN.2 violations.

Shrinking the M3 land of VIA_VIA23_1_3_36_36 in the y-direction by 40 dbu produced no net violation reduction and was rejected as net_positive by the cu_pool (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00); the identical resize_via_shape operation was also dropped at assemble with reason cu_pool:rejected_net_positive in trial:i01.ug.leaf_0035.13. Growing the same M3 land in y by 24 dbu was applied with a net −12 violation reduction (trial:i03.cu.def:VIA_VIA23_1_3_36_36.00). Enlarging the M3 via-land in the enclosure direction resolves V2.M3.EN.2-related deficits; shrinking it does not.

## V2.M3.AUX.2 — V2 Width Must Match M3 Width in the Perpendicular Direction

V2.M3.AUX.2 requires V2 to span exactly the same width as M3 in the direction perpendicular to the M3 run.

When a resize_end is applied to an M3 polygon's end edge, all V2 cut edges oriented in the perpendicular direction must remain strictly inside the new M3 boundary. In trial:i03.ug.leaf_0003.02, the repair of p1543 (right edge moved from 13876 to 13868 dbu) preserved V2.M3.AUX.2 because the V2 cut rightmost edges at 13860 dbu remained inside the resized extent. Avoid resize_end operations that move an M3 boundary edge to a position beyond an embedded V2 cut edge; trial:i03.ug.leaf_0003.02 confirms that such a displacement would violate V2.M3.AUX.2 and that checking the V2 edge positions before committing the resize is required.

## V3.M3.EN.1 — Enclosure of V3 by M3 on Two Opposite Sides (5 nm)

V3 appears in touched_layers for trial:i02.ug.leaf_0003.02 and trial:i02.ug.leaf_0004.03 (both gated_in), but no V3.M3.EN.1 violations appear in either trial's per_rule breakdown. No M3 repairs targeting V3.M3.EN.1 are present in the measured history.

## M3.W.1 — Minimum Width (18 nm)

The minimum M3 width is 18 nm (72 dbu). In trial:i03.ug.leaf_0003.02, the resize_end on p1543 was applied exclusively to the x-direction (high-x end edge) while leaving the y-dimension (72 dbu = 18 nm) unchanged, confirming that end-edge shrinks along one axis preserve the minimum width measured on the perpendicular axis when that dimension is not altered.

## Connectivity Gating

A trial combining an M3 resize_via_shape (−40 dbu in y on VIA_VIA23_1_3_36_36), one small M3 end shrink (−4 dbu on p1214), two large M3 end extensions (+192 dbu on p1178 and +100 dbu on p1255), and five instance moves was gated_out with conn_broken (trial:i01.ug.leaf_0034.12). A concurrent trial in the same design state that applied only uniform M3 y-axis shrinks of 64 dbu to 12 polygons was gated_in with conn_preserved (trial:i01.ug.leaf_0035.13). Avoid combining large M3 polygon end-extensions (+100 dbu or greater) with multiple instance translations in a single pass; trial:i01.ug.leaf_0034.12 shows this combination produced conn_broken gating while a simpler, uniform-resize pass on the same design state succeeded.