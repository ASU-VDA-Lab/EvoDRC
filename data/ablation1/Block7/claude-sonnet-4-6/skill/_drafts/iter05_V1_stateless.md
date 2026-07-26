**General repair patterns**

The complete measured history for V1 contains 53 trials across 5 iterations, all with `conn_preserved: true` and `decision: "gated_in"`. Every accepted repair preserved inter-layer connectivity. The knowledge below describes what connectivity-preserving operations successfully advance the design state.

---

**Dominant operation: lateral instance moves**

The most frequent repair operation across all iterations is `move_instance` with delta_dbu in the X axis. A move magnitude of +36 dbu is the single most common value and appears in the majority of trials: trial:i01.ug.Block7_union_row15.05 (seven instances all +36x), trial:i01.ug.Block7_union_row18.08 (four instances all +36x), trial:i02.ug.Block7_union_row6.08 (five instances all +36x), trial:i02.ug.Block7_union_row14.01, trial:i03.ug.Block7_union_row24.05. Smaller X moves of +28 dbu appear in trial:i01.ug.Block7_union_row4.16 and trial:i01.ug.Block7_union_row6.18; +40 dbu in trial:i01.ug.Block7_union_row20.10. Negative X moves of -36 dbu are used when an instance is too close on the left side: trial:i01.ug.Block7_union_row11.01 (two instances -36x), trial:i01.ug.Block7_union_row16.06 (-36x for i0407, +40x for i0320 in the same trial).

Under V1.S.1, lateral separation between V1 instances on the same M2 track must reach 18 nm and between parallel tracks must reach 27 nm (not aligned) or 18 nm (aligned) via projection. Lateral instance moves in X directly increase that projected spacing and are the primary repair mechanism for V1.S.1 violations. The 36 dbu move appears most frequently across all five iterations, indicating it reliably closes the V1.S.1 gap in this design style. Use 36 dbu as the first-attempt X displacement for V1.S.1 violations; use 28 dbu when the measured gap deficit is smaller (trial:i01.ug.Block7_union_row4.16) or 40 dbu when a single neighboring instance requires more clearance (trial:i01.ug.Block7_union_row20.10).

Larger X displacements appear when a unit's local via cluster has several instances all too close together: +64 dbu in trial:i01.ug.Block7_union_row8.20, +72 dbu in trial:i01.ug.leaf_0002.23 and trial:i01.ug.leaf_0095.26, +92 dbu in trial:i02.ug.Block7_union_row19.04, +104 dbu in trial:i02.ug.leaf_0001.09, and +108 dbu in trial:i01.ug.Block7_union_row7.19 and trial:i04.ug.leaf_0001.01. Apply these larger magnitudes only when the measured inter-instance gap deficit warrants it; starting from 36 dbu and stepping up is the measured pattern.

---

**Polygon resize_end for enclosure and width correction**

`resize_end` operations on polygon ends (axis x or y, end high or low) appear in most multi-operation trials and correct V1.M1.EN.1, V1.M2.EN.2, and V1.M2.AUX.2 violations that are introduced or exposed when an instance moves away from its original metal coverage.

For V1.M2.EN.2 (M2 must enclose V1 on two opposite sides at 5 & 5 nm or 5 & 0 nm), resize_end on the high end of an M2 polygon restores enclosure after a positive-X instance move. trial:i01.ug.Block7_union_row3.15 pairs resize_end x high +49 on p3379 with a -36x instance move. trial:i01.ug.leaf_0008.24 uses resize_end x high +164 on p3771 alongside +108x and +40x instance moves. trial:i01.ug.Block7_union_row24.14 uses resize_end x high +36 on p3058 with a +36x instance move. Apply resize_end to the M2 end in the same direction as the instance move to restore the enclosure that the move has reduced.

For V1.M1.EN.1 (M1 must enclose V1 on two opposite sides at 5 & 2 nm), the same resize_end pattern applies to M1 polygon ends. trial:i04.ug.leaf_0001.01 combines resize_end x low -40 on p3297 and resize_end x high +108 on p3696 with instance moves of +108x and +60x, handling both enclosure edges on M1 and M2 in a single trial.

