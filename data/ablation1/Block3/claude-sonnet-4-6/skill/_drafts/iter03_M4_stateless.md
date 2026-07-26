## Via-Cell M4 Resize: Prefer Non-M4 Adjustments When Fixing V4.M4.EN.1

In VIA_VIA45_1_2_58_58, trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 applied a +152 dbu x-axis resize to the M4 via shape alongside two large V4 x-resizes (+384 dbu each) and V4 repositioning. Despite reducing the total DRC count by 18 (leaf_0018: 32→22, leaf_0019: 35→27), this multi-operation package lost the tournament to trial:i01.cu.def:VIA_VIA45_1_2_58_58.02, which touched only M5 (a single -88 dbu y-resize) and achieved a delta of -20. Do not reach for M4 x-resizes in this via cell when an M5-only adjustment is available; the M5 operation produces a larger net reduction at lower perturbation cost.

## Y-Direction Instance Moves Must Stay on the 24 dbu Grid

Every gated-in unit_gate trial that touches M4 uses y-direction instance move deltas that are exact multiples of 24 dbu. Trial:i02.ug.leaf_0002.01 used deltas of −48, −48, −96, −96, +48, and +48 dbu (all ×24). Trial:i02.ug.leaf_0003.02 used +72, +72, +24, +24, −24, −24, +24, +24 dbu (all ×24). Trial:i03.ug.leaf_0003.02 used −96 dbu for two instances (×24). This is required by M4.AUX.1 (horizontal edges at 24 nm grid) and M4.AUX.2 (minimum-width M4 tracks must land on the routing grid at 192 dbu pitch with 48 dbu offset). Never propose a y-delta for an instance move that is not a multiple of 24 dbu when M4 is among the touched layers.

## Positive X-Shifts on M5/V4 Shapes Cause Large M4-Region Spill into Adjacent Windows

Trial:i02.cu.def:VIA_VIA45_1_2_58_58.00 moved M5 polygon p1060 and the associated M5 via shape +32 dbu in x. Although leaf_0002 improved by 1 violation (12→11), leaf_0003 degraded by 29 violations (17→46), yielding a net-positive delta_total of +28 and a rejected_net_positive decision. The M4, M5, and V4 layers were all listed as touched. A +32 dbu x-shift is less than the 40 dbu M4.S.2 minimum horizontal spacing and less than the 44 dbu M4.W.5 minimum horizontal width; such sub-grid adjustments disturb the horizontal spacing geometry across window boundaries without satisfying any spacing rule. Never apply a raw +32 dbu x-shift to M5/via shapes in VIA_VIA45_1_2_58_58 when leaf_0003 is inside the active repair locus.

## fix_m5aux1 Group: −64 dbu X Group Move Is the Correct Correction Direction

After trial:i02.cu.def:VIA_VIA45_1_2_58_58.00 was rejected (the +32 x-shift attempt), trial:i03.ug.leaf_0002.01 applied the fix_m5aux1 group: M5 polygon p1060 and five instances (i0163, i0177, i0079, i0078, i0140) were each moved −64 dbu in x. This was gated_in, adding 8 new in-crop violations while preserving connectivity. The touched layers included M4 and M5. The correction is in the opposite direction (−64 vs the failed +32) and at a larger magnitude. When the fix_m5aux1 group is needed, apply −64 dbu x simultaneously to the M5 polygon and all associated instances; applying only one component was dropped at assembly (trial:i02.ug.leaf_0002.01 assemble_drops shows +32 x on p1060 and its via shape were individually excluded as cu_pool:rejected_net_positive).

## Polygon End Resizes in X Touch M4 Indirectly Through Multi-Layer Cells

Trial:i02.ug.leaf_0003.02 resized polygon p1059 ends in x (+64 dbu at the low end, +320 dbu at the high end) as part of a 10-operation package that also moved 8 instances in y. M4 was listed among touched layers alongside M3, M5, V3, and V4. The trial was gated_in with 12 new in-crop violations. The x-end resize deltas (+64, +320) are multiples of 64, not directly multiples of 40 (M4.S.2) or 44 (M4.W.5); the M4 impact here flows through the parent cell geometry, not from a direct M4 polygon resize. When an x end-resize on a non-M4 polygon touches M4, verify that the resulting M4 geometry still satisfies M4.S.2 (40 nm horizontal spacing) and M4.W.5 (44 nm horizontal width) before committing.

## M4.W.3 and M4.W.4 Constrain Permissible Vertical Width Values

No trial in this history directly triggered M4.W.3 or M4.W.4, but the rules establish absolute forbidden values for M4 vertical width. M4.W.3 prohibits even-integer multiples of 24 nm: 48, 96, 144, 192, 240, 288, 336, 384, 432, 480 nm. M4.W.4 additionally prohibits widths that span an even number of minimum-width routing tracks: 72, 168, 264, 360, 456 nm. After any y-direction instance move that touches M4 (as in trial:i02.ug.leaf_0002.01 and trial:i03.ug.leaf_0003.02), verify that no M4 polygon vertical extent lands on these values.

## M4.AUX.3 (No Bends) and NONORTHOGONAL Rule Constrain All Reshape Operations

M4.AUX.3 requires that M4 polygons not bend; the NONORTHOGONAL block forbids any non-orthogonal edges on M4. Neither rule was violated in any trial in this history, consistent with all observed M4 operations being axis-aligned resizes and instance moves. Do not apply diagonal or rotational transforms to M4 shapes. All resize_end and resize_via_shape operations observed (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 at +152 x on M4; trial:i02.ug.leaf_0003.02 at +64/+320 x on p1059) are single-axis.