## Operation Taxonomy

Across all 18 accepted trials (iterations 1–4), three primitive operation types appear on V1-touching repairs: `move_instance`, `resize_end`, and `resize` (symmetric). A fourth composite pattern — `delete_instance` + `add_via` — appears once. Every trial carries `decision: gated_in` and `conn_preserved: true`, confirming that connectivity preservation is a hard gating condition for acceptance.

---

## Rule V1.AUX.1 — V1 Must Lie Inside M1 ∩ M2

V1.AUX.1 flags any V1 polygon not fully contained within both M1 and M2. Every repair in the measured record that touches V1 simultaneously adjusts M1 and/or M2 in the same operation bundle (`touched_layers: ["M1","M2","V1"]` in all 18 trials, e.g., trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row8.07, trial:i04.ug.leaf_0004.03). Never move a V1 polygon without also repositioning or resizing the enclosing M1 and M2 shapes in the same commit; isolated V1 displacement re-triggers V1.AUX.1.

---

## Rule V1.M2.AUX.2 — V1 Width Must Match M2 Width Perpendicular to M2 Length

V1.M2.AUX.2 requires that the V1 polygon edge along the direction perpendicular to M2 length is flush with (coincident with) exactly two opposite M2 edges. Resize operations in the history always operate on the axis parallel to M2 length (x-axis `resize_end` on polygons p1320, p1321, p1370, p1238, p1297, p1301, p1253, p1295, p1390 — trial:i01.ug.Block1_union_row1.00 through trial:i03.ug.leaf_0004.01). Symmetric resize on the perpendicular axis is not used to fix this rule; instead, the via instance is replaced by an `add_via` call that places a correctly sized via cell (trial:i02.ug.leaf_0004.02, which deleted instance i0300 and inserted `VIA_VIA12` at an explicit origin). When the V1 width mismatch cannot be resolved by a single `resize_end`, use the `delete_instance` + `add_via` replacement path rather than attempting a perpendicular resize.

---

## Rule V1.W.1 — Minimum Width 18 nm Along M2 Length

V1.W.1 enforces a minimum 18 nm V1 width measured along M2 length. Violations are resolved by widening the V1 instance, which in practice means either resizing the M2 polygon end (`resize_end`, `end: high` or `end: low`) to extend coverage, or replacing the cell with a via cell that already meets the width requirement. In trial:i01.ug.Block1_union_row1.00, `resize_end` with `delta_dbu: 128` on p1320 and `delta_dbu: 92` on p1321 (both x-axis, `end: high`) resolved width issues while simultaneously preserving 4 in-crop violations as acceptable. In trial:i01.ug.leaf_0031.11, a symmetric `resize` of delta 36 dbu on p1390 addressed width in that locus. Do not apply `resize_end` to only one polygon when two adjacent M2 polygons share the V1 span — trial:i01.ug.Block1_union_row1.00 demonstrates that both must be resized together.

---

## Rule V1.M1.EN.1 — M1 Enclosure of V1 (5 nm + 2 nm on Opposite Sides)

V1.M1.EN.1 requires that M1 encloses V1 by at least 5 nm on one axis-aligned side pair and at least 2 nm on the opposite side (projection measurement). Because V1 and M1 are co-repaired in every trial, `move_instance` shifts on M1 instances serve double duty: they re-establish M1 enclosure while also keeping V1 within bounds. In trial:i01.ug.Block1_union_row5.05, both `resize_end` (polygons p1297, p1301) and `move_instance` (instances i0313, i0294, i0433) were applied together to satisfy enclosure on both ends. A single-direction move of 36 dbu — the dominant step size across trial:i01.ug.Block1_union_row9.08 and trial:i03.ug.Block1_union_row3.00 — is sufficient to restore the 2 nm minimum when the prior gap was marginally short. When the short-enclosure side is the high end of M1, apply `resize_end` with `end: high`; when it is the low end, use `end: low` (trial:i01.ug.Block1_union_row5.05, trial:i01.ug.leaf_0020.10).

---

## Rule V1.M2.EN.2 — M2 Enclosure of V1 (5+5 or 5+0 nm on Opposite Sides)

V1.M2.EN.2 accepts two configurations: 5 nm enclosure on both opposite sides, or 5 nm on one side and flush (0 nm, coincident edge) on the other. The flush configuration corresponds to V1 being a "no end-cap" (NEC) via in the deck's classification. Moving an M2-connected instance by a multiple of 36 dbu (trial:i01.ug.leaf_0004.09: +36 dbu; trial:i03.ug.leaf_0004.01: +72 dbu on i0294 plus `resize_end` +72 dbu on p1295) restores the 5 nm enclosure on the lagging side. The `resize_end` applied to M2 polygon p1295 in trial:i03.ug.leaf_0004.01 followed the same 72 dbu delta as the corresponding `move_instance`, confirming that the M2 polygon end must track the via's new position to maintain enclosure without creating a gap.

