## V4 via-cell M5 resize is the only directly effective repair observed

Trial i02.cu.def:VIA_VIA45_1_2_58_58.02 (cu_pool channel) applied one resize_via_shape on the M5 layer within cell VIA_VIA45_1_2_58_58, shrinking it 88 dbu in the y-axis. This reduced total violations by 15 (leaf_0002: 17→8, leaf_0003: 25→19) with conn_preserved=true and decision "applied". This is the only operation in the two-iteration history that was accepted by the cu_pool channel and directly reduced V4-touching-layer violations. Resize the M5 landing-pad shape inside the via cell in the y-direction to reduce violations when VIA_VIA45_1_2_58_58 is flagged (trial i02.cu.def:VIA_VIA45_1_2_58_58.02).

## V4 moves with host M4/M5 without independently triggering V4 rule violations

Trials i01.ug.leaf_0010.07 and i02.ug.leaf_0002.01 both include V4 in touched_layers while applying move_instance operations (y-deltas of ±24 and ±72 dbu in trial i01.ug.leaf_0010.07; x-delta of +32 dbu plus y-deltas in trial i02.ug.leaf_0002.01). Neither trial's per_rule delta records any violation under V4.W.1, V4.S.1, V4.S.2, V4.S.3, V4.M4.EN.1, V4.M5.EN.2, V4.AUX.1, or V4.M5.AUX.2. V4 instances displaced as part of instance moves remain compliant provided the host M4/M5 routing is well-formed.

## M5 violations introduced by unit_gate moves are distinct from V4 violations

Trial i02.ug.leaf_0002.01 introduced 27 new in-crop violations (M5.AUX.1: +7, M5.AUX.3: +13, M5.S.4: +2, M5.W.5: +5) but zero V4-category violations, even though V4 was in touched_layers. This confirms that the M5 rule violations produced by the unit_gate instance shift are M5-layer issues, not V4 enclosure or spacing violations. Do not conflate M5 violation counts with V4 enclosure repair needs when both layers appear in touched_layers (trial i02.ug.leaf_0002.01).

## cu_pool M5 resize for the via cell takes assembly priority over conflicting polygon ops

In trial i02.ug.leaf_0002.01, two operations targeting polygon p879 on M5 were dropped at assembly: the x+32 dbu move was dropped with reason "reserved_by_cu_pool_winner" (conflict with leaf_0002), and a y+96 dbu resize was dropped with reason "cu_pool:applied". The cu_pool resize from trial i02.cu.def:VIA_VIA45_1_2_58_58.02 was protected. Avoid scheduling independent M5 polygon moves or resizes that overlap the M5 footprint of VIA_VIA45_1_2_58_58 when a cu_pool resize for that cell has been applied; the assembler will drop the conflicting ops (trial i02.ug.leaf_0002.01).

## V4.M5.AUX.2 constraint on M5 resize magnitude

V4.M5.AUX.2 requires that V4 width exactly matches M5 width along the perpendicular-to-M5-length direction. The 88 dbu y-shrink applied to the M5 shape inside VIA_VIA45_1_2_58_58 (trial i02.cu.def:VIA_VIA45_1_2_58_58.02) was accepted without a V4.M5.AUX.2 violation appearing in the result. This means the resize brought the M5 shape into exact alignment with the V4 shape width rather than away from it; a resize that widens M5 beyond the V4 instance boundary, or narrows it below that boundary, would trigger V4.M5.AUX.2.

## V4.AUX.1 compliance maintained across all trials

V4.AUX.1 (V4 must lie inside both M4 and M5) produced no violations in any of the three trials. Instance moves that shift M4 and M5 together (trials i01.ug.leaf_0010.07 and i02.ug.leaf_0002.01) and the M5 via-shape resize (trial i02.cu.def:VIA_VIA45_1_2_58_58.02) all preserved this constraint. Resize or move operations that shift M5 or M4 independently of the V4 shape risk V4.AUX.1; the shrink in trial i02.cu.def:VIA_VIA45_1_2_58_58.02 was applied to a via-cell shape that kept V4 inside the remaining M5 area.