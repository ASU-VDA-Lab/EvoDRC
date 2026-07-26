## Observed Repair Patterns

### X-Axis Resize as the Primary M4 Operation

All accepted trials that targeted M4-specific violations used `resize_end` operations on the horizontal (x) axis, expanding polygon endpoints at either the `high` or `low` end. No y-axis `resize_end` operations on M4 polygons appear in the accepted history. Applied deltas ranged from 56 to 172 dbu within a single trial: trial:i01.ug.Block4_union_row10.01 applied four separate x-axis `resize_end` ops (p1551 +128 high, p1589 +72 low, p1605 +92 high, p1379 +64 low) and was accepted with no new violations; trial:i01.ug.Block4_union_row7.06 applied four expansions of 56–172 dbu, all at the `high` end (p1395 +172, p1595 +164, p1577 +92, p1556 +56), also accepted with no new violations; trial:i01.ug.leaf_0001.07 applied a single +96 dbu expansion at the `high` end of p1374 and was accepted.

Both the `high` and `low` ends of distinct M4 polygons may need adjustment in the same trial. Expanding only one end per polygon is valid when the opposing end is already compliant (trial:i01.ug.leaf_0001.07). Applying fixes to multiple polygons in one pass is consistent with accepted outcomes (trial:i01.ug.Block4_union_row10.01, trial:i01.ug.Block4_union_row7.06).

### M4.W.5 and M4.S.2 Interaction During Horizontal Resizes

Rule M4.W.5 requires a minimum horizontal width of 44 nm; rule M4.S.2 requires a minimum horizontal spacing of 40 nm between any two M4 vertical edges. When a `resize_end` expansion at the `high` end of one polygon brings it closer to the next polygon on the right, the expansion delta must not reduce the inter-polygon gap below 40 nm. The accepted expansions in trial:i01.ug.Block4_union_row7.06 (deltas 56–172 dbu across four polygons) and trial:i01.ug.Block4_union_row10.01 (deltas 64–128 dbu across four polygons) satisfied both constraints simultaneously, confirming that both rules must be checked together before committing any x-axis delta.

### Y-Axis Move Increments Must Be Multiples of 24 dbu

Rule M4.AUX.1 requires M4 horizontal edges to lie on a 24 nm grid. In trial:i04.ug.leaf_0002.01 the accepted instance moves that displaced M4 geometry used y-deltas exclusively in the set {0, +24, −24, +72} dbu, all of which are integer multiples of 24. This trial was gated in (two new in-crop violations were tolerated because connectivity was preserved). Use only y-deltas that are multiples of 24 dbu when moving instances or polygons that carry M4 geometry, to preserve M4.AUX.1 compliance.

### M4.AUX.2 Centerline Constraint for Minimum-Width Tracks

Rule M4.AUX.2 requires that minimum-width M4 tracks (vertical extent ≤ 24 nm) have their y-centerlines on the grid 192n+48 dbu (base filter: polygons whose top and bottom y-coordinates are both multiples of 96 dbu). The y-delta increments of ±24 and +72 used in trial:i04.ug.leaf_0002.01 are consistent with shifting a track from one valid centerline position to another on this 192 dbu pitch grid (e.g., from centerline 48 to 72 is a +24 shift; from 48 to 120 is a +72 shift). Verify that after any y-shift the new centerline satisfies (centerline − 48) % 192 == 0 before accepting the move for minimum-width M4 tracks.

### M4.AUX.3: No Bending

Rule M4.AUX.3 prohibits any M4 polygon from having a corner with an interior angle other than 90°, i.e., M4 polygons must remain rectilinear and non-branching. All accepted x-axis `resize_end` operations in the history modified only one edge endpoint per operation, leaving the other three edges of each rectangular M4 bar unchanged (trial:i01.ug.Block4_union_row10.01, trial:i01.ug.Block4_union_row7.06, trial:i01.ug.leaf_0001.07). Resize operations that would introduce a notch or step in the polygon boundary are prohibited by M4.AUX.3.

### Via Cell Resizes Can Increase M4-Region Violations

