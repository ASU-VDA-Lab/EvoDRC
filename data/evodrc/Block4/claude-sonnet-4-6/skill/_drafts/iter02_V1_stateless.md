## Repair Strategy: Instance Moves and M2 Geometry Adjustments

All twelve recorded trials were accepted (decision: gated_in, conn_preserved: true), providing a complete positive sample of repair patterns that satisfy the V1 DRC rule set. Every operation sequence was accepted; none were rejected. The sole exception regarding new violation count is trial:i02.ug.leaf_0003.02, which introduced 2 new in-crop violations but was still gated_in because connectivity was preserved—establishing that conn_preserved takes priority over a nonzero n_new_in_crop count.

### X-Axis-Only Movement Is the Universal Action Primitive

Every move_instance operation in the history has a Y-delta of zero: deltas take the form [dx, 0] exclusively. Trials i01.ug.leaf_0008.08, i01.ug.leaf_0020.09, i01.ug.leaf_0021.10, i02.ug.leaf_0001.00 each resolved their V1 violations with a single move_instance along X. This confirms that V1 violations in this design arise from X-axis mis-alignment between instances and their landing M1/M2 geometry, not from Y-axis offsets.

### Opposite-Direction Moves Resolve Spacing Violations (V1.S.1 Family)

When two via instances crowd each other along a shared M2 track, moving one in +x and the other in -x opens the required spacing. Trial:i01.ug.Block4_union_row3.03 moved i0170 by −36 dbu and i0292 by +36 dbu simultaneously. Trial:i01.ug.Block4_union_row10.01 moved i0025 by +108 dbu and i0041 by −108 dbu—a symmetric spread equal to the V1.S.1 aligned-track minimum (108 dbu corresponds to 27 nm at 4 dbu/nm). These opposing-delta pairs satisfy V1.S.1's projected spacing constraints without altering net positions of the connected M2 tracks.

### M2 Polygon End-Extension Accompanies Instance Moves When Enclosure Is Marginal

When a move_instance alone would leave insufficient M2 enclosure of V1 (V1.M2.EN.2), the repair extends the relevant M2 polygon end (resize_end, axis: x, end: high or low) by the corresponding shortfall. This pattern appeared in trial:i01.ug.Block4_union_row2.02 (resize_end high on p1548 +56 dbu alongside +36 dbu move), trial:i01.ug.Block4_union_row5.04 (resize_end high on p1608 and p1593 both +120 dbu alongside +64 dbu moves), trial:i01.ug.Block4_union_row7.06 (resize_end high on p1595 +164 dbu, p1577 +92 dbu, p1556 +56 dbu, p1395 +172 dbu alongside instance moves), and trial:i01.ug.Block4_union_row10.01 (resize_end high and low across multiple polygons). In every case the resize_end delta is larger than the instance move delta, compensating for the net change in via position relative to the M2 edge.

### New M2 Polygons Added When No Existing Segment Provides Enclosure

Trial:i01.ug.Block4_union_row1.00 added two entirely new M2 polygons alongside instance moves, rather than extending existing ones. The added segments each measured 192 × 72 dbu in footprint (48 nm × 18 nm at 4 dbu/nm); the 72 dbu height matches the V1.W.1 minimum width of 18 nm exactly, confirming these segments were placed to provide full M2 enclosure for via instances whose original M2 coverage was absent or insufficient for V1.M2.EN.2.

### Grouped Resize-and-Move Operations Maintain Layout Consistency

Trial:i02.ug.leaf_0003.02 applied a resize_end and a move_instance both tagged group: group_D, binding the polygon endpoint and the instance together into a single atomic step. This ensures that M2 geometry and the V1 position remain coincident after adjustment, which is required by V1.M2.AUX.2 (V1 width must match M2 width along the perpendicular direction). Using matched group tags for co-moving polygon endpoints and via instances prevents the M2 edge from separating from the via footprint.

### Repairs Span Multiple Touched Layers but V1 Geometry Itself Is Never Directly Edited

Across all twelve trials, the touched_layers field always includes M1, M2, and V1; five trials also touch M4, and one touches M3 and V2. Despite V1 appearing in touched_layers in every trial, no operation targets V1 directly—there are no add_polygon, resize_end, or move_instance ops labeled with layer_name V1. V1 geometry is changed only as a side effect of moving the cell instances (i0xxx) that contain the via, not by editing the via polygon in isolation. This means V1.W.1 compliance (minimum 18 nm width) and V1.M2.AUX.2 compliance (V1 width equals M2 width perpendicularly) are controlled through instance placement and M2 shaping, not through direct V1 polygon edits.

### M1 Enclosure Is Satisfied Implicitly via Instance Moves

V1.M1.EN.1 requires M1 to enclose V1 by at least 5 nm on one axis and 2 nm on the orthogonal axis. Because via instances carry M1 geometry as part of the cell, every move_instance that repositions a via also repositions the accompanying M1 landing pad. All twelve trials were accepted with conn_preserved, indicating the instance moves kept V1 within the repositioned M1 boundary without requiring any standalone M1 polygon edits. Explicit M1 resize_end operations do not appear in any trial.

### V1.AUX.1 Compliance Is Maintained by Keeping Moves Within M1∩M2 Overlap Zones

V1.AUX.1 requires V1 to lie inside both M1 and M2. Every accepted trial achieved this by ensuring that instance moves and M2 extensions were coordinated: the via lands inside the moved M1 cell, and M2 either already covered the new via position or was extended/added to cover it. No trial accepted a configuration where the via footprint fell outside either metal layer.

### Iteration-2 Repairs Are Smaller in Scope

The two iteration-2 trials (i02.ug.leaf_0001.00, i02.ug.leaf_0003.02) each operate on a single leaf unit with 1–3 ops, compared to iteration-1 trials that ranged from 1–8 ops across larger row-level units. The iteration-2 design state (d63aa666...) differs from iteration-1 (d279330...), indicating that iteration-1 repairs changed the design and left only residual localized violations for iteration 2 to address.