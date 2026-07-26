## Primary Repair Strategy: X-Axis Instance Moves

Moving instances by 36 dbu in the X direction is the dominant repair for M2 spacing violations. Seven independent trials each applied move_instance with delta_dbu=[36,0] to one or more instances touching M2 and were accepted with zero new in-crop violations: trial:i01.ug.Block2_union_row1.00, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0011.06, trial:i01.ug.leaf_0013.08, trial:i04.ug.leaf_0001.00. Apply 36 dbu as the default X step when resolving M2.S.1, M2.S.2, or M2.S.6 violations by lateral instance displacement.

A single-instance move of 37 dbu in X (trial:i01.ug.leaf_0004.04) also resolved the violation without new violations, confirming the 36 dbu step is not a strict grid requirement; however, 36 dbu is the value used in all other accepted trials and is the reliable reference step.

## Single-Polygon X Moves on M2

When a spacing violation involves a single isolated M2 polygon not shared with other cell instances, move the polygon directly rather than moving an instance. In trial:i02.ug.leaf_0002.01, moving polygon p1053 by 76 dbu in X on M2 alone (no other touched layers) was accepted with zero new violations. Prefer a direct polygon move over an instance move in this situation to limit collateral geometry changes on other layers.

## Y-Axis Moves Increase In-Crop M2 Violation Count

Do not use Y-axis instance moves as the primary repair for M2 violations. In trial:i04.ug.leaf_0003.02, three move_instance operations with delta_dbu=[0,24] or [0,-24] on instances touching M2/M3/M4/M5/V2/V3/V4 introduced 2 new in-crop violations. In trial:i05.ug.leaf_0003.01, five move_instance operations with delta_dbu=[0,24] or [0,-24] on instances touching M1/M2/M3/M4/M5/V1/V3/V4 introduced 13 new in-crop violations. Both trials were gated_in only because connectivity was preserved. The new-violation count scaled with the number of simultaneously Y-displaced instances; avoid expanding the Y-move set beyond the minimum required.

## V1 Enclosure Preservation

The 36 dbu X instance move preserves V1.M2.EN.2 (≥5 nm enclosure of V1 by M2 on two opposite sides) and V1.M2.AUX.2 (V1 width matches M2 width perpendicular to the M2 length direction). All seven trials that applied delta_dbu=[36,0] to instances with both M2 and V1 in their touched-layers list were accepted with zero new violations in either rule: trial:i01.ug.Block2_union_row1.00, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0011.06, trial:i01.ug.leaf_0013.08, trial:i04.ug.leaf_0001.00.

## V2 Enclosure Repair via cu_pool Channel

Resolve V2.M2.EN.1 failures through the cu_pool channel by adjusting V2 via shape positions and sizes. In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, moving two V2 shapes by ±144 dbu in X and resizing all three V2 shapes by +288 dbu in X within cell VIA_VIA23_1_3_36_36 (touching M2, M3, V2) reduced the total violation count by 24. Use V2 shape adjustment within the via cell as the repair path for V2.M2.EN.1; resizing M2 itself was not applied in any accepted trial for this failure mode.

V2 shape operations generated during unit_gate trials are dropped and deferred to the cu_pool channel. In trial:i01.ug.leaf_0013.08, five V2 ops (move/resize of VIA_VIA23_1_3_36_36) appeared in assemble_drops with reason "cu_pool:applied", indicating trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 had already applied them. Do not re-apply V2 adjustments in unit_gate ops when the cu_pool channel has already handled the same via cell.

## Resize Operations Complementing Instance Moves

resize_end on M2-adjacent geometry is accepted when paired with connectivity-preserving operations. In trial:i02.ug.leaf_0001.00, the sequence—delete polygon p1101, delete instance i0086, insert via VIA_VIA12 at [5472,2340], and extend polygon p957 by +172 dbu at its low-x end—resolved the layout on M1/M2/M4/V1 with zero new violations. In trial:i01.ug.Block2_union_row1.00, resizing polygon p1053 by +184 dbu in X on M1 as part of a multi-instance move set also produced zero new M2 violations. Both cases confirm that large positive X resizes on polygons connected to M2 are safe when the moved instance set is internally consistent.

## Minimum Spacing and Width Reference Values

The following thresholds bound all M2 repair operations:

- Side-to-side spacing (both edges >36 nm): 18 nm minimum (M2.S.1). The 36 dbu X moves in trial:i01.ug.Block2_union_row1.00, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02 satisfy this threshold.
- Tip-to-side spacing (one edge ≤36 nm, other >36 nm, projection): 25 nm minimum (M2.S.2). Met by 36 dbu X instance moves in trial:i01.ug.Block2_union_row3.01 and trial:i01.ug.Block2_union_row5.02.
- Tip-to-tip spacing (both tips 24–36 nm, projection): 27 nm minimum (M2.S.3).
- Tip-to-tip spacing (both tips <24 nm, projection): 31 nm minimum (M2.S.4).
- Tip-to-tip spacing (one tip 24–36 nm, other <24 nm, projection): 31 nm minimum (M2.S.5).
- Corner-to-corner (Euclidean): 20 nm minimum (M2.S.6). Met by 36 dbu X moves in trial:i01.ug.leaf_0007.05 and trial:i01.ug.leaf_0011.06.
- M2.S.7: tip-to-tip gap of 18 nm co-located with side-to-side spacing ≤32 nm is forbidden; parallel run length 35 nm minimum when side spacing ≤32 nm. Y-axis moves in trial:i04.ug.leaf_0003.02 and trial:i05.ug.leaf_0003.01 introduced new in-crop violations in this geometry class.
- M2.S.8: diagonal center-to-center distance between tip-to-tip gaps on different tracks: 80 nm minimum (Euclidean). Y-axis moves in trial:i04.ug.leaf_0003.02 and trial:i05.ug.leaf_0003.01 repositioned M2 track segments and introduced new in-crop violations in the wider gap-spacing geometry.
- M2.W.1: minimum wire width 18 nm.
- M2.A.1: minimum polygon area 504 nm².