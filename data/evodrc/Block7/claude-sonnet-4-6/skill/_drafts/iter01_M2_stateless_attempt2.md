## Repair Operation Patterns

Every trial in this iteration carries `decision=gated_in` with `conn_preserved=true` (trial:i01.ug.Block7_union_row10.00 through trial:i01.ug.leaf_0095.26). Connectivity preservation is the hard gate; all 27 accepted repairs maintained it.

## n_new_in_crop Does Not Gate Acceptance

Trials with `n_new_in_crop > 0` were all accepted. Values of 1 appear in trial:i01.ug.Block7_union_row13.03, trial:i01.ug.Block7_union_row19.09, trial:i01.ug.Block7_union_row4.16, trial:i01.ug.Block7_union_row5.17, and trial:i01.ug.leaf_0024.25. Values of 2 appear in trial:i01.ug.Block7_union_row22.12, trial:i01.ug.Block7_union_row24.14, and trial:i01.ug.leaf_0002.23. A value of 9 appears in trial:i01.ug.Block7_union_row21.11. All were gated_in. Do not discard a repair candidate solely because `n_new_in_crop > 0`; the acceptance criterion is connectivity preservation, not a zero new in-crop violation count.

## Dominant Repair Primitives on M2

The primary primitives are `move_instance` along the x-axis and `resize_end` on individual M2 polygon endpoints. Pure y-direction displacement is rare: only trial:i01.ug.Block7_union_row16.06 (delta [0,-12]) and trial:i01.ug.leaf_0095.26 (delta [0,48] with `resize_end axis=y`) include y-axis adjustments. All other trials repair exclusively in x.

The most common `move_instance` step is 36 dbu, appearing in trial:i01.ug.Block7_union_row11.01, trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row6.18, and trial:i01.ug.Block7_union_row9.21, among others. Larger steps of 72, 108, 136, and 288 dbu appear in trial:i01.ug.Block7_union_row18.08, trial:i01.ug.Block7_union_row7.19, trial:i01.ug.Block7_union_row13.03, and trial:i01.ug.Block7_union_row10.00 respectively, when greater separation is required.

## Bidirectional Instance Moves

When instances on both sides of an M2 spacing gap contribute to the violation, moving them in opposite x-directions simultaneously is an accepted repair strategy. Trial:i01.ug.Block7_union_row14.04 moves i0519 by [-36,0] and i0920 by [+108,0] in the same operation sequence. Trial:i01.ug.Block7_union_row18.08 moves i0428 by [-72,0] while moving i0978, i0317, i0292, and i0442 by [+72,0]. Trial:i01.ug.Block7_union_row19.09 moves i0026 by [-72,0] while i0294 moves [+36,0] and i0418 moves [+72,0]. Use bidirectional moves when instances on both sides of a spacing gap each need to be repositioned; all three of these trials were gated_in.

## resize_end Accompanying move_instance

`resize_end` operations on M2 polygon endpoints are paired with `move_instance` in many trials. When a polygon endpoint must advance independently of the instance grid step, `resize_end` is applied in addition to the move. Trial:i01.ug.Block7_union_row10.00 combines a +288 dbu instance move on i1180 with a `resize_end end=high` of +308 dbu on the separate polygon p3286. Trial:i01.ug.Block7_union_row5.17 pairs +36 dbu instance moves with `resize_end end=high` of +92 dbu on both p3737 and p3746. Trial:i01.ug.Block7_union_row7.19 pairs a +108 dbu instance move with a `resize_end end=high` of +128 dbu on p3317.

A `move_instance` and a `resize_end` that go in opposing x-directions on separate objects is acceptable when connectivity is preserved. Trial:i01.ug.Block7_union_row3.15 moves i1623 by [-36,0] while trimming p3384's low end by +56 dbu (moving that edge rightward); the result was gated_in. Trial:i01.ug.Block7_union_row8.20 moves i1891 by [-36,0] while trimming p3430's low end by +56 dbu; also gated_in. Do not assume that opposing-direction adjustments on distinct objects cancel each other's geometric effect; each acts on a different edge or shape.

## Bidirectional resize_end on the Same Polygon

Trial:i01.ug.Block7_union_row13.03 applies `resize_end` to polygon p3526 twice in the same repair: first `end=low` by +56 dbu (retracting the low edge rightward), then `end=high` by +100 dbu (extending the high edge rightward). Both operations act on the same polygon and the trial was gated_in. This pattern shifts the polygon's footprint while simultaneously adjusting its total length. Apply bidirectional `resize_end` on the same polygon when one end must be retracted to clear a spacing rule while the other must be extended to maintain enclosure or increase parallel run length.

## M2.S.7: Parallel Run Length Requirement

M2.S.7 forbids co-location of an 18 nm tip-to-tip gap with a side-to-side spacing <= 32 nm and requires parallel run length >= 35 nm when side spacing is at or below 32 nm. `resize_end end=high` operations that extend M2 polygons along the run direction increase parallel run length. Trial:i01.ug.Block7_union_row14.04 extends p3200 by +72 dbu end=high, p3215 by +56 dbu end=high, and p3539 by +16 dbu end=high. Trial:i01.ug.Block7_union_row24.14 extends p3058 by +136 dbu end=high, p3635 by +120 dbu end=high, and p3564 by +128 dbu end=high. Parallel run length must reach the 35 nm minimum when side spacing is at or below 32 nm; use `resize_end end=high` to add run length without shifting the polygon's anchor end.

## V1 Co-Movement with M2

V1 appears in `touched_layers` alongside M2 in 25 of the 27 trials. V1.M2.EN.2 requires M2 to enclose V1 by >= 5 nm on two opposite sides, and V1.M2.AUX.2 requires V1 width to match M2 width perpendicular to M2 length. Move M2-bearing instances together with their enclosed V1 contents; all trials where M2 was moved also list V1 in `touched_layers` (e.g., trial:i01.ug.Block7_union_row9.21, trial:i01.ug.Block7_union_row6.18, trial:i01.ug.Block7_union_row15.05). Failing to co-move V1 with M2 creates V1.M2.EN.2 or V1.M2.AUX.2 violations at the same step.

## add_polygon as a Repair Primitive

Trial:i01.ug.Block7_union_row20.10 uses `add_polygon` on M2 to insert a rectangle with corners at [[5992,22824],[5992,22896],[6048,22896],[6048,22824]], forming a shape 56 dbu wide and 72 dbu tall, paired with a single `move_instance` of [-36,0] on i0753. The repair was gated_in with `n_new_in_crop=0`. Insert a small M2 patch only when a connectivity gap cannot be closed by instance moves or polygon resizing alone; the patch must satisfy M2.W.1, M2.A.1, and all spacing rules at its perimeter.

## M3/V2 Involvement on Y-Axis Repairs

Two trials touch M3 and V2 in addition to M2, M1, and V1: trial:i01.ug.Block7_union_row16.06 (y-direction moves of [0,-12] on instances i0336 and i0308, plus `op=move axis=y` on polygon p3516) and trial:i01.ug.leaf_0095.26 (y-direction moves of [0,48] on instances i0177 and i0184, with `resize_end axis=y end=high` of +68 dbu on p2432 and +48 dbu on p3537). When an M2 repair requires y-axis displacement, upper metal (M3) and upper via (V2) shapes are also displaced and must be included in `touched_layers`. All x-only repairs in this iteration involve only M1, M2, and V1.