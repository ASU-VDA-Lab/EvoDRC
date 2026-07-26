## M5 Width Rules

**M5.W.5: Minimum vertical width 44 nm**

Trial i02.ug.leaf_0002.01 introduced 5 new M5.W.5 violations as part of a compound operation that moved polygon p879 by x+32 nm and shifted multiple instances by mixed x and y deltas. When M5 polygons or via shapes are resized in y, the remaining vertical span must be verified to stay at or above 44 nm. The cu_pool y-shrink of the M5 shape inside VIA_VIA45_1_2_58_58 by 88 nm (trial i02.cu.def:VIA_VIA45_1_2_58_58.02) did not introduce new M5.W.5 violations and netted a delta_total of -15, confirming that shrinking an over-extended M5 via shape in y can be done without triggering W.5 when the pre-shrink height far exceeds 44 nm.

## M5 Spacing Rules

**M5.S.4: Tip-to-tip spacing on parallel-run-length adjacent tracks (40 nm)**

Trial i02.ug.leaf_0002.01 introduced 2 new M5.S.4 violations alongside its x+32 nm move of polygon p879 and associated instance moves. Shifting M5 polygon endpoints in x while leaving neighboring polygons in place alters the parallel run-length relationship between tip pairs on adjacent tracks, converting geometries not previously governed by M5.S.4 into configurations where tip pairs share a run length and the 40 nm spacing requirement applies.

## M5 Grid and Routing Track Rules

**M5.AUX.1: Vertical edges must lie on 24 nm x-grid**

Trial i02.ug.leaf_0002.01 moved polygon p879 by x+32 nm — a delta not divisible by 24 nm — and introduced 7 new M5.AUX.1 violations. Moving M5 polygons in x by amounts that are not multiples of 24 nm shifts previously on-grid vertical edges to off-grid positions. This is the highest single-rule violation count attributable to a non-compliant x-delta in this history.

Trial i03.ug.leaf_0001.00 applied resize_end operations of x+28 nm on polygon p946 and x+64 nm on polygon p968 (neither 28 nor 64 is a multiple of 24 nm) and the trial recorded 5 new in-crop violations total. The per-rule breakdown for that trial is not present in the history, so the M5.AUX.1 contribution cannot be individually isolated, but the co-occurrence of non-24 nm x-end resizes with new violations is consistent with the AUX.1 behavior observed in trial i02.ug.leaf_0002.01.

Trial i03.ug.leaf_0003.02 moved polygon p878 by x+32 nm under the "m5_fix" group label and recorded 15 new in-crop violations; the per-rule breakdown for that trial is not present in the history, so the M5.AUX.1 impact of that specific move cannot be separately quantified.

**M5.AUX.3: M5 may not bend**

Trial i02.ug.leaf_0002.01 produced 13 new M5.AUX.3 violations — the single largest M5 rule count in the measured history — alongside moving polygon p879 by x+32 nm and moving instances i0114, i0112, i0073, i0075, i0076, i0105 by differing combinations of x and y deltas (x+32 paired with y values of 0, -48, +96, +48, +96, -48). Displacing different connected instances by different x and y amounts in the same trial set causes previously straight M5 paths to develop corner junctions flagged by AUX.3.

The cu_pool y-resize of p879 by +96 nm (trial i02.cu.poly:p879.00) and the M5 via shape y-shrink by -88 nm (trial i02.cu.def:VIA_VIA45_1_2_58_58.02) introduced no AUX.3 violations, confirming that pure y-axis resizes that do not alter a polygon's x-extent are AUX.3-safe.

## Via–M5 Enclosure Rules

**V4.M5.AUX.2: V4 must be exactly the same width as M5 perpendicular to M5 length**

