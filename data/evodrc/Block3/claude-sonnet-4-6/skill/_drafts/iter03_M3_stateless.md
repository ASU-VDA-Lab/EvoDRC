## Via-Cell X-Axis Expansion to Resolve V2.M3.EN.2 / V2.M3.AUX.2

Expanding V2 shapes along the x-axis within the via cell definition is an effective repair path for violations driven by V2.M3.EN.2 and V2.M3.AUX.2 on M3. In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, a cu_pool repair to cell `VIA_VIA23_1_3_36_36` combined lateral shifts (`move_via_shape` by ±144 dbu on x) with symmetric width expansions (`resize_via_shape` by +288 dbu on x) across three V2 shape indices, touching M2, M3, and V2. The result was a net reduction of 27 violations across units `leaf_0018` (−15) and `leaf_0019` (−12), and the trial was accepted (`decision: applied`).

The move-then-resize pattern observed in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 — shift the via shape toward the M3 edge to center it, then expand — directly addresses the projection-based two-opposite-sides enclosure check in V2.M3.EN.2 (minimum 5 nm on both sides) and the coincident-edge requirement in V2.M3.AUX.2. Apply this cell-level operation before attempting instance-level moves when M3/V2 enclosure violations are the dominant violation type in the window.

## Unit-Gate Instance Moves Touching M3: Gating Behavior

The unit_gate channel consistently gates in M3-touching operations when connectivity is preserved (`conn_preserved: true`), even when new in-crop violations are introduced.

- trial:i01.ug.leaf_0008.06 produced 0 new in-crop and 0 out-of-crop violations; gated_in.
- trial:i02.ug.leaf_0003.02 produced 0 new in-crop and 0 out-of-crop violations; gated_in.
- trial:i02.ug.leaf_0004.03 produced 2 new in-crop and 0 out-of-crop violations; gated_in (conn_preserved).
- trial:i03.ug.leaf_0001.00 produced 1 new in-crop and 0 out-of-crop violations; gated_in (conn_preserved).

Do not treat `n_new_in_crop > 0` as a disqualifying signal for unit_gate operations on M3 when `conn_preserved` is the stated gate reason. Across all four unit_gate trials touching M3, the gate accepted every operation where connectivity was preserved regardless of new in-crop count.

Do not apply operations that introduce out-of-crop violations: all four unit_gate trials in this record show `n_new_out_of_crop: 0`, and the gate accepted all of them. No trial in this history tests acceptance with `n_new_out_of_crop > 0`.

## Instance Move Magnitudes on M3-Touching Unit-Gate Operations

Unit-gate instance moves that touch M3 are bounded within the range of 16–144 dbu per axis in this history. Specifically: trial:i01.ug.leaf_0008.06 used x-moves of +4 and +136 dbu; trial:i02.ug.leaf_0003.02 used y-moves of ±48 and ±96 dbu; trial:i02.ug.leaf_0004.03 used x-move of +32 dbu combined with y-moves of ±24 and ±72 dbu; trial:i03.ug.leaf_0001.00 used an x-move of −16 dbu. The largest single-axis move observed is 144 dbu (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 via shape move). Larger displacements are untested against M3 spacing rules in this history; step sizes within this observed range have preserved connectivity across all trials.

## Polygon Resize-End Operations on M3 Polygons

The unit_gate channel resizes M3 polygon endpoints in conjunction with instance moves. In trial:i01.ug.leaf_0008.06, polygon `p1159` was extended at its high-y end by +20 dbu and polygon `p1261` was extended at its high-x end by +92 dbu while simultaneously moving instances; the result was 0 new violations and gated_in. In trial:i02.ug.leaf_0004.03, polygons `p1101`–`p1104` each had y-axis resize_end operations of ±24 or ±72 dbu alongside instance moves, resulting in 2 new in-crop violations but still gated_in. Apply polygon resize_end only at the same end as the associated instance displacement (high-end resize with positive-delta move, low-end resize with negative-delta move), consistent with both referenced trials.

## M3 Spacing Rules and Edge-Length Thresholds

M3.S.1 applies only to edges longer than 36 nm; M3.S.2 applies when one edge is ≤ 36 nm (tip) and the other is > 36 nm (side), with a 25 nm projection-based constraint; M3.S.3 applies when both edges are 24–36 nm, requiring 27 nm tip-to-tip; M3.S.4 applies when both edges are < 24 nm, requiring 31 nm; M3.S.5 applies when one edge is 24–36 nm and the other is < 24 nm, requiring 31 nm. The cu_pool via-cell x-axis expansions in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 reduced M3 violations by widening M3 coverage, which reduces the probability of short-edge (tip) configurations on the M3 side adjacent to V2. Avoid operations that shorten M3 edges below 36 nm along directions adjacent to other M3 polygons: this transitions the applicable rule from M3.S.1 (18 nm) to the stricter M3.S.2/S.3/S.4/S.5 regime (25–31 nm).

## V3.M3.EN.1 Considerations Under Instance Moves

Three trials — trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03, and trial:i03.ug.leaf_0001.00 — touch both M3 and V3 through instance moves. V3.M3.EN.1 requires that V3 be enclosed by M3 by at least 5 nm on two opposite sides (either left+right or top+bottom). Instance y-moves of ±48 and ±96 dbu (trial:i02.ug.leaf_0003.02) and y-moves of ±24/±72 dbu with x-move of +32 dbu (trial:i02.ug.leaf_0004.03) did not generate out-of-crop violations, consistent with enclosure being maintained. The x-move of −16 dbu in trial:i03.ug.leaf_0001.00 introduced 1 new in-crop violation while touching M3 and V3; the trial was still gated_in. Move V3-bearing instances in increments consistent with the observed range, and verify that opposing M3 edges extend at least 5 nm beyond the V3 boundary in the moved position before committing.