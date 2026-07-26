## Design-State Dependence of M1 Operations

The measured history spans three distinct design states (fa7319ee in iteration 1, cd809b6a in iteration 2, 382d59e7 in iteration 3). Operations that produced zero new in-crop violations in one design state produced ten new in-crop violations when applied in a later design state. Specifically, a move_instance of -36 dbu in x on instance i0099 in design_state 382d59e7 yielded n_new_in_crop=10 despite decision="gated_in" and conn_preserved=true (trial:i03.ug.leaf_0003.02). Do not treat the success of any M1-touching operation in a prior design state as evidence that the same operation magnitude is safe in the current design state.

## gated_in Does Not Imply Zero New DRC Violations

The decision field "gated_in" reflects only that connectivity was preserved; it does not certify that n_new_in_crop is zero. In trial:i03.ug.leaf_0003.02, both conn_preserved=true and decision="gated_in" coexist with n_new_in_crop=10. All ten new violations were introduced to M1 (and co-touched M2, V1). Treat any gated_in trial at iteration 3 design state as a source of new violations that must be verified against all applicable M1 rules (M1.W.1, M1.S.1 through M1.S.6, M1.A.1, V0.M1.EN.1, V0.M1.AUX.3, V1.M1.EN.1, M1.R.0) before accepting the resulting state.

## x-Axis Move Operations on M1-Touching Instances

In iterations 1 and 2, x-moves of +36 dbu on M1-touching instances consistently produced zero new in-crop violations across all measured trials: trial:i01.ug.Block3_union_row2.01 (two instances moved +36 dbu), trial:i01.ug.Block3_union_row5.02 (three instances at +36 dbu), trial:i01.ug.leaf_0006.04 (two instances at +36 dbu), trial:i01.ug.leaf_0009.07 (one instance at +36 dbu), trial:i01.ug.leaf_0013.09 (one instance at -36 dbu). These results held under design_state fa7319ee. Under design_state 382d59e7, a move of -36 dbu introduced 10 new violations (trial:i03.ug.leaf_0003.02). Do not extrapolate zero-violation outcomes from fa7319ee to 382d59e7 for any M1-touching x-move.

## x-Axis resize_end (high end) Operations

Multiple iter-1 trials applied resize_end on the x-axis at the high end of M1 polygons. Delta magnitudes ranged from 56 dbu (trial:i01.ug.leaf_0007.05, polygons p1223 and p1189) to 192 dbu (trial:i01.ug.Block3_union_row1.00, polygons p1254 and p1270), with intermediate values of 92 dbu (trial:i01.ug.Block3_union_row8.03, polygon p1257; trial:i01.ug.leaf_0008.06, polygon p1261), 108 dbu (trial:i01.ug.leaf_0012.08, polygon p1256), 128 dbu (trial:i01.ug.Block3_union_row8.03, polygons p1266 and p1269; trial:i02.ug.leaf_0002.01, polygon p1226), and 164 dbu (trial:i01.ug.Block3_union_row8.03, polygon p1267). All produced zero new in-crop violations in design_state fa7319ee (iter 1) and design_state cd809b6a (iter 2 for trial:i02.ug.leaf_0002.01). These resize operations extend M1 in x, directly affecting M1.S.1 (side-to-side spacing), M1.S.2 (tip-to-side spacing), V0.M1.EN.1 (V0 enclosure), and V1.M1.EN.1 (V1 enclosure). No resize_end operations were measured in design_state 382d59e7; results from earlier states do not transfer.

## y-Axis resize_end on M1

One y-axis resize_end was measured: polygon p1159, high end, +20 dbu, in trial:i01.ug.leaf_0008.06 (design_state fa7319ee), zero new in-crop violations. This operation touches M1 height and is relevant to M1.W.1 (minimum width 18 nm) and V0.M1.EN.1 / V1.M1.EN.1 enclosure on the orthogonal axis. No y-axis resize was measured in design_states cd809b6a or 382d59e7.

## Combined move_instance + resize_end Patterns

Several trials paired a move_instance with a resize_end on the same crop region. In trial:i01.ug.Block3_union_row1.00, three instances were moved +136 dbu in x while three polygons were extended +192 dbu at their high-x end; zero new violations resulted (design_state fa7319ee). In trial:i01.ug.Block3_union_row8.03, four instances moved at +72 or +108 dbu while four polygons were extended at +92 to +164 dbu; zero new violations (fa7319ee). In trial:i02.ug.leaf_0002.01, one instance moved +104 dbu while one polygon extended +128 dbu; zero new violations (cd809b6a). The pattern of resizing M1 proportionally larger than the instance shift was used in all multi-op iter-1 and iter-2 trials without introducing violations. No combined-operation trial was measured in design_state 382d59e7.

## M1 Spacing Rules and Operation Risk

M1.S.1 (minimum 18 nm side-to-side, edges >36 nm) and M1.S.2 (minimum 25 nm tip-to-side) are the spacing rules most directly disturbed by x-axis moves and high-end resizes. The zero-violation outcomes in trials:i01.ug.Block3_union_row1.00, i01.ug.leaf_0007.05, i01.ug.leaf_0012.08, and i02.ug.leaf_0002.01 confirm that extending M1 polygons at their high-x end can be executed without triggering M1.S.1 or M1.S.2 violations, provided the design state is fa7319ee or cd809b6a. The 10 new violations in trial:i03.ug.leaf_0003.02 arose under design_state 382d59e7 from a single move with no accompanying resize; the specific rules fired are not broken out in the record, but any of M1.W.1, M1.S.1 through M1.S.6, V0.M1.EN.1, V0.M1.AUX.3, V1.M1.EN.1, or M1.A.1 may be responsible.

## V0 and V1 Enclosure Coupling to M1 Moves

All measured trials touched M1 together with V1 (and many with M2). This co-touch pattern is consistent with enclosure constraints V0.M1.EN.1 (5 nm on two opposite sides, or 5 & 0 nm) and V1.M1.EN.1 (5 nm and 2 nm on opposite sides). When an instance is moved in x without a paired M1 resize, the via's position relative to M1 shifts, directly risking these enclosure rules. The single-op move in trial:i03.ug.leaf_0003.02 (no resize, -36 dbu x) produced 10 new violations, which is consistent with enclosure violations introduced when M1 is not extended to track the via displacement. All zero-violation multi-op trials in design_state fa7319ee paired instance moves with proportional M1 high-end resizes (e.g., trial:i01.ug.Block3_union_row1.00, trial:i01.ug.Block3_union_row8.03, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0012.08).

## V0.M1.AUX.3 Width-Matching Constraint

V0.M1.AUX.3 requires that V0 exactly match M1 width along the direction perpendicular to M1 length. This constraint fires when V0 edges are not coincident with M1 edges. All measured trials with resize_end operations extended M1 at the high end only; no operation was observed to narrow M1 or shift its perpendicular edges. This is consistent with zero AUX.3 violations across all fa7319ee and cd809b6a trials (trial:i01.ug.Block3_union_row1.00 through trial:i02.ug.leaf_0002.01). Whether AUX.3 contributed to the 10 violations in trial:i03.ug.leaf_0003.02 is not determinable from the record.

## Iteration 3 State Summary

At iteration 3 (design_state 382d59e7), only one trial has been measured: trial:i03.ug.leaf_0003.02. That trial produced 10 new in-crop violations while still being accepted as gated_in. The M1 operations in this state carry demonstrated risk of introducing violations. Any further M1 operations in this design state must account for the existing 10 new in-crop violations already present and the demonstrated non-zero violation rate.