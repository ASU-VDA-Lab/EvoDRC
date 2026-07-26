**Connectivity preservation is the gating criterion**

The single gated_out outcome (trial:i01.ug.leaf_0034.12) was rejected because `conn_preserved=false`, reason `conn_broken`. All 11 gated_in trials have `conn_preserved=true`. Do not apply any M1 operation set that severs net connectivity; trial:i01.ug.leaf_0034.12 shows this is a hard gate that overrides all other considerations.

**New violations inside the crop window do not block gating when connectivity is preserved**

Three gated_in trials introduced net-new violations inside the crop window: trial:i01.ug.Block1_union_row1.00 (n_new_in_crop=4), trial:i01.ug.Block1_union_row6.06 (n_new_in_crop=1), and trial:i01.ug.leaf_0031.11 (n_new_in_crop=4); all three were accepted. All 12 trials report n_new_out_of_crop=0, meaning violations must not escape outside the crop boundary.

**The unit_gate channel always co-modifies M1, V1, and M2**

Every trial has `touched_layers` containing M1, V1, and M2 (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row3.03, trial:i01.ug.Block1_union_row4.04, trial:i01.ug.Block1_union_row5.05, trial:i01.ug.Block1_union_row6.06, trial:i01.ug.Block1_union_row8.07, trial:i01.ug.Block1_union_row9.08, trial:i01.ug.leaf_0004.09, trial:i01.ug.leaf_0020.10, trial:i01.ug.leaf_0031.11, trial:i01.ug.leaf_0034.12). M1 endpoint adjustments must satisfy V0.M1.EN.1 (M1 must enclose V0 on two opposite sides by 5 & 5 nm or 5 & 0 nm), V0.M1.AUX.3 (V0 width must exactly match M1 width perpendicular to M1 length), and V1.M1.EN.1 (M1 must enclose V1 on two opposite sides by 5 & 2 nm) whenever a V0 or V1 via is present in the affected region.

**Apply move_instance to shift cells along the x-axis**

All move_instance operations across the 12 trials use a [dx, 0] displacement vector with the y component equal to zero (trial:i01.ug.Block1_union_row1.00 i0507 delta_dbu=[136,0]; trial:i01.ug.leaf_0020.10 i0082 delta_dbu=[-56,0]; trial:i01.ug.Block1_union_row6.06 i0455 delta_dbu=[-72,0]). Positive x-displacements observed in accepted trials: 8, 36, 37, 64, 72, 108, 136 dbu (trial:i01.ug.Block1_union_row4.04 i0300 delta_dbu=[8,0]; trial:i01.ug.Block1_union_row9.08 i0195 delta_dbu=[36,0]; trial:i01.ug.Block1_union_row1.00 i0507 delta_dbu=[136,0]). Negative x-displacements observed in accepted trials: -36, -56, -64, -72 dbu (trial:i01.ug.Block1_union_row5.05 i0433 delta_dbu=[-36,0]; trial:i01.ug.leaf_0020.10 i0082 delta_dbu=[-56,0]; trial:i01.ug.Block1_union_row8.07 i0258 delta_dbu=[-64,0]; trial:i01.ug.Block1_union_row6.06 i0455 delta_dbu=[-72,0]).

**Apply resize_end to adjust individual M1 polygon endpoints along axis x**

All resize_end operations in accepted trials specify `axis=x` and target either `end=high` or `end=low` (trial:i01.ug.Block1_union_row1.00 p1320 axis=x end=high delta=136; trial:i01.ug.Block1_union_row5.05 p1295 axis=x end=high delta=156 and p1305 axis=x end=low delta=56; trial:i01.ug.Block1_union_row6.06 p1323 axis=x end=high delta=36, p1329 axis=x end=high delta=128, p1346 axis=x end=low delta=36, p1325 axis=x end=high delta=128, p1250 axis=x end=high delta=92; trial:i01.ug.Block1_union_row8.07 p1388 axis=x end=high delta=192 and p1345 axis=x end=high delta=192). resize_end changes the length of one M1 segment edge, which can alter whether that edge classifies as a tip (≤ 36 nm) or side (> 36 nm) under M1.S.1 through M1.S.5.

**Do not couple M1 changes to modifications of M3 or higher layers**

trial:i01.ug.leaf_0034.12 is the only trial to include M3, M4, and V2 in `touched_layers`, and it is the only gated_out trial. Avoid extending M1 repairs to operations that touch M3 or higher layers in the same trial; the 11 accepted trials exclusively touched M1, V1, and M2 (trial:i01.ug.Block1_union_row1.00 through trial:i01.ug.leaf_0031.11).

**Retraction operations must preserve M1.W.1 and M1.A.1 minimums**

M1.W.1 requires a minimum M1 width of 18 nm; M1.A.1 requires a minimum area of 504 nm². Any resize_end that shortens an M1 segment must leave the resulting polygon no narrower than 18 nm and no smaller than 504 nm². Accepted trials include end=low retraction operations: trial:i01.ug.Block1_union_row5.05 retracts p1305 (axis=x end=low delta=56) and trial:i01.ug.Block1_union_row6.06 retracts p1346 (axis=x end=low delta=36); both trials were gated_in.

**M1 spacing rules classify edges by length into three tiers**

M1 edges longer than 36 nm are side edges; edges from 24 nm to 36 nm inclusive are wide tips; edges below 24 nm are narrow tips. Minimum spacings: side-to-side 18 nm (M1.S.1, both edges > 36 nm); tip-to-side 25 nm (M1.S.2, one tip ≤ 36 nm and one side > 36 nm); wide-tip-to-wide-tip 27 nm (M1.S.3, both 24–36 nm); narrow-tip-to-narrow-tip 31 nm (M1.S.4, both < 24 nm); wide-tip-to-narrow-tip 31 nm (M1.S.5); corner-to-corner 20 nm (M1.S.6). A resize_end that crosses the 36 nm or 24 nm length threshold changes which spacing rule applies to that edge. Accepted trials include large end=high extensions that substantially lengthen segments: trial:i01.ug.Block1_union_row8.07 delta=192 on p1388 and p1345, and trial:i01.ug.Block1_union_row5.05 delta=156 on p1295.

**M1.R.0 flags isolated M1 islands near large empty M1 regions**

M1.R.0 identifies M1 polygons that enclose exactly one small V0 via when those polygons are within 400 nm of a large empty M1 region (>= 500 nm wide, area > 2.5 µm²). The rule is computed by identifying empty M1 space, filtering by size, expanding by 400 nm, and flagging any single-via M1 island inside the expanded zone.

**All M1 edges must remain orthogonal**

GEOMETRY.NONORTHOGONAL applies to M1. Never introduce diagonal M1 edges through repair operations; the resize_end and move_instance operations used across all accepted trials produce only rectilinear 0° and 90° edges (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row5.05, trial:i01.ug.Block1_union_row6.06, trial:i01.ug.Block1_union_row8.07, trial:i01.ug.leaf_0004.09).