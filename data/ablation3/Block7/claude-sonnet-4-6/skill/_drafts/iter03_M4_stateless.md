## M4 Geometry Constraints

**Vertical (Y-axis) width — M4.W.1, M4.W.2, M4.W.3, M4.W.4.**
The minimum vertical width is 24 nm; the maximum is 480 nm. Widths that are exact even-integer multiples of 24 nm (48, 96, 144, 192, 240, 288, 336, 384, 432, 480 nm) are separately prohibited by M4.W.3. M4.W.4 additionally prohibits the set 72, 168, 264, 360, 456 nm. Permitted vertical widths within the 24–480 nm range are therefore those that are neither an even multiple of 24 nm nor in the M4.W.4 set; examples include 24 nm (1×), 120 nm (5×), 216 nm (9×).

**Horizontal (X-axis) width — M4.W.5.**
The minimum horizontal width is 44 nm. The DRC check uses a Euclidean measurement on vertical edges (with_angle(90)).

**Grid alignment — M4.AUX.1.**
All horizontal (constant-Y) edges of M4 must lie on a 24 nm grid. Off-grid horizontal edges trigger M4.AUX.1 regardless of shape size.

**Routing-track alignment — M4.AUX.2.**
Minimum-width M4 wires (shapes whose Y-extent is less than 13 nm after a ±13 nm sizing, i.e., wires thinner than approximately 26 nm before erosion) must have their centerlines on a 192 nm pitch with a 48 nm origin offset (centerlines at Y = 48, 240, 432, … nm in design units). The check applies only to shapes whose bottom and top edges are already on the 96 nm base grid.

**Wide-polygon track-edge rule — M4.AUX.4.**
Wide M4 polygons (shapes surviving a ±13 nm Y-erosion) must not have their horizontal outer edges coincide with any routing-track edge derived from minimum-width wires. The check finds horizontal edges of the wide polygon that fall within the horizontal band extended from nearby 1× wires.

**No bending — M4.AUX.3.**
M4 shapes with any 0°–90° interior corner trigger M4.AUX.3. All M4 polygons are required to be single-direction rectilinear bars without turns.

**Orthogonality — m4.GEOMETRY.NONORTHOGONAL.**
All M4 edges must be at exactly 0° or 90°. Any edge at 1°–89°, 91°–179°, −179° – −91°, or −89° – −1° is flagged.

## M4 Spacing Constraints

**Vertical spacing — M4.S.1.**
The minimum vertical separation between any two M4 polygon edges is 24 nm. The rule fires on both a projection check (parallel edges) and a Euclidean fallback for edge pairs not caught by projection. A 1 nm Euclidean global check also catches overlapping or touching polygons.

**Horizontal spacing — M4.S.2.**
The minimum horizontal separation between any two vertical M4 edges is 40 nm, measured Euclidean. The check operates on the full set of 90° edges across all M4 polygons.

**Tip-to-tip spacing on adjacent tracks — M4.S.3, M4.S.4.**
When a M4 wire tip (a vertical end-edge) is extended 30 nm inward and 30 nm outward and that extension reaches another M4 edge, the tip is considered "on an adjacent track." The minimum tip-to-tip spacing is 40 nm (projection) for both the case where the two wires share no parallel run length (M4.S.3) and the case where they do share a parallel run length (M4.S.4).

**Parallel run length — M4.S.5.**
When two M4 polygons on adjacent tracks have a vertical gap smaller than 24 nm (triggering projection interaction) and the gap region is narrower than 44 nm horizontally, M4.S.5 fires. The effective requirement is that any two M4 wires running alongside each other on adjacent tracks share at least 44 nm of parallel overlap horizontally.

## Via Enclosure Constraints

**V3 enclosure by M4 — V3.M4.EN.2.**
M4 must enclose every V3 shape by at least 11 nm on at least two opposite sides. The check uses independent X and Y sizing erosions (sized(-11 nm, 0) and sized(0, -11 nm)) and flags V3 shapes that remain after both erosions, i.e., shapes with less than 11 nm enclosure in at least one axis direction.

**V3 width match — V3.M4.AUX.2.**
V3 shapes not fully inside M4 are flagged outright. V3 shapes inside M4 are flagged unless at least two of their edges are coincident with M4 edges on opposite sides. This enforces that V3 width exactly equals the M4 width perpendicular to the wire direction.

**V4 enclosure by M4 — V4.M4.EN.1.**
M4 must enclose every V4 shape that is inside M4 by at least 11 nm on at least two opposite sides (same two-sided erosion logic as V3.M4.EN.2, but applies only to V4 shapes already inside M4).

## Repair Operation Observations

The one confirmed M4 repair in this iteration extended the high-X endpoint of polygon p2279 by +232 dbu on the X-axis (trial:i03.ug.whole_design.00). The operation was accepted (decision: gated_in) and preserved all connectivity. Resize the high-X end of an M4 polygon to correct a horizontal under-width or horizontal under-spacing violation, as grounded by trial:i03.ug.whole_design.00. The delta of 232 dbu was sufficient to resolve the triggering violation in that case without introducing secondary DRC violations, confirming that moderate-length horizontal endpoint extensions are viable repair moves for M4 (trial:i03.ug.whole_design.00).