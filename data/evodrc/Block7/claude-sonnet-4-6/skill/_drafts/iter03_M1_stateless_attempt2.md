## Operation Types Applied to M1

The history records four operation types across 43 trials in three iterations, all with `conn_preserved: true` and `decision: gated_in`. The operations are: `move_instance` (translating a cell instance and its contained M1 geometry), `resize_end` (extending or retracting one endpoint of a named polygon along a specified axis and end), `resize` (uniformly adjusting a polygon along an axis), and `move` (translating a whole polygon by a scalar delta on one axis). Every accepted fix in this corpus preserved connectivity.

## Instance Translation (move_instance)

Instance moves are the dominant repair mechanism. The most frequent x-axis delta is 36 dbu, appearing in trial:i01.ug.Block7_union_row11.01, trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row6.18, trial:i01.ug.Block7_union_row9.21, and many others. Larger x-deltas (72, 108, 136 dbu) appear when the instance must clear wider spacing margins, as in trial:i01.ug.Block7_union_row14.04 (108 dbu on i0920) and trial:i01.ug.Block7_union_row24.14 (136 dbu on i0215). Y-axis instance moves occur in trial:i01.ug.Block7_union_row16.06 (delta [0,-12]), trial:i01.ug.Block7_union_row19.09 (delta [0,-48]), trial:i02.ug.Block7_union_row15.03 (delta [0,-84]), and trial:i01.ug.leaf_0095.26 (delta [0,48]); each of these trials also touches M2, M3, V1, or V2, confirming that y-direction moves propagate through the via stack. Apply y-axis moves only when the corresponding via enclosure rules (V0.M1.EN.1, V1.M1.EN.1) are re-verified on the shifted geometry (trial:i02.ug.leaf_0014.08, trial:i03.ug.leaf_0011.07).

## resize_end: Polygon Endpoint Adjustment

`resize_end` extends or retracts one end of an M1 polygon to correct enclosure or spacing defects. In trial:i01.ug.Block7_union_row10.00, the high-x end of p3286 was extended 308 dbu to establish V0 enclosure after a 52-dbu instance move. In trial:i01.ug.Block7_union_row7.19, p3317's high-x end was extended 128 dbu; in trial:i01.ug.Block7_union_row24.14, three polygons (p3058, p3635, p3564) each received high-x extensions of 136, 120, and 128 dbu respectively to satisfy enclosure requirements after large instance moves. In trial:i01.ug.Block7_union_row13.03, both the low-x (56 dbu) and high-x (100 dbu) ends of p3526 were extended in the same pass, together with a 192-dbu high-x extension on p3525, indicating a via insufficiently enclosed on both sides. Apply `resize_end` at the end not constrained by a neighboring metal polygon to avoid introducing a new M1.S.1 or M1.S.2 violation; trial:i01.ug.Block7_union_row17.07 extends only the low-x end of p3187 (56 dbu), and trial:i01.ug.Block7_union_row3.15 extends only the low-x end of p3384 (56 dbu), consistent with the adjacent high-x side being already bounded.

## resize and move (Polygon Operations)

The `resize` operation uniformly adjusts a polygon's size along one axis. In trial:i01.ug.Block7_union_row15.05, p3586 received a 160-dbu x-resize; in trial:i01.ug.Block7_union_row19.09, polygons p3619, p3654, and p3523 each received x-resizes of 40, -72, and 72 dbu respectively; in trial:i02.ug.Block7_union_row15.03, p3592 received a 96-dbu y-resize. Use `resize` when both ends of the polygon need to grow uniformly and neither end abuts a spacing constraint, as evidenced by trial:i01.ug.Block7_union_row15.05 applying this alongside 7 instance moves across a wide locus.

The `move` operation translates a whole polygon without changing its shape. It appears in trial:i01.ug.Block7_union_row16.06 (p3516, y-axis, -12 dbu) and trial:i02.ug.leaf_0014.08 (p3515, y-axis, -12 dbu); both trials also move instances in the same direction and both touch M2/M3/V1/V2. Apply `move` to shift a standalone M1 polygon away from a spacing violator while maintaining its length, consistent with the -12 dbu y-shifts observed in both of those trials.

## Multi-Operation Compound Repairs

When multiple DRC errors co-locate, fixes combine instance moves with polygon resizes. Trial:i01.ug.Block7_union_row14.04 applies 11 operations across a locus approximately 23 kDBU wide: 9 instance moves (including one negative-direction move of -36 dbu on i0519) plus 3 `resize_end` extensions on polygons p3200, p3215, and p3539. Trial:i01.ug.Block7_union_row5.17 applies 6 operations including two `resize_end` extensions of 92 dbu each on polygons p3737 and p3746. The number of operations scales with locus width: trials with locus x-spans below 4 kDBU (trial:i01.ug.leaf_0001.22, trial:i01.ug.Block7_union_row3.15, trial:i02.ug.leaf_0022.10) use 1-2 operations, while trials with spans above 15 kDBU (trial:i01.ug.Block7_union_row14.04 at ~22976 dbu, trial:i01.ug.Block7_union_row5.17 at ~15048 dbu) use 6-11.

## Units Requiring Multiple Iteration Passes

Several units returned as targets across successive iterations, indicating that initial repairs introduced secondary violations or only partially resolved the original set.

