## Repair Strategy: Instance-Level Moves Dominate V1 Fixes

All ten accepted trials in iteration 1 resolved V1 violations exclusively through `move_instance` operations on the instances containing the offending V1 shapes; no trial directly edited a V1 polygon. The touched-layers field consistently lists V1 alongside M1 and M2, confirming that V1 moves as a passenger inside repositioned instances rather than as a standalone polygon target (trial:i01.ug.Block4_union_row1.00, trial:i01.ug.Block4_union_row10.01, trial:i01.ug.Block4_union_row2.02, trial:i01.ug.Block4_union_row5.04, trial:i01.ug.Block4_union_row6.05, trial:i01.ug.Block4_union_row7.06, trial:i01.ug.leaf_0008.08, trial:i01.ug.leaf_0020.09, trial:i01.ug.leaf_0021.10). Do not attempt to resize or move a V1 polygon in isolation; target the containing instance instead.

## Axis of Movement: Predominantly Horizontal

Every accepted repair displaced instances along the x-axis. Nine of the ten trials used pure horizontal deltas (y-component = 0). The single exception, trial:i01.ug.leaf_0021.10, applied delta [36, 44] dbu and was still accepted with zero new violations. The strong bias toward x-only movement is consistent with M2 routing along a horizontal preferred direction and the projection-based spacing checks in V1.S.1, which measure spacing along the x-axis between same-track vias.

## Move Magnitude Range

Accepted horizontal displacements span 12 dbu to 108 dbu. Small corrections (12 dbu, trial:i01.ug.Block4_union_row10.01) suffice when the spacing shortfall is minor. Larger shifts (108 dbu, trial:i01.ug.Block4_union_row2.02) are required when the violation margin or the instance grid forces a bigger step. Mixed-magnitude moves within the same repair are also confirmed: trial:i01.ug.Block4_union_row2.02 combined a 108 dbu instance shift, a 16 dbu polygon nudge, and a 28 dbu instance shift in a single accepted operation set.

## Coordinated Multi-Instance Moves

Several trials moved multiple instances simultaneously in the same direction to satisfy V1 spacing rules without introducing new violations elsewhere. trial:i01.ug.Block4_union_row6.05 moved three instances each +36 dbu x; trial:i01.ug.Block4_union_row5.04 moved four instances, three at +37 dbu and one at -36 dbu. Moving only the violating via's instance while leaving neighboring instances fixed can create new spacing violations on the opposite side; coordinating adjacent instances avoids this. When the repair locus spans a wide row (e.g., x range 3400–12456 dbu in trial:i01.ug.Block4_union_row6.05), move all instances in the affected row together.

## Bidirectional Adjustment Is Valid

trial:i01.ug.Block4_union_row5.04 used both a positive shift (+37 dbu, three instances) and a negative shift (-36 dbu, one instance) within the same repair and was accepted with no new violations. Splitting the available gap between two approaching via groups — rather than pushing all vias in one direction — is a confirmed strategy when spacing violations exist between two groups on the same or adjacent M2 tracks.

## Wire Stretching Must Accompany Large Instance Shifts

When an instance carrying a V1 is moved far enough that its connected M2 (or higher-layer) wire endpoint no longer reaches, a `resize_end` on the wire polygon is required to restore the connection. trial:i01.ug.Block4_union_row7.06 moved two instances -28 dbu x and simultaneously extended polygon p1395's high-x end by +172 dbu. trial:i01.ug.leaf_0008.08 moved instance i0274 +36 dbu x and extended polygon p1604's high-x end by +92 dbu. Both were accepted with conn_preserved=true and zero new violations. Failure to stretch the wire when the instance moves beyond the current wire endpoint will break connectivity; always pair a large instance move with a matching `resize_end` on the attached M2 segment.

## Polygon-Only Moves for Minor Adjustments

trial:i01.ug.Block4_union_row2.02 included a direct polygon move (`axis: x, delta_dbu: 16, polygon_id: p1548`) alongside two instance moves. This suggests that when a connecting M2 wire segment needs a small repositioning that is less than the full instance delta, a targeted polygon x-move on that wire is acceptable. This was accepted with full connectivity preservation.

## V1.AUX.1 and V1.M2.AUX.2 Are Automatically Maintained by Instance Moves

Because V1 shapes reside inside their parent instances and move rigidly with them, instance-level moves leave the geometric relationship between V1 and its enclosing M1/M2 shapes unchanged. No trial introduced new V1.AUX.1 (V1 outside M1∩M2) or V1.M2.AUX.2 (V1 width mismatch with M2) violations, consistent with the fact that those rules are intra-instance constraints satisfied by construction. Wire stretches (resize_end) extend the M2 polygon endpoint without changing M2 width, so V1.M2.AUX.2 remains satisfied after a stretch.

## Enclosure Rules V1.M1.EN.1 and V1.M2.EN.2 Are Not Disrupted by Instance Moves

All ten accepted trials preserved the M1 and M2 enclosure of V1 (V1.M1.EN.1 requires 5 & 2 nm on opposite sides; V1.M2.EN.2 requires 5 & 5 nm or 5 & 0 nm on opposite sides). Instance moves that shift both the via and its enclosing metal together do not alter the enclosure margin; wire stretches that extend a M2 endpoint do not reduce M2 width and therefore do not reduce enclosure on the sides perpendicular to the extension direction. No enclosure violation was introduced in any iteration-1 trial.

## All Iteration-1 Repairs Were Accepted

Every trial in this layer's history carries decision="gated_in", n_new_in_crop=0, n_new_out_of_crop=0, and conn_preserved=true. The repair channel "unit_gate" accepted all ten moves. This means the chosen deltas were sufficient to clear the DRC violations that triggered each repair and did not open new violations in the cropped locus or outside it.