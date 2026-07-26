## M4 Width Rules

**Vertical width (M4.W.1 / M4.W.2 / M4.W.3 / M4.W.4):** The minimum vertical width is 24 nm and the maximum is 480 nm. M4.W.3 forbids any vertical width that is an exact even integer multiple of 24 nm: 48, 96, 144, 192, 240, 288, 336, 384, 432, and 480 nm. M4.W.4 additionally forbids 72, 168, 264, 360, and 456 nm (widths spanning an even number of minimum routing tracks). No M4.W.3 or M4.W.4 violations were generated in the observed history; operations touching M4 in the y-direction either preserved existing widths or, as in the +44 dbu resize of p1154 in trial:i02.ug.leaf_0002.01, produced a final width outside both forbidden sets.

**Horizontal width (M4.W.5):** The minimum horizontal width is 44 nm. X-axis instance moves of +32 dbu and -16 dbu applied differentially across large groups of instances in trial:i02.ug.leaf_0003.02 introduced 2 M4.W.5 violations; the same differential move pattern in trial:i02.ug.leaf_0004.03 introduced 3 M4.W.5 violations. Check M4 polygon horizontal extents after applying differential instance x-moves (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03).

## M4 Spacing Rules

**Vertical spacing (M4.S.1):** Minimum vertical spacing between M4 polygon horizontal edges is 24 nm, evaluated with both projection and euclidean metrics. The 24 nm minimum equals the M4 horizontal-edge grid pitch (M4.AUX.1), so y-moves that land on the 24 nm grid and do not close a vertical gap below 24 nm preserve M4.S.1 on initially compliant geometries.

**Horizontal spacing (M4.S.2):** Minimum horizontal spacing between M4 vertical edges is 40 nm (euclidean). No M4.S.2 violations appeared in the full history despite repeated x-axis instance moves of +32 dbu and -16 dbu across multiple trials (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03, trial:i04.ug.leaf_0003.02), indicating those displacement magnitudes did not close horizontal clearances below 40 nm in the affected cells.

**Tip-to-tip spacing (M4.S.3 / M4.S.4):** Minimum tip-to-tip spacing between M4 polygons on adjacent tracks is 40 nm, regardless of whether the polygons share a parallel run. No M4.S.3 or M4.S.4 violations were recorded across the observed history.

**Parallel run length (M4.S.5):** Minimum parallel run length between adjacent M4 polygons on adjacent tracks is 44 nm. Trial:i02.ug.leaf_0003.02 introduced 1 M4.S.5 violation; that trial applied polygon x-moves of +32 dbu to p1143 and -16 dbu to p1142 in conjunction with bulk instance moves. When x-moves alter the relative overlap of adjacent M4 runs, any resulting shared run length below 44 nm violates M4.S.5 (trial:i02.ug.leaf_0003.02).

## Routing Track Alignment (AUX Rules)

**M4.AUX.1 (horizontal edge grid):** All M4 horizontal edges must fall on a 24 nm y-grid. The y-axis resize of polygon p1154 by +44 dbu (low end) in trial:i02.ug.leaf_0002.01 produced no new violations: the locus bottom was at 14548 dbu, and 14548 + 44 = 14592, which is exactly divisible by 24 (14592 / 24 = 608). The target edge coordinate after any y-resize must satisfy dest_dbu mod 24 == 0 (trial:i02.ug.leaf_0002.01).

**M4.AUX.2 (minimum-width track centerlines):** Minimum-width M4 segments — those whose y-extent is eliminated by a 13 nm bilateral y-shrink — must have centerlines satisfying (centerline_dbu - 48) mod 192 == 0. Allowed centerline positions are 48, 240, 432, 624 dbu, etc., spaced 192 dbu apart. Moving a minimum-width track by exactly 192 dbu maps a compliant centerline to the next compliant position. Y-axis instance moves of ±48 dbu and ±96 dbu in trial:i04.ug.leaf_0002.01 touched M4 and introduced 20 new in-crop violations despite connectivity being preserved; no per-rule breakdown was recorded in that trial, so the specific rules triggered are not identified from that record alone.

