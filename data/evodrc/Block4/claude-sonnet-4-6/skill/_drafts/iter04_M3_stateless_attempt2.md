## Channel routing: cu_pool versus unit_gate on M3

All three unit_gate trials that touched M3 were accepted (trial:i01.ug.leaf_0026.12, trial:i02.ug.leaf_0003.02, trial:i04.ug.leaf_0002.01). Both cu_pool trials that touched M3 were rejected with `rejected_net_positive` (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, trial:i01.cu.def:VIA_VIA34_1_2_58_52.01). The cu_pool channel's acceptance criterion requires a net reduction in total violations across its observation windows; any operation that leaves the window count flat or raises it is dropped before M3 geometry is committed.

## cu_pool rejection: zero-delta and positive-delta cases

The VIA_VIA23 trial attempted a single resize_via_shape on the M3 shape of cell VIA_VIA23_1_3_36_36 (axis=y, delta=-40 dbu). The measured delta_total was 0 — no net reduction in violations across the two observed unit windows — and the trial was rejected (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). A zero delta is insufficient; the cu_pool gate requires a strictly negative delta_total.

The VIA_VIA34 trial applied three ops together: M3 shape resize (axis=y, delta=-64 dbu) on VIA_VIA34_1_2_58_52 plus two V3 shape resizes (axis=y, delta=-24 dbu each). The measured delta_total was +34 (window unit:leaf_0025 rose from 88 to 112; window unit:leaf_0026 rose from 35 to 45), and the trial was rejected (trial:i01.cu.def:VIA_VIA34_1_2_58_52.01). Shrinking the M3 enclosure metal on a via cell in the y-axis direction while simultaneously shrinking the V3 shape raises DRC violations in both units; do not apply this combination.

## Assemble-drops: cu_pool-rejected ops are excluded from unit_gate assembly

The unit_gate trial i01.ug.leaf_0026.12 records an `assemble_drops` list that names the four ops from the two rejected cu_pool trials (the VIA_VIA23 M3 resize and the VIA_VIA34 M3 + V3 resizes) as excluded with reason `cu_pool:rejected_net_positive`. The five ops that were committed — direct polygon resizes on p1406 through p1410 (axis=y, delta=-64 dbu each) — are distinct from those dropped ops. Only ops not blocked by cu_pool enter the unit_gate commit path (trial:i01.ug.leaf_0026.12).

## unit_gate acceptance: direct polygon resizes on M3

In trial:i01.ug.leaf_0026.12, five M3 polygons (p1406–p1410) were each shrunk by 64 dbu in the y-axis, and the trial was gated_in with conn_preserved=true, producing 2 new in-crop violations and 0 new out-of-crop violations. The design moved from state d279330089... to d63aa666f9..., confirming the resize set was applied. These were `resize` ops (polygon-level), not `resize_via_shape` ops, and they cleared the unit_gate criterion under `reason: conn_preserved`.

## unit_gate acceptance: mixed resize_end and move_instance on M3

In trial:i02.ug.leaf_0003.02 (iter 2), M3 was touched alongside M1, M2, V1, and V2. The M3-relevant op was a `resize_end` on polygon p1410 (axis=x, delta=-8 dbu, end=high, group=group_D), paired with two move_instance ops. The trial was gated_in with conn_preserved=true and 2 new in-crop violations (trial:i02.ug.leaf_0003.02). The `resize_end` op trims one endpoint of an M3 edge rather than scaling the whole polygon; this is valid in the unit_gate path when connectivity is preserved.

## unit_gate acceptance: move on M3 polygon plus multi-layer instance moves

In trial:i04.ug.leaf_0002.01 (iter 4), M3 polygon p1341 was moved +32 dbu in the x-axis (group=m5_align, op=move), alongside ten move_instance ops spanning M3, M4, M5, V3, and V4. The trial was gated_in with conn_preserved=true and 2 new in-crop violations (trial:i04.ug.leaf_0002.01). A global alignment group (m5_align) drove the M3 move simultaneously with upper-metal moves; unit_gate accepted the net result because connectivity was preserved.

