## Repair Patterns

### Unit-gate channel: x-axis instance moves with paired polygon resizes

All seven unit-gate trials in iter 1 (trial:i01.ug.Block2_union_row1.00, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0001.03, trial:i01.ug.leaf_0004.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0011.06) were accepted with decision `gated_in` and n_new_out_of_crop=0. Every one of them moves one or more instances in +x and co-touches layers ["M1","M2","V1"]. Move magnitudes that were accepted: 36 dbu (trial:i01.ug.Block2_union_row1.00, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.leaf_0004.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0011.06), 64 dbu (trial:i01.ug.Block2_union_row5.02), and 128 dbu (trial:i01.ug.leaf_0001.03).

When an instance move shifts M2 endpoints away from adjacent polygons or via stacks, the repair must accompany the move with a `resize_end` on the affected M2 polygon to maintain continuity. This pairing occurred in four of the seven iter-1 unit-gate trials:

- trial:i01.ug.Block2_union_row3.01 paired a 36-dbu +x instance move with a 36-dbu high-x-end resize of p1040.
- trial:i01.ug.Block2_union_row5.02 paired a 64-dbu +x instance move with 64-dbu high-x-end resizes of p1059 and p1057.
- trial:i01.ug.leaf_0001.03 paired a 128-dbu +x instance move with a 184-dbu high-x-end resize of p1065 and a 176-dbu low-x-end resize of p957.
- trial:i01.ug.leaf_0011.06 paired a 36-dbu +x instance move with a 36-dbu high-x-end resize of p1052.

In trial:i01.ug.leaf_0001.03 the polygon endpoint extensions (176–184 dbu) exceed the instance move (128 dbu). The additional stretch beyond the move magnitude provides extra enclosure margin so that via enclosure rules (V1.M2.EN.2, V2.M2.EN.1) remain satisfied after the instance is repositioned.

All resize_end operations in the unit-gate channel target the x-axis (high or low end), consistent with M2 running horizontally in this design. No y-axis polygon resizes appear in unit-gate M2 repairs in this history.

### Unit-gate channel: iter-4 mixed x/y repair

trial:i04.ug.leaf_0002.01 (iter 4, unit:leaf_0002) used a compound operation: instances i0099, i0111, i0061, i0066 and polygon p937 were all moved -64 dbu in x, while instance i0063 and polygon p1036 were moved +36 dbu in y. This trial co-touched ["M1","M2","M4","M5","V1","V4"], a deeper stack than any iter-1 unit-gate trial. The trial was accepted (`gated_in`) with n_new_in_crop=1, meaning one new violation appeared inside the local crop, but connectivity was preserved and the repair was committed. No iter-1 unit-gate trial introduced any in-crop violations (all show n_new_in_crop=0), so the tolerance of n_new_in_crop=1 is a measured outcome specific to this iter-4 case, not a general budget.

### CU-pool channel: VIA_VIA23_1_3_36_36 y-axis shrink

Two cu_pool trials targeted the same cell definition and applied an identical operation structure:

- trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 (iter 1, design_state a1a0a882...): shrank the VIA_VIA23_1_3_36_36 via cell shape on M3 by -40 dbu in y, and shrank M2/M3 polygons p965, p964, p963, p962 each by -64 dbu in y. Result: delta_total = -8, applied.
- trial:i02.cu.def:VIA_VIA23_1_3_36_36.00 (iter 2, design_state 376b1311...): identical structure on polygons p961, p960, p959, p958. Result: delta_total = -8, applied.

Both trials touch layers ["M2","M3","V2"] and leave M1/V1 untouched. Each application removes exactly 8 violations. The operation is repeatable across design states: the same -40-dbu via cell adjustment and -64-dbu M2/M3 polygon y-shrink yielded -8 each time, across two successive design snapshots.

M2 polygon y-axis shrinks appear exclusively in cu_pool via-cell repairs in this history. Applying a y-shrink of 64 dbu to M2 polygons associated with VIA_VIA23_1_3_36_36 is a directly measured, repeatable fix (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, trial:i02.cu.def:VIA_VIA23_1_3_36_36.00).

## Layer co-move requirements

M2 repairs in the unit-gate channel always co-touch M1 and V1 (trial:i01.ug.Block2_union_row1.00, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0001.03, trial:i01.ug.leaf_0004.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0011.06, trial:i04.ug.leaf_0002.01). Moving M2 instance geometry without the corresponding M1 and V1 via-stack geometry breaks connectivity; all accepted repairs move these layers together.

M2 repairs in the cu_pool channel co-touch M3 and V2, never M1 or V1 (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, trial:i02.cu.def:VIA_VIA23_1_3_36_36.00). The M2/V2 interface is addressed by shrinking the M2 polygon y-extent together with the V2 cell shape and the M3 polygon, as a coordinated group.

## Decision outcomes

No trial in this history received a rejection or non-improvement decision. All unit-gate trials show decision=`gated_in` with conn_preserved=true. Both cu_pool trials show decision=`applied` with conn_preserved=true and delta_total=-8 each. The history contains no examples of a rejected M2 repair or a move that introduced violations outside the crop.