**M4.AUX.3 (no bends):** M4 polygons must not contain convex corners. Every M4 operation in the observed history was either an end-resize or a whole-polygon translation; no M4.AUX.3 violations were generated. Avoid any op that introduces a non-straight M4 polygon (no trial in the history produced a bend without it being rejected).

**M4.AUX.4 (wide polygon outer edge restriction):** Outer horizontal edges of wide M4 polygons (those surviving a 13 nm bilateral y-shrink) must not coincide with minimum-width routing track edges. No M4.AUX.4 violations appeared in the observed history.

## Via Enclosure

**V4.M4.EN.1 (V4 enclosure by M4):** V4 vias must be enclosed by M4 on at least two opposite sides by a minimum of 11 nm. In trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, shrinking the M5 metal shape of cell VIA_VIA45_1_2_58_58 by -88 dbu in y (touching M4 and V4) reduced total DRC violations by 52. Via cell y-shrinkage resolves over-extension at M4/V4 interfaces without expanding the enclosing M4 polygon (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01).

**V3.M4.EN.2 / V3.M4.AUX.2:** V3 must be enclosed by M4 by at least 11 nm on two opposite sides, and V3 width must match M4 width perpendicular to the M4 run direction. Trials applying bulk instance moves that touched both V3 and M4 (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03) introduced no V3.M4.EN.2 or V3.M4.AUX.2 violations, confirming those move magnitudes did not disturb V3–M4 enclosure.

## Connectivity and Operation Gating

**Retracting M4 polygon ends breaks connectivity.** Trial:i01.ug.leaf_0034.12 was rejected (decision: gated_out) with 89 new violations because connectivity was broken. That trial included a -4 dbu retraction of the right edge of M4 polygon p1214 combined with other operations on M1–V2. The connection was severed by the retraction; avoid retracting M4 ends in directions that reduce overlap with a V3 or V4 landing pad (trial:i01.ug.leaf_0034.12).

**Extending M4 endpoints outward is safe when the extended segment clears adjacent polygons.** Right-end extensions of +456 dbu on p1211 and +240 dbu on p1216 in trial:i01.ug.Block1_union_row12.02 produced zero new violations and preserved connectivity. Positive x-end extensions on isolated M4 segments do not inherently introduce width or spacing violations (trial:i01.ug.Block1_union_row12.02).

**Bulk differential instance x-moves introduce M4.W.5 and M4.S.5 violations.** Trial:i02.ug.leaf_0003.02 applied +32 dbu and -16 dbu x-moves to dozens of instances, resulting in 2 M4.W.5 violations and 1 M4.S.5 violation; trial:i02.ug.leaf_0004.03 applied the same pattern and introduced 3 M4.W.5 violations. Both trials were accepted (gated_in, conn_preserved) because violations were in-crop and connectivity held. Identify affected M4 horizontal widths and adjacent-track run lengths before committing differential instance x-moves (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03).

**Y-axis instance moves touching M4 can introduce in-crop violations even when connectivity is preserved.** Trial:i04.ug.leaf_0002.01 applied ±48 and ±96 dbu y-moves to 16 instances (touching M3, M4, M5, V3, V4) and introduced 20 new in-crop violations with connectivity intact. No per-rule breakdown is available from that record.

**Single-instance moves on M4/V4-touching cells at iter 3 and iter 4 were violation-free.** Trial:i03.ug.leaf_0001.00 (resize_end -32 dbu x-high on p1187, plus move_instance i0181 +76 dbu x) and trial:i04.ug.leaf_0001.00 (move_instance i0181 -76 dbu x) each produced zero new violations with connectivity preserved. Small, targeted single-instance displacements on M4/V4 cells carry lower violation risk than bulk multi-instance moves.