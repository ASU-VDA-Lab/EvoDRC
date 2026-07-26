## V2 Repair Knowledge — Layer V2, Iteration 2

### Measured trial inventory

Four trials exist across iterations 1–2.

**Iteration 1:**
- trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 — single-op cu_pool; `conn_preserved = true`; `decision = rejected_net_positive`; `delta_total = 0`.
- trial:i01.ug.leaf_0034.12 — 10-op unit_gate; `conn_preserved = false`; `decision = gated_out`; `reason = conn_broken`.

**Iteration 2:**
- trial:i02.ug.leaf_0003.02 — 85-op unit_gate on Block1/leaf_0003; `conn_preserved = true`; `decision = gated_in`; introduces 6 new V2.M3.EN.2 violations among 80 total new in-crop violations; touched layers M2, M3, M4, M5, M6, V2, V3, V4, V5.
- trial:i02.ug.leaf_0004.03 — 41-op unit_gate on Block1/leaf_0004; `conn_preserved = true`; `decision = gated_in`; introduces 6 new V2.M3.EN.2 violations among 47 total new in-crop violations; touched layers M2, M3, M4, M5, M6, V2, V3, V4, V5.

### M3 y-axis shrink on VIA_VIA23_1_3_36_36 is ineffective

Shrinking M3 in the y-axis by 40 dbu (`resize_via_shape`, `axis = y`, `delta_dbu = -40`) on cell `VIA_VIA23_1_3_36_36` produced zero net DRC reduction (`delta_total = 0`) and was rejected (trial:i01.cu.def:VIA_VIA23_1_3_36_56.00). Do not re-issue this same operation on the same cell; the measured outcome is a no-op improvement against the V2 rule set.

### Combined move-and-resize sequences on VIA_VIA23_1_3_36_36 break connectivity

The 10-op sequence in trial:i01.ug.leaf_0034.12 combined the same M3 y-axis shrink with instance moves (up to `dx_dbu = 136`) and M3/M1 edge resizes on polygons p1178, p1214, p1255. The result was `conn_preserved = false`. Avoid pairing `resize_via_shape` on M3 (y, -40 dbu) for this cell with lateral instance translations on co-touched layers M1, M2, M3, M4, V1, V2; the connectivity breakage is measured and the gating is confirmed (trial:i01.ug.leaf_0034.12).

### Bulk M3 polygon displacement introduces new V2.M3.EN.2 violations

In trial:i02.ug.leaf_0003.02, M3 polygons p1143 and p1145 were moved +32 dbu in x, while p1142 and p1144 were moved −16 dbu in x, and polygons p1561/p1562/p1563 were moved −96/−112/−64 dbu in y. In trial:i02.ug.leaf_0004.03, polygons p1143 and p1142 were moved +32 and −16 dbu in x respectively, and p1561 was moved +32 dbu in y. Both trials simultaneously moved large numbers of V2-touching instances by different displacements (x: +32 or −16 dbu; y: 0, ±24, ±32, ±72, ±96, or −112 dbu). Both trials introduced exactly 6 new V2.M3.EN.2 violations as a side effect (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03). Rule V2.M3.EN.2 requires M3 to enclose V2 on two opposite sides by 5 & 5 nm or 5 & 0 nm; displacing M3 polygons without correspondingly adjusting all enclosed V2 boundaries reduces or eliminates that enclosure on the affected edges.

Both iteration-2 trials were `gated_in` because overall DRC improvement across other rules outweighed the 6 new V2.M3.EN.2 violations. The V2.M3.EN.2 violations were not repaired; they were generated as a secondary consequence of the broader M3/instance restructuring.

### Rule V2.M3.AUX.2 and V2.M3.EN.2 interaction with M3 sizing

Rule V2.M3.AUX.2 requires V2 to be exactly the same width as M3 along the direction perpendicular to M3 length. Rule V2.M3.EN.2 requires M3 to enclose V2 by 5 nm on two opposite sides (5 & 5 nm or 5 & 0 nm). The M3 y-shrink in iteration 1 reduces available M3 overlap with V2 perpendicularly, which is consistent with the zero-improvement result in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00. In iteration 2, x-axis and y-axis polygon moves that shift M3 shape boundaries without equivalently shifting V2 boundaries produce V2.M3.EN.2 enclosure failures on the displaced edges, as confirmed in both trial:i02.ug.leaf_0003.02 and trial:i02.ug.leaf_0004.03.

### Rule V2.AUX.1 interaction with instance moves

Rule V2.AUX.1 requires V2 to reside inside both M2 and M3. Trial:i01.ug.leaf_0034.12 moved multiple instances laterally (up to 136 dbu) while simultaneously resizing M3 edges; this broke connectivity. Moving via instances without correspondingly extending their enclosing M2 and M3 boundaries risks V2.AUX.1 violations in addition to connectivity loss, as evidenced by the gated-out outcome in trial:i01.ug.leaf_0034.12. In contrast, both iteration-2 trials moved instances with `conn_preserved = true`; V2.AUX.1 was not listed among the new violations, indicating the instance displacements used in trial:i02.ug.leaf_0003.02 and trial:i02.ug.leaf_0004.03 stayed within M2/M3 boundaries.

### Rule V2.W.1 — no positive evidence from current trials

Rule V2.W.1 mandates a minimum V2 width of 18 nm along M3 length. No measured trial produced a passing outcome that grounds a repair prescription for this rule. No width-increasing operation was attempted or confirmed effective in the current history.

### Rule V2.S.1 through V2.S.4 — no positive evidence from current trials

No trial in the current history produced a passing spacing fix for V2.S.1, V2.S.2, V2.S.3, or V2.S.4. The spacing rules (18 nm same-track, 27 nm parallel not-aligned, 23 nm corner-to-corner with end-cap, 30 nm corner-to-corner without end-cap, 27 nm mixed) are not yet grounded by a successful repair in this layer's history.

### Rule V2.M2.EN.1 — no positive evidence from current trials

Rule V2.M2.EN.1 requires M2 to enclose V2 by at least 5 nm on two opposite sides. No trial confirmed a repair for this rule; the current history does not support a prescriptive statement beyond what the rule text specifies.

### Summary of actionable negatives

- Do not apply `resize_via_shape` M3 y-axis −40 dbu to `VIA_VIA23_1_3_36_36` as a standalone fix; it yields zero DRC improvement (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).
- Do not combine that same M3 shrink with lateral instance moves on co-touched layers for this cell; connectivity is broken and the trial is gated out (trial:i01.ug.leaf_0034.12).
- Bulk M3 polygon displacement (x or y axis) applied without matching adjustment to all co-located V2 boundaries introduces new V2.M3.EN.2 violations; both measured bulk-restructuring trials produced 6 new V2.M3.EN.2 violations each despite being gated in on balance (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03).
- No iteration in this layer's history has confirmed a net-positive V2.M3.EN.2 repair; all V2.M3.EN.2 changes in the measured record are increases, not decreases.