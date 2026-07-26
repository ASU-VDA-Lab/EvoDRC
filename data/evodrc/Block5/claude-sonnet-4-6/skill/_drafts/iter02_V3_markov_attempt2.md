Now I have everything I need. Let me produce the updated knowledge body.

## Repair Operation Observations

Measured repairs combine `move_instance` and direct polygon `move` operations. trial:i01.ug.leaf_0010.07 used exclusively `move_instance` operations; trial:i02.ug.leaf_0002.01 used seven `move_instance` operations alongside one polygon move (`move` on polygon p879, axis x, delta +32 dbu). No resize or geometry-edit operations appear in the ops lists of either trial; a resize on p879 (y, +96 dbu) that appears in the assemble_drops for trial:i02.ug.leaf_0002.01 carries reason `cu_pool:applied`, meaning it was applied by the cu_pool coordinator outside this trial's op sequence and is not a repair op attributed to this trial.

## Move Direction

trial:i01.ug.leaf_0010.07 applied purely Y-direction moves (x-component = 0 for all six ops). trial:i02.ug.leaf_0002.01 applied mixed X+Y moves: i0114 [+32, 0], i0112 [+32, −48], i0073 [+32, +96], i0062 [+32, +48], i0105 [0, −48], i0075 [0, +96], i0076 [0, +48]. Both X-only and mixed X+Y instance moves are established repair directions for V3-touching violations.

## Multi-Instance Coordinated Moves

In trial:i01.ug.leaf_0010.07, six instances were moved in one batch across three paired Y-deltas (+72 dbu for i0113 and i0099, +24 dbu for i0001 and i0002, −24 dbu for i0067 and i0070). In trial:i02.ug.leaf_0002.01, seven instances plus one polygon were moved with varying X and Y components. Both trials touched M3, M4, M5, V3, and V4 simultaneously. Do not treat V3 violations in isolation from M3/M4 context; repair moves applied to parent metal layers propagate into V3 spacing and enclosure metrics across rules V3.S.1, V3.M3.EN.1, V3.M4.EN.2, and V3.M4.AUX.2.

## Gating Criteria

Both measured trials were accepted (`decision: gated_in`) with `conn_preserved: true` and `n_new_out_of_crop: 0` (trial:i01.ug.leaf_0010.07, trial:i02.ug.leaf_0002.01). trial:i01.ug.leaf_0010.07 introduced 3 new in-crop violations and was still accepted. trial:i02.ug.leaf_0002.01 introduced 0 new in-crop violations and was accepted. Connectivity preservation is a necessary condition for acceptance; avoid any move sequence that breaks connectivity even if it would otherwise resolve V3 DRC errors. Zero new in-crop violations is achievable with coordinated mixed-axis moves as shown by trial:i02.ug.leaf_0002.01.

## Rule V3.W.1 (Minimum Width 18 nm)

V3 minimum width along the M4 length direction is 18 nm. The measured repairs (trial:i01.ug.leaf_0010.07, trial:i02.ug.leaf_0002.01) moved M3/M4/M5 parent layers touching V3 without altering V3 shape geometry. Width along M4 length is determined by the V3 shape itself, not by the enclosing metal position, so instance moves and polygon positional moves alone do not alter V3.W.1 compliance directly. Width violations require geometry changes to the V3 shape rather than moves.

## Rules V3.S.1 / V3.S.2 / V3.S.3 / V3.S.4 (Spacing Rules)

V3 spacing rules depend on whether instances carry a 5 nm M4 end-cap (full-flush-M4 condition). The DRC deck classifies V3 shapes as `v3_nec` (no end-cap, fully coincident with M4 edges) or `v3_wec` (with end-cap, having non-coincident edges). Minimum projection spacings differ: same-track or aligned parallel-track V3 spacing is 18 nm (V3.S.1), corner-to-corner spacing for two wec instances is 23 nm (V3.S.2), for two nec instances is 30 nm (V3.S.3), and for a mixed wec/nec pair is 27 nm (V3.S.4). In trial:i01.ug.leaf_0010.07, Y-direction moves of M4-touching instances altered inter-via separations and produced 3 new in-crop violations while clearing out-of-crop violations. In trial:i02.ug.leaf_0002.01, mixed X+Y moves cleared violations with 0 new violations introduced, demonstrating that coordinated multi-axis displacement can resolve V3 spacing errors without creating new ones.

## Rule V3.M3.EN.1 (M3 Enclosure 5 nm on Opposite Sides)

V3 must be enclosed by M3 by at least 5 nm on at least one pair of opposite sides (left+right OR top+bottom, as implemented by `v3.inside(m3.sized(-5.nm, 0))` and `v3.inside(m3.sized(0, -5.nm))`). In both trial:i01.ug.leaf_0010.07 and trial:i02.ug.leaf_0002.01, M3 was moved together with M4 and V3 (touched_layers includes M3 in both); coordinated layer moves preserve the relative M3-to-V3 overlap. Never move V3 or M3 independently in a way that reduces enclosure below 5 nm on both axis pairs simultaneously, as this triggers V3.M3.EN.1.

## Rule V3.M4.EN.2 (M4 Enclosure 11 nm on Opposite Sides)

V3 must be enclosed by M4 by at least 11 nm on at least one pair of opposite sides. The deck checks this with `m4.sized(-11.nm, 0)` and `m4.sized(0, -11.nm)`. In trial:i01.ug.leaf_0010.07, M4 and V3-carrying instances were moved by equal Y-deltas, preserving M4 enclosure. In trial:i02.ug.leaf_0002.01, M4 and V3-carrying instances were moved by matching mixed X+Y deltas, likewise preserving enclosure. Apply equal delta moves in both axes to M4 and V3 instance groups to maintain V3.M4.EN.2 compliance.

## Rule V3.AUX.1 (V3 Inside M3 AND M4)

V3 must be fully inside the intersection of M3 and M4. In both trial:i01.ug.leaf_0010.07 and trial:i02.ug.leaf_0002.01, M3, M4, and V3 were all moved together (touched_layers includes all three in both trials), keeping V3 within the moving metal overlap region. Never displace V3 without moving its enclosing M3 and M4 shapes by the same delta, or V3.AUX.1 will fire.

## Rule V3.M4.AUX.2 (V3 Width Matches M4 Width)

V3 must be exactly the same width as M4 in the direction perpendicular to the M4 length. The DRC check requires at least two coincident edges between V3 and M4. In trial:i01.ug.leaf_0010.07, moves were in Y only and all V3-touching instances were moved by matching deltas paired with their M4 parents; in trial:i02.ug.leaf_0002.01, mixed X+Y moves were applied consistently to V3-touching instances and their M4 parents. Both trials preserved the edge coincidence that V3.M4.AUX.2 requires. Resize operations on M4 that change its perpendicular width without a matching resize of V3 will violate V3.M4.AUX.2.

## Nonorthogonal Geometry

All V3 edges must be strictly orthogonal (0 or 90 degrees). trial:i01.ug.leaf_0010.07 used move_instance operations with integer dbu Y-offsets (+72, +24, −24 dbu). trial:i02.ug.leaf_0002.01 used move_instance and polygon move operations with integer dbu X and Y offsets (+32, −48, +96, +48, 0 dbu components). All measured repair deltas are integer dbu values, which preserve the orthogonality of all moved geometry. Never introduce diagonal edges or fractional-coordinate placements when repairing V3 violations.