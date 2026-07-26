## Observed Operation Types and Outcomes

All 13 trials in the measured history were accepted (`decision: "gated_in"`, `conn_preserved: true`). The full set spans iterations 1–3 and covers units including Block6_union_row3–8 and leaf_0001, leaf_0004, leaf_0011, leaf_0015, leaf_0018.

Every accepted trial touched layers M1, M2, and V1 together (trial:i01.ug.Block6_union_row3.00, trial:i01.ug.Block6_union_row5.01, trial:i01.ug.Block6_union_row7.02, trial:i01.ug.Block6_union_row8.03, trial:i01.ug.leaf_0001.04, trial:i01.ug.leaf_0011.05, trial:i01.ug.leaf_0015.06, trial:i01.ug.leaf_0018.07, trial:i02.ug.Block6_union_row4.00, trial:i02.ug.Block6_union_row7.01, trial:i02.ug.Block6_union_row8.02, trial:i02.ug.leaf_0004.04, trial:i03.ug.leaf_0001.00). No trial in the history touches M1 in isolation from V1.

## Axis Constraint: All Operations Are Horizontal

Every `move_instance` op in the history carries a `delta_dbu` of the form `[dx, 0]` — the y-component is zero in every case (trial:i01.ug.Block6_union_row3.00, trial:i01.ug.Block6_union_row5.01, trial:i01.ug.Block6_union_row7.02, trial:i01.ug.Block6_union_row8.03, trial:i01.ug.leaf_0001.04, trial:i01.ug.leaf_0011.05, trial:i01.ug.leaf_0015.06, trial:i01.ug.leaf_0018.07, trial:i02.ug.Block6_union_row4.00, trial:i02.ug.Block6_union_row7.01, trial:i02.ug.Block6_union_row8.02, trial:i02.ug.leaf_0004.04, trial:i03.ug.leaf_0001.00). Every `resize_end` op specifies `axis: "x"` (trial:i01.ug.Block6_union_row5.01, trial:i01.ug.Block6_union_row7.02, trial:i01.ug.leaf_0001.04, trial:i01.ug.leaf_0015.06, trial:i02.ug.Block6_union_row4.00). No y-axis resize and no diagonal move appear anywhere in the history.

The GEOMETRY.NONORTHOGONAL rule (deck lines 1136–1141) fires on edges at any angle other than 0 or 90 degrees. The exclusive use of axis-aligned (`axis: "x"`) resizes and zero-y moves across all accepted trials is consistent with this hard constraint.

## resize_end Usage for Enclosure Fixes

`resize_end` operations extend one end of an M1 polygon along the x-axis. The `end` field is either `"high"` (extend the trailing/right edge outward) or `"low"` (extend the leading/left edge outward). Accepted examples:

- trial:i01.ug.Block6_union_row5.01: `resize_end` on p2072, axis x, end high, delta 92 dbu
- trial:i01.ug.Block6_union_row7.02: `resize_end` on p1903, axis x, end high, delta 124 dbu; separate `resize_end` on p1920, axis x, end low, delta 56 dbu
- trial:i01.ug.leaf_0001.04: `resize_end` on p2016, axis x, end high, delta 132 dbu
- trial:i01.ug.leaf_0015.06: `resize_end` on p1923, axis x, end high, delta 48 dbu
- trial:i02.ug.Block6_union_row4.00: `resize_end` on p2020, axis x, end high, delta 132 dbu

These are consistent with satisfying V0.M1.EN.1 (minimum 5 nm enclosure of V0 by M1 on two opposite sides) and V1.M1.EN.1 (minimum enclosure of V1 by M1: 5 nm on one side, 2 nm on the other). Extending the high or low end of an M1 polygon increases the projection-measured enclosure on the corresponding side of the via.

## Transaction Composition: Mixed move_instance and resize_end

Several accepted trials combine `move_instance` and `resize_end` ops in a single transaction:

- trial:i01.ug.Block6_union_row5.01: 4 instance moves + 1 resize_end (5 ops total)
- trial:i01.ug.Block6_union_row7.02: 2 instance moves + 2 resize_ends (4 ops total)
- trial:i01.ug.leaf_0001.04: 1 instance move + 1 resize_end (2 ops total)
- trial:i01.ug.leaf_0015.06: 2 instance moves + 1 resize_end (3 ops total)
- trial:i02.ug.Block6_union_row4.00: 2 instance moves + 1 resize_end (3 ops total)

Mixed transactions are consistently accepted. Transactions with only `move_instance` ops also succeed (trial:i01.ug.Block6_union_row3.00, trial:i01.ug.Block6_union_row8.03, trial:i01.ug.leaf_0011.05, trial:i01.ug.leaf_0018.07, trial:i02.ug.Block6_union_row7.01, trial:i02.ug.Block6_union_row8.02, trial:i02.ug.leaf_0004.04, trial:i03.ug.leaf_0001.00).

