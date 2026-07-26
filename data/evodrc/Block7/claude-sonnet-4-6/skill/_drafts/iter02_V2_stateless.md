## Repair Operation Patterns

All four recorded trials for V2 resulted in `gated_in` decisions with `conn_preserved=true` and zero new violations introduced (`n_new_in_crop=0`, `n_new_out_of_crop=0`). Every repair that touched V2 also touched M2 and M3 in the same operation set (trial:i01.ug.Block7_union_row16.06, trial:i01.ug.leaf_0095.26, trial:i02.ug.leaf_0001.07, trial:i02.ug.leaf_0014.08). Never move a V2 instance in isolation; always co-move the enclosing M2 and M3 shapes in the same operation batch, because V2.AUX.1 (V2 must be inside M2 and M3), V2.M2.EN.1 (5 nm enclosure on opposite sides by M2), and V2.M3.EN.2 (5 nm enclosure on opposite sides by M3) are all sensitive to relative V2-to-metal displacement.

## Y-Axis Moves

Y-axis displacement is the dominant repair motion for V2. In trial:i02.ug.leaf_0001.07, a V2-touching instance and its co-located M3 polygon were both shifted by -57 dbu on the y-axis; in trial:i02.ug.leaf_0014.08, two instances and one polygon were shifted by -12 dbu on the y-axis. Both produced zero new violations. In trial:i01.ug.Block7_union_row16.06, a polygon move of -12 dbu on the y-axis accompanied instance moves on both x and y axes, also without introducing new violations. Apply y-axis co-moves to instance and polygon together, not to one without the other, as demonstrated in trial:i02.ug.leaf_0001.07 where both the instance (`i1643`) and its polygon (`p3383`) received the identical delta of -57 dbu.

## Resize-End Operations

trial:i01.ug.leaf_0095.26 is the only record containing `resize_end` operations on the y-axis (high-end extensions of +68 dbu and +48 dbu on polygons p2432 and p3537). This trial also touched M1, M2, M3, V1, and V2 simultaneously and passed without new violations. When a spacing or enclosure violation requires extending an adjacent metal end rather than translating the via, apply `resize_end` on the high end of the relevant polygon and pair it with any needed instance moves in the same operation batch, as shown in trial:i01.ug.leaf_0095.26.

## Enclosure Rules (V2.M2.EN.1, V2.M3.EN.2, V2.M3.AUX.2)

V2.M2.EN.1 requires M2 to enclose V2 by at least 5 nm on two opposite sides. V2.M3.EN.2 requires M3 to enclose V2 by 5 & 5 nm or 5 & 0 nm on two opposite sides. V2.M3.AUX.2 requires V2 to match the M3 width exactly in the direction perpendicular to M3 length. All successful repairs maintained M2 and M3 in the touched-layers set alongside V2 (trial:i01.ug.Block7_union_row16.06, trial:i01.ug.leaf_0095.26, trial:i02.ug.leaf_0001.07, trial:i02.ug.leaf_0014.08), confirming that adjusting V2 position without simultaneously adjusting M2/M3 would violate these enclosure constraints.

## Spacing Rules (V2.S.1 through V2.S.4)

V2.S.1 governs projection-based spacing: 18 nm on the same M3 track, 27 nm between parallel non-aligned tracks, and 18 nm between parallel aligned tracks. V2.S.2 sets a 23 nm euclidean corner-to-corner minimum for via pairs where both instances carry a 5 nm M3 end-cap (wec class). V2.S.3 sets a 30 nm euclidean corner-to-corner minimum where neither instance has a 5 nm end-cap (nec class). V2.S.4 sets a 27 nm euclidean corner-to-corner minimum for mixed wec/nec pairs. No trial produced new spacing violations; the consistent co-movement of M3 with V2 in all four trials keeps the mask geometry (v2_mask, v2_wec_mask, v2_nec_mask) coherent with the via positions so spacing checks remain satisfied.

## Width Rule (V2.W.1)

V2.W.1 requires a minimum width of 18 nm along the M3 length direction. No resize operation on V2 width was recorded in any trial; all width-relevant changes were confined to metal polygon end extensions (trial:i01.ug.leaf_0095.26). Do not shrink V2 width below 18 nm in any repair that modifies the M3 end geometry, since V2.M3.AUX.2 simultaneously constrains V2 to match the M3 width exactly.

## Connectivity Preservation

All four trials preserved connectivity (`conn_preserved=true`). The repair strategy of moving instances and their directly associated polygons by identical deltas on the same axis (trial:i02.ug.leaf_0001.07: instance i1643 and polygon p3383 both -57 dbu; trial:i02.ug.leaf_0014.08: instances i0519, i0524 and polygon p3515 all -12 dbu on y) maintains the topological relationship between via and metal without breaking nets. Always apply the same delta to every shape that forms the V2-M2-M3 stack at a given location.