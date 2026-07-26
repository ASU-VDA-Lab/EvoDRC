**Move Direction and V1 Violation Generation**

All pure X-axis instance moves in this layer's history produced zero new V1-rule violations. This holds for single-instance moves (trial:i01.ug.Block4_union_row1.00, delta [36,0]; trial:i01.ug.leaf_0020.09, delta [36,0]; trial:i02.ug.Block4_union_row3.02, delta [-28,0]; trial:i03.ug.leaf_0001.01, delta [36,0]), for multi-instance moves with uniform direction (trial:i01.ug.Block4_union_row6.05, three instances each [36,0]; trial:i03.ug.Block4_union_row7.00, two instances each [36,0]), and for multi-instance moves with mixed positive and negative X displacements within the same trial (trial:i01.ug.Block4_union_row5.04, instances moved [37,0], [37,0], [-36,0], [37,0]).

Pure Y-axis instance moves introduced V1 violations in all three cases recorded. Trial:i02.ug.leaf_0008.04 moved i0038 by [0,-44] and introduced one new V1.M2.EN.2 violation (n_new_in_crop:2 total). Trial:i02.ug.leaf_0013.06 moved i0038 by [0,-36] and introduced four new V1.M1.EN.1 violations (n_new_in_crop:9 total). Trial:i03.ug.leaf_0004.02 moved i0038 by [0,-64] and introduced two new in-crop violations. Do not apply pure Y-direction instance moves when V1 is in the touched layer set: trial:i02.ug.leaf_0008.04, trial:i02.ug.leaf_0013.06, and trial:i03.ug.leaf_0004.02 each produced V1 enclosure failures from Y-only deltas on instance i0038.

One diagonal move ([36,44] on i0038, trial:i01.ug.leaf_0021.10) produced zero new V1 violations in iter:1 design state d279330089d1cc7ae7faf9a64991c183a651656d2a44f921bf86d5225ab3dacd. This trial differs from the pure-Y trials in both the presence of an X component and the design state; the pure-Y trials operated on design states 6eb8acc6... (iter:2) and da6d950e... (iter:3). No generalization across the Y-component can be drawn from this single diagonal datapoint alone.

**V1.M1.EN.1: M1 Enclosure Sensitivity to Y Displacement**

V1.M1.EN.1 requires M1 to enclose V1 on two opposite sides with at least 5 nm and 2 nm (projection metric). Moving instance i0038 by [0,-36] introduced four simultaneous V1.M1.EN.1 violations in trial:i02.ug.leaf_0013.06. No X-direction move in the history triggered V1.M1.EN.1. Avoid Y-direction instance moves when M1 enclosure margins are near the 5 nm or 2 nm thresholds: trial:i02.ug.leaf_0013.06 shows that a 36 dbu Y displacement alone is sufficient to produce four concurrent M1-enclosure failures on V1.

**V1.M2.EN.2: M2 Enclosure Sensitivity to Y Displacement**

V1.M2.EN.2 requires M2 to enclose V1 on two opposite sides by 5&5 nm or 5&0 nm (projection metric). Moving i0038 by [0,-44] introduced one V1.M2.EN.2 violation in trial:i02.ug.leaf_0008.04. No X-direction move in the history triggered V1.M2.EN.2. Avoid Y-direction moves that shift V1 out of M2 end-cap coverage: trial:i02.ug.leaf_0008.04 demonstrates that a 44 dbu Y shift is sufficient to break M2 enclosure compliance on V1.

**resize_end Operations Do Not Introduce V1 Violations**

Resizing the high X end of M2 polygons alongside X-direction instance moves does not introduce V1 violations. Trial:i01.ug.leaf_0008.08 resized p1604 by +92 dbu (high X end) while moving i0274 by [36,0]: n_new_in_crop:0. Trial:i02.ug.Block4_union_row10.01 resized p1551 by +16 dbu (high X end) alongside multiple instance moves: n_new_in_crop:0. Trial:i02.ug.Block4_union_row7.03 resized p1595 by +52 dbu (high X end) with a [108,0] instance move: n_new_in_crop:0. Trial:i01.ug.Block4_union_row7.06 resized p1395 by +172 dbu (high X end) alongside [-28,0] moves of two instances and two polygon X-shifts: n_new_in_crop:0 for all V1 rules. Use resize_end on the high X end as a complement to X-direction instance moves: every recorded case of this pattern produced zero V1 violations (trial:i01.ug.leaf_0008.08, trial:i02.ug.Block4_union_row10.01, trial:i02.ug.Block4_union_row7.03, trial:i01.ug.Block4_union_row7.06).

**Gating Behavior: New In-Crop V1 Violations Do Not Block Acceptance**

The gating decision is gated_in whenever conn_preserved=true and n_new_out_of_crop=0, regardless of n_new_in_crop count. Trial:i02.ug.leaf_0008.04 was gated_in with n_new_in_crop:2 (including V1.M2.EN.2:1). Trial:i02.ug.leaf_0013.06 was gated_in with n_new_in_crop:9 (including V1.M1.EN.1:4). Trial:i03.ug.leaf_0004.02 was gated_in with n_new_in_crop:2. All remaining trials were gated_in with n_new_in_crop:0. No trial in this history has n_new_out_of_crop greater than 0.

**Assemble Drops from Inter-Leaf Conflicts on Instance i0038**

When two leaves claim conflicting ops on the same instance, the harness drops one (external_conflict_dropped) and executes the other. In iter:2, trial:i02.ug.leaf_0008.04 and trial:i02.ug.leaf_0013.06 both targeted i0038 with Y-direction moves; each trial dropped the other leaf's op. The surviving op in each case was a pure Y-direction move ([0,-44] and [0,-36] respectively), both of which introduced V1 enclosure violations. The assemble_drop mechanism does not affect whether V1 rules are triggered; violation generation is determined solely by the geometry of the executed ops.

**Common X-Move Magnitudes**

The 36 dbu increment appears in more X-direction instance moves than any other step size in this layer's history: trial:i01.ug.Block4_union_row1.00, trial:i01.ug.Block4_union_row6.05 (×3), trial:i01.ug.leaf_0020.09, trial:i01.ug.leaf_0008.08, trial:i02.ug.Block4_union_row1.00 (one of two ops), trial:i03.ug.Block4_union_row7.00 (×2), trial:i03.ug.leaf_0001.01. Every 36 dbu X-direction instance move in the history recorded zero new V1 violations. Multiples of 36 dbu (72 in trial:i02.ug.Block4_union_row1.00; 108 in trial:i01.ug.Block4_union_row2.02 and trial:i02.ug.Block4_union_row7.03) also produced zero V1 violations. Non-multiples (12, 28, 37, 52, 92, 172 dbu) applied in X-only contexts likewise produced zero V1 violations in their respective trials.