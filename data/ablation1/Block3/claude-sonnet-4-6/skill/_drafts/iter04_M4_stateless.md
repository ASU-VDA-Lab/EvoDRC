**Via enclosure — prefer M5 trim over M4 resize when competing fixes exist (V3.M4.EN.2, V4.M4.EN.1)**

When a via-enclosure shortfall drives M4 violations, resizing the M4 via shape produced a worse outcome than trimming the adjacent M5 shape. In trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, a five-op fix that included resize_via_shape on M4 (x-axis, +152 dbu) for cell VIA_VIA45_1_2_58_58 achieved delta_total=−18 but lost_tournament. The competing single-op fix in trial:i01.cu.def:VIA_VIA45_1_2_58_58.02 trimmed only M5 (resize_via_shape, y-axis, −88 dbu) and achieved delta_total=−20, which was applied. When both a V4.M4.EN.1/V3.M4.EN.2 repair and an M5 trim are in the pool for the same via cell, rank the M5 trim first.

**Horizontal-edge grid — all y-moves must be multiples of 24 dbu (M4.AUX.1)**

M4.AUX.1 requires every horizontal M4 edge to lie on a 24 nm grid. Every y-direction delta_dbu in applied or gated_in trials is a multiple of 24: ±24, ±48, ±72, ±96 dbu appear in trial:i02.ug.leaf_0002.01 and trial:i02.ug.leaf_0003.02 and trial:i03.ug.leaf_0003.02. Never move M4 geometry in y by an amount that is not a multiple of 24 dbu; any such move would displace every horizontal edge of the polygon off-grid and fire M4.AUX.1 at each.

The −4 dbu instance move in trial:i04.ug.leaf_0001.00 is a horizontal (x-axis) shift and does not change horizontal-edge y-coordinates; that trial was gated_in with n_new_out_of_crop=0, confirming that a pure x-direction move does not trigger M4.AUX.1.

**Routing-track centerline alignment — x-axis shifts do not trigger M4.AUX.2**

M4.AUX.2 checks that minimum-width M4 tracks lie on horizontal centerlines at a 192 dbu pitch with a 48 dbu offset (y-axis only). In trial:i03.ug.leaf_0002.01 (group fix_m5aux1), M4 polygon p1060 and five instances were all shifted −64 dbu in x. That trial was gated_in with n_new_out_of_crop=0, showing that a pure x-translation does not move track centerlines off the required y-grid and does not fire M4.AUX.2. When correcting M5.AUX violations that also touch M4, a coordinated x-shift of the M4 polygon with its via instances is safe with respect to M4.AUX.2.

**No-bend constraint — single-axis edge moves are safe; simultaneous multi-edge moves on non-parallel sides are not (M4.AUX.3)**

M4.AUX.3 prohibits bends (corner angles in the 0°–90° range). All applied M4 shape edits in the history operate on a single axis at a time: resize_via_shape along x in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 and resize_end along x for polygon p1059 (low-end +64 dbu, high-end +320 dbu) in trial:i02.ug.leaf_0003.02. Both trials were either applied or gated_in with no M4.AUX.3 fires. Single-axis edge moves on a rectilinear M4 polygon cannot introduce a corner. Avoid any operation that simultaneously displaces non-parallel M4 edges, as that is the geometry class that can insert a new corner and violate M4.AUX.3.

**Wide-polygon track-edge rule — horizontal resizes that stay in the safe y-band are clean (M4.AUX.4)**

M4.AUX.4 prohibits horizontal edges of wide M4 polygons from coinciding with routing-track boundaries. The resize_end in trial:i02.ug.leaf_0003.02 expanded p1059 by +320 dbu on the high x-end; n_new_out_of_crop=0 confirms the polygon's horizontal (y-constant) edges were not moved onto forbidden track boundaries by that resize. When extending a wide M4 polygon along x, the y-positions of its top and bottom edges are unchanged, so M4.AUX.4 is not disturbed by horizontal-only resizes.

**Vertical width — keep width in odd-multiple-of-24 dbu range (M4.W.1, M4.W.2, M4.W.3, M4.W.4)**

M4.W.1 sets minimum vertical width at 24 nm; M4.W.2 caps it at 480 nm; M4.W.3 and M4.W.4 prohibit widths that are even multiples of 24 nm (48, 96, 144, …, 480 nm) or that span even numbers of routing tracks (72, 168, 264, 360, 456 nm). Every y-axis delta in gated_in or applied trials (±24, ±48, ±72, ±96 dbu — trial:i02.ug.leaf_0002.01, trial:i02.ug.leaf_0003.02, trial:i03.ug.leaf_0003.02) maintains widths at values that are odd multiples of 24 (e.g., 24, 120, 216 nm) or at known-safe starting widths. After any resize that changes M4 vertical extent, verify the resulting width is not an even multiple of 24 nm and is not in the forbidden even-track-count set before committing.

**V3 width-matching preserved by co-moving via instances (V3.M4.AUX.2)**

V3.M4.AUX.2 requires V3 to exactly match M4 width in the direction perpendicular to M4 length. In trial:i02.ug.leaf_0002.01, trial:i02.ug.leaf_0003.02, and trial:i03.ug.leaf_0002.01, instance moves shift M4-bearing and via-bearing cells together; all three trials report n_new_out_of_crop=0 and conn_preserved=true. Moving M4 instances and their via instances by the same delta preserves the relative geometry required by V3.M4.AUX.2. Never move an M4-bearing instance without co-moving the corresponding V3/V4 via instances by the same vector.

**Repeated rejection of +32 dbu x-shift on polygon p1060 (M4.S.1, M4.S.2)**

Moving polygon p1060 and M5 via shape 0 in cell VIA_VIA45_1_2_58_58 by +32 dbu in x increased the total DRC violation count by 28 (trial:i02.cu.def:VIA_VIA45_1_2_58_58.00, rejected_net_positive). The same operation was assembled and then dropped from trial:i02.ug.leaf_0002.01 with reason cu_pool:rejected_net_positive. The M4 layer is in touched_layers for both records. Do not apply the +32 dbu x-shift to polygon p1060 or to M5 via shape 0 in that cell at this locus; it has been rejected at both the cu_pool and unit_gate stages.

**Sub-grid x-moves on instances do not disturb M4.AUX.1 or M4.AUX.2**

The −4 dbu x-move on instance i0132 in trial:i04.ug.leaf_0001.00 touches M3, M4, and V3. The trial was gated_in with n_new_in_crop=10 and n_new_out_of_crop=0. Because M4.AUX.1 checks horizontal-edge y-coordinates and M4.AUX.2 checks y-centerlines of minimum-width tracks, neither rule is disturbed by a displacement that is purely along x. A sub-24 dbu x-shift on an instance is safe with respect to both M4.AUX.1 and M4.AUX.2 as long as the move does not cause M4 vertical edges to violate M4.S.2 spacing.