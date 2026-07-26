## Repair Behavior and Accepted Operation Patterns

All fourteen gated-in trials across iterations 1–3 carry `conn_preserved:true`. The single rejected trial (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00) did not violate connectivity, but produced `delta_total:0` and was rejected on the net-positive criterion. Connectivity preservation is a necessary condition for acceptance; zero net improvement in violation count causes rejection regardless of connectivity.

## Primary Repair Operation: move_instance

`move_instance` is the dominant primitive. Thirteen of the fourteen gated-in trials contain at least one `move_instance` op (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row10.01, trial:i01.ug.Block1_union_row3.03, trial:i01.ug.Block1_union_row4.04, trial:i01.ug.Block1_union_row5.05, trial:i01.ug.Block1_union_row6.06, trial:i01.ug.Block1_union_row8.07, trial:i01.ug.Block1_union_row9.08, trial:i01.ug.leaf_0004.09, trial:i01.ug.leaf_0020.10, trial:i01.ug.leaf_0031.11, trial:i02.ug.Block1_union_row6.01, trial:i03.ug.Block1_union_row3.00, trial:i03.ug.leaf_0004.01, trial:i03.ug.leaf_0005.02).

The most common x-axis move delta is +36 dbu, appearing in almost every trial. Larger multiples of 36 dbu (+72, +108) appear where a single-step move proved insufficient: instance i0290 was moved +36 dbu in iter 1 (trial:i01.ug.Block1_union_row3.03) and the same unit returned in iter 3 where i0290 required +72 dbu (trial:i03.ug.Block1_union_row3.00), confirming that accumulated prior moves shift the baseline and subsequent corrections must account for the cumulative displacement. Instance i0041 moved +36 dbu in iter 1 (trial:i01.ug.Block1_union_row10.01) and again +72 dbu in iter 3 (trial:i03.ug.leaf_0005.02).

Negative x-axis moves also appear: -36 dbu (trial:i01.ug.Block1_union_row5.05 i0433, trial:i01.ug.leaf_0020.10 i0082, trial:i02.ug.Block1_union_row6.01 i0455) and -32 dbu (trial:i01.ug.Block1_union_row6.06 i0455, trial:i01.ug.Block1_union_row8.07 i0258). Both -32 and -36 dbu negative moves were accepted; -32 dbu is not a multiple of 36 and represents a non-standard step that was nonetheless accepted in the unit_gate channel.

A diagonal move of [+36, -36] dbu was accepted in trial:i01.ug.Block1_union_row4.04 (instance i0300). This is the only y-component non-zero instance move in the history, and it was gated in successfully.

## resize_end Operations

`resize_end` on M2 polygon ends appears in seven gated-in trials as a companion to `move_instance`. Observed deltas on the high end: +36 (trial:i01.ug.Block1_union_row5.05 p1297, trial:i03.ug.leaf_0004.01 p1295), +52 (trial:i01.ug.Block1_union_row4.04 p1238), +72 (trial:i03.ug.leaf_0004.01 p1295, trial:i03.ug.leaf_0004.01), +92 (trial:i01.ug.Block1_union_row3.03 p1370, trial:i01.ug.Block1_union_row1.00 p1321), +128 (trial:i01.ug.Block1_union_row1.00 p1320). Low-end resize: +36 dbu on p1301 (trial:i01.ug.Block1_union_row5.05) and +36 on p1253 (trial:i01.ug.leaf_0020.10).

Extending polygon ends at larger deltas (92, 128 dbu) alongside instance moves was accepted without introducing net new out-of-crop violations (trial:i01.ug.Block1_union_row1.00). M2.S.7 requires parallel run length >= 35 nm when side-to-side spacing is <= 32 nm; the resize_end operations at these scales are consistent with extending run lengths to satisfy this constraint, as all trials extending polygon ends were accepted.

## resize (symmetric) Operation

One trial uses a symmetric `resize` (not `resize_end`): trial:i01.ug.leaf_0031.11 applies +36 dbu resize on polygon p1390 along with a +36 dbu instance move. This was gated in with 4 new violations introduced in crop but accepted because conn_preserved remained true.

## Via Manipulation: Rejected Pattern

