## Observed Repair Patterns on M2

### Instance moves and M2 geometry

The dominant repair action on M2 across all three iterations is a horizontal (x-axis) `move_instance` applied to one or more instances within the unit crop. Steps of 36 dbu were accepted in every iteration that used them: trial:i01.ug.Block5_union_row3.00, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05, and trial:i03.ug.leaf_0002.01. In all six cases the decision was `gated_in` and no new out-of-crop violations were introduced. 36 dbu is therefore the confirmed grid pitch for M2-touching instance moves in Block5.

A smaller step of 4 dbu was also accepted at trial:i01.ug.Block5_union_row6.01, but the same unit (Block5_union_row6) required a subsequent 104 dbu move in the next iteration (trial:i02.ug.Block5_union_row6.00) before the violation count stabilised. A 4 dbu x-move is insufficient to clear M2 spacing rules when the residual gap after the small move remains below the applicable minimum; the unit returned for a much larger correction one iteration later.

### resize_end co-occurrence with instance moves

`resize_end` on the x-high end of an M2 polygon co-occurs with instance moves in three accepted trials:

- trial:i01.ug.Block5_union_row3.00: resize_end p967 x-high +36 alongside a +36 move of i0117.
- trial:i01.ug.leaf_0001.02: resize_end p974 x-high +72 alongside a +36 move of i0011. The resize delta is twice the move delta; the polygon end is stretched independently to maintain enclosure or spacing.
- trial:i02.ug.Block5_union_row6.00: resize_end p955 x-high +20 alongside +104 moves of i0025 and i0019.

In all three cases the operation set was `gated_in` with zero new violations. Stretching an M2 polygon end by a delta different from the instance move delta is accepted, provided connectivity is preserved. A resize larger than the instance step (as in trial:i01.ug.leaf_0001.02, +72 vs +36) is permissible.

### Bilateral instance spreading on M2

trial:i01.ug.leaf_0002.03 moved i0056 by +36 dbu and i0103 by −36 dbu in the same operation set. The result was `gated_in` with no new violations. Spreading two instances symmetrically away from each other clears M2 side-to-side spacing (M2.S.1) without shifting the centroid of the affected region, and is a valid approach when a single-direction push would violate spacing on the opposite side.

### M2 involvement in V2 via-cell repair (cu_pool channel)

Three trials from the `cu_pool` channel touched M2 as a side effect of operating on via cell `VIA_VIA23_1_3_36_36` (which spans M2, V2, M3):

**trial:i02.cu.def:VIA_VIA23_1_3_36_36.00** — Sole op: resize_via_shape on M3 y-axis −40 dbu. Decision: `rejected_net_positive`, delta_total=0. The design state was `c529...` (post-iter-1). The shrink produced no net improvement.

**trial:i02.cu.def:VIA_VIA23_1_3_36_36.01** — Ten ops: resize_via_shape on M3, V3 (multiple shapes), plus resize_end on M2 polygons p891, p892, p893 at both y-low and y-high ends by −32 dbu each. Decision: `rejected_net_positive`, delta_total=+5 (leaf_0005 worsened by +8, leaf_0006 improved by −3). Shrinking M2 polygons on both y-ends simultaneously in the same operation set as multi-layer via resizes increased the total violation count. This combined operation is not an effective repair strategy.

**trial:i03.cu.def:VIA_VIA23_1_3_36_36.00** — Identical op to trial:i02.cu.def:VIA_VIA23_1_3_36_36.00 (resize_via_shape M3 y −40), but in design state `d7ef...` (post-iter-2 unit_gate repairs). Decision: `applied`, delta_total=−8. The same via resize that had zero effect in iter 2 reduced the leaf_0001 violation count from 18 to 10 when applied after additional unit_gate corrections had been committed. Via-cell M3 shrinks that touch M2 are order-dependent: the same operation produces different outcomes depending on what M2 geometry has already been corrected in earlier iterations.

### gated_in with n_new_in_crop > 0

trial:i03.ug.leaf_0002.01 (move_instance i0111 +36 dbu, touching M1/M2/V1) was accepted as `gated_in` despite `n_new_in_crop=1`. The gate criterion is connectivity preservation (`conn_preserved=true`), not zero new violations inside the crop. An instance move that preserves connectivity is accepted even if it introduces one new in-crop violation; the expectation is that the downstream violation will be resolved by a subsequent operation or by a `cu_pool` pass.

### M2.S.1 / M2.S.2 / M2.W.1 interaction with instance moves

All accepted unit_gate trials on M2 operate exclusively on the x-axis. M2 spacing rules M2.S.1 (side-to-side, 18 nm) and M2.S.2 (tip-to-side, 25 nm) are the rules most likely targeted by horizontal instance moves, since M2 routing in Block5 runs in the x-direction (vertical edges are the long sides, horizontal edges are tips). The 36 dbu grid pitch directly addresses minimum spacing and minimum width (M2.W.1, 18 nm) in a single step that does not undercut the minimum.

### What does not work: shrinking M2 y-extent alongside multi-layer via resizes

trial:i02.cu.def:VIA_VIA23_1_3_36_36.01 applied −32 dbu to both ends of three M2 polygons (p891, p892, p893) on the y-axis simultaneously with resizes on M3 and V3. The net result was a +5 violation increase. Shrinking M2 polygon y-extent in a single compound operation touching four metal layers produces net-positive outcomes and is not a viable repair move for this via cell.

### Summary of accepted vs rejected moves

Accepted (gated_in / applied):
- x-axis move_instance steps of 36 dbu, singular or bilateral: trial:i01.ug.Block5_union_row3.00, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05, trial:i02.ug.leaf_0002.02, trial:i03.ug.leaf_0002.01.
- x-axis resize_end on M2 polygon high end (+36, +72, +20 dbu) co-occurring with instance moves: trial:i01.ug.Block5_union_row3.00, trial:i01.ug.leaf_0001.02, trial:i02.ug.Block5_union_row6.00.
- Via M3 y-shrink (−40 dbu) applied after prior M2 unit_gate corrections: trial:i03.cu.def:VIA_VIA23_1_3_36_36.00.

Rejected (rejected_net_positive):
- Via M3 y-shrink (−40 dbu) applied before sufficient M2 unit_gate corrections: trial:i02.cu.def:VIA_VIA23_1_3_36_36.00.
- Combined y-shrink of M2 polygons at both ends (−32 dbu) plus multi-layer via resizes: trial:i02.cu.def:VIA_VIA23_1_3_36_36.01.