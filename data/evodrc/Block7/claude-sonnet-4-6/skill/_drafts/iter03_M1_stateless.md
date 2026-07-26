## Accepted Operation Types on M1

The repair operations applied to M1 across iterations 1, 2, and 3 are: `move_instance` (x or y translation of a cell instance), `resize_end` (extension or retraction of one end of a named polygon along one axis), `resize` (translation of a full polygon along one axis), and `move` (free translation of a named polygon). No `add_polygon` operation targets M1 in any record; the two `add_polygon` ops in the history create patches on M2 (trial:i01.ug.Block7_union_row20.10) and M3 (trial:i03.ug.leaf_0002.04) only. All 40 trials carry `decision: gated_in` and `conn_preserved: true`.

## M1 Repairs Always Include V1 and M2 in the Same Transaction

Every accepted trial has `touched_layers` containing at minimum `["M1", "M2", "V1"]`. Five trials extend the set to include M3 and V2: trial:i01.ug.Block7_union_row16.06, trial:i01.ug.leaf_0095.26, trial:i02.ug.leaf_0014.08, trial:i03.ug.leaf_0002.04, and trial:i03.ug.leaf_0011.07. All five of those involve y-direction adjustments. No trial with solely M1 changes appears in the record; always scope the transaction to include V1 and M2 at minimum, and add M3 and V2 when y-direction moves are required.

## move_instance: Primary Repair Vector on a 36 dbu X-Grid

The most frequent repair is a `move_instance` with `delta_dbu [+36, 0]`. This appears in trial:i01.ug.Block7_union_row11.01, trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row17.07, trial:i01.ug.Block7_union_row8.20, trial:i01.ug.Block7_union_row6.18 (for five of six instances), trial:i02.ug.Block7_union_row12.01, trial:i02.ug.Block7_union_row13.02, trial:i03.ug.Block7_union_row13.01, and many others. Integer multiples are used when larger x-separation is required: 72 dbu in trial:i01.ug.Block7_union_row14.04 and trial:i01.ug.Block7_union_row18.08; 108 dbu in trial:i01.ug.leaf_0001.22 and trial:i01.ug.Block7_union_row23.13; 136 dbu in trial:i01.ug.Block7_union_row15.05 and trial:i01.ug.Block7_union_row24.14. Negative x-moves are equally accepted: -36 dbu in trial:i01.ug.Block7_union_row14.04 and trial:i01.ug.Block7_union_row16.06; -72 dbu in trial:i01.ug.Block7_union_row18.08 and trial:i01.ug.Block7_union_row19.09; -96 dbu in trial:i02.ug.Block7_union_row15.03; -108 dbu in trial:i01.ug.leaf_0024.25.

Sub-36 x-moves appear in three trials: +28 dbu in trial:i01.ug.Block7_union_row6.18, +4 dbu as the sole op in trial:i01.ug.Block7_union_row22.12, and +3 dbu as the sole op in trial:i02.ug.leaf_0022.10. All three are accepted.

Apply y-direction moves only when the transaction also touches M3 and V2. Accepted y-deltas are: -12 dbu in trial:i01.ug.Block7_union_row16.06 and trial:i02.ug.leaf_0014.08; +48 dbu in trial:i01.ug.leaf_0095.26 and trial:i02.ug.leaf_0017.09; -48 dbu in trial:i01.ug.Block7_union_row19.09 and trial:i03.ug.leaf_0011.07; -84 dbu in trial:i02.ug.Block7_union_row15.03; +84 dbu in trial:i03.ug.leaf_0007.05.

## resize_end: Single-Edge Adjustment, 56 dbu Most Frequent Delta

`resize_end` adjusts one end of a named polygon and is used throughout all three iterations. On the x-axis low end, 56 dbu is the value used most consistently: polygon p3384 in trial:i01.ug.Block7_union_row3.15, p3526 in trial:i01.ug.Block7_union_row13.03, p3187 in trial:i01.ug.Block7_union_row17.07, p3430 in trial:i01.ug.Block7_union_row8.20, and p3048 on the high end in trial:i02.ug.Block7_union_row20.04. Larger x-high-end extensions appear when more enclosure or polygon area is needed: 72 dbu in trial:i01.ug.Block7_union_row14.04, 92 dbu in trial:i01.ug.Block7_union_row18.08 and trial:i02.ug.Block7_union_row22.05, 112 dbu in trial:i02.ug.Block7_union_row9.06, 120-136 dbu in trial:i01.ug.Block7_union_row24.14, and 308 dbu in trial:i01.ug.Block7_union_row10.00.

