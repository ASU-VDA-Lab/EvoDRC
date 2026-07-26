## Operation Patterns

**Move-instance is the primary repair operation for V1-touching units.** Across all accepted trials, `move_instance` along the x-axis dominates the op lists. Displacements of +36 dbu were used in the largest number of units and were universally accepted (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row10.01, trial:i01.ug.Block1_union_row3.03, trial:i01.ug.Block1_union_row4.04, trial:i01.ug.Block1_union_row5.05, trial:i01.ug.Block1_union_row9.08, trial:i01.ug.leaf_0004.09, trial:i04.ug.leaf_0001.00, trial:i05.ug.leaf_0005.04). Displacements of +72 dbu also succeeded in several contexts (trial:i03.ug.Block1_union_row3.00, trial:i03.ug.leaf_0004.01, trial:i03.ug.leaf_0005.02). Displacements of +108 dbu succeeded in trial:i01.ug.Block1_union_row1.00 and trial:i01.ug.Block1_union_row8.07. Negative x-moves of -32 and -36 dbu were also accepted (trial:i01.ug.Block1_union_row6.06, trial:i01.ug.Block1_union_row8.07, trial:i01.ug.Block1_union_row5.05).

**A 72 dbu x-move of a previously-moved instance broke connectivity and was rejected.** In trial:i04.ug.leaf_0001.00 (gated_in), instance i0453 was shifted +36 dbu. In the following iteration, trial:i05.ug.leaf_0001.00 (gated_out, conn_broken) attempted a further +72 dbu move of the same instance. The rejection was due to `conn_broken`, not DRC. Do not apply large x-displacements to instances that have already been repositioned in prior iterations without verifying that the cumulative shift stays within connectivity reach of their nets.

## M2 Enclosure Co-Repairs (V1.M2.EN.2 / V1.M2.AUX.2)

**When a V1-carrying instance moves along x, extend the M2 polygon end at the high or low x-edge to maintain enclosure.** This pattern is observed in trial:i01.ug.Block1_union_row1.00 (move +36 dbu then resize_end x high +128 dbu on p1320 and +92 dbu on p1321), trial:i01.ug.Block1_union_row3.03 (move +36 dbu then resize_end x high +92 dbu on p1370), trial:i01.ug.Block1_union_row4.04 (move +36 dbu then resize_end x high +52 dbu on p1238), trial:i01.ug.Block1_union_row5.05 (resize_end x high +36 dbu on p1297 and x low +36 dbu on p1301), trial:i01.ug.leaf_0020.10 (move -36 dbu then resize_end x low +36 dbu on p1253), trial:i03.ug.leaf_0004.01 (move +72 dbu then resize_end x high +72 dbu on p1295). V1.M2.EN.2 requires M2 to enclose V1 by ≥5 nm on two opposite sides (either 5&5 nm or 5&0 nm with a flush edge). V1.M2.AUX.2 requires the V1 width to equal the M2 width in the direction perpendicular to M2 length. Pairing a resize_end on the M2 polygon with an instance move in the same direction and of comparable magnitude satisfies both constraints in all accepted trials above.

**The resize delta need not equal the instance move delta.** In trial:i01.ug.Block1_union_row1.00 the instance moved +36 dbu but the M2 end extended +128 dbu on p1320. In trial:i01.ug.Block1_union_row3.03 the instance moved +36 dbu but the M2 end extended +92 dbu on p1370. The resize delta is set to close the enclosure gap, which depends on the existing overhang before the move, not solely on the move magnitude.

## V1.M1.EN.1 Violations from Bulk Moves

**Bulk instance moves in large loci introduce new V1.M1.EN.1 violations.** In trial:i05.ug.leaf_0005.04, four instance moves of +36 dbu each across a wide locus (1728,3148 to 14256,14132) produced 15 new V1.M1.EN.1 violations (among 24 total new in-crop violations). V1.M1.EN.1 requires M1 to enclose V1 by ≥5 nm on one projection axis and ≥2 nm on the other. Moving a V1 instance toward or past the M1 boundary on either axis degrades this enclosure. When a move batch spans the full block, M1 polygons that were previously providing adequate enclosure may become insufficient on the direction of motion. The trial was gated_in because `conn_preserved`; the 15 new V1.M1.EN.1 violations were accepted as in-crop new violations without triggering rejection.