For V1.M2.AUX.2 (V1 must be exactly the same width as M2 perpendicular to M2 length), width-direction resize_end operations bring M2 edges flush with V1 edges when a Y-axis move has introduced a mismatch. trial:i03.ug.Block7_union_row13.00 uses resize_end y high -44 on p3538 after a -88y instance move; trial:i01.ug.leaf_0024.25 uses resize_end x high +36 and resize_end y high +44 on the same polygon p3538 alongside a +72x +44y instance move.

Within a trial, enclosure violations in both X and Y axes can be corrected simultaneously by combining axis-specific resize_end operations on the same polygon. trial:i01.ug.leaf_0024.25 demonstrates this with two resize_end calls on p3538 (x high +36, y high +44) combined with a compound instance move.

---

**Vertical (Y-axis) moves and resize corrections**

Y-axis instance moves address V1.S.1 violations between V1 instances on parallel M2 tracks (minimum 27 nm projected) and correct V1.M1.EN.1 and V1.M2.EN.2 enclosure in the Y direction. Observed effective Y-axis move magnitudes from accepted trials:

- 8 dbu: trial:i01.ug.Block7_union_row12.02 (instances i1356, i1358 moved +8y; paired with resize_end y high +8 and resize_end y low -8 on p3694)
- 16 dbu: trial:i02.ug.leaf_0023.16 (-16y for instances i0336, i0308; polygon p3516 also moved -16y)
- 44 dbu: trial:i01.ug.Block7_union_row22.12 (i0132 moved +36x -48y; other instances +36x), trial:i03.ug.leaf_0010.08 (i1062 +4x +44y)
- 48 dbu: trial:i03.ug.leaf_0020.09 (i0235 +48y), trial:i04.ug.leaf_0009.07 (i0235 -44y, adjacent to the +48y)
- 52 dbu: trial:i01.ug.Block7_union_row19.09 and trial:i03.ug.Block7_union_row19.03 (instances i0949, i0950 moved ±52y), trial:i02.ug.leaf_0032.17 (i0949, i0950 +52y), trial:i04.ug.leaf_0008.06 (same instances +52y)
- 57 dbu: trial:i02.ug.Block7_union_row17.02 (instances i0794, i0810 +57y; polygon p3631 +57y), trial:i04.ug.Block7_union_row13.00 (instances i0507, i0520 -57y; polygon p3526 -57y)
- 64 dbu: trial:i02.ug.leaf_0021.14 (-64y), trial:i04.ug.leaf_0005.03 (-64y), trial:i03.ug.Block7_union_row14.01 (+64y for i0920 with resize_end y high +8 on p3515), trial:i05.ug.leaf_0004.04 (+64y with resize_end y low -64 on p3576)
- 68 dbu: trial:i04.ug.leaf_0007.05 (+68y for instances i0794, i0810 and polygon p3631, with resize_end y high +68 on p2596)
- 72 dbu: trial:i03.ug.Block7_union_row23.04 (+72y for i0041)
- 88 dbu: trial:i03.ug.Block7_union_row13.00 (-88y for i0347, paired with resize_end y high -44 on p3538)

After any Y-axis instance move, apply resize_end on the Y end of the adjacent metal polygon to restore enclosure. trial:i01.ug.Block7_union_row14.04 illustrates this: instances i0894 and i0920 move +64y and resize_end y high +64 is applied to p3576. trial:i05.ug.leaf_0004.04 combines +64y instance move with resize_end y low -64 on p3576.

---

**Polygon move (op="move") for floating metal segments**

When a metal polygon's position must track an instance move but the polygon is not the instance itself, `op: "move"` on the polygon with matching delta keeps it aligned. Apply a matching polygon move whenever an instance move would leave an M2 or M3 segment stranded relative to V1, which would violate V1.AUX.1 or V1.M2.AUX.2.

trial:i02.ug.Block7_union_row17.02 moves instances i0794 and i0810 by +57y and also moves polygon p3631 by +57y. trial:i03.ug.Block7_union_row17.02 reverses all three by -57y. trial:i01.ug.Block7_union_row9.21 moves polygon p2720 by +56x alongside several instance moves in the same locus. trial:i04.ug.leaf_0007.05 moves instances i0794, i0810 by +68y, polygon p3631 by +68y, and applies resize_end y high +68 on p2596 — showing that a polygon move and a resize_end on a different polygon can be needed simultaneously to satisfy both position and enclosure constraints.

---

**Recurrent units and repair convergence**

