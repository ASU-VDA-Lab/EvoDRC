## Width (M3.W.1)

M3.W.1 flags M3 polygons narrower than 18 nm in any dimension.

## Spacing Classification (M3.S.1–M3.S.5)

The spacing rules classify each participating edge by length to select the applicable minimum gap:

- M3.S.1 (18 nm): both edges > 36 nm (side-to-side, projection).
- M3.S.2 (25 nm): one edge ≤ 36 nm, the other > 36 nm (tip-to-side, projection).
- M3.S.3 (27 nm): both edges 24–36 nm (wide-tip-to-wide-tip, projection).
- M3.S.5 (31 nm): one edge 24–36 nm, the other < 24 nm (wide-tip-to-narrow-tip, projection).
- M3.S.4 (31 nm): both edges < 24 nm (narrow-tip-to-narrow-tip, projection).

Identifying which rule fired on a given spacing error depends on measuring both facing edge lengths independently, since the five rules share overlapping edge-length ranges at their boundaries.

## Corner Spacing (M3.S.6)

M3.S.6 targets polygon pairs whose corners come within 20 nm by euclidean distance but whose edges do not form a projection-detectable overlap. The rule is computed as polygons violating 20 nm euclidean space minus those that also violate 20 nm projection space, isolating pure corner-proximity cases that the projection-based rules leave undetected.

## Area (M3.A.1)

M3.A.1 flags any M3 polygon with area below 504 nm². Small fragments left after Boolean operations are common sources of this violation.

## V2 Enclosure by M3 (V2.M3.EN.2, V2.M3.AUX.2)

V2.M3.EN.2 checks that M3 encloses V2 by at least 5 nm on two opposite sides; the asymmetric 5 & 0 nm configuration (one side flush) is also acceptable. V2.M3.AUX.2 checks separately that V2's width in the direction perpendicular to the M3 wire length exactly equals M3's width in that direction; neither a narrower nor a wider via satisfies this check.

In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, via shapes in cell VIA_VIA23_1_3_36_36 were widened along the x-axis: shape 0 was moved −144 dbu and resized +288 dbu, shape 1 was resized +288 dbu, and shape 2 was moved +144 dbu and resized +288 dbu (all V2 layer operations). The repair was applied and reduced the total DRC count by 27 across units leaf_0018 (−15) and leaf_0019 (−12), with M2, M3, and V2 as the touched layers. The symmetric move-plus-resize pattern kept the via center fixed while expanding the via extent in x, indicating the original via width was below the M3 enclosure or width-match threshold on that axis (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). Because the fix targeted the via cell definition rather than individual instances, it resolved violations across all placements of that cell simultaneously (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

## V3 Enclosure by M3 (V3.M3.EN.1)

V3.M3.EN.1 checks that each V3 is fully inside either the horizontally-eroded M3 (m3.sized(−5 nm, 0)) or the vertically-eroded M3 (m3.sized(0, −5 nm)). A V3 passes when M3 extends at least 5 nm beyond the V3 boundary on both the left and right sides, or at least 5 nm on both the top and bottom sides; satisfaction on one axis is sufficient. V3 instances that fail both orientations, or lie entirely outside M3, are flagged.

## Non-Orthogonal Geometry (NONORTHOGONAL)

M3 edges at any angle other than 0°, 90°, 180°, or 270° trigger a NONORTHOGONAL violation. This check applies to all M3 drawing edges.

## Observed Repair History

**trial:i01.cu.def:VIA_VIA23_1_3_36_36.00** (channel: cu\_pool, applied, −27 total DRC): All five operations were x-axis via shape moves and resizes on V2 shapes within cell VIA\_VIA23\_1\_3\_36\_36. Touched layers: M2, M3, V2. Net reduction: 15 violations in unit leaf\_0018, 12 in unit leaf\_0019. The cell-level repair propagated the fix to every instance placement.

**trial:i01.ug.leaf\_0008.06** (channel: unit\_gate, gated\_in, not applied): Included a y-axis resize of M3 polygon p1159 (high-end +20 dbu) and an x-axis resize of M3 polygon p1261 (high-end +92 dbu), combined with instance moves of i0239 (+4 dbu x) and i0047 (+136 dbu x). The trial was gated out under the conn\_preserved decision — no DRC reduction was recorded for the crop window and connectivity was already intact. Touched layers: M1, M2, M3, V1.