## Instance Move Operations

All eight iteration-1 unit_gate trials that touched V1 applied `move_instance` ops with x-axis deltas of 36 dbu (trial:i01.ug.Block2_union_row1.00, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0004.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0011.06, trial:i01.ug.leaf_0013.08) or 37 dbu (trial:i01.ug.leaf_0004.04). Every one of these closed with `n_new_in_crop:0` and `n_new_out_of_crop:0` in the V1-relevant portion of the design, confirming that a single-step lateral shift in x at that granularity is a safe first-resort repair for V1 spacing and enclosure violations when the unit_gate channel is active.

A smaller shift of 12 dbu combined with an explicit M1 polygon addition also closed cleanly for the same unit in iteration 1 (trial:i01.ug.leaf_0001.03), demonstrating that sub-grid-step moves are viable when accompanied by metal geometry that restores connectivity.

## Via Replacement Sequence

When iteration-1 repair of `leaf_0001` left residual V1 geometry (trial:i01.ug.leaf_0001.03 added an M1 patch via `add_polygon` and shifted i0086 by 12 dbu), iteration 2 superseded that approach entirely with a four-op replacement sequence on the same unit (trial:i02.ug.leaf_0001.00):

1. Delete polygon p1101 (the prior M1 patch).
2. Delete instance i0086 (the shifted cell).
3. Place a fresh `VIA_VIA12` via cell at origin [5472, 2340] dbu via `add_via`.
4. Apply `resize_end` on polygon p957, axis x, end low, delta +172 dbu.

This sequence touched M1, M2, M4, and V1 and closed with `n_new_in_crop:0`, `n_new_out_of_crop:0`, `conn_preserved:true`. The `VIA_VIA12` cell is the confirmed standard V1 (M1–M2) via cell name used in this design. The accompanying `resize_end` on the low x-end of an M1/M2 run by 172 dbu provided the required enclosure margin after repositioning the via.

## Gating Under Collateral Violations

The gating criterion `conn_preserved:true` overrides a small increase in in-crop violations in adjacent layers. Trial:i01.ug.leaf_0013.08 introduced one new `M1.A.1` violation in-crop while touching V1, yet was accepted because connectivity was preserved (`decision:"gated_in"`). Do not treat a non-zero `n_new_in_crop` from a non-V1 rule as a disqualifier when `conn_preserved` is true; the channel accepts the trade.

During that same trial, pool-applied V2 shape operations (three resize_via_shape and two move_via_shape ops on `VIA_VIA23_1_3_36_36`) were listed in `assemble_drops` with reason `cu_pool:applied`, meaning they had already been committed at assembly and were correctly excluded from re-application. These drops do not affect V1 DRC outcomes (trial:i01.ug.leaf_0013.08).

## Multi-Instance Coordination

Several fixes moved two or three instances together in a single trial. Moving i0103 and i0115 together by [36,0] dbu resolved violations in `Block2_union_row3` (trial:i01.ug.Block2_union_row3.01). Moving i0083, i0018, and i0034 together by [36,0] dbu resolved violations in `Block2_union_row5` (trial:i01.ug.Block2_union_row5.02). Moving i0159 and i0152 together by [36,0] dbu plus an M2 polygon resize (p1053, axis x, +184 dbu) resolved violations in `Block2_union_row1` (trial:i01.ug.Block2_union_row1.00). Coordinated multi-instance moves that keep all affected cells at identical x-offsets produce zero new violations; staggered moves that change relative inter-instance spacing have no measured support.

## Enclosure and Width Repair Context

The V1.M1.EN.1 rule requires opposite-side M1 enclosure of at least 5 nm and 2 nm. The V1.M2.EN.2 rule requires M2 enclosure of at least 5 nm on both opposite sides or 5 nm on one side and 0 nm flush on the other. V1.M2.AUX.2 requires V1 width to exactly match M2 width perpendicular to M2 length. The `resize_end` of +172 dbu applied to polygon p957 in trial:i02.ug.leaf_0001.00, combined with a `VIA_VIA12` placement at [5472, 2340], is the only directly measured enclosure-restoring geometry change for V1 in this history. Resize operations that extend the low-x end of an M1/M2 run toward the via origin are the confirmed approach when via placement is shifted relative to an existing metal endpoint.

## Non-Orthogonal Geometry

No trial in this history introduced non-orthogonal V1 edges. All `add_via` and `move_instance` ops in the measured records produce axis-aligned geometry. The GEOMETRY.NONORTHOGONAL check applies to V1; avoid any polygon or via placement that produces edges deviating from 0° or 90°.