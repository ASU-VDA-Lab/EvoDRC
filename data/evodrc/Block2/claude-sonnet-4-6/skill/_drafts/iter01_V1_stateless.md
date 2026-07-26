## Operation Outcomes

Every trial in this iteration was accepted (decision: gated_in) with zero new DRC violations introduced or removed in crop (n_new_in_crop: 0, n_new_out_of_crop: 0). The gating criterion in every case was conn_preserved: true. No trial was rejected.

## Layer Co-movement Requirement

V1 was never touched in isolation. All seven accepted trials list V1 alongside M1 and M2 in touched_layers, and trial:i01.ug.leaf_0001.03 also includes M4. This is consistent with V1.AUX.1, which requires V1 to remain inside both M1 and M2 simultaneously: any operation that displaces a V1-bearing instance must also adjust the enclosing metal geometry, or a violation results.

## Instance Move + Polygon Resize Pairing

The dominant accepted pattern is pairing move_instance operations with resize_end operations on the same axis and direction as the move. Examples:

- trial:i01.ug.Block2_union_row3.01 moved instances i0115 and i0103 by +36 dbu in x and simultaneously extended polygon p1040 by +36 dbu on its high-x end.
- trial:i01.ug.Block2_union_row5.02 moved instances i0083, i0018, and i0034 by +64 dbu in x and extended polygons p1059 and p1057 by +64 dbu on their high-x ends.
- trial:i01.ug.leaf_0011.06 moved instance i0027 by +36 dbu in x and extended polygon p1052 by +36 dbu on its high-x end.

In all three of these trials the resize delta matched the move delta exactly, producing zero new violations. This directly satisfies V1.M2.EN.2 (M2 must enclose V1 on two opposite sides by 5 & 5 nm or 5 & 0 nm) and V1.M1.EN.1 (M1 enclosure 5 & 2 nm on opposite sides): if the enclosing metal polygon end is not extended by the same displacement as the instance, one enclosure edge would fall short.

## Unequal Resize Deltas

trial:i01.ug.leaf_0001.03 is the only trial with unequal resize deltas: the instance moved +128 dbu in x, while polygon p1065 was extended +184 dbu on its high-x end and polygon p957 was shrunk by extending its low-x end +176 dbu (i.e., the low edge advanced toward the high edge, reducing that polygon). This trial also produced zero new violations. The asymmetry between the 128 dbu move and the 184/176 dbu resizes indicates the pre-move geometry had slack on one side and deficit on another; correcting both simultaneously while moving is accepted provided connectivity is preserved.

## Move Without Resize

Two trials moved a single instance by +36 dbu in x with no accompanying resize:

- trial:i01.ug.leaf_0004.04: one move_instance op, zero resize ops.
- trial:i01.ug.leaf_0007.05: one move_instance op, zero resize ops.

Both produced zero new violations. This demonstrates that when sufficient pre-existing enclosure headroom is present on both M1 and M2, a 36 dbu x-shift of a V1-containing instance does not breach V1.M1.EN.1, V1.M2.EN.2, V1.AUX.1, or V1.M2.AUX.2. Do not assume a resize is always required; the need depends on the available enclosure margin before the move.

## Move Magnitudes Seen

Accepted x-axis move deltas: 36 dbu (trial:i01.ug.Block2_union_row1.00, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.leaf_0004.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0011.06), 64 dbu (trial:i01.ug.Block2_union_row5.02), 128 dbu (trial:i01.ug.leaf_0001.03). All were positive (high-x direction). No y-axis moves appear in the V1-touching trials.

## Spacing and Width Rules: No Violations Observed

None of the seven trials produced violations attributed to V1.W.1 (18 nm minimum width), V1.S.1 (projection spacing), V1.S.2 (corner-to-corner WEC-to-WEC), V1.S.3 (corner-to-corner NEC-to-NEC), or V1.S.4 (corner-to-corner WEC-to-NEC). The operations shifted instances and extended/contracted metal ends along x; they did not alter V1 polygon dimensions directly, so the width rule V1.W.1 and the M2.AUX.2 same-width constraint were satisfied by construction when metal resizes tracked instance moves.

## Connectivity as Gate

Across all seven trials, conn_preserved: true was both necessary and sufficient for gated_in. No trial was accepted with conn_preserved: false, and no trial with conn_preserved: true was rejected. Operations that co-move instance and associated metal polygon ends by consistent deltas reliably preserve connectivity, as demonstrated by trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02, and trial:i01.ug.leaf_0011.06.