**To avoid generating V1.M1.EN.1 violations, pair instance moves with M1 resizes** that extend the M1 boundary in the direction of motion, or confirm the pre-move M1 enclosure exceeds the move delta by ≥5 nm (high side) or ≥2 nm (low side). The accepted trials that produced zero new V1.M1.EN.1 violations (e.g., trial:i01.ug.Block1_union_row3.03, trial:i01.ug.Block1_union_row4.04, trial:i03.ug.leaf_0004.01) all used small loci with limited instance counts, reducing the probability of marginal enclosure conditions.

## Via Replacement as an Alternative to Instance Move

**Deleting an instance and inserting a VIA_VIA12 cell at a new coordinate resolves V1-region conflicts while preserving connectivity.** In trial:i02.ug.leaf_0004.02, instance i0300 was deleted and a VIA_VIA12 was placed at origin [5904,6300] dbu. The trial was gated_in with zero new in-crop and zero new out-of-crop violations. This establishes that for cases where a move would produce spacing or enclosure violations, replacing the via instance with a freshly placed VIA_VIA12 cell at the correct location is a valid clean-slate alternative.

## Co-Layer Constraint: V1 Always Co-Modifies M1 and M2

**Every V1 repair touches M1 and M2 as co-modified layers.** All 20 trials in the history list `["M1","M2","V1"]` in `touched_layers` (trial:i05.ug.leaf_0005.04 additionally includes M6). V1.AUX.1 requires V1 to lie inside M1 ∩ M2; any geometric change to V1 requires that both M1 and M2 continue to cover it. Plan all V1 repair ops as three-layer edits from the outset; single-layer V1 moves without M1/M2 adjustment are not represented anywhere in the accepted history.

## Nonorthogonal Geometry

**All V1 shapes must have exclusively 0° and 90° edges.** The GEOMETRY.NONORTHOGONAL rule fires on any edge whose angle falls in (1°..89°), (91°..179°), (-179°..-91°), or (-89°..-1°). No trial in this history introduced nonorthogonal V1 edges; all `resize_end` and `resize` operations used axis-aligned endpoints. Every op generating or reshaping a V1 polygon must produce a rectilinear result.

## Spacing and Width Rules — Operative Thresholds

**V1.W.1 sets a 18 nm minimum width along the M2 length direction.** No trial in this history recorded a V1.W.1 violation, and all accepted resize operations preserved the existing V1 width. Do not reduce a V1 polygon's extent along M2 below 18 nm.

**V1.S.1 minimum spacing is 18 nm (same track, aligned) or 27 nm (parallel tracks, not aligned).** The rule uses a masked representation that extends the V1 boundary by the M2 end-cap geometry before checking projection spacing. All accepted trials maintained the V1 instance positions relative to neighbors within the track constraints; no V1.S.1 violation appears in the per_rule breakdown of any trial. When shifting an instance toward a neighbor on the same M2 track, confirm the remaining gap in the masked representation stays ≥18 nm.

**V1.S.2 (≥23 nm Euclidean corner-to-corner for two end-capped instances) and V1.S.3 (≥30 nm Euclidean for two non-end-capped instances) and V1.S.4 (≥27 nm Euclidean mixed) did not fire** in any trial in this history. These corner rules engage only when instances are diagonally adjacent; the x-only moves observed here do not create such geometry within a given row.

## Decision Gate Behavior

**Connectivity preservation is the primary gate; DRC violation count alone does not block acceptance.** trial:i05.ug.leaf_0005.04 was gated_in despite 24 new in-crop violations including 15 V1.M1.EN.1 violations because `conn_preserved` was true. trial:i04.ug.leaf_0004.03 was gated_in despite 80 new in-crop violations for the same reason. Conversely, trial:i05.ug.leaf_0001.00 was gated_out with zero new DRC violations because `conn_broken` was true. Repair sequences that break a net connection are rejected regardless of DRC improvement; repair sequences that generate new violations are accepted if connectivity holds.