## Move Magnitude Range

Observed `delta_dbu` x-values (y is always 0) across all accepted trials:

- Small moves (4–36 dbu): trial:i02.ug.Block6_union_row7.01 (4 dbu), trial:i01.ug.Block6_union_row3.00 (72 dbu), trial:i01.ug.Block6_union_row5.01 (36 dbu), trial:i01.ug.Block6_union_row8.03 (36 dbu), trial:i01.ug.leaf_0011.05 (36 dbu), trial:i01.ug.leaf_0018.07 (36 dbu), trial:i02.ug.Block6_union_row8.02 (8 dbu, 36 dbu), trial:i03.ug.leaf_0001.00 (36 dbu), trial:i01.ug.leaf_0015.06 (28 dbu)
- Larger moves (72–112 dbu): trial:i01.ug.Block6_union_row7.02 (104 dbu, -36 dbu), trial:i01.ug.leaf_0001.04 (112 dbu), trial:i02.ug.Block6_union_row4.00 (56 dbu, 112 dbu), trial:i02.ug.leaf_0004.04 (72 dbu)

Negative delta_dbu is also accepted: trial:i01.ug.Block6_union_row7.02 uses `delta_dbu: [-36, 0]` on i0074. All move magnitudes in the history are multiples of 4 dbu.

## V0.M1.AUX.3 and V0 Co-movement

V0.M1.AUX.3 requires V0 width along the direction perpendicular to M1 length to exactly match M1 width in that direction. Because all repairs use x-axis-only moves and resizes, the perpendicular (y-axis) alignment between V0 and M1 is not disturbed. When an instance containing V0 is moved horizontally, M1 within the same instance moves with it, preserving the perpendicular co-alignment. All accepted instance-move trials satisfy this implicitly (trial:i01.ug.Block6_union_row3.00, trial:i01.ug.Block6_union_row5.01, trial:i01.ug.Block6_union_row7.02, trial:i01.ug.Block6_union_row8.03, trial:i01.ug.leaf_0001.04, trial:i01.ug.leaf_0011.05, trial:i01.ug.leaf_0015.06, trial:i01.ug.leaf_0018.07, trial:i02.ug.Block6_union_row4.00, trial:i02.ug.Block6_union_row7.01, trial:i02.ug.Block6_union_row8.02, trial:i02.ug.leaf_0004.04, trial:i03.ug.leaf_0001.00).

## Repeated Unit Repair Across Iterations

Unit Block6_union_row7 was repaired in both iteration 1 and iteration 2, at the same locus (8368, 8748, 14400, 9612):

- trial:i01.ug.Block6_union_row7.02 used 4 ops (2 moves, 2 resize_ends), accepted
- trial:i02.ug.Block6_union_row7.01 used 1 op (move i0093 by 4 dbu), accepted

The design_state changed between iterations (from `685706506...` to `35ec6414a...`), reflecting that the first repair altered global state and left a residual small offset that iteration 2 corrected with a 4 dbu nudge. A small follow-up move on the same instance (i0093) in a subsequent iteration is consistent with iterative convergence.

Unit Block6_union_row8 similarly received repairs in both iteration 1 (trial:i01.ug.Block6_union_row8.03, 1 op) and iteration 2 (trial:i02.ug.Block6_union_row8.02, 2 ops), at overlapping loci, across different design states.

Unit leaf_0001 received repairs in iteration 1 (trial:i01.ug.leaf_0001.04) and iteration 3 (trial:i03.ug.leaf_0001.00), indicating that this unit required multiple passes to reach full DRC closure.

## Connectivity Preservation Is Universal

Every trial records `conn_preserved: true` and `n_new_in_crop: 0`, `n_new_out_of_crop: 0` (trial:i01.ug.Block6_union_row3.00, trial:i01.ug.Block6_union_row5.01, trial:i01.ug.Block6_union_row7.02, trial:i01.ug.Block6_union_row8.03, trial:i01.ug.leaf_0001.04, trial:i01.ug.leaf_0011.05, trial:i01.ug.leaf_0015.06, trial:i01.ug.leaf_0018.07, trial:i02.ug.Block6_union_row4.00, trial:i02.ug.Block6_union_row7.01, trial:i02.ug.Block6_union_row8.02, trial:i02.ug.leaf_0004.04, trial:i03.ug.leaf_0001.00). No trial introduced or removed nets. All resize_end deltas in the history are positive (net extension, not shrink), which keeps area above the M1.A.1 minimum (504 nm²) and does not risk creating sub-minimum-width necks.