## Geometry Constraints

**M6.W.1 / M6.W.2 / M6.W.3 / M6.W.4:** M6 vertical (Y-direction) width has a minimum of 32 nm, a maximum of 640 nm, and is forbidden at every even-integer multiple of 32 nm (64, 128, 192, 256, 320, 384, 448, 512, 576, 640 nm per M6.W.3) and at widths that cause the polygon to span an even number of 32 nm routing tracks vertically (96, 224, 352, 480, 608 nm per M6.W.4). The permitted vertical width values are therefore those in the range [32, 640] nm that are neither even multiples of 32 nm nor in the M6.W.4 prohibited set — for example 32, 48, 80, 112, 144, 160, 176 nm, etc.

**M6.W.5:** M6 horizontal (X-direction) width minimum is 44 nm.

**M6.AUX.3:** M6 polygons must be strictly rectilinear with no bends (no convex 0–90° corners). Any L-shape, T-shape, or non-straight segment on M6 triggers this rule.

**GEOMETRY.NONORTHOGONAL:** All M6 edges must be exactly horizontal (0°) or vertical (90°). Diagonal edges are unconditionally prohibited.

## Grid and Track Alignment

**M6.AUX.1:** Every horizontal (0°) M6 edge must land on a 32 nm Y-grid. Any vertical resize or shape move that places a horizontal M6 edge off this grid fires M6.AUX.1.

**M6.AUX.2:** Minimum-width M6 tracks (those not wide enough to survive a ±17 nm vertical erosion-dilation) must have their centerline on the routing track grid: Y-pitch 256 dbu, offset 64 dbu from origin, restricted to polygons whose bottom and top are on a 128 dbu base grid. Violations occur when the centerline of a 1× (minimum-width) M6 wire does not satisfy `(centerline − 64) mod 256 == 0` in database units.

**M6.AUX.4:** Wide M6 polygons (those that survive a ±17 nm vertical erosion-dilation) must not have any horizontal outer edge co-incident with the horizontal band of any separate minimum-width M6 track's edges. When a wide M6 polygon's horizontal edge falls on the same Y-coordinate as a 1× M6 routing track edge, M6.AUX.4 fires.

## Spacing Rules

**M6.S.1:** Minimum vertical spacing between any two M6 shapes is 32 nm, checked both by projection (for facing edges) and globally (point-to-point). Vertical gaps tighter than 32 nm fire unconditionally regardless of edge length.

**M6.S.2:** Minimum horizontal spacing between M6 shapes is 40 nm, measured along the 90° (horizontal) direction. Polygons on different horizontal tracks whose facing vertical edges are closer than 40 nm violate this rule.

**M6.S.3:** For two M6 polygons on adjacent vertical tracks that do not share a parallel run length, the tip-to-tip horizontal spacing must be at least 40 nm. The check is activated via a 48 nm vertical dilation to detect near-misses.

**M6.S.4:** For two M6 polygons on adjacent vertical tracks that do share a parallel run length (facing horizontal edges within 32 nm+1 dbu of each other), the tip-to-tip horizontal spacing must still be at least 40 nm. The gap region is extended laterally 1000 nm to identify wings, then checked with a 40 nm vertical dilation.

**M6.S.5:** When two M6 polygons are on adjacent vertical tracks (Y-gap ≤ 32 nm), their shared parallel run length along X must be at least 44 nm. Sub-44 nm overlaps on adjacent tracks fire M6.S.5.

## Via Enclosure Rules

**V5.M6.EN.2:** Every V5 via that lands inside M6 must be enclosed by M6 by at least 11 nm on two opposite sides (both X and Y). The rule fires on vias where M6 fails to surround them with an 11 nm border in either the X or Y direction.

**V5.M6.AUX.2:** V5 must be exactly flush with M6 in the direction perpendicular to the M6 run direction. V5 edges must be co-incident with M6 edges on at least two sides; any V5 not fully inside M6, or inside M6 without two coincident edges, violates this rule.

**V6.M6.EN.1:** Every V6 via inside M6 must be enclosed by M6 by at least 11 nm on at least two opposite sides, identical in structure to V5.M6.EN.2.

## Observed Repair Behavior

In trial:i01.ug.leaf_0025.11 (Block4, unit_gate channel), moving two instances (i0234, i0305) by +64 dbu in the Y direction produced a repair decision of `gated_in` with `conn_preserved: true`. The move touched layers M5, M6, and V5, and introduced 9 new DRC markers within the crop locus ([1728, 2068, 13168, 13052]) while producing 0 new markers outside the crop. The repair was accepted despite the new in-crop markers because connectivity was preserved.

The 64 dbu Y-displacement in trial:i01.ug.leaf_0025.11 is exactly one-quarter of the M6.AUX.2 track pitch (256 dbu), corresponding to a 32 nm shift — exactly the M6 minimum vertical width (M6.W.1) and the M6.AUX.1 horizontal-edge grid step. Instance moves at multiples of 32 nm (the M6 grid unit) are therefore consistent with maintaining M6.AUX.1 grid compliance on any M6 edges attached to the moved instances, as demonstrated by trial:i01.ug.leaf_0025.11.