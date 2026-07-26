## Operation History Overview

All 18 recorded trials belong to Block1, channel "unit_gate", and carry `decision: gated_in` with `conn_preserved: true`. M1 is touched alongside M2 and V1 in every trial. No trial produced `n_new_out_of_crop > 0`, confirming that the repair strategy keeps displaced violations confined to the crop region.

## Move Quantum

The dominant X-axis move delta across the history is 36 dbu and its integer multiples. Trials applying 36-dbu multiples — 36 dbu (trial:i01.ug.Block1_union_row9.08, trial:i01.ug.leaf_0004.09), 72 dbu (trial:i03.ug.Block1_union_row3.00, trial:i03.ug.leaf_0004.01), 108 dbu (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row8.07) — each produced zero or a small, bounded number of new in-crop violations (0–4). Apply move deltas that are multiples of 36 dbu; move deltas of -32 dbu appear in trial:i01.ug.Block1_union_row6.06 and trial:i01.ug.Block1_union_row8.07 and each trial introduced at least 1 new in-crop violation, showing -32 dbu is not a safe grid increment. Avoid the sub-grid delta pattern seen in trial:i04.ug.leaf_0004.03, which used `"delta":4` (not `"delta_dbu"`) and produced 80 new in-crop violations — the highest violation count in the entire history.

## Resize-End Operations

`resize_end` operations (asymmetric, one end only) appear across iterations 1–3 (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row3.03, trial:i01.ug.Block1_union_row4.04, trial:i01.ug.Block1_union_row5.05, trial:i01.ug.leaf_0020.10, trial:i03.ug.leaf_0004.01). When paired with 36-dbu-aligned deltas (36, 52, 72, 92, 128 dbu), these trials produced at most 4 new in-crop violations and zero out-of-crop violations. The single symmetric `resize` operation (`"op":"resize"`, delta 36 dbu on polygon p1390) occurs in trial:i01.ug.leaf_0031.11 and introduced 4 new in-crop violations. Prefer `resize_end` with 36-dbu-aligned deltas (trial:i01.ug.Block1_union_row3.03, trial:i01.ug.leaf_0020.10) because adjusting only one end leaves the far edge of the M1 polygon undisturbed, reducing the risk of creating a new M1.W.1 or V0.M1.EN.1 violation on the unchanged side.

When resizing the trailing (low) end of an M1 polygon, apply `end:"low"` resize_end as in trial:i01.ug.Block1_union_row5.05 on p1301 and trial:i01.ug.leaf_0020.10 on p1253, which retract only the tip and preserve M1.S.1 compliance on the side edges of adjacent polygons.

The resize_end deltas observed (52, 72, 92, 128 dbu) all exceed 18 dbu, which corresponds to the M1.W.1 minimum width of 18 nm. Use resize_end deltas that leave the resulting polygon edge position consistent with this floor; trial:i01.ug.Block1_union_row1.00 (128 dbu) and trial:i01.ug.Block1_union_row3.03 (92 dbu) confirm that large end-aligned extensions remain violation-free when the starting geometry is legal.

## Via Replacement as Alternative to Instance Move

Trial trial:i02.ug.leaf_0004.02 resolved the row4 locus by deleting instance i0300 and adding a new VIA_VIA12 via at origin [5904, 6300], producing zero new violations. This same locus had required a multi-op move-plus-resize_end approach in trial:i01.ug.Block1_union_row4.04 in iteration 1. When a via instance move alone cannot satisfy V0.M1.EN.1 or V0.M1.AUX.3 constraints, delete-and-re-place of the via at the corrected grid position (trial:i02.ug.leaf_0004.02) eliminates the enclosure error without requiring M1 polygon resizing.

## Diagonal Instance Moves

