## Operation Patterns Observed Across All Trials

Every trial in the measured history (12 total across iterations 1 and 2) was accepted with `decision: gated_in`, `conn_preserved: true`, `n_new_in_crop: 0`, and `n_new_out_of_crop: 0`. No trial introduced new DRC violations on M1 or any co-touched layer. All prescriptive guidance below derives from this set of accepted trials.

---

## Move-Instance and Resize-End Pairing

The dominant repair pattern combines a `move_instance` on an instance with a `resize_end` (axis `x`, end `high`) on one or more M1 polygons connected to that instance. This co-motion pattern appeared in trial:i01.ug.Block3_union_row1.00, trial:i01.ug.Block3_union_row5.02, trial:i01.ug.Block3_union_row8.03, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0012.08, and trial:i02.ug.leaf_0002.01.

When you move an instance by `+dx` in x, extend the high x-end of every M1 polygon that was previously stretched tightly between that instance and its neighbor by at least `dx` dbu — and frequently more. In trial:i01.ug.Block3_union_row1.00 each of three instances moved +136 dbu while the connected M1 polygon high-end was extended +192 dbu. In trial:i01.ug.leaf_0007.05 two instances each moved +36 dbu while their M1 polygons were extended +56 dbu. In trial:i01.ug.leaf_0012.08 an instance moved +72 dbu while the polygon was extended +108 dbu. The resize delta consistently exceeds or equals the move delta; do not resize by exactly the move delta when extra enclosure margin is needed to satisfy V0.M1.EN.1 or V1.M1.EN.1.

Instance-only moves (no polygon resize) are also valid when no enclosure margin is at risk. trial:i01.ug.Block3_union_row2.01 moved two instances by +36 dbu each without any polygon operation, and trial:i01.ug.leaf_0006.04 moved two instances by +36 dbu each without resizes, both with zero new violations. Apply this lighter form only when both the before and after positions leave the M1 enclosure of any co-located V0 or V1 comfortably above 5 nm on the constraining sides per V0.M1.EN.1 and V1.M1.EN.1.

---

## Resize-End Direction: Always High, Predominantly X-Axis

All `resize_end` operations in the history target `end: high`. No `end: low` operation appears in any accepted trial. Extend the far (high) end of an M1 segment to gain enclosure or spacing clearance; do not retract the near (low) end when the high end is the natural growth direction.

All resize operations except one are on `axis: x`. The single y-axis resize in the history (+20 dbu, polygon p1159, trial:i01.ug.leaf_0008.06) occurred alongside an x-axis resize on a different polygon in the same trial, and that trial also touched M3 in addition to M1, M2, and V1. Use y-axis resizes only when the violation geometry is orthogonal to the principal M1 run direction; x-axis extension is the standard path.

---

## Delta Quantization

All measured move deltas are multiples of 36 dbu (36, 72, 108, 136, 104) with the single exception of 104 dbu in trial:i02.ug.leaf_0002.01. The 36 dbu increment is the base grid step; 104 is close to 3×36 (108) and may reflect a constraint-derived snap. Prefer 36 dbu multiples when choosing move magnitudes; if a non-multiple is required, trial:i02.ug.leaf_0002.01 shows that non-36-aligned moves can be accepted without violations when the enclosure and spacing margins permit.

Polygon resize deltas (x-axis) observed across accepted trials: 36, 56, 92, 108, 128, 164, 192 dbu. These are not strict multiples of 36; the resize amount is determined by the required enclosure gain, not by grid quantization alone.

---

## Multi-Instance Coordination Within a Locus

Several trials moved multiple instances within a single locus. trial:i01.ug.Block3_union_row1.00 coordinated three instances (i0233, i0246, i0205) each moved +136 dbu with their connected polygons extended +192 dbu, all within a single accepted trial. trial:i01.ug.Block3_union_row8.03 coordinated four instances (i0017, i0016, i0019, i0021) with non-uniform deltas (+108, +72, +72, +72 dbu) and corresponding polygon extensions (+164, +128, +128, +92 dbu), still zero violations. When the locus spans multiple instances that must all shift together to avoid intra-locus spacing violations (M1.S.1, M1.S.2), move them simultaneously in one trial rather than sequentially.

---

## Connectivity Preservation Across All Trials

Every trial preserved connectivity (`conn_preserved: true`). When pairing `move_instance` with `resize_end`, the resize must extend the M1 polygon far enough to maintain overlap with any V0 or V1 vias that depend on that polygon for landing. V0.M1.EN.1 requires 5 nm enclosure on two opposite sides (or 5 & 0 with endpoint-zero relief). V1.M1.EN.1 requires 5 & 2 nm enclosure on two opposite sides. In trial:i01.ug.Block3_union_row1.00 the +192 dbu resize versus +136 dbu move provides 56 dbu of additional margin beyond the raw instance shift, which trial:i01.ug.Block3_union_row8.03 confirms is sometimes necessary (polygon p1257 gained only +92 dbu from a +72 dbu move, a smaller surplus, and was still accepted). The minimum safe surplus depends on the via position within the polygon; always verify that after the resize the via remains enclosed by at least 5 nm on the binding sides before committing.

---

## Negative Moves

Negative x-direction moves are accepted. trial:i01.ug.leaf_0013.09 moved instance i0023 by -36 dbu (no polygon resize) with zero violations. trial:i02.ug.leaf_0001.00 moved instance i0233 by -36 dbu (no polygon resize) with zero violations. Neither negative-move trial required a polygon resize, indicating that moving an instance in the -x direction typically relaxes the polygon's enclosure margin on the high end rather than tightening it, making a compensating resize unnecessary. Do not add a high-end resize when moving an instance in the -x direction unless the move also compresses the polygon against a via on its low side.

---

## Layer Co-Touch Profile

M1 is co-touched with M2 and V1 in every accepted trial. In trial:i01.ug.leaf_0008.06 M3 is additionally touched. No trial touches M1 in isolation. When planning an M1 repair, account for the effect on V1 enclosure (V1.M1.EN.1) and on M2 geometry in the same locus. The consistent M2 co-touch means M1 polygon extensions in x do not in practice cause M2 spacing problems within these loci, as all trials were accepted; however, this observation is locus-specific and does not generalize beyond the loci represented in the history.

---

## Design State and Iteration Boundary

Iteration 1 trials (trial:i01.ug.Block3_union_row1.00 through trial:i01.ug.leaf_0013.09) all operated from design state `fa7319ee...`. Iteration 2 trials (trial:i02.ug.leaf_0001.00 and trial:i02.ug.leaf_0002.01) operate from design state `cd809b6a...`, confirming that the iteration-1 repairs were committed before iteration 2 began. Iteration 2 repairs are incrementally smaller in op count (1-2 ops per trial vs. up to 8 in iteration 1), consistent with residual violations remaining after the bulk of the work was done in iteration 1.