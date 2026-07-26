## Horizontal Width Rules

M5.W.1 sets a 24 nm minimum horizontal wire width. M5.W.2 caps the maximum horizontal width at 480 nm. M5.W.3 and M5.W.4 together impose an additional set of forbidden exact widths within that range. M5.W.3 eliminates even-integer multiples of 24 nm: 48, 96, 144, 192, 240, 288, 336, 384, 432, and 480 nm. M5.W.4 eliminates widths spanning an even count of minimum-width routing tracks: 72, 168, 264, 360, and 456 nm. The combined forbidden set is {48, 72, 96, 144, 168, 192, 240, 264, 288, 336, 360, 384, 432, 456, 480} nm. Note that 480 nm appears in M5.W.3's forbidden list, making the effective legal maximum 479 nm.

Resize_end operations on M5 polygon ends along the x-axis constitute a confirmed repair action: trial:i01.ug.leaf_0012.07 applied a 64 dbu resize at the low-x end and a 128 dbu resize at the high-x end of polygon p938, and the result was accepted (decision=gated_in, conn_preserved=true).

## Vertical Width Rule

M5.W.5 sets a 44 nm minimum vertical (y-axis) wire width. No upper bound on vertical width is specified in the M5 rule set.

## Horizontal Spacing

M5.S.1 sets a 24 nm minimum horizontal spacing between any two M5 polygon edges, regardless of edge length or mask color. Tip-to-tip spacing on adjacent tracks is independently constrained: M5.S.3 requires at least 40 nm between wire ends that share no parallel run length, and M5.S.4 requires at least 40 nm between wire ends that do share a parallel run. M5.S.5 further requires that any pair of adjacent-track wires sharing a parallel run have a run length of at least 44 nm.

## Vertical Spacing

M5.S.2 sets a 40 nm minimum vertical spacing between M5 horizontal edges (0° edges).

## Grid and Track Alignment

M5.AUX.1 requires all M5 vertical edges (90° edges, i.e., edges that fix an x-coordinate) to land on a 24 nm x-grid. Any operation that moves a vertical edge must result in a position that is an exact integer multiple of 24 nm; fractional positions on this grid constitute an AUX.1 violation regardless of other width or spacing compliance. The resize_end deltas applied in trial:i01.ug.leaf_0012.07 (64 dbu at the low-x end and 128 dbu at the high-x end of p938) both satisfy this constraint, consistent with the repair passing DRC at the gated-in stage.

M5.AUX.2 identifies minimum-width M5 tracks — polygons that do not survive a ±13 dbu horizontal erosion — and requires their x-axis centerlines to lie on vertical routing tracks defined by pitch 192 dbu and offset 48 dbu from origin. Polygons that do survive the ±13 dbu erosion are classified as wide and are not subject to the AUX.2 centerline constraint, but they are subject to M5.AUX.4: the outer vertical edges of a wide M5 polygon may not coincide with a routing track edge position occupied by a minimum-width wire's vertical edge.

## No-Bend Constraint

M5.AUX.3 flags any M5 corner whose interior angle falls between 0° and 90°, detected via `m5.corners(0..90)`. M5 geometry is strictly rectilinear: L-shapes, jogs, and any polygon that changes direction are prohibited. All M5 polygons in a compliant layout are simple rectangles.

## Via Enclosure

V4.M5.EN.2 requires V4 vias inside M5 to be enclosed by at least 11 nm on two opposite sides, checked independently for x and y. V4.M5.AUX.2 additionally requires that V4 width in the direction perpendicular to M5 length exactly matches the M5 width at that location — neither narrower nor wider. V5.M5.EN.1 applies the same 11 nm two-opposite-side enclosure requirement for V5 vias inside M5.

## Geometry

The GEOMETRY.NONORTHOGONAL rule prohibits any M5 edge at an angle other than exactly 0° or 90°. All M5 polygon edges must be strictly axis-aligned.

## Observed Repair Behavior

Trial:i01.ug.leaf_0012.07 is the only measured operation in this iteration. It applied two resize_end operations to a single M5 polygon (p938) in Block2's unit_gate channel: the low-x end shifted by 64 dbu and the high-x end by 128 dbu. Both operations targeted the same polygon in a single repair pass. Connectivity was preserved (conn_preserved=true) and the repair was accepted (decision=gated_in). Two new DRC violations were introduced inside the crop region (n_new_in_crop=2) with none introduced outside the crop. The gated_in decision despite n_new_in_crop=2 shows that introducing crop-interior violations does not block acceptance when the primary connectivity criterion is satisfied.