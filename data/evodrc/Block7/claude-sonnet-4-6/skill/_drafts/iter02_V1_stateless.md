**Dominant repair pattern: lateral instance movement with M2 polygon adjustment**

Across all 37 accepted trials in iterations 1 and 2, `move_instance` on the X axis is the primary operation used to resolve V1 DRC violations in Block7. Trials including trial:i01.ug.Block7_union_row9.21, trial:i01.ug.Block7_union_row6.18, and trial:i01.ug.Block7_union_row11.01 demonstrate that groups of 2–6 instance moves in the positive X direction, with magnitudes of 36–108 dbu, clear spacing violations without triggering new ones. When instance moves are applied, paired `resize_end` operations on M2 polygons are required to preserve connectivity. In trial:i01.ug.Block7_union_row14.04, 11 operations combining instance moves and a `resize_end` on polygon p3539 by 16 dbu successfully resolved violations without producing new crop violations.

**Grid-snapped move magnitudes**

Instance moves in the X direction cluster at multiples of 4 dbu: 4, 12, 24, 28, 32, 36, 40, 52, 56, 60, 64, 68, 72, 92, 96, 100, 108, 120, 128, 136, 160, 192, 288 dbu. Moves of 36 dbu and 72 dbu are the most frequent, appearing in trial:i01.ug.Block7_union_row11.01, trial:i01.ug.Block7_union_row17.07, trial:i01.ug.Block7_union_row23.13, and trial:i02.ug.Block7_union_row12.01, among many others. Use move magnitudes that are multiples of 4 dbu; non-multiples of 4 do not appear in successful repairs.

**M2 resize_end accompanies instance moves that shift polygon endpoints**

When a `move_instance` shifts the position of a V1 or M1 instance relative to its M2 endpoint, a corresponding `resize_end` on the M2 polygon is required. In trial:i01.ug.Block7_union_row10.00, polygon p3751 receives two sequential `resize_end` operations (low end +180 dbu, high end +56 dbu) alongside instance moves, demonstrating that both endpoints may require independent adjustment. In trial:i01.ug.Block7_union_row7.19, a `resize_end` of 128 dbu on the high end of p3317 accompanies a 108 dbu instance move while a separate instance moves only 40 dbu, confirming that resize deltas need not match instance move deltas exactly.

**M2 polygon addition for connectivity restoration**

In trial:i01.ug.Block7_union_row20.10, a new M2 rectangle (56 dbu wide × 72 dbu tall, coordinates [[5992,22824],[5992,22896],[6048,22896],[6048,22824]]) was added via `add_polygon` to restore M2 coverage, paired with a -36 dbu X move on instance i0753. This demonstrates that `add_polygon` on M2 is a valid repair operation when a move would otherwise leave a V1 instance without sufficient M2 enclosure per V1.M2.EN.2 or V1.M2.AUX.2.

**Y-axis moves are used for inter-row and cross-track adjustments**

Y-direction instance moves are less frequent than X-direction moves but appear in trials that also touch M3 and V2. In trial:i01.ug.Block7_union_row16.06, instances i0336 and i0308 receive Y moves of -12 dbu and polygon p3516 receives a Y `move` of -12 dbu, with the repair spanning M1, M2, M3, V1, and V2. The same cross-layer pattern appears in trial:i01.ug.leaf_0095.26 (Y moves of +48 dbu on instances, +68 dbu and +48 dbu on polygons p2432 and p3537, touching M1, M2, M3, V1, V2) and trial:i02.ug.leaf_0014.08 (Y moves of -12 dbu, layers M1, M2, M3, V1, V2). Apply Y-direction moves when V1 violations are entangled with V2 spacing or enclosure constraints on adjacent rows.

**New in-crop violations are tolerated when connectivity is preserved; revisits clear residuals**

Several iteration-1 trials were accepted despite introducing new violations within the crop window. Trial:i01.ug.Block7_union_row22.12 produced 2 new in-crop violations with a single 4 dbu move. Trial:i01.ug.Block7_union_row21.11 produced 9 new in-crop violations from a 2-op sequence. Block7_union_row22 returned in iteration 2 as trial:i02.ug.Block7_union_row22.05 (6 ops, 0 new violations), extending the operation set to clear the residuals introduced in iteration 1. When a small move introduces new violations, a follow-up pass with additional M2 resize or broader instance repositioning is required to reach zero.