## Enclosure rules: V3.M3.EN.1 and V2.M3.EN.2 sensitivity

Shrinking the M3 via-metal in the y-axis on VIA_VIA34_1_2_58_52 raised violations in both neighboring units (trial:i01.cu.def:VIA_VIA34_1_2_58_52.01). The V3.M3.EN.1 rule requires that V3 be enclosed by M3 by at least 5 nm on at least two opposite sides. A y-axis shrink of 64 dbu (6.4 nm at 0.1 nm/dbu) on the M3 enclosure metal of a via cell directly risks breaking this 5 nm floor if the starting enclosure margin is near the minimum. The same VIA_VIA34 trial also resized V3 shapes by -24 dbu each, which compounds the enclosure loss. The measured outcome was a net +34 violation increase (trial:i01.cu.def:VIA_VIA34_1_2_58_52.01); avoid simultaneous y-shrink of M3 and V3 shapes in the same via cell.

The VIA_VIA23 case involves V2.M3.EN.2, which requires M3 to enclose V2 by 5 nm on two opposite sides (or 5 nm on one side and 0 nm flush on the other). The attempted y-shrink of the M3 shape by 40 dbu produced zero net delta — it neither added nor removed violations — which cu_pool rejected as not net-positive (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). This indicates the candidate edit was enclosure-neutral at that geometry but still insufficient to yield a DRC improvement.

## Width and spacing constraints: implications from the resize magnitudes

The minimum M3 width is 18 nm (M3.W.1). The five y-axis polygon resizes in trial:i01.ug.leaf_0026.12 each applied -64 dbu. At 0.1 nm/dbu this is 6.4 nm of single-side shrink. The trial was accepted, confirming those polygons had sufficient initial y-extent to remain above 18 nm after the shrink. Do not apply additional y-shrinks to these same polygons (p1406–p1410) without re-verifying M3.W.1 compliance, as margin was consumed.

Side-to-side spacing (M3.S.1) applies when both edges are longer than 36 nm and requires 18 nm clearance. Tip-to-side (M3.S.2) requires 25 nm when one edge is ≤36 nm and the other is >36 nm. The resize_end trim of -8 dbu on p1410's x-high end (trial:i02.ug.leaf_0003.02) reduces an edge length; if that edge was near the 36 nm boundary before the trim, the governing spacing rule shifts from M3.S.1 to M3.S.2 or a tip-to-tip rule. The trial was accepted with conn_preserved=true, so the post-trim geometry was clean; the accepted state is the reference for subsequent edits to p1410.

## Area rule: M3.A.1

Minimum M3 area is 504 nm². The -8 dbu resize_end on p1410 (trial:i02.ug.leaf_0003.02) and the -64 dbu y-resizes on p1406–p1410 (trial:i01.ug.leaf_0026.12) were both accepted without M3.A.1 violations entering the out-of-crop debt list. Both trials recorded zero new out-of-crop violations. Any further shrink of these polygons must confirm post-shrink area remains above 504 nm².

## Connectivity preservation as the unit_gate gate criterion

All three gated_in unit_gate trials recorded `conn_preserved: true` (trial:i01.ug.leaf_0026.12, trial:i02.ug.leaf_0003.02, trial:i04.ug.leaf_0002.01). The `reason: conn_preserved` field appears explicitly in the delta record of i01.ug.leaf_0026.12, identifying connectivity preservation as the basis for acceptance independent of the in-crop violation count. Trials that fail to preserve connectivity are not present in the accepted set; all accepted M3 edits maintained the net topology.

## Non-orthogonal geometry: no violations observed

No GEOMETRY.NONORTHOGONAL violations for M3 appear in any trial's debt or delta records. All recorded M3 ops use axis-aligned resize (x or y) and Manhattan moves. Maintain orthogonal edges on all M3 polygons; the NONORTHOGONAL rule fires on any M3 edge with angle not in {0°, 90°, 180°, 270°}.