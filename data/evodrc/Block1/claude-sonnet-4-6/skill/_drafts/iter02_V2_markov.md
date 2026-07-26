## V2 Repair Knowledge — Layer V2, Iteration 2

### Measured trial inventory

Four trials exist across iterations 1 and 2.

**Iteration 1:**
- trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 — single-op cu_pool; `conn_preserved = true`; `decision = rejected_net_positive`; `delta_total = 0`.
- trial:i01.ug.leaf_0034.12 — 10-op unit_gate; `conn_preserved = false`; `decision = gated_out`; `reason = conn_broken`.

**Iteration 2:**
- trial:i02.ug.leaf_0003.02 — 85-op unit_gate on Block1, locus [1728,2068,14256,13680]; `conn_preserved = true`; `decision = gated_in`; introduced 80 new in-crop violations including `V2.M3.EN.2: 6`; touched layers M2, M3, M4, M5, M6, V2, V3, V4, V5.
- trial:i02.ug.leaf_0004.03 — 41-op unit_gate on Block1, locus [1728,3148,14256,14132]; `conn_preserved = true`; `decision = gated_in`; introduced 47 new in-crop violations including `V2.M3.EN.2: 6`; touched layers M2, M3, M4, M5, M6, V2, V3, V4, V5.

### Lateral M3 polygon moves without co-moving V2 create new V2.M3.EN.2 violations

Both iteration-2 trials applied x-axis moves to M3 polygons (p1143 +32 dbu, p1142 −16 dbu in both; p1145 +32 dbu, p1144 −16 dbu in trial:i02.ug.leaf_0003.02) while leaving V2 instances stationary. Each trial introduced exactly 6 new `V2.M3.EN.2` violations (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03). Rule V2.M3.EN.2 requires M3 to enclose V2 by 5 nm on two opposite sides (5 & 5 nm or 5 & 0 nm). Shifting the M3 boundary polygon laterally while V2 remains in place shrinks the M3 overhang on the retreating side below the 5 nm minimum. Do not move M3 polygons in the x-axis without correspondingly translating any V2 instances that share enclosure with that M3 edge.

### V2.M3.EN.2 new violations are introduced by large-scale instance sweeps that reposition M3 tracks

Trial:i02.ug.leaf_0003.02 moved 78 instances by [+32,0] or [−16,0] dbu (plus a diagonal subset by [+32,−64], [+32,−112], [+32,−96], [−16,−64], [−16,−112], [−16,−96] dbu). Trial:i02.ug.leaf_0004.03 moved 38 instances by [+32,y] or [−16,y] offsets (y ranging −72 to +72 dbu). Both operations touched V2 instances as part of the instance group. Despite `conn_preserved = true` in both, 6 new V2.M3.EN.2 violations appeared in each. The instance moves repositioned M3 track segments relative to V2 instances that were not included in the same move group, creating enclosure gaps. When bulk-sweeping instance columns, every V2 instance must either be included in the same displacement group as the M3 track it terminates on, or the M3 polygon must be extended to maintain ≥5 nm enclosure on both sides.

### gated_in does not mean V2-clean; iteration-2 trials were accepted at net cost to V2

Both iteration-2 trials have `decision = gated_in` because overall DRC improvement across all rules was positive, but each added 6 new V2.M3.EN.2 violations (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03). The gating mechanism accepts a trial when `conn_preserved = true` and `n_new_out_of_crop = 0` even if new in-crop violations appear. V2.M3.EN.2 violations introduced this way accumulate as debt; do not treat `gated_in` as evidence that V2.M3.EN.2 is resolved.

### M3 y-axis shrink on VIA_VIA23_1_3_36_36 is ineffective

Shrinking M3 in the y-axis by 40 dbu (`resize_via_shape`, `axis = y`, `delta_dbu = −40`) on cell `VIA_VIA23_1_3_36_36` produced zero net DRC reduction (`delta_total = 0`) and was rejected (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). Do not re-issue this operation on the same cell; the outcome is a no-op against the V2 rule set.

### Combined move-and-resize sequences on VIA_VIA23_1_3_36_36 break connectivity

The 10-op sequence in trial:i01.ug.leaf_0034.12 combined the M3 y-axis shrink (−40 dbu) with lateral instance moves (up to `dx_dbu = 136`) and M3/M1 edge resizes on polygons p1178, p1214, p1255. The result was `conn_preserved = false` and `decision = gated_out`. Avoid pairing `resize_via_shape` on M3 (y, −40 dbu) for this cell with lateral instance translations on co-touched layers M1, M2, M3, M4, V1, V2; the connectivity breakage is confirmed (trial:i01.ug.leaf_0034.12).

### Rule V2.M3.AUX.2 and V2.M3.EN.2 interaction with M3 sizing

Rule V2.M3.AUX.2 requires V2 to be exactly the same width as M3 perpendicular to M3 length. Rule V2.M3.EN.2 requires M3 to enclose V2 by 5 nm on two opposite sides. The iteration-1 M3 y-shrink trades one violation type for another rather than resolving the underlying enclosure deficit (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). The iteration-2 x-axis M3 polygon moves add new EN.2 violations by reducing M3 overhang on the side toward which M3 retreats (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03). Both axes of M3 sizing require simultaneous V2 repositioning or M3 extension to avoid creating new enclosure violations.

### Rule V2.AUX.1 interaction with instance moves

Rule V2.AUX.1 requires V2 to reside inside both M2 and M3. Trial:i01.ug.leaf_0034.12 moved multiple instances laterally (up to 136 dbu) while simultaneously resizing M3 edges and broke connectivity. Moving via instances without correspondingly extending enclosing M2 and M3 boundaries risks V2.AUX.1 violations in addition to connectivity loss, as evidenced by the gated-out outcome in trial:i01.ug.leaf_0034.12. The iteration-2 trials used smaller displacements (±16/±32 dbu x-axis) that preserved connectivity but still generated V2.M3.EN.2 debt, consistent with partial-but-insufficient M3 coverage of co-moved V2 instances (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03).

### Rule V2.W.1 — no positive evidence

Rule V2.W.1 mandates a minimum V2 width of 18 nm along M3 length. No trial in the current history produced a passing outcome that grounds a repair prescription for this rule.

### Rule V2.S.1 through V2.S.4 — no positive evidence

No trial in the current history produced a passing spacing fix for V2.S.1, V2.S.2, V2.S.3, or V2.S.4. The spacing rules (18 nm same-track, 27 nm parallel not-aligned, 23 nm corner-to-corner with end-cap, 30 nm corner-to-corner without end-cap, 27 nm mixed) are not grounded by a successful repair in this layer's history.

### Rule V2.M2.EN.1 — no positive evidence

Rule V2.M2.EN.1 requires M2 to enclose V2 by at least 5 nm on two opposite sides. No trial confirmed a repair for this rule.

### Summary of actionable negatives

- Do not apply `resize_via_shape` M3 y-axis −40 dbu to `VIA_VIA23_1_3_36_56` as a standalone fix; it yields zero DRC improvement (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).
- Do not combine that M3 shrink with lateral instance moves on co-touched layers for that cell; connectivity breaks and the trial is gated out (trial:i01.ug.leaf_0034.12).
- Do not move M3 polygons in the x-axis without co-moving every V2 instance whose M3 enclosure depends on the shifted edge; each displaced-only-M3 operation introduced 6 new V2.M3.EN.2 violations (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03).
- Do not treat `gated_in` as V2-clean; both iteration-2 trials were accepted while adding V2.M3.EN.2 debt (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03).