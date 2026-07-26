## Geometry Constraints

**Width rules (horizontal).** M5.W.1 requires a minimum horizontal width of 24 nm. M5.W.2 caps horizontal width at 480 nm. M5.W.3 forbids horizontal widths that are exact even-integer multiples of 24 nm (i.e., 48, 96, 144, 192, 240, 288, 336, 384, 432, 480 nm are all prohibited widths). M5.W.4 additionally forbids widths of 72, 168, 264, 360, and 456 nm (widths that would span an even number of minimum-width routing tracks). M5.W.5 requires a minimum vertical width of 44 nm.

**Spacing rules.** M5.S.1 requires a minimum horizontal spacing of 24 nm between any two M5 polygon edges, regardless of edge length or mask color. M5.S.2 requires a minimum vertical spacing of 40 nm. M5.S.3 applies a 40 nm tip-to-tip minimum between polygons on adjacent tracks that do not share a parallel run length. M5.S.4 applies the same 40 nm tip-to-tip minimum when the polygons do share a parallel run length. M5.S.5 requires a minimum parallel run length of 44 nm between M5 polygons on adjacent tracks.

**Grid and track placement.** M5.AUX.1 requires all M5 vertical edges to fall on a 24 nm horizontal grid (1 dbu tolerance). M5.AUX.2 requires minimum-width M5 tracks (those that are exactly minimum width, i.e., not wider than 26 nm after the ±13 nm erosion-dilation test) to center on vertical routing tracks spaced at multiples of 192 dbu with a 48 dbu offset from the origin. M5.AUX.4 prohibits the outside vertical edges of wide M5 polygons from coinciding with any routing track edge occupied by a minimum-width track.

**Bending prohibition.** M5.AUX.3 prohibits any bend in an M5 polygon: no corner with an interior angle between 0° and 90° (exclusive) is permitted. All M5 geometry must be strictly rectilinear and non-self-intersecting.

**Non-orthogonal edge prohibition.** The GEOMETRY.NONORTHOGONAL block applies to M5: any edge at an angle other than 0° or 90° (i.e., angles 1–89°, 91–179°, −179° to −91°, or −89° to −1°) is a violation.

## Via Enclosure Constraints

**V4 enclosure.** V4.M5.EN.2 requires M5 to enclose each V4 via by at least 11 nm on two opposite sides (both horizontal and vertical). V4.M5.AUX.2 requires V4 to exactly match the width of M5 in the direction perpendicular to the M5 length; each V4 must have at least two coincident edges with M5 and must be fully inside M5.

**V5 enclosure.** V5.M5.EN.1 requires M5 to enclose each V5 via by at least 11 nm on at least two opposite sides.

## Observed Repair Behavior

The single recorded trial for this layer is trial:i01.ug.whole_design.00. All 24 operations in this trial belonged to the `m6_snap` group and moved M6 polygons and cell instances along the Y axis; no direct M5 polygon operations were performed. M5 appeared in `touched_layers` because the M6/V5 movements affected inter-layer DRC checks involving M5 (V5.M5.EN.1 and V4.M5.AUX.2 in particular). The trial was accepted with `conn_preserved:true` and zero new violations entering or leaving crop (trial:i01.ug.whole_design.00). This establishes that Y-axis snapping of M6 and co-moving instances, while touching M5 indirectly through via enclosure checks, does not itself introduce M5 violations when M5 geometry remains unmodified.