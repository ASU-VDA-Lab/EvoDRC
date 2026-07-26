**V4.W.1 — Minimum width 24 nm**

No width violations were directly isolated in the two recorded trials. The rule requires every V4 instance to be at least 24 nm wide along the M5 length direction. In trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 the repair operated on via cell VIA_VIA45_1_2_58_58, which carries a nominal shape size of 58×58 dbu; that cell geometry already satisfies the 24 nm floor, and no W.1 errors appeared in the post-repair delta. Retain the per-cell shape size at or above the 24 nm threshold when sizing V4 shapes.

**V4.S.1 / V4.S.2 / V4.S.3 — Minimum spacing 33 nm (same net, different net, corner-to-corner)**

All three spacing rules share the 33 nm threshold and differ only in the net-connectivity partition and measurement mode (projection vs. Euclidean). The unit-gate repair in trial:i02.ug.whole_design.00 moved 24 via instances along x in coordinated groups (delta_dbu values of 32, 48, 72, 96 dbu) while simultaneously extending M4/M5 polygon ends on the x-high edge, and the gate recorded zero new violations introduced into the crop window with conn_preserved=true. Move via instances as a group aligned to their shared metal segment rather than individually to avoid collapsing the inter-via gap below 33 nm (trial:i02.ug.whole_design.00). When instance displacements are small relative to the spacing budget, apply a uniform x-shift to the entire cluster rather than shifting a subset, as the grouped moves in trial:i02.ug.whole_design.00 preserved all spacing relationships across V1 through V4 simultaneously.

**V4.M4.EN.1 — Enclosure of V4 by M4 on at least two opposite sides ≥ 11 nm**

In trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, the repair applied resize_via_shape to both the V4 shape (shape_index 0 and 1, axis x, delta_dbu +152) and the M4 shape (shape_index 0, axis x, delta_dbu +152) within the same via cell, reducing total violations by 16 (from 68 to 52). The equal delta applied to both V4 and M4 in the same axis direction means the M4 boundary expanded by the same amount as the V4 shape, preserving the enclosure margin rather than shrinking it. Apply resize_via_shape to the M4 shape with the same axis and delta as the V4 shape resize when correcting enclosure in the x-direction (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01).

**V4.M5.EN.2 — Enclosure of V4 by M5 on two opposite sides ≥ 11 nm**

The repair in trial:i02.ug.whole_design.00 included resize_end operations on the x-high end of M5 polygons (e.g., p965, p964, p963, p962, p961, p960, p959, p958, p1065, p1036) with deltas ranging from 32 to 116 dbu, while via instances connected to those segments were moved by matching x-displacements. No new V4 violations were introduced, confirming that extending the M5 high-x end while shifting the via instance by the same or lesser x-delta maintains V4.M5.EN.2 compliance (trial:i02.ug.whole_design.00). Do not extend only one end of M5 without accounting for the via instance position; the instance moves in trial:i02.ug.whole_design.00 were paired with the polygon end resizes to keep V4 centered within the extended M5 envelope.

**V4.AUX.1 — V4 must be inside both M4 and M5**

In trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, the repair touched layers M4, M5, and V4 together (touched_layers field), and the V4 shape and M4 shape received identical x-axis deltas (+152 dbu each). The M5 layer was listed in touched_layers as well, indicating M5 was already at least as large as V4 in that cell or was adjusted concurrently. Resize V4 and its enclosing M4/M5 shapes together in the same operation group to keep V4 inside both metals simultaneously (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01).

**V4.M5.AUX.2 — V4 width must equal M5 width perpendicular to M5 length**

The unit-gate repair in trial:i02.ug.whole_design.00 included multiple resize_end operations on M5 polygon ends paired with via instance moves, and the gate verified zero new violations across the whole design crop. This confirms that when M5 is extended along its length (x-high end), the perpendicular width of M5 is not altered, and V4 width-match compliance is maintained as long as the via cell geometry is not independently resized in the perpendicular axis (trial:i02.ug.whole_design.00). In trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, the V4 shape resize was applied on the x-axis only (axis="x"), consistent with adjusting along the M5 length rather than the perpendicular direction; this repair reduced violations by 16 without introducing new V4.M5.AUX.2 failures, confirming that x-only shape resizes within a via cell do not disturb the perpendicular width match (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01).

**GEOMETRY.NONORTHOGONAL — No non-orthogonal edges**

All V4 operations in both recorded trials used axis-aligned moves (axis="x" resizes, integer dbu translations on x and y) and instance moves with orthogonal delta_dbu vectors. No non-orthogonal edges were introduced. Restrict all V4 shape edits to orthogonal axis-aligned operations to comply with the nonorthogonal block rule (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, trial:i02.ug.whole_design.00).

**Repair sequencing observed across trials**

The cu_pool trial (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01) targeted a single via cell definition and achieved a net reduction of 16 violations in 3 ops. The unit_gate trial (trial:i02.ug.whole_design.00) operated across the whole design with 45 ops and was gated in with no new violations, indicating that global instance repositioning paired with M5 end extension is a safe secondary pass after per-cell via resizes have been applied. Apply targeted via-cell resizes before global instance shift-and-extend passes; the ordering in trials i01 then i02 produced a monotonically decreasing violation count with no regression.