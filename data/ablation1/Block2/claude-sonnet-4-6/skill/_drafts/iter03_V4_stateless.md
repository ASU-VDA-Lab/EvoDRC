## Repair Operation Patterns

**Multi-layer coupling: V4 repairs always touch M4, M5, and adjacent via layers together.**
In trial:i03.ug.leaf_0002.01 the touched_layers set was ["M3","M4","M5","V3","V4"], confirming that correcting a V4 DRC violation required simultaneous adjustment of both bounding metal layers (M4 below and M5 above) and the adjacent via stack (V3). Do not attempt to repair V4 in isolation; any op set that modifies V4 geometry must also be evaluated against M4 and M5 and, where the via column continues, V3.

**Metal polygon resize on the x-axis is a valid enclosure repair primitive.**
In trial:i03.ug.leaf_0002.01 polygon p937 was widened on both x-axis ends (low end +64 dbu, high end +320 dbu) as part of the accepted repair. This asymmetric bilateral extension (low end smaller than high end) still satisfied V4.M4.EN.1 and V4.M5.EN.2, which require 11 nm enclosure on at least two opposite sides. When enclosure is short on both the low-x and high-x sides, growing both ends independently is acceptable; the minimum per-side extension needed to clear the 11 nm enclosure rule is 11 nm (110 dbu at 1 dbu = 0.1 nm). Extensions of 64 dbu (~6.4 nm) and 320 dbu (~32 nm) in trial:i03.ug.leaf_0002.01 indicate the repair addressed not just the minimum enclosure threshold but also downstream spacing margin or a coincident M5 width constraint from V4.M5.AUX.2.

**Y-axis instance moves fan outward symmetrically at two step sizes.**
In trial:i03.ug.leaf_0002.01 eight instances were displaced in Y in two magnitude bands: 72 dbu (~7.2 nm) applied to i0098/i0094 (positive) and i0066/i0069 (negative), and 24 dbu (~2.4 nm) applied to i0110/i0090 (positive) and i0061/i0070 (negative). The symmetrical fan pattern -- equal positive/negative pairs at each step size -- indicates the repair spread instances away from a central congestion point to satisfy the 33 nm projection-based spacing rules V4.S.1 and V4.S.2. The smaller 24 dbu moves address near-neighbor spacing violations while the larger 72 dbu moves address farther pairs, consistent with projection-mode spacing being sensitive to the shadow overlap of non-adjacent vias aligned along the same axis.

**conn_preserved=true is the operative gate-in condition when in-crop violations increase.**
Trial:i03.ug.leaf_0002.01 was accepted with decision "gated_in" despite introducing 2 new in-crop DRC violations (n_new_in_crop=2, n_new_out_of_crop=0). The stated reason was "conn_preserved". This means the gate logic accepts a net increase in local violations as long as connectivity is not broken. Do not treat a non-zero n_new_in_crop as grounds to discard a candidate op set; evaluate connectivity preservation first.

## Rule-Specific Constraints and Minimums

**V4.W.1 -- Minimum width 24 nm (240 dbu).**
The via must be at least 24 nm wide along the M5 length direction. No resize_end operation on a V4 polygon should produce a width below 240 dbu on the axis parallel to M5. In trial:i03.ug.leaf_0002.01 the resize operations were on the x-axis of a metal polygon (p937, identified as M4 or M5 context), not directly on a V4 instance, so width of the via itself was maintained by the enclosing metal geometry.

**V4.S.1 / V4.S.2 / V4.S.3 -- All spacing minimums are 33 nm, checked under three distinct geometric modes.**
Projection-mode (V4.S.1, V4.S.2) fires when two vias have overlapping shadows along a shared axis; Euclidean corner-to-corner (V4.S.3) fires when no projection overlap exists. The symmetrical Y-fan in trial:i03.ug.leaf_0002.01 addresses projection-mode violations between same-net (V4.S.1) or different-net (V4.S.2) via pairs. Moves that clear the projection check may expose a residual corner-to-corner violation under V4.S.3 if the diagonal distance falls below 33 nm; verify V4.S.3 after every Y or X translation repair pass.

**V4.M4.EN.1 / V4.M5.EN.2 -- 11 nm enclosure required on two opposite sides by both M4 and M5.**
Both rules use the same 11 nm threshold and the same two-opposite-sides logic (implemented via `sized(-11.nm, 0)` and `sized(0, -11.nm)` checks). A repair that grows the enclosing metal on one axis (x or y) must grow it enough on both the low and high ends of that axis to satisfy the opposite-sides requirement simultaneously. In trial:i03.ug.leaf_0002.01 p937 was extended on both x ends, consistent with this requirement.

**V4.AUX.1 -- V4 must lie entirely within the intersection of M4 and M5.**
Any move or resize that shifts a V4 instance must keep the via footprint inside both M4 and M5. In trial:i03.ug.leaf_0002.01 the repair moved M4/M5 metal (polygon p937) rather than moving the via itself, which is the correct direction of repair when the via is at risk of falling outside a metal boundary -- expand the metal to cover the via, not the reverse.

**V4.M5.AUX.2 -- V4 width along the axis perpendicular to M5 length must exactly match M5 width on that axis, with two coincident edges required.**
This rule is stricter than the enclosure rules: the via edges must be coincident with the M5 edges (not merely enclosed). When resizing M5 (or a polygon on M5's layer) in x as in trial:i03.ug.leaf_0002.01, the corresponding V4 instance edges on x must also be set to match the new M5 boundary. Asymmetric metal extension (64 dbu low, 320 dbu high in trial:i03.ug.leaf_0002.01) will produce a V4.M5.AUX.2 violation unless the V4 polygon x-extents are updated to the same new M5 edge positions.

**GEOMETRY.NONORTHOGONAL -- All V4 edges must be strictly horizontal or vertical.**
V4 is included in the nonorthogonal block check. No repair op should introduce diagonal edges on V4 polygons. Resize operations that move a single end on one axis (as in trial:i03.ug.leaf_0002.01, axis="x", end="low"/"high") are safe because they move one rectilinear edge at a time and cannot introduce angular edges, provided the polygon was already orthogonal.

## Gating and Op-Count Context

The accepted trial in this layer's history (trial:i03.ug.leaf_0002.01) used 10 ops across five layers in a unit_gate channel for Block2 at iteration 3. The op mix was 8 move_instance and 2 resize_end. The repair was accepted in a context where 2 new in-crop violations were introduced, indicating the gating policy for V4 in the unit_gate channel at iter 3 tolerates localized violation increase when connectivity is maintained.