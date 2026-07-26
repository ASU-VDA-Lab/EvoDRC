## Repair Strategy: Direct V5 Shape Adjustment vs. Adjacent-Layer Manipulation

In cell `VIA_VIA56_2_2_66_58`, applying coordinated y-axis `move_via_shape` + `resize_via_shape` operations directly to V5 shapes reduced the total DRC violation count by 80 (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02, decision: applied). The same cell saw a net increase of 234 violations when the repair instead resized M6 along y and M5 along x without touching V5 shapes directly (trial:i02.cu.def:VIA_VIA56_2_2_66_58.01, decision: rejected_net_positive). Do not use M5/M6 resize as the primary repair lever for V5 violations in this cell family; apply corrections directly to V5 shapes on the axis of the violation.

## Move-Then-Resize Pairing on the Same Axis

The successful trial (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02) used eight operations organized as four pairs, each pair consisting of a `move_via_shape` followed by a `resize_via_shape` on the same axis (y) and the same shape index. Shapes 0 and 1 were displaced by −132 dbu then expanded by +512 dbu on y; shapes 2 and 3 were displaced by +132 dbu then expanded by +512 dbu on y. This paired pattern yielded a strict violation reduction across all four sampled windows (unit:Block7_union_row21, unit:Block7_union_row22, unit:leaf_0103, unit:leaf_0104). Apply move and resize as a coupled pair on the same axis rather than as independent single operations; the rejected trial (trial:i02.cu.def:VIA_VIA56_2_2_66_58.01) used only standalone resize operations on M5 and M6 and increased violations in every sampled window.

## Symmetric Displacement Around Center

In trial:i01.cu.def:VIA_VIA56_2_2_66_58.02, shapes split into two groups displaced symmetrically in opposite directions (−132 dbu and +132 dbu) before being expanded by the same magnitude (+512 dbu each). This symmetric push-out pattern was the one accepted and conn-preserved outcome for this cell. The asymmetric M5-x / M6-y resize in trial:i02.cu.def:VIA_VIA56_2_2_66_58.01 was rejected. When adjusting multiple V5 shapes in a single via cell, apply opposing displacements of equal magnitude to maintain center alignment before resizing.

## Unit-Gate Channel: Instance + Polygon Co-movement

Trials in the `unit_gate` channel (trial:i03.ug.leaf_0013.09, trial:i05.ug.leaf_0005.04) passed gating with 15 operations each, mixing direct polygon moves (`op: move` on `polygon_id`) with instance moves (`op: move_instance`). Both trials preserved connectivity. trial:i05.ug.leaf_0005.04 introduced zero new violations in-crop and zero out-of-crop; trial:i03.ug.leaf_0013.09 introduced 217 new violations in-crop but was still gated in because connectivity was preserved. The unit-gate channel accepts trials that preserve connectivity even when in-crop violation counts increase, as confirmed by both decisions being `gated_in` (trial:i03.ug.leaf_0013.09, trial:i05.ug.leaf_0005.04).

## Axis Alignment of Polygon Moves in Unit-Gate Repairs

In trial:i03.ug.leaf_0013.09, V5-touching polygon moves were split by axis: three polygon_ids moved along x (deltas: +32, −16, −64 dbu) and three along y (deltas: +32, −16, +64 dbu), with corresponding instance moves carrying the same per-axis deltas. In trial:i05.ug.leaf_0005.04, polygon moves were also split by axis: three polygon_ids moved along x (deltas: +32, −16, +32 dbu) and three along y (deltas: −64, +16, −32 dbu), again with matched instance moves. Use axis-separated polygon and instance moves with matched deltas when operating in the unit-gate channel on V5-touching layouts.

## V5.AUX.1 and V5.M6.AUX.2 Containment Constraints

Rule V5.AUX.1 requires every V5 shape to lie inside both M5 and M6. Rule V5.M6.AUX.2 requires V5 width along the direction perpendicular to M6 length to exactly match M6 width. The successful resize operations in trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 applied +512 dbu expansion on y to all four V5 shapes. The rejected trial:i02.cu.def:VIA_VIA56_2_2_66_58.01 resized M6 by +128 dbu on y and M5 by −96 dbu on x, which altered the M5/M6 envelope without correspondingly adjusting V5 shapes, violating the containment relationship that V5.AUX.1 and V5.M6.AUX.2 enforce. Resize operations that modify M5 or M6 without a matching V5 adjustment risk breaking these containment rules; resize V5 shapes to match any envelope change, or resize V5 shapes directly and leave the enclosing metal unchanged.

## Enclosure Rules V5.M5.EN.1 and V5.M6.EN.2

Both rules require 11 nm enclosure by the respective metal on at least two opposite sides. The net-positive outcome of trial:i02.cu.def:VIA_VIA56_2_2_66_58.01, which shrunk M5 along x by 96 dbu while expanding M6 along y by 128 dbu, is consistent with the enclosure margin on at least one axis being consumed or reversed by that resize. Do not shrink the enclosing metal layer on the same axis as an existing enclosure margin without verifying the 11 nm minimum is maintained after the change.