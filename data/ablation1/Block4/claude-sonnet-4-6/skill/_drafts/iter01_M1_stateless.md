## Repair Operation Inventory

All ten trials in the iteration-1 history were accepted (`decision: gated_in`) with connectivity preserved and zero net-new violations introduced inside or outside the crop window. The complete accepted operation set for M1 in this iteration comprises three primitives: `move_instance`, `move` (single-polygon translate), and `resize_end` (single-edge extension on one axis). No operation removed geometry, split polygons, or introduced new shapes. Every trial that touched M1 also touched at least M2 and V1 (trial:i01.ug.Block4_union_row1.00, trial:i01.ug.Block4_union_row6.05, trial:i01.ug.leaf_0020.09, and all others in the set), confirming that M1 repairs propagate connectivity obligations upward to V1 and M2; repairs that preserve `conn_preserved: true` must account for those coupled layers.

## Dominant Move Direction and Magnitude

Horizontal (X-axis) displacement is the sole axis used for instance moves in nine of ten trials. Only trial:i01.ug.leaf_0021.10 applied a non-zero Y component ([36, 44] dbu), and it was still accepted with zero new violations. Do not treat pure-X moves as insufficient when Y-axis enclosure also needs correction; trial:i01.ug.leaf_0021.10 demonstrates that combined X+Y moves clear DRC without introducing new violations.

The magnitude 36 dbu recurs as the dominant horizontal instance-move step across trial:i01.ug.Block4_union_row1.00, trial:i01.ug.Block4_union_row6.05, trial:i01.ug.leaf_0020.09, and trial:i01.ug.leaf_0008.08. Smaller steps (12 dbu in trial:i01.ug.Block4_union_row10.01, 28 dbu in trial:i01.ug.Block4_union_row7.06) and larger steps (108 dbu in trial:i01.ug.Block4_union_row2.02) also produced accepted outcomes. Use the minimum displacement that resolves the violation; both fine (12 dbu) and coarse (108 dbu) steps have been accepted without introducing new violations.

## Multi-Instance Coordinated Moves

Moving multiple instances simultaneously within a single crop window is an established accepted pattern. Trial:i01.ug.Block4_union_row5.04 moved four instances with a mix of positive and negative deltas ([37, 0], [37, 0], [-36, 0], [37, 0]) in one operation set and was accepted. Trial:i01.ug.Block4_union_row6.05 moved three instances all by [36, 0] and was accepted. Trial:i01.ug.Block4_union_row7.06 moved two instances and two polygons all by [-28, 0] in a single accepted batch. When M1 spacing violations arise between multiple neighbors, apply coordinated multi-instance moves that shift both sides of the spacing constraint rather than moving only one party; trial:i01.ug.Block4_union_row5.04 and trial:i01.ug.Block4_union_row7.06 confirm this produces zero new violations.

## Polygon-Level Move (Non-Instance)

Direct polygon moves (`op: move`) were applied in trial:i01.ug.Block4_union_row2.02 (polygon p1548, axis x, +16 dbu) and trial:i01.ug.Block4_union_row7.06 (polygons p1596 and p1477, axis x, -28 dbu each). In both accepted trials the polygon move delta matched or was consistent with the co-applied instance move deltas within the same repair batch (28 dbu in trial:i01.ug.Block4_union_row7.06). Apply polygon-level moves only when the move delta is consistent with the enclosing instance moves in the same batch; mismatched deltas risk breaking V0.M1.EN.1 or V0.M1.AUX.3 enclosure constraints, which require M1 edges to track V0 boundaries.

## M1 End Extension via resize_end

`resize_end` on the high-x end of M1 polygons was accepted in trial:i01.ug.leaf_0008.08 (polygon p1604, +92 dbu) and trial:i01.ug.Block4_union_row7.06 (polygon p1395, +172 dbu). Both extensions were on the `high` end of the x axis only; no low-end or y-axis resize appears in accepted history. Use `resize_end` to extend M1 length when enclosure of V0 or V1 is deficient on one side (rules V0.M1.EN.1 and V1.M1.EN.1 require 5 nm enclosure on two opposite sides); extending the high-x end of an M1 segment is a confirmed accepted repair path. Do not apply `resize_end` if it would reduce an M1 tip length below 36 nm and thereby change which M1.S spacing rule class applies, without verifying that the resulting tip-to-side or tip-to-tip spacing meets M1.S.2/M1.S.3/M1.S.4/M1.S.5 at the new geometry.

