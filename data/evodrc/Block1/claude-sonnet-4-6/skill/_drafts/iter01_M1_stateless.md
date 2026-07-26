## Repair operation patterns on M1

All 11 gated_in trials operate exclusively in the horizontal (x) direction. Every `move_instance` delta and every `resize_end` operation across trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row10.01, trial:i01.ug.Block1_union_row3.03, trial:i01.ug.Block1_union_row4.04, trial:i01.ug.Block1_union_row5.05, trial:i01.ug.Block1_union_row6.06, trial:i01.ug.Block1_union_row8.07, trial:i01.ug.Block1_union_row9.08, trial:i01.ug.leaf_0004.09, trial:i01.ug.leaf_0020.10, and trial:i01.ug.leaf_0031.11 carries `[dx, 0]` form — dy equals zero in every record. The gated_out trial:i01.ug.leaf_0034.12 also contains only horizontal deltas on its instance moves. No y-direction perturbation appears in any M1 repair record at this iteration.

## Move delta granularity and grid alignment

The recurrent unit delta is 36 dbu (equal to M1.W.1 minimum 18 nm plus M1.S.1 minimum 18 nm — the minimum M1 pitch). It appears as the sole delta in trial:i01.ug.Block1_union_row9.08 (three instances, all 36 dbu), trial:i01.ug.leaf_0004.09 (36 dbu), and trial:i01.ug.leaf_0031.11 (36 dbu). Larger successful deltas are 72 (trial:i01.ug.Block1_union_row4.04, trial:i01.ug.Block1_union_row6.06), 108 (trial:i01.ug.Block1_union_row10.01, trial:i01.ug.Block1_union_row3.03), 136 (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row5.05, trial:i01.ug.Block1_union_row8.07), and 192 dbu (trial:i01.ug.Block1_union_row8.07) — all multiples of 36 dbu.

Sub-pitch and off-pitch deltas also appear in gated_in records: 8 dbu (instance i0300 in trial:i01.ug.Block1_union_row4.04), 37 dbu (instances i0482 and i0496 in trial:i01.ug.Block1_union_row1.00), and 64 dbu (instances i0199, i0258, i0100 in trial:i01.ug.Block1_union_row8.07 — not a multiple of 36). These non-grid moves are accepted when connectivity is preserved, so delta alignment to the 36 dbu pitch is not itself the gating criterion.

## resize_end operations address M1 enclosure rules

`resize_end` on M1 polygons always specifies `axis: "x"`, extending or retracting a horizontal end of the polygon. High-end extensions occur in trial:i01.ug.Block1_union_row1.00 (polygon p1320, delta 136 dbu), trial:i01.ug.Block1_union_row5.05 (p1295 delta 156, p1366 delta 92, p1297 delta 48), trial:i01.ug.Block1_union_row6.06 (p1323 delta 36, p1329 delta 128, p1325 delta 128, p1250 delta 92), and trial:i01.ug.Block1_union_row8.07 (p1388 and p1345, both delta 192). Low-end adjustments also appear: trial:i01.ug.Block1_union_row5.05 retracts the low end of p1305 (delta 56) and trial:i01.ug.Block1_union_row6.06 retracts the low end of p1346 (delta 36). All trials using resize_end on M1 are gated_in. These operations extend M1 end coverage to satisfy V0.M1.EN.1 (5 nm minimum enclosure of V0 by M1 on two opposite sides) and V1.M1.EN.1 (5 nm / 2 nm enclosure of V1 by M1 on opposite sides); the delta magnitudes are consistently larger than the 5 nm enclosure minimums, reflecting that the resize also accommodates the displaced instance.

## Negative (leftward) moves succeed when coordinated with resize_end

Three gated_in trials include leftward x-direction instance moves. trial:i01.ug.Block1_union_row5.05 moves instance i0433 by -36 dbu paired with a low-end retraction of p1305 (delta 56 dbu). trial:i01.ug.Block1_union_row6.06 moves instance i0455 by -72 dbu paired with a low-end retraction of p1346 (delta 36 dbu). trial:i01.ug.Block1_union_row8.07 moves instance i0258 by -64 dbu alongside high-end extensions of p1388 and p1345 (delta 192 dbu each). All three produce 0 new in-crop violations and are gated_in. In every case the signed move and the resize_end act on the same region, keeping V0/V1 enclosure intact while shifting the instance.

## Gating criterion: connectivity preservation, not violation count

Trials that introduce new in-crop violations are gated_in when conn_preserved is true. trial:i01.ug.Block1_union_row1.00 introduced 4 new violations and was gated_in. trial:i01.ug.Block1_union_row6.06 introduced 1 new violation and was gated_in. trial:i01.ug.leaf_0031.11 introduced 4 new violations (a single 36 dbu instance move with no resize_end) and was gated_in. In all three cases n_new_out_of_crop remains 0. The sole gated_out record, trial:i01.ug.leaf_0034.12, was rejected because conn_preserved is false (reason: "conn_broken"), not because of its 89 new in-crop violations.

n_new_out_of_crop is 0 in every trial, including trial:i01.ug.leaf_0034.12, confirming that none of the repair operations displaced violations across the crop boundary regardless of outcome.

## Cross-layer scope correlates with connectivity risk

Every gated_in trial touches exactly three layers: M1, M2, and V1. trial:i01.ug.leaf_0034.12, the only gated_out record, touches six layers: M1, M2, M3, M4, V1, and V2. That trial also introduces a `resize_via_shape` operation on the M3 VIA_VIA23_1_3_36_36 cell (y-axis, delta -40 dbu) — the only via-shape resize in the entire history — and includes two large polygon resizes (p1178 delta 192, p1255 delta 100) alongside five instance moves. The combination of expanded layer scope, via-shape resizing across multiple metal levels, and the larger number of distinct operations (10 ops vs a maximum of 10 in trial:i01.ug.Block1_union_row6.06 which was gated_in) coincides with the connectivity breakage. Repairs in this iteration that remain within M1/M2/V1 and avoid via-shape modifications at higher metal levels preserve connectivity.

## Operation count and repair complexity

Successful trials range from 1 operation (trial:i01.ug.leaf_0004.09, trial:i01.ug.leaf_0020.10, trial:i01.ug.leaf_0031.11) to 10 operations (trial:i01.ug.Block1_union_row6.06). Higher operation counts at or below 10 ops do not preclude a gated_in outcome when confined to M1/M2/V1. The gated_out trial:i01.ug.leaf_0034.12 also has 10 ops, so operation count alone does not distinguish safe from unsafe repairs; layer scope and via-shape manipulation are the distinguishing factors.

## All trials share the same base design state

Every record in this iteration carries `design_state: "796a62668ac7e368d71fcb67038c38c1b27a9a85bb6eda7a3ee1f1ebd18ab3b3"`, confirming that all 12 trials are independent repair candidates applied to the same starting layout. The gated_in decisions are additive candidates evaluated against this common baseline, not a sequential repair chain.