The cu_pool operation trial i02.cu.def:VIA_VIA45_1_2_58_58.02 resized the M5 layer shape (shape_index 0) inside via cell VIA_VIA45_1_2_58_58 by y-88 nm and produced delta_total -15 (unit:leaf_0002 dropped from 17 to 8 violations; unit:leaf_0003 dropped from 25 to 19 violations). This is the highest-yield single M5 repair in the measured history. V4.M5.AUX.2 flags M5 shapes that extend beyond the V4 body width in the direction perpendicular to M5 routing; trimming the M5 via shape in y to match V4 width resolves this class of violations. Trial i02.cu.def:VIA_VIA45_1_2_58_58.02 shows that large y-shrinks (88 nm) on over-extended M5 via shapes are both connectivity-safe (conn_preserved: true) and high-yield.

## cu_pool Channel Behavior on M5

Two cu_pool operations touching M5 were applied in iter 2, both recorded as "applied":

- trial i02.cu.poly:p879.00: resize polygon p879 in y by +96 nm on the M5 layer, delta_total -2. The unit_gate trial i02.ug.leaf_0002.01 had also targeted p879 with an x+32 nm move; the x-move was dropped at assembly (assemble_drops, reason: reserved_by_cu_pool_winner) and only the cu_pool's y-resize was applied. This demonstrates that cu_pool operations take priority over conflicting unit_gate polygon moves when both target the same polygon in the same iteration.

- trial i02.cu.def:VIA_VIA45_1_2_58_58.02: resize M5 via shape in y by -88 nm, delta_total -15. Touched layers M4, M5, V4. No new violations were recorded.

## assemble_drops and Inter-Unit Conflicts

Two assemble_drop events appear in the history:

- trial i02.ug.leaf_0002.01 dropped the x+32 move of p879 (reason: reserved_by_cu_pool_winner). The cu_pool's y-resize of p879 and V2 via move were noted in assemble_drops as already applied via cu_pool.

- trial i03.ug.leaf_0002.01 dropped the move_instance i0073 x-32 op (reason: external_duplicate) because both leaf_0001 (trial i03.ug.leaf_0001.00) and leaf_0002 (trial i03.ug.leaf_0002.01) independently included the same instance move. When two unit_gate trials in the same iteration claim the same instance move, the duplicate is dropped at assembly. Trial i03.ug.leaf_0002.01 proceeded with its three remaining instance moves (i0114, i0112, i0062 all x-32) and was gated_in with 45 new in-crop violations (per-rule: M1.A.1: 4, M4.W.5: 2, V1.M1.EN.1: 12); no M5-specific rule violations appeared in its per-rule breakdown, indicating that the x-32 instance moves in that trial did not generate M5.* violations despite touching M4, M5, and V4 layers.

## y-Axis Resizes on M5 Polygons

y-axis resizes on M5 do not alter the x-coordinates of vertical edges and therefore carry no M5.AUX.1 risk. Trial i02.cu.poly:p879.00 (y+96 nm, delta -2) and trial i02.cu.def:VIA_VIA45_1_2_58_58.02 (y-88 nm, delta -15) both confirm y-resizes are AUX.1-safe and do not produce AUX.3 bend violations.

Trial i03.ug.leaf_0003.02 applied a symmetric y-shrink to polygon p892: resize_end y low +32 nm paired with resize_end y high -32 nm. Symmetric inward y-resizes shorten a polygon's vertical extent while preserving its vertical center position. That trial also includes a p878 x+32 nm move (m5_fix group) and recorded 15 new in-crop violations with no per-rule breakdown available, so the y-shrink contribution to the violation count cannot be isolated.

## Connectivity Gating

All six trials in the measured history (iter 1–3) were decided as gated_in with conn_preserved: true (unit_gate channel) or applied (cu_pool channel). No trial was rejected for connectivity loss. Operations that move a polygon and all topologically connected instances as a coordinated group — as in trial i03.ug.leaf_0003.02, where polygon p878 and instances i0001, i0067, i0113 were all moved x+32 nm together under the "m5_fix" label — preserve connectivity by keeping all electrically connected elements displaced by the same delta.