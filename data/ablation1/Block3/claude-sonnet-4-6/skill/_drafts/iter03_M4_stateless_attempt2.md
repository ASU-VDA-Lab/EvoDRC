**V4.M4.EN.1: Resizing M5 Outperforms Resizing M4 or V4**

In iter 1 at target def:VIA_VIA45_1_2_58_58, two candidates competed. trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 resized M4 by +152 dbu on the x-axis and moved/resized two V4 shapes, reaching delta_total=-18. trial:i01.cu.def:VIA_VIA45_1_2_58_58.02 resized only the M5 shape by -88 dbu on the y-axis, reached delta_total=-20, and was applied; the M4+V4 candidate lost the tournament. When correcting V4.M4.EN.1 enclosure violations at this via cell, resize M5 instead of M4 or V4: trial:i01.cu.def:VIA_VIA45_1_2_58_58.02 confirms this produces the lower violation count.

**+32 dbu X-Shift on M5 Shapes in VIA_VIA45_1_2_58_58 Increases Violations When leaf_0003 Is in the Locus**

trial:i02.cu.def:VIA_VIA45_1_2_58_58.00 applied a +32 dbu x-move to M5 polygon p1060 and to the M5 via shape in VIA_VIA45_1_2_58_58. The outcome was rejected_net_positive with delta_total=+28; the leaf_0003 window count rose from 17 to 46. The identical ops were independently dropped from trial:i02.ug.leaf_0002.01 at assemble time (assemble_drops reason: cu_pool:rejected_net_positive) when leaf_0003 was inside the repair locus. Do not apply a +32 dbu x-shift to p1060 or the M5 via shape of VIA_VIA45_1_2_58_58 when leaf_0003 is within the active repair window, as confirmed by both trial:i02.cu.def:VIA_VIA45_1_2_58_58.00 and trial:i02.ug.leaf_0002.01.

**-64 dbu X-Move Resolves fix_m5aux1 Without New Out-of-Crop Violations**

trial:i03.ug.leaf_0002.01 applied -64 dbu x-moves to p1060 and to instances i0163, i0177, i0079, i0078, i0140 under group fix_m5aux1 and was gated_in with n_new_in_crop=8 and n_new_out_of_crop=0. This negative x-direction group shift was accepted where the +32 dbu shift was not. Use -64 dbu x-moves in the fix_m5aux1 group rather than +32 dbu, as established by trial:i03.ug.leaf_0002.01.

**Y-Direction Instance Moves Must Be Multiples of 24 dbu**

Every y-axis instance move that was gated_in used a displacement that is a multiple of 24 dbu. trial:i02.ug.leaf_0002.01 applied moves of -48, -48, -96, -96, +48, +48 dbu on the y-axis (all multiples of 48, hence of 24). trial:i02.ug.leaf_0003.02 applied +72, +72, +24, +24, -24, -24, +24, +24 dbu. trial:i03.ug.leaf_0003.02 applied -96, -96 dbu. Apply y-direction instance moves only in multiples of 24 dbu to preserve M4 horizontal-edge alignment on the 24 nm grid (M4.AUX.1) and to keep minimum-width M4 tracks on the horizontal routing tracks (M4.AUX.2), as confirmed across trial:i02.ug.leaf_0002.01, trial:i02.ug.leaf_0003.02, and trial:i03.ug.leaf_0003.02.

**X-Axis End Resizes on p1059**

trial:i02.ug.leaf_0003.02 resized the low end of polygon p1059 by +64 dbu and the high end by +320 dbu on the x-axis and was gated_in with n_new_in_crop=12 and n_new_out_of_crop=0. These horizontal end resizes did not introduce out-of-crop violations, consistent with M4.W.5 (minimum horizontal width 44 nm) being satisfied by the resulting geometry.