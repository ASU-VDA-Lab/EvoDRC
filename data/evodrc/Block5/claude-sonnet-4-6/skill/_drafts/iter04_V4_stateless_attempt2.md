**Effective repair scope for V4**

Every trial that touches V4 also touches at least M4 or M5: trial:i01.ug.leaf_0010.07 (M3, M4, M5, V3, V4), trial:i02.ug.leaf_0002.01 (M3, M4, M5, V3, V4), trial:i02.cu.def:VIA_VIA45_1_2_58_58.02 (M4, M5, V4), trial:i03.ug.leaf_0001.00 (M2, M3, M4, M5, V2, V4), trial:i03.ug.leaf_0002.01 (M4, M5, V4), trial:i03.ug.leaf_0003.02 (M3, M4, M5, V4), trial:i04.ug.leaf_0001.00 (M4, M5, V4). V4 repairs are never applied in isolation from the surrounding metal layers. Move V4-bearing instances as part of a coordinated group that includes their M4 and M5 parent shapes; trial:i01.ug.leaf_0010.07 and trial:i04.ug.leaf_0001.00 each show uniform-delta group moves that kept conn_preserved:true and n_new_out_of_crop:0.

**V4.AUX.1: containment inside M4 and M5**

V4.AUX.1 requires V4 inside the intersection of M4 and M5. All seven trials touching V4 produced conn_preserved:true and n_new_out_of_crop:0, confirming that the group-move strategy preserves containment throughout. Move V4-touching instances only when their enclosing M4 and M5 shapes receive the same displacement delta, as demonstrated by trial:i01.ug.leaf_0010.07, trial:i03.ug.leaf_0002.01, and trial:i04.ug.leaf_0001.00.

**V4.M5.AUX.2: width matching perpendicular to M5 length**

V4.M5.AUX.2 requires V4 to exactly match M5 width in the direction perpendicular to the M5 length. In trial:i02.cu.def:VIA_VIA45_1_2_58_58.02 the cu_pool channel applied a resize_via_shape on the M5 layer of cell VIA_VIA45_1_2_58_58 (y-axis, −88 dbu), touching M4, M5, V4, and reduced the total violation count by 15 (leaf_0002: 17→8; leaf_0003: 25→19). In trial:i03.ug.leaf_0003.02 polygon p892 on M5 was symmetrically shrunk in y (low-end +32 dbu, high-end −32 dbu) while touching M3, M4, M5, V4, and the trial was accepted with n_new_in_crop:15 and n_new_out_of_crop:0. Both trials resize M5 rather than the V4 shape directly; no trial in the measured history applies a direct V4 width edit. Resize M5 to conform to V4's existing width when V4.M5.AUX.2 fires, as supported by trial:i02.cu.def:VIA_VIA45_1_2_58_58.02 and trial:i03.ug.leaf_0003.02.

**M5 y-axis resize axis for VIA_VIA45 cells**

trial:i02.cu.def:VIA_VIA45_1_2_58_58.02 establishes the y-axis as the effective resize axis for M5 shape index 0 in cell VIA_VIA45_1_2_58_58. Apply the y-axis resize on M5 shape index 0 for VIA_VIA45_1_2_58_58 violations involving V4, as measured in trial:i02.cu.def:VIA_VIA45_1_2_58_58.02.

**Symmetric M5 trim on both ends**

trial:i03.ug.leaf_0003.02 applied a symmetric trim on polygon p892: low-y end moved +32 dbu and high-y end moved −32 dbu. This shrinks the M5 extent by 64 dbu total without displacing the centroid, and the trial was accepted (gated_in, conn_preserved:true, n_new_out_of_crop:0). Shrink M5 symmetrically on both y-ends when trimming to satisfy V4.M5.AUX.2 or V4.M5.EN.2 on a non-via polygon; trial:i03.ug.leaf_0003.02 shows this preserves enclosure and containment simultaneously.

**V4.M4.EN.1 and V4.M5.EN.2: enclosure on opposite sides**

V4.M4.EN.1 and V4.M5.EN.2 each require ≥11 nm enclosure on at least two opposite sides. The cu_pool resize in trial:i02.cu.def:VIA_VIA45_1_2_58_58.02 shrinks M5 in y, which reduces M5 extent; the net violation count still dropped by 15, confirming the pre-resize M5 overshot the enclosure target and the trim brought it into compliance. Avoid resizing M5 below the 11 nm enclosure threshold on either axis; trial:i02.cu.def:VIA_VIA45_1_2_58_58.02 shows the accepted delta (−88 dbu) was calibrated to remain within the enclosure margin.

