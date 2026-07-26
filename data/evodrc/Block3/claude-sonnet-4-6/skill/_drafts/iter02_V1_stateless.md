## Operation patterns across all accepted trials

Every trial in the measured history has `decision: "gated_in"` and `conn_preserved: true`, meaning each set of operations resolved violations without introducing new in-crop violations and without breaking connectivity. No rejected trials exist in this layer's history.

All accepted operations are translations in the x-direction only or resize_end extensions along the x-axis high end (or one y-axis high-end resize). The y-axis is touched exactly once across all trials (trial:i01.ug.leaf_0008.06, p1159 y high +20 dbu alongside an x-axis move and resize). All other moves are [±N, 0].

## V1 is never moved in isolation

Every accepted trial moves V1 instances by operating on instance moves that simultaneously displace M1, M2, and V1 together (`touched_layers` always includes all three). No operation type directly repositions a V1 polygon independently of its enclosing metal. This is required because V1.AUX.1 demands V1 remain inside both M1 and M2, and V1.M2.AUX.2 demands V1 width match M2 width perpendicular to M2 length; decoupled V1 movement would violate both rules. trial:i01.ug.Block3_union_row1.00, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0012.08, and all other trials confirm this co-move pattern.

## resize_end supplements move_instance when approaching the extended end

When a move_instance displaces an instance in +x, the M2 polygon at the high-x end of that instance is extended via resize_end on axis x, end high, by an amount that equals the move delta plus a surplus. The surplus represents the pre-existing enclosure deficit that must be closed to satisfy V1.M2.EN.2 (minimum M2 enclosure of V1 of 5 & 5 nm or 5 & 0 nm) and V1.M1.EN.1 (minimum M1 enclosure of V1 of 5 & 2 nm on opposite sides). Observed surplus values across trials vary from 20 dbu to 88 dbu, indicating each repair site carries its own enclosure gap:

- trial:i01.ug.Block3_union_row1.00: move 136 dbu, resize 192 dbu, surplus 56 dbu (three instance groups, same surplus each)
- trial:i01.ug.Block3_union_row8.03: i0017 move 108, resize 164, surplus 56; i0016/i0019 move 72, resize 128, surplus 56; i0021 move 72, resize 92, surplus 20
- trial:i01.ug.leaf_0007.05: move 36, resize 56, surplus 20
- trial:i01.ug.leaf_0008.06: instance i0047 move 136, resize 92 dbu — note the resize (92) is less than the move (136), suggesting the high-x enclosure was already partially present, and the surplus was negative by 44 dbu (the existing enclosure absorbed part of the displacement); this trial also applies a y-axis resize of +20 dbu on a separate polygon p1159
- trial:i01.ug.leaf_0012.08: move 72, resize 108, surplus 36
- trial:i02.ug.leaf_0002.01: move 104, resize 128, surplus 24

The resize_end must be applied on the same side as the direction of movement. When moving in +x, resize the high-x end. Resizing the low-x end after a +x move would violate V1.M2.AUX.2 by changing the width of M2 where it wraps V1 without adjusting V1 itself.

## Pure instance moves without resize are accepted when enclosure headroom is pre-existing

Several trials apply only move_instance operations with no accompanying resize_end and are accepted, confirming that resize_end is not always required:

- trial:i01.ug.Block3_union_row2.01: two instances moved +36 dbu, no resize
- trial:i01.ug.leaf_0006.04: two instances moved +36 dbu, no resize
- trial:i01.ug.leaf_0009.07: one instance moved +36 dbu, no resize
- trial:i01.ug.leaf_0013.09: one instance moved −36 dbu, no resize
- trial:i02.ug.leaf_0001.00: one instance moved −36 dbu, no resize

These cases share small absolute displacements (36 dbu) or negative-x direction. In the negative-x direction (trial:i01.ug.leaf_0013.09, trial:i02.ug.leaf_0001.00), moving toward the low-x end increases the distance from the high-x M2 edge to V1, which cannot worsen high-end V1.M2.EN.2 compliance, and the M2 low-x enclosure improves or is unaffected because the via moves toward that edge. No resize is therefore needed at either end.

## Spacing rules govern when multiple instances in the same locus are moved together

When a locus region contains multiple V1 instances on adjacent or parallel M2 tracks, all affected instances in that locus are moved within the same trial. trial:i01.ug.Block3_union_row1.00 moves three instances (i0233, i0246, i0205) by the same 136 dbu delta, each with its own resize_end. trial:i01.ug.Block3_union_row8.03 moves four instances with varying deltas (108, 72, 72, 72 dbu). Moving instances by differing amounts within the same locus, as in trial:i01.ug.Block3_union_row8.03, is accepted so long as the resulting inter-via spacing satisfies V1.S.1 (minimum 17–18 nm projection spacing depending on mask context), V1.S.2 (minimum 16.4 nm euclidean corner-to-corner for wec pairs), V1.S.3 (minimum 16.12 nm euclidean corner-to-corner for nec pairs), and V1.S.4 (minimum 17.11 nm euclidean separation between wec and nec masks). The accepted differential moves in trial:i01.ug.Block3_union_row8.03 (deltas spread from 72 to 108 dbu) confirm that non-uniform shifts within a locus do not automatically violate spacing rules when starting positions already provide margin.

## V1.W.1 minimum width is not disturbed by any observed operation

No trial applies a resize that reduces V1 width. All resize_end operations act on M1 or M2 polygons at their length-direction ends, not on V1 polygon width. V1.W.1 requires minimum width of 18 nm along the M2 length direction. Since V1 instances move rigidly and no resize contracts them, V1.W.1 compliance is maintained by the co-move strategy without explicit width checks. trial:i01.ug.Block3_union_row1.00 through trial:i02.ug.leaf_0002.01 all confirm zero new violations after operation.

## M3 co-involvement does not change V1 repair strategy

trial:i01.ug.leaf_0008.06 is the only trial with `touched_layers` including M3 in addition to M1, M2, V1. Its operations (resize_end on p1159 y high +20, move_instance i0239 by [4,0], move_instance i0047 by [136,0], resize_end p1261 x high +92) follow the same co-move-with-metal-extension pattern used across all other trials. The presence of M3 in the touched set does not alter V1-specific repair logic; it indicates an M3 polygon also required extension to preserve connectivity through the same locus. The trial was accepted with zero new in-crop violations, confirming that V1 repairs can proceed identically when upper metal layers are also adjusted within the same operation set.