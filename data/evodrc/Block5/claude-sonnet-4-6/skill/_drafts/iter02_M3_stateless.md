## VIA_VIA23_1_3_36_36: cu_pool repairs on M3

For via cell VIA_VIA23_1_3_36_36, the cu_pool channel applied two distinct M3-touching repairs across consecutive iterations. In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, y-axis shrinkage was applied to the M3 via metal shape (-40 dbu) and to four adjacent M3 polygons p894, p895, p896, p897 (each -64 dbu in y); this reduced the total violation count by 8 (leaf_0009: 25 -> 17, leaf_0010 unchanged at 25). Both the via shape resize and the polygon shrinks were grouped under the same cu_pool operation and received decision "applied" with conn_preserved true. In trial:i02.cu.def:VIA_VIA23_1_3_36_36.01, a +144 dbu x-axis reposition of the V2 via shape (touching M2, M3, V2) reduced the count by a further 7 (leaf_0002: 17 -> 13, leaf_0003: 25 -> 22), also with decision "applied" and conn_preserved true. The two cu_pool operations on the same via cell netted -15 violations across iterations 1 and 2.

When residual violations remain on VIA_VIA23_1_3_36_36 after y-direction M3 and via shape shrinkage, move the V2 via shape laterally in x to achieve additional reduction (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, trial:i02.cu.def:VIA_VIA23_1_3_36_36.01). The magnitude used in the measured repair was +144 dbu in x (trial:i02.cu.def:VIA_VIA23_1_3_36_36.01).

## cu_pool priority blocks unit_gate ops on shared M3 polygons

Unit_gate operations targeting M3 polygons are dropped at assembly when cu_pool has already acted on those polygons. In trial:i02.ug.leaf_0002.01, an x-axis move of M3 polygon p879 (+32 dbu) was dropped with assemble reason "reserved_by_cu_pool_winner"; a y-axis resize of p879 (+96 dbu) and a V2 via shape x-move were each dropped with reason "cu_pool:applied". All three drops occurred in the same assemble pass and produced zero net change on the M3 violation count for that polygon group.

Do not issue unit_gate ops on M3 polygons that a cu_pool winner has already modified; those ops are silently dropped and have no effect on violation totals (trial:i02.ug.leaf_0002.01). Checking the cu_pool applied set before scheduling unit_gate polygon moves avoids wasted operations and misleading per-trial delta accounting.

## M3 shape resize in y propagates violations to lower layers

In trial:i02.ug.leaf_0003.02, a y-axis shrink of M3 polygon p893 by -64 dbu, combined with an x-axis move of p910 (+8 dbu) and a move_instance on i0111 (+36 dbu in x), touched layers M1, M2, M3, and V1. The trial introduced 7 new violations on layers below M3: M1.A.1 (4 new) and V1.M1.EN.1 (3 new). The trial was accepted (gated_in, conn_preserved true) with n_new_out_of_crop zero, so the new violations fell within the gating budget, but the new_in_crop count was nonzero.

Resize M3 shapes in y only when the resulting lower-layer violation budget -- specifically M1.A.1 and V1.M1.EN.1 -- is acceptable within the gating threshold in effect for that unit (trial:i02.ug.leaf_0003.02). A -64 dbu y-shrink is the measured magnitude associated with this cross-layer debt.

## Unit_gate trials touching M3: instance moves dominate and are accepted

All three unit_gate trials that included M3 in touched_layers received decision "gated_in" with conn_preserved true (trial:i01.ug.leaf_0010.07, trial:i02.ug.leaf_0002.01, trial:i02.ug.leaf_0003.02). In each case, move_instance operations were the primary mechanism; direct M3 polygon ops (resize, move) were either secondary or dropped at assembly due to cu_pool preemption.

Prefer move_instance over direct M3 polygon moves when the repair target is connectivity-driven; direct polygon moves on M3 are subject to cu_pool preemption and may be silently dropped with no violation benefit (trial:i02.ug.leaf_0002.01). Instance moves that include M3 in touched_layers proceed to gated_in when conn_preserved is satisfied, even when other layers in the same trial accrue new violations (trial:i02.ug.leaf_0003.02).

## Observed M3 operation magnitudes (measured values only)

The following deltas were applied in accepted or gated_in trials and are cited here for reference when calibrating new ops:

- M3 via metal shape y-shrink: -40 dbu (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00)
- M3 polygon y-shrink (p894-p897): -64 dbu each (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00)
- M3 polygon y-shrink (p893): -64 dbu (trial:i02.ug.leaf_0003.02)
- M3 polygon x-move (p910): +8 dbu (trial:i02.ug.leaf_0003.02)
- V2 via shape x-reposition (touching M3): +144 dbu (trial:i02.cu.def:VIA_VIA23_1_3_36_36.01)

No direct M3 polygon moves in x were successfully applied in the measured history; the only attempted x-move on an M3 polygon (p879, +32 dbu) was dropped at assembly (trial:i02.ug.leaf_0002.01). Do not rely on unit_gate x-moves to M3 polygons as a primary repair mechanism when cu_pool is active on the same via cell (trial:i02.ug.leaf_0002.01).