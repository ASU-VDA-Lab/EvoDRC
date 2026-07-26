## Operation Mechanics

All 11 trials across both iterations — trial:i01.ug.Block3_union_row1.00 through trial:i02.ug.leaf_0001.00 — produced `decision: gated_in` with `n_new_in_crop: 0` and `n_new_out_of_crop: 0`. Every repair accepted by the channel introduced zero new V1 violations. The complete set of operations observed is: `move_instance` and `resize_end` (axis: x, end: high). No y-axis moves or resize operations on the y-axis appear in any trial.

## Move-Instance on the X-Axis

Every `move_instance` delta is of the form `[±N, 0]` with N ∈ {36, 72, 108} dbu. No trial carries a nonzero y-component in any instance move (trial:i01.ug.Block3_union_row1.00, trial:i01.ug.Block3_union_row2.01, trial:i01.ug.Block3_union_row5.02, trial:i01.ug.Block3_union_row8.03, trial:i01.ug.leaf_0006.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0008.06, trial:i01.ug.leaf_0009.07, trial:i01.ug.leaf_0012.08, trial:i01.ug.leaf_0013.09, trial:i02.ug.leaf_0001.00). V1 spacing violations on V1 (V1.S.1 through V1.S.4) are resolved exclusively by horizontal (x-axis) instance displacement. Never apply a y-axis move to resolve a V1 spacing violation — the full history contains no such operation and none was needed.

The minimum nonzero x-displacement applied is 36 dbu (trial:i01.ug.Block3_union_row2.01, trial:i01.ug.leaf_0009.07, and others). Larger displacements of 72 dbu (trial:i02.ug.leaf_0001.00) and 108 dbu (trial:i01.ug.Block3_union_row1.00, trial:i01.ug.Block3_union_row8.03) also resolve violations cleanly. All observed deltas are integer multiples of 36 dbu; do not attempt sub-grid moves.

One trial uses a negative x-displacement: trial:i01.ug.leaf_0013.09 moves instance i0023 by `[-36, 0]`. This confirms that moving an instance leftward (toward lower x) is a valid repair direction and does not introduce new violations when the gap on the lower-x side is sufficient.

## Compound Ops: Move + Resize-End

Two trials combine a `move_instance` with a `resize_end` on the same polygon (p1261): trial:i01.ug.leaf_0008.06 (move i0047 by [36,0], resize_end p1261 axis:x end:high delta:36) and trial:i02.ug.leaf_0001.00 (move i0047 by [72,0], resize_end p1261 axis:x end:high delta:72). In both cases the resize delta equals the instance move delta, and both trials were accepted with zero new violations. This pattern — extending the high-x endpoint of the M2 wire by the same amount as the via displacement — preserves M2 enclosure of V1 (V1.M2.EN.2) and the M2 width constraint (V1.M2.AUX.2) when a via is shifted rightward. Do not move a via rightward along M2 without also extending the M2 high-x end by the same delta; failing to do so risks violating V1.M2.EN.2 or V1.AUX.1.

The `resize_end` operation as observed is always `axis: x, end: high` — the high-x (rightward) end of the M2 segment is extended. No `end: low` or `axis: y` resize appears in the history. When a via moves in the positive-x direction, use a matching high-x resize on the M2 polygon; no such paired operation is needed for negative-x moves in the observed data (trial:i01.ug.leaf_0013.09 uses a negative move with no resize and still passes).

## Multi-Instance Co-Moves

Trials move between 1 and 4 instances in a single operation set. trial:i01.ug.Block3_union_row8.03 moves 4 instances simultaneously (i0016 by [36,0], i0017 by [108,0], i0019 by [36,0], i0021 by [36,0]) with a mixed-delta pattern, and the result is gated in with zero new violations. trial:i01.ug.Block3_union_row1.00 similarly uses non-uniform deltas within a single trial ([36,0] and [108,0]). Co-moving multiple instances with different displacement magnitudes is valid and does not inherently produce new V1 violations; what matters is that each instance lands in a legal position relative to its neighbors.

## Connectivity Preservation

All 11 trials report `conn_preserved: true`. Every combination of move_instance and resize_end applied in this history preserved signal connectivity. When composing a move + M2-resize as in trial:i01.ug.leaf_0008.06 and trial:i02.ug.leaf_0001.00, the resize is necessary precisely to maintain the M2 conductor spanning the via so that the connection is not broken.

## Iteration-State Transition

The design_state hash is `fa7319...` for all 10 iter:1 trials (trial:i01.ug.Block3_union_row1.00 through trial:i01.ug.leaf_0013.09) and transitions to `8472bf...` for the single iter:2 trial (trial:i02.ug.leaf_0001.00). The iter:2 trial operates on the already-repaired layout from iter:1 and still resolves its violation cleanly. The larger delta used in iter:2 (72 dbu for both move and resize on p1261/i0047, versus 36 dbu for the same polygon in trial:i01.ug.leaf_0008.06) reflects that the iter:1 partial repair moved the violation constraint, requiring a larger correction in iter:2.

## Layer Interaction

All trials in this history touch layers M1, M2, and V1 together (`touched_layers: ["M1","M2","V1"]` in every record). V1 repairs are not isolated to V1 geometry alone — M1 and M2 are always co-modified, consistent with V1.AUX.1 (V1 must be inside both M1 and M2) and V1.M1.EN.1/V1.M2.EN.2 (enclosure requirements on both surrounding metal layers). Do not attempt to repair a V1 DRC violation by modifying only V1 without also adjusting the enclosing M1 and M2 context.