trial:i02.cu.def:VIA_VIA23_1_3_36_36.00 applied `resize_via_shape` on a V2 via (cell VIA_VIA23_1_3_36_36, y-axis, -40 dbu, on M3 shape). The channel was `cu_pool`, not `unit_gate`. Result: `rejected_net_positive` with `delta_total:0`. No M2 spacing or width improvement was measured from shrinking this via's M3 landing shape. Do not use `resize_via_shape` on V2/M3 shapes as the sole operation to resolve M2 violations; the measured outcome is zero net benefit.

## Via Replacement: Accepted Structural Change

trial:i02.ug.leaf_0004.02 deleted instance i0300 and placed a new VIA_VIA12 via at origin [5904, 6300] dbu. This was gated in with zero new violations. This is the only `delete_instance` + `add_via` combination in the history and it resolved the locus without introducing new violations.

## M2-V1 Co-movement Requirement

Every gated-in trial in the unit_gate channel touches layers M1, M2, and V1 together. No trial modifies M2 in isolation from V1. This is consistent with rules V1.M2.EN.2 and V1.M2.AUX.2: moving M2 segments without co-moving their V1 vias would violate enclosure or width-matching requirements. The trial set includes no counterexample; all accepted repairs treat M2 and V1 as a coupled unit.

## New Violations Introduced During Repair

Four trials introduced new violations within the crop window (n_new_in_crop > 0) and were still gated in: trial:i01.ug.Block1_union_row1.00 (4 new), trial:i01.ug.Block1_union_row6.06 (1 new), trial:i01.ug.leaf_0031.11 (4 new), trial:i02.ug.Block1_union_row6.01 (1 new). In all cases conn_preserved was true and n_new_out_of_crop was 0. New in-crop violations do not block acceptance when connectivity is preserved and no violations escape the crop boundary.

## Recurrent Units Requiring Multi-Iteration Attention

Three units required repair across multiple iterations:

**Block1_union_row6**: Repaired in iter 1 (trial:i01.ug.Block1_union_row6.06, single -32 dbu move of i0455, 1 new in-crop violation) and iter 2 (trial:i02.ug.Block1_union_row6.01, five moves including i0455 at -36 dbu, 1 new in-crop violation). The iter 1 single-instance -32 dbu move left residual violations; iter 2 required coordinating five instances.

**leaf_0004**: Repaired in iter 1 (trial:i01.ug.leaf_0004.09, +36 dbu move), iter 2 (trial:i02.ug.leaf_0004.02, delete+add_via), and iter 3 (trial:i03.ug.leaf_0004.01, +72 dbu move + +72 dbu resize_end on p1295). Three distinct repair attempts across three iterations without elimination from the work queue; each iteration required different or larger operations.

**Block1_union_row3**: iter 1 (trial:i01.ug.Block1_union_row3.03, +36 dbu move of i0290 + +92 dbu resize_end on p1370) and iter 3 (trial:i03.ug.Block1_union_row3.00, +36 dbu move of i0299, +72 dbu move of i0290, +36 dbu move of i0453). Instance i0290 accumulated a total of +108 dbu in x across both iterations.

Units that reappear across iterations need larger aggregate displacements. When a unit returns after a prior accepted repair, subsequent moves on the same instances must exceed the prior delta to produce net improvement.

## Operation Count and Locus Scale

Trials range from 1 to 5 ops. Single-op trials (trial:i01.ug.Block1_union_row6.06, trial:i01.ug.leaf_0004.09, trial:i03.ug.leaf_0005.02) were accepted. Five-op trials (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row5.05, trial:i01.ug.Block1_union_row8.07, trial:i02.ug.Block1_union_row6.01) were also accepted. Higher op count did not cause rejection. Locus windows vary from narrow single-cell crops ([9936,4048,10620,4212] in trial:i01.ug.leaf_0004.09) to full-block spans ([2536,6588,14328,7452] in trial:i01.ug.Block1_union_row5.05); both scales produced accepted outcomes.

## M2 Geometry: Orthogonality

The NONORTHOGONAL rule flags any M2 edge with angle outside {0°, 90°, 180°, 270°}. All accepted operations in this history use axis-aligned moves (x-only or y-only deltas, with the single [+36,-36] exception in trial:i01.ug.Block1_union_row4.04) and axis-aligned resize_end (axis:x). No diagonal polygon geometry was introduced. Diagonal instance placement ([+36,-36] in trial:i01.ug.Block1_union_row4.04) was accepted because the instance's internal M2 geometry remains orthogonal after the move.