## V0.M1.EN.1 and V0.M1.AUX.3 Coupling

Every accepted trial in this history touches V1 and M2 alongside M1, and the repair operations include both instance moves and direct polygon moves that keep M1 edges aligned with via boundaries. V0.M1.AUX.3 requires V0 width to exactly match M1 width perpendicular to the M1 run direction; any M1 resize or move that changes the M1 edge position along the via-perpendicular axis violates AUX.3 unless the V0 boundary is co-moved. Trial:i01.ug.Block4_union_row7.06 demonstrates the accepted pattern: polygon moves on M1 shapes (p1596, p1477) are applied at the same delta as instance moves, keeping relative M1-to-via geometry intact. Do not resize M1 in the direction perpendicular to its run without also adjusting the associated V0 shape.

## V1.M1.EN.1 Enclosure

V1.M1.EN.1 requires M1 to enclose V1 by 5 nm on one opposite pair of sides and 2 nm on the other pair. All accepted trials that move instances containing V1 connections (trial:i01.ug.Block4_union_row1.00 through trial:i01.ug.leaf_0021.10) preserve `conn_preserved: true`, confirming that instance-level moves that shift the entire M1+V1 stack together do not violate V1.M1.EN.1 because the relative enclosure geometry is unchanged. Apply instance moves (rather than isolated polygon moves) when the goal is to relocate an M1 segment that encloses V1, to avoid introducing a V1.M1.EN.1 deficiency.

## M1.W.1 and M1.A.1 Width and Area Floors

M1.W.1 sets a minimum width of 18 nm and M1.A.1 sets a minimum area of 504 nm². The accepted `resize_end` extensions in trial:i01.ug.leaf_0008.08 (+92 dbu) and trial:i01.ug.Block4_union_row7.06 (+172 dbu) grow M1 area and cannot cause M1.W.1 or M1.A.1 violations by themselves. Instance moves and polygon translates do not change shape dimensions. None of the accepted operations in this history reduce M1 width or area. Do not use `resize_end` with a negative delta (shrink) on a short M1 segment without verifying the resulting area exceeds 504 nm² and width remains at or above 18 nm.

## M1.S Spacing Class Awareness

The M1.S rules split spacing requirements by edge length: side edges >36 nm require 18 nm spacing (M1.S.1); tip-to-side (one edge ≤36 nm, other >36 nm) requires 25 nm (M1.S.2); tip-to-tip both 24–36 nm requires 27 nm (M1.S.3); both <24 nm requires 31 nm (M1.S.4); mixed 24–36 nm and <24 nm requires 31 nm (M1.S.5); corner-to-corner requires 20 nm (M1.S.6). Instance moves in trial:i01.ug.Block4_union_row5.04 applied asymmetric deltas (three instances at +37 dbu, one at -36 dbu) to open spacing simultaneously from both sides of a constraint. When the required separation involves tip edges (M1.S.2 through M1.S.5), the required clearance is larger than the side-to-side minimum; coordinate move magnitudes accordingly. All accepted multi-instance move batches in this history produced zero new M1.S violations, confirming that bi-directional displacement is a valid strategy when a single-direction move would push one shape into a new conflict with a third neighbor.

## M1.R.0 Redundant Island Avoidance

M1.R.0 flags M1 islands that enclose exactly one small V0 via and sit near a large empty M1 region. None of the accepted trials in this history create isolated M1 islands; all operations move or extend existing connected M1 geometry. Do not use `resize_end` or `move` to detach an M1 segment from its neighbors if the detachment would leave it enclosing exactly one V0 in proximity to a large empty zone, as that geometry matches the M1.R.0 trigger condition.