**Iteration 2 repairs on previously addressed units require fewer or different ops**

Units revisited in iteration 2 show either reduced operation counts or zero new violations relative to their iteration-1 fixes. Block7_union_row13 dropped from 6 ops in trial:i01.ug.Block7_union_row13.03 to 3 ops in trial:i02.ug.Block7_union_row13.02. Block7_union_row9 dropped from 5 ops in trial:i01.ug.Block7_union_row9.21 to 2 ops in trial:i02.ug.Block7_union_row9.06. Block7_union_row22 expanded from 1 op in trial:i01.ug.Block7_union_row22.12 to 6 ops in trial:i02.ug.Block7_union_row22.05, achieving zero new violations. Prefer complete repair over partial repair in a single pass to avoid re-queuing units.

**Mixed positive/negative moves within a single trial resolve bidirectional crowding**

Several trials apply both positive and negative X-direction moves within the same operation sequence. In trial:i01.ug.Block7_union_row14.04, instance i0519 moves -36 dbu while six other instances move +36 to +108 dbu. In trial:i01.ug.Block7_union_row19.09, instance i0026 moves -72 dbu while others move +36 to +72 dbu. In trial:i02.ug.Block7_union_row13.02, instance i1059 moves -72 dbu while others move +36 dbu. This bidirectional pattern resolves V1.S.1 spacing violations where a via pair is crowded from both sides on the same M2 track.

**Symmetric resize is used when both ends of a polygon must move together**

In trial:i01.ug.Block7_union_row15.05, `resize` on polygon p3586 by 160 dbu (symmetric resize, not `resize_end`) is combined with seven instance moves. In trial:i01.ug.Block7_union_row19.09, polygons p3619, p3654, and p3523 each receive symmetric `resize` operations. Use symmetric `resize` when both ends of an M2 polygon must extend together to track a repositioned V1 or maintain enclosure; use `resize_end` when only one endpoint requires adjustment.

**Leaf-level units are repaired with single-operation moves; residuals can propagate**

Single-instance repairs are used for isolated leaf cells. Trial:i01.ug.leaf_0001.22, trial:i01.ug.leaf_0002.23, trial:i02.ug.leaf_0017.09, and trial:i02.ug.leaf_0022.10 each contain exactly one `move_instance` operation. Despite minimal operation counts, trial:i01.ug.leaf_0002.23 introduced 2 new in-crop violations and trial:i02.ug.leaf_0022.10 introduced 3, confirming that isolated leaf moves shift V1 spacing relationships with neighboring instances outside the leaf boundary. Leaf-level repairs with non-zero n_new_in_crop require inspection of the surrounding crop for secondary violations.

**Nonorthogonal geometry is never introduced**

No trial applies any operation that would produce non-axis-aligned polygon edges. All `resize_end`, `resize`, and `move` operations act on a single axis (x or y). The GEOMETRY.NONORTHOGONAL rule applies to V1 edges as it does to all drawing layers; all polygon-level operations must be restricted to horizontal or vertical edges to avoid triggering this check.

**V1 containment within M1 and M2 is maintained through coordinated moves**

All repairs in the dataset preserve V1 containment within M1 and M2 per V1.AUX.1. The M2 `add_polygon` in trial:i01.ug.Block7_union_row20.10 provides direct evidence that when a move would push V1 outside its M2 boundary, adding an M2 extension polygon is the correct repair rather than moving V1 back. V1.M2.AUX.2 requires that V1 width matches M2 width perpendicular to the M2 length; the preponderance of X-axis moves in this dataset (parallel to the M2 run direction) confirms that repairs along the M2 length axis are safe for V1.M2.AUX.2 compliance. Y-axis resizes of M2 that would alter the perpendicular width are avoided except in explicit multi-layer cross-track operations as in trial:i01.ug.leaf_0095.26 and trial:i02.ug.Block7_union_row15.03, where the Y dimension adjustment is intentional and coordinated with V2 and M3.