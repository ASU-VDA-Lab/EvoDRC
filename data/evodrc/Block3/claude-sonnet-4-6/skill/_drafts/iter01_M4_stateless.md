## Repair Patterns and Observed Outcomes

### Horizontal M4 Resize in Via Cells

The only measured repair on this layer widened the M4 shape inside via cell `VIA_VIA45_1_2_58_58` by +152 dbu along the x-axis (`resize_via_shape`, `shape_index=0`, `axis=x`, `delta_dbu=+152`), combined with coordinated V4 shape moves and resizes on the same cell (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01). The repair was applied (`decision=applied`), reduced total violations by 18 across two windows (`unit:leaf_0018`: −10; `unit:leaf_0019`: −8), and preserved connectivity (`conn_preserved=true`).

M4.W.5 requires a minimum horizontal width of 44 nm. M4.S.2 requires a minimum horizontal spacing of 40 nm between M4 vertical edges. V4.M4.EN.1 requires that V4 inside M4 has at least 11 nm enclosure on two opposite sides. Widening M4 horizontally in a via cell simultaneously addresses M4.W.5 shortfalls and V4.M4.EN.1 enclosure deficits on the x-axis faces of the enclosed V4 shapes. The coordinated V4 moves (±116 dbu) and V4 resizes (+384 dbu each) in the same five-operation bundle confirm that M4 resizing alone does not satisfy V4.M4.EN.1; M4 and V4 shapes must be adjusted together in the same repair to close enclosure violations without introducing new spacing errors (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01).

### V3.M4.AUX.2 and V3.M4.EN.2 Interaction

V3.M4.AUX.2 mandates that V3 width exactly matches M4 width in the direction perpendicular to M4 length, meaning any horizontal M4 resize that changes the M4 boundary touching a V3 shape will break AUX.2 unless the V3 shape is adjusted to match. V3.M4.EN.2 independently requires 11 nm enclosure on at least two opposite sides. The measured trial did not touch V3 or M3 (`touched_layers: ["M4","M5","V4"]`), which confirms that the repair locus did not include any V3 interactions at that site (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01). Repairs that do involve M4 shapes enclosing V3 must account for both rules simultaneously.

### Width Constraints (M4.W.1–M4.W.4)

M4.W.1 sets a minimum vertical width of 24 nm. M4.W.2 caps vertical width at 480 nm. M4.W.3 forbids vertical widths that are even integer multiples of 24 nm (i.e., 48, 96, 144, …, 480 nm). M4.W.4 additionally forbids widths of 72, 168, 264, 360, and 456 nm. The measured M4 resize was horizontal (axis=x), so vertical width was not altered in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01; vertical width rules were not the driving constraint in that repair. Any future vertical resize of M4 must land outside the forbidden even-multiple set (M4.W.3) and outside the five additional forbidden values (M4.W.4).

### Spacing Rules and Tip Geometry (M4.S.1–M4.S.5)

M4.S.1 requires 24 nm minimum vertical spacing. M4.S.2 requires 40 nm minimum horizontal spacing between vertical edges. M4.S.3 and M4.S.4 impose 40 nm tip-to-tip spacing between M4 polygons on adjacent tracks, with M4.S.3 applying when polygons do not share parallel run length and M4.S.4 when they do. M4.S.5 requires a minimum parallel run length of 44 nm for M4 polygons on adjacent tracks. The horizontal M4 resize of +152 dbu in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 increased M4 extent in x; whether M4.S.2 or M4.S.3/S.4 spacing to neighboring shapes was affected is not separately reported in that trial's delta breakdown, but the net result was a reduction in violations, confirming that the sizing did not open new spacing DRC errors.

### Grid and Track Alignment (M4.AUX.1, M4.AUX.2, M4.AUX.4)

M4.AUX.1 requires all M4 horizontal edges to lie on a 24 nm grid. M4.AUX.2 requires minimum-width M4 tracks to have their centerlines at positions satisfying `(cl − 48) mod 192 = 0` (i.e., on a 192 dbu pitch with a 48 dbu offset from the origin). M4.AUX.4 forbids horizontal edges of wide M4 polygons from coinciding with routing track edges. The measured horizontal resize did not alter M4 horizontal edge positions, only the extent of M4 in x, so AUX.1 and AUX.2 track alignment were not disturbed by trial:i01.cu.def:VIA_VIA45_1_2_58_58.01. Any vertical M4 resize or move must snap horizontal edges to the 24 nm grid (AUX.1) and, for minimum-width shapes, must land on the defined track grid (AUX.2).

### No-Bend Constraint (M4.AUX.3)

M4.AUX.3 prohibits any bend in M4 polygons (corners with included angle 0°–90°). The via cell targeted in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 produced no AUX.3 violations after the repair was applied. All M4 shapes in via cells and routing segments must remain strictly rectilinear; no L-turns or jogs are permitted.

### Vertical Spacing and Track Pitch (M4.S.1, M4.AUX.2)

M4.S.1 enforces 24 nm vertical spacing, the same as M4.W.1's minimum width, so the combined pitch for minimum-width M4 tracks is 48 nm. M4.AUX.2 operates on a 192 dbu (192 nm) super-pitch with a 48 nm offset, implying the legal track centerline positions repeat every 192 nm. Repairs must not push M4 shapes into the 24 nm vertical gap between adjacent tracks.

### Repair Bundle Composition

The successful five-operation repair bundle in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 followed the pattern: move both V4 shapes outward/inward along x to center them, resize both V4 shapes to meet enclosure, then resize M4 to cover the new V4 extents with required margin. The M4 resize (+152 dbu) was the final step and the smallest delta in the bundle. This ordering—via shape repositioning first, metal resize last—produced a net −18 violation result with no new violations introduced.