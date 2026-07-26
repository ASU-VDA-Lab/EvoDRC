## Repair Strategy: Combined Instance-Move and Polygon Resize in X

The single measured operation sequence in trial:i02.ug.whole_design.00 demonstrates that M1 DRC violations across a whole-design crop can be resolved without introducing new violations (n_new_in_crop=0, n_new_out_of_crop=0) by combining coordinated instance moves with x-axis resize_end operations on individual M1 polygons. All instance moves in that trial carried delta_dbu=[32,0] along x (or [72,0] for two instances), while the corresponding polygon resize_end operations extended the high x-end by matching or larger amounts (32, 80, or 116 dbu). This co-movement pattern preserved connectivity (conn_preserved=true) and was accepted (decision=gated_in) in trial:i02.ug.whole_design.00.

## X-End Extension Amounts Are Not Uniform

In trial:i02.ug.whole_design.00, most M1 polygon resize_end(axis=x, end=high) operations used delta_dbu=32, matching the instance translation. Two polygons (p1065 and p1036) required larger extensions of 116 and 80 dbu respectively, paired with instance moves of 72 dbu. This indicates that where local M1 geometry demands extra enclosure margin or spacing clearance, the resize_end delta must exceed the instance translation delta. Do not assume uniform 32-dbu extension is sufficient for all M1 polygons; where an instance moves by 72 dbu, the associated M1 polygon may need up to 116 dbu of high-end x extension (trial:i02.ug.whole_design.00).

## Y-Axis Repositioning Combined with X-End Extension

Polygons p958 through p965 in trial:i02.ug.whole_design.00 each received a y-axis move (ranging from -96 to +72 dbu) immediately before a resize_end(axis=x, end=high, delta=32). This combined move-then-extend pattern produced zero new violations, confirming that repositioning an M1 polygon vertically while simultaneously extending its x-high end is a viable repair primitive when connectivity is preserved. Apply y-move before x-resize_end to avoid intermediate states that could transiently violate M1.S.1 or M1.S.2 spacing rules (trial:i02.ug.whole_design.00).

## Enclosure Rules Drive Extension Direction

V0.M1.EN.1 requires M1 to enclose V0 by at least 5 nm on two opposite sides (or 5 nm and 0 nm). V1.M1.EN.1 requires M1 to enclose V1 by 5 nm on one side and 2 nm on the other. In trial:i02.ug.whole_design.00, all resize_end operations targeted the x-high end only, leaving the x-low end of each polygon unchanged. This asymmetric extension is consistent with repairing enclosure violations on one side without reducing enclosure on the opposite side. Never shrink the low end of an M1 polygon when the high-end extension is the only operation needed to meet enclosure (trial:i02.ug.whole_design.00).

## V0.M1.AUX.3 Constrains Width-Matched Edges

V0.M1.AUX.3 requires V0 to exactly match M1 width in the direction perpendicular to M1 length. No AUX.3 violations were introduced in trial:i02.ug.whole_design.00, which is consistent with the repair sequence leaving perpendicular (y-axis) M1 edges unchanged on polygons that moved only in x. When moving M1 polygons only along x, the y-extent of the polygon is unaffected, preserving the width-match condition. Avoid any operation that independently modifies a single y-edge of an M1 polygon that encloses a V0, as this would break the width-match (trial:i02.ug.whole_design.00).

## Minimum Width, Spacing, and Area Must Be Checked After Extension

M1.W.1 (minimum width 18 nm), M1.S.1 (side-to-side spacing 18 nm when both edges >36 nm), M1.S.2 (tip-to-side 25 nm), M1.S.3 (tip-to-tip 27 nm for 24-36 nm tips), and M1.A.1 (minimum area 504 nm²) are all metric constraints that can be violated by resize operations. In trial:i02.ug.whole_design.00, n_new_in_crop=0 confirms that extending the high x-end by 32-116 dbu did not create any new width, spacing, or area violations in that context. However, this result is specific to the geometry of that crop; do not assume that any positive x-high extension is universally safe — verify spacing to neighbors in x after each resize_end operation (trial:i02.ug.whole_design.00).

## NONORTHOGONAL Constraint Is Absolute

The NONORTHOGONAL rule applies to M1 and prohibits any edge with an angle other than 0 or 90 degrees. All operations in trial:i02.ug.whole_design.00 are axis-aligned moves and resize_end operations, and no nonorthogonal edges were introduced (n_new_in_crop=0). Always use axis-aligned ops (move in x or y, resize_end on x-high or x-low or y-high or y-low) for M1; never introduce diagonal edges (trial:i02.ug.whole_design.00).

## M1.R.0 Redundant Island Risk After Instance Isolation

M1.R.0 flags an M1 polygon that encloses exactly one small V0 via when it sits near a large empty M1 region. In trial:i02.ug.whole_design.00, the repair translated multiple instances and extended multiple M1 polygons together as a coordinated group, keeping each M1 island interacting with its full set of vias. Avoid operations that leave a single-V0 M1 island isolated by moving nearby M1 geometry away without moving the island itself (trial:i02.ug.whole_design.00).