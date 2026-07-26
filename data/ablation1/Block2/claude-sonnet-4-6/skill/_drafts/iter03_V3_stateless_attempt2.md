## V3.W.1 — Minimum Width

The minimum width of a V3 instance along the M4 length direction is 18 nm. Trial:i03.ug.leaf_0002.01 resized both x-axis ends of polygon p937 while V3 remained in touched_layers and the result was gated_in, confirming that width constraints were satisfied after the resize.

## V3.S.1 — Minimum Spacing

V3 spacing requirements are context-dependent based on end-cap classification. Instances on the same M4 track require at least 18 nm projection spacing; instances on parallel M4 tracks that are not aligned require at least 27 nm projection spacing; instances on parallel M4 tracks that are aligned require at least 18 nm projection spacing. The DRC deck constructs separate v3_nec (no end-cap, fully flush with M4 edges) and v3_wec (with end-cap, not fully flush) masks before applying the projection checks. Trial:i03.ug.leaf_0002.01 moved eight instances across M3, M4, M5, V3, and V4 and was gated_in, confirming that V3.S.1 constraints were satisfied in the resulting configuration.

## V3.S.2 — Corner-to-Corner Spacing, Both with End-Cap

When both V3 instances carry a 5 nm M4 end-cap (v3_wec class), the minimum Euclidean corner-to-corner spacing is 23 nm. The rule isolates true diagonal violations by retaining only Euclidean hits that do not interact with their projection equivalents. Trial:i03.ug.leaf_0002.01 was gated_in across all V3 and V4 operations, confirming no V3.S.2 violation was introduced by those adjustments.

## V3.S.3 — Corner-to-Corner Spacing, Both without End-Cap

When both V3 instances lack a 5 nm M4 end-cap (v3_nec class), the minimum Euclidean corner-to-corner spacing is 30 nm. The deck applies a 5 nm isotropic sizing to v3_nec_mask before performing the Euclidean check. Trial:i03.ug.leaf_0002.01 accepted all V3 operations under gated_in without introducing V3.S.3 violations.

## V3.S.4 — Corner-to-Corner Spacing, Mixed End-Cap

When one V3 instance has and one lacks a 5 nm M4 end-cap, the minimum Euclidean corner-to-corner separation between their respective masks (v3_wec_mask to v3_nec_mask) is 27 nm. Trial:i03.ug.leaf_0002.01 confirmed no V3.S.4 error in the gated_in outcome.

## V3.M3.EN.1 — M3 Enclosure

M3 must enclose V3 by at least 5 nm on at least one pair of opposite sides. The deck tests horizontal enclosure via `inside(m3.sized(-5.nm, 0))` and vertical enclosure via `inside(m3.sized(0, -5.nm))`; a V3 that fails both checks triggers the violation. Trial:i03.ug.leaf_0002.01 touched M3 and V3 in the same operation set and the gated_in result confirms that the move operations preserved adequate M3 enclosure on at least one opposite-side pair for every V3 in the crop.

## V3.M4.EN.2 — M4 Enclosure

M4 must enclose V3 by at least 11 nm on at least one pair of opposite sides, checked via `m4.sized(-11.nm, 0)` for horizontal pairs and `m4.sized(0, -11.nm)` for vertical pairs. When resizing M4-related polygons, both resize deltas must leave at least 11 nm between each V3 edge and the corresponding M4 boundary. Trial:i03.ug.leaf_0002.01 applied resize_end to both ends of p937 along the x-axis while V3 was in touched_layers; the gated_in result confirms the resize did not violate V3.M4.EN.2.

## V3.AUX.1 — V3 Must Lie Inside M3 and M4

Every V3 instance must lie entirely within the intersection of M3 and M4. Any move or resize operation that exposes a V3 edge outside either metal layer produces a V3.AUX.1 violation. Trial:i03.ug.leaf_0002.01 modified M3, M4, and V3 together and was gated_in, confirming that the combined adjustments kept all V3 geometry within both metal regions.

## V3.M4.AUX.2 — V3 Width Must Match M4 Width

A V3 instance inside M4 must have at least two edges coincident with M4 edges, one on each lateral side perpendicular to the M4 length, so that the V3 width exactly equals the M4 width in that direction. This is enforced by `v3_aux2_coinc = v3_aux2_in.edges.and(m4.edges)` followed by `interacting(v3_aux2_coinc, 2)`. Trial:i03.ug.leaf_0002.01 performed resize_end on both x-axis ends of p937 while V3 remained in touched_layers; the gated_in result confirms that after resizing, V3 continued to satisfy the two-coincident-edge requirement with M4.

## GEOMETRY.NONORTHOGONAL — Rectilinear Constraint

All V3 edges must be strictly horizontal or vertical. Edges at any angle in the ranges 1°–89°, 91°–179°, −179°–−91°, or −89°–−1° trigger a GEOMETRY.NONORTHOGONAL violation. Trial:i03.ug.leaf_0002.01 applied resize_end along the x-axis and move_instance operations to V3-containing instances; the gated_in outcome confirms that these operation types preserve orthogonal V3 geometry.