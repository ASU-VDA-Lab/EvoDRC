## Observed Repair Patterns on M1

### Operation Vocabulary

Every accepted M1 repair in this history uses one or more of these primitive operations, always with `conn_preserved: true` and `decision: gated_in`: `move_instance`, `resize_end` (one axis, one end), `resize` (full polygon resize), `move` (whole polygon translation), and `add_polygon` (used only on M2 or M3, never directly on M1, in trials that touch M1). No trial added a new M1 polygon directly. The combined set forms the complete observed repair vocabulary (trial:i01.ug.Block7_union_row10.00 through trial:i05.ug.leaf_0004.03).

### Instance Moves and Compensating M1 End Stretches

The dominant repair pattern pairs a `move_instance` with one or more `resize_end` operations on M1 polygons in the parent cell. When an instance is displaced along X, the M1 wires that abut it (landing on V0 or V1 pins inside the instance) need their near end extended to maintain the required enclosure. The resize_end delta does not equal the move delta exactly; it is typically larger, reflecting the need to recover both the lost overlap and satisfy V0.M1.EN.1 (5 nm enclosure on two opposite sides) or V1.M1.EN.1 (5&2 nm enclosure). For example, trial:i01.ug.Block7_union_row10.00 moves i1140 by +52 dbu along X and extends the high end of p3286 by +308 dbu along X. Trial:i01.ug.Block7_union_row7.19 moves i1446 by +108 dbu and extends the high end of p3317 by +128 dbu. Trial:i02.ug.Block7_union_row9.06 moves i1150 by +56 dbu and extends the high end of p3683 by +112 dbu. The resize_end delta is always strictly positive in the direction of the instance move when the end faces the moved instance.

### Low-End Resize_end

`resize_end` with `end: low` and a positive delta_dbu advances the low edge of an M1 polygon toward higher coordinates, shrinking the polygon from its lower end. This is used when a gap between two M1 shapes on one side must be widened to satisfy M1.S.1 (18 nm side-to-side) or M1.S.2 (25 nm tip-to-side). Trial:i01.ug.Block7_union_row3.15 resizes the low end of p3384 by +56 dbu, paired with moving i1623 by -36 dbu. Trial:i01.ug.Block7_union_row17.07 resizes the low end of p3187 by +56 dbu along X, paired with five instance moves of +36 dbu. Trial:i01.ug.Block7_union_row8.20 resizes the low end of p3430 by +56 dbu along X, paired with a move of -36 dbu on i1891.

### Multi-Instance Moves at Uniform Delta

When several instances must shift together to relieve a cluster of M1 spacing or enclosure violations, the repair moves all of them by the same delta. This preserves relative spacing between instances and avoids introducing new M1.S.1 violations between shapes within the moved group. Trial:i01.ug.Block7_union_row11.01 moves i1828 and i1728 both by +36 dbu. Trial:i01.ug.Block7_union_row6.18 moves six instances all by +36 dbu. Trial:i01.ug.Block7_union_row9.21 moves five instances all by +40 dbu.

### Move Granularity

Most instance move deltas are multiples of 36 dbu: 36, 72, 108, -36, -72, -108 dbu along X appear across the majority of trials (trial:i01.ug.Block7_union_row11.01, trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row13.03, trial:i01.ug.Block7_union_row14.04, trial:i01.ug.Block7_union_row17.07, and many others). A smaller set of trials uses non-36 deltas: 40 dbu (trial:i01.ug.Block7_union_row9.21, trial:i01.ug.Block7_union_row15.05 for i0913), 52 dbu (trial:i01.ug.Block7_union_row10.00 for i1140, trial:i01.ug.Block7_union_row14.04 for i0528), 56 dbu (trial:i02.ug.Block7_union_row9.06), 64 dbu (trial:i01.ug.Block7_union_row24.14 for i0561), 68 dbu (trial:i01.ug.Block7_union_row4.16), 136 dbu (trial:i01.ug.Block7_union_row13.03, trial:i01.ug.Block7_union_row15.05 for i0913). These non-36 values arise when the specific enclosure or spacing gap requires a non-grid-aligned correction to exactly satisfy the rule threshold.

Sub-grid nudges of 3-4 dbu are accepted and preserve connectivity: trial:i02.ug.leaf_0022.10 moves i0100 by +3 dbu along X, and trial:i01.ug.Block7_union_row22.12 moves i0132 by +4 dbu along X, both with n_new_in_crop ≥ 2 and conn_preserved=true.

### Y-Axis Adjustments

