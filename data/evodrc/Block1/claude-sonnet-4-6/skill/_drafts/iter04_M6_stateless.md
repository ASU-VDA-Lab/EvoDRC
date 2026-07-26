**M6.AUX.1 — Horizontal edges must lie on the 32 nm vertical grid**

M6.AUX.1 fires when any horizontal M6 edge has a y-coordinate that is not a multiple of 32 dbu. In trial:i02.ug.leaf_0003.02 one M6.AUX.1 violation was cleared by y-axis polygon moves: p1561 by −96 dbu, p1562 by −112 dbu, and p1563 by −64 dbu; the move delta need not itself be a multiple of 32 — what matters is the final edge position. In trial:i02.ug.leaf_0004.03 the same single M6.AUX.1 violation was cleared by moving polygon p1561 by +32 dbu in y.

Apply the exact y-delta required to snap every affected horizontal edge to the nearest multiple of 32 dbu (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03). Do not introduce a y-delta that leaves any other horizontal edge of the same polygon off-grid.

**M6.AUX.3 — M6 may not bend**

M6.AUX.3 fires when an M6 polygon contains a corner whose interior angle falls in [0°, 90°], i.e., the polygon deviates from a strictly rectilinear shape. In trial:i02.ug.leaf_0003.02, 7 M6.AUX.3 violations were cleared through a combination of x-axis instance moves (+32 dbu or −16 dbu applied to all instances in the locus) and the same polygon y-moves that also fixed M6.AUX.1. In trial:i02.ug.leaf_0004.03 the same 7 M6.AUX.3 violations were cleared by analogous x-axis instance moves together with a single polygon y-move on p1561 (+32 dbu).

Correct M6.AUX.3 by moving the contributing instance(s) so that shared M6 boundary edges at cell interfaces become collinear and the bend is eliminated (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03). All M6 polygons must be axis-aligned rectangles or rectilinear polygons with no diagonal or bent segments. When a bend is created by a placement offset between adjacent instances, an x-axis instance move of +32 dbu or −16 dbu at the affected boundary is the demonstrated repair pattern.

**M6.AUX.2 — Minimum-width M6 tracks must align to horizontal routing tracks**

M6.AUX.2 requires that minimum-width M6 tracks (those that do not survive bilateral y-erosion of 17 dbu) have their center lines at positions satisfying (cl − 64) mod 256 == 0, restricted to shapes whose vertical extents are multiples of 128 dbu. No M6.AUX.2 violations appear in trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03, or trial:i04.ug.leaf_0003.02; the rule has not been triggered in the recorded history.

**M6.AUX.4 — Wide M6 polygon outside edges may not touch a routing track edge**

M6.AUX.4 fires when a wide M6 polygon (surviving bilateral y-erosion of 17 dbu) has a horizontal outside edge coincident with a routing track edge defined by the nearest minimum-width track. No M6.AUX.4 violations appear in trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03, or trial:i04.ug.leaf_0003.02.

**M6.W rules — Width constraints**

No M6.W.1 (minimum vertical width 32 nm), M6.W.2 (maximum vertical width 640 nm), M6.W.3 (vertical width must not be an even integer multiple of 32 nm), M6.W.4 (vertical width must not span an even number of minimum-width routing tracks), or M6.W.5 (minimum horizontal width 44 nm) violations appear in trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03, or trial:i04.ug.leaf_0003.02.

**M6.S rules — Spacing constraints**

No M6.S.1 (minimum vertical spacing 32 nm), M6.S.2 (minimum horizontal spacing 40 nm), M6.S.3 (minimum tip-to-tip spacing on adjacent tracks without shared parallel run 40 nm), M6.S.4 (minimum tip-to-tip spacing on adjacent tracks with shared parallel run 40 nm), or M6.S.5 (minimum parallel run length on adjacent tracks 44 nm) violations appear in trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03, or trial:i04.ug.leaf_0003.02.

**V5.M6.EN.2, V5.M6.AUX.2, and V6.M6.EN.1 — Via enclosure**

No V5.M6.EN.2 (V5 enclosure by M6 ≥ 11 nm on two opposite sides), V5.M6.AUX.2 (V5 width must match M6 width perpendicular to M6 length), or V6.M6.EN.1 (V6 enclosure by M6 ≥ 11 nm on at least two opposite sides) violations appear in trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03, or trial:i04.ug.leaf_0003.02. V5 and V6 are moved alongside M6 in all three trials (via instance moves that displace the entire cell), preserving enclosure relationships.

**M6.GEOMETRY.NONORTHOGONAL**

No nonorthogonal edge violations on M6 appear in any recorded trial. The nonorthogonal block applies to all layers; M6 must have only horizontal and vertical edges (angles 0° and 90°). The recorded repair operations use only x-axis or y-axis moves and never introduce diagonal geometry.

**Multi-leaf conflict resolution at the assemble stage**

When two leaf agents propose moves for the same instance with different delta vectors, the assemble stage drops one operation. In the assembly of trial:i02.ug.leaf_0003.02, 26 instance-move ops were dropped as "external_conflict_dropped" because leaf_0004 had claimed the same instances with conflicting y-components; the retained ops used x-only deltas of +32 dbu or −16 dbu. In the assembly of trial:i02.ug.leaf_0004.03, 40 ops were dropped — the majority as "external_conflict_dropped" (y-components differed between leaves), three polygon moves as "cross_crop_first_wins" (leaf_0003 had already applied those polygon moves), and several as "external_duplicate" (both leaves proposed identical x-only deltas, one copy retained). Despite these drops, both assemblies achieved conn_preserved=true and zero new out-of-crop violations (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03).

Instance moves that include a y-component at cross-crop boundaries are routinely dropped when the adjacent leaf has claimed the same instance (trial:i02.ug.leaf_0004.03). Restrict instance moves at cross-crop boundaries to the x-axis when M6.AUX.3 or M6.AUX.1 repair is the goal; pure x-axis moves survive the assemble filter and deliver the observed violation reductions.

**Iteration 4 pattern**

Trial:i04.ug.leaf_0003.02 (iter 4) cleared 8 new in-crop violations across the touched layers M3, M4, M5, M6, V3, V4, V5 using 26 instance-move ops and no polygon-level moves. The ops consisted of 12 moves of +32 dbu in x, 12 moves of −16 dbu in x, and two diagonal moves ([+32, −96] for i0345 and [−16, −96] for i0505). The per-rule breakdown is absent from the iter-4 record, so the M6-specific contribution within the 8 cleared violations cannot be isolated beyond the touched-layers declaration. The x-axis magnitudes (+32 dbu, −16 dbu) match exactly the pattern used in iter 2 (trial:i02.ug.leaf_0003.02), confirming these step sizes as the operative repair quanta for this locus.