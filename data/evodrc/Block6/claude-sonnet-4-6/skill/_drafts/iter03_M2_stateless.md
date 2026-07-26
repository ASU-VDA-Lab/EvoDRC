## Repair Operation Repertoire

Every M2-touching repair in the measured history uses either `move_instance` or `resize_end` exclusively along the X axis; no Y-axis displacement or Y-axis resize has been recorded for M2 in any trial (trial:i01.ug.Block6_union_row3.00, trial:i01.ug.Block6_union_row5.01, trial:i01.ug.Block6_union_row7.02, trial:i01.ug.Block6_union_row8.03, trial:i01.ug.leaf_0001.04, trial:i01.ug.leaf_0011.05, trial:i01.ug.leaf_0015.06, trial:i01.ug.leaf_0018.07, trial:i02.ug.Block6_union_row4.00, trial:i02.ug.Block6_union_row7.01, trial:i02.ug.Block6_union_row8.02, trial:i02.ug.leaf_0004.04, trial:i03.ug.leaf_0001.00). Do not apply Y-axis moves or resizes to M2 polygons or instances containing M2.

All M2-touching trials in the unit_gate channel carry `conn_preserved: true` and report `n_new_in_crop: 0` and `n_new_out_of_crop: 0`, confirming that X-only move and resize operations do not introduce new M2 violations when the connectivity gate accepts the result.

## Move-Instance Granularity

The measured X deltas span a wide range: 4 dbu (trial:i02.ug.Block6_union_row7.01), 8 dbu (trial:i02.ug.Block6_union_row8.02), 28 dbu (trial:i01.ug.leaf_0015.06), 36 dbu (trial:i01.ug.Block6_union_row8.03, trial:i01.ug.leaf_0011.05, trial:i01.ug.leaf_0018.07, trial:i02.ug.Block6_union_row8.02, trial:i03.ug.leaf_0001.00), 72 dbu (trial:i01.ug.Block6_union_row3.00, trial:i02.ug.leaf_0004.04), 104 dbu (trial:i01.ug.Block6_union_row7.02), and 112 dbu (trial:i01.ug.leaf_0001.04). Fine adjustments at 4–8 dbu are sufficient when the design state is close to compliance (trial:i02.ug.Block6_union_row7.01, trial:i02.ug.Block6_union_row8.02); coarser moves at 72–112 dbu are applied when greater positional correction is required (trial:i01.ug.Block6_union_row3.00, trial:i01.ug.leaf_0001.04). Start with the smallest move that resolves the measured gap before trying larger offsets.

All recorded `move_instance` X deltas are positive (rightward). No leftward instance move has been applied to M2 in any accepted trial; the one negative delta in the dataset (trial:i01.ug.Block6_union_row7.02, instance i0074, delta [-36,0]) is paired with a co-located resize_end on polygon p1920 that extends the low end by +56 dbu, making the net geometric effect on the wire extension still rightward/positive.

## resize_end Operations

`resize_end` on M2 polygons always targets the X axis and always applies a positive delta. The recorded end targets are `end:high` (trial:i01.ug.Block6_union_row5.01 +92 on p2072; trial:i01.ug.Block6_union_row7.02 +124 on p1903; trial:i01.ug.leaf_0001.04 +132 on p2016; trial:i01.ug.leaf_0015.06 +48 on p1923; trial:i02.ug.Block6_union_row4.00 +132 on p2020) and `end:low` (trial:i01.ug.Block6_union_row7.02 +56 on p1920). The `end:low` with a positive delta extends the polygon leftward (lower X boundary moves further left). Extending the high or low end of an M2 wire by these amounts did not introduce new violations in any accepted trial, confirming that elongating wires within this range is safe when the resulting geometry satisfies M2.S.1 side spacing (18 nm min for edges > 36 nm) and M2.S.7 parallel-run-length requirements (run length >= 35 nm when side spacing <= 32 nm).

When a `move_instance` and `resize_end` are co-applied within a single trial, they address separate geometry: the instance move corrects inter-wire spacing, and the resize corrects the wire endpoint position relative to enclosure or tip-spacing constraints (trial:i01.ug.Block6_union_row7.02, trial:i01.ug.leaf_0001.04, trial:i01.ug.leaf_0015.06, trial:i02.ug.Block6_union_row4.00).

## Rule M2.S.7: Parallel Run Length

