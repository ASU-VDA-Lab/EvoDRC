**M4.W.5 is the only M4 rule recorded as newly introduced across this block's history**

M4.W.5 (minimum horizontal width 44 nm) is the sole M4-specific rule appearing in any `new_in_crop_by_rule` field in this layer's measured history. Trial trial:i03.ug.leaf_0002.01 introduced 2 M4.W.5 violations when four instances (i0114, i0112, i0073, i0062) were each shifted −32 dbu in x simultaneously. The direction of the shift — compressing the x-extent of M4 wire ends that were already near the 44 dbu minimum — caused the violations. Avoid applying uniform negative-x multi-instance shifts to clusters that contain near-minimum horizontal M4 wire ends without first checking that resulting horizontal extents remain ≥44 dbu (trial:i03.ug.leaf_0002.01).

**Positive-x shifts of 32 dbu have not introduced M4.W.5 or any other M4 violation**

Trials trial:i02.ug.leaf_0002.01, trial:i03.ug.leaf_0003.02, and trial:i04.ug.leaf_0001.00 each applied +32 dbu x-moves to M4-touching instances or polygons without introducing M4-specific violations. When horizontal M4 segments are being extended outward (positive shift on the leading end), M4.W.5 risk is absent; the risk appears when shifts compress existing horizontal extents (trial:i03.ug.leaf_0002.01).

**Y-axis moves use 24 dbu multiples; no M4.AUX.1 violations observed**

Trial trial:i01.ug.leaf_0010.07 applied y-axis instance moves of ±72 dbu and ±24 dbu across M4-touching instances. No M4.AUX.1 (horizontal edge on 24 nm grid) violations were reported. All observed y-deltas across the full history — 24, 48, 72, 96 dbu — are exact multiples of 24 dbu, consistent with the M4.AUX.1 grid requirement and the M4.W.1 minimum vertical width of 24 nm.

**Symmetric y-resize (shrink from both ends) on an M4 polygon did not introduce M4.W.3 or M4.W.4 violations**

Trial trial:i03.ug.leaf_0003.02 applied a paired resize to polygon p892: low end moved +32 dbu (upward), high end moved −32 dbu (downward), reducing total height by 64 dbu. No M4.W.3 (even-integer multiples of 24 nm forbidden) or M4.W.4 (widths 72, 168, 264, 360, 456 nm forbidden) violations were recorded for that trial. The post-resize height landed on a legal value. Both resize endpoints were moved in equal magnitude, preserving any M4.AUX.1 horizontal-edge alignment provided both original edges were already on the 24 dbu grid (trial:i03.ug.leaf_0003.02).

**cu_pool via-def y-resize affects M4 as a touched layer**

Trial trial:i02.cu.def:VIA_VIA45_1_2_58_58.02 resized the M5 enclosure shape inside via cell definition VIA_VIA45_1_2_58_58 by −88 dbu in y; M4 is listed as a touched layer alongside M5 and V4. This single cu_pool operation reduced violations by 15 net (leaf_0002: −9, leaf_0003: −6). M4 exposure in via-def resizes arises because the V4 via sits between M4 and M5, and its M4 land must satisfy V4.M4.EN.1 (minimum 11 nm enclosure on at least two opposite sides). Verify V4.M4.EN.1 enclosure on M4 lands after any cu_pool via-def y-resize that shrinks the M5 shape (trial:i02.cu.def:VIA_VIA45_1_2_58_58.02).

**Polygon p879 was dropped at assemble due to cu_pool reservation; re-attempted successfully in iteration 4**

In trial trial:i02.ug.leaf_0002.01, a +32 dbu x-move on polygon p879 was listed in `assemble_drops` with reason `reserved_by_cu_pool_winner`. The same move — +32 x on p879 — was applied without conflict in trial trial:i04.ug.leaf_0001.00 in iteration 4. The cu_pool operation that reserved p879 (trial:i02.cu.def:VIA_VIA45_1_2_58_58.02, decision `applied`) was committed before iteration 4, freeing the polygon for unit_gate re-attempt. Do not abandon unit_gate moves on polygons dropped for `reserved_by_cu_pool_winner`; requeue them after the cu_pool round commits (trial:i02.ug.leaf_0002.01, trial:i04.ug.leaf_0001.00).

**external_duplicate drops in the assembled cluster do not prevent remaining M4 moves, but M4.W.5 exposure must be reassessed on the surviving subset**

Trial trial:i03.ug.leaf_0002.01 dropped the move of instance i0073 by [−32, 0] (reason: `external_duplicate`, claimed by both leaf_0001 and leaf_0002). The remaining three moves — i0114, i0112, i0062, each −32 x — were applied and produced 2 M4.W.5 violations. When a duplicate-conflicted M4-touching instance move is dropped at assemble, the surviving cluster still executes and can introduce M4.W.5 violations; re-evaluate M4.W.5 exposure on the actual applied subset, not the originally proposed full set (trial:i03.ug.leaf_0002.01).

**All M4 polygon operations in the history are straight-segment moves or single-axis end-resizes; M4.AUX.3 (no bends) is preserved**

Every M4 polygon operation across all trials is either a full translate (`move` with x- or y-delta) or a single-axis `resize_end` targeting one edge at a time. No operation simultaneously modified both x and y extents of the same M4 polygon in a way that could introduce corner geometry. M4.AUX.3 prohibits any bend in M4; do not combine x- and y-resize operations on the same polygon in a single step unless the polygon remains a simple rectangle with four orthogonal corners (trial:i03.ug.leaf_0003.02, trial:i03.ug.leaf_0001.00).

**V3.M4.EN.2 and V3.M4.AUX.2 constraints apply when V3 and M4 are co-touched**

Trials trial:i01.ug.leaf_0010.07 and trial:i02.ug.leaf_0002.01 both list V3 and M4 as touched layers. V3.M4.EN.2 requires ≥11 nm M4 enclosure of V3 on at least two opposite sides; V3.M4.AUX.2 requires V3 to be exactly the same width as M4 perpendicular to M4's length direction. Neither V3.M4.EN.2 nor V3.M4.AUX.2 appears as a newly introduced violation in those trials' per_rule fields (where per_rule is recorded), consistent with the moves being snapped to legal M4-track increments. When moving M4 relative to a V3 via, verify that the resulting enclosure on both transverse sides remains ≥11 dbu (trial:i01.ug.leaf_0010.07, trial:i02.ug.leaf_0002.01).