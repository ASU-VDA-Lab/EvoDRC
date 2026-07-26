**V4.M5.AUX.2 — Width-match violations: resize M5 in the perpendicular axis**

Rule V4.M5.AUX.2 requires V4 to be exactly the same width as M5 along the direction perpendicular to M5's length. When this rule fires, the effective repair is to resize the M5 shape (not the V4 shape) along the mismatched axis until the edges are coincident. In trial:i01.cu.def:VIA_VIA45_1_2_58_58.00, a `resize_via_shape` op on M5 with `axis=y`, `delta_dbu=-88` in cell `VIA_VIA45_1_2_58_58` eliminated the mismatch and reduced total DRC count by 56 errors across two windows (leaf_0019: -30, leaf_0020: -26). The op group label `v4_m5_aux2_fix` confirms the direct association. Connectivity was preserved. Apply axis-aligned shrink or grow to M5 to close the edge gap; do not resize V4 itself for this rule class.

**V4.AUX.1 and enclosure rules — M5 resize side-effects on M4 and V4 checks**

The resize operation in trial:i01.cu.cu.def:VIA_VIA45_1_2_58_58.00 listed touched layers as M4, M5, and V4. This means that resizing M5 to fix V4.M5.AUX.2 simultaneously perturbs the geometry relevant to V4.M4.EN.1 (M4 must enclose V4 by ≥11 nm on two opposite sides) and V4.AUX.1 (V4 must be inside both M4 and M5). After any M5 resize targeting V4.M5.AUX.2, re-check V4.AUX.1 and V4.M4.EN.1 in the same locus; the trial shows all three layers move together in the via cell context.

**Move-instance repair at the unit level — V4 violations increase in crop when instances shift**

In trial:i04.ug.leaf_0003.01, 24 `move_instance` operations across 12 instance pairs (touching M3, M4, M5, V3, V4) were gated in solely on `conn_preserved=true`, even though 68 new DRC violations entered the crop window (`n_new_in_crop=68`, `n_new_out_of_crop=0`). This shows that bulk instance moves in a unit can introduce V4 spacing, enclosure, or AUX violations at scale. The gate criterion was connectivity preservation, not DRC cleanliness. Do not treat a gated-in move-instance trial as DRC-clean for V4; the 68 new in-crop violations require subsequent targeted repair passes.

**Spacing rules V4.S.1, V4.S.2, V4.S.3 — projection vs. euclidean checks**

Rules V4.S.1 and V4.S.2 use projection-based spacing (33 nm), while V4.S.3 uses Euclidean spacing (33 nm) for corner-to-corner gaps. The instance moves in trial:i04.ug.leaf_0003.01 repositioned pairs of instances to shared grid coordinates (e.g., multiple pairs to x=2896,y=3216 and x=13696,y=3216), which can place V4 shapes in proximity. When two instances land at the same origin, their V4 shapes may violate S.1, S.2, or S.3 depending on net membership and shape geometry. After any batch move, audit spacing in both projection and Euclidean modes; the projection check alone will not catch diagonal near-misses governed by V4.S.3.

**V4.W.1 — Minimum width 24 nm; no width violations recorded but enclosure constrains minimum**

No V4.W.1 violations appear in the recorded trials, but the minimum width of 24 nm is a hard floor. Because V4.M5.AUX.2 ties V4 width to M5 width in the perpendicular direction, shrinking M5 (as in trial:i01.cu.def:VIA_VIA45_1_2_58_58.00 with delta_dbu=-88 in y) must not reduce the M5 width below 24 nm in the via dimension, or a downstream V4.W.1 violation will be created. Verify post-resize M5 width in the via cell before committing.

**V4.M5.EN.2 — M5 enclosure ≥11 nm on two opposite sides**

Rule V4.M5.EN.2 requires M5 to enclose V4 by at least 11 nm on two opposite sides. The `resize_via_shape` fix in trial:i01.cu.def:VIA_VIA45_1_2_58_58.00 operated on M5 with a negative delta in y, reducing M5 extent in that axis. This is consistent with an oversize M5 that failed V4.M5.AUX.2 (M5 too wide relative to V4), not an undersize. When the repair direction is a shrink of M5, confirm that the post-shrink M5 still satisfies EN.2 (11 nm enclosure on two opposite sides); a large negative delta can flip from AUX.2 violation to EN.2 violation.

**Repair channel and decision patterns**

The `cu_pool` channel (trial:i01.cu.def:VIA_VIA45_1_2_58_58.00) operates at the individual via cell level and applies single targeted ops with `decision=applied`. The `unit_gate` channel (trial:i04.ug.leaf_0003.01) operates at the leaf-unit level with bulk move ops and uses `decision=gated_in` when connectivity is preserved, regardless of new in-crop violations. V4 violations surfaced by unit-gate trials are not resolved by the gate pass itself; they require follow-on cu_pool or equivalent targeted repairs.