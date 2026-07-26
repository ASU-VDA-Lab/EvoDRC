## Layer M4 Repair Knowledge

### Layer orientation and geometry

M4 is a horizontal routing layer. Rules M4.W.1/W.2 constrain vertical (y-axis) width to 24–480 nm, while M4.W.5 constrains horizontal (x-axis) width to a minimum of 44 nm. M4.AUX.3 prohibits any bending. All repair operations observed in the history operate exclusively on x-axis endpoints (resize_end axis:x, move_via_shape axis:x), consistent with horizontal wire extension or shrinkage being the only geometrically legal M4 modification.

### Effective repair pattern: horizontal endpoint extension

The dominant successful M4 repair is `resize_end` on the x-axis, extending either the high or low endpoint. In trial:i01.ug.Block4_union_row10.01, four M4 polygons were extended horizontally (deltas +64, +72, +92, +128 dbu on mixed high/low ends) with zero new violations introduced. In trial:i01.ug.Block4_union_row7.06, four M4 polygons were extended at the high end (+56, +92, +164, +172 dbu) with zero new violations. In trial:i01.ug.leaf_0001.07, a single M4 polygon (p1374) was extended +96 dbu at the high end on M4 exclusively, accepted with zero new violations. All three were accepted via the unit_gate channel with `conn_preserved=true` and `gated_in` decisions.

### Via cell M4 resize via the cu_pool channel

Via cell repairs that include M4 shapes are conducted through the cu_pool channel. In trial:i05.cu.def:VIA_VIA45_1_2_58_58.01, an M4 via shape was resized +152 dbu in x (resize_via_shape, shape_index 0), paired with lateral movement and enlargement of V4 shapes; this trial was applied with a net reduction of 38 violations across two units. This is the only cu_pool trial in the history where M4 changes were accepted.

### Via shrinkage on adjacent layers can increase M4-region violations

In trial:i01.cu.def:VIA_VIA34_1_2_58_52.01, shrinking M3 and V3 via shapes along the y-axis (M3: −64 dbu, V3: −24 dbu each for two shapes) in a cell that also touches M4 was rejected with `rejected_net_positive` (+34 new violations, split across leaf_0025 and leaf_0026). Although the ops did not directly modify M4 geometry, the design state touched M4 and the violation count increased. Avoid y-axis shrinkage of adjacent via-cell layers when M4 is part of the same via stack without confirming the M4 enclosure margins satisfy V3.M4.EN.2 (11 nm minimum on two opposite sides) and V3.M4.AUX.2 (V3 width must equal M4 width perpendicular to M4 length).

### Instance moves paired with M4 extension

Multi-instance moves in the unit_gate channel consistently accompany M4 resize_end operations. In trial:i01.ug.Block4_union_row10.01, three instance moves (±108, +36 dbu in x) accompanied four M4 endpoint adjustments. In trial:i01.ug.Block4_union_row7.06, four instance moves (−28, +36, +36, +108 dbu in x) accompanied four M4 high-end extensions. The M4 resize deltas are not equal to the corresponding instance delta_dbu values, indicating the M4 polygon dimensions are adjusted independently to maintain spacing and enclosure rules (M4.S.1 24 nm vertical spacing, M4.S.2 40 nm horizontal spacing, M4.W.5 44 nm minimum horizontal width) relative to the repositioned via and instance geometry.

### Enclosure rules constrain M4 length relative to V3 and V4

V3.M4.EN.2 requires V3 to be enclosed by M4 by at least 11 nm on two opposite sides. V3.M4.AUX.2 requires V3 to exactly match M4 width in the direction perpendicular to M4 length. V4.M4.EN.1 imposes the same 11 nm two-sided enclosure for V4 by M4. These rules directly bound how far M4 endpoints may be retracted near via locations. The successful cu_pool repair in trial:i05.cu.def:VIA_VIA45_1_2_58_58.01 extended M4 (+152 dbu x) while enlarging V4 shapes (+384 dbu x each), maintaining the enclosure margin rather than shrinking it.

### Track grid and forbidden widths

M4.AUX.1 requires M4 horizontal edges on a 24 nm grid. M4.AUX.2 requires minimum-width M4 tracks to have their centerlines on horizontal routing tracks spaced at 192 dbu pitch with a 48 dbu offset from origin. M4.W.3 and M4.W.4 forbid vertical widths that are even integer multiples of 24 nm (48, 96, 144, 192, 240, 288, 336, 384, 432, 480 nm) and widths equal to 72, 168, 264, 360, or 456 nm. Valid minimum-width M4 is 24 nm vertically. All successful repairs in trial:i01.ug.Block4_union_row10.01, trial:i01.ug.Block4_union_row7.06, and trial:i01.ug.leaf_0001.07 operated only on x-axis endpoints and did not alter the M4 vertical width, avoiding these forbidden-width violations entirely.

### Multi-layer moves with M4 involvement but no direct M4 ops

In trial:i04.ug.leaf_0002.01, M4 was listed in touched_layers but all operations were x-axis moves of M5 polygon and y-axis moves of M5/V3/V4 instances under the m5_align group. No M4 polygon or via-shape ops were performed directly. The trial was accepted (gated_in, conn_preserved) despite introducing 2 new violations within the crop window, because connectivity was preserved. This shows that M4 can appear in touched_layers due to adjacent-layer perturbations without requiring direct M4 modification, and the gating criterion is connectivity preservation, not zero new local violations.