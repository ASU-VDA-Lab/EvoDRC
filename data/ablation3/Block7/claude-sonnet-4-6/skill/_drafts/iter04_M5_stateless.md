## Geometry: Straight Wires, No Bends, No Non-Orthogonal Edges

M5 polygons must be strictly rectilinear and straight. Rule M5.AUX.3 fires on any polygon that has an interior corner angle between 0° and 90° exclusive, which means no L-bends or T-junctions may appear on a single polygon. Rule GEOMETRY.NONORTHOGONAL catches any edge not at 0° or 90°. Trial:i01.ug.whole_design.00 and trial:i04.ug.whole_design.00 both touched M5 and were accepted with zero new violations, confirming that the repair flow maintains straight-wire geometry throughout.

## Horizontal Width Constraints

Rule M5.W.1 sets a minimum horizontal (x-direction) width of 24 nm. Rule M5.W.2 caps horizontal width at 480 nm. Rules M5.W.3 and M5.W.4 eliminate a large set of intermediate widths:

- M5.W.3 forbids any horizontal width that is an even integer multiple of 24 nm: 48, 96, 144, 192, 240, 288, 336, 384, 432, and 480 nm are all illegal.
- M5.W.4 additionally forbids horizontal widths of 72, 168, 264, 360, and 456 nm, which correspond to polygon extents that span an even number of routing-track pitches.

When moving or resizing M5 polygons, the resulting horizontal width must avoid every value in both forbidden sets. Trial:i04.ug.whole_design.00 applied x-axis moves of -64, -16, and +32 dbu to six M5 polygons (p2211 through p2216) and was accepted with zero new violations, confirming that the post-move widths satisfied M5.W.1 through M5.W.4.

## Vertical Width (Wire Length) Constraint

Rule M5.W.5 requires a minimum vertical (y-direction) extent of 44 nm on each M5 polygon. Any operation that shortens an M5 polygon in y must not reduce its y-extent below 44 nm. Trial:i04.ug.whole_design.00 moved the six M5 polygons only in x, leaving y-extents unchanged, and was accepted with zero new violations, consistent with M5.W.5 remaining satisfied when y-dimensions are not altered.

## Horizontal Spacing Constraints

Rule M5.S.1 requires at least 24 nm of horizontal clearance between any two M5 polygon edges and a blanket minimum of 1 dbu for all orientations combined. Rules M5.S.3 and M5.S.4 both enforce 40 nm tip-to-tip spacing between M5 polygons on adjacent tracks:

- M5.S.3 applies when the two polygons do not share any parallel run length (staggered ends).
- M5.S.4 applies when the two polygons do share a parallel run length (co-linear tips on adjacent tracks).

Rule M5.S.5 further requires that when two adjacent-track M5 polygons run in parallel, their shared parallel run length is at least 44 nm.

Trial:i04.ug.whole_design.00 moved M5 polygons horizontally by three distinct amounts (-64, -16, +32 dbu) and introduced no new M5.S.1, M5.S.3, M5.S.4, or M5.S.5 violations, showing that the repair solver's x-displacements respected all horizontal spacing rules simultaneously.

## Vertical Spacing Constraint

Rule M5.S.2 requires at least 40 nm of vertical clearance between M5 polygons. Trial:i01.ug.whole_design.00 touched M5 as a side effect of M6 y-snapping (all ops labeled m6_snap group, moving M5-connected instances in y) and produced no new M5 vertical-spacing violations, confirming that co-moving instances that carry M5 geometry in y can preserve the 40 nm floor.

## Vertical-Edge Grid Alignment

Rule M5.AUX.1 requires every vertical (y-direction) edge of every M5 polygon to lie on a 24 nm x-grid. When computing a repair x-displacement for an M5 polygon, the resulting left and right edge x-coordinates must each be divisible by 24 dbu. Trial:i04.ug.whole_design.00 applied x-moves of -64, -16, and +32 dbu to M5 polygons without introducing new M5.AUX.1 violations. These displacements are not themselves multiples of 24 dbu, which means the repair engine selects moves that bring existing edge positions to on-grid results rather than requiring the displacement itself to be a 24 dbu multiple.

## Minimum-Width Track Routing Grid (M5.AUX.2)

Rule M5.AUX.2 constrains the x-centerline of minimum-width (24 nm) M5 tracks. The centerline cl must satisfy (cl - 48) ≡ 0 (mod 192) dbu, gated by a sub-filter that requires both the left and right edges of the polygon to be on a 96 dbu sub-grid before the centerline check applies. Valid centerline positions on the primary routing track set are therefore at x = 48, 240, 432, ... dbu (i.e., 48 + N × 192). Trial:i04.ug.whole_design.00 moved M5 polygons in x by -64, -16, and +32 dbu with zero new M5.AUX.2 violations, confirming that the post-move centerlines of min-width tracks land on valid routing positions.

## Wide M5 Placement Constraint (M5.AUX.4)

Rule M5.AUX.4 prohibits the outer vertical edge of any wide M5 polygon from touching a routing-track-band edge. The check projects min-width track positions across the full y-extent and flags any wide M5 edge that coincides with those projected bands. Trial:i04.ug.whole_design.00 moved the same set of M5 polygons (p2211 through p2216) that were also affected by the wide-polygon sizing logic and was accepted with zero new M5.AUX.4 violations, confirming that the chosen x-displacements kept wide polygon outer edges clear of routing track band edges.

## Via Enclosure and Sizing Rules

Rule V4.M5.EN.2 requires M5 to enclose every V4 via by at least 11 nm on two opposite sides. Rule V4.M5.AUX.2 requires V4 to exactly match the M5 wire width in the direction perpendicular to the M5 routing direction — both edges of V4 must coincide with the corresponding M5 edges, with no partial overlap permitted. Rule V5.M5.EN.1 requires M5 to enclose every V5 via by at least 11 nm on two opposite sides.

When an M5 polygon is moved, both the V4 below and the V5 above must be evaluated. Trial:i01.ug.whole_design.00 co-touched M5, V5, and M6 and was accepted with zero new violations, showing that moving M5-connected V5 instances as a unit with M5 preserves V5.M5.EN.1. Trial:i04.ug.whole_design.00 co-touched V4 and V5 alongside M5 and was accepted with zero new violations, confirming that multi-metal-via stack moves that maintain relative via-to-metal geometry do not introduce new V4.M5.EN.2, V4.M5.AUX.2, or V5.M5.EN.1 violations.

## Multi-Layer Co-Movement Pattern

M5 repair operations in this design always involve adjacent metal and via layers simultaneously. Trial:i01.ug.whole_design.00 touched M5, M6, and V5 together (iter 1, 24 ops). Trial:i04.ug.whole_design.00 touched M3, M4, M5, M6, V3, V4, and V5 together (iter 4, 162 ops). Both achieved gated_in acceptance with connectivity preserved and zero new violations. Moving M5 in isolation without co-adjusting V4, V5, and the connected M4/M6 geometry violates the enclosure rules cited above; the repair engine treats the full metal-via stack as the unit of movement.