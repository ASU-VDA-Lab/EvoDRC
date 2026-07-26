## Effective Repair Operations for M5 Horizontal Geometry

All three accepted repairs used `resize_end` on the x-axis (horizontal) as the primary M5 operation: trial:i01.ug.leaf_0012.07 applied two x-axis endpoint moves to p938, trial:i02.ug.leaf_0003.02 applied one x-axis endpoint move to p938, and trial:i03.ug.leaf_0002.01 applied two x-axis endpoint moves to p937. Do not use y-axis `resize_end` as the primary repair for horizontal-domain violations; no accepted instance of that approach exists in this layer's history.

## Simultaneous Low-End and High-End Resizing

Resize both endpoints of an M5 polygon in the same compound operation when a constraint requires coordinated adjustment of the horizontal span. Trial:i01.ug.leaf_0012.07 moved the low end by 64 dbu and the high end by 128 dbu on p938 in a single compound op and was accepted. Trial:i03.ug.leaf_0002.01 moved the low end by 64 dbu and the high end by 320 dbu on p937 in a single compound op and was accepted. Single-end resizing is also accepted: trial:i02.ug.leaf_0003.02 moved only the low end by 192 dbu on p938 and was gated in.

## Delta Magnitudes and Grid Alignment

All x-axis resize deltas in accepted operations are multiples of 64 dbu: 64 and 128 in trial:i01.ug.leaf_0012.07; 192 in trial:i02.ug.leaf_0003.02; 64 and 320 in trial:i03.ug.leaf_0002.01. Rule M5.AUX.1 requires all M5 vertical edges to lie on a 24 nm grid; rule M5.AUX.2 requires minimum-width M5 tracks to lie on routing tracks at a 192 dbu pitch with a 48 dbu offset from origin. Apply resize deltas that are multiples of 64 dbu when adjusting M5 horizontal endpoints; a delta of exactly 192 dbu (one full routing pitch) cleanly relocates a minimum-width track to the nearest on-track position, as trial:i02.ug.leaf_0003.02 demonstrates.

## Forbidden Horizontal Widths (M5.W.3 and M5.W.4)

Rules M5.W.3 and M5.W.4 prohibit horizontal widths that are even integer multiples of the 24 nm minimum (48, 96, 144, 192, 240, 288, 336, 384, 432, 480 nm) and widths that cause a polygon to span an even number of minimum-width routing tracks horizontally (72, 168, 264, 360, 456 nm). Before committing any endpoint resize, verify the resulting width does not fall on any of these forbidden values. All three accepted repairs produced widths that cleared these forbidden values: trial:i01.ug.leaf_0012.07, trial:i02.ug.leaf_0003.02, and trial:i03.ug.leaf_0002.01.

## Instance Moves for Vertical Geometry Corrections

When vertical spacing or width violations require adjustment, move instances in y by multiples of 24 dbu. Trial:i03.ug.leaf_0002.01 moved eight instances by ±24 dbu or ±72 dbu (all multiples of 24 dbu) and was accepted while touching M3, M4, M5, V3, and V4. Combine instance moves with endpoint resizing when the same repair must also fix a horizontal extent violation; trial:i03.ug.leaf_0002.01 applied its instance moves and the p937 endpoint resize in a single 10-op compound operation.

## Multi-Layer Operations Are Accepted

Repairs that touch multiple metal and via layers in one compound operation are accepted. Trial:i03.ug.leaf_0002.01 modified M3, M4, M5, V3, and V4 in a single 10-op operation and was gated in with connectivity preserved. Do not restrict operations to M5 alone when the root cause of a violation involves connected layers.

## Connectivity Preservation Is a Hard Gate

Every accepted repair preserved connectivity: conn_preserved is true in trial:i01.ug.leaf_0012.07, trial:i02.ug.leaf_0003.02, and trial:i03.ug.leaf_0002.01, and all three received decision "gated_in". Apply endpoint resizing that extends or maintains enclosure of attached via structures. Rule V4.M5.EN.2 requires 11 nm enclosure of V4 by M5 on two opposite sides; rule V4.M5.AUX.2 requires V4 width to exactly match M5 width in the direction perpendicular to M5 length. Retracting an M5 endpoint past the edge of a V4 or V5 via breaks these enclosure rules and severs connectivity.

## No-Bend Constraint (M5.AUX.3)

Rule M5.AUX.3 prohibits any M5 polygon from bending (no corners between 0° and 90°). All accepted repairs used only x-axis endpoint resizing, preserving the rectilinear, single-direction nature of M5 wires: trial:i01.ug.leaf_0012.07, trial:i02.ug.leaf_0003.02, trial:i03.ug.leaf_0002.01. Never introduce a bend by applying a resize that creates a non-axis-aligned edge or an L-shaped polygon on M5.