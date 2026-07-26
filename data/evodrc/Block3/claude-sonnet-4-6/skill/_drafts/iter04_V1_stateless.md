## Successful repair patterns

### Move-and-resize pairing for x-axis shifts

When an instance carrying V1 and its associated M2 polygon is displaced in +x and the M2 polygon is separately addressable (i.e., not integral to the instance), the M2 polygon's high-x edge must be extended by a delta strictly larger than the instance translation delta. The excess maintains the M2 overhang on the far side of V1, keeping V1.M2.EN.2 enclosure and the V1.M2.AUX.2 coincident-edge constraint satisfied. This pattern appeared in every positive-x move trial that included a resize and produced zero violations:

- trial:i01.ug.Block3_union_row1.00: three instances moved +136 dbu; each M2 polygon resized high-x +192 dbu (net additional extension 56 dbu per polygon); 0 new violations.
- trial:i01.ug.Block3_union_row8.03: instances moved +108/+72/+72/+72 dbu; M2 polygons resized high-x +164/+128/+128/+92 dbu respectively; 0 new violations.
- trial:i01.ug.leaf_0007.05: two instances moved +36 dbu; both M2 polygons resized high-x +56 dbu; 0 new violations.
- trial:i01.ug.leaf_0012.08: instance moved +72 dbu; M2 polygon resized high-x +108 dbu; 0 new violations.
- trial:i02.ug.leaf_0002.01: instance moved +104 dbu; M2 polygon resized high-x +128 dbu; 0 new violations.

In every case the resize delta exceeded the move delta. Apply high-x resize whenever a separately-addressable M2 polygon must follow a +x instance move.

### Pure instance moves when M2 is integral to the instance

When V1 and its covering M2 polygon are part of the same instance, a rigid translation preserves all enclosure and width relationships without any explicit polygon resize. Pure move-only operations produced 0 new violations in:

- trial:i01.ug.Block3_union_row2.01: two instances moved +36 dbu.
- trial:i01.ug.leaf_0006.04: two instances moved +36 dbu.
- trial:i01.ug.leaf_0009.07: one instance moved +36 dbu.
- trial:i01.ug.leaf_0013.09: one instance moved −36 dbu.
- trial:i02.ug.leaf_0001.00: one instance moved −36 dbu.

Negative-x (leftward) moves are safe under this condition, as confirmed by trial:i01.ug.leaf_0013.09 and trial:i02.ug.leaf_0001.00. Do not apply resize_end to such instances; the move alone is sufficient and correct.

### Mixed loci: some instances need resize, others do not

trial:i01.ug.Block3_union_row5.02 moved three instances by +36 dbu and included a single high-x resize (+36 dbu on p1265) for one of them (i0124), while i0011 and i0033 received only move_instance; 0 new violations resulted. This confirms that within a single locus, whether a resize is needed depends on each instance's M2 geometry, not a global property of the locus.

### Y-axis M2 extension for perpendicular enclosure

trial:i01.ug.leaf_0008.06 applied resize_end y high +20 dbu on M2 polygon p1159 alongside a small +x instance move ([4,0] dbu on i0239), and separately moved i0047 +136 dbu with M2 polygon p1261 resized high-x +92 dbu; 0 new violations. The y-axis resize maintains the V1.M2.EN.2 enclosure margin in the direction perpendicular to the primary translation when a small x-shift risks eroding it. Apply y-axis M2 resizes when perpendicular enclosure margins are tight.

---

## Violation-producing patterns

### Isolated leftward move of an instance with a separately-addressable M2 polygon

trial:i03.ug.leaf_0003.02 moved instance i0099 by −36 dbu with no M2 polygon resize; 10 new in-crop violations were introduced across the locus. The leftward displacement of V1 without a corresponding M2 adjustment violates enclosure and coincident-edge constraints (V1.M2.EN.2, V1.M2.AUX.2) for the affected V1 shapes. Do not apply move_instance alone in −x on an instance whose M2 polygon is separately addressable.

### Low-end M2 contraction combined with leftward move does not resolve violations

trial:i04.ug.leaf_0001.00 moved i0099 −76 dbu and resized the low-x end of p1207 by +132 dbu (contracting the polygon from its left edge). Despite the added resize operation, 10 new in-crop violations persisted — the same count as in trial:i03.ug.leaf_0003.02. Contracting the low-x edge of M2 while shifting V1 leftward does not restore the enclosure relationship on the high-x side or correct the width mismatch flagged by V1.M2.AUX.2. Avoid resize_end x low as the sole M2 adjustment when moving V1 in −x relative to M2.

---

## Gating behavior

All 14 trials across iterations 1–4 received decision "gated_in." When conn_preserved = true and n_new_in_crop = 0, the fix is accepted cleanly (all iteration 1 and iteration 2 trials). When conn_preserved = true and n_new_in_crop > 0 — trial:i03.ug.leaf_0003.02 (10 violations) and trial:i04.ug.leaf_0001.00 (10 violations) — the fix is still gated_in under the unit_gate channel: connectivity preservation takes priority over new DRC counts. No trial in this history was rejected. The 10 in-crop violations introduced in iteration 3 (trial:i03.ug.leaf_0003.02) persisted into iteration 4 (trial:i04.ug.leaf_0001.00) without being resolved; they are outstanding DRC debt carried forward by the gating policy.

---

## Summary of repair principles

**Use resize_end x high with delta exceeding the move delta** whenever a separately-addressable M2 polygon must follow a +x instance move. Confirmed by trial:i01.ug.Block3_union_row1.00, trial:i01.ug.Block3_union_row8.03, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0012.08, and trial:i02.ug.leaf_0002.01.

**Do not apply resize_end when M2 is integral to the instance.** Pure move_instance operations on such instances produce 0 violations in both +x and −x directions. Confirmed by trial:i01.ug.Block3_union_row2.01, trial:i01.ug.leaf_0006.04, trial:i01.ug.leaf_0009.07, trial:i01.ug.leaf_0013.09, and trial:i02.ug.leaf_0001.00.

**Do not move a separately-addressable V1-bearing instance in −x without a corrective M2 polygon adjustment.** trial:i03.ug.leaf_0003.02 establishes that a −36 dbu move of i0099 alone produces 10 new violations.

**Do not use resize_end x low as the corrective adjustment for a −x move.** trial:i04.ug.leaf_0001.00 shows that moving i0099 −76 dbu while contracting p1207's low-x end by 132 dbu leaves 10 violations unresolved.

**Apply resize_end y high when a small x-shift reduces perpendicular M2 enclosure.** trial:i01.ug.leaf_0008.06 confirms a y-axis extension on M2 is a valid and effective tool in this situation.