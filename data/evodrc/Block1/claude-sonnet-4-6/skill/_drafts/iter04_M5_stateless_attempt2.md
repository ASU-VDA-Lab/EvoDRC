**M5.AUX.3 — Bends in M5**

M5.AUX.3 detects any M5 polygon whose outline contains a corner in the 0°–90° angular range and flags all edges incident to those corners. Trial `i02.ug.leaf_0004.03` introduced 38 new M5.AUX.3 violations, the largest single-rule M5 violation count in the measured history (trial:i02.ug.leaf_0004.03). The op batch for that trial included 41 instance moves, of which many carried non-zero x and y components in a single displacement vector, for example [32,32], [−16,32], [32,72], [−16,72], [32,24], [−16,24], [32,−24], [−16,−24], [32,−72], [−16,−72] dbu. The instance moves that shift cell placements in both x and y simultaneously are the measured source of M5.AUX.3 violations in this block (trial:i02.ug.leaf_0004.03).

**M5.AUX.1 — Vertical M5 edges on the 24 nm grid**

M5.AUX.1 checks `m5.merged.ongrid(24.nm, 1.dbu)`, requiring every M5 vertical edge to lie at an integer multiple of 24 nm in x. Trial `i02.ug.leaf_0004.03` introduced 12 M5.AUX.1 violations from instance moves carrying +32 dbu or −16 dbu x-components applied to cells containing M5 geometry (trial:i02.ug.leaf_0004.03). These 12 violations, the 38 M5.AUX.3 violations, the 12 M5.W.5 violations, and the 4 M5.S.4 violations all originated from a single op batch in that trial. Displacement magnitudes of 32 dbu and 16 dbu are not integer multiples of 24 nm; when applied to cells whose M5 vertical edges are initially grid-aligned, they produce off-grid landing positions.

**M5.W.5 — Minimum vertical width of M5**

M5.W.5 applies `m5.width(44.nm, euclidian).with_angle(0)`, flagging any M5 shape whose minimum Euclidean distance between horizontal edges falls below 44 nm. Trial `i02.ug.leaf_0004.03` introduced 12 M5.W.5 violations from the same instance-move batch that produced the M5.AUX.3 and M5.AUX.1 violations (trial:i02.ug.leaf_0004.03). The W.5 violations co-occurred with M5.AUX.3 violations in counts of 12 and 38 respectively from identical ops.

**M5.S.4 — Minimum tip-to-tip spacing for M5 polygons sharing a parallel run**

M5.S.4 flags pairs of M5 polygon ends on adjacent tracks that share a parallel run length and whose tips are separated by less than 40 nm. Trial `i02.ug.leaf_0004.03` introduced 4 M5.S.4 violations from the same diagonal instance-move batch (trial:i02.ug.leaf_0004.03).

**V4.M5.AUX.2 — V4 width must match M5 width perpendicular to M5 length**

V4.M5.AUX.2 requires each V4 inside an M5 polygon to share edges with M5 on both sides in the direction perpendicular to M5's length, so that V4's width in that direction equals the enclosing M5 width. Trial `i02.ug.leaf_0003.02` introduced 4 V4.M5.AUX.2 violations as part of a batch that included lateral polygon moves of +32 dbu in x on p1145 and −16 dbu in x on p1144, plus y-axis moves on polygons p1563 (−64 dbu), p1562 (−112 dbu), and p1561 (−96 dbu), alongside numerous instance moves (trial:i02.ug.leaf_0003.02).

**V4.M5.EN.2 — Enclosure of V4 by M5 on two opposite sides**

V4.M5.EN.2 checks that V4 is enclosed by M5 by at least 11 nm on two opposite sides. Trial `i01.cu.def:VIA_VIA45_1_2_58_58.01` resized the M5 shape (shape_index 0, axis y, delta −88 dbu) inside cell VIA_VIA45_1_2_58_58, achieving a total violation reduction of 52 split evenly across two windows (unit:leaf_0034: −26, unit:leaf_0035: −26) with conn_preserved=true, touching layers M4, M5, and V4 (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01). This y-axis resize of the M5 via-anchor shape is the only recorded repair operation for that via cell in the measured history.

**Instance moves that introduce M5 violations without per-rule attribution**

Trial `i04.ug.leaf_0002.01` applied 16 y-axis-only instance moves (x=0, y values ±48 dbu and ±96 dbu) to cells touching M3, M4, M5, V3, and V4, producing 20 new in-crop violations; no per-rule breakdown was recorded for that trial (trial:i04.ug.leaf_0002.01). Trial `i04.ug.leaf_0003.02` applied 26 instance moves with x-components of +32 dbu or −16 dbu (y=0 for most, with two diagonal moves [32,−96] and [−16,−96] dbu) on cells touching M3, M4, M5, M6, V3, V4, and V5, producing 8 new in-crop violations with no per-rule breakdown (trial:i04.ug.leaf_0003.02). Both trials were accepted as gated_in with conn_preserved=true.

**Multi-leaf assembly conflict resolution**

Trials `i02.ug.leaf_0003.02` and `i02.ug.leaf_0004.03` (iteration 2) cover overlapping sets of instances and M5 polygons. For each instance claimed with contradictory move vectors by both leaf_0003 and leaf_0004, the assembler dropped the later leaf's op as `external_conflict_dropped` (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03). Where both leaves specified identical move vectors for the same instance, the second occurrence was dropped as `external_duplicate`. Polygon-level conflicts in the cross-crop zone were resolved by `cross_crop_first_wins`; the leaf_0003 execution of p1143 (+32 dbu x), p1142 (−16 dbu x), and p1561 (−96 dbu y) took precedence, and leaf_0004's claimed moves for those same polygons were dropped (trial:i02.ug.leaf_0004.03). Dropped operations leave no footprint in the resulting design state.

**Rules without observed violations in measured history**

M5.W.1, M5.W.2, M5.W.3, M5.W.4, M5.S.1, M5.S.2, M5.S.3, M5.S.5, M5.AUX.2, M5.AUX.4, and V5.M5.EN.1 each appear in zero per-rule violation entries across all measured trials through iteration 4. No repair operations targeting these rules are recorded in the history.