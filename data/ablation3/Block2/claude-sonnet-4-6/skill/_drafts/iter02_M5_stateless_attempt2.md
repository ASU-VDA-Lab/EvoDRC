## Grid and Track Alignment

M5.AUX.1 requires all M5 vertical edges to land on a 24 nm (24 dbu) x-grid. M5.AUX.2 requires minimum-width M5 tracks (those satisfying `m5 - m5.sized(-13.nm,0).sized(13.nm,0)`) to have their centerlines at positions `48 + N×192` dbu from the origin on the x-axis. Trial i02.ug.whole_design.00 corrected grid alignment by moving M5 polygons p937 and p938 by +32 dbu in x, and by extending the high x-end of polygons p958 through p965 each by +32 dbu; the result was gated in with no new violations and connectivity preserved. Additional alignment was achieved with a +116 dbu high-end resize on p1065 and a +80 dbu high-end resize on p1036, each paired with instance moves of [72, 0] dbu; these also passed with no new violations (trial i02.ug.whole_design.00).

## Width Rules

M5.W.1 sets minimum horizontal width at 24 nm. M5.W.2 sets maximum horizontal width at 480 nm. M5.W.3 prohibits widths that are exact even integer multiples of 24 nm (48, 96, 144, 192, 240, 288, 336, 384, 432, 480 nm). M5.W.4 prohibits widths that cause the polygon to span an even number of minimum-width routing tracks horizontally, specifically those tested at gap distances of 72, 168, 264, 360, and 456 nm. M5.W.5 sets minimum vertical width at 44 nm.

The end-resize magnitudes applied in trial i02.ug.whole_design.00 (+32, +80, +116 dbu) were all accepted with no new violations, confirming these delta values do not push affected M5 polygons into the forbidden width bands defined by M5.W.3 and M5.W.4. When selecting a resize delta, the resulting total width must not equal any of the prohibited multiples enumerated in M5.W.3 or produce a gap distance matching the M5.W.4 test values.

## Spacing Rules

M5.S.1 requires horizontal spacing between M5 edges of at least 24 nm (projection check along x, and absolute 1 nm everywhere). M5.S.2 requires vertical spacing of at least 40 nm. M5.S.3 requires tip-to-tip spacing of 40 nm between polygons on adjacent tracks when they share no parallel run length. M5.S.4 requires 40 nm tip-to-tip spacing between polygons on adjacent tracks that do share a parallel run length. M5.S.5 requires that two M5 polygons on adjacent tracks with horizontal spacing less than 25 nm share at least 44 nm of parallel run length.

Trial i02.ug.whole_design.00 applied y-axis instance displacements of ±48, ±72, and ±96 dbu concurrently with +32 dbu x-moves and produced no new violations; these y-offsets are multiples of the 48 dbu vertical step (2× the 24 nm minimum width) and maintain the spacing relationships required by M5.S.2 through M5.S.5. The x-moves of +32 dbu on p937, p938, and p958–p965 kept all horizontal spacings at or above the M5.S.1 minimum of 24 nm.

## No-Bend Constraint

M5.AUX.3 prohibits any bend in M5 polygons; any edge that participates in a corner with an interior angle between 0° and 90° (exclusive) causes a violation. Both recorded trials used only rectilinear move and resize operations: trial i01.cu.def:VIA_VIA45_1_2_58_58.01 applied x-axis resize ops on V4 and M4 shapes, and trial i02.ug.whole_design.00 applied x-axis moves and high-end x resizes. Neither trial introduced new M5 violations, confirming that axis-aligned move and resize operations preserve M5's non-bending geometry. Do not introduce diagonal edges or non-orthogonal vertices into M5 shapes; the GEOMETRY.NONORTHOGONAL rule fires on any edge with an angle between 1° and 89° or 91° and 179°.

## Wide Polygon Track-Edge Constraint

M5.AUX.4 prohibits the vertical (x-direction) outside edges of wide M5 polygons from coinciding with any routing track edge. A polygon is wide when it survives `m5.sized(-13.nm,0).sized(13.nm,0)` erosion. Wide polygon vertical edges must not fall at positions that are also routing track edges (i.e., positions in the set `48 + N×192` dbu). Trial i02.ug.whole_design.00 applied end-resizes of +80 dbu on p1036 and +116 dbu on p1065 without producing new violations, establishing that these specific delta magnitudes position the resulting high edges at locations that do not coincide with routing track edges.

## Via Enclosure: V4

V4.M5.EN.2 requires that V4 vias inside M5 be enclosed by at least 11 nm on two opposite sides. V4.M5.AUX.2 requires each V4 via to exactly match the M5 wire width in the direction perpendicular to the M5 length (i.e., in x for horizontally-routed M5). Trial i01.cu.def:VIA_VIA45_1_2_58_58.01 fixed violations in cell VIA_VIA45_1_2_58_58 by resizing V4 shape_index 0 and shape_index 1 each by +152 dbu in x, and simultaneously resizing the M4 shape_index 0 by +152 dbu in x. This reduced total violations by 16 (from 68 to 52) with connectivity preserved. Resizing both V4 shapes by the same delta in x aligns them to the M5 horizontal extent to satisfy V4.M5.AUX.2's exact-width requirement. The co-resize of M4 by the same +152 dbu is required to keep the M4–V4 interface consistent; omitting it would leave M4 undersized relative to V4.

## Via Enclosure: V5

V5.M5.EN.1 requires V5 vias inside M5 to be enclosed by at least 11 nm on at least two opposite sides. No V5-specific repair operations appear in either recorded trial; the rule governs the M5 geometry at V5 via locations symmetrically to how V4.M5.EN.2 governs it at V4 locations.

## Validated Repair Patterns

**Via-cell V4 horizontal resize** (trial i01.cu.def:VIA_VIA45_1_2_58_58.01): In a via cell, resize both V4 shapes (shape_index 0 and 1) by the same delta in x, and resize the M4 shape by the same delta. A +152 dbu x-resize across all three shapes reduced violations by 16 with connectivity preserved. The equal delta across V4 shapes and the paired M4 resize are both required; the M5 polygon geometry in the cell was not directly modified.

**M5 polygon x-alignment moves and end-resizes** (trial i02.ug.whole_design.00): Move M5 polygons by a uniform +32 dbu in x, or extend the high x-end by +32 dbu (resize_end, axis x, end high). For polygons that require larger correction, +80 dbu and +116 dbu high-end resizes are validated at the whole-design scope, each paired with instance moves of [72, 0] dbu. Y-axis instance displacements of ±48, ±72, and ±96 dbu are safe companions to x-axis corrections and do not introduce new M5 violations.