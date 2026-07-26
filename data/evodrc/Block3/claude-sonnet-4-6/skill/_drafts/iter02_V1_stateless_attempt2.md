## Repair Operation Patterns

All 12 trials in iterations 1 and 2 were accepted (`decision: gated_in`, `conn_preserved: true`, zero new violations outside crop). Two distinct operation primitives appear: `move_instance` and `resize_end`. Repairs combine them or use `move_instance` alone; no trial uses `resize_end` alone.

## Paired Move-and-Resize: Direction and Magnitude

When an instance carrying V1 shapes is moved in the positive x-direction, a `resize_end` on the x-axis high-end of the corresponding M2 polygon is required in the same trial. In every accepted repair that pairs a positive-x move with a resize, the `resize_end` is applied to the high-x end — the same end toward which the instance moves — and the resize delta meets or exceeds the move delta (trial:i01.ug.Block3_union_row1.00: three instances moved +136 dbu, three polygon ends resized +192 dbu on x-high; trial:i01.ug.leaf_0007.05: move +36 dbu, resize +56 dbu x-high; trial:i01.ug.leaf_0012.08: move +72 dbu, resize +108 dbu x-high; trial:i02.ug.leaf_0002.01: move +104 dbu, resize +128 dbu x-high).

Do not apply `resize_end` to the opposite end from the movement direction: all accepted paired repairs set `end: high` for positive-x moves (trial:i01.ug.Block3_union_row1.00, trial:i01.ug.Block3_union_row8.03, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0012.08, trial:i02.ug.leaf_0002.01).

The resize delta must be large enough to close any pre-existing gap between the V1 edge and the M2 boundary on the advancing side. In trial:i01.ug.Block3_union_row1.00 the per-pair surplus is 56 dbu (192 − 136); in trial:i01.ug.Block3_union_row8.03 the surplus ranges from 20 to 56 dbu across the four pairs (164 − 108, 128 − 72, 128 − 72, 92 − 72). The variable surplus reflects different pre-existing enclosure margins at each site, consistent with V1.M2.EN.2's requirement that M2 enclose V1 on opposite sides.

## Move-Only Repairs (No Resize Required)

When the instance displacement is in the negative x-direction, no `resize_end` is needed. Trial:i01.ug.leaf_0013.09 moved instance i0023 by [−36, 0] dbu with no polygon resize and was accepted. Trial:i02.ug.leaf_0001.00 moved instance i0233 by [−36, 0] dbu with no polygon resize and was accepted. Negative-x displacement increases the high-x enclosure margin of the existing M2 polygon, so V1.M2.EN.2 is satisfied without extension.

Small positive-x moves also succeed without resize when the existing M2 enclosure on the advancing side already covers the displacement. Trial:i01.ug.Block3_union_row2.01 (two moves of +36 dbu each, no resize), trial:i01.ug.leaf_0006.04 (two moves of +36 dbu, no resize), and trial:i01.ug.leaf_0009.07 (one move of +36 dbu, no resize) were all accepted. Trial:i01.ug.Block3_union_row5.02 moved three instances +36 dbu and resized one polygon end +36 dbu (surplus = 0), indicating that a resize with delta equal to the move is sufficient when the enclosure margin is exactly zero before repair.

## Multi-Instance Coordinated Moves

When multiple instances in the same locus share a spacing violation, move all affected instances together in a single trial. Trial:i01.ug.Block3_union_row1.00 moved three instances (i0233, i0246, i0205) by the same delta [136, 0] and extended three corresponding M2 polygon ends (p1254, p1270, p1255) each by +192 dbu. Trial:i01.ug.Block3_union_row8.03 moved four instances with individual deltas (108, 72, 72, 72 dbu) and extended four M2 polygon ends with individual deltas (164, 128, 128, 92 dbu). Trial:i01.ug.Block3_union_row2.01 and trial:i01.ug.leaf_0006.04 each moved two instances together with no resize. Coordinating all co-located instances in one trial preserves inter-instance spacing (V1.S.1) while correcting the target violation.

## Y-Axis Resize

Trial:i01.ug.leaf_0008.06 included a `resize_end` on the y-axis (+20 dbu, y-high, polygon p1159) alongside an x-axis move (+136 dbu, instance i0047) and an x-axis resize (+92 dbu, x-high, polygon p1261). This trial also touched M3 in addition to M1, M2, and V1 — the only trial to span three metal layers. A y-axis resize on M2 is valid when needed to satisfy V1.M2.EN.2 enclosure in the orthogonal direction.

## Layer Scope

Every trial touched M1, M2, and V1 together. No trial modified V1 in isolation. Trial:i01.ug.leaf_0008.06 additionally touched M3, confirming that M2 adjustments can require updates to the layer above.