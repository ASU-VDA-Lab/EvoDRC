## Operation Patterns That Resolved M1 Violations

All three recorded M1 trials (trial:i02.ug.whole_design.00, trial:i03.ug.whole_design.00, trial:i04.ug.whole_design.00) reached a `gated_in` decision with `conn_preserved: true` and zero net new violations (`n_new_in_crop: 0`, `n_new_out_of_crop: 0`). Every trial's op list for M1 combines `move_instance` shifts in the positive-x direction with `resize_end` expansions on the x-axis high end of M1 polygons. No trial in the recorded history used any other repair strategy on M1.

## Pair Instance Moves with High-End Extension of M1 Polygons

Apply `resize_end` on the x-axis high end of affected M1 polygons whenever instances are moved in the positive-x direction. This pairing produced gated_in outcomes with zero new violations and preserved connectivity across all three recorded trials (trial:i02.ug.whole_design.00, trial:i03.ug.whole_design.00, trial:i04.ug.whole_design.00). Every success in the measured record follows this pattern.

## Resize Delta Can Exceed Instance Move Delta

Do not assume the polygon resize delta equals the instance move delta. In trial:i02.ug.whole_design.00, most instance moves used +32 dbu in x and most polygon resize_end operations also used +32 dbu, but polygon p1065 required +116 dbu and polygon p1036 required +80 dbu — both substantially larger than the nominal +32 dbu shift applied to the other polygons in that same trial. The measured record shows that some M1 polygons require extra extension beyond the base instance translation delta (trial:i02.ug.whole_design.00).

## Polygons That Required Multiple Rounds of Adjustment

Do not treat a single resize_end as necessarily final for a given M1 polygon. Polygon p1036 received a +80 dbu high-end resize in trial:i02.ug.whole_design.00 and an additional +84 dbu resize in trial:i03.ug.whole_design.00. Polygon p1065 received +116 dbu in trial:i02.ug.whole_design.00 and a further +72 dbu in trial:i04.ug.whole_design.00. Both polygons required successive adjustments across multiple iterations before the design stabilized, as shown by their recurrence across those trials.

## Uniform-Delta Strategy for Coordinated Shifts

Apply the same delta to all affected instances and all affected polygon high ends when the required x-direction adjustment is uniform across the group. In trial:i04.ug.whole_design.00, all 11 instance moves and all 11 polygon resize_end operations used exactly +72 dbu, and the result was zero new violations with connectivity fully preserved. The matched uniform delta is the recorded successful approach for that class of operation.

## Y-Axis Instance Adjustments Do Not Require M1 Polygon Y-Resizes

In trial:i02.ug.whole_design.00, instance y-offsets varied across -96, -72, -48, 0, +48, and +72 dbu within the same trial, while all M1 polygon resize_end operations in that trial applied only to the x-axis high end. No y-axis resize_end operations on M1 polygons appear in any trial in the recorded history (trial:i02.ug.whole_design.00, trial:i03.ug.whole_design.00, trial:i04.ug.whole_design.00). M1 polygon correction in the measured record is confined to x-axis high-end extension regardless of any y-axis instance repositioning.

## V1 and M2 Are Co-Affected by M1 Resize Operations

Trials that applied resize_end to M1 polygons also included V1 and M2 in their `touched_layers`. Trial:i03.ug.whole_design.00 and trial:i04.ug.whole_design.00 — both dominated by M1 polygon high-end resizes — listed M1, M2, and V1 as touched. Trial:i02.ug.whole_design.00, which included the largest set of M1 operations, additionally touched M3, M4, M5, V2, V3, and V4. V1.M1.EN.1 (minimum enclosure of V1 by M1 on two opposite sides is 5 nm and 2 nm) is an active constraint on this layer; the co-occurrence of V1 in the touched_layers of every M1-resize trial (trial:i03.ug.whole_design.00, trial:i04.ug.whole_design.00) indicates that M1 high-end extension directly affects V1 enclosure state.

## No Shrink Operations in Recorded History

Every resize_end operation in the recorded M1 history uses a positive delta value, expanding the high end of the polygon. No negative or zero resize_end operations on M1 polygons appear across trial:i02.ug.whole_design.00, trial:i03.ug.whole_design.00, or trial:i04.ug.whole_design.00. Avoid applying negative resize_end on M1 polygon high ends as a repair strategy; the measured record contains no successful instance of this approach for M1.