Rule M2.S.7 forbids an 18 nm tip-to-tip gap co-located with side-to-side spacing <= 32 nm and requires parallel run length >= 35 nm when side spacing <= 32 nm. The `resize_end` operations in the history extend wire endpoints, which directly increases the parallel run length of adjacent wires. Extending polygon endpoints by 48–132 dbu (trial:i01.ug.leaf_0015.06 through trial:i01.ug.leaf_0001.04) was accepted without new violations in all cases where M2.S.7 was at risk, indicating that these magnitudes are sufficient to push run lengths above the 35 nm threshold. Apply `resize_end` on the tip-facing edge when M2.S.7 flags a short-run-length condition.

## Rule M2.S.1 and Spacing via Instance Moves

M2.S.1 requires 18 nm side-to-side spacing for edges longer than 36 nm. The X-axis `move_instance` operations at 36–112 dbu (trial:i01.ug.Block6_union_row3.00 through trial:i01.ug.leaf_0001.04) increase inter-wire spacing on M2 and were accepted in every case. A 36 dbu move is the smallest instance-level adjustment confirmed to preserve connectivity and yield zero new violations (trial:i01.ug.Block6_union_row8.03, trial:i01.ug.leaf_0011.05, trial:i01.ug.leaf_0018.07, trial:i03.ug.leaf_0001.00). Use 36 dbu as the default minimum move increment for M2 side-to-side spacing repairs when a single-instance move suffices.

## Rule V1.M2.EN.2 and Via Enclosure

All unit_gate trials touch both M2 and V1, with every accepted trial reporting `conn_preserved: true`. Moving instances that contain M2 and V1 together along X preserves the relative alignment of V1 within its M2 enclosure, satisfying V1.M2.EN.2 (minimum 5 nm enclosure on two opposite sides). When multiple instances are moved by the same delta in the same trial (e.g., all three instances at +72 in trial:i01.ug.Block6_union_row3.00), the enclosure geometry is unchanged and no new V1.M2.EN.2 violations arise. Never move an M2-containing instance without also moving the co-located V1-containing instance by the same delta; every accepted trial in the history that included a V1-touching polygon moved all co-located instances by matching deltas.

## Rule V2.M2.EN.1 and Via Cell Reshaping

The one cu_pool trial (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00) addressed V2.M2.EN.1 (minimum 5 nm enclosure of V2 by M2 on two opposite sides) by reshaping via cell VIA_VIA23_1_3_36_36 on V2, touching M2 and M3. The operation applied move_via_shape (–144 dbu and +144 dbu on X for shapes 0 and 2) combined with resize_via_shape (+264 dbu and +288 dbu on X for shapes 0, 1, and 2), resulting in a net reduction of 78 DRC violations across the two affected windows (leaf_0019 reduced from 139 to 97; leaf_0020 reduced from 154 to 118). Do not attempt to repair V2.M2.EN.1 solely by moving M2 polygons; reshape the via cell geometry directly as demonstrated in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00.

## Iteration Convergence

Across iterations 1 through 3, each successive iteration operates on a new design state hash and applies progressively fewer and smaller operations: iteration 1 produced nine trials with up to five ops each (trial:i01.ug.Block6_union_row5.01), iteration 2 produced four trials with up to three ops each (trial:i02.ug.Block6_union_row4.00), and iteration 3 has produced one trial with one op (trial:i03.ug.leaf_0001.00). The repair problem is contracting with each iteration. Apply only the minimum number of ops needed to resolve remaining violations rather than repeating large-delta corrections that were already applied in prior iterations; the 4 dbu and 8 dbu moves in iteration 2 (trial:i02.ug.Block6_union_row7.01, trial:i02.ug.Block6_union_row8.02) confirm that residual violations after a coarser pass require only fine-tuning.

## All-Orthogonal Geometry Requirement

The NONORTHOGONAL rule applies to M2: all M2 edges must have angles of exactly 0 or 90 degrees. Every `move_instance` and `resize_end` in the measured history operates strictly along the X axis, producing only horizontal displacements of rectilinear polygons. No diagonal moves, non-integer snapping, or oblique resize vectors have been applied. Never introduce diagonal or non-orthogonal edges on M2 when applying repair ops (confirmed by the complete absence of GEOMETRY.NONORTHOGONAL violations across all accepted trials).