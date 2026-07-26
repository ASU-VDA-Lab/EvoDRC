**Accepted operation mix**

All 37 trials in this layer's history carry `decision: gated_in` with `conn_preserved: true`. The gating criterion is connectivity preservation, not violation count: trials with `n_new_in_crop` as high as 9 (trial:i01.ug.Block7_union_row21.11) and 3 (trial:i02.ug.leaf_0017.09, trial:i02.ug.leaf_0022.10) were accepted without restriction. Do not reject a candidate repair solely because `n_new_in_crop` is nonzero; connectivity preservation is the necessary and sufficient acceptance condition observed across this full dataset.

`n_new_out_of_crop` is 0 in every trial. Operations are fully contained within each locus and do not push violations into adjacent regions. Size the locus to fully enclose all modified instances before applying operations.

---

**Primary operation: move_instance (x-axis)**

The dominant repair operation is `move_instance` with an x-axis delta. The 36 dbu step (18 nm, equal to the M1.W.1 minimum width) is the most frequent single-instance displacement, confirmed in trial:i01.ug.Block7_union_row11.01, trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row6.18, trial:i01.ug.Block7_union_row8.20, trial:i01.ug.Block7_union_row9.21, trial:i02.ug.Block7_union_row12.01, trial:i02.ug.Block7_union_row13.02, trial:i02.ug.Block7_union_row22.05, and others. Multiples of 36 dbu (72, 108, 136) appear when spacing violations are larger: trial:i01.ug.Block7_union_row14.04 moves i0920 by 108 dbu, trial:i01.ug.Block7_union_row15.05 moves i0913 by 136 dbu, trial:i01.ug.Block7_union_row7.19 moves i1446 by 108 dbu. Use 36 dbu as the base displacement quantum; scale to multiples of 36 when the measured gap demands it.

Sub-36-dbu x-moves occur in specific fine-tuning contexts: trial:i01.ug.Block7_union_row6.18 displaces i1473 by 28 dbu, trial:i01.ug.Block7_union_row22.12 displaces i0132 by 4 dbu, and trial:i02.ug.leaf_0022.10 displaces i0100 by 3 dbu. Apply sub-quantum moves only when the nearest 36-dbu step would overshoot a spacing limit or violate V0.M1.AUX.3 width-match.

Negative x-moves are confirmed at −36 dbu (trial:i01.ug.Block7_union_row14.04 i0519, trial:i01.ug.Block7_union_row16.06 i0928 and i0407, trial:i01.ug.Block7_union_row8.20 i1891, trial:i02.ug.Block7_union_row13.02 i1059), −72 dbu (trial:i01.ug.Block7_union_row19.09 i0026, trial:i02.ug.Block7_union_row15.03 i0913), −96 dbu (trial:i02.ug.Block7_union_row15.03 i0913—note this trial uses a later design state after row15 was revisited), −108 dbu (trial:i01.ug.leaf_0024.25 i1062), and −24 dbu (trial:i01.ug.leaf_0024.25 i1292). Negative moves resolve over-crowded spacing by pulling an instance back toward a fixed neighbor rather than pushing it away.

---

**Secondary operation: resize_end**

`resize_end` extends or retracts one endpoint of an M1 polygon without displacing the opposite end. High-end x-axis extensions are the most frequent form: trial:i01.ug.Block7_union_row14.04 extends p3200 by +72 dbu and p3215 by +56 dbu; trial:i01.ug.Block7_union_row24.14 extends p3058 by +136 dbu, p3635 by +120 dbu, and p3564 by +128 dbu; trial:i02.ug.Block7_union_row9.06 extends p3683 by +112 dbu; trial:i01.ug.Block7_union_row5.17 extends p3737 and p3746 each by +92 dbu.

Low-end x-axis adjustments appear with a +56 dbu delta at "end":"low" in trial:i01.ug.Block7_union_row3.15 (p3384), trial:i01.ug.Block7_union_row17.07 (p3187), and trial:i01.ug.Block7_union_row8.20 (p3430). A positive delta on the low end moves the low edge in the positive direction (inward), shortening the polygon from that side to eliminate an enclosure overhang or AUX.3 mismatch.

Y-axis `resize_end` appears in trial:i01.ug.leaf_0095.26, which extends p2432 by +68 dbu and p3537 by +48 dbu at "end":"high" on the y-axis, co-occurring with y-axis instance moves (+48 dbu) in the same trial.

Apply `resize_end` together with `move_instance` whenever the instance displacement alone would leave the M1 polygon under-enclosing the V0 or V1 via it carries (V0.M1.EN.1 or V1.M1.EN.1). Do not resize both ends independently when only one end violates enclosure.

---

**Symmetric resize**

The `resize` operation (both ends equally) is confirmed in three trials. Trial:i01.ug.Block7_union_row15.05 applies +160 dbu symmetric x-resize to p3586. Trial:i01.ug.Block7_union_row19.09 applies +40 dbu to p3619, −72 dbu to p3654, and +72 dbu to p3523 (all symmetric x). Trial:i02.ug.Block7_union_row15.03 applies +96 dbu symmetric y-resize to p3592, paired with a y-axis move_instance of −84 dbu (i0913) and a separate y-axis polygon `move` of −84 dbu (i1062). Use symmetric resize when both ends of the polygon require the same adjustment magnitude; use `resize_end` when only one end needs to change.

---

**Y-axis operations and multi-layer co-adjustment**