Block7_union_row13 required three consecutive passes: trial:i01.ug.Block7_union_row13.03 (6 ops, 1 new in-crop violation introduced), trial:i02.ug.Block7_union_row13.02 (3 ops, 0 new in-crop), trial:i03.ug.Block7_union_row13.01 (2 ops, 0 new in-crop). The progressive decrease in op count and new-violation count demonstrates convergence; the iter-1 pass introduced 1 new in-crop violation that drove the iter-2 and iter-3 follow-ups.

Block7_union_row20 was addressed in all three iterations: trial:i01.ug.Block7_union_row20.10 (2 ops, including an M2 add_polygon), trial:i02.ug.Block7_union_row20.04 (3 ops: 2 instance moves plus 1 resize_end on p3048), trial:i03.ug.Block7_union_row20.02 (1 op: instance move on i0600). The add_polygon in iter 1 established M2 connectivity needed by the shifted M1, but M1 spacing or enclosure required two further fix passes.

Block7_union_row10 appeared in iter 1 (trial:i01.ug.Block7_union_row10.00, 6 ops) and again in iter 3 (trial:i03.ug.Block7_union_row10.00, 2 ops), with no iter-2 entry for that unit. The iter-3 fix (1 instance move plus 1 resize_end on p3305) is a targeted correction of a residual violation exposed by the global iter-2 changes.

leaf_0002 appeared in iter 1 (trial:i01.ug.leaf_0002.23, 1 op, 2 new in-crop) and iter 3 (trial:i03.ug.leaf_0002.04, 5 ops touching M1/M2/M3/V1/V2). The iter-1 single-instance move introduced 2 new in-crop violations; the iter-3 repair added an M3 polygon and applied a resize_end on p3300 (axis x, delta -88 dbu, end low) to resolve the resulting via-layer enclosure issues.

Do not treat a unit as resolved when its trial has `n_new_in_crop > 0`; follow-up iterations are required (trial:i01.ug.Block7_union_row13.03 with 1 new in-crop led to trial:i02.ug.Block7_union_row13.02; trial:i01.ug.leaf_0002.23 with 2 new in-crop led to trial:i03.ug.leaf_0002.04).

## n_new_in_crop as a Convergence Signal

Trials where `n_new_in_crop > 0` are accepted when connectivity is preserved but require further iteration. The trials with nonzero counts are: trial:i01.ug.Block7_union_row13.03 (1), trial:i01.ug.Block7_union_row4.16 (1), trial:i01.ug.Block7_union_row5.17 (1), trial:i01.ug.Block7_union_row21.11 (9), trial:i01.ug.Block7_union_row22.12 (2), trial:i01.ug.Block7_union_row24.14 (2), trial:i01.ug.leaf_0002.23 (2), trial:i01.ug.leaf_0024.25 (1), trial:i02.ug.leaf_0017.09 (3), trial:i02.ug.leaf_0022.10 (3), trial:i03.ug.leaf_0007.05 (3), trial:i03.ug.leaf_0008.06 (1). The highest count, trial:i01.ug.Block7_union_row21.11 (9 new in-crop from 2 instance moves of 36 dbu each), results from large-delta moves that simultaneously shift many M1 metal ends, each of which may fall short of enclosure or spacing on the opposite boundary.

## V0 and V1 Enclosure on M1

V0.M1.EN.1 requires M1 to enclose V0 by 5 nm on two opposite sides (5&5 or 5&0 pattern). V1.M1.EN.1 requires 5 nm on one side and 2 nm on the opposite. Fixes use `resize_end` to extend the M1 polygon over the via, as in trial:i01.ug.Block7_union_row10.00 (308-dbu high-x extension on p3286), trial:i01.ug.Block7_union_row7.19 (128-dbu high-x extension on p3317), and trial:i02.ug.Block7_union_row9.06 (112-dbu high-x extension on p3683). Instance moves that reposition the via relative to existing M1 metal are used when the metal is already long enough to provide enclosure after the shift, as in trial:i01.ug.Block7_union_row11.01 and trial:i01.ug.Block7_union_row6.18. Avoid shrinking M1 in the direction perpendicular to the metal run when V0 or V1 is present, as V0.M1.AUX.3 requires V0 width to match M1 width in that direction; the history exclusively applies width-preserving moves along the metal run axis when vias are involved (trial:i01.ug.Block7_union_row9.21, trial:i01.ug.Block7_union_row6.18).

## Orthogonality Maintenance

All resize and move operations in this history are strictly axis-aligned: `resize_end` and `resize` specify axis as "x" or "y"; `move` specifies axis as "x" or "y"; `move_instance` uses delta vectors with integer dbu components and no diagonal term. No non-orthogonal delta appears in any of the 43 trials. Maintain axis-aligned operations on M1 to avoid NONORTHOGONAL markers; trial:i01.ug.Block7_union_row16.06 uses delta [0,-12] and trial:i01.ug.leaf_0095.26 uses delta [0,48], both strictly axis-aligned, as representative of the pattern observed throughout the corpus.

## add_polygon Usage on Adjacent Layers

No trial adds a polygon directly on M1. New polygons appear only on M2 (trial:i01.ug.Block7_union_row20.10, a rectangle at coordinates [5992,22824]-[6048,22896]) and M3 (trial:i03.ug.leaf_0002.04, at coordinates [11664,11756]-[11908,11828]). These additions restore via landing pads displaced by M1 or instance movements on the same repair pass, not to fix M1 DRC directly.