Vertical moves on M1 polygons or instances occur when vertical enclosure or spacing violations must be corrected. These use `op: move` on a polygon with `axis: y`, or `move_instance` with a Y-component delta. Trial:i01.ug.Block7_union_row16.06 moves i0336 and i0308 by [0,-12] and moves p3516 by y -12. Trial:i02.ug.leaf_0014.08 moves i0519 and i0524 by [0,-12] and moves p3515 by y -12. Both touch layers M1, M2, M3, V1, V2, indicating that vertical M1 adjustments propagate to vias and upper metals. Trial:i01.ug.leaf_0095.26 moves i0177 and i0184 by [0,+48] and extends the high end of p3537 along Y by +48 dbu, also touching M3 and V2.

Y-axis `resize_end` appears in trial:i03.ug.leaf_0002.04, which extends the high end of p2720 by +20 dbu along Y and retracts the low end of p3300 by -88 dbu along X in the same composite operation, also adding an M3 polygon.

### Full Polygon Resize and Move

When a single M1 polygon must shift without changing its dimensions, `op: resize` with a scalar delta_dbu translates the polygon body. Trial:i01.ug.Block7_union_row15.05 applies `resize` with delta +160 dbu to p3586 along X, paired with a move of +136 dbu on i0913. This differs from `resize_end`, which changes polygon length. Trial:i03.ug.leaf_0007.05 applies `resize` with delta +96 dbu along Y to p3592 after adjusting both its low and high ends on Y, shrinking it symmetrically: low end +(-48) and high end +(-48) dbu.

### High-Fanout Instance Moves and Crop Inflation

A single `move_instance` applied to a high-fanout instance can generate a large count of new in-crop violations. Trial:i04.ug.leaf_0006.05 moves i0235 by -108 dbu along X over a crop window spanning nearly the full design extent [1728,2068,28728,28172] and reports n_new_in_crop=173. Trial:i04.ug.leaf_0007.06 moves i0177 by [0,+48] over a similarly large window and reports n_new_in_crop=48. Both are accepted (gated_in, conn_preserved=true), indicating the harness accepts large in-crop counts when connectivity is intact. These cases demonstrate that a single-operation repair can be correct even when it incidentally touches many M1 edges across the block.

### Iterative Repair on Persistent Units

Several units appear in multiple iterations, indicating that a first-pass repair leaves residual violations that require additional passes. Block7_union_row10 is repaired in iter 1 (trial:i01.ug.Block7_union_row10.00, 6 ops) and again in iter 3 (trial:i03.ug.Block7_union_row10.00, 2 ops). Block7_union_row13 is repaired in iter 1 (trial:i01.ug.Block7_union_row13.03, 6 ops), iter 2 (trial:i02.ug.Block7_union_row13.02, 3 ops), and iter 3 (trial:i03.ug.Block7_union_row13.01, 2 ops). Block7_union_row20 is repaired in iter 1 (trial:i01.ug.Block7_union_row20.10), iter 2 (trial:i02.ug.Block7_union_row20.04), and iter 3 (trial:i03.ug.Block7_union_row20.02). leaf_0095 (iter 1, trial:i01.ug.leaf_0095.26) is followed by leaf_0011 (iter 3, trial:i03.ug.leaf_0011.07) on nearby geometry involving the same M1/M2/M3 polygons p3537, i0177, i0184. Each successive repair uses fewer operations and a smaller locus, converging toward the residual violation.

### Enclosure and Width Rule Context for resize_end Sizing

V0.M1.EN.1 requires M1 to enclose V0 by at least 5 nm on two opposite sides, or 5 nm on one side and 0 nm on the other. V0.M1.AUX.3 additionally requires V0 to be exactly as wide as M1 in the direction perpendicular to M1 length, meaning M1 cannot be wider than V0 in that direction. V1.M1.EN.1 requires 5 nm on one axis and 2 nm on the other for V1. When a `resize_end` extends an M1 polygon end over a via, the extension must bring the enclosure to at least the rule minimum while not violating M1.S.1 (18 nm side-to-side), M1.S.2 (25 nm tip-to-side), M1.S.3 (27 nm tip-to-tip for 24-36 nm edges), or M1.A.1 (minimum area 504 nm²) with respect to neighboring M1 shapes. All accepted resize_end operations in this history satisfy these constraints simultaneously, as evidenced by the zero n_new_out_of_crop counts in virtually all trials.

### Connectivity Preservation Is Necessary for Acceptance

Every accepted trial has `conn_preserved: true`. No trial in this history was accepted with `conn_preserved: false`. When combining `move_instance` and `resize_end` operations in a single repair, the set of operations must be jointly applied so that the M1 polygon end remains in overlap with the pin inside the moved instance after the move. The resize_end delta must exceed the displacement delta whenever the pre-repair overlap was exactly at the enclosure minimum (trial:i01.ug.Block7_union_row10.00 illustrates this: the resize_end of +308 dbu far exceeds the instance move of +52 dbu, extending well into the instance to ensure the enclosure gap is more than satisfied).