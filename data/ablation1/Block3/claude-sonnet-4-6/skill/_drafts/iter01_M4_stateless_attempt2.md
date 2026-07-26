## Grid and Topology Constraints

M4.AUX.1 checks `m4.merged.ongrid(1.dbu, 24.nm)`: horizontal edges are flagged when they fall off the 24 nm vertical grid.

M4.AUX.2 isolates minimum-width M4 segments (those eliminated by a ±13 nm vertical erosion) whose horizontal edges are already on a 96 dbu base grid, then flags any segment whose centerline is not on a 192 dbu pitch with a 48 dbu offset from origin.

M4.AUX.3 flags any M4 corner with an included angle in the 0..90 degree range; the rule fires independently of M4.GEOMETRY.NONORTHOGONAL, which separately flags M4 edges at any non-orthogonal angle.

## Vertical Width Rules

M4.W.1 flags M4 polygons narrower than 24 nm in the vertical direction; M4.W.2 flags polygons wider than 480 nm vertically. Within that range, M4.W.3 additionally flags widths equal to even integer multiples of 24 nm (48, 96, 144, 192, 240, 288, 336, 384, 432, 480 nm), and M4.W.4 additionally flags widths of 72, 168, 264, 360, and 456 nm (widths that span an even number of minimum-width routing tracks). The set of vertical widths that pass all four rules in the 24–480 nm range is therefore limited to 24, 120, 216, 312, and 408 nm.

## Horizontal Width and Spacing

M4.W.5 flags M4 polygons whose euclidian horizontal width is below 44 nm (checked against vertical edges).

M4.S.1 flags M4-to-M4 vertical spacing below 24 nm (both projection and euclidian checks). M4.S.2 flags horizontal spacing below 40 nm between any two vertical M4 edges. M4.S.3 and M4.S.4 each enforce a 40 nm tip-to-tip floor between M4 polygons on adjacent tracks regardless of whether the polygons share a parallel run length. M4.S.5 additionally flags cases where two M4 polygons on adjacent tracks have a parallel run shorter than 44 nm.

## Via Enclosure

V3.M4.EN.2 flags V3 vias that lack at least 11 nm of M4 enclosure on two opposite sides simultaneously. V3.M4.AUX.2 flags V3 that either lies outside M4 or lies inside M4 but does not share at least two coincident edges with it, enforcing width-match between V3 and M4 perpendicular to the wire direction.

V4.M4.EN.1 applies the same two-opposite-side 11 nm enclosure check for V4 vias within M4.

## Wide-Polygon Track Alignment

M4.AUX.4 separates M4 polygons into minimum-width segments and wide segments, constructs horizontal bands from the minimum-width neighbors, and flags horizontal edges of wide polygons that fall inside a band coinciding with a routing-track edge position.

## Observed Repair History

The complete recorded history for M4 at iteration 1 covers one repair target, `def:VIA_VIA45_1_2_58_58`, at locus `[1728, 2068, 11016, 10892]`.

The applied fix (trial:i01.cu.def:VIA_VIA45_1_2_58_58.02) performed a single operation: an M5 y-axis resize of −88 dbu. Total DRC count fell by 20 (−11 in window `unit:leaf_0018`, −9 in `unit:leaf_0019`). M4 is listed in `touched_layers` for trial:i01.cu.def:VIA_VIA45_1_2_58_58.02, confirming that correcting M5 geometry at this locus resolves M4-associated violations — most likely enclosure violations under V4.M4.EN.1 — without any direct M4 shape edit.

A competing candidate (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01) applied five operations: a V4 x-move of −116 dbu, a V4 x-resize of +384 dbu, a V4 x-move of +116 dbu, a second V4 x-resize of +384 dbu, and one M4 x-axis resize of +152 dbu. That candidate reduced violations by only 18 and lost the tournament. The M4 x-axis resize included in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 did not produce a better outcome than the M5-only approach in trial:i01.cu.def:VIA_VIA45_1_2_58_58.02.