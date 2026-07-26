**Via shape sizing on M5**

The `resize_via_shape` operation on M5 in cell `VIA_VIA45_1_2_58_58`, shrinking the shape by 88 dbu along the y-axis, reduced total violations by 52 across two windows (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01). This repair touches M4, M5, and V4 simultaneously via the via-shape mechanism; connectivity was preserved. Y-axis via-shape resizes on M5 are a viable single-operation fix when the via cell generates violations in multiple windows (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01).

**M5.AUX.1 — Vertical edges must land on a 24 nm grid**

M5.AUX.1 checks that every vertical (90-degree) edge of M5 is at an x-coordinate that is a multiple of 24 nm. In trial:i02.ug.leaf_0004.03, moving M5 polygons p1143 by +32 dbu and p1142 by -16 dbu in x introduced 12 new M5.AUX.1 violations. Neither +32 nor -16 is a multiple of 24, so those moves placed vertical edges off-grid. Do not move M5 polygons by x-deltas that are not multiples of 24 dbu; use multiples of 24 (e.g., ±24, ±48) to maintain grid compliance (trial:i02.ug.leaf_0004.03).

**M5.AUX.3 — M5 may not bend**

M5.AUX.3 fires whenever an M5 polygon contains a corner angle between 0° and 90° (i.e., a non-straight segment). In trial:i02.ug.leaf_0004.03, moving polygon p1561 by +32 dbu in y alongside numerous instance moves introduced 38 new M5.AUX.3 violations — the largest single-rule count in the measured history. Never move or resize one end of an M5 polygon without correspondingly adjusting all connected M5 segments; a partial move creates a kink at the cell boundary where moved wires meet unmoved wires (trial:i02.ug.leaf_0004.03). When a unit move introduces M5.AUX.3 violations in large numbers, the moved cell contains M5 wires that connect across the crop boundary to wires that were not co-moved.

**M5.W.5 — Minimum vertical width is 44 nm**

M5.W.5 requires that every M5 polygon has a vertical (y-axis) extent of at least 44 nm. In trial:i02.ug.leaf_0004.03, the same polygon and instance moves that caused M5.AUX.3 violations also introduced 12 new M5.W.5 violations, indicating that shifting instance placements vertically without adjusting the corresponding M5 routing endpoints can compress wire heights below the 44 nm floor. When performing instance moves that shift M5 endpoints vertically, verify the resulting wire height does not drop below 44 dbu (trial:i02.ug.leaf_0004.03).

**M5.S.4 — Tip-to-tip spacing ≥ 40 nm for polygons sharing parallel run length**

M5.S.4 requires at least 40 nm tip-to-tip clearance between ends of M5 wires that share parallel run length on adjacent tracks. Trial:i02.ug.leaf_0004.03 introduced 4 new M5.S.4 violations as a side effect of the same polygon and instance moves that caused M5.AUX.3 and M5.W.5 violations. When shortening M5 wire endpoints or bringing adjacent-track M5 wires closer in y, verify that tip-to-tip separations remain at or above 40 nm (trial:i02.ug.leaf_0004.03).

**V4.M5.AUX.2 — V4 width must exactly match M5 width perpendicular to M5 length**

V4.M5.AUX.2 requires that each V4 via inside M5 spans exactly the same width as M5 measured perpendicular to the M5 wire direction. In trial:i02.ug.leaf_0003.02, x-axis moves of M5 polygons (p1145 by +32, p1144 by −16, p1143 by +32, p1142 by −16) without corresponding V4 adjustments introduced 4 new V4.M5.AUX.2 violations. When moving M5 polygons in x, simultaneously move or resize co-located V4 shapes by the same delta so the via-to-metal width relationship is preserved (trial:i02.ug.leaf_0003.02).

**Cross-leaf instance move conflicts**

In iter 2, leaf_0003 and leaf_0004 attempted conflicting x-axis moves on shared instances (e.g., i0345 was claimed by both leaves with different deltas: [32,−96] from leaf_0003 and [32,32] from leaf_0004). The assembler dropped both claims under `external_conflict_dropped`, and applied `cross_crop_first_wins` to polygon moves where both leaves touched the same polygon (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03). The first-committed leaf wins cross-crop polygon conflicts; instance conflicts between two claiming leaves result in both ops being dropped, leaving the underlying M5 violations unresolved. When repairing M5 violations in a region that spans multiple leaf crops, ensure the same instance is not assigned conflicting deltas by different leaves.

**Successful zero-side-effect repair patterns**

Two trials produced zero new violations of any rule: trial:i02.ug.leaf_0002.01 (move_instance i0181 by [−76,0] paired with resize_end on M5 polygon p1154 by +44 dbu at the low-y end) and trial:i03.ug.leaf_0001.00 (resize_end on M5 polygon p1187 by −32 dbu at the high-x end paired with move_instance i0181 by [76,0]). Both involved a single targeted M5 polygon end adjustment coupled with one instance move, touching only M4, M5, and V4. Pairing an M5 resize_end with a co-directional instance move is a proven zero-side-effect repair pattern for this design (trial:i02.ug.leaf_0002.01, trial:i03.ug.leaf_0001.00).