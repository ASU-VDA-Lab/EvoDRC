## Repair Patterns and Operation Outcomes

### X-axis Instance Moves Are Consistently Safe

Lateral (x-axis) instance moves spanning 12 dbu to 108 dbu have produced zero new M2 violations across every gated-in unit-gate trial in iterations 1 through 3. Magnitudes observed: 12 dbu (trial:i01.ug.Block4_union_row10.01), 28 dbu (trial:i02.ug.Block4_union_row3.02, trial:i01.ug.Block4_union_row7.06), 36 dbu (trial:i01.ug.Block4_union_row1.00, trial:i01.ug.Block4_union_row6.05, trial:i01.ug.leaf_0008.08, trial:i01.ug.leaf_0020.09, trial:i03.ug.leaf_0001.01), 37 dbu (trial:i01.ug.Block4_union_row5.04), 72 dbu and 96 dbu (trial:i02.ug.Block4_union_row1.00, trial:i02.ug.Block4_union_row10.01), and 108 dbu (trial:i02.ug.Block4_union_row7.03). Prefer x-axis displacements when a spacing or enclosure target can be satisfied without y-axis movement.

### Y-axis Instance Moves Introduce M2.S.2, M2.S.7, and V1.M2.EN.2 Violations

Moving an instance in the y-direction at the magnitudes tested in iteration 2 reliably triggered new M2-layer violations even when connectivity was preserved:

- A move of [0, −44] dbu on instance i0038 (trial:i02.ug.leaf_0008.04) introduced 1 new M2.S.2 violation (tip-to-side spacing < 25 nm) and 1 new V1.M2.EN.2 violation (V1 enclosure by M2 < 5 nm on two opposite sides).
- A move of [0, −36] dbu on instance i0038 (trial:i02.ug.leaf_0013.06) introduced 1 new M2.S.7 violation (tip-to-tip gap co-located with side-to-side spacing ≤ 32 nm, parallel run length < 35 nm) along with violations on M1, M4, and V1 layers (9 new total in crop).

Both trials were gated_in only because conn_preserved was true; the new violations represent DRC debt deferred into future iterations. Do not rely on conn_preserved acceptance as validation that a y-axis move is M2-clean. When a y-axis move is necessary, verify that the resulting M2 tip edges satisfy the 25 nm tip-to-side rule (M2.S.2) and that M2 enclosure of V1 meets 5 nm on at least one pair of opposite sides (V1.M2.EN.2) before committing.

The [0, −64] dbu move in trial:i03.ug.leaf_0004.02 also registered n_new_in_crop = 2, though no per-rule breakdown was recorded for that trial; the pattern of y-displacement introducing new violations is consistent across iterations 2 and 3.

### M2.S.7: Parallel Run Length Must Reach 35 nm When Side Spacing ≤ 32 nm

M2.S.7 fires when an 18 nm tip-to-tip gap is co-located with a side-to-side separation ≤ 32 nm, or when the parallel run length between facing side edges is < 35 nm under that same side spacing. trial:i02.ug.leaf_0013.06 is the direct measured example: a [0, −36] dbu y-shift on i0038 created exactly this geometry. When adjusting M2 wires in dense rows where side-to-side spacing is at or below 32 nm, ensure the parallel overlap between adjacent wires is ≥ 35 nm before finalizing any vertical offset or tip relocation.

### Resize_end on M2 Polygons Combines With Instance Moves

Several accepted trials pair a resize_end operation on an M2 polygon with one or more instance moves:

- trial:i01.ug.leaf_0008.08: resize_end +92 dbu (axis x, end high) on polygon p1604, combined with instance move [36, 0] on i0274, zero new violations.
- trial:i02.ug.Block4_union_row7.03: resize_end +52 dbu (axis x, end high) on polygon p1595, combined with move [108, 0] on i0153, zero new violations.
- trial:i02.ug.Block4_union_row10.01: resize_end +16 dbu (axis x, end high) on polygon p1551, combined with three instance moves, zero new violations.
- trial:i01.ug.Block4_union_row2.02: polygon p1548 moved +16 dbu along x as part of a three-operation set, zero new violations.

In iteration 4, trial:i04.ug.leaf_0003.01 applied resize_end −8 dbu (axis x, end high) on polygon p1410 combined with instance move [−8, 0] on i0238, touching M2, M3, and V2, and introduced 2 new in-crop violations while still being gated_in. Small negative x resizes on M2 polygons that reduce wire length toward an enclosure or spacing minimum carry violation risk; verify M2 width ≥ 18 nm (M2.W.1) and area ≥ 504 nm² (M2.A.1) after any shrink of polygon extent.