On the y-axis, `resize_end` extends a polygon end along y to recover enclosure for vias that are offset vertically: +68 dbu high end in trial:i01.ug.leaf_0095.26, +48 dbu high end in trial:i01.ug.leaf_0095.26, -48 dbu on both ends of p3592 in trial:i03.ug.leaf_0007.05, -48 dbu high end of p3537 in trial:i03.ug.leaf_0011.07, and +20 dbu high end of p2720 in trial:i03.ug.leaf_0002.04. A negative delta on x-low also appears: -88 dbu on p3300 in trial:i03.ug.leaf_0002.04, used alongside a y-extension to rebalance the M1 landing.

## resize and move (Polygon): Coarser Adjustments

The `resize` operation (no `end` argument; shifts the whole polygon uniformly along one axis) is used for larger displacements: +160 dbu x in trial:i01.ug.Block7_union_row15.05, +40 dbu and ±72 dbu x in trial:i01.ug.Block7_union_row19.09, and +96 dbu y in trial:i02.ug.Block7_union_row15.03. The `move` polygon operation is used only for y-axis shifts of -12 dbu, as seen in trial:i01.ug.Block7_union_row16.06 (polygon p3516) and trial:i02.ug.leaf_0014.08 (polygon p3515); both trials also carry y-direction instance moves and touch M3/V2.

## Connectivity Is the Gate Criterion; New Within-Crop Violations Are Tolerated

The acceptance gate is `conn_preserved: true`, not `n_new_in_crop == 0`. Trials with non-zero new violations are accepted throughout all iterations: n_new_in_crop = 1 in trial:i01.ug.Block7_union_row13.03, trial:i01.ug.Block7_union_row4.16, trial:i01.ug.Block7_union_row5.17, and trial:i03.ug.leaf_0008.06; n_new_in_crop = 2 in trial:i01.ug.Block7_union_row22.12 and trial:i01.ug.Block7_union_row24.14; n_new_in_crop = 3 in trial:i02.ug.leaf_0017.09, trial:i02.ug.leaf_0022.10, and trial:i03.ug.leaf_0007.05; and n_new_in_crop = 9 in trial:i01.ug.Block7_union_row21.11. Do not reject a repair candidate solely because it introduces new within-crop violations; the iteration loop addresses residual violations in subsequent passes.

## Iteration Convergence: Narrowing Loci and Fewer Units Per Pass

The count of units requiring repair decreases with each iteration: 27 trials in iteration 1 (trial:i01.ug.Block7_union_row10.00 through trial:i01.ug.leaf_0095.26), 10 in iteration 2 (trial:i02.ug.Block7_union_row12.01 through trial:i02.ug.leaf_0022.10), and 7 in iteration 3 (trial:i03.ug.Block7_union_row10.00 through trial:i03.ug.leaf_0011.07). Loci in iteration 3 are narrower than in iteration 1 for the same unit: the crop for Block7_union_row10 spans 9704 dbu in x at iteration 1 (trial:i01.ug.Block7_union_row10.00) but only 3096 dbu at iteration 3 (trial:i03.ug.Block7_union_row10.00), and involves fewer ops (2 vs. 6). Iteration 3 trials use smaller op counts and finer deltas on average, consistent with residual local violations being resolved with targeted single-polygon edits rather than broad multi-instance repositioning.

## Multi-Instance Coordination Within a Single Trial

Many trials move multiple instances and resize multiple polygons within a single locus. Trial:i01.ug.Block7_union_row14.04 applies 11 ops (7 move_instance and 2 resize_end), and trial:i01.ug.Block7_union_row10.00 applies 6 ops including both instance moves and polygon resize_end on two different polygons. When a locus contains multiple M1 spacing or enclosure violations, apply all necessary move_instance and resize_end ops within the same transaction rather than splitting them across passes.