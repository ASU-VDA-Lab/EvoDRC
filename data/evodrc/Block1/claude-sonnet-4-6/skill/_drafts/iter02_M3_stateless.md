## M3.S.2 — Tip-to-Side Spacing (25 nm minimum)

M3.S.2 triggers when a tip edge (≤ 36 nm) and a side edge (> 36 nm) on two separate polygons are closer than 25 nm (projection). Uniform y-axis shrinking of M3 polygon rows by −64 dbu per polygon produced 2 new M3.S.2 violations while leaving connectivity intact (trial:i01.ug.leaf_0035.13, gated_in, 24 total new-in-crop violations across rules). Do not apply bulk uniform y-axis shrinks to M3 polygon rows without first checking that tip-to-side clearances remain ≥ 25 nm; trial:i01.ug.leaf_0035.13 confirms that a −64 dbu y-resize across a leaf's full M3 polygon population is sufficient to violate this rule.

M3.S.2 also appeared as 2 new violations in trial:i02.ug.leaf_0004.03 (gated_in), where M3 polygons p1143 and p1142 were moved +32 dbu and −16 dbu in x respectively alongside M3 polygon p1561 moved +32 dbu in y, combined with a large volume of instance moves. The recurrence at exactly 2 violations across two different loci indicates that the same two polygon pairs are sensitive to M3 repositioning in either axis.

## V2.M3.EN.2 — M3 Enclosure of V2 (5 nm on two opposite sides)

V2.M3.EN.2 requires that M3 encloses V2 by at least 5 nm on two opposite sides (either left+right or top+bottom; 5 & 0 nm is also acceptable on one pair). Moving M3 polygons independently of their placed via instances creates enclosure deficits. Both iter-2 leaves that touched M3 introduced exactly 6 new V2.M3.EN.2 violations each: trial:i02.ug.leaf_0003.02 (M3 polygons p1145/p1144 moved ±32 dbu in x and p1563/p1562/p1561 moved −64/−112/−96 dbu in y) and trial:i02.ug.leaf_0004.03 (p1143/p1142 moved ±32 dbu in x, p1561 moved +32 dbu in y, plus instance moves for the same via cells). The identical count of 6 violations across both trials, sharing the same design_state, confirms that these violations originate from the same six V2 instances whose M3 landing geometry shifted.

Do not move M3 polygons that carry V2 landings in x or y without simultaneously adjusting the via instance position or the M3 polygon extent to restore ≥ 5 nm enclosure on the moved axis. X-moves as small as 32 dbu and −16 dbu were sufficient to break enclosure for these instances (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03).

## VIA_VIA23_1_3_36_36 M3 Via-Shape Resize — Ineffective

The op `resize_via_shape` on M3 for cell VIA_VIA23_1_3_36_36 (axis=y, delta=−40 dbu) was evaluated three times across the recorded history:

1. It was included in the multi-op set for trial:i01.ug.leaf_0034.12, which was gated out due to conn_broken before DRC delta was evaluated.
2. As a standalone cu_pool candidate it returned delta_total=0 with no change in violation count in either affected window (unit:leaf_0034: 182→182, unit:leaf_0035: 113→113), causing the cu_pool to reject it as net_positive (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).
3. The assembler for trial:i02.ug.leaf_0003.02 dropped the same op with reason "cu_pool:rejected_net_positive", confirming the rejection persists across iterations.

Do not re-attempt shrinking VIA_VIA23_1_3_36_36 M3 via shape in y by −40 dbu; the measured record shows zero net DRC benefit (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, trial:i02.ug.leaf_0003.02).

## Connectivity Gating and M3 Resize Combinations

Trial:i01.ug.leaf_0034.12 combined the VIA_VIA23 M3 via-shape resize with resize_end ops on M3 polygons p1214 (right edge, −4 dbu), p1178 (right edge, +192 dbu), and p1255 (right edge, +100 dbu), plus x-direction instance moves of 72–136 dbu. The trial was gated out with conn_broken (89 new in-crop violations reported but the trial was discarded). This shows that large asymmetric M3 polygon end-resizes (+192 dbu or +100 dbu on one edge while simultaneously moving instances 72–136 dbu) break M3 net connectivity. Resize_end magnitudes of this scale on M3 require connectivity verification before committing; the −4 dbu right-edge resize on p1214 alone would not be expected to break connectivity, but the combination with large positive resizes and instance moves did (trial:i01.ug.leaf_0034.12).

## M3 Polygon Move Mechanics and Cross-Crop Conflicts

In iter 2, M3 polygons p1143 and p1142 (x-axis) and p1561 (y-axis) were claimed by both leaf_0003 and leaf_0004. Leaf_0003 obtained them first and applied +32 dbu (p1143, x), −16 dbu (p1142, x), and −96 dbu (p1561, y) (trial:i02.ug.leaf_0003.02). Leaf_0004's conflicting moves on the same polygons were dropped with reason "cross_crop_first_wins" (trial:i02.ug.leaf_0004.03). The effective committed M3 state on p1561 is the leaf_0003 value (−96 dbu in y); leaf_0004's alternate value (+32 dbu in y) was not applied.

Cross-crop polygon conflicts on M3 are resolved by first-claim; the losing leaf's ops are silently dropped without error. Any knowledge about what DRC state results must be attributed to the winning leaf's ops, not the dropped alternatives.

## M3.W.1, M3.S.1, M3.S.3, M3.S.4, M3.S.5, M3.S.6, M3.A.1, V3.M3.EN.1, V2.M3.AUX.2 — No Violations Observed

None of these rules appear in any `new_in_crop_by_rule` entry across the full history. M3.W.1 (18 nm minimum width), M3.S.1 (side-to-side 18 nm), M3.S.3 (wide-tip-to-wide-tip 27 nm), M3.S.4 (narrow-tip-to-narrow-tip 31 nm), M3.S.5 (wide-tip-to-narrow-tip 31 nm), M3.S.6 (corner-to-corner 20 nm Euclidean), M3.A.1 (504 nm² minimum area), V3.M3.EN.1 (5 nm enclosure of V3 by M3), and V2.M3.AUX.2 (V2 width match to M3) produced zero new violations across all four trials. No prescriptive guidance for these rules is grounded in the measured history.