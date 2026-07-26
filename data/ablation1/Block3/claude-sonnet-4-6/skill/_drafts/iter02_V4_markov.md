**Cell VIA_VIA45_1_2_58_58: repair summary across two iterations**

Both iteration-1 trials operated on cell `VIA_VIA45_1_2_58_58` at locus [1728, 2068, 11016, 10892], with violations spread across two windows: `unit:leaf_0018` (baseline 32) and `unit:leaf_0019` (baseline 35). Layers M4, M5, and V4 were marked as touched in all cu_pool trials at this locus.

**Applied fix: single M5 y-axis resize (iteration 1 winner)**

Trial:i01.cu.def:VIA_VIA45_1_2_58_58.02 applied one operation — an M5 shape y-axis resize of -88 dbu — and was the applied winner with a total delta of -20 (leaf_0018: 32→21, leaf_0019: 35→26). This single-operation approach produced the larger violation reduction across both windows.

**Losing approach: five-operation V4/M4 x-axis rework (iteration 1)**

Trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 executed five operations targeting V4 and M4: two V4 shape moves along the x-axis (-116 dbu and +116 dbu respectively), two V4 shape x-axis resizes (+384 dbu each, one per shape), and one M4 shape x-axis resize (+152 dbu). Despite this broader intervention, the total delta was only -18 (leaf_0018: 32→22, leaf_0019: 35→27), and the trial lost the tournament against trial:i01.cu.def:VIA_VIA45_1_2_58_58.02.

**x-axis M5 move spreads violations across adjacent windows: do not apply**

Trial:i02.cu.def:VIA_VIA45_1_2_58_58.00 moved both polygon p1060 and the VIA_VIA45_1_2_58_58 M5 via shape (shape_index 0) +32 dbu along the x-axis. This was rejected as net_positive: delta_total was +28, with leaf_0002 improving by only -1 (12→11) while leaf_0003 worsened by +29 (17→46). Do not apply x-axis M5 moves at locus [1728, 2068, 11016, 10892] without verifying the leaf_0003 window; trial:i02.cu.def:VIA_VIA45_1_2_58_58.00 confirms this cross-window damage is severe. The same two ops were also listed in the assemble_drops for trial:i02.ug.leaf_0002.01 under the reason `cu_pool:rejected_net_positive`, confirming the rejection propagated into the unit-gate assembly.

**y-axis instance moves at this locus introduce M1/V1 cascades**

Trial:i02.ug.leaf_0002.01 applied six instance moves (y-axis offsets: i0177 -48, i0152 -48, i0079 -96, i0102 -96, i0078 +48, i0101 +48 dbu) touching layers M3, M4, M5, V3, V4 at locus [1728, 2068, 11016, 10892]. The trial was gated_in on conn_preserved grounds but introduced 8 new violations — 4 in M1.A.1 and 4 in V1.M1.EN.1. Instance moves that shift upper-metal instances in y at this locus propagate geometry changes into M1 and V1 layers. Avoid y-axis instance moves at this locus without checking M1.A.1 and V1.M1.EN.1 impacts; trial:i02.ug.leaf_0002.01 demonstrates this cascade.

**Mixed x-resize and y-instance-move repairs at adjacent locus also introduced violations (iteration 2)**

Trial:i02.ug.leaf_0003.02 at locus [1728, 3148, 11016, 9812] applied 10 operations: two x-axis resize_end operations on polygon p1059 (+64 dbu low end, +320 dbu high end, net +384 dbu) and eight y-axis instance moves across instances i0173, i0151, i0147, i0192, i0083, i0096, i0085, i0088. It was gated_in via conn_preserved but introduced 12 new_in_crop violations. Polygon p1059 x-axis expansion of net +384 dbu at this adjacent locus carries a substantial new-violation cost similar to the pattern seen in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, which also used +384 dbu V4 x-axis resizes and underperformed the M5-only approach.

**Rule context: why M5 y-axis resizing is load-bearing for V4 violations**

Rule V4.M5.AUX.2 requires that every V4 instance match the M5 width in the direction perpendicular to the M5 length; V4 edges must be coincident with M5 edges on at least two sides. Rule V4.M5.EN.2 additionally requires M5 to enclose V4 by at least 11 nm on two opposite sides. Shrinking M5 in the y-axis (trial:i01.cu.def:VIA_VIA45_1_2_58_58.02) simultaneously adjusts the M5 boundary relative to V4, directly affecting both the coincidence check in V4.M5.AUX.2 and the enclosure check in V4.M5.EN.2 without changing V4 geometry.

**Direct V4 x-axis resizing interacts with spacing rules**

Rules V4.S.1 and V4.S.2 both impose a 33 nm projection-mode minimum spacing between V4 instances (same-net and different-net respectively). Rule V4.S.3 imposes a 33 nm euclidean corner-to-corner minimum. In trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, the two V4 shapes were each resized +384 dbu along the x-axis; enlarging V4 shapes directly expands the geometry subject to all three spacing checks. That trial lost the tournament with a smaller net delta (-18) compared to the M5-only approach (-20 in trial:i01.cu.def:VIA_VIA45_1_2_58_58.02). The +384 dbu x-axis polygon expansion at locus [1728, 3148, 11016, 9812] in trial:i02.ug.leaf_0003.02 further corroborates that large x-axis expansions of M5/V4-adjacent polygons introduce violations.

**Rule V4.AUX.1 and containment during M5 resize**

Rule V4.AUX.1 requires every V4 instance to lie fully inside the intersection of M4 and M5. A y-axis M5 shrink (trial:i01.cu.def:VIA_VIA45_1_2_58_58.02) reduces the M5 boundary and, if V4 is not also shrunk or moved, risks a V4.AUX.1 violation. The fact that trial:i01.cu.def:VIA_VIA45_1_2_58_58.02 was applied with `conn_preserved: true` and produced a net improvement confirms that the -88 dbu y-axis shrink did not push V4 outside M5 in this instance. Future M5 y-axis resizes must be verified against V4.AUX.1 containment using the specific V4 dimensions at the target locus.

**Rule V4.W.1 and minimum width**

Rule V4.W.1 requires each V4 instance to be at least 24 nm wide along the M5 length direction. The two +384 dbu x-axis resizes in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 expanded V4 width, moving away from V4.W.1 risk. The applied trial:i01.cu.def:VIA_VIA45_1_2_58_58.02 did not touch V4 geometry at all, leaving V4 width unchanged; V4.W.1 compliance was unaffected by the winning repair.

**Rule V4.M4.EN.1 and M4 interaction**

Rule V4.M4.EN.1 requires M4 to enclose V4 by at least 11 nm on two opposite sides (checked via x- and y-axis erosions). Trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 included an M4 x-axis resize of +152 dbu alongside the V4 moves and resizes, indicating that expanding V4 in x required compensating M4 growth to satisfy V4.M4.EN.1. The applied trial:i01.cu.def:VIA_VIA45_1_2_58_58.02 required no M4 change, consistent with no V4 geometry modification.

**Op-count and operation-type observations**

The 5-operation sequence in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 produced a smaller DRC reduction (-18) than the 1-operation sequence in trial:i01.cu.def:VIA_VIA45_1_2_58_58.02 (-20). The 2-operation x-axis M5 move in trial:i02.cu.def:VIA_VIA45_1_2_58_58.00 was net_positive (+28). The 6-operation y-axis instance-move sequence in trial:i02.ug.leaf_0002.01 introduced 8 new M1/V1 violations. At this locus family, M5 y-axis shrink is the only measured approach that reduced violations without generating new ones in other layers or windows.