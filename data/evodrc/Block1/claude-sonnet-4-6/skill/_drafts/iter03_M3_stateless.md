**M3.S.2 (tip-to-side spacing, minimum 25 nm)**

M3.S.2 violations are the primary recurring M3 spacing issue across the measured history. Two violations appeared as new-in-crop in trial:i01.ug.leaf_0035.13 (bulk M3 resize pass on leaf_0035, axis-y shrink of 64 dbu on twelve polygons), and a further two appeared in trial:i02.ug.leaf_0004.03 (mixed polygon-move and instance-move pass on leaf_0004). Both sets were resolved together in trial:i03.ug.leaf_0003.02 using an 8 dbu inward resize_end on the high-x (right) edge of the offending tip polygon: shrinking p1543 right edge from 13876 to 13868 dbu opened the gap to the adjacent side edge of p1534 (left at 13968) to exactly 100 dbu = 25 nm, clearing violation v0014. Violation v0015 required a two-part coordinated fix: resize_end on p1458 right edge by -8 dbu, combined with a move_instance on the VIA23 cell i0180 by dx=-40 dbu so that the via's M3 land right edge also landed at 3068 dbu, achieving a 100 dbu = 25 nm gap to the adjacent M3 polygon p1480 (left at 3168). The key lesson from trial:i03.ug.leaf_0003.02 is that when a M3 tip edge abuts a via landing pad, both the freestanding M3 polygon end and the via-cell M3 shape must be moved together; adjusting only one leaves the combined merged M3 tip still violating spacing.

The minimum legal gap for M3.S.2 is exactly 25 nm (100 dbu). In trial:i03.ug.leaf_0003.02 both fixes targeted 100 dbu precisely, with no margin added beyond the rule minimum.

**V2.M3.AUX.2 (V2 width must match M3 width in perpendicular direction)**

When resizing M3 polygon ends to clear M3.S.2, V2.M3.AUX.2 alignment must be verified. In trial:i03.ug.leaf_0003.02, the resize_end on p1543 right edge (from 13876 to 13868) was confirmed safe because all V2 cut shapes inside p1543 had their rightmost edge at x=13860, which is less than the new polygon boundary at 13868, preserving the required width alignment. Do not shrink an M3 polygon end past the innermost V2 cut edge on that axis, or V2.M3.AUX.2 will be violated.

**V2.M3.EN.2 (V2 must be enclosed by M3 on two opposite sides by at least 5 nm)**

Six new V2.M3.EN.2 violations appeared as new-in-crop in trial:i02.ug.leaf_0003.02 and six more in trial:i02.ug.leaf_0004.03. Both trials involved coordinated instance moves of many cells that collectively shifted M3 landing pads relative to stationary V2 cuts. Instance moves that simultaneously shift M3 and the via cell maintain enclosure, but when M3 polygon moves and instance moves are partially applied (e.g. due to cross-crop conflicts recorded in the assemble_drops of trial:i02.ug.leaf_0004.03), the M3 polygon can end up displaced from the via, opening an enclosure gap.

Shrinking VIA_VIA23_1_3_36_36's M3 shape by -40 dbu in y at iter 1 (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00) produced zero net DRC improvement and was rejected as net_positive. Expanding the same cell's M3 shape by +24 dbu in y at iter 3 (trial:i03.cu.def:VIA_VIA23_1_3_36_36.00) was applied and reduced total DRC count by 12 in the leaf_0002 window. The direction of the via shape adjustment is critical: contraction of the M3 metal in the via cell tightens enclosure margins and can expose V2.M3.EN.2 violations, while expansion restores margin. Apply expansion via cu_pool resize_via_shape on the M3 shape when V2.M3.EN.2 violations are traced to a specific via cell definition.

**Connectivity preservation constraints on M3 resize**

Trial:i01.ug.leaf_0034.12 was gated out with decision conn_broken despite zero new out-of-crop violations (89 new in-crop). The ops in that trial included a -4 dbu resize_end on p1214, a +192 dbu resize_end on p1178, a +100 dbu resize_end on p1255, and several instance moves with dx=72–136 dbu. The combination of large end-extensions and instance displacement broke connectivity. Do not combine large polygon end-extensions with aggressive instance translations in a single M3 pass; the gating logic rejects the entire set when any net's connectivity is broken, producing a large new-in-crop count with no applied benefit.

**Cross-leaf conflict resolution and partial application**

In trial:i02.ug.leaf_0004.03, 40 ops were dropped due to external_conflict or cross_crop_first_wins because leaf_0003 had already claimed the same polygons (p1143, p1142, p1561) and instances. The surviving ops still moved p1143 (+32 x), p1142 (-16 x), and p1561 (+32 y), and the trial was gated_in. However the partial application of only half the intended lateral M3 moves (the instance moves for shared instances were dropped) is what introduced the 2 new M3.S.2 violations recorded in that trial, which were then fixed by the targeted resize in trial:i03.ug.leaf_0003.02. When cross-leaf conflicts cause instance move drops, the freestanding M3 polygon moves that depend on those instances for spacing clearance must be independently verified against M3.S.2.

**Via cell M3 shape sizing via cu_pool**

The cu_pool channel evaluated VIA_VIA23_1_3_36_36 M3 shape modification twice. At iter 1 (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00), a -40 dbu y-contraction of the M3 shape was evaluated against windows unit:leaf_0034 and unit:leaf_0035; both showed zero delta (before=182/113, after=182/113), so the op was rejected. At iter 3 (trial:i03.cu.def:VIA_VIA23_1_3_36_36.00), a +24 dbu y-expansion of the M3 shape (alongside V2 expansions of +64 dbu and M2 expansion of +64 dbu) was applied with delta_total=-12 against window unit:leaf_0002 (before=93, after=81). The same via cell that rejected a contraction at iter 1 accepted an expansion at iter 3, consistent with V2.M3.EN.2 being resolved by adding M3 metal rather than removing it.

**Bulk M3 polygon resizing for M3.S.2 clearance**

Trial:i01.ug.leaf_0035.13 applied a uniform -64 dbu axis-y resize to twelve M3 polygons (p1501, p1493, p1491, p1460, p1459, p1458, p1543, p1538, p1535, p1420, p1435, p1434) and was gated in with conn_preserved. This pass reduced M3 polygon height along y. However it introduced 2 new M3.S.2 violations (recorded in the per_rule breakdown of that trial). Uniform shrink of a set of M3 polygons along one axis reduces width risk (M3.W.1) on that axis but can open new tip-to-side spacing violations if the shrunk edge becomes a new tip edge (≤36 nm) that approaches a neighboring side edge at less than 25 nm. After bulk shrink, verify tip-to-side gaps on all newly exposed short edges.

**M3 width (M3.W.1, minimum 18 nm)**

No M3.W.1 violations appear in any new_in_crop_by_rule breakdown across the measured history. The -64 dbu axis-y resizes in trial:i01.ug.leaf_0035.13 did not trigger M3.W.1, indicating the polygon heights before shrink were sufficiently above 18 nm (72 dbu) that a 64 dbu reduction was safe. The resize_end ops in trial:i03.ug.leaf_0003.02 also did not trigger M3.W.1, as they modified the x-axis ends rather than reducing width. Track minimum polygon dimension before applying any resize to confirm 18 nm (72 dbu) is maintained on both axes after the operation.

**M3.A.1 (minimum area 504 nm²) and M3.S.6 (corner-to-corner spacing 20 nm)**

Neither M3.A.1 nor M3.S.6 appears in any new_in_crop_by_rule breakdown across the measured history. No prescriptive guidance is grounded in the measured records for these rules.