### VIA_VIA23 Cell Repairs via cu_pool: Group Resizes Outperform Single-Shape Edits

The cu_pool channel targets cell definition VIA_VIA23_1_3_36_36, which touches M2, M3, and V2. Two competing strategies were tested in iteration 1:

- trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 (applied, delta_total = −24): Applied 13 operations — one resize_via_shape on M3 (axis y, −40 dbu) and twelve group_v2m3 polygon resizes (axis y, −64 dbu each on p1411–p1422). This coordinated group shrink reduced violations by 24 across windows leaf_0025 (88→64) and leaf_0026 (35→35).
- trial:i01.cu.def:VIA_VIA23_1_3_36_36.01 (lost_tournament, delta_total = 0): Applied only the single resize_via_shape on M3 (axis y, −40 dbu) without the group polygon resizes. Zero improvement; lost the tournament.

Apply the full group_v2m3 resize set together, not the via-shape resize in isolation, when targeting this via cell definition. In iteration 3, trial:i03.cu.def:VIA_VIA23_1_3_36_36.00 (applied, delta_total = −17) instead moved a V2 via shape laterally +144 dbu along x, reducing violations by 17 across leaf_0006 (63→51) and leaf_0007 (33→28). Both strategies succeeded when applied as the winning tournament candidate; the single-shape attempt did not.

### Instance i0038 Is a Multi-Unit Conflict Hotspot

Instance i0038 was independently targeted in iteration 2 by both leaf_0008 (proposing [0, −44]) and leaf_0013 (proposing [0, −36]), and again in iteration 3 by leaf_0004 (proposing [0, −64]). The assemble step dropped one of the conflicting operations in each iteration 2 trial due to external_conflict_dropped (trial:i02.ug.leaf_0008.04, trial:i02.ug.leaf_0013.06). When multiple units claim the same instance, the losing operation is silently dropped at assembly, and the winning move's M2 impact must be evaluated in isolation. Do not assume that a proposed move on i0038 will be present in the final assembled state when another unit also proposes a move on it in the same iteration.

### V1.M2.EN.2 and V1.M2.AUX.2: Enclosure Constraint Triggered by Y-Displacement

V1.M2.EN.2 requires M2 to enclose V1 by ≥ 5 nm on two opposite sides (either 5 & 5 nm or 5 & 0 nm). V1.M2.AUX.2 requires V1 width to match M2 width along the direction perpendicular to M2 length (i.e., V1 edges must be coincident with M2 edges on at least two sides). trial:i02.ug.leaf_0008.04 demonstrates that a y-displacement of −44 dbu on an instance containing M2 wires over V1 can break the enclosure requirement. Any instance move with a y-component must be checked against V1 positions to ensure M2 maintains the required enclosure on both horizontal and vertical edge pairs.

### All M2 Geometry Must Remain Orthogonal

The NONORTHOGONAL rule applies to M2 alongside all other drawing layers. No edge of any M2 polygon may carry an angle other than 0° or 90°. All operations in the recorded history — move_instance, resize_end, polygon move, resize_via_shape, move_via_shape — produce axis-aligned deltas exclusively. Do not introduce diagonal moves or non-rectilinear polygon edits on M2 at any stage of repair.

### Observed Effective Operation Magnitudes (M2 Layer, Iterations 1–4)

Across all gated_in, applied, and conn_preserved trials touching M2:

- X-axis instance displacements that produced zero new M2 violations: 12, 16, 28, 36, 37, 72, 96, 108 dbu (trial:i01.ug.Block4_union_row10.01, trial:i01.ug.Block4_union_row2.02, trial:i02.ug.Block4_union_row3.02, trial:i01.ug.Block4_union_row1.00, trial:i01.ug.Block4_union_row5.04, trial:i02.ug.Block4_union_row1.00, trial:i02.ug.Block4_union_row10.01, trial:i02.ug.Block4_union_row7.03).
- Y-axis instance displacements that introduced new M2 violations: −36 dbu (trial:i02.ug.leaf_0013.06), −44 dbu (trial:i02.ug.leaf_0008.04), −64 dbu (trial:i03.ug.leaf_0004.02).
- Polygon resize_end on M2 axis x that produced zero new violations: +16, +52, +92 dbu (trial:i01.ug.Block4_union_row2.02, trial:i02.ug.Block4_union_row7.03, trial:i01.ug.leaf_0008.08).
- Polygon resize_end on M2 axis x that introduced 2 new violations: −8 dbu (trial:i04.ug.leaf_0003.01).
- Group y-resizes on M2/M3 group_v2m3 polygons of −64 dbu (12 shapes simultaneously) that reduced violations by 24: trial:i01.cu.def:VIA_VIA23_1_3_36_36.00.