Y-axis `move_instance` and polygon adjustments are confirmed in a distinct subset of trials that always touch M1, M2, M3, V1, and V2 together. Trial:i01.ug.Block7_union_row16.06 moves i0336 and i0308 by [0,−12] dbu and applies a y-axis `move` of −12 dbu to p3516, with `touched_layers: [M1, M2, M3, V1, V2]`. Trial:i01.ug.leaf_0095.26 moves i0177 and i0184 by [0,+48] dbu and applies y-axis `resize_end` on two polygons, also touching M1, M2, M3, V1, V2. Trial:i02.ug.leaf_0014.08 moves i0519 and i0524 by [0,−12] dbu and applies a y-axis `move` of −12 dbu to p3515, also touching M1, M2, M3, V1, V2.

Pure M1/M2/V1 repair sets (the majority of trials) never include y-axis moves. When a y-axis M1 adjustment is needed, plan simultaneous co-adjustment of M2, M3, V1, and V2.

The −12 dbu y-correction recurs across two trials on the row-16 region: trial:i01.ug.Block7_union_row16.06 (instances i0336, i0308, polygon p3516) and trial:i02.ug.leaf_0014.08 (instances i0519, i0524, polygon p3515). This demonstrates that a −6 nm vertical misalignment in this region was not fully resolved in iteration 1 and required a second-pass correction at a different sub-locus in iteration 2.

---

**V1 is always co-modified with M1**

Every trial lists both M1 and V1 in `touched_layers`. M1 polygons carry V1 vias; moving or resizing an M1 polygon changes the enclosure geometry around the V1 via and requires V1 to be repositioned concurrently. Always include V1 in the operation set when modifying M1 positions or shapes. Trials also always include M2, confirming that M1 repairs propagate upward through the via stack to M2.

---

**add_polygon as a connectivity bridge**

Trial:i01.ug.Block7_union_row20.10 uses a single `move_instance` (i0753, −36 dbu x) plus an `add_polygon` on M2 with coordinates [[5992,22824],[5992,22896],[6048,22896],[6048,22824]]—a 56 dbu × 72 dbu (28 nm × 36 nm) patch. This M1-layer trial resolved a connectivity gap not by extending the M1 polygon itself but by inserting a small M2 bridge polygon. When a move_instance creates a gap in the via chain above M1, add a small polygon on the higher layer rather than extending M1 geometry. The resulting trial was accepted with `n_new_in_crop: 0`.

---

**Multi-iteration behavior**

Iteration 2 revisits rows 12, 13, 15, 20, 22, and 9, all processed in iteration 1:

- Row 12: trial:i01.ug.Block7_union_row12.02 (iter 1, n_new_in_crop=0) → trial:i02.ug.Block7_union_row12.01 (iter 2, n_new_in_crop=0). Different instance IDs (i1208, i1356 in iter 1; i1311, i1320, i1759 in iter 2) confirm distinct residual violations at different sub-locations.
- Row 13: trial:i01.ug.Block7_union_row13.03 (iter 1, n_new_in_crop=1) → trial:i02.ug.Block7_union_row13.02 (iter 2, n_new_in_crop=0). The single new in-crop violation from iter 1 was cleared in iter 2.
- Row 15: trial:i01.ug.Block7_union_row15.05 (iter 1, n_new_in_crop=0) → trial:i02.ug.Block7_union_row15.03 (iter 2, n_new_in_crop=0). The iter-2 repair added a y-axis correction absent from iter 1, using a smaller locus [7092,17388,15480,18252] vs. [4048,17388,24336,18252].
- Row 20: trial:i01.ug.Block7_union_row20.10 (iter 1, n_new_in_crop=0) → trial:i02.ug.Block7_union_row20.04 (iter 2, n_new_in_crop=0). The iter-2 pass used a different locus (shifted east) and operated on different polygon (p3048 vs. none in iter 1's M1 ops).
- Row 22: trial:i01.ug.Block7_union_row22.12 (iter 1, n_new_in_crop=2) → trial:i02.ug.Block7_union_row22.05 (iter 2, n_new_in_crop=0). The two new violations from iter 1 were cleared in iter 2 using six operations vs. one in iter 1.
- Row 9: trial:i01.ug.Block7_union_row9.21 (iter 1, n_new_in_crop=0) → trial:i02.ug.Block7_union_row9.06 (iter 2, n_new_in_crop=0). Smaller locus in iter 2 [10960,10908,14400,11772] vs. [3184,10908,18288,11772].

Schedule a second iteration over any row that shows `n_new_in_crop > 0` in iteration 1, and also over rows where the iter-1 locus is large enough to have masked residual sub-region violations.

---

**Operation count and locus sizing**

Trial complexity ranges from 1 operation (trial:i01.ug.leaf_0001.22, trial:i01.ug.Block7_union_row22.12, trial:i02.ug.leaf_0017.09, trial:i02.ug.leaf_0022.10) to 11 operations (trial:i01.ug.Block7_union_row14.04). Leaf-unit trials consistently use 1–2 operations and small loci (e.g., [7072,2268,7920,3132] in trial:i01.ug.leaf_0001.22). Union-row trials use 2–11 operations and wider loci (up to [3088,16308,26064,17172] in trial:i01.ug.Block7_union_row14.04). When multiple instances must be co-moved to resolve coupled M1.S.1 or M1.S.2 spacing violations, expand the locus to contain all affected instances. Trial:i01.ug.Block7_union_row14.04 with 11 operations and the widest locus of any trial in this dataset (23.0 µm span) demonstrates that highly coupled rows require a correspondingly large repair window.