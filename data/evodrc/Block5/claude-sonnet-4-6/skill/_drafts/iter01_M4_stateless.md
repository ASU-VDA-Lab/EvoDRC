## Width Constraints

M4 vertical (Y-axis) width must be exactly 24 nm or an odd multiple of 24 nm that does not also fall on a forbidden value. Rule M4.W.1 sets the floor at 24 nm; rule M4.W.2 caps vertical width at 480 nm. Rule M4.W.3 forbids vertical widths that are even integer multiples of 24 nm: 48, 96, 144, 192, 240, 288, 336, 384, 432, and 480 nm are all illegal. Rule M4.W.4 additionally forbids 72, 168, 264, 360, and 456 nm, which span an even number of routing tracks. The combined effect is that legal vertical widths form a restricted set; when sizing an M4 shape vertically, confirm the resulting height is not in either forbidden list before committing. Rule M4.W.5 independently sets the minimum horizontal (X-axis) width at 44 nm.

The single recorded repair moved instances by 24 nm and 72 nm steps along Y (trial:i01.ug.leaf_0010.07), consistent with the 24 nm minimum vertical width and the M4.AUX.1 requirement that horizontal edges lie on a 24 nm grid. All vertical move deltas in that trial are exact multiples of 24 nm.

## Grid and Track Alignment

Rule M4.AUX.1 requires every M4 horizontal edge to lie on a 24 nm Y-grid. Any vertical move of an M4-bearing instance must therefore be a nonzero integer multiple of 24 nm or the shape will violate AUX.1. In trial:i01.ug.leaf_0010.07, all six move operations use deltas of ±24 nm or ±72 nm (3×24), maintaining grid compliance.

Rule M4.AUX.2 applies to minimum-width M4 tracks (shapes that erode to nothing under a 13 nm Y-shrink). Their centerlines must land on Y positions satisfying `(cl - 48) mod 192 == 0`, where cl is in database units. The base constraint additionally requires the shape's bottom and top Y edges to be multiples of 96 dbu before the centerline check applies. When placing or repositioning a narrow M4 run, verify the centerline after moving: only offsets 48, 240, 432, 624, ... (mod 192) are legal.

## No-Bend Constraint

Rule M4.AUX.3 forbids any M4 polygon from having corners with an interior angle in the range 0°–90° (i.e., bends). M4 must be purely rectilinear and single-direction — no L-shapes, T-shapes, or jogs. Any repair that introduces a bend to route around a spacing violation creates an AUX.3 violation instead. The repair in trial:i01.ug.leaf_0010.07 used instance moves rather than shape modifications, which avoids introducing bends.

## Wide Shape Restrictions

Rule M4.AUX.4 forbids the horizontal (0°-angle) outer edges of any wide M4 polygon from coinciding with a routing track edge. Wide M4 is any polygon that survives the 13 nm Y-shrink (i.e., vertical height > 26 nm after merging). When expanding a narrow track into a wide pad or bus segment, the outer horizontal edges must not fall exactly on a track boundary.

## Spacing Constraints

**Vertical spacing (M4.S.1):** Minimum 24 nm between any two M4 polygon edges measured along Y (projection or Euclidean). Because the vertical width floor is also 24 nm, the combined pitch of a minimum-width M4 track plus minimum gap is 48 nm, which is also a forbidden width (M4.W.3). This means adjacent minimum-width tracks with exactly 24 nm of clearance are correct — the 48 nm forbidden value applies to a single polygon's height, not to pitch.

**Horizontal spacing (M4.S.2):** Minimum 40 nm between any two M4 vertical (90°) edges, Euclidean.

**Tip-to-tip on adjacent tracks (M4.S.3 / M4.S.4):** Both rules set 40 nm minimum tip-to-tip clearance between M4 shapes on adjacent horizontal tracks, whether or not the shapes share a parallel run length. The distinction between S.3 and S.4 is geometric (non-overlapping vs. overlapping projections), but the numeric limit is identical: 40 nm.

**Minimum parallel run (M4.S.5):** When two M4 shapes on adjacent tracks have a gap of 24–25 nm between their horizontal edges (i.e., they are at minimum vertical spacing), any region of parallel overlap must be at least 44 nm long measured horizontally. Parallel runs shorter than 44 nm at minimum spacing violate M4.S.5.

## Via Enclosure

Rule V3.M4.EN.2 requires M4 to enclose each V3 via by at least 11 nm on at least two opposite sides. Rule V4.M4.EN.1 imposes the same 11 nm two-opposite-side enclosure for V4 vias within M4. Both rules use the `sized(-11.nm, 0)` / `sized(0, -11.nm)` interacting pattern, so they fire when the via extends within 11 nm of the M4 edge in either X or Y independently.

Rule V3.M4.AUX.2 is a harder constraint: V3 must be exactly the same width as the M4 it sits inside in the direction perpendicular to the M4 run. V3 vias touching the M4 edge on at least two coincident edges satisfy this; any V3 that is narrower than M4 in the transverse direction and does not have two coincident-edge touches fails. In trial:i01.ug.leaf_0010.07, V3 and V4 were among the touched layers, confirming that vertical instance moves propagate changes to via enclosure simultaneously across both via levels.

## Repair Move Granularity and Pairing

In trial:i01.ug.leaf_0010.07, instances were moved in symmetrically paired groups: two instances received +72 nm, two received +24 nm, and two received -24 nm. All deltas are multiples of 24 nm. The repair was accepted (decision: gated_in) with connectivity preserved and three new violations introduced inside the crop window. This shows that a multi-instance move touching M3, M4, M5, V3, and V4 simultaneously can be accepted even when it generates new in-crop violations, provided connectivity is preserved.

The minimum safe move quantum for any M4-bearing instance along Y is 24 nm to satisfy M4.AUX.1. Moving by 72 nm (3×24) is also grid-legal. Moves of 48 nm, 96 nm, 144 nm, or other even-multiple-of-24 amounts are grid-legal per AUX.1 but must not produce a single M4 polygon whose resulting vertical height lands on a W.3 or W.4 forbidden value.

## Non-Orthogonal Geometry

The global GEOMETRY.NONORTHOGONAL block applies to M4. Any M4 edge that is not exactly horizontal (0°) or vertical (90°) is illegal. Shape editing, merging, or boolean operations that produce diagonal edges must be corrected before sign-off.