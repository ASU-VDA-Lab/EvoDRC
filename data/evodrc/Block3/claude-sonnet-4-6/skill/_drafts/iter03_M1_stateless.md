## Operation Outcomes

All thirteen trials in this history were accepted (decision=gated_in, conn_preserved=true). Twelve of the thirteen introduced zero new in-crop DRC violations; one trial introduced ten.

---

## Safe Operation Patterns

**Positive-x instance move paired with resize_end(x, high):** Every trial that moved instances in the positive-x direction and simultaneously extended one or more M1 polygon high-x edges produced zero new in-crop violations. This pattern is confirmed across seven trials: trial:i01.ug.Block3_union_row1.00 (instances +136 dbu, polygons high-x +192 dbu), trial:i01.ug.Block3_union_row5.02 (instance +36 dbu, polygon +36 dbu), trial:i01.ug.Block3_union_row8.03 (four instances +72 to +108 dbu, four polygon high-x edges +92 to +164 dbu), trial:i01.ug.leaf_0007.05 (instances +36 dbu, polygons +56 dbu), trial:i01.ug.leaf_0008.06 (instances +4 to +136 dbu in x, polygon p1261 high-x +92 dbu, polygon p1159 high-y +20 dbu), trial:i01.ug.leaf_0012.08 (instance +72 dbu, polygon +108 dbu), and trial:i02.ug.leaf_0002.01 (instance +104 dbu, polygon +128 dbu).

**Instance move without polygon resize:** Trials that moved instances without any accompanying polygon resize also produced zero new violations: trial:i01.ug.Block3_union_row2.01 (two instances +36 dbu in x), trial:i01.ug.leaf_0006.04 (two instances +36 dbu in x), trial:i01.ug.leaf_0009.07 (one instance +36 dbu in x).

**Negative-x instance moves in iterations 1 and 2:** Moving a single instance -36 dbu in x produced zero new violations in trial:i01.ug.leaf_0013.09 (design state fa7319..., locus [6696,9376,8048,9612]) and in trial:i02.ug.leaf_0001.00 (design state cd809b..., locus [7276,2268,7704,3132]).

**y-direction resize at high end:** A resize_end(y, high, +20 dbu) on polygon p1159 in trial:i01.ug.leaf_0008.06 produced zero new violations. This is the only y-axis resize in the history; it is safe at this magnitude in that design state.

---

## Violation-Producing Operation

Trial trial:i03.ug.leaf_0003.02 moved instance i0099 by -36 dbu in x, with no accompanying polygon resize, and produced 10 new in-crop violations (n_new_in_crop=10). The trial was still accepted because conn_preserved=true. This trial operated on design state 382d59... (the iteration-3 state) with a large locus [1728,3148,11016,9812] that spans most of the design footprint.

The identical delta (-36 dbu, single instance move, no polygon resize) caused zero new violations in earlier design states (trial:i01.ug.leaf_0013.09, trial:i02.ug.leaf_0001.00) but ten violations in the iteration-3 state (trial:i03.ug.leaf_0003.02). Do not apply a bare negative-x instance move in the iteration-3 design state without a verification pass on the resulting in-crop violation count.

When a negative-x move is required, pair it with a polygon adjustment to compensate for the shift, following the pattern confirmed to be safe in trial:i01.ug.Block3_union_row1.00, trial:i01.ug.leaf_0007.05, and trial:i01.ug.leaf_0012.08, where instance moves were always accompanied by resize_end(x, high) operations that kept enclosure margins intact.

---

## resize_end Delta vs. move_instance Delta

In every trial where both a move_instance and a resize_end(x, high) appear on related shapes, the resize delta exceeds the move delta:

- trial:i01.ug.Block3_union_row1.00: move +136 dbu, resize +192 dbu (ratio ~1.41)
- trial:i01.ug.Block3_union_row8.03: moves +72 to +108 dbu, resizes +92 to +164 dbu (ratios ~1.28 to ~1.52)
- trial:i01.ug.leaf_0007.05: move +36 dbu, resize +56 dbu (ratio ~1.56)
- trial:i01.ug.leaf_0012.08: move +72 dbu, resize +108 dbu (ratio 1.50)
- trial:i02.ug.leaf_0002.01: move +104 dbu, resize +128 dbu (ratio ~1.23)

When pairing a move_instance with a resize_end(x, high), set the polygon extension delta strictly larger than the instance move delta. A resize matching the move delta exactly (as in trial:i01.ug.Block3_union_row5.02, +36 move, +36 resize) is the lower bound observed without new violations, but all larger-ratio cases were also clean.

---

## M1 Co-modification with V1 and M2

Every trial in this history that modified M1 also modified V1 and M2 in the same operation set. Trial trial:i01.ug.leaf_0008.06 additionally modified M3. No trial in this history modifies M1 without also touching V1 and M2; always include V1 and M2 in the touched-layers set when adjusting M1 positions or extents, as confirmed across all thirteen trials.

---

## High-End Resizing

All resize_end operations in the history target the "high" end of either the x or y axis. No low-end (end="low") resizing appears in any trial. When extending an M1 polygon, extend the high-x or high-y edge, as confirmed in trial:i01.ug.Block3_union_row1.00, trial:i01.ug.Block3_union_row8.03, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0008.06, trial:i01.ug.leaf_0012.08, trial:i02.ug.leaf_0002.01, and trial:i02.ug.leaf_0002.01.

---

## Design-State Sensitivity

The design state changed three times across the history: fa7319... (iteration 1, trials i01.ug.Block3_union_row1.00 through i01.ug.leaf_0013.09), cd809b... (iteration 2, trials i02.ug.leaf_0001.00 and i02.ug.leaf_0002.01), and 382d59... (iteration 3, trial i03.ug.leaf_0003.02). Operations that were clean in earlier states produced violations in state 382d59.... Never assume that an operation that succeeded in a prior iteration state is automatically safe in a later iteration state; verify in-crop violation counts after each iteration-state transition.