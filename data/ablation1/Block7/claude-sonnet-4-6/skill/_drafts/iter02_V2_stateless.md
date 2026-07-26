## Repair Operation Patterns

All accepted V2-touching trials in this layer's history use `move_instance` as the primary operation, with `resize_end` on connected M3 polygons as a secondary adjustment when needed. Every gated-in trial preserved connectivity (`conn_preserved=true`): trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row13.03, trial:i01.ug.Block7_union_row14.04, trial:i01.ug.Block7_union_row19.09, trial:i01.ug.Block7_union_row9.21, trial:i02.ug.Block7_union_row17.02, trial:i02.ug.leaf_0010.13, trial:i02.ug.leaf_0023.16, trial:i02.ug.leaf_0032.17. Connectivity preservation is a required condition for acceptance, but not sufficient on its own: trial:i02.cu.def:VIA_VIA23_1_3_36_36.00 preserved connectivity yet was rejected because it produced `delta_total=0` — no net reduction in violations across any window.

Do not issue a `resize_via_shape` targeting only a via cell's M3 shape to repair V2 violations. The sole attempt of this form (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00, `resize_via_shape` on `M3` layer of cell `VIA_VIA23_1_3_36_36`, `delta_dbu=-40` in Y) produced zero improvement across all five checked windows and was rejected.

## Multi-Layer Instance Moves

When a V2 violation is addressed by moving an instance, the accepted operations always move associated M2 and M3 instances in the same operation set. In trial:i01.ug.Block7_union_row12.02 nine operations spanning M1, M2, M3, V1, and V2 were bundled together. In trial:i02.ug.leaf_0010.13, the minimal accepted repair moved instance `i1358` by `[0,-36]` on layers M2/M3/V2 only — confirming that V2 moves are executed via the owning instance, not by directly repositioning a V2 polygon. Never attempt to move a V2 polygon in isolation from its enclosing M2 and M3 geometry, because V2.AUX.1 requires V2 to remain inside both M2 and M3, and V2.M3.AUX.2 requires V2 width to exactly match M3 width perpendicular to the M3 length direction.

## Move Delta Magnitudes and Axes

Accepted repairs use integer multiples of small grid steps. X-axis instance move deltas observed: 36 dbu (trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row9.21), 37 dbu (trial:i01.ug.Block7_union_row19.09), 40 dbu (trial:i01.ug.Block7_union_row13.03), 56 dbu (trial:i01.ug.Block7_union_row9.21), 108 dbu (trial:i01.ug.Block7_union_row9.21). Y-axis instance move deltas observed: 8 dbu (trial:i01.ug.Block7_union_row12.02), 12 dbu (trial:i01.ug.Block7_union_row14.04), 16 dbu (trial:i02.ug.leaf_0023.16), 36 dbu (trial:i02.ug.leaf_0010.13), 52 dbu (trial:i01.ug.Block7_union_row19.09, trial:i02.ug.leaf_0032.17), 57 dbu (trial:i02.ug.Block7_union_row17.02), 64 dbu (trial:i01.ug.Block7_union_row14.04). Moves in both positive and negative Y were accepted (trial:i01.ug.Block7_union_row19.09 moved `[0,-52]`, trial:i02.ug.leaf_0032.17 moved `[0,52]`). Moves in both positive and negative X were accepted (trial:i01.ug.Block7_union_row19.09 used both `[37,0]` and `[-37,0]` in the same trial).

## New Violations Introduced in Crop

The unit_gate channel accepts trials that introduce new in-crop violations provided connectivity is preserved and the trial passes the gate. Trial:i01.ug.Block7_union_row13.03 introduced 1 new in-crop violation and was gated in. Trial:i02.ug.leaf_0032.17 introduced 4 new in-crop violations and was still gated in. Do not reject a candidate repair solely because `n_new_in_crop > 0` in the unit_gate channel.

## M3 Polygon Resize Accompanying Instance Moves

Several accepted trials include `resize_end` operations on M3 polygons alongside instance moves, to maintain M3 end-cap geometry consistent with V2.M3.EN.2 and V2.M3.AUX.2 after the instance is repositioned. Trial:i01.ug.Block7_union_row12.02 resized M3 polygon `p3273` by `+56 dbu` on the x-high end after moving instances. Trial:i01.ug.Block7_union_row14.04 resized polygon `p3200` by `+48 dbu` on the x-high end. Trial:i01.ug.Block7_union_row13.03 resized `p3526` by `+4 dbu` on x-high. These adjustments are applied after the instance move, not independently. Apply `resize_end` on the connected M3 polygon when an instance move would otherwise leave a V2 without the required enclosure on two opposite sides (V2.M3.EN.2: at least 5 nm on one side, 0 nm or 5 nm on the opposite).

## End-Cap Classification and Spacing Rules

The spacing rules V2.S.1 through V2.S.4 depend on whether each V2 instance has a 5 nm M3 end-cap (WEC, with-end-cap) or no M3 end-cap (NEC, no-end-cap). A V2 is WEC when at least one of its edges does not coincide with an M3 edge — i.e., M3 extends beyond the V2 end. A V2 is NEC when all its edges are flush with M3 edges. This classification drives which spacing threshold applies:

- Two WEC instances: corner-to-corner minimum 23 nm (V2.S.2, euclidean check at 16.4 nm).
- Two NEC instances: corner-to-corner minimum 30 nm (V2.S.3, euclidean check at 16.12 nm).
- One WEC and one NEC instance: corner-to-corner minimum 27 nm (V2.S.4, euclidean check at 17.11 nm).
- Projection-based spacing (V2.S.1): same-track or aligned parallel-track minimum 18 nm; non-aligned parallel tracks minimum 27 nm.

When moving a V2 instance to resolve a spacing violation, determine whether the source and target instances are WEC or NEC before computing the required minimum separation. Trial:i02.ug.leaf_0010.13 moved instance `i1358` by `[0,-36]` on M2/M3/V2 layers, achieving separation within a compact locus of 126×60 dbu, consistent with resolving a same-track or aligned-track spacing violation where the 18 nm projection threshold applies.

## V2.M2.EN.1 — Enclosure by M2

V2 must be enclosed by M2 by at least 5 nm on two opposite sides. All accepted move operations keep the M2 instance co-moved with the V2 instance (confirmed in every multi-instance move trial where M2 appears in `touched_layers`). Do not move a V2-containing instance without also moving the M2 instance that encloses it, or the 5 nm M2 enclosure on two opposite sides required by V2.M2.EN.1 will be violated. In trial:i02.ug.leaf_0010.13, only M2/M3/V2 were touched and the single instance move `[0,-36]` was accepted — the M2 enclosure of V2 moved with the instance by construction.

## V2.W.1 — Minimum Width

The minimum V2 width along the M3 length direction is 18 nm. No trial in this history includes a resize of a V2 polygon's own width; all shape changes are on M3 or M2 polygons. V2 width is set by the via cell definition (e.g., `VIA_VIA23_1_3_36_36`). Avoid operations that shrink V2 width below 18 nm; the cu_pool attempt to resize the M3 shape of that via cell (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00) produced no improvement and was rejected.

## Geometry Constraints

All V2 shapes must be orthogonal (no edges with angles 1–89° or 91–179°). No non-orthogonal V2 geometry appears in any accepted trial. All observed move_instance and resize_end operations produce only axis-aligned delta vectors (all `delta_dbu` entries are `[int, 0]` or `[0, int]`, never diagonal), preserving orthogonality through every repair in this history.