The only instance move with a non-zero Y component is trial:i01.ug.Block1_union_row4.04, where instance i0300 carries delta_dbu [-36, -36]. That trial produced 0 new violations, but the same instance i0300 was subsequently deleted in trial:i02.ug.leaf_0004.02 and replaced with a new via, confirming that the diagonal placement introduced a configuration requiring replacement rather than further adjustment. Avoid diagonal instance moves (non-zero Y delta); the history shows they necessitate subsequent corrective passes, as demonstrated by trial:i01.ug.Block1_union_row4.04 and trial:i02.ug.leaf_0004.02.

## Violation Budget by Operation Count and Delta

Across the 18 trials, `n_new_in_crop` values are: 0 for 12 trials, 1 for 2 trials (trial:i01.ug.Block1_union_row6.06, trial:i02.ug.Block1_union_row6.01), 4 for 2 trials (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.leaf_0031.11), and 80 for 1 trial (trial:i04.ug.leaf_0004.03). The 80-violation outcome in trial:i04.ug.leaf_0004.03 is the direct result of using a sub-grid 4-unit delta. For trials using 36-dbu-aligned moves and resize_end, the in-crop violation count stays at 4 or below. Use 36-dbu-aligned deltas to bound new violation counts at 4 or fewer; the evidence from trial:i04.ug.leaf_0004.03 shows that sub-grid moves cause runaway violation accumulation.

## Locus-Specific Recurrence: Row6

The row6 locus ([8152,7668,13752,8532]) was visited in two successive iterations. In iteration 1, trial:i01.ug.Block1_union_row6.06 moved instance i0455 by -32 dbu, leaving 1 residual in-crop violation. In iteration 2, trial:i02.ug.Block1_union_row6.01 applied five move operations — all at +36 dbu for i0097, i0434, i0436, i0116, and -36 dbu reversing i0455 — yet still recorded 1 new in-crop violation. The recurrence of this locus across two iterations confirms that -32 dbu moves do not fully resolve violations; use only 36-dbu-aligned moves at this locus, as the iter-2 attempt (trial:i02.ug.Block1_union_row6.01) with 36-dbu increments was closer to resolution than the iter-1 -32 dbu attempt (trial:i01.ug.Block1_union_row6.06).

## Locus-Specific Recurrence: Row3

The row3 locus ([5128,4428,11376,5292]) was visited in iteration 1 (trial:i01.ug.Block1_union_row3.03) and iteration 3 (trial:i03.ug.Block1_union_row3.00). The iteration-1 attempt combined a 36-dbu move with a 92-dbu resize_end on p1370, producing 0 new violations. The iteration-3 follow-up applied three 36/72-dbu instance moves, also producing 0 new violations. Multi-pass repair with 36-dbu-aligned operations on this locus produces stable, zero-new-violation outcomes across both passes, as shown by trial:i01.ug.Block1_union_row3.03 and trial:i03.ug.Block1_union_row3.00.

## V1.M1.EN.1 and V0.M1.EN.1 Enclosure Maintenance

V0.M1.EN.1 requires M1 to enclose V0 by 5 nm on two opposite sides. V1.M1.EN.1 requires M1 to enclose V1 by 5 nm on one side and 2 nm on the opposite. All trials that touch V1 alongside M1 use 36-dbu-aligned move or resize_end operations and none reports `n_new_out_of_crop > 0` attributable to enclosure violations, as confirmed across trial:i01.ug.Block1_union_row1.00 through trial:i04.ug.leaf_0001.00. Use resize_end deltas larger than the enclosure minimum to extend M1 past the via edge; the 92-dbu and 128-dbu resize_end deltas in trial:i01.ug.Block1_union_row3.03 and trial:i01.ug.Block1_union_row1.00 are each substantially larger than the 5 nm enclosure requirement, confirming safe enclosure margin after each operation.

## V0.M1.AUX.3 Width Matching

V0.M1.AUX.3 requires V0 to exactly match M1 width along the direction perpendicular to M1 length. The via replacement in trial:i02.ug.leaf_0004.02 (delete i0300, add VIA_VIA12 at [5904, 6300]) produced zero new violations including for AUX.3, confirming that placing a fresh via on-grid at the correct position satisfies width-matching without separate M1 polygon adjustment.