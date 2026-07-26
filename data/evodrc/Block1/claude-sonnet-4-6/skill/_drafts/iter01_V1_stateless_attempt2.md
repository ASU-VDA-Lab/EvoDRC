## Repair Acceptance Is Governed by Connectivity Preservation

Every trial accepted in this iteration carried `conn_preserved: true` and received `decision: gated_in` (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row10.01, trial:i01.ug.Block1_union_row3.03, trial:i01.ug.Block1_union_row4.04, trial:i01.ug.Block1_union_row5.05, trial:i01.ug.Block1_union_row6.06, trial:i01.ug.Block1_union_row8.07, trial:i01.ug.Block1_union_row9.08, trial:i01.ug.leaf_0004.09, trial:i01.ug.leaf_0020.10, trial:i01.ug.leaf_0031.11). The single trial with `conn_preserved: false` was rejected: trial:i01.ug.leaf_0034.12 produced 89 new in-crop violations and broke net topology, yielding `decision: gated_out`. Do not accept any V1 repair sequence that breaks electrical connectivity; net preservation is the binding acceptance gate, as confirmed by trial:i01.ug.leaf_0034.12 versus the full set of accepted trials above.

## New In-Crop Violations Do Not Block Acceptance When Connectivity Is Preserved

Several accepted trials introduced new DRC violations within the crop window without triggering rejection. trial:i01.ug.Block1_union_row1.00 added 4 new in-crop violations (`n_new_in_crop: 4`), trial:i01.ug.Block1_union_row6.06 added 1, and trial:i01.ug.leaf_0031.11 added 4; all three were `gated_in` with `conn_preserved: true`. A repair that introduces a bounded number of new in-crop violations is accepted provided connectivity is preserved, as these three trials confirm.

## M2 Endpoint Resizing Accompanies Instance Moves in Accepted Repairs

Multiple accepted trials paired `resize_end` operations on M2 polygons with `move_instance` operations. trial:i01.ug.Block1_union_row1.00 extended p1320 high-x end by 136 dbu alongside moving i0507 by +136 dbu on x. trial:i01.ug.Block1_union_row5.05 applied four `resize_end` ops (deltas 156, 56, 92, 48 dbu) paired with three `move_instance` ops on M1/M2/V1. trial:i01.ug.Block1_union_row6.06 applied five `resize_end` ops (deltas 36, 128, 36, 128, 92 dbu) alongside five `move_instance` ops. trial:i01.ug.Block1_union_row8.07 applied two `resize_end` ops (delta 192 dbu each) alongside three `move_instance` ops. Extending the M2 polygon endpoint to cover the new via position after a move satisfies V1.AUX.1 (V1 inside M1 and M2), V1.M2.AUX.2 (V1 width matches M2 width perpendicular to M2 run direction), and V1.M2.EN.2 (M2 enclosure of V1 by 5 and 5 nm or 5 and 0 nm), as the four cited trials demonstrate.

## M2 Resize Delta May Exceed Instance Move Delta to Satisfy Enclosure

In trial:i01.ug.Block1_union_row8.07, both i0244 and i0079 were moved +136 dbu on x, but their associated M2 polygons p1388 and p1345 were extended by +192 dbu on the high-x end. The larger M2 extension relative to the via displacement maintains the 5 nm M2 end-cap enclosure required by V1.M2.EN.2 and the enclosure geometry consumed by V1.S.1's mask derivation. Use a resize delta equal to or larger than the move delta when the via approaches the M2 wire's existing endpoint, as trial:i01.ug.Block1_union_row8.07 confirms.

## Common Move Magnitudes in Accepted Repairs

Accepted move deltas cluster at small integer multiples of 36 dbu. Observed values: 36 dbu in trial:i01.ug.Block1_union_row4.04, trial:i01.ug.Block1_union_row9.08, trial:i01.ug.leaf_0004.09, trial:i01.ug.leaf_0031.11; 64 dbu in trial:i01.ug.Block1_union_row8.07; 72 dbu in trial:i01.ug.Block1_union_row3.03, trial:i01.ug.Block1_union_row6.06; 108 dbu in trial:i01.ug.Block1_union_row10.01; 136 dbu in trial:i01.ug.Block1_union_row1.00 and trial:i01.ug.Block1_union_row5.05. Negative (leftward) displacements also appear in accepted repairs: -36 dbu in trial:i01.ug.Block1_union_row5.05 (i0433), -64 dbu in trial:i01.ug.Block1_union_row8.07 (i0258), -72 dbu in trial:i01.ug.Block1_union_row6.06 (i0455), -56 dbu in trial:i01.ug.leaf_0020.10 (i0082).

