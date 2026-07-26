## Layer M5 — Measured Repair Knowledge (Iteration 3)

### Rule Summary: Width

M5.W.1 sets minimum horizontal width at 24 nm. M5.W.2 caps horizontal width at 480 nm. M5.W.3 forbids horizontal widths that are exact even-integer multiples of 24 nm (48, 96, 144, 192, 240, 288, 336, 384, 432, 480 nm). M5.W.4 independently forbids horizontal widths of 72, 168, 264, 360, or 456 nm. M5.W.5 sets minimum vertical width at 44 nm.

The intersection of M5.W.3 and M5.W.4 means the legal set of horizontal widths is the set of positive values ≥ 24 nm and ≤ 480 nm that are neither even-integer multiples of 24 nm nor members of {72, 168, 264, 360, 456 nm}. Odd multiples of 24 nm that do not appear in the M5.W.4 list (e.g., 24, 120, 216, 312, 408 nm) are the primary valid widths.

### Rule Summary: Spacing

M5.S.1 requires minimum horizontal spacing of 24 nm between any two M5 polygon edges, regardless of edge length or mask color; a separate catch-all requires spacing ≥ 1 dbu globally. M5.S.2 requires minimum vertical spacing of 40 nm. M5.S.3 and M5.S.4 each require a minimum tip-to-tip spacing of 40 nm between M5 polygons on adjacent tracks, regardless of whether a parallel run length is shared. M5.S.5 requires a minimum parallel run length of 44 nm between M5 polygons on adjacent tracks.

### Rule Summary: Geometry and Grid

M5.AUX.1 requires all M5 vertical edges to lie on a 24 nm horizontal grid. M5.AUX.2 requires that minimum-width M5 tracks (width ≤ ~24 nm, identified by the erosion-restoration test with 13 nm margin) have their centerlines at positions satisfying `(cl - 48) mod 192 == 0` in dbu, i.e., centerlines at 48, 240, 432, 624, … dbu. Wide M5 polygons (wider than ~26 nm) are excluded from M5.AUX.2 but are subject to M5.AUX.4: the outside vertical edge of a wide M5 polygon must not coincide with a routing-track edge. M5.AUX.3 prohibits M5 from bending; any corner with an interior angle in the range 0–90° constitutes a violation, so all M5 shapes must be purely rectilinear L-free strips.

M5.GEOMETRY.NONORTHOGONAL prohibits edges at any non-axis-aligned angle.

### Rule Summary: Via Enclosure

V4.M5.EN.2 requires at least 11 nm enclosure of V4 by M5 on two opposite sides. V4.M5.AUX.2 requires that V4 be exactly the same width as M5 in the direction perpendicular to the M5 length direction; V4 edges must be coincident with M5 edges in that dimension. V5.M5.EN.1 requires at least 11 nm enclosure of V5 by M5 on at least two opposite sides.

### Measured Repair Patterns

**Via-cell x-axis resize (cu_pool channel):** Expanding both V4 shapes in cell `VIA_VIA45_1_2_58_58` by +152 dbu along the x-axis, together with an equal +152 dbu expansion of the M4 shape in the same cell, reduced windowed violation counts by 8 per unit in both `leaf_0012` and `leaf_0013` (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, delta_total −16). The M5 layer was among the touched layers in that operation. The pattern is consistent with V4.M5.AUX.2 requiring exact width match between V4 and M5 perpendicular to the M5 run direction: when V4 was undersized relative to M5 in x, expanding the V4 cell shapes until their edges became coincident with the enclosing M5 edges resolved the rule. Resize both V4 shapes within the cell (shape_index 0 and 1) and the corresponding metal shape together to maintain the exact-width constraint (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01).

**Instance x-axis moves and polygon moves:** A +32 dbu move of polygon p938 combined with matching +32 dbu moves of instances i0098, i0097, i0064, and i0068 produced zero new in-crop and zero new out-of-crop violations on M5 (trial:i02.ug.leaf_0002.01). A 32 nm shift is a sub-pitch correction consistent with snapping a minimum-width M5 track centerline onto the AUX.2 grid (pitch 192 dbu, offset 48 dbu). Move polygon and all co-placed instances together to avoid introducing relative misalignment that would violate V4.M5.AUX.2 or M5.AUX.2 (trial:i02.ug.leaf_0002.01).

**Instance y-axis moves:** Vertical instance moves in multiples of 48 dbu (trials i01.ug.leaf_0012.07, i03.ug.leaf_0001.00) and 72 dbu (trial:i03.ug.leaf_0002.01) produced zero new out-of-crop M5 violations across all three trials. The 48 dbu step (48 nm) exceeds the M5.S.2 minimum vertical spacing of 40 nm and the M5.W.5 minimum vertical width of 44 nm, making it a safe minimum step size for vertical repositioning of instances that include M5 geometry. The 72 dbu step similarly clears both constraints. Use y-axis moves that are multiples of 48 dbu to stay clear of M5.S.2 and M5.W.5 violations (trial:i01.ug.leaf_0012.07, trial:i03.ug.leaf_0001.00, trial:i03.ug.leaf_0002.01).

**Connectivity-gated acceptance:** All five trials that touched M5 were accepted (decisions: `applied` or `gated_in`) with `conn_preserved: true`. Two trials introduced new in-crop violations on unrelated rules — trial:i01.ug.leaf_0012.07 introduced 2 new V1.M1.EN.1 in-crop violations and trial:i03.ug.leaf_0002.01 introduced 1 new in-crop violation — but both were still accepted because connectivity was preserved. The M5 operations themselves did not introduce new out-of-crop violations in any trial.

**Paired counter-moves:** Trials i01.ug.leaf_0012.07 and i03.ug.leaf_0002.01 both apply pairs of instances moved in opposite y-directions (e.g., −48 for i0097/i0092 and +96 for i0064/i0072; +72 for i0095/i0099 and −72 for i0069/i0066). These paired moves adjust relative row positions while keeping the M5 routing geometry compliant. Zero new out-of-crop M5 violations resulted from such paired opposite moves (trial:i01.ug.leaf_0012.07, trial:i03.ug.leaf_0002.01).