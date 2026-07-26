## Geometry constraints

M3 edges must be strictly orthogonal. The NONORTHOGONAL check flags any edge whose angle falls outside {0°, 90°, 180°, 270°}. No trial in this layer's history generated or left non-orthogonal M3 edges; every resize and move operation recorded in trial:i01.ug.whole_design.00 and trial:i04.cu.def:VIA_VIA23_1_3_36_36.00 operated on axis-aligned endpoints only, consistent with this constraint.

## Width and area floors

M3.W.1 requires every M3 polygon to be at least 18 nm wide. M3.A.1 requires every M3 polygon to carry at least 504 nm² of area. In trial:i04.cu.def:VIA_VIA23_1_3_36_36.00, the repair engine shrank seven M3 polygons (p891–p897) by 64 dbu along the y-axis and shrank the M3 shape inside cell VIA_VIA23_1_3_36_36 by 40 dbu along y. These shrinks were accepted and applied (decision: "applied"), which confirms that the resulting geometries still satisfied both the 18 nm width floor and the 504 nm² area floor after the reductions. Do not shrink an M3 polygon below 18 nm on any axis, and verify that area remains ≥ 504 nm² after any resize.

## Spacing rules

M3.S.1 governs side-to-side spacing: both edges must be longer than 36 nm and must be separated by at least 18 nm. M3.S.2 governs tip-to-side spacing: when one edge is ≤ 36 nm and the opposing edge is > 36 nm, the required separation is 25 nm. M3.S.3 governs tip-to-tip spacing when both edges fall in the 24–36 nm range: the minimum is 27 nm. M3.S.5 governs tip-to-tip spacing when one edge is in the 24–36 nm range and the other is below 24 nm: the minimum is 31 nm. M3.S.4 governs tip-to-tip spacing when both edges are below 24 nm: the minimum is also 31 nm. M3.S.6 adds a Euclidean corner-to-corner floor of 20 nm that catches diagonal proximity not caught by projection-based checks.

In trial:i04.cu.def:VIA_VIA23_1_3_36_36.00, the y-axis shrinks applied to p891–p897 reduced the y-extent of those polygons. The trial was accepted without introducing new spacing violations, confirming that the shrunken shapes cleared all six spacing rules in their context. When shortening a polygon tip (reducing a tip edge), the tip-to-tip and tip-to-side rules (M3.S.2–M3.S.5) become easier to satisfy on the shortened axis, but the reduction also changes which edge-length bracket the tip falls into; always recheck which of M3.S.3, M3.S.4, or M3.S.5 applies after a tip resize.

## V2.M3.AUX.2: via-width matching

V2.M3.AUX.2 requires that every V2 via be exactly the same width as its enclosing M3 polygon measured perpendicular to the M3 length direction. Violation of this rule was the explicit repair target in trial:i04.cu.def:VIA_VIA23_1_3_36_36.00 (group label "v2m3aux2_fix"). The fix shrank the M3 shape inside the via cell by 40 dbu along y (resize_via_shape op on cell VIA_VIA23_1_3_36_36, layer M3) and simultaneously shrank the surrounding M3 routing polygons p891–p897 by 64 dbu along the same axis. This co-reduction of both the cell-internal M3 shape and the connected routing polygons resolved 8 violations (window went from 30 to 22). The repair must be applied symmetrically: changing only the via cell shape without matching the routing polygon width, or vice versa, leaves the width-mismatch intact. Always adjust the M3 shape inside the via cell and the abutting M3 routing shapes together when correcting V2.M3.AUX.2.

## V2.M3.EN.2: V2 enclosure by M3

V2.M3.EN.2 requires M3 to enclose V2 by at least 5 nm on two opposite sides (either left+right or top+bottom), with the second side allowed to be 0 nm only when the first side is ≥ 5 nm. The via-cell M3 resize in trial:i04.cu.def:VIA_VIA23_1_3_36_36.00 modified the same M3 shape that must provide this enclosure; the trial was accepted, confirming that the 40 dbu y-shrink left sufficient enclosure on the remaining axes. When shrinking via-cell M3 shapes to fix V2.M3.AUX.2, verify that at least one pair of opposite sides retains ≥ 5 nm enclosure over V2 after the reduction.

## V3.M3.EN.1: V3 enclosure by M3

V3.M3.EN.1 requires M3 to enclose V3 by at least 5 nm on at least one pair of opposite sides (either left+right via a 5 nm horizontal inset, or top+bottom via a 5 nm vertical inset). The history records no V3.M3.EN.1 violations or targeted repairs in trial:i01.ug.whole_design.00 or trial:i04.cu.def:VIA_VIA23_1_3_36_36.00. Instance moves that shift M3 routing relative to fixed V3 positions can bring enclosure margins close to the 5 nm boundary; verify V3 enclosure after any M3 instance move or polygon resize that touches a via landing.

## Trial disposition summary

trial:i01.ug.whole_design.00 (iter 1) was gated in rather than applied; it touched M3 among other layers but produced no net violation reduction credited to M3. trial:i04.cu.def:VIA_VIA23_1_3_36_36.00 (iter 4) was applied and reduced total violations by 8, targeting V2.M3.AUX.2 through coordinated y-axis shrinks of both the via-cell M3 shape and seven connected M3 routing polygons.