## V5 Layer — DRC Repair Knowledge (iteration 3)

### Rule Interactions Observed

**V5.M6.AUX.2 and V5.M5.EN.1/V5.M6.EN.2 are tightly coupled.** Resizing an enclosing metal layer without a matching V5 resize breaks V5.M6.AUX.2, which requires V5 to match M6's width exactly perpendicular to the M6 run direction. trial:i02.cu.def:VIA_VIA56_2_2_66_58.01 resized M6 in y by +128 dbu and M5 in x by -96 dbu with no V5 shape changes; that trial was rejected with delta_total +234. Do not resize M6 or M5 in isolation when V5 is involved: the V5 shape must be co-adjusted to maintain the exact-width coincidence required by V5.M6.AUX.2.

**Direct V5 resize in the y-axis, paired with a move, reliably reduces violations.** trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 applied eight operations on four V5 shapes inside cell VIA_VIA56_2_2_66_58: each shape received a y-axis move followed by a y-axis resize of +512 dbu. Shapes 0 and 1 moved -132 dbu; shapes 2 and 3 moved +132 dbu. The trial was applied with delta_total -80, reducing violations across four windows (unit:Block7_union_row21 -6, unit:Block7_union_row22 -2, unit:leaf_0103 -36, unit:leaf_0104 -36). Apply move-then-resize in the same axis and keep the resize magnitude equal across all shapes in the via cell to satisfy V5.W.1 (≥24 nm) and V5.M5.EN.1/V5.M6.EN.2 (≥11 nm enclosure on two opposite sides) simultaneously.

**Symmetric paired moves on opposing via shapes preserve V5.S.1/V5.S.2/V5.S.3 spacing.** In trial:i01.cu.def:VIA_VIA56_2_2_66_58.02, the two shape pairs moved in equal-and-opposite y directions (±132 dbu), keeping the center of each pair stable while enlarging each shape outward. Use this symmetric pattern when adjusting multiple V5 shapes in a single via cell; asymmetric displacements risk collapsing projection-measured spacing below the 33 nm minimum required by V5.S.1, V5.S.2, and V5.S.3.

**V5.AUX.1 compliance is maintained by confining resize operations to the axis of the metal run.** trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 resized only in y and was applied with conn_preserved=true; trial:i02.cu.def:VIA_VIA56_2_2_66_58.01 resized M6 in y and M5 in x independently and was rejected. When V5 is resized, apply the resize along the axis where both M5 and M6 provide adequate enclosure margin; simultaneous x and y resizes on M5 and M6 without matching V5 changes cause V5 to fall outside one or both metals, violating V5.AUX.1.

### Channel and Repair Strategy Notes

**The cu_pool channel handles via-cell-level repairs; the unit_gate channel handles polygon and instance moves.** trial:i01 and trial:i02 both targeted def:VIA_VIA56_2_2_66_58 via cu_pool using move_via_shape and resize_via_shape ops. trial:i03.ug.leaf_0013.09 was dispatched via unit_gate and used move and move_instance ops on polygons and instances across a larger locus (x: 1728–28728, y: 3148–27092), touching M5, M6, and V5 together; it was gated_in with 217 new in-crop violations and 0 new out-of-crop violations.

**Only axis-aligned operations appear in all three recorded trials.** trial:i01.cu.def:VIA_VIA56_2_2_66_58.02, trial:i02.cu.def:VIA_VIA56_2_2_66_58.01, and trial:i03.ug.leaf_0013.09 each used exclusively x-axis or y-axis moves and resizes with no diagonal or rotational components. The GEOMETRY.NONORTHOGONAL rule flags any V5 edge not at 0°, 90°, 180°, or 270°; the accepted trial:i01 and the gated trial:i03 both used strictly axis-aligned operations and produced no NONORTHOGONAL flags on V5.

### What Has Not Worked

Resizing enclosing metal layers (M5, M6) without corresponding V5 shape changes introduced 234 net new violations (trial:i02.cu.def:VIA_VIA56_2_2_66_58.01, rejected as rejected_net_positive). Avoid this approach for any repair targeting V5.M6.AUX.2 or V5.M5.EN.1/V5.M6.EN.2.