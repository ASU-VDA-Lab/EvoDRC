## V1 Violation Sources Observed in Measured History

### V1.M2.EN.2 — M2 Enclosure Violation from Y-Direction Instance Move

The single recorded V1.M2.EN.2 violation entered the crop in trial:i02.ug.leaf_0008.04. That trial performed a pure Y-axis displacement of instance i0038 by [0, -44] dbu. The violation count rose to 1 new in-crop violation attributed to V1.M2.EN.2. The trial was nonetheless gated_in because connectivity was preserved (conn_preserved=true, n_new_out_of_crop=0).

By contrast, all iteration-1 trials that touched V1 — including trial:i01.ug.leaf_0021.10, which moved instance i0038 by [36, +44] dbu (positive X and positive Y) — produced zero new V1.M2.EN.2 violations. The sign reversal in the Y component (negative vs. positive) between trial:i01.ug.leaf_0021.10 and trial:i02.ug.leaf_0008.04 coincides with the appearance of this enclosure violation.

V1.M2.EN.2 requires M2 to enclose V1 on two opposite sides by either 5 nm & 5 nm or 5 nm & 0 nm (projection). A negative-Y displacement of a V1-bearing instance can reduce the M2 enclosure on the lower edge below the required threshold while the upper edge remains adequate, producing exactly one enclosure failure per affected via. Do not move V1-bearing instances in the negative Y direction without verifying that M2 enclosure on the trailing side remains ≥ 5 nm on the projection axis: trial:i02.ug.leaf_0008.04 confirms this violation mode.

### V1.M1.EN.1 — M1 Enclosure Violations from Y-Direction Instance Move

Trial:i02.ug.leaf_0013.06 recorded 4 new in-crop V1.M1.EN.1 violations from a single move of instance i0038 by [0, -36] dbu. This is the largest single-trial V1 violation count in the measured history. The trial was gated_in (conn_preserved=true, n_new_out_of_crop=0) despite the 4 new enclosure failures.

V1.M1.EN.1 requires M1 to enclose V1 on two opposite sides with the larger enclosure ≥ 5 nm and the smaller ≥ 2 nm (projection). A -36 dbu (-9 nm) displacement in Y can simultaneously degrade M1 enclosure on the lower sides of multiple vias within the same instance, creating one failing via per under-enclosed edge pair. Four simultaneous V1.M1.EN.1 violations from a 36-dbu Y move (trial:i02.ug.leaf_0013.06) confirm that a single small instance displacement can produce a burst of enclosure failures when the instance contains multiple V1 shapes near the enclosure minimum.

No V1.M1.EN.1 violations were recorded in any iteration-1 trial. The earliest M1 enclosure failure appears only in iteration 2 when negative-Y moves were applied to this locus.

### Conflict Between Leaf Trials and its Effect on V1 Violations

Trial:i02.ug.leaf_0008.04 and trial:i02.ug.leaf_0013.06 each attempted to move instance i0038 and each dropped the other's operation as an external conflict (assemble_drops, reason: external_conflict_dropped). The assembler honored each trial's own move but discarded the conflicting move from the other trial. As a result, each trial applied only its own displacement to i0038 in isolation, and the V1 violations recorded in each trial reflect the effect of that single move without the compensating move from the other trial. Do not infer that the two moves are additive or canceling: trial:i02.ug.leaf_0008.04 shows [0, -44] producing V1.M2.EN.2, and trial:i02.ug.leaf_0013.06 shows [0, -36] producing V1.M1.EN.1, each independently.

### X-Axis Instance Moves: No V1 Violations Observed

Every trial in iterations 1 and 2 that applied only X-axis instance moves produced zero new V1 violations. This holds across a wide range of X displacements:

- trial:i01.ug.Block4_union_row1.00: [36, 0] dbu — 0 new V1 violations
- trial:i01.ug.Block4_union_row5.04: multiple moves including [37, 0], [-36, 0] — 0 new V1 violations
- trial:i01.ug.Block4_union_row6.05: three moves of [36, 0] — 0 new V1 violations
- trial:i02.ug.Block4_union_row1.00: [72, 0] and [36, 0] — 0 new V1 violations
- trial:i02.ug.Block4_union_row3.02: [-28, 0] — 0 new V1 violations
- trial:i02.ug.Block4_union_row7.03: [108, 0] plus a resize_end — 0 new V1 violations

X-axis instance moves at the displacements recorded here do not produce V1 enclosure, spacing, or width violations when the V1 shapes ride inside their instances. This is consistent with V1 rules that gate enclosure on opposite-side projection and with M2 tracks running along the X axis (the length direction), so an X-axis shift moves V1 along the M2 track without changing the cross-track enclosure margins.

### Polygon-Level Operations: No V1 Violations Observed

Several trials combined instance moves with polygon-level resize_end or axis-move operations on M2 polygons (e.g., trial:i01.ug.Block4_union_row7.06 resized p1395 by +172 dbu; trial:i01.ug.leaf_0008.08 resized p1604 by +92 dbu; trial:i02.ug.Block4_union_row10.01 resized p1551 high end by +16 dbu). None of these produced new V1 violations. Extending M2 polygons in the X direction at the magnitudes recorded does not create V1 violations, consistent with V1.M2.AUX.2 (V1 width must match M2 in the perpendicular direction, not the length direction) and V1.M2.EN.2 (enclosure measured by projection across the via, not along the track).

### Rules with No Violations in Measured History

The following V1 rules have no recorded violations across all 15 trials in iterations 1 and 2: V1.W.1 (minimum width 18 nm), V1.S.1 (minimum spacing, same and parallel tracks), V1.S.2 (corner-to-corner spacing with 5 nm end-cap, euclidian), V1.S.3 (corner-to-corner spacing without end-cap, euclidian), V1.S.4 (mixed end-cap spacing, euclidian), V1.AUX.1 (V1 must be inside M1 and M2), V1.M2.AUX.2 (V1 width matches M2 perpendicular width), and the GEOMETRY.NONORTHOGONAL rule for V1. The absence of these violations in the measured record does not license ignoring them; it means the operations applied so far (instance moves and M2 end extensions along X) have not disturbed spacing, width, or alignment constraints on V1.

### Summary of V1-Specific Repair Guidance

Negative Y-direction displacement of V1-bearing instances is the sole repair action in the measured history that produced V1 violations: trial:i02.ug.leaf_0008.04 (V1.M2.EN.2, 1 violation, [0, -44] dbu move) and trial:i02.ug.leaf_0013.06 (V1.M1.EN.1, 4 violations, [0, -36] dbu move). Both trials were gated_in because conn_preserved=true took priority over the new in-crop violations, so the violations entered the design state. Future iterations targeting this locus must account for these 5 pre-existing V1 enclosure violations (1 M2.EN.2 + 4 M1.EN.1) introduced in iteration 2. X-axis instance moves and M2 polygon X-extensions at the magnitudes in this history are safe with respect to all V1 rules.