## M6 Grid and Width Constraints

M6 horizontal edges must lie on a 32 nm vertical grid (M6.AUX.1). All y-axis resize deltas in trial:i01.ug.leaf_0020.09 that produced accepted results used values (96, 32, 16, 112 dbu) chosen such that the resulting edge coordinate lands on the 32 nm grid; each delta must be selected with the current edge position in mind, not simply rounded to 32 nm independently.

Minimum-width (1x) M6 tracks must have their centerlines on a grid of pitch 256 nm with offset 64 nm from the origin (M6.AUX.2). The y-axis resize operations on p2107 and p2106 in trial:i01.ug.leaf_0020.09 moved ends by differing amounts (low end -96, high end +32 for p2107; low end -16, high end +112 for p2106), reflecting the need to satisfy both AUX.1 edge placement and AUX.2 centerline alignment simultaneously rather than applying a single uniform delta.

Minimum vertical width is 32 nm (M6.W.1) and minimum horizontal width is 44 nm (M6.W.5). Vertical widths that are even integer multiples of 32 nm (64, 128, 192, 256, 320, 384, 448, 512, 576, 640 nm) are prohibited by M6.W.3, and widths 96, 224, 352, 480, 608 nm are prohibited by M6.W.4. These constraints eliminate a large fraction of seemingly valid widths; when resizing M6 vertically, verify that the resulting height is not in either prohibited set.

## M6 Spacing Constraints

Minimum vertical spacing between M6 polygon edges is 32 nm (M6.S.1). Minimum horizontal spacing is 40 nm (M6.S.2). Tip-to-tip spacing on adjacent tracks—both for polygons that do not share a parallel run length (M6.S.3) and those that do (M6.S.4)—is also 40 nm. Minimum parallel run length between M6 polygons on adjacent tracks is 44 nm (M6.S.5). When moving M6 polygons horizontally, the 40 nm spacing constraint (M6.S.2) and the 44 nm width constraint (M6.W.5) jointly govern the minimum step; the x-axis moves of +32 and -16 dbu observed in trial:i03.ug.leaf_0003.02 and trial:i04.cu.def:VIA_VIA56_2_2_66_58.00 were non-uniform across neighboring polygons and were chosen to open or maintain these clearances, not to apply a single uniform shift.

## M6 Shape Constraints

M6 polygons must be rectilinear (M6.AUX.3). No 0–90 degree corner vertices are permitted; all polygon geometry must be purely orthogonal. No bends of any kind are introduced by any operation in the recorded history.

Wide M6 polygons (those surviving a ±17 nm vertical erosion) must not have their horizontal outer edges coincide with routing track centerlines (M6.AUX.4). When moving M6 y-coordinates, verify that the resulting horizontal edges of any wide shape do not land on a track edge as defined by the 1x routing grid.

## V5–M6 Enclosure and Width Matching

V5 vias must be enclosed by M6 by at least 11 nm on two opposite sides (V5.M6.EN.2). V5 must also match the M6 width exactly in the direction perpendicular to the M6 length (V5.M6.AUX.2). In trial:i01.cu.def:VIA_VIA56_2_2_66_58.02, the repair applied to cell VIA_VIA56_2_2_66_58 moved all four V5 via shapes symmetrically along the x-axis (shapes 0 and 2 by -116 dbu, shapes 1 and 3 by +116 dbu) and then resized all four by +320 dbu along the x-axis. The symmetric move repositions each via shape laterally under the M6 track while the resize extends the V5 shape to span the full M6 width and satisfy both EN.2 and AUX.2.

In trial:i04.cu.def:VIA_VIA56_2_2_66_58.00, the same cell was modified again along the y-axis: shapes 0 and 1 moved -132 dbu, shapes 2 and 3 moved +132 dbu, and all four were resized by +512 dbu along y. This followed prior M6 polygon moves (p2109 by -64 y and p2108 by -112 y) within the same operation group, confirming that via shape adjustments must track the actual positions of the M6 polygons after those polygons are repositioned. The y-axis V5 resize (+512 dbu) was larger than the earlier x-axis resize (+320 dbu) in iter 1, reflecting the greater displacement required after the M6 polygons themselves shifted vertically. Applying the combined operation reduced the violation count from 70 to 56 in leaf_0002 (trial:i04.cu.def:VIA_VIA56_2_2_66_58.00).

When repairing V5.M6.EN.2 or V5.M6.AUX.2 violations in a shared via cell definition, the fix propagates to every instance of that cell across units; trial:i04.cu.def:VIA_VIA56_2_2_66_58.00 recorded no change in leaf_0003 (delta 0) while leaf_0002 improved, showing that cell-level fixes do not uniformly benefit all units but do affect all placements.

## V6–M6 Enclosure

V6 must be enclosed by M6 on at least two opposite sides by 11 nm (V6.M6.EN.1). No V6 enclosure violations appear in the recorded trial operations; all recorded V5 enclosure fixes were sufficient to address the history presented. The rule structure mirrors V5.M6.EN.2 and the same two-opposite-sides logic applies.

## Multi-Layer Coupling of M6 Moves

Every x-axis M6 polygon move in the history was accompanied by coordinated moves of instances on multiple layers (M4, M5, V4, V5) within the same operation group. In trial:i03.ug.leaf_0003.02, moving p1683 by +32 x and p1682 by -16 x required moving eight and eight instances respectively on those other layers. In trial:i04.cu.def:VIA_VIA56_2_2_66_58.00, the corresponding M6 x-moves (+32 for p1685, -16 for p1684) similarly required fourteen co-moved instances. Isolated M6 polygon moves that leave companion vias and lower-metal shapes unshifted will break connectivity and introduce new enclosure violations on other layers.

## Via Cell Repair Ordering Within a Group

In trial:i04.cu.def:VIA_VIA56_2_2_66_58.00, M6 polygon moves (x and y) were grouped together with V5 via shape moves and resizes under a single operation group ("g1"). The V5 adjustments used position deltas (±132 y) that are consistent with the M6 polygon displacements (-64 y for p2109, -112 y for p2108) applied in the same group. Via shape moves must reflect the post-move M6 coordinates, not the pre-move coordinates; grouping all operations in a single committed set is the observed pattern for maintaining correctness.

## Observed Move Quantization

All M6 and companion instance x-axis moves in the history are multiples of 16 dbu: +32 and -16 appear in trial:i03.ug.leaf_0003.02 and trial:i04.cu.def:VIA_VIA56_2_2_66_58.00. M6 y-axis end resizes in trial:i01.ug.leaf_0020.09 use values 96, 32, 16, and 112 dbu, the smallest being 16 dbu. M6 y-axis polygon moves in trial:i04.cu.def:VIA_VIA56_2_2_66_58.00 are -64 and -112 dbu. These values satisfy M6.AUX.1 (final horizontal edge positions on 32 nm grid) given the starting positions of the polygons involved; the repair planner must verify that starting coordinate plus delta lands on grid before committing any y-axis operation.