## Large Locus and Cross-Layer Operations Carry Connectivity Risk

The rejected trial trial:i01.ug.leaf_0034.12 had a locus spanning 1728-14256 x 2068-13680 dbu, the largest in the iteration, and touched six layers (M1, M2, M3, M4, V1, V2), including a `resize_via_shape` on an M3 cell. This produced 89 new in-crop violations and broke connectivity. Every accepted trial operated on at most three layers (M1, M2, V1) and used only `move_instance` and `resize_end` operations (trial:i01.ug.Block1_union_row1.00 through trial:i01.ug.leaf_0031.11). Limit V1 repairs to the M1/M2/V1 layer set and avoid cross-tier via reshaping operations that can cascade into connectivity failures, as the contrast between trial:i01.ug.leaf_0034.12 and all accepted trials demonstrates.

## V1 Must Remain Inside M1 and M2 with Width Matching M2

V1.AUX.1 requires every V1 polygon to lie entirely within M1 intersected with M2. V1.M2.AUX.2 requires that V1's dimension perpendicular to the M2 run direction exactly equals the M2 width on that axis. A `move_instance` that shifts a via must therefore be accompanied by the M2 `resize_end` that keeps M2 fully covering the new via position, as shown in trial:i01.ug.Block1_union_row1.00 (i0507 +136 dbu; p1320 high-x end +136 dbu) and trial:i01.ug.Block1_union_row8.07 (i0244 and i0079 each +136 dbu; p1388 and p1345 high-x ends each +192 dbu).

## V1 Spacing Rules: End-Cap Presence Determines the Active Threshold

V1.S.1 enforces projection-based spacing through derived mask geometries. The applicable minimum depends on the M2 track relationship: same track (18 nm), parallel unaligned tracks (27 nm), parallel aligned tracks (18 nm). V1.S.2 checks Euclidean spacing (threshold 16.4 nm, corresponding to 23 nm corner-to-corner) between `v1_wec_mask` shapes (vias that have a 5 nm M2 end-cap). V1.S.3 checks Euclidean spacing (threshold 16.12 nm, corresponding to 30 nm corner-to-corner) between `v1_nec_mask` shapes (vias without end-cap), excluding violations that also appear in the projection check. V1.S.4 checks Euclidean separation (threshold 17.11 nm, corresponding to 27 nm corner-to-corner) between `v1_wec_mask` and `v1_nec_mask`. Repair moves must satisfy all four checks in the post-move configuration. The accepted sequences in trial:i01.ug.Block1_union_row5.05 and trial:i01.ug.Block1_union_row6.06 confirm that coordinated `move_instance` plus `resize_end` sets with offsets chosen to align with the M2 track pitch satisfy all active spacing rules simultaneously.

## M1 and M2 Enclosure Requirements

V1.M1.EN.1 requires M1 to enclose V1 by at least 5 nm on one pair of opposite sides and at least 2 nm on the orthogonal pair. V1.M2.EN.2 requires M2 to enclose V1 by at least 5 nm on one axis and 5 nm or 0 nm (flush end permitted) on the other axis. All eleven accepted trials satisfied these enclosure rules within the crop window. The multi-op repair sequences in trial:i01.ug.Block1_union_row5.05 (7 ops) and trial:i01.ug.Block1_union_row6.06 (10 ops) show that `resize_end` adjustments with varying deltas on low and high ends of M2 polygons maintain enclosure on both axes simultaneously while resolving spacing violations.

## V1 Width Minimum

V1.W.1 sets the minimum V1 width along the M2 length direction at 18 nm. All accepted trials moved existing via instances without resizing via shapes, preserving the as-drawn width. Do not apply `resize_end` or `resize_via_shape` to V1 geometry in a way that reduces via width below 18 nm; the accepted trials (e.g., trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row6.06) achieve repair exclusively through position adjustment and M2 wire extension, leaving via dimensions intact.

## No Nonorthogonal Geometry

The NONORTHOGONAL rule flags any V1 edge with an angle outside 0, 90, 180, or 270 degrees. Every accepted trial applied only axis-aligned `move_instance` and `resize_end` operations with single-axis delta_dbu values, producing no diagonal edges (trial:i01.ug.Block1_union_row1.00 through trial:i01.ug.leaf_0031.11). Restrict all V1 shape modifications to rectilinear moves and axis-aligned endpoint stretches; diagonal or angled edits are not represented in any recorded operation and would trigger the NONORTHOGONAL violation.