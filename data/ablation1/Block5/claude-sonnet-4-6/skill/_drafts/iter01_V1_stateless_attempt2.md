All six trials in the measured history share three outcome properties: `decision` is `gated_in`, `conn_preserved` is `true`, and both `n_new_in_crop` and `n_new_out_of_crop` are `0`. Every repair strategy documented below therefore achieved zero net DRC degradation while preserving connectivity.

## Axis of Repair

Every operation recorded across all six trials acts exclusively on the X axis. No Y-axis move or resize appears in any trial (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.Block5_union_row6.01, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05). V1 spacing violations that triggered these repairs—governed by V1.S.1, V1.S.2, V1.S.3, and V1.S.4—are therefore resolved by horizontal displacement alone in this design context.

## Move-Only Repairs

Single-instance X-axis moves suffice when the locus contains only one conflicting V1 grouping. Trial:i01.ug.leaf_0005.04 resolves its violation with a single `move_instance` of +36 dbu on i0017, and trial:i01.ug.leaf_0006.05 does the same with +36 dbu on i0012. Both accept with zero new violations, confirming that a +36 dbu horizontal shift clears the measured spacing shortfall in those units without violating V1.M1.EN.1, V1.M2.EN.2, V1.AUX.1, or V1.M2.AUX.2.

Two-instance moves in the same direction are accepted when both instances share the conflict direction. Trial:i01.ug.Block5_union_row6.01 moves i0025 and i0019 each by +4 dbu and is accepted, showing that a smaller delta (+4 dbu) is sufficient in some loci and does not under-correct to leave residual violations.

Opposing-direction moves resolve conflicts where two instances encroach on each other. Trial:i01.ug.leaf_0002.03 moves i0056 by +36 dbu and i0103 by −36 dbu simultaneously, achieving acceptance with no new violations. This bidirectional pattern satisfies V1.S.1 or V1.S.3/V1.S.4 spacing by splitting the required gap between both instances rather than displacing all slack onto one side.

## Move-Plus-Resize Repairs

When a `move_instance` shifts a V1 instance toward the high-X edge of its enclosing M2 rectangle, the M2 end must be extended to maintain V1.M2.EN.2 (≥5 nm enclosure on opposite sides) and V1.AUX.1 (V1 fully inside M1 ∩ M2). In both cases where a `resize_end` appears, the resize targets axis `x`, end `high`, extending the M2 polygon's far edge outward.

Trial:i01.ug.Block5_union_row3.00 pairs a +36 dbu move on i0117 with a `resize_end` of +36 dbu on polygon p967, plus a second +36 dbu move on i0131—three operations total, accepted cleanly. Trial:i01.ug.leaf_0001.02 pairs a +36 dbu move on i0011 with a `resize_end` of +72 dbu on polygon p974—two operations, accepted cleanly. The resize delta in trial:i01.ug.leaf_0001.02 is twice the move delta, indicating that the M2 extension must cover both the shifted V1 footprint and any pre-existing enclosure deficit beyond the instance displacement.

Do not move a V1-bearing instance toward the high-X M2 boundary without a matching `resize_end` on that M2 polygon; the paired approach in trial:i01.ug.Block5_union_row3.00 and trial:i01.ug.leaf_0001.02 is what keeps V1.AUX.1 and V1.M2.EN.2 clean after the move.

## Multi-Layer Touch

All trials record `touched_layers` as `["M1","M2","V1"]`. No trial modifies only V1 or only M2. Any X-axis displacement of a V1 instance propagates into both the M1 and M2 layers (via the instance hierarchy), making it normal—not exceptional—for a V1 repair to register changes across all three layers simultaneously (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.Block5_union_row6.01, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05).

## Operation Count and Repair Complexity

Accepted repairs range from one operation (trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05) to three operations (trial:i01.ug.Block5_union_row3.00). Two-operation repairs appear in trial:i01.ug.Block5_union_row6.01, trial:i01.ug.leaf_0001.02, and trial:i01.ug.leaf_0002.03. Loci requiring a `resize_end` always use at least two operations; loci requiring only instance moves may use one or two. Prefer the smallest operation count that achieves the required spacing correction, since all single-operation and two-operation repairs in this history are accepted without residual violations.