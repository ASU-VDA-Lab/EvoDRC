## V1 Repair Knowledge — Iteration 3

### Overview of V1 Violations Observed

Two V1 rules produced measured violations across the recorded history: V1.M2.EN.2 (M2 enclosure of V1) and V1.M1.EN.1 (M1 enclosure of V1). Both were triggered exclusively by Y-direction instance moves. No V1 violation was introduced by any X-direction move or by any M2 polygon resize_end operation.

---

### V1.M2.EN.2 — M2 Enclosure Sensitivity to Y-Displacement

V1.M2.EN.2 requires M2 to enclose V1 by at least 5 nm on two opposite sides (or by 5 nm and 0 nm). The rule checks enclosure via projection; a V1 instance that shifts in the Y direction relative to its parent M2 wire can exit the enclosure envelope on a projected edge.

A downward move of instance i0038 by [0, −44] dbu introduced 1 new V1.M2.EN.2 violation within the crop (trial:i02.ug.leaf_0008.04). The same instance had been moved by [+36, +44] in iteration 1 without any V1.M2.EN.2 violation (trial:i01.ug.leaf_0021.10), confirming that the positive-Y component in iteration 1 moved V1 further into the M2 enclosure rather than out of it. Reversing the Y direction to −44 dbu was sufficient to breach the enclosure minimum on at least one projected axis.

Do not apply negative-Y moves to instances that place V1 geometries near the Y-edge of their covering M2 wire. The enclosure margin consumed by a −44 dbu displacement was enough to create a violation (trial:i02.ug.leaf_0008.04); smaller negative displacements were not tested in isolation for this instance, so no safe floor for negative-Y is established from the records.

The assemble_drops mechanism dropped a conflicting op ([0, −44] on i0038) from a different unit before the trial executed (as recorded in trial:i02.ug.leaf_0008.04's assemble_drops log), yet the trial itself still introduced V1.M2.EN.2. This means conflict-dropping at the assembly stage does not prevent enclosure violations that arise from the remaining applied ops; the dropped op and the violation-producing op were independent moves of the same instance in different units.

---

### V1.M1.EN.1 — M1 Enclosure Sensitivity to Y-Displacement

V1.M1.EN.1 requires M1 to enclose V1 with at least 5 nm on one pair of opposite sides and 2 nm on the other pair; an instance that lacks a qualifying good-direction pair fails the rule. The rule fires per-via, not per-instance edge, which explains why a single instance move can produce multiple simultaneous violations.

A downward move of instance i0038 by [0, −36] dbu introduced 4 new V1.M1.EN.1 violations in one trial (trial:i02.ug.leaf_0013.06). The breadth — four violations from a single 36 dbu Y-displacement — indicates that instance i0038 contains multiple V1 shapes whose M1 enclosure on the Y-axis was already marginal before iteration 2. Moving the instance downward by 36 dbu pushed all four below the 2 nm floor on at least one axis.

The same instance was successfully moved by [+36, +44] in iteration 1 without V1.M1.EN.1 violations (trial:i01.ug.leaf_0021.10), confirming that upward Y displacement is safe for M1 enclosure whereas downward Y displacement is not.

Avoid negative-Y moves on instances whose V1 footprints are close to the bottom edge of M1. A displacement as small as −36 dbu is sufficient to produce four simultaneous V1.M1.EN.1 violations on instance i0038 (trial:i02.ug.leaf_0013.06).

---

### V1 Violations From Larger Y-Displacements (Iteration 3)

A move of [0, −64] dbu on instance i0038 in iteration 3 introduced 2 new in-crop violations (trial:i03.ug.leaf_0004.02). The per-rule breakdown is not present in this record, but the pattern of Y-direction displacement introducing V1-touching violations on this instance is consistent with the violations documented in trial:i02.ug.leaf_0008.04 and trial:i02.ug.leaf_0013.06. The trial was nonetheless accepted (gated_in, conn_preserved=true, n_new_out_of_crop=0).

---

### Safe Operations for V1: X-Direction Moves and Polygon Resize

All X-direction instance moves in the history produced zero new V1 violations, across a range of displacements including [+108, 0], [+96, 0], [+72, 0], [+36, 0], [+28, 0], [+12, 0], [−28, 0], [−36, 0], [−108, 0] dbu (trial:i01.ug.Block4_union_row1.00, trial:i01.ug.Block4_union_row10.01, trial:i01.ug.Block4_union_row2.02, trial:i01.ug.Block4_union_row5.04, trial:i01.ug.Block4_union_row6.05, trial:i01.ug.Block4_union_row7.06, trial:i02.ug.Block4_union_row1.00, trial:i02.ug.Block4_union_row3.02, trial:i02.ug.Block4_union_row10.01, trial:i03.ug.Block4_union_row7.00, trial:i03.ug.leaf_0001.01).

Resize_end operations on M2 polygons in the X direction are also safe for V1. A resize_end of +172 dbu on polygon p1395, +92 dbu on p1604, +52 dbu on p1595, and +16 dbu on p1551 each produced zero new V1 violations (trial:i01.ug.Block4_union_row7.06, trial:i01.ug.leaf_0008.08, trial:i02.ug.Block4_union_row7.03, trial:i02.ug.Block4_union_row10.01). Extending M2 in the X direction does not disturb V1 enclosure because V1.M2.EN.2 and V1.M1.EN.1 are evaluated by projection on the axis perpendicular to M2 length; adding length to M2 can only increase or maintain enclosure margin on that axis.

---

### Acceptance Behavior: gated_in Despite In-Crop V1 Violations

Every trial in the history was accepted (decision: gated_in). Trials that introduced V1 violations — specifically trial:i02.ug.leaf_0008.04 (1 V1.M2.EN.2) and trial:i02.ug.leaf_0013.06 (4 V1.M1.EN.1) and trial:i03.ug.leaf_0004.02 (2 unspecified) — were accepted because conn_preserved=true and n_new_out_of_crop=0. The gating criterion tolerates new in-crop violations when connectivity is preserved and no violations escape the crop boundary. New V1 violations that remain inside the crop and do not break connectivity do not block a trial from being committed.

This means operations that introduce V1 violations are not locally blocked by the harness, and the violations accumulate in the design state unless a subsequent repair operation resolves them. Prefer moves that introduce zero new V1 violations (all X-direction moves in the history qualify), and treat any operation with a negative-Y component on instances containing V1 geometry as requiring pre-verification of M1 and M2 enclosure margins on the Y axis.

---

### V1.W.1 and Spacing Rules: No Violations Observed

No violations of V1.W.1 (18 nm minimum width), V1.S.1 (spacing between V1 instances), V1.S.2 (5 nm end-cap corner-to-corner spacing), V1.S.3 (no-end-cap corner-to-corner spacing), V1.S.4 (mixed end-cap spacing), V1.AUX.1 (V1 inside M1 and M2), or V1.M2.AUX.2 (V1 width matches M2 width) were introduced in any trial across iterations 1–3. The repair operations applied — instance moves in X, instance moves in Y for units not containing i0038, and M2 polygon resize_end — did not produce violations of these rules. No prescriptive guidance on these rules can be grounded in the measured history beyond the observation that X-direction moves and M2 resize_end operations carry zero observed risk for them.