Trial:i01.cu.def:VIA_VIA34_1_2_58_52.01 targeted the `VIA_VIA34_1_2_58_52` via cell by shrinking its M3 shape (−64 dbu y) and two V3 shapes (−24 dbu y each). The trial was rejected because it increased the total violation count by 34: leaf unit `leaf_0025` went from 88 to 112 violations and `leaf_0026` from 35 to 45. M4 geometry is downstream of V3/M4 enclosure rules (V3.M4.EN.2, V3.M4.AUX.2). Shrinking V3 vertically can violate V3.M4.EN.2 (minimum 11 nm enclosure on two opposite sides) or V3.M4.AUX.2 (V3 must match M4 width perpendicularly). Do not reduce via cell V3 or M3 shape dimensions when doing so propagates new violations into adjacent leaf units; a net-positive delta across any window causes rejection regardless of whether the via itself is locally improved.

### V3-to-M4 Enclosure Rules

Rule V3.M4.EN.2 requires V3 to be enclosed by M4 by at least 11 nm on at least two opposite sides. Rule V3.M4.AUX.2 requires V3 to be exactly as wide as M4 in the direction perpendicular to M4's length. These rules interact with x-axis M4 resizes: expanding the `high` or `low` end of an M4 polygon extends M4 past the V3 footprint in the horizontal direction, satisfying the enclosure rule on the expanded end. The accepted expansions in trial:i01.ug.Block4_union_row10.01 and trial:i01.ug.Block4_union_row7.06 demonstrate that x-axis M4 expansion is the repair mechanism for V3.M4.EN.2 violations on the horizontal axis without disturbing V3.M4.AUX.2 (the perpendicular, vertical dimension is unchanged).

Rule V4.M4.EN.1 imposes the same 11 nm two-side enclosure for V4 by M4. While no V4-specific repair trial appears in the history, the enclosure geometry is symmetric to V3.M4.EN.2 and the same x-axis `resize_end` approach applies.

### M4.W.3 and M4.W.4: Forbidden Vertical Widths

Rule M4.W.3 forbids M4 vertical widths that are even multiples of 24 nm (48, 96, 144, 192, 240, 288, 336, 384, 432, 480 nm). Rule M4.W.4 additionally forbids widths 72, 168, 264, 360, and 456 nm. All accepted trials that adjusted M4 geometry did so via x-axis (horizontal) resizes, leaving the vertical (y) extent of each M4 polygon unchanged (trial:i01.ug.Block4_union_row10.01, trial:i01.ug.Block4_union_row7.06, trial:i01.ug.leaf_0001.07). Only the y-displacement moves in trial:i04.ug.leaf_0002.01 shifted M4 vertically, but these were rigid moves of the whole instance, not resizes, so the vertical width of each polygon was preserved. Do not change the vertical extent (y size) of M4 polygons during horizontal-axis repairs; any operation that does alter vertical extent must produce a width outside the M4.W.3 and M4.W.4 forbidden sets.

### M4.S.1, M4.S.3, M4.S.4, M4.S.5: Vertical and Tip-to-Tip Spacing

Rule M4.S.1 requires ≥ 24 nm vertical spacing between M4 polygon edges. Rules M4.S.3 and M4.S.4 each require ≥ 40 nm tip-to-tip spacing between M4 polygons on adjacent tracks (distinguished by whether a parallel run length exists). Rule M4.S.5 requires a parallel run length of ≥ 44 nm between adjacent-track M4 polygons. The accepted history shows no y-axis M4 resize operations; all vertical-geometry concerns are managed by choosing x-axis deltas that do not create new tip-to-tip proximity (trial:i01.ug.Block4_union_row7.06 applied four simultaneous expansions in the same y-band without triggering new violations). When expanding multiple M4 polygons in one trial, verify that each expansion does not extend a polygon end to within 40 nm of an adjacent polygon end on the same track pair (M4.S.3/M4.S.4) and that any newly created parallel facing length satisfies M4.S.5's 44 nm minimum.

### M4.AUX.4: Wide M4 Outer Edge Constraint

Rule M4.AUX.4 prohibits the outer (horizontal) edge of a wide M4 polygon from touching a routing track edge. Wide M4 polygons are those not classified as minimum-width (vertical extent > 24 nm after accounting for the 13 nm sizing margin in the rule). All accepted M4 operations in the history operated on minimum-width track geometries (single `resize_end` or rigid instance moves), avoiding wide M4 shape modification. When a wide M4 polygon must be adjusted, its top and bottom edges must not be repositioned to a y-coordinate that coincides with a minimum-width track's top or bottom edge.