Several unit_ids required repair in multiple consecutive iterations, indicating that a repair in one iteration exposed secondary violations. The iterations at which each unit was repaired:

- Block7_union_row13: trial:i01.ug.Block7_union_row13.03, trial:i02.ug.Block7_union_row13.00, trial:i03.ug.Block7_union_row13.00, trial:i04.ug.Block7_union_row13.00 (four consecutive iterations).
- Block7_union_row14: trial:i01.ug.Block7_union_row14.04, trial:i02.ug.Block7_union_row14.01, trial:i03.ug.Block7_union_row14.01.
- Block7_union_row17: trial:i02.ug.Block7_union_row17.02 (+57y), trial:i03.ug.Block7_union_row17.02 (-57y); iter 3 reverses iter 2's move direction.
- Block7_union_row19: trial:i01.ug.Block7_union_row19.09, trial:i02.ug.Block7_union_row19.04, trial:i03.ug.Block7_union_row19.03.
- Block7_union_row23: trial:i01.ug.Block7_union_row23.13, trial:i02.ug.Block7_union_row23.06, trial:i03.ug.Block7_union_row23.04.
- leaf_0001: trial:i01.ug.leaf_0001.22 (+4x), trial:i02.ug.leaf_0001.09 (+104x), trial:i04.ug.leaf_0001.01 (+108x +60x with resize_end).
- Locus [14112,17388,15696,18252]: repaired as leaf_0022 in iter 2 (trial:i02.ug.leaf_0022.15, -44y) and as leaf_0006 in iter 4 (trial:i04.ug.leaf_0006.04, -44y).
- leaf_0007 / leaf_0005: locus [2516,17120,10516,17316] repaired with -64y in trial:i02.ug.leaf_0021.14 and trial:i04.ug.leaf_0005.03.

When Block7_union_row17 recurred, iter 3 reversed the iter 2 move direction (trial:i02.ug.Block7_union_row17.02 vs trial:i03.ug.Block7_union_row17.02). Do not over-translate V1 instances in a single step when a unit has recurred across iterations; the reversal pattern in this unit shows that a +57y move overshot the target spacing window. For leaf_0001, the iter 1 move of +4x (trial:i01.ug.leaf_0001.22) was insufficient, iter 2 escalated to +104x (trial:i02.ug.leaf_0001.09), and iter 4 applied +108x with enclosure resize_end (trial:i04.ug.leaf_0001.01) — indicating that when a small initial move fails to clear a unit from the recurrence list, a substantially larger move is required.

---

**n_new_in_crop is not a rejection criterion**

Trials with `n_new_in_crop > 0` are accepted when `conn_preserved` is true. trial:i01.ug.Block7_union_row21.11 has n_new_in_crop = 9 with a single +4x instance move. trial:i02.ug.leaf_0041.19 has n_new_in_crop = 5 from a -44y instance move. trial:i03.ug.leaf_0020.09 has n_new_in_crop = 5 from a +48y instance move. trial:i01.ug.Block7_union_row13.03, trial:i01.ug.Block7_union_row22.12, and trial:i01.ug.leaf_0024.25 each have n_new_in_crop = 2. The gating criterion is connectivity preservation, not absence of in-crop violations. New in-crop violations introduced by a repair are addressed in subsequent iteration passes; prioritize moves that preserve connectivity over moves that avoid introducing secondary in-crop violations.

---

**V1.S.2, V1.S.3, V1.S.4 corner-spacing rules**

These euclidean corner-to-corner spacing rules (23 nm for V1.S.2, 30 nm for V1.S.3, 27 nm for V1.S.4) are driven by the v1_wec_mask and v1_nec_mask geometry derived from M2 end-cap presence. Repairs that adjust M2 end positions via resize_end change whether a V1 instance is classified as wec (with end-cap) or nec (without), and therefore which corner-spacing threshold applies. trial:i01.ug.leaf_0024.25 combines instance moves in both axes with resize_end operations on p3538 (x high +36, y high +44) and p2333 (y high +20), modifying both the via position and the mask boundary simultaneously. trial:i04.ug.leaf_0001.01 adjusts multiple polygon ends (resize_end x low -40 on p3297, x high +108 on p3696, y high -12 on p2719) alongside instance moves, resolving euclidean corner violations by shifting the mask geometry in addition to moving the via.

