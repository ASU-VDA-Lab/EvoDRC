**V4 geometry is entirely coupled to its enclosing M4/M5 via-cell shapes; no standalone V4 polygon edits appear in this history.**

Across every trial that lists V4 in `touched_layers` — trial:i01.ug.leaf_0010.07, trial:i02.ug.leaf_0002.01, trial:i02.cu.def:VIA_VIA45_1_2_58_58.02, trial:i03.ug.leaf_0001.00, trial:i03.ug.leaf_0002.01, trial:i03.ug.leaf_0003.02, trial:i04.ug.leaf_0001.00 — the operations applied were either `move_instance`, `move` on M4/M5 polygons, or `resize_via_shape` on M5 within a via-cell definition. The V4 geometry moved or was reshaped only as a rigid passenger of those enclosing layers. No op in the history targeted a V4 polygon directly.

**Rule V4.AUX.1: V4 must remain inside both M4 and M5 simultaneously.**

Because M4 and M5 must both cover every V4 instance (V4.AUX.1), any operation that displaces M4 or M5 without the same displacement applied to the other enclosing layer risks an AUX.1 violation. trial:i02.cu.def:VIA_VIA45_1_2_58_58.02 applied a y-axis resize of −88 dbu to the M5 shape inside via cell `VIA_VIA45_1_2_58_58` and listed both M4 and V4 as touched layers alongside M5, confirming that a single M5-only shape change propagates DRC exposure to V4 as well. When resizing an M5 via shape, verify that the resulting M5 boundary still covers the full V4 extent on all sides.

**Rule V4.M5.AUX.2: V4 width must match M5 width in the direction perpendicular to M5 length.**

trial:i02.cu.def:VIA_VIA45_1_2_58_58.02 shrank the M5 via shape in y by 88 dbu (decision `applied`, delta_total −15). V4 appeared in `touched_layers`, confirming that a y-axis M5 resize forces re-evaluation of the perpendicular-width match constraint. The fact that this trial was accepted (`applied`, conn_preserved) and produced a net violation reduction of 15 shows that shrinking an over-sized M5 via shape to tighten the perpendicular match is a valid repair strategy. Avoid leaving M5 via shapes larger than V4 in the axis perpendicular to the M5 wire direction.

**Rules V4.M4.EN.1 and V4.M5.EN.2: 11 nm minimum two-sided enclosure.**

No trial in this history produced a new out-of-crop V4.M4.EN.1 or V4.M5.EN.2 violation. All seven accepted trials preserved connectivity (`conn_preserved: true`) and introduced zero new out-of-crop violations (`n_new_out_of_crop: 0`). Instance moves of ±24, ±32, ±64, ±72, or ±96 dbu along x or y were uniformly safe under the enclosure rules when the same displacement was applied to the via instance as a whole (trial:i01.ug.leaf_0010.07, trial:i03.ug.leaf_0001.00, trial:i03.ug.leaf_0002.01, trial:i03.ug.leaf_0003.02, trial:i04.ug.leaf_0001.00). Moving a via instance as a rigid body preserves M4/M5 enclosure because the enclosing layers are co-moved; splitting the displacement — moving only the via or only the M4/M5 wire — is the configuration that risks enclosure violations.

**Rules V4.W.1, V4.S.1, V4.S.2, V4.S.3: width and spacing.**

No in-crop or out-of-crop violation for V4.W.1, V4.S.1, V4.S.2, or V4.S.3 was reported across any trial in this history. The x-axis displacements of ±32 dbu applied in trial:i02.ug.leaf_0002.01, trial:i03.ug.leaf_0002.01, trial:i03.ug.leaf_0003.02, and trial:i04.ug.leaf_0001.00 did not trigger spacing or width errors for V4, indicating that the existing inter-via pitches in this block comfortably exceed the 33 nm spacing minima at the 32 dbu step granularity in use.

**Polygon p879 conflict and re-application pattern.**

Polygon p879 (an M5 wire) was moved x+32 in trial:i02.ug.leaf_0002.01 but the move was dropped during assembly because the cu_pool had already claimed that polygon via a prior applied op (assemble_drops reason `reserved_by_cu_pool_winner`). The same move — p879 x+32 — was applied successfully in trial:i04.ug.leaf_0001.00 two iterations later, accompanied by x+32 moves of instances i0114, i0112, i0073, and i0062, with n_new_in_crop=8 and n_new_out_of_crop=0. This demonstrates that when an M5/V4-touching polygon move is blocked by a cu_pool winner in one iteration, resubmitting it in a later iteration after the cu_pool op has been absorbed is safe and effective.

**cu_pool channel versus unit_gate channel for V4-touching ops.**

The cu_pool channel operates on via-cell definitions (target `def:VIA_VIA45_1_2_58_58` in trial:i02.cu.def:VIA_VIA45_1_2_58_58.02), meaning a single accepted op propagates to every instantiation of that cell simultaneously, producing block-wide violation reduction (−15 total across leaf_0002 and leaf_0003). The unit_gate channel operates instance-by-instance; its V4-touching moves are per-leaf and may conflict with cu_pool claims on shared polygons. When a cu_pool op on an M5 via shape is pending or recently applied, unit_gate ops on polygons shared with that via cell will be dropped (trial:i02.ug.leaf_0002.01 assemble_drops). Schedule cu_pool via-shape repairs before unit_gate instance moves on the same via geometry.

**New in-crop violations introduced by V4-touching trials are not V4 rule violations.**

trial:i03.ug.leaf_0002.01 introduced 45 new in-crop violations when four instances were moved x−32, yet the `per_rule` breakdown lists M1.A.1 (4), M4.W.5 (2), and V1.M1.EN.1 (12) — no V4 rule appears. trial:i02.ug.leaf_0002.01 introduced new_in_crop violations for M5.AUX.1 (7), M5.AUX.3 (13), M5.S.4 (2), and M5.W.5 (5) with V4 in touched_layers — again no V4 rule. This consistent pattern across all gated-in trials confirms that V4 DRC rules are not the binding constraint for V4-touching moves in this block; the congestion driving the repair iterations originates in M5 and M4 rules, and V4 rides along without independently generating new violations.

**Connectivity preservation is a hard gate for all accepted trials.**

Every trial in this history was accepted only with `conn_preserved: true`. No trial was accepted with a connectivity loss. For V4-touching moves, this means the entire co-move group — via instance plus all connected M4/M5 wire segments — must be displaced together. trial:i03.ug.leaf_0003.02 illustrates the required group structure: p878 (M5), i0001, i0067, and i0113 all carried group tag `m5_fix` and were moved x+32 as a unit, preserving the net topology through V4 while also accepting simultaneous y-axis shrink of p892 (resize low +32, high −32) on the same M5 wire without introducing out-of-crop violations.