## Operation patterns observed in iteration 1

All eight trials in this iteration used the `unit_gate` channel and all reached `decision: gated_in` with `conn_preserved: true`, `n_new_in_crop: 0`, and `n_new_out_of_crop: 0` (trial:i01.ug.Block6_union_row3.00, trial:i01.ug.Block6_union_row5.01, trial:i01.ug.Block6_union_row7.02, trial:i01.ug.Block6_union_row8.03, trial:i01.ug.leaf_0001.04, trial:i01.ug.leaf_0011.05, trial:i01.ug.leaf_0015.06, trial:i01.ug.leaf_0018.07). Every op set touched layers `["M1","M2","V1"]` together, confirming that V1 geometry does not move independently of its enclosing M1/M2 context in this channel.

## Move-instance as the primary V1 repair vehicle

The dominant operation across all eight trials is `move_instance` on the x-axis. Because V1 is placed inside cell instances, repositioning an instance translates V1 together with its bounding M1 and M2 geometry, which keeps V1.AUX.1 (V1 must be inside M1 and M2) and V1.M2.AUX.2 (V1 width must equal M2 width perpendicular to M2 length) satisfied without any direct polygon edits to V1.

Move magnitudes applied in this iteration (all x-direction, all in dbu):

| Trial | Move delta(s) | Instances moved |
|---|---|---|
| trial:i01.ug.Block6_union_row3.00 | +72 | i0471, i0324, i0481 (3 instances) |
| trial:i01.ug.Block6_union_row5.01 | +36 | i0015, i0459, i0437, i0446 (4 instances) |
| trial:i01.ug.Block6_union_row7.02 | +104 / −36 | i0093 / i0074 (mixed direction) |
| trial:i01.ug.Block6_union_row8.03 | +36 | i0078 |
| trial:i01.ug.leaf_0001.04 | +112 | i0404 |
| trial:i01.ug.leaf_0011.05 | +36 | i0066 |
| trial:i01.ug.leaf_0015.06 | +28 | i0213, i0204 |
| trial:i01.ug.leaf_0018.07 | +36 | i0060 |

Moving multiple instances in the same direction by the same delta (as in trial:i01.ug.Block6_union_row3.00 with +72 dbu applied to three instances, and trial:i01.ug.Block6_union_row5.01 with +36 dbu applied to four instances) preserved connectivity and introduced zero new violations, establishing that co-moving all instances that share a V1 spacing conflict region is a safe strategy for V1.S.1 / V1.S.2 / V1.S.3 / V1.S.4 violations caused by insufficient inter-via distance.

## Resize-end operations to maintain M2 enclosure after moves

Four of the eight trials paired `move_instance` with `resize_end` on M2 polygons. The resize extends or contracts one end of an M2 segment to maintain continuity or enclosure after nearby instances were repositioned:

- trial:i01.ug.Block6_union_row5.01: polygon p2072, axis x, high end, +92 dbu, alongside four +36 dbu instance moves.
- trial:i01.ug.Block6_union_row7.02: polygon p1903 high end +124 dbu (paired with +104 dbu move of i0093) and polygon p1920 low end +56 dbu (paired with −36 dbu move of i0074).
- trial:i01.ug.leaf_0001.04: polygon p2016 high end +132 dbu, alongside +112 dbu move of i0404.
- trial:i01.ug.leaf_0015.06: polygon p1923 high end +48 dbu, alongside +28 dbu moves of i0213 and i0204.

In all four cases the resize delta is larger than the corresponding move delta (92 > 36; 124 > 104; 132 > 112; 48 > 28). Apply a `resize_end` to the M2 segment end that points away from the moved instance whenever the instance delta alone would leave the M2 end-cap shorter than the 5 nm minimum required by V1.M2.EN.2. The surplus between resize delta and move delta (e.g., 92 − 36 = 56 dbu in trial:i01.ug.Block6_union_row5.01) represents additional M2 length being added to restore or maintain the enclosure margin.

When a move is in the positive-x direction, the high end of the connecting M2 segment is the end that risks losing enclosure; `resize_end` with `end: high` corrects this (trial:i01.ug.Block6_union_row5.01, trial:i01.ug.leaf_0001.04, trial:i01.ug.leaf_0015.06). When a move is in the negative-x direction (−36 dbu for i0074 in trial:i01.ug.Block6_union_row7.02), the low end of the opposing M2 segment requires extension; `resize_end` with `end: low` corrects this.

## Spacing rules: projection vs. euclidean distinction

V1.S.1 uses projection-based spacing checks. V1.S.2, V1.S.3, and V1.S.4 use euclidean checks for corner-to-corner scenarios. The `move_instance` repairs in this iteration resolved spacing violations without needing to distinguish which spacing rule fired, because co-moving all instances in a conflict cluster (as in trial:i01.ug.Block6_union_row3.00 and trial:i01.ug.Block6_union_row5.01) increases inter-instance distances uniformly, satisfying both projection and euclidean checks simultaneously.

Mixed-direction moves (trial:i01.ug.Block6_union_row7.02: +104 for i0093 and −36 for i0074) resolve violations where two via clusters need to move apart from each other; this pattern is appropriate when only one instance can move in the positive-x direction due to downstream constraints.

## V1.W.1 and V1.M1.EN.1 in the context of instance moves

No trial applied any direct resize to a V1 polygon. V1 width (V1.W.1, minimum 18 nm along M2 length) and M1 enclosure of V1 (V1.M1.EN.1, 5 & 2 nm on opposite sides) are fixed by the cell definition. Because all repairs used `move_instance` rather than resizing V1 directly, these two rules are maintained implicitly: moving a whole instance cannot change the V1 dimensions or the relative M1-to-V1 enclosure within that instance. Do not apply `resize_end` or any direct polygon edit to V1 polygons; all measured successful repairs (trial:i01.ug.Block6_union_row3.00 through trial:i01.ug.leaf_0018.07) avoided direct V1 polygon modification entirely.

## Connectivity preservation

All eight trials set `conn_preserved: true` and `target: null`. The `unit_gate` channel enforces connectivity preservation as a gate condition before committing any move. Move sets that would break nets are not accepted. The zero new-violation count across all trials confirms that, when connectivity is preserved, x-axis instance moves in this design do not introduce secondary V1 DRC violations within the repair crop region.