---

## Rules V1.S.1 / V1.S.2 / V1.S.3 / V1.S.4 — Spacing

V1.S.1 governs minimum projection spacing between V1 mask regions (18 nm same-track, 27 nm parallel non-aligned, 18 nm parallel aligned). V1.S.2–S.4 govern euclidean corner-to-corner spacing depending on end-cap presence (23 nm WEC–WEC, 30 nm NEC–NEC, 27 nm WEC–NEC).

The measured repair strategy for spacing violations is lateral displacement of the via instance or the M2 polygon it sits on, not resizing V1 itself. In trial:i01.ug.Block1_union_row4.04, instance i0300 was moved [36, -36] dbu (including a y-component) plus instances i0432 and i0438 were shifted +36 dbu x, combined with `resize_end` +52 dbu on p1238, to relieve a spacing conflict. The y-component move of -36 dbu in that trial is the only non-zero y-delta in the entire history; it shifts the V1 mask off a parallel track that was too close, directly addressing a V1.S.1 parallel-track spacing scenario.

For WEC (with-end-cap) via spacing (V1.S.2), moving the offending instance by 36 dbu or a multiple thereof resolves the 23 nm euclidean requirement when the initial gap was close to the limit, as confirmed by the consistent 36 dbu step size across trial:i01.ug.Block1_union_row9.08 and trial:i03.ug.leaf_0005.02. For NEC vias (V1.S.3, 30 nm euclidean), the larger clearance demand means a single 36 dbu move may be insufficient when the spacing deficit exceeds 36 dbu; in those cases, two sequential moves on the same unit across consecutive iterations are the observed pattern (trial:i01.ug.Block1_union_row3.03 → trial:i03.ug.Block1_union_row3.00, where i0290 received +36 dbu in iteration 1 then +72 dbu in iteration 3).

---

## Via Replacement Pattern

When a via instance cannot satisfy both V1.M2.AUX.2 and spacing rules simultaneously through positional moves, the repair uses `delete_instance` + `add_via` with cell `VIA_VIA12` at a corrected origin. This was applied in trial:i02.ug.leaf_0004.02: instance i0300 was deleted and a new via was inserted at origin [5904, 6300] dbu, yielding zero new violations in that crop. The replacement via origin must be chosen to land on M2 with exactly two coincident M2 edges (satisfying V1.M2.AUX.2) and adequate clearance to neighbors. After replacement, re-check the M1 enclosure (V1.M1.EN.1) because the new via origin changes which M1 polygon provides enclosure.

---

## Grid Alignment

All `move_instance` deltas in the accepted history are multiples of 4 dbu, with the dominant step being 36 dbu (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row10.01, trial:i01.ug.Block1_union_row3.03, trial:i01.ug.Block1_union_row4.04, trial:i01.ug.Block1_union_row5.05, trial:i01.ug.Block1_union_row9.08, trial:i01.ug.leaf_0004.09, trial:i01.ug.leaf_0031.11, trial:i02.ug.Block1_union_row6.01, trial:i03.ug.leaf_0004.01, trial:i03.ug.leaf_0005.02, trial:i04.ug.leaf_0001.00). The smallest observed move is 4 dbu (trial:i04.ug.leaf_0004.03, where a single x-delta of 4 dbu on i0060 gated in with 80 new in-crop violations still accepted due to conn_preserved). Off-36 deltas (-32 dbu in trial:i01.ug.Block1_union_row6.06 and trial:i01.ug.Block1_union_row8.07) also accepted, so the grid is not strictly enforced at 36 dbu, but 36 dbu and its multiples are the standard repair step for this layer.

---

## GEOMETRY.NONORTHOGONAL — All V1 Edges Must Be Axis-Aligned

The GEOMETRY.NONORTHOGONAL rule flags any V1 edge not at 0° or 90°. Every `resize_end` and `resize` operation in the measured history is confined to the x-axis (`axis: "x"` in all resize records: trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row3.03, trial:i01.ug.Block1_union_row5.05, trial:i01.ug.leaf_0020.10, trial:i01.ug.leaf_0031.11, trial:i03.ug.leaf_0004.01), and all `move_instance` deltas in the history have integer x and y components with no diagonal component except the single [36,-36] case in trial:i01.ug.Block1_union_row4.04, which moves the entire instance orthogonally in both axes simultaneously rather than introducing a diagonal edge. Apply only axis-aligned resizes (x-axis or y-axis independently) to V1 or its enclosing M2 polygons; do not use diagonal or rotated geometry operations on any polygon that shares an edge with V1.