## Repair Behavior Observed (iteration 2)

### General

Only one trial is recorded for V3 in iteration 2: trial:i02.ug.whole_design.00. All prescriptive guidance below is grounded exclusively in that record.

### Trial i02.ug.whole_design.00 — accepted, connectivity preserved

The trial was accepted (decision: `gated_in`, `conn_preserved: true`) and touched layers M1, M2, M3, M4, M5, V1, V2, V3, V4. The repair applied 45 operations consisting of instance moves and polygon-level move/resize_end actions. The dominant translation was +32 dbu in x for the bulk of V3 instances and their associated polygons (trial:i02.ug.whole_design.00). Several polygons also received resize_end extensions on their high-x edge (by 32, 80, or 116 dbu) in the same pass (trial:i02.ug.whole_design.00).

### Multi-layer co-movement is required for V3 repairs

Because V3.M3.EN.1, V3.M4.EN.2, V3.AUX.1, and V3.M4.AUX.2 together constrain V3 to be fully enclosed by both M3 and M4, any positional adjustment to a V3 shape must be accompanied by corresponding adjustments to the enclosing M3 and M4 geometries. The accepted trial moved V3 as part of a coordinated operation spanning M1–M5 and V1–V4 (trial:i02.ug.whole_design.00). Do not move V3 in isolation without co-moving the enclosing metal layers.

### V3.W.1 — minimum width 18 nm along M4 length

The resize_end operations in the accepted trial extended polygon high-x ends (trial:i02.ug.whole_design.00), consistent with recovering width along the M4 direction after a positional shift. When a translation reduces the overlap between a V3 shape and its M4 parent in the length direction, apply a compensating resize_end on the trailing edge rather than leaving the width violation uncorrected.

### V3.M4.AUX.2 — V3 must exactly match M4 width perpendicular to M4 length

V3.M4.AUX.2 requires that V3 is exactly as wide as M4 in the direction perpendicular to M4's length (i.e., the short dimension of M4). The repair in trial:i02.ug.whole_design.00 included y-axis moves alongside x-axis moves for groups of instances (e.g., [32, -48], [32, -96], [32, 48], [32, 72], [32, -72]), indicating that y-offsets were used to realign V3 shapes to their M4 track rather than resizing them transversely. Do not resize V3 in the direction perpendicular to M4 length; use move operations to restore the correct centering instead (trial:i02.ug.whole_design.00).

### V3.AUX.1 — V3 must be inside both M3 and M4

The simultaneous adjustment of both M3 and M4 metal layers in trial:i02.ug.whole_design.00 confirms that achieving V3.AUX.1 compliance after a V3 displacement requires that both bounding metals be repositioned or resized so their overlap region continues to fully contain V3. A repair that moves only M4 or only M3 risks introducing a V3.AUX.1 violation on the other side.

### V3.M3.EN.1 — 5 nm enclosure on at least two opposite sides by M3

The rule requires that M3 encloses V3 by at least 5 nm on either the left+right pair or the top+bottom pair. In the accepted trial, x-axis polygon resize_end operations on what are consistent with M3 shapes accompanied the V3 translations (trial:i02.ug.whole_design.00). When a V3 shape shifts in x, extend the downstream M3 edge (resize_end on the high-x or low-x end as appropriate) to maintain the 5 nm enclosure margin rather than allowing M3 to underrun V3 on one side.

### V3.M4.EN.2 — 11 nm enclosure on at least two opposite sides by M4

The larger extension deltas observed in trial:i02.ug.whole_design.00 (resize_end values of 80 dbu and 116 dbu on polygons p1036 and p1065) are consistent with recovering the 11 nm M4 enclosure margin after a lateral shift. Apply larger x-end extensions to M4 than to M3 when the end-cap must clear 11 nm on both sides following a +x translation (trial:i02.ug.whole_design.00).

### V3.S.1, V3.S.2, V3.S.3, V3.S.4 — spacing rules

The trial moved multiple V3 instances by identical deltas grouped by y-offset class (trial:i02.ug.whole_design.00). Moving a complete y-offset group together preserves inter-via spacing within that group. The y-offset values used (-96, -72, -48, 0, +48, +72 dbu alongside +32 dbu x translation) suggest the repair redistributed V3 placements to clear spacing violations while keeping each V3 on its M4 track. Do not translate individual V3 instances independently when a spacing violation spans a group; move the entire same-track or same-y-offset group by the same delta so relative spacings within the group are unchanged (trial:i02.ug.whole_design.00).

### NONORTHOGONAL constraint

All polygon operations in trial:i02.ug.whole_design.00 were axis-aligned (move with axis x or y, and resize_end on axis x). No diagonal edges were introduced and the trial was accepted. Apply only axis-aligned move and resize operations to V3 shapes; never introduce oblique edges (trial:i02.ug.whole_design.00).