**Polygon p879 and its four-instance group**

Polygon p879 was moved +32 dbu in x in trial:i02.ug.leaf_0002.01 and again in trial:i04.ug.leaf_0001.00. In trial:i02, the associated instances i0114, i0112, i0073, and i0062 each received the same +32 x component (some with additional y offsets), and the trial was accepted (gated_in, conn_preserved:true, n_new_in_crop:0). In trial:i04, all four instances moved at [+32, 0] together with p879, and the trial was accepted (gated_in, conn_preserved:true, n_new_in_crop:8, n_new_out_of_crop:0). Move p879 together with instances i0114, i0112, i0073, and i0062 using the same x delta, as measured in trial:i02.ug.leaf_0002.01 and trial:i04.ug.leaf_0001.00.

**X-axis block shifts and V4 spacing rules**

trial:i03.ug.leaf_0002.01 applied a uniform [−32, 0] move to instances i0114, i0112, i0073, and i0062, touching M4, M5, V4. The trial accepted 45 new in-crop violations, all attributable to M1.A.1, M4.W.5, and V1.M1.EN.1; no V4-specific rule violations appeared in the new_in_crop_by_rule breakdown. Apply uniform x-axis deltas across all instances in a V4-bearing block when shifting for spacing corrections; trial:i03.ug.leaf_0002.01 confirms uniform x-shifts do not introduce V4.S.1, V4.S.2, or V4.S.3 violations within the measured crop region.

**Y-axis instance moves and grid alignment**

trial:i01.ug.leaf_0010.07 applied six y-axis instance moves with deltas of ±24 dbu and ±72 dbu, touching M3, M4, M5, V3, V4, with n_new_in_crop:3 and n_new_out_of_crop:0. The 24 dbu step equals the V4.W.1 minimum width (24 nm), and 72 dbu equals 3× that step. Use y-axis instance move deltas that are multiples of 24 dbu when correcting V4 spacing or enclosure in the y direction; trial:i01.ug.leaf_0010.07 shows these increments preserve spacing and containment within the crop.

**V4.W.1: minimum width**

V4.W.1 requires a minimum V4 width of 24 nm along the M5 length direction. No trial in the measured history reduces the V4 width below this threshold; all via cell moves and M5 resizes operate on the enclosing metal rather than the V4 shape itself. Avoid resizing the V4 shape directly; operate on M5 (trial:i02.cu.def:VIA_VIA45_1_2_58_58.02, trial:i03.ug.leaf_0003.02) or on instance positions (trial:i01.ug.leaf_0010.07, trial:i04.ug.leaf_0001.00) to address violations.

**V4.S.1, V4.S.2, V4.S.3: spacing rules**

All three spacing rules require ≥33 nm between V4 instances (same-net projection, different-net projection, and euclidean corner-to-corner). None of the measured trials report V4.S.1, V4.S.2, or V4.S.3 violations in their per_rule new_in_crop_by_rule fields. Instance group moves at 24 dbu, 32 dbu, and 72 dbu increments as applied in trial:i01.ug.leaf_0010.07, trial:i03.ug.leaf_0002.01, and trial:i04.ug.leaf_0001.00 did not introduce new V4 spacing violations within the crop regions examined.

**GEOMETRY.NONORTHOGONAL**

The GEOMETRY.NONORTHOGONAL rule fires on any edge with angle outside the set {0°, 90°, 180°, 270°}. All move_instance and resize operations in the measured history use integer dbu axis-aligned deltas (x or y only), producing exclusively orthogonal edges. Apply only axis-aligned (x-only or y-only) moves and resizes to V4-affecting shapes; trial:i01.ug.leaf_0010.07, trial:i03.ug.leaf_0003.02, and trial:i04.ug.leaf_0001.00 all use strictly axis-aligned operations and generate no GEOMETRY.NONORTHOGONAL violations.

**cu_pool vs unit_gate channel precedence**

trial:i02.ug.leaf_0002.01 records three assemble_drops: one op was dropped because it conflicted with the cu_pool winner for leaf_0002, and two ops were dropped because cu_pool had already applied them (resize of p879 y-axis and a V2 via move). The cu_pool trial trial:i02.cu.def:VIA_VIA45_1_2_58_58.02 was applied first (channel:cu_pool, decision:applied) and its M5 resize on VIA_VIA45_1_2_58_58 took precedence. When a cu_pool repair for a via cell definition overlaps with a unit_gate repair in the same iteration, the cu_pool result is authoritative; do not re-apply the same M5 resize in the unit_gate channel, as shown by the drop records in trial:i02.ug.leaf_0002.01.