## Geometry Constraints

**Vertical width**

M4 vertical width must be at least 24 nm (M4.W.1) and at most 480 nm (M4.W.2). Widths equal to any even integer multiple of 24 nm — specifically 48, 96, 144, 192, 240, 288, 336, 384, 432, and 480 nm — are forbidden by M4.W.3. Widths of 72, 168, 264, 360, and 456 nm are additionally forbidden by M4.W.4 because they cause a polygon to span an even number of minimum-width routing tracks vertically. The compliant vertical widths within the 24–480 nm range are 24, 120, 216, 312, and 408 nm, plus any non-integer-multiple-of-24 values between 24 and 480 nm that also avoid the M4.W.4 list.

Resize_end operations on the y-axis high end are an accepted M4 repair move: polygon p879 received a +48 nm and polygon p910 a +20 nm high-end resize in trial:i01.ug.whole_design.00, and both were accepted in a gated-in, connection-preserving repair.

**Horizontal width**

Minimum horizontal width of M4 is 44 nm (M4.W.5). In trial:i01.ug.whole_design.00, polygon p910 was shifted +8 nm along the x-axis and the repair was gated_in, confirming that small positive x-axis moves on M4 polygons are viable when horizontal-width clearance is maintained.

**Grid alignment of horizontal edges (M4.AUX.1)**

All M4 horizontal edges must lie on a 24 nm absolute grid. Resize operations that adjust vertical endpoints must target coordinates that are multiples of 24 nm. In trial:i01.ug.whole_design.00 the accepted +48 nm high-end resize of p879 is a multiple of 24 nm, consistent with this requirement; the repair was gated_in.

**Routing track centerline alignment (M4.AUX.2)**

Minimum-width M4 tracks (vertical width = 24 nm, i.e., shapes whose top and bottom are both multiples of 96 nm) must have their centerline at y = 48 + N×192 nm for non-negative integer N. The fourteen instance y-moves in trial:i01.ug.whole_design.00 use deltas of 24, 48, 72, and 96 nm — all multiples of 24 nm — and the repair was gated_in, confirming that instance displacements that are multiples of 24 nm do not inherently break routing track alignment for minimum-width M4 shapes.

**No bending (M4.AUX.3)**

M4 polygons must contain no corners with included angles other than 90° or 270°; M4 may not bend. All edits must produce strictly rectilinear (Manhattan) geometry. The resize_end and move operations applied to M4 polygons p879 and p910 in trial:i01.ug.whole_design.00 preserve rectilinear geometry; the repair was gated_in.

**Wide M4 polygon track-edge constraint (M4.AUX.4)**

The outer horizontal edges of M4 polygons wider than 24 nm vertically must not coincide with a routing track edge (i.e., must not fall on y = 48 + N×192 nm or y = 72 + N×192 nm for integer N, which are the bottom and top edges of minimum-width tracks). Resize operations on wide M4 shapes must avoid placing the resulting horizontal edge at these track boundaries.

**Non-orthogonal edges**

M4 must not contain edges at any angle other than 0° or 90° (M4.GEOMETRY.NONORTHOGONAL). The move and resize_end operations applied to M4 in trial:i01.ug.whole_design.00 satisfy this constraint; the repair was accepted as gated_in.

---

## Spacing Constraints

**Vertical spacing (M4.S.1)**

Minimum vertical spacing between horizontal edges of different M4 polygons is 24 nm, enforced both via projection and euclidian measurement. Vertical resizes and instance moves that shift M4 shapes along y must leave at least 24 nm between all opposing horizontal edges on different polygons.

**Horizontal spacing (M4.S.2)**

Minimum horizontal spacing between vertical edges of different M4 polygons is 40 nm (euclidian). The +8 nm x-axis move on polygon p910 in trial:i01.ug.whole_design.00 was accepted as part of a gated-in repair, confirming that small positive x-axis shifts on M4 polygons are viable when the 40 nm horizontal clearance is satisfied after the move.

**Tip-to-tip spacing (M4.S.3 / M4.S.4)**

Minimum tip-to-tip spacing between M4 polygons on adjacent tracks is 40 nm, whether or not the polygons share a parallel run length. Vertical resizes that shorten or extend M4 tips must preserve at least 40 nm separation from any nearby tip on a neighboring track.

**Parallel run length (M4.S.5)**

When two M4 polygons on adjacent tracks share a parallel run — i.e., their extents along the track direction overlap — that run length must be at least 44 nm. Resize or move operations must not create short parallel overlaps shorter than 44 nm between neighboring M4 shapes.

---

## Via Enclosure

**V3 enclosure (V3.M4.EN.2 / V3.M4.AUX.2)**

M4 must enclose each contained V3 via by at least 11 nm on at least two opposite sides. Furthermore, V3 width in the direction perpendicular to M4's length must exactly match the M4 width in that direction; V3 must not protrude beyond or fall short of M4's edges in the perpendicular direction. Vertical resizes on M4 polygons that contain V3 vias must preserve the 11 nm minimum enclosure margin. In trial:i01.ug.whole_design.00 the V3 layer was touched alongside M4 and the repair was accepted as gated_in with conn_preserved=true, confirming that simultaneous M4 resize and V3 layer adjustments can satisfy these enclosure rules.

**V4 enclosure (V4.M4.EN.1)**

M4 must enclose each contained V4 via by at least 11 nm on at least two opposite sides. Resize or move operations on M4 polygons that contain V4 vias must preserve this enclosure margin. In trial:i01.ug.whole_design.00 the V4 layer was adjusted concurrently with M4 and the repair was gated_in with conn_preserved=true, confirming that coordinated M4 and V4 edits can satisfy V4 enclosure.

---

## Observed Repair Operation Patterns

In trial:i01.ug.whole_design.00 (the only measured trial), M4 was repaired by:

- **resize_end, axis=y, end=high, +48 nm** on polygon p879 — accepted, gated_in, conn_preserved.
- **move, axis=x, +8 nm** on polygon p910 — accepted, gated_in, conn_preserved.
- **resize_end, axis=y, end=high, +20 nm** on polygon p910 — accepted, gated_in, conn_preserved.
- **14 instance moves** (x and y) with deltas of 8, 28, and 136 nm in x, and 24, 48, 72, and 96 nm in y — all accepted as part of the same gated-in, conn_preserved repair.

The repair spanned layers M1–M5 and V1–V4 in a single 19-op transaction (n_ops=19), confirming that multi-layer coordinated repairs touching M4 alongside adjacent metal and via layers can resolve M4 DRC violations while preserving connectivity (trial:i01.ug.whole_design.00).