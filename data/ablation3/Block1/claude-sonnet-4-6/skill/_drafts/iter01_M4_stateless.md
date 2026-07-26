## Rule Landscape

M4 is a horizontal-preferred routing layer with a rich set of dimensional, spacing, grid, and topology constraints. The rules fall into five categories: width (M4.W.1–5), spacing (M4.S.1–5), grid and track alignment (M4.AUX.1–4), via enclosure from below (V3.M4.EN.2, V3.M4.AUX.2), via enclosure from above (V4.M4.EN.1), and the universal non-orthogonal geometry block.

**Width rules (M4.W.1–5).** Vertical (horizontal-edge) width has a floor of 24 nm and a ceiling of 480 nm. Widths that are exact even integer multiples of 24 nm (48, 96, 144, 192, 240, 288, 336, 384, 432, 480 nm) are forbidden by M4.W.3. Widths of 72, 168, 264, 360, and 456 nm are additionally excluded by M4.W.4, because they would span an even number of minimum-width routing tracks vertically. Horizontal (vertical-edge) width has a floor of 44 nm (M4.W.5).

**Spacing rules (M4.S.1–5).** Vertical spacing between M4 polygons is 24 nm minimum (M4.S.1, projection along horizontal edges). Horizontal spacing between vertical edges is 40 nm minimum (M4.S.2). Tip-to-tip spacing on adjacent tracks is 40 nm whether or not the segments share parallel run length (M4.S.3, M4.S.4). Parallel run length for segments on adjacent tracks must be at least 44 nm (M4.S.5).

**Grid and topology rules (M4.AUX.1–4).** Horizontal edges must fall on a 24 nm grid (M4.AUX.1). Minimum-width (1× track) M4 segments must have centerlines on the horizontal routing grid: pitch 192 dbu with an offset of 48 dbu from the origin (M4.AUX.2). M4 polygons must be strictly rectilinear—no bends are permitted (M4.AUX.3). The outer horizontal edges of wide (>1× track) M4 polygons must not coincide with any routing-track centerline edge that belongs to a separate 1× segment (M4.AUX.4).

**Via enclosure rules.** V3 vias must be enclosed by M4 by at least 11 nm on at least two opposite sides (V3.M4.EN.2), and V3 must be exactly flush with M4 in the direction perpendicular to the M4 length (V3.M4.AUX.2). V4 vias inside M4 are subject to the same 11 nm two-side enclosure requirement (V4.M4.EN.1).

**Geometry.** All M4 edges must be strictly orthogonal (m4.GEOMETRY.NONORTHOGONAL).

---

## Measured Operation Evidence (iteration 1)

The single trial in this layer's history is trial:i01.cu.def:VIA_VIA45_1_2_58_58.00. The operation was a `resize_via_shape` applied to the M5 shape in cell `VIA_VIA45_1_2_58_58`, shrinking it by 88 dbu in the y-axis. M4, M5, and V4 were all recorded as touched layers, the decision was applied, and connectivity was confirmed preserved. The repair reduced the total violation count by 52 across the whole design.

Because the fix operated on M5 while M4 and V4 were co-touched, the enclosure relationship governed by V4.M4.EN.1 is the most direct M4-side constraint implicated (trial:i01.cu.def:VIA_VIA45_1_2_58_58.00). Shrinking the via cell's M5 shape vertically in a shared via-cell context adjusted geometry visible to both M4 (as the lower landing metal) and V4 (as the via itself), and the net result was a large violation reduction with no connectivity loss.

No direct resize or move of M4 shapes was performed in this iteration. All M4-specific geometric rules (width, spacing, grid, bend prohibition) were not the target of any recorded operation in trial:i01.cu.def:VIA_VIA45_1_2_58_58.00; their current compliance status is therefore not grounded in a measured repair for this iteration.