When a trial touches V1 and requires resize_end on M2 polygon ends, check whether the end-cap change alters the via's wec/nec classification and adjust the corner-spacing budget accordingly.

---

**NONORTHOGONAL constraint**

The NONORTHOGONAL rule prohibits any V1 edge at angles outside {0, 90, 180, 270} degrees. Every accepted repair in the history uses axis-aligned integer-dbu deltas only; no trial introduces diagonal polygon edges. Apply instance moves and resize_end exclusively along X or Y axes: trial:i01.ug.Block7_union_row15.05 (seven instance moves all purely in X), trial:i05.ug.leaf_0004.04 (instance move purely in Y, resize_end on Y axis only). Never use non-axis-aligned delta_dbu values for V1 or any layer touching V1.

---

**Operation sequencing within a trial**

Within a trial, instance moves and resize_end operations combine to handle multiple violation types simultaneously. trial:i01.ug.leaf_0024.25 (6 ops): instance move [+72x, +44y], resize_end x high +36 on p3538, resize_end y high +44 on p3538, resize_end y high +20 on p2333, instance move -16x on i1292, resize_end x low +52 on p3706. This resolves X-spacing, Y-spacing, and enclosure violations in a single trial. trial:i04.ug.leaf_0007.05 (4 ops): two instance moves +68y, polygon move +68y on p3631, resize_end y high +68 on p2596 — combining position correction with enclosure restoration in one step. When multiple violation types coexist at a locus, group their remedies into a single trial rather than staging them across iterations; the history shows this approach succeeds (conn_preserved=true in all such cases).

---

**Effective move magnitude reference (from measured trials)**

X-axis displacements accepted across the history:

- 4 dbu: trial:i01.ug.leaf_0001.22, trial:i01.ug.Block7_union_row21.11
- 28 dbu: trial:i01.ug.Block7_union_row4.16, trial:i01.ug.Block7_union_row6.18
- 36 dbu: trial:i01.ug.Block7_union_row15.05, trial:i01.ug.Block7_union_row18.08, trial:i02.ug.Block7_union_row6.08, trial:i02.ug.Block7_union_row14.01, trial:i03.ug.Block7_union_row24.05, and numerous others
- 37 dbu: trial:i01.ug.Block7_union_row19.09, trial:i03.ug.Block7_union_row19.03
- 40 dbu: trial:i01.ug.Block7_union_row16.06, trial:i01.ug.Block7_union_row20.10
- 44 dbu: trial:i01.ug.Block7_union_row14.04
- 56 dbu: trial:i01.ug.Block7_union_row9.21
- 60 dbu: trial:i04.ug.leaf_0001.01
- 64 dbu: trial:i01.ug.Block7_union_row8.20
- 72 dbu: trial:i01.ug.Block7_union_row23.13, trial:i01.ug.leaf_0002.23, trial:i01.ug.leaf_0095.26
- 92 dbu: trial:i02.ug.Block7_union_row19.04
- 104 dbu: trial:i02.ug.leaf_0001.09
- 108 dbu: trial:i01.ug.Block7_union_row7.19, trial:i01.ug.Block7_union_row9.21, trial:i04.ug.leaf_0001.01

Y-axis displacements accepted across the history:

- 8 dbu: trial:i01.ug.Block7_union_row12.02
- 12 dbu: trial:i01.ug.Block7_union_row14.04 (i0519, i0524 moved -12y)
- 16 dbu: trial:i02.ug.leaf_0023.16
- 44 dbu: trial:i01.ug.leaf_0024.25 (i0347), trial:i03.ug.leaf_0010.08
- 48 dbu: trial:i03.ug.leaf_0020.09
- 52 dbu: trial:i01.ug.Block7_union_row19.09, trial:i02.ug.leaf_0032.17, trial:i03.ug.Block7_union_row19.03, trial:i04.ug.leaf_0008.06
- 57 dbu: trial:i02.ug.Block7_union_row17.02, trial:i04.ug.Block7_union_row13.00
- 64 dbu: trial:i02.ug.leaf_0021.14, trial:i03.ug.Block7_union_row14.01, trial:i04.ug.leaf_0005.03, trial:i05.ug.leaf_0004.04
- 68 dbu: trial:i04.ug.leaf_0007.05
- 72 dbu: trial:i03.ug.Block7_union_row23.04
- 88 dbu: trial:i03.ug.Block7_union_row13.00