## Safe operation classes observed on M1

**Horizontal instance moves are the dominant safe repair action on M1.** Across all nine iter-1 trials that touched M1, every repair was accepted with zero new in-crop or out-of-crop M1 violations (trial:i01.ug.Block4_union_row1.00, trial:i01.ug.Block4_union_row10.01, trial:i01.ug.Block4_union_row2.02, trial:i01.ug.Block4_union_row5.04, trial:i01.ug.Block4_union_row6.05, trial:i01.ug.Block4_union_row7.06, trial:i01.ug.leaf_0008.08, trial:i01.ug.leaf_0020.09, trial:i01.ug.leaf_0021.10). These trials applied X-axis `move_instance` deltas ranging from -108 to +108 dbu, along with M1 polygon `move` and `resize_end` operations. None introduced M1.W.1, M1.S.1, M1.S.2, M1.S.3, M1.A.1, V0.M1.EN.1, V0.M1.AUX.3, or V1.M1.EN.1 violations.

**The 36 dbu step is the dominant safe X-axis quantum for M1-touching moves.** The value +36 dbu appears as the move delta in trial:i01.ug.Block4_union_row1.00, all three instances in trial:i01.ug.Block4_union_row6.05, trial:i01.ug.leaf_0008.08, trial:i01.ug.leaf_0020.09, the second op in trial:i02.ug.Block4_union_row1.00, and the first op in trial:i02.ug.Block4_union_row10.01. Multiples of 36 dbu (72, 108) were also applied without producing M1 violations in trial:i02.ug.Block4_union_row1.00 and trial:i02.ug.Block4_union_row7.03. Non-multiples such as 12, 16, 28, 37, 52, 92, and 96 dbu were also accepted cleanly in their respective trials; 36 dbu is the most frequently reused and confirmed safe step.

**Mixed-direction instance moves (nonzero X and Y simultaneously) passed without M1 violations in iter 1.** The delta [36, 44] applied to i0038 in trial:i01.ug.leaf_0021.10 introduced zero new M1 violations. This establishes that diagonal moves are not categorically unsafe, provided the displacement magnitudes stay within safe ranges.

**M1 polygon `move` and `resize_end` operations are compatible with DRC compliance when paired with instance moves.** In trial:i01.ug.Block4_union_row2.02 a single polygon move of p1548 by +16 dbu on axis-x alongside two instance moves produced zero new violations. In trial:i01.ug.Block4_union_row7.06 two polygon moves (-28 dbu each on p1596 and p1477) and a `resize_end` of +172 dbu on the high-x end of p1395 produced zero new violations. In trial:i01.ug.leaf_0008.08 a `resize_end` of +92 dbu on the high-x end of p1604 produced zero new violations. In trial:i02.ug.Block4_union_row10.01 a `resize_end` of +16 dbu on p1551 produced zero new violations, and in trial:i02.ug.Block4_union_row7.03 a `resize_end` of +52 dbu on p1595 produced zero new violations. In all cases the resize extended the high-x end of the polygon, consistent with extending M1 to improve enclosure or close a spacing gap.

---

## Y-axis moves generate M1 violations

**A pure Y-axis instance move of -36 dbu simultaneously triggered M1.A.1, M1.S.2, and V1.M1.EN.1 violations.** In trial:i02.ug.leaf_0013.06 the single op `move_instance i0038 [0, -36]` produced 9 new in-crop violations: M1.A.1 (×2), M1.S.2 (×1), M2.S.7 (×1), M4.W.5 (×1), and V1.M1.EN.1 (×4). The M1-specific failures are:

- **M1.A.1 (×2):** The -36 dbu Y displacement caused at least two M1 shapes to fall below the 504 nm-sq minimum area threshold. Area violations produced by a Y-move indicate that the displacement disturbed polygon merges or splits that reduced effective M1 area.
- **M1.S.2 (×1):** A tip-to-side spacing below 25 nm was created between an M1 tip edge (≤36 nm length) and an M1 side edge (>36 nm length). Y-axis instance displacement moved a tip edge into proximity with a side edge of a neighboring M1 polygon.
- **V1.M1.EN.1 (×4):** Four V1 vias lost compliant enclosure by M1. Rule V1.M1.EN.1 requires M1 to enclose V1 by at least 5 nm on two opposite sides (with 5 & 2 nm as the asymmetric minimum). A -36 dbu Y shift is sufficient to pull the enclosing M1 edge away from the via on one side below that threshold for multiple vias simultaneously.

Do not apply unconstrained Y-axis instance moves in regions where M1 enclosure of V1 is already near the minimum (trial:i02.ug.leaf_0013.06). When a Y-move is required, verify that all V1 vias within the affected locus retain at least 5 nm M1 enclosure on the pair of opposite edges after the displacement.

**A Y-axis move of -44 dbu did not cause M1 violations but introduced M2 and V1/M2 violations.** In trial:i02.ug.leaf_0008.04 the op `move_instance i0038 [0, -44]` produced M2.S.2 (×1) and V1.M2.EN.2 (×1) in-crop. No M1-layer violations appeared. This establishes that the sensitivity of M1 to Y-axis displacement is locus-dependent: the same instance moved in a different assembly context may or may not produce M1 violations.

