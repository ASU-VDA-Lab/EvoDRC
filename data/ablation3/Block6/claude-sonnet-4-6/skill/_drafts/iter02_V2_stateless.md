**V2 Shape Sizing and Positioning Along X (M3-Parallel Axis)**

In trial:i02.cu.def:VIA_VIA23_1_3_36_36.00, all five operations targeted the x-axis exclusively, acting on three V2 shapes within cell `VIA_VIA23_1_3_36_36`. The sequence combined `move_via_shape` and `resize_via_shape` on the same shapes: shape 0 received a −144 dbu move followed by a +288 dbu resize; shape 1 received only a +288 dbu resize; shape 2 received a +144 dbu move followed by a +288 dbu resize. This asymmetric but balanced pattern — outward moves on the outer shapes paired with uniform positive resizes on all three — reduced the unit-whole-design violation count from 159 to 81, a net delta of −78, with connectivity preserved (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00).

**Resize Before or With Move: Order Within a Shape Matters**

Each shape that received both a move and a resize had the move applied first (lower op index), then the resize. The outer shapes (indices 0 and 2) were displaced symmetrically away from center (−144 dbu and +144 dbu respectively) before being widened (+288 dbu each). Shape 1, the center shape, received only the resize. Apply moves to outer shapes before resizing so that the resize extends from the correct post-move anchor; trial:i02.cu.def:VIA_VIA23_1_3_36_36.00 demonstrates this ordering produced a net −78 improvement.

**Minimum Width Compliance Under V2.W.1**

V2.W.1 requires a minimum V2 width of 18 nm along the M3 length direction. The +288 dbu resizes applied in trial:i02.cu.def:VIA_VIA23_1_3_36_36.00 expand shapes along x. Resizes must not shrink V2 below the 18 nm minimum; only positive (expanding) x-resizes were used in this trial, and the result was a net violation reduction, confirming that expansion along x is a safe direction when V2 shapes are undersized or mis-spaced relative to V2.W.1 (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00).

**Spacing Rules V2.S.1–V2.S.4: Multi-Shape Simultaneous Adjustment**

V2.S.1 governs minimum projection-space between V2 instances on the same or parallel M3 tracks (18 nm same-track, 27 nm not-aligned parallel, 18 nm aligned parallel). V2.S.2 sets a 23 nm euclidean corner-to-corner minimum for shapes both carrying a 5 nm M3 end-cap. V2.S.3 sets a 30 nm euclidean corner-to-corner minimum for shapes both without a 5 nm end-cap. V2.S.4 sets a 27 nm euclidean corner-to-corner minimum between one end-capped and one non-end-capped shape. When multiple V2 shapes in a via cell are spacing-violating, adjusting all of them in the same repair pass — as done across the three shapes in trial:i02.cu.def:VIA_VIA23_1_3_36_36.00 — achieves a larger net reduction (−78) than addressing a single shape in isolation would be expected to achieve, because spacing violations are pairwise and fixing one edge of a pair requires the companion shape to also move or resize.

**M3 Enclosure (V2.M3.EN.2) and Containment (V2.AUX.1, V2.M3.AUX.2)**

V2.M3.EN.2 requires M3 to enclose V2 by at least 5 nm on two opposite sides (either 5&5 nm or 5&0 nm in projection). V2.AUX.1 requires V2 to lie entirely inside the intersection of M2 and M3. V2.M3.AUX.2 requires V2 width perpendicular to M3 length to exactly match M3 width. The trial touched M2, M3, and V2 together (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00), and connectivity was preserved, confirming that coordinated adjustment of all three layers is required when V2 x-resizes risk violating enclosure or containment rules. Do not resize V2 along x without verifying that M3 either already provides sufficient enclosure or is co-adjusted in the same operation.

**M2 Enclosure (V2.M2.EN.1)**

V2.M2.EN.1 requires M2 to enclose V2 by at least 5 nm on at least two opposite sides. The trial touched M2 as part of the multi-layer repair, ensuring that x-axis expansion of V2 did not violate M2 enclosure (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00). Expand V2 along x only when M2 already provides sufficient enclosure in x, or co-resize M2 in the same pass.

**Effective Repair Pattern for Via Cell V2**

The single measured repair for V2 at iteration 2 establishes the following concrete pattern: within a multi-shape via cell, apply outward ±18 nm (±144 dbu) moves to outer V2 shapes first, then apply uniform +36 nm (+288 dbu) x-resizes to all shapes, co-touching M2 and M3 in the same operation. This produced a 49% reduction in violations (159→81) with connectivity intact (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00). Use this as the baseline operation set for `VIA_VIA23_1_3_36_36`-class cells in the cu_pool channel.