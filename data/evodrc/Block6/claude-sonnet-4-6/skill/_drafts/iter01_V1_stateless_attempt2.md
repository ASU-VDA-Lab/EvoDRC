## Repair operation types observed

All eight accepted trials in this iteration used `move_instance` and/or `resize_end` operations exclusively. No trial introduced a new polygon or deleted an existing one. Every trial touched layers M1, M2, and V1 simultaneously, consistent with V1 geometry being embedded inside cell instances whose M1 and M2 geometry moves with the instance (trial:i01.ug.Block6_union_row3.00, trial:i01.ug.Block6_union_row5.01, trial:i01.ug.Block6_union_row7.02, trial:i01.ug.Block6_union_row8.03, trial:i01.ug.leaf_0001.04, trial:i01.ug.leaf_0011.05, trial:i01.ug.leaf_0015.06, trial:i01.ug.leaf_0018.07).

## Direction of moves

Every `move_instance` delta recorded in this iteration was along the x-axis only (`delta_dbu` second component is 0 in all cases). No y-direction instance moves appear anywhere in the accepted record (trial:i01.ug.Block6_union_row3.00 delta [72,0]; trial:i01.ug.Block6_union_row8.03 delta [36,0]; trial:i01.ug.leaf_0011.05 delta [36,0]; trial:i01.ug.leaf_0018.07 delta [36,0]; trial:i01.ug.leaf_0015.06 deltas [28,0] and [28,0]; trial:i01.ug.Block6_union_row5.01 deltas all [36,0]; trial:i01.ug.Block6_union_row7.02 deltas [104,0] and [-36,0]; trial:i01.ug.leaf_0001.04 delta [112,0]).

## Resize-end operations accompany moves in multi-op repairs

Four of the eight accepted trials combined `move_instance` with at least one `resize_end` operation on an M2 polygon. In each such trial, the resize targeted the x-axis (`axis: "x"`) and extended the high or low end of the M2 polygon to maintain enclosure after the instance shifted. Specifically: trial:i01.ug.Block6_union_row5.01 resized polygon p2072 high end by +92 dbu after moving four instances by +36 dbu; trial:i01.ug.Block6_union_row7.02 resized p1903 high end by +124 dbu and p1920 low end by +56 dbu paired with instance moves of +104 and -36 dbu; trial:i01.ug.leaf_0001.04 resized p2016 high end by +132 dbu paired with a +112 dbu instance move; trial:i01.ug.leaf_0015.06 resized p1923 high end by +48 dbu paired with two +28 dbu instance moves.

This pattern is consistent with V1.M1.EN.1 and V1.M2.EN.2 requirements: shifting a V1-bearing instance without extending the adjacent M2 polygon would reduce M2 enclosure on the trailing edge below the 5 nm or 0 nm minimum, triggering violations. Resize-end on the leading end compensates.

## Connectivity gate: all accepted trials cleared it

All eight trials recorded `conn_preserved: true` and `decision: "gated_in"`, with `n_new_in_crop: 0` and `n_new_out_of_crop: 0` (trial:i01.ug.Block6_union_row3.00 through trial:i01.ug.leaf_0018.07). No trial was rejected by the connectivity gate. Repairs that would break a net are not recorded as accepted in this iteration's history; the absence of any `conn_preserved: false` or `decision: "rejected"` record means the gating criterion filtered out destructive moves before they reached the `gated_in` state.

## Move magnitude range

Accepted instance move magnitudes span 28 dbu to 112 dbu in this iteration. The smallest recorded move is 28 dbu (trial:i01.ug.leaf_0015.06, two instances). The largest is 112 dbu (trial:i01.ug.leaf_0001.04). Negative moves also appear: trial:i01.ug.Block6_union_row7.02 moved instance i0074 by -36 dbu (leftward) while moving i0093 by +104 dbu (rightward) in the same trial, producing a diverging pair. This trial was accepted, confirming that mixed-sign moves within a single trial are viable when connectivity is preserved.

## Multi-instance coordination within a trial

Three trials moved more than two instances simultaneously. Trial:i01.ug.Block6_union_row3.00 moved three instances (i0471, i0324, i0481) by the same +72 dbu delta. Trial:i01.ug.Block6_union_row5.01 moved four instances (i0015, i0459, i0437, i0446) each by +36 dbu and resized one polygon. Trial:i01.ug.Block6_union_row7.02 moved two instances by different amounts (+104 and -36 dbu) and resized two polygons. All were accepted. Uniform-delta group moves and mixed-delta group moves both appear in the accepted record.

## V1 spacing rules: operational implications

V1.S.1 governs minimum spacing between V1 masks along and across M2 tracks (18 nm on-track, 27 nm across parallel non-aligned tracks, 18 nm across aligned parallel tracks). V1.S.2 governs corner-to-corner spacing for vias with 5 nm M2 end-caps (23 nm, checked euclidean with 16.4 nm threshold). V1.S.3 governs corner-to-corner spacing for vias without end-caps (30 nm, euclidean). V1.S.4 governs spacing between one end-capped and one non-end-capped via (27 nm, euclidean corner). The x-direction instance moves in trials such as trial:i01.ug.Block6_union_row3.00 (+72 dbu = 7.2 nm at 0.1 nm/dbu) and trial:i01.ug.Block6_union_row8.03 (+36 dbu = 3.6 nm) are sub-grid relative to the 18 nm and 27 nm spacing minima, indicating that small incremental moves are sufficient to clear spacing violations when the initial gap deficit is small.

## V1.W.1: minimum width

V1.W.1 requires 18 nm minimum width along the M2 length direction. No `resize` operation in this iteration targeted a V1 polygon directly; all resizes targeted M2 polygons (p2072, p1903, p1920, p2016, p1923). V1 width violations, if present, were resolved indirectly by repositioning the instance carrying the V1 shape rather than by resizing V1 itself (trial:i01.ug.Block6_union_row3.00, trial:i01.ug.Block6_union_row8.03, trial:i01.ug.leaf_0011.05, trial:i01.ug.leaf_0018.07 each used only `move_instance` with no resize).

## V1.AUX.1 and V1.M2.AUX.2: containment rules

V1.AUX.1 requires V1 to lie inside the intersection of M1 and M2. V1.M2.AUX.2 requires V1 width perpendicular to M2 length to exactly match M2 width. Because all accepted trials preserved connectivity and produced zero new violations in crop (`n_new_in_crop: 0`), the move-and-resize combinations applied were consistent with maintaining V1 inside the M1-M2 overlap and preserving the V1-to-M2 width match. Trials that included a resize_end on M2 (trial:i01.ug.Block6_union_row5.01, trial:i01.ug.Block6_union_row7.02, trial:i01.ug.leaf_0001.04, trial:i01.ug.leaf_0015.06) did so on the x-axis only, which extends the M2 length and does not alter M2 width perpendicular to its length, leaving V1.M2.AUX.2 compliance intact.

## Design-state uniformity

All eight trials share the identical `design_state` hash `685706506817f4f5a58d885e68808402b61fcf189fed22cc344fa6dec38c0f99`, indicating they were all evaluated against the same base layout snapshot. Results are therefore directly comparable without accounting for cumulative layout drift between trials within this iteration.