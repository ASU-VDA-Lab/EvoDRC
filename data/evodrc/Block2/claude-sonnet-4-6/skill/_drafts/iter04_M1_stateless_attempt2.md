## Observed Operation Patterns on M1

All eight recorded trials for M1 were accepted with `decision: gated_in` and `conn_preserved: true`. No trial produced a net increase in out-of-crop violations; seven of eight produced zero new violations of any kind in the crop window (trial:i01.ug.Block2_union_row1.00, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0001.03, trial:i01.ug.leaf_0004.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0011.06). The single trial with `n_new_in_crop: 1` was still gated in (trial:i04.ug.leaf_0002.01).

## Move-Instance Operations

Move-instance operations displacing M1-touching instances along +x are consistently accepted. Single-instance moves of 36 dbu in +x were accepted without new violations in trial:i01.ug.leaf_0004.04 and trial:i01.ug.leaf_0007.05. Multi-instance coordinated moves of 36 dbu in +x across two instances were accepted in trial:i01.ug.Block2_union_row1.00. When moving instances, apply the same delta to all instances in the locus that share connectivity on M1 to satisfy conn_preserved; all multi-instance moves in the history that preserved connectivity used a uniform delta across co-moved instances (trial:i01.ug.Block2_union_row1.00, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02).

Move-instance operations along +y are also accepted. In trial:i04.ug.leaf_0002.01, one instance was moved 36 dbu in +y while others moved in -x; the combined operation was gated in with conn_preserved.

Move-instance operations using -x displacement (64 dbu in -x across four instances simultaneously) were accepted in trial:i04.ug.leaf_0002.01, indicating that both positive and negative x-axis instance displacements are viable when M1 connectivity is preserved across the moved set.

## Resize-End Operations on M1 Polygons

Resize-end operations extending M1 polygon ends along the x-axis are accepted when paired with corresponding instance moves. In trial:i01.ug.Block2_union_row3.01, a single resize_end of 36 dbu at the high-x end of polygon p1040 was accepted alongside two instance moves. In trial:i01.ug.Block2_union_row5.02, two resize_end operations of 64 dbu at the high-x ends of polygons p1059 and p1057 were accepted together with three instance moves. In trial:i01.ug.leaf_0001.03, resize_end of 184 dbu at the high end of p1065 and 176 dbu at the low end of p957 were both accepted alongside an instance move, demonstrating that asymmetric resize magnitudes and low-end (shrink toward center) resizes on M1 polygons are viable. In trial:i01.ug.leaf_0011.06, a 36 dbu high-end resize on p1052 was accepted with one instance move.

All accepted resize_end operations in the history extend or adjust M1 polygon ends along the x-axis (`axis: "x"`). No y-axis resize_end operations on M1 appear in the history.

## Rule-Relevant Dimensional Context

**M1.W.1 (minimum width 18 nm) and M1.S.1/S.2/S.3 (spacing rules):** All accepted trials produced zero new spacing or width violations in the crop. Resize-end deltas observed range from 36 to 184 dbu. No trial introduced a new M1.W.1 or M1.S.* violation, confirming that the chosen resize magnitudes were compatible with the minimum-width and spacing constraints in the affected loci (trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0001.03, trial:i01.ug.leaf_0011.06).

**V0.M1.EN.1 and V1.M1.EN.1 (via enclosure):** All trials that touched M1 also touched V1 (and in some cases V0 implicitly through M1 reshaping). All were accepted with conn_preserved, indicating that the combined move-and-resize strategy maintained adequate via enclosure on both ends. When resizing M1 polygon ends while moving instances, enclosure constraints on co-located vias are satisfied as long as the instance move and polygon resize are applied together (trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0001.03).

**V0.M1.AUX.3 (V0 width must match M1 width along perpendicular):** All accepted trials with M1 resize operations preserved this constraint implicitly; no AUX.3 violation was introduced across any trial touching M1 (trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0001.03, trial:i01.ug.leaf_0011.06).

**M1.A.1 (minimum area 504 nm-sq):** No trial introduced a new M1.A.1 violation. All resize operations kept M1 polygons above the minimum area threshold, including the smaller 36 dbu deltas (trial:i01.ug.Block2_union_row3.01, trial:i01.ug.leaf_0011.06).

## Multi-Layer Coordination

When M1 violations require repair in proximity to M2 and V1, operations on all three layers are bundled into a single trial. Every trial in the history touches M1, M2, and V1 together. Trials touching additional layers (M4 in trial:i01.ug.leaf_0001.03; M4, M5, V4 in trial:i04.ug.leaf_0002.01) were also accepted, confirming that multi-layer bundles involving M1 are viable when connectivity is preserved across the full touched-layer set.

## Iteration 4 Specifics

The sole iteration-4 record (trial:i04.ug.leaf_0002.01) used a move operation (`op: "move"`) on polygon p937 with a -64 dbu x-axis delta, combined with four instance moves of [-64, 0] and one instance move of [0, 36], plus a polygon move of p1036 by 36 dbu in y. This was accepted with `n_new_in_crop: 1` and `n_new_out_of_crop: 0`, meaning one new in-crop marker appeared but the gating criterion was still met. Direct polygon move operations on M1 (not resize_end, but translating the whole polygon) are accepted when paired with instance moves that preserve connectivity, as demonstrated in trial:i04.ug.leaf_0002.01.