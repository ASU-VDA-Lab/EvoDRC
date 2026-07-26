## Rule Summaries and Geometric Constraints

**M4.W.1 — Minimum vertical (y-axis) width: 24 nm.**
Polygons narrower than 24 nm in the vertical direction violate M4.W.1. The rule fires on horizontal projection edges only (`with_angle(0)`).

**M4.W.2 — Maximum vertical width: 480 nm.**
Any M4 polygon that survives `sized(0, -240.nm).sized(0, 240.nm)` is too tall; maximum vertical span is 480 nm.

**M4.W.3 — Forbidden even-multiple vertical widths.**
Vertical widths that are exact even integer multiples of the 24 nm minimum (48, 96, 144, 192, 240, 288, 336, 384, 432, 480 nm) are forbidden. The rule is checked via vertical projection edges whose length exactly equals one of those values, and via horizontal polygon bounding-box heights matching the same set.

**M4.W.4 — Additional forbidden vertical widths spanning even routing-track counts.**
Widths of 72, 168, 264, 360, and 456 nm are also disallowed. These correspond to polygon heights that span an even number of minimum-width routing tracks.

**M4.W.5 — Minimum horizontal (x-axis) width: 44 nm.**
The Euclidean width check fires on edges at 90°; polygons narrower than 44 nm in the x-direction violate M4.W.5.

**M4.S.1 — Minimum vertical spacing: 24 nm.**
Both a projection-based and a Euclidean check cover vertical separation. The projection check fires on edges at 0°; a catch-all Euclidean pass handles any cases the projection check misses.

**M4.S.2 — Minimum horizontal spacing: 40 nm.**
Vertical edges (90°) must be separated by at least 40 nm in the Euclidean sense.

**M4.S.3 / M4.S.4 — Tip-to-tip spacing on adjacent tracks: 40 nm.**
Both rules check tip-to-tip clearance between vertical M4 edges that are on adjacent tracks. S.3 applies when there is no shared parallel run length; S.4 applies when there is a shared run length. The tip region is defined by extending vertical edges 30 nm beyond each endpoint; only the portion of the extension that lies outside M4 and that interacts with other M4 edges is checked.

**M4.S.5 — Minimum parallel run length: 44 nm.**
When two M4 polygons on adjacent tracks share a parallel run, the run must be at least 44 nm long (checked via horizontal projection).

**M4.AUX.1 — Horizontal edge grid: 24 nm.**
Every horizontal M4 edge must have its y-coordinate on the 24 nm grid relative to the database origin (`ongrid(1.dbu, 24.nm)`).

**M4.AUX.2 — Minimum-width track centering.**
Minimum-width M4 tracks (strips not wider than 24 nm after the erosion/dilation probe) must be centered on horizontal routing tracks spaced at 192 dbu pitch with a 48 dbu offset from the origin. The centerline must satisfy `(cl - 48) % 192 == 0` in dbu.

**M4.AUX.3 — No bends.**
M4 polygons may not contain corners in the 0–90° range, meaning all angles must be strictly 90° (orthogonal Manhattan shapes only). Any polygon with a non-right-angle corner triggers this rule.

**M4.AUX.4 — Wide polygon edges must not touch routing track edges.**
Wide M4 polygons (wider than 24 nm in the y-direction after the erosion probe) may not have their horizontal (0°) edges collinear with the horizontal edges of adjacent minimum-width tracks. The check extends minimum-width track edge bands across the full canvas and tests for intersection.

**V3.M4.EN.2 — V3 enclosure by M4: 11 nm on at least two opposite sides.**
M4 must enclose every V3 via by at least 11 nm on both the left and right sides (x-axis) or both the top and bottom sides (y-axis). A V3 that fails both the `sized(-11.nm, 0)` and the `sized(0, -11.nm)` containment tests triggers this rule.

**V3.M4.AUX.2 — V3 must match M4 width perpendicular to M4 length.**
V3 vias inside M4 must have at least two of their edges coincident with M4 edges. V3 polygons not fully inside M4, or inside M4 but lacking two coincident edges, both fail.

**V4.M4.EN.1 — V4 enclosure by M4: 11 nm on at least two opposite sides.**
Same enclosure logic as V3.M4.EN.2 applies to V4, but only for V4 vias that are already inside M4 (`v4.inside(m4)`).

**GEOMETRY.NONORTHOGONAL — No non-orthogonal edges.**
Any M4 edge whose angle is in [1..89], [91..179], [-179..-91], or [-89..-1] degrees triggers the global nonorthogonal check.

## Observed Operation Behavior

**X-axis high-end extension accepted with no new violations.**
In trial:i02.ug.Block1_union_row12.00, polygon p1216 had its high x-end extended by +132 dbu. The operation was gated in with zero new in-crop or out-of-crop violations and with connectivity fully preserved. This confirms that an x-axis extension of this magnitude, in this locus region ([3980, 14400] to [9312, 14708]), does not intrinsically conflict with M4.S.2, M4.S.3, M4.S.4, M4.W.5, or V3.M4.EN.2 when the surrounding geometry provides adequate horizontal clearance and enclosure margin (trial:i02.ug.Block1_union_row12.00).