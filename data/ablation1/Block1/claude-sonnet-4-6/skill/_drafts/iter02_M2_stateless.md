## Effective Operation Types on M2

All M2 repairs in the measured history used three polygon-level operation categories — `move_instance`, `resize_end`, and `resize` — plus via-cell operations (`add_via`, `delete_instance`, `resize_via_shape`) that carry M2 consequences.

**move_instance** is the dominant op. Observed X-axis deltas: +36, −36, +108, −32 dbu. One Y-axis delta of −36 dbu appeared in trial:i01.ug.Block1_union_row4.04. All move trials that preserved connectivity were accepted, even when they introduced new in-crop violations. Use +36 dbu as the default grid step; +108 dbu (3× step) is valid when a larger displacement is needed to clear a spacing violation (trial:i01.ug.Block1_union_row8.07). Non-grid steps of −32 dbu were applied successfully in trial:i01.ug.Block1_union_row6.06 and trial:i01.ug.Block1_union_row8.07, so the solver is not strictly constrained to 36 dbu multiples.

**resize_end** adjusts one tip of an M2 polygon. All accepted resize_end operations extended rather than retracted polygon ends. High-end (x-axis) extensions: +128 dbu on p1320 and +92 dbu on p1321 (trial:i01.ug.Block1_union_row1.00); +92 dbu on p1370 (trial:i01.ug.Block1_union_row3.03); +52 dbu on p1238 (trial:i01.ug.Block1_union_row4.04); +36 dbu on p1297 (trial:i01.ug.Block1_union_row5.05). Low-end extensions: +36 dbu on p1301 (trial:i01.ug.Block1_union_row5.05) and +36 dbu on p1253 (trial:i01.ug.leaf_0020.10). Paired high-end and low-end resizes on distinct polygons within one trial are accepted (trial:i01.ug.Block1_union_row5.05 extended the high end of p1297 and the low end of p1301 in the same commit). `resize_end` directly addresses tip-spacing rules by moving the tip edge; it is the natural tool for M2.S.2, M2.S.3, M2.S.4, M2.S.5, M2.S.7, and M2.S.8 violations.

**resize** (symmetric, both ends simultaneously) was applied once: p1390 was expanded +36 dbu symmetrically in trial:i01.ug.leaf_0031.11. That trial introduced 4 new in-crop violations but was still gated_in because connectivity was preserved. Use symmetric resize to increase M2 enclosure around a via when an asymmetric extension would break routing continuity.

## Acceptance Gate: Connectivity Preservation Dominates

Every gated_in trial in the record had `conn_preserved: true`. The gating criterion is connectivity-first: new in-crop DRC violations do not prevent acceptance when connectivity is intact. Trials with n_new_in_crop = 4 (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.leaf_0031.11) and n_new_in_crop = 1 (trial:i01.ug.Block1_union_row6.06, trial:i02.ug.Block1_union_row6.01) were all gated_in. Do not discard an op set solely because it introduces in-crop violations if connectivity is preserved.

The only rejection in the M2-touching record is trial:i02.cu.def:VIA_VIA23_1_3_36_36.00, which was `rejected_net_positive` with delta_total = 0: no reduction in DRC violation count was achieved across units leaf_0014 (175 before, 175 after) and leaf_0015 (113 before, 113 after). Rejection on net_positive grounds is distinct from a connectivity failure — the op itself was legal; it simply produced no benefit. Do not commit via-cell resizes that leave the total DRC count unchanged.

## Via Enclosure: V1 on M2

**Via replacement (V1.M2.EN.2, V1.M2.AUX.2):** In trial:i02.ug.leaf_0004.02, a `delete_instance` + `add_via` (cell VIA_VIA12) at origin [5904, 6300] on the M1/M2/V1 layer set produced zero new violations (n_new_in_crop = 0). Via replacement at a fresh position resolves V1.M2.EN.2 enclosure shortfalls without introducing spacing violations on M2, provided the new origin is chosen inside a region where M2 enclosure on two opposite sides meets the 5 nm minimum. The complementary rule V1.M2.AUX.2 — requiring V1 width to match M2 width in the perpendicular direction — is automatically satisfied when the replacement via cell carries the correct geometry and is placed fully within the existing M2 stripe.

## Via Enclosure: V2 on M2

**V2 via shrink (V2.M2.EN.1):** In trial:i02.cu.def:VIA_VIA23_1_3_36_36.00, shrinking the M3 shape of cell VIA_VIA23_1_3_36_36 by −40 dbu in Y produced delta_total = 0 — no reduction in DRC errors. Contracting the M3 dimension of a V2 via cell in the Y direction does not resolve M2-side violations under V2.M2.EN.1. Address V2.M2.EN.1 shortfalls by extending the M2 polygon to satisfy the 5 nm enclosure on at least two opposite sides; do not rely on shrinking the via cell's non-M2 metal layer.

## Sizing Bounds Implied by the Record

Every `resize_end` delta in the accepted history is positive (polygon extension). No accepted trial retracted an M2 polygon tip. This is consistent with V1.M2.EN.2 and V1.M2.AUX.2: shrinking M2 risks dropping below the 5 nm enclosure margin or making M2 narrower than the co-located V1.

M2.A.1 requires area ≥ 504 nm². With M2.W.1 enforcing minimum width 18 nm, the minimum length of a rectangular M2 segment is 504 / 18 = 28 nm. No trial in the history retracted an M2 end, so no trial tested this lower bound; however, any future `resize_end` with a negative delta must be checked against M2.A.1 before committing.

M2.W.1 (minimum width 18 nm) sets the floor on any transverse resize. All symmetric and asymmetric extensions observed in the history move away from this floor. Avoid any resize that reduces M2 width below 18 nm on any edge segment.

## Grid Step Reference

The 36 dbu step appears in every unit-gate trial: trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row10.01, trial:i01.ug.Block1_union_row3.03, trial:i01.ug.Block1_union_row4.04, trial:i01.ug.Block1_union_row5.05, trial:i01.ug.Block1_union_row6.06 (in addition to −32), trial:i01.ug.Block1_union_row8.07, trial:i01.ug.Block1_union_row9.08, trial:i01.ug.leaf_0004.09, trial:i01.ug.leaf_0020.10, trial:i01.ug.leaf_0031.11, trial:i02.ug.Block1_union_row6.01. Non-36 move deltas observed: −32 dbu (trial:i01.ug.Block1_union_row6.06, trial:i01.ug.Block1_union_row8.07), +108 dbu (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row8.07). Non-36 resize_end deltas: +52, +92, +128 dbu (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row3.03, trial:i01.ug.Block1_union_row4.04). Use 36 dbu as the baseline; larger steps are valid when 36 dbu leaves the spacing violation unsatisfied.