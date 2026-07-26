## Via enclosure violations: resize the via, not the metal

The single resolved trial on this layer targeted cell `VIA_VIA56_2_2_66_58`, applying four `resize_via_shape` operations on `V5` along the y-axis (delta +248 dbu each), which reduced the total violation count by 32 with connectivity preserved (trial:i01.cu.def:VIA_VIA56_2_2_66_58.01). `M6` was among the touched layers in that repair, confirming that M6-side violations (most directly V5.M6.EN.2, which requires ≥11 nm enclosure of V5 by M6 on two opposite sides) were resolved by bringing the V5 shape into alignment with the existing M6 metal rather than resizing M6 itself.

When V5.M6.EN.2 fires, resize the V5 via shapes in the y-axis to achieve the required enclosure; do not move or resize the M6 polygon to chase the via (trial:i01.cu.def:VIA_VIA56_2_2_66_58.01).

All four V5 shapes in `VIA_VIA56_2_2_66_58` received identical y-axis deltas of 248 dbu in the same operation batch (trial:i01.cu.def:VIA_VIA56_2_2_66_58.01). Apply the same delta to every via shape within the cell instance; partial application across shapes in the same cell left no residual violations in this case.

## Width and spacing rules: no measured repair yet

Rules M6.W.1 (min vertical width 32 nm), M6.W.2 (max vertical width 640 nm), M6.W.3 (even-multiple-of-32 nm widths forbidden), M6.W.4 (widths spanning an even number of routing tracks forbidden), M6.W.5 (min horizontal width 44 nm), M6.S.1 (min vertical spacing 32 nm), M6.S.2 (min horizontal spacing 40 nm), M6.S.3 (tip-to-tip spacing on adjacent tracks without shared parallel run 40 nm), M6.S.4 (tip-to-tip spacing on adjacent tracks with shared parallel run 40 nm), and M6.S.5 (min parallel run length on adjacent tracks 44 nm) have produced no repair records in this layer's history. No prescriptive repair guidance is available for these rules yet.

## Grid and routing-track alignment: no measured repair yet

M6.AUX.1 (M6 horizontal edges on 32 nm grid), M6.AUX.2 (minimum-width M6 tracks must center on horizontal routing tracks pitched at 256 dbu with 64 dbu offset), M6.AUX.3 (M6 may not bend), M6.AUX.4 (outside edge of a wide M6 polygon may not touch a routing track edge), and V5.M6.AUX.2 (V5 width must match M6 width perpendicular to M6 length) have produced no repair records in this layer's history. No prescriptive repair guidance is available for these rules yet.

## V6 enclosure: no measured repair yet

V6.M6.EN.1 (min enclosure of V6 by M6 on at least two opposite sides is 11 nm) has produced no repair records in this layer's history. No prescriptive repair guidance is available for this rule yet.