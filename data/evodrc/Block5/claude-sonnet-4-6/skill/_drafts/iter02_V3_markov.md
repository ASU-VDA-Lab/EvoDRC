## Repair Operation Observations

Measured repairs use `move_instance` operations; no shape-resize or geometry-edit operations appear in the V3-touching history for this layer. Moves may be purely in the Y direction or may include combined X and Y components: trial:i01.ug.leaf_0010.07 used Y-only deltas (+72, +24, -24 dbu), while trial:i02.ug.leaf_0002.01 used both X and Y components across instance moves ([32,0], [32,-48], [32,96], [32,48], [0,-48], [0,96], [0,48] dbu). Combined X+Y repositioning is used when spacing violations span both axes. Polygon-level move ops (e.g., `move polygon_id`) may be proposed alongside move_instance ops but can be dropped by the assembler due to cu_pool conflicts (trial:i02.ug.leaf_0002.01); the effective repair is carried by the surviving move_instance ops.

## Multi-Instance Coordinated Moves

Both measured trials applied multi-instance moves in a single repair batch with touched layers M3, M4, M5, V3, and V4. In trial:i01.ug.leaf_0010.07, moves were paired with three shared delta values (+72, +24, -24 dbu Y-only across six instances). In trial:i02.ug.leaf_0002.01, seven instances received non-uniform deltas with varied X and Y components across the batch. Do not treat V3 violations in isolation from M3/M4 context; repair moves applied to parent metal layers propagate into V3 spacing and enclosure metrics across rules V3.S.1, V3.M3.EN.1, V3.M4.EN.2, and V3.M4.AUX.2.

## Gating Criteria

Both accepted trials share `conn_preserved: true` and `n_new_out_of_crop: 0` (trial:i01.ug.leaf_0010.07, trial:i02.ug.leaf_0002.01). trial:i01.ug.leaf_0010.07 introduced 3 new in-crop violations and was still accepted; trial:i02.ug.leaf_0002.01 introduced 0 new in-crop violations. Connectivity preservation and zero new out-of-crop violations are both required for acceptance. Non-zero new in-crop violations do not block acceptance when the above two conditions hold.

## Rule V3.W.1 (Minimum Width 18 nm)

V3 minimum width along the M4 length direction is 18 nm. Both measured repairs (trial:i01.ug.leaf_0010.07, trial:i02.ug.leaf_0002.01) addressed V3-touching violations via instance moves without altering V3 shape geometry. Width along M4 length is determined by the V3 shape itself, not by the enclosing metal position, so instance moves alone do not alter V3.W.1 compliance directly. Width violations require geometry changes to the V3 shape rather than moves.

## Rules V3.S.1 / V3.S.2 / V3.S.3 / V3.S.4 (Spacing Rules)

V3 spacing rules depend on whether instances carry a 5 nm M4 end-cap (full-flush-M4 condition). The DRC deck classifies V3 shapes as `v3_nec` (no end-cap, fully coincident with M4 edges) or `v3_wec` (with end-cap, having non-coincident edges). Minimum projection spacings: same-track or aligned parallel-track spacing is 18 nm (V3.S.1); corner-to-corner spacing for two wec instances is 23 nm (V3.S.2); for two nec instances is 30 nm (V3.S.3); for a mixed wec/nec pair is 27 nm (V3.S.4). In trial:i01.ug.leaf_0010.07, Y-only moves altered inter-via separations and produced 3 new in-crop violations while clearing out-of-crop violations; moves that close spacing on one axis can open violations on another. In trial:i02.ug.leaf_0002.01, non-uniform X+Y deltas across seven instances produced 0 new in-crop violations; assigning varied per-instance deltas across the batch can resolve spacing violations on both axes simultaneously without introducing new ones.

## Rule V3.M3.EN.1 (M3 Enclosure 5 nm on Opposite Sides)

V3 must be enclosed by M3 by at least 5 nm on at least one pair of opposite sides (left+right OR top+bottom, as implemented by `v3.inside(m3.sized(-5.nm, 0))` and `v3.inside(m3.sized(0, -5.nm))`). Both measured trials (trial:i01.ug.leaf_0010.07, trial:i02.ug.leaf_0002.01) moved M3 along with M4 and V3 together (touched_layers includes M3, M4, V3 in both); coordinated layer moves preserve the relative M3-to-V3 overlap. Never move V3 or M3 independently in a way that reduces enclosure below 5 nm on both axis pairs simultaneously, as this triggers V3.M3.EN.1.

## Rule V3.M4.EN.2 (M4 Enclosure 11 nm on Opposite Sides)

V3 must be enclosed by M4 by at least 11 nm on at least one pair of opposite sides. The deck checks this with `m4.sized(-11.nm, 0)` and `m4.sized(0, -11.nm)`. Both measured trials (trial:i01.ug.leaf_0010.07, trial:i02.ug.leaf_0002.01) moved M4 with the same per-instance delta as the V3-carrying shapes, maintaining the M4 enclosure relationship through the repair. Apply equal per-instance deltas to M4 and V3 instance groups to preserve V3.M4.EN.2 compliance.

## Rule V3.AUX.1 (V3 Inside M3 AND M4)

V3 must be fully inside the intersection of M3 and M4. In both measured trials (trial:i01.ug.leaf_0010.07, trial:i02.ug.leaf_0002.01), M3, M4, and V3 were all moved together (touched_layers includes all three), keeping V3 within the moving metal overlap region. Never displace V3 without moving its enclosing M3 and M4 shapes by the same delta, or V3.AUX.1 will fire.

## Rule V3.M4.AUX.2 (V3 Width Matches M4 Width)

V3 must be exactly the same width as M4 in the direction perpendicular to the M4 length; the DRC check requires at least two coincident edges between V3 and M4. In both measured trials (trial:i01.ug.leaf_0010.07, trial:i02.ug.leaf_0002.01), all V3-touching instances were moved by matching deltas paired with their M4 parents, preserving the edge coincidence that V3.M4.AUX.2 requires. Resize operations on M4 that change its perpendicular width without a matching resize of V3 will violate V3.M4.AUX.2.

## Nonorthogonal Geometry

All V3 edges must be strictly orthogonal (0 or 90 degrees). Both measured repairs (trial:i01.ug.leaf_0010.07, trial:i02.ug.leaf_0002.01) used only move_instance operations with integer dbu offsets, which preserve the orthogonality of all moved geometry. Never introduce diagonal edges or fractional-coordinate placements when repairing V3 violations.