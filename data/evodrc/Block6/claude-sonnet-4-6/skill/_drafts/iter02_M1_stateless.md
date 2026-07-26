## General Acceptance Pattern

Every trial in both iterations was accepted with `decision:"gated_in"`, `conn_preserved:true`, and `n_new_in_crop:0` / `n_new_out_of_crop:0`. This holds across all 12 trials from trial:i01.ug.Block6_union_row3.00 through trial:i02.ug.leaf_0004.04. No trial introduced a new DRC violation or broke connectivity on M1, M2, or V1.

## Channel and Operation Type

All repairs run through the `unit_gate` channel. Use only `move_instance` and `resize_end` operations for M1 repair in this design; the complete measured history contains no other operation types (trial:i01.ug.Block6_union_row3.00 through trial:i02.ug.leaf_0004.04).

## Axis Constraint: X Only

All operations in the history are strictly on the x-axis. Every `move_instance` delta is of the form `[delta_x, 0]` with zero y-component, and every `resize_end` specifies `"axis":"x"`. Never apply y-direction moves or y-axis resizes to M1 in this design; no y-direction operation appears in any accepted trial across both iterations (verified in trial:i01.ug.Block6_union_row3.00 through trial:i02.ug.leaf_0004.04).

## Move Instance: Magnitude Range and Sign

Move magnitudes span a wide range and both positive and negative x-deltas appear in accepted trials. Magnitudes observed: 4 dbu (trial:i02.ug.Block6_union_row7.01, instance i0093), 8 dbu (trial:i02.ug.Block6_union_row8.02, instance i0213), 28 dbu (trial:i01.ug.leaf_0015.06), 36 dbu (trial:i01.ug.Block6_union_row8.03, trial:i01.ug.leaf_0011.05, trial:i01.ug.leaf_0018.07, trial:i02.ug.Block6_union_row8.02), 56 dbu (trial:i02.ug.Block6_union_row4.00, instance i0319), 72 dbu (trial:i01.ug.Block6_union_row3.00, trial:i02.ug.leaf_0004.04), 104 dbu (trial:i01.ug.Block6_union_row7.02, instance i0093), 112 dbu (trial:i01.ug.leaf_0001.04, trial:i02.ug.Block6_union_row4.00). A negative x-move of -36 dbu on instance i0074 was accepted in trial:i01.ug.Block6_union_row7.02 without violating M1.S.1 or M1.W.1, confirming that small negative x-moves are not categorically forbidden. Do not treat positive-only moves as required; mix signs when the geometry calls for it, as demonstrated in trial:i01.ug.Block6_union_row7.02.

## Resize End: Extend High-X Edge as Primary Strategy

The dominant resize pattern is extending the high-x (right) edge of an M1 polygon with a positive delta. This appears in five distinct trials: trial:i01.ug.Block6_union_row5.01 (+92 dbu on p2072, end:high), trial:i01.ug.Block6_union_row7.02 (+124 dbu on p1903, end:high), trial:i01.ug.leaf_0001.04 (+132 dbu on p2016, end:high), trial:i01.ug.leaf_0015.06 (+48 dbu on p1923, end:high), and trial:i02.ug.Block6_union_row4.00 (+132 dbu on p2020, end:high). Apply high-x extension to lengthen M1 polygons when enclosure violations (V0.M1.EN.1 or V1.M1.EN.1) arise on the right side of the via.

## Resize End: Low-X Edge Shift

A low-x end resize with a positive delta (+56 dbu on polygon p1920, end:low) was accepted in trial:i01.ug.Block6_union_row7.02. A positive delta on the low end moves the left edge rightward, narrowing the polygon from the left. This passed M1.W.1 (minimum width 18 nm) and M1.A.1 (minimum area 504 nm²) in combination with the accompanying move and high-end resize in the same trial. Apply low-x end retraction only when the companion high-end extension maintains minimum width and area on the same polygon.

## Coordinated Multi-Instance Group Moves

