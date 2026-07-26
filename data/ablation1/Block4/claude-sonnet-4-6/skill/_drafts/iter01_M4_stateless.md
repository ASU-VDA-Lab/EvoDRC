## M4 Geometry Constraints

M4 is a horizontal-routing metal layer. Its vertical (y-axis) edges are the routing edges, and its horizontal (x-axis) edges define track boundaries. The rules impose hard quantized constraints in both axes.

**Vertical-width quantization (M4.W.1–M4.W.4).** Legal vertical widths are between 24 nm and 480 nm, but must not be any even multiple of 24 nm (48, 96, 144, 192, 240, 288, 336, 384, 432, 480 nm are all forbidden by M4.W.3) and must not equal 72, 168, 264, 360, or 456 nm (forbidden by M4.W.4). This leaves a sparse set of legal heights. When resizing in y, snap to a legal value rather than incrementing by the minimum step.

**Horizontal-width floor (M4.W.5).** Minimum horizontal width is 44 nm. Widening in x is the primary repair for violations involving polygon p1374 (trial:i01.ug.leaf_0001.07, +200 dbu x-resize, gated_in) and polygon p1395 (trial:i01.ug.Block4_union_row7.06, +172 dbu high-x resize_end, gated_in).

**Horizontal-edge grid (M4.AUX.1).** All M4 horizontal edges must land on the 24 nm grid. Any y-coordinate resize must produce a y-value that is a multiple of 24 nm. Off-grid horizontal edges trigger M4.AUX.1 regardless of width legality.

**Track alignment for minimum-width stripes (M4.AUX.2).** M4 stripes whose vertical extent is within 13 nm of the minimum width (i.e., effective 1x tracks) must have their centerlines at y positions satisfying `(cl − 48) mod 192 = 0` in dbu. Moving or resizing a minimum-width stripe in y must land the resulting centerline on this grid, not just any 24 nm-grid point.

**No bends allowed (M4.AUX.3).** M4 polygons must be purely rectilinear with no interior corners in the 0–90° range. Do not introduce L-shaped or T-shaped M4 geometries; the checker rejects any polygon with a concave corner.

**Wide-shape track-edge rule (M4.AUX.4).** For wide M4 polygons (vertical extent > 24 nm after the 13 nm erosion), the horizontal outer edges must not coincide with any minimum-width routing track edge. When expanding a polygon vertically past 1x, verify the new outer edges do not touch track boundaries.

## Vertical and Horizontal Spacing

**Vertical spacing (M4.S.1).** Minimum vertical gap between any two M4 edges is 24 nm. Both projection-based and euclidean checks are applied, so irregular-length edges are caught by the secondary euclidean pass. When moving polygons in y, maintain at least 24 nm clearance from all neighbors.

**Horizontal spacing (M4.S.2).** Minimum horizontal gap between M4 vertical edges is 40 nm, measured euclidean. Widening a polygon in x (as in trial:i01.ug.leaf_0001.07 and trial:i01.ug.Block4_union_row7.06) must not close this gap to a neighbor on the same track.

**Tip-to-tip spacing on adjacent tracks (M4.S.3, M4.S.4).** When two M4 stripes share no parallel run length, the minimum tip-to-tip horizontal gap is 40 nm (M4.S.3). When they do share parallel run length, the same 40 nm gap applies (M4.S.4). Extending a stripe's endpoint in x can simultaneously resolve an enclosure violation while risking a tip-to-tip violation; check both before committing.

**Parallel run length floor (M4.S.5).** Two M4 polygons on adjacent tracks with a horizontal gap narrower than 24 nm must have a parallel overlap of at least 44 nm. Short stubs that face a neighbor without 44 nm of parallel run are flagged. Extending a polygon in x to reach 44 nm parallel run resolves this violation.

## Via Enclosure Coupling

**V3 enclosure (V3.M4.EN.2).** V3 vias must be enclosed by M4 by at least 11 nm on two opposite sides. When M4 is resized or moved, verify V3 enclosure is maintained in both the horizontal and vertical axes.

**V3 width match (V3.M4.AUX.2).** V3 must match M4's width in the direction perpendicular to M4's length. Resizing a M4 stripe in y without correspondingly adjusting V3 will trigger this rule. The multi-layer coordinated move in trial:i01.ug.Block4_union_row7.06 (which touched M1, M2, M3, M4, V1, V2 together) demonstrates that via-coupled polygons must move together to preserve this relationship.

**V4 enclosure (V4.M4.EN.1).** V4 vias inside M4 require 11 nm enclosure on at least two opposite sides. Applies symmetrically to the V4/M4 interface.

## Repair Strategies Observed

**Horizontal extension of M4 stripes resolves violations without introducing new ones.** A +200 dbu x-resize of polygon p1374 was accepted with zero new in-crop or out-of-crop violations and full connectivity preservation (trial:i01.ug.leaf_0001.07). A +172 dbu high-x resize_end of polygon p1395, combined with coordinated x-moves of adjacent polygons and instances, was similarly accepted with zero new violations (trial:i01.ug.Block4_union_row7.06).

**Multi-polygon, multi-layer coordinated moves are feasible in the unit_gate channel.** The five-operation repair in trial:i01.ug.Block4_union_row7.06 moved two instances and two metal polygons (in x by −28 dbu each) and resized one M4 polygon endpoint, spanning M1 through M4 and V1/V2, with connectivity and DRC both satisfied. Coordinating instance moves with polygon moves is necessary when the instance's internal routing pins must stay aligned with the abutting metal.

**Small x-deltas on the order of 28 dbu are legal moves for M4 polygons in this design context.** The −28 dbu moves of p1596 and p1477 in trial:i01.ug.Block4_union_row7.06 were accepted, indicating that the surrounding spacing and grid constraints permitted this step size at those loci.