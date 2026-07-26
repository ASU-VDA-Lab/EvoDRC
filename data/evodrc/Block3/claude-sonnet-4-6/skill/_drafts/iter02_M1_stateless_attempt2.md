## Operation Types Observed on M1

All accepted trials apply one or more of: `move_instance` (translating a cell instance along x), `resize_end` (extending one edge of an M1 polygon), or both in combination. All 12 trials across iterations 1 and 2 carry `conn_preserved: true` and `n_new_in_crop: 0`, `n_new_out_of_crop: 0`, confirming that each accepted operation set introduced no new M1 DRC violations within crop boundaries (trial:i01.ug.Block3_union_row1.00 through trial:i02.ug.leaf_0002.01).

## resize_end: Always Extend the High End

Every `resize_end` operation recorded for M1 uses `end: "high"`. Never use `end: "low"` on an M1 polygon. The complete set of resize_end occurrences — trial:i01.ug.Block3_union_row1.00 (three high-x extensions), trial:i01.ug.Block3_union_row5.02 (one high-x extension), trial:i01.ug.Block3_union_row8.03 (four high-x extensions), trial:i01.ug.leaf_0007.05 (two high-x extensions), trial:i01.ug.leaf_0008.06 (one high-y and one high-x extension), trial:i01.ug.leaf_0012.08 (one high-x extension), trial:i02.ug.leaf_0002.01 (one high-x extension) — all use `end: "high"`. Do not retract the low end of an M1 polygon as a repair strategy; the measured record contains no accepted trial that reduces the low-end extent (trial:i01.ug.Block3_union_row1.00 through trial:i02.ug.leaf_0002.01).

## Pairing move_instance with resize_end

When a move_instance displaces an M1 instance along x, pair it with a resize_end on the same axis at `end: "high"` with a delta equal to or greater than the move delta. In trial:i01.ug.Block3_union_row1.00, instances moved +136 dbu while associated polygon high ends were extended +192 dbu. In trial:i01.ug.leaf_0007.05, instances moved +36 dbu while high ends were extended +56 dbu. In trial:i01.ug.leaf_0012.08, the instance moved +72 dbu and the polygon high end was extended +108 dbu. In trial:i02.ug.leaf_0002.01, the instance moved +104 dbu and the high end was extended +128 dbu. In trial:i01.ug.Block3_union_row5.02, move and resize deltas were equal at +36 dbu. In trial:i01.ug.Block3_union_row8.03, instance moves of +72–108 dbu were paired with resize_end deltas of +92–164 dbu. No accepted trial sets the resize_end delta below the corresponding move_instance delta.

## Move-Only Operations

Some units require only `move_instance` with no accompanying resize_end. Apply move-only repairs when M1 polygon geometry is already compliant and only cell placement requires adjustment. trial:i01.ug.Block3_union_row2.01, trial:i01.ug.leaf_0006.04, trial:i01.ug.leaf_0009.07, and trial:i01.ug.leaf_0013.09 each consist entirely of move_instance operations and were accepted with no new violations.

## Move Direction on X

Do not restrict move_instance delta to positive x only. trial:i01.ug.leaf_0013.09 uses delta_dbu [-36, 0] and trial:i02.ug.leaf_0001.00 uses delta_dbu [-36, 0]; both were accepted with `conn_preserved: true` and zero new violations. Move direction is determined by the geometry context, not by a sign convention.

## Multi-Axis Repair

trial:i01.ug.leaf_0008.06 applies a y-axis resize_end (axis:y, end:high, +20 dbu) alongside an x-axis resize_end and move_instance in the same operation batch, touching M1, M2, M3, and V1. Apply resize_end on axis:y at end:"high" when M1 enclosure along the vertical direction is deficient, consistent with the two-opposite-sides enclosure requirements in V0.M1.EN.1 and V1.M1.EN.1 (trial:i01.ug.leaf_0008.06).

## Co-Modified Layers

M1 repair operations consistently co-modify M2 and V1. Every trial in the history lists at least M1, M2, and V1 in touched_layers (trial:i01.ug.Block3_union_row1.00 through trial:i02.ug.leaf_0002.01). trial:i01.ug.leaf_0008.06 additionally includes M3. Treat V1 and M2 as co-repair layers whenever M1 geometry is adjusted; include their modifications in the same operation batch to preserve connectivity.