Several trials move multiple instances simultaneously within a single repair step. Group sizes: 3 instances in trial:i01.ug.Block6_union_row3.00, 4 instances in trial:i01.ug.Block6_union_row5.01, 2 instances in trial:i01.ug.Block6_union_row7.02 and trial:i01.ug.leaf_0015.06, 2 instances in trial:i02.ug.Block6_union_row4.00. All group moves preserve M1.S.1 spacing between co-moved instances and between moved and static M1 edges. Move all instances in a row or unit together when a single-instance move would create a new M1.S.1 or M1.S.2 violation against the unmoved neighbors.

## Iterative Refinement Across Design States

The design state changes between iteration 1 (`685706506817f4f5a58d885e68808402b61fcf189fed22cc344fa6dec38c0f99`) and iteration 2 (`35ec6414a52ad9c906954900ee4dc0046bac1f44990f43b2bbdc06464f8e14a4`), confirming that iter1 committed changes form the baseline for iter2. Two units received repairs in both iterations:

- **Block6_union_row7**: iter1 applied large corrections (moves of +104 and -36 dbu, resizes of +124 and +56 dbu) in trial:i01.ug.Block6_union_row7.02; iter2 applied a residual fine correction of +4 dbu on the same instance i0093 in trial:i02.ug.Block6_union_row7.01.
- **Block6_union_row8**: iter1 moved instance i0078 by +36 dbu in trial:i01.ug.Block6_union_row8.03; iter2 moved instances i0213 (+8 dbu) and i0071 (+36 dbu) in trial:i02.ug.Block6_union_row8.02.

Apply coarse corrections first, then expect a residual fine-correction pass in the subsequent iteration. A 4 dbu move is the smallest observed adjustment (trial:i02.ug.Block6_union_row7.01) and is sufficient to resolve a residual rule violation.

## V1.M1.EN.1 Enclosure Preservation

All trials touch layers M1, M2, and V1 together. The two-opposite-sides enclosure requirement of V1.M1.EN.1 (5 nm on one side, minimum 2 nm on the opposite side) is maintained in every accepted trial because instance moves carry the M1 polygon and the V1 via together, preserving relative geometry. Resize operations that extend M1 only (without moving the via) increase enclosure on the extended side and do not reduce it on the opposing side. Both patterns are confirmed safe: trial:i01.ug.Block6_union_row5.01 (resize only on p2072) and trial:i01.ug.Block6_union_row7.02 (mixed moves and resizes). Do not resize an M1 polygon inward on the side that already provides the minimum 2 nm enclosure for a V1.

## M1.S.1, M1.S.2, and Corner-Spacing Safety at Observed Move Magnitudes

No spacing violation (M1.S.1, M1.S.2, M1.S.3, M1.S.6) was introduced at any observed move magnitude from 4 dbu to 112 dbu (trial:i02.ug.Block6_union_row7.01 and trial:i01.ug.leaf_0001.04, respectively). The grid increment used in this design (multiples of 4 dbu) aligns with the 18 nm minimum spacing requirement of M1.S.1 and the 25 nm tip-to-side requirement of M1.S.2. Move and resize operations stay on 4 dbu grid steps in all accepted trials.

## Non-Orthogonal Geometry: No Violations Introduced

The GEOMETRY.NONORTHOGONAL rule applies to M1. All accepted move and resize operations maintain axis-aligned (0° and 90°) M1 edges because operations are restricted to x-axis translation and x-axis end extension. No diagonal geometry is introduced by any repair in this history (trial:i01.ug.Block6_union_row3.00 through trial:i02.ug.leaf_0004.04).

## M1.R.0 Redundancy: Not Triggered

The M1.R.0 rule flags M1 islands enclosing exactly one small V0 via near large empty M1 regions. No M1.R.0 violation arose in any trial. The unit_gate repairs move and extend existing multi-via M1 polygons rather than creating isolated single-via islands, which keeps repaired polygons outside the M1.R.0 detection condition (trial:i01.ug.Block6_union_row3.00 through trial:i02.ug.leaf_0004.04).