---

## Assemble-conflict drops affect which M1 ops execute

**When two units claim a move on the same instance, one unit's op is dropped before assembly.** In both trial:i02.ug.leaf_0008.04 and trial:i02.ug.leaf_0013.06 the `move_instance i0038 [0,-44]` and `move_instance i0038 [0,-36]` were each dropped from one of the two competing units (leaf_0008 and leaf_0013, respectively) due to `reason: external_conflict_dropped`. The op that survives determines the final geometry. In trial:i02.ug.leaf_0013.06 the surviving [0,-36] move produced 9 new violations, while in trial:i02.ug.leaf_0008.04 the surviving [0,-44] move produced no M1 violations. The M1 outcome therefore depends on which unit wins the conflict resolution, not solely on the nominal delta magnitude.

When the same M1-touching instance is claimed by multiple units, the drop outcome is non-deterministic from any single unit's perspective. Design repair ops to be safe regardless of which competing move survives, or constrain M1-touching ops to instances that are not shared across unit boundaries.

---

## Gating behavior: conn_preserved overrides new M1 violations

**Trials that preserved connectivity were gated in even when new M1 violations appeared.** trial:i02.ug.leaf_0013.06 carried `conn_preserved: true` and `decision: gated_in` despite introducing M1.A.1 (×2), M1.S.2 (×1), and V1.M1.EN.1 (×4). The gating logic accepts repairs that preserve connectivity even when they introduce new in-crop violations, provided no new out-of-crop violations are created (`n_new_out_of_crop: 0`). M1 DRC violations alone do not cause rejection when connectivity is intact. Repairs that would push violations out of the crop boundary are rejected regardless of connectivity status; no trial in this history produced out-of-crop M1 violations.

---

## Rule-specific repair guidance grounded in measured records

**V1.M1.EN.1 — enclosure of V1 by M1 (5 & 2 nm minimum):** The 4 V1.M1.EN.1 violations produced by trial:i02.ug.leaf_0013.06 were all caused by a single Y-axis displacement. To repair or avoid V1.M1.EN.1, extend M1 in the direction of deficient enclosure. The `resize_end` pattern used successfully in trial:i01.ug.leaf_0008.08 (+92 dbu on high-x end of p1604), trial:i01.ug.Block4_union_row7.06 (+172 dbu on high-x end of p1395), trial:i02.ug.Block4_union_row10.01 (+16 dbu on high-x end of p1551), and trial:i02.ug.Block4_union_row7.03 (+52 dbu on high-x end of p1595) all extended enclosure without introducing M1 spacing or area violations. Apply `resize_end` on the deficient edge to restore the required 5 nm enclosure on the short side.

**M1.A.1 — minimum area 504 nm-sq:** Two M1.A.1 violations appeared after the Y-axis move in trial:i02.ug.leaf_0013.06. Area falls below the minimum when M1 shapes are displaced relative to their neighbors and previously merged areas split, or when a shape is resized to a smaller extent. No M1.A.1 violations appeared in any iter-1 trial or in the clean iter-2 trials (trial:i02.ug.Block4_union_row1.00, trial:i02.ug.Block4_union_row3.02, trial:i02.ug.Block4_union_row7.03, trial:i02.ug.Block4_union_row10.01). Avoid Y-axis displacements in loci where M1 shapes are near the minimum area, since the 504 nm-sq threshold (M1.A.1) can be breached by displacement-induced splits.

**M1.S.2 — tip-to-side spacing 25 nm:** One M1.S.2 violation appeared in trial:i02.ug.leaf_0013.06. The rule applies when a tip edge (≤36 nm) approaches a side edge (>36 nm) of a neighboring M1 polygon. All iter-1 X-axis moves avoided this rule. Y-axis moves that bring an M1 tip into proximity with a neighbor's side edge must account for the 25 nm minimum measured by `projection`. When resizing to close enclosure, use `resize_end` on the non-tip (side) end to avoid creating a new tip-to-side violation on the opposite face.

**V0.M1.EN.1 — enclosure of V0 by M1 (5 & 5 nm or 5 & 0 nm):** No V0.M1.EN.1 violations appeared in any trial in this history. The X-axis instance moves and `resize_end` operations applied across all trials were sufficient to avoid disturbing V0 enclosure. No specific guidance beyond what is already established by the successful enclosure-extending `resize_end` pattern (trial:i01.ug.Block4_union_row7.06, trial:i01.ug.leaf_0008.08) is grounded in measured data.

**V0.M1.AUX.3 — V0 width must equal M1 width in perpendicular direction:** No V0.M1.AUX.3 violations appeared in any trial. All polygon moves on M1 preserved the perpendicular width relationship, consistent with moves being axis-aligned and not altering the M1 edge that co-incides with V0 in the perpendicular direction.

**M1.W.1, M1.S.1, M1.S.3, M1.S.4, M1.S.5, M1.S.6, M1.R.0:** None of these rules produced violations in any trial in this history. No repair guidance specific to these rules is grounded in measured records.