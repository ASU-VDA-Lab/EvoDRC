## Repair Operations on M1 (Iteration 4 Summary)

### Dominant Repair: Instance Move in X at 36 dbu

The primary repair pattern across all recorded iterations is `move_instance` with `delta_dbu=[36,0]` (X-axis shift, 36 dbu). This step cleanly eliminates M1-touching violations without introducing new in-crop errors in the following units and rows: trial:i01.ug.Block2_union_row1.00, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0004.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0011.06, trial:i01.ug.leaf_0013.08, trial:i04.ug.leaf_0001.00. Apply 36-dbu X moves as the first-choice repair when spacing or enclosure violations affect M1 in block or leaf units.

A smaller X move of 12 dbu combined with an M1 polygon addition also produced zero new violations in the same iteration (trial:i01.ug.leaf_0001.03), and a move of 37 dbu was similarly clean (trial:i01.ug.leaf_0004.04). Do not treat 36 dbu as a hard snap requirement; the criterion is that the resulting M1 geometry satisfies M1.W.1 (≥18 nm width), M1.S.1/S.2/S.3/S.4/S.5/S.6 spacing rules, and V0.M1.EN.1/V1.M1.EN.1 enclosure rules after the move.

### M1 Polygon Addition: Use Only When Required for Connectivity

Trial trial:i01.ug.leaf_0001.03 added a rectangular M1 polygon at coordinates [5332,2340]–[5532,2448] (200×108 dbu) alongside a small instance move. That polygon was subsequently deleted in trial:i02.ug.leaf_0001.00 (the next iteration's repair of the same unit), which replaced the approach with a proper via insertion (`add_via VIA_VIA12` at [5472,2340]) and an M1 polygon-end resize (`resize_end` on p957, +172 dbu on the low X end). Do not retain ad-hoc add_polygon operations across iterations; the measured sequence shows the correct resolution is via placement with M1 end extension, not a free-standing added polygon.

When adding a via and extending an M1 polygon end, the resize_end at +172 dbu (low end) on the affected M1 shape was sufficient to satisfy V0.M1.EN.1 and V1.M1.EN.1 enclosure requirements with zero new violations (trial:i02.ug.leaf_0001.00). Extend the M1 polygon end by at least the enclosure margin (5 nm per V0.M1.EN.1 and V1.M1.EN.1) beyond the via edge.

### M1.A.1 Violations from Instance Moves

A `move_instance` that shifts M1 shapes can sever or reshape M1 polygons in ways that produce fragments below the 504 nm² minimum area (M1.A.1). Trial trial:i01.ug.leaf_0013.08 recorded `n_new_in_crop: 1` attributed to M1.A.1 after a 36-dbu X instance move; the trial was still accepted because `conn_preserved=true`. Do not rely on connectivity preservation to suppress M1.A.1 fragments indefinitely; the in-crop violation count accumulates. When a move produces an M1.A.1 hit, either merge the fragment into an adjacent M1 shape or delete it if it carries no via.

### Resize Operations on M1

A polygon resize of +184 dbu in X (trial:i01.ug.Block2_union_row1.00) produced zero new violations when applied to M1 polygon p1053 in the context of a multi-instance move. Resizes are clean provided the resulting polygon satisfies M1.W.1 (≥18 nm on all cross-sections) and does not close spacing to a neighboring M1 shape below M1.S.1 (18 nm side-to-side for edges >36 nm), M1.S.2 (25 nm tip-to-side), M1.S.3 (27 nm tip-to-tip, 24–36 nm edges), M1.S.4 (31 nm tip-to-tip, both <24 nm), M1.S.5 (31 nm mixed tip-to-tip), or M1.S.6 (20 nm corner-to-corner). No violations from resizes were recorded in the history.

### Via Enclosure: V0.M1.EN.1 and V1.M1.EN.1

Both enclosure rules require M1 to surround the via by 5 nm on at least two opposite sides (V0.M1.EN.1 allows 5 & 0 nm; V1.M1.EN.1 requires 5 & 2 nm). When a via is repositioned via `add_via`, extend the nearest M1 polygon end to restore enclosure before committing. Trial trial:i02.ug.leaf_0001.00 shows this pattern: `add_via VIA_VIA12` at [5472,2340] paired immediately with `resize_end` +172 dbu on the low end of p957, yielding zero enclosure violations.

V0.M1.AUX.3 requires that V0's width in the direction perpendicular to the M1 run matches M1's width exactly at that location. When resizing M1 in X, verify that any co-located V0 does not gain a non-coincident edge relative to the M1 boundary; the resize_end approach used in trial:i02.ug.leaf_0001.00 preserves this coincidence by extending only the end of M1, not its sides.

### M1.R.0 (Redundant Island Rule)

No M1.R.0 violations were recorded in any trial. The delete-and-replace sequence in trial:i02.ug.leaf_0001.00 (deleting ad-hoc polygon p1101 and migrating to a proper via) eliminated any M1 island that would have been flagged near a large empty M1 region. Do not leave isolated M1 polygons enclosing exactly one small V0 near large empty M1 regions; the measured correction is to delete the island and route connectivity through an adjacent properly-enclosed M1 wire.

### Non-Orthogonal Geometry

All recorded M1 operations (move_instance, resize, resize_end, add_polygon, delete) produced only rectilinear (0° and 90°) M1 edges. The NONORTHOGONAL block flags any M1 edge at 1–89° or 91–179°. All add_polygon and resize operations in the history used axis-aligned coordinates exclusively (trial:i01.ug.leaf_0001.03, trial:i01.ug.Block2_union_row1.00, trial:i02.ug.leaf_0001.00). Maintain this invariant: every new or modified M1 polygon must have edges only at 0° or 90°.

### Gating Behavior

Every trial in the history was accepted (`decision: gated_in`). The determining factor for acceptance was `conn_preserved: true`, not zero new violations — trial:i01.ug.leaf_0013.08 was accepted with one new M1.A.1 in-crop violation because connectivity was intact. The repair pipeline tolerates a small increase in in-crop M1.A.1 count when connectivity is the priority. However, no trial introduced any out-of-crop violations (all `n_new_out_of_crop: 0`), so do not push new violations across crop boundaries.