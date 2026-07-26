## M2 Geometry Rules

**M2.W.1** sets the minimum M2 polygon width at 18 nm. **M2.A.1** sets the minimum M2 polygon area at 504 nm². Polygons below either threshold are independently flagged violations; they are separate checks.

All M2 edges must be strictly orthogonal (0° or 90°). The NONORTHOGONAL block applies to every drawing layer including M2; any angled edge is an immediate violation regardless of which rule family introduced it.

## M2 Spacing Rule Hierarchy

Spacing rules depend on the edge-length classification of the two interacting edges. The thresholds that separate rule applicability are 24 nm and 36 nm:

- Edges longer than 36 nm are "side" edges governed by **M2.S.1** (side-to-side, 18 nm minimum, both edges must exceed 36 nm) and by **M2.S.2** (tip-to-side, 25 nm minimum, when the opposing edge is ≤ 36 nm).
- Edges in the range [24 nm, 36 nm] are "wide tips" governed by **M2.S.3** (tip-to-tip between two wide tips, 27 nm minimum) and by **M2.S.5** (wide-tip to narrow-tip, 31 nm minimum).
- Edges shorter than 24 nm are "narrow tips" governed by **M2.S.4** (tip-to-tip between two narrow tips, 31 nm minimum).

**M2.S.6** adds a Euclidean corner-to-corner minimum of 20 nm, catching diagonal proximity that projection-based checks miss. It is triggered by pairs that pass the projection check but are still within 20 nm Euclidean distance.

## M2.S.7 and M2.S.8: Compound Spacing Constraints

**M2.S.7** prohibits the combination of an 18 nm tip-to-tip gap co-located with a side-to-side spacing ≤ 32 nm on the same pair of polygons. When side spacing is ≤ 32 nm, the parallel run length of the neighboring edges must be ≥ 35 nm. This is a two-part check: the deck uses both an interacting-polygon test and a bounding-box-width test (bboxwidth < 35 nm on the projection-space polygon).

**M2.S.8** governs diagonal spacing between tip-to-tip gap centers on different M2 tracks. Each 18 nm tip-to-tip gap is characterized by shrinking it 8.5 nm per side to find the center; the Euclidean distance between any two such centers on different tracks must be ≥ 80 nm. This rule catches staggered patterns where individual gaps are individually legal but their diagonal proximity creates a reliability concern.

## Via Enclosure Rules Involving M2

**V1.M2.EN.2** requires M2 to enclose V1 on two opposite sides. The legal enclosure patterns are 5 & 5 nm (both sides enclosed by ≥ 5 nm) or 5 & 0 nm (one side at exactly zero, flush coincidence). The deck checks for both the 5 nm minimum and the flush-edge case using `projection` distance. An edge of V1 that has no enclosure on its corresponding M2 side at all (not even flush) fails this rule.

**V1.M2.AUX.2** requires V1 to exactly match the M2 width along the direction perpendicular to M2 length. V1 edges must be coincident with M2 edges on both sides in that perpendicular direction; a V1 narrower or wider than the M2 stripe in that axis fails. The deck implements this by checking that each V1 has at least two coincident edges with M2 boundary edges.

**V2.M2.EN.1** requires M2 to enclose V2 by at least 5 nm on at least two opposite sides. The check is expressed as `m2.sized(-5.nm, 0)` and `m2.sized(0, -5.nm)` to test x- and y-direction enclosure independently; a V2 that fails both tests is flagged.

## Observed Operation Patterns

Instance moves on M2-bearing cells were performed at x-axis displacements of ±36 dbu and +72 dbu (trial:i02.ug.whole_design.00, trial:i04.ug.whole_design.00) and at y-axis displacements of ±24, ±48, +72, and +96 dbu (trial:i01.ug.whole_design.00). All such moves were accepted with no new M2 violations introduced (decision gated_in, conn_preserved=true, n_new_in_crop=0).

Polygon-level resizes on M2-adjacent shapes were performed in trial:i01.ug.whole_design.00: p879 was extended +48 dbu on its high-y end, and p910 was shifted +8 dbu in x and extended +20 dbu on its high-y end. Both were accepted without introducing new M2 violations.

The cu_pool trial trial:i04.cu.def:VIA_VIA23_1_3_36_36.00 targeted cell VIA_VIA23_1_3_36_36 and listed M2 among its touched layers while performing y-axis shrinks of -40 dbu on the M3 via shape and -64 dbu on polygons p891–p897. This reduced total violations by 8 (from 30 to 22). The M2 impact was indirect, through V2.M2.EN.1 sensitivity to the M3/V2 geometry within the via cell.

The iter 4 unit_gate trial (trial:i04.ug.whole_design.00) had assemble_drops for the same v2m3aux2_fix group, indicating those ops were already consumed by the cu_pool channel before the unit_gate assembly ran. No M2 violations were introduced or dropped by the unit_gate move set itself.