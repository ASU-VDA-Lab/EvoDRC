The measured history for layer V2 at iteration 2 contains exactly two trials. Every prescriptive claim below is grounded in those records.

## Repair Outcome Summary

Two trials have touched V2 in this layer's history. Neither trial directly targeted a V2 DRC violation as its primary objective; V2 appeared in `touched_layers` as a side-effect of M3 reshape and instance-movement operations.

---

## V2.W.1 — Minimum Width Along M3 Length (18 nm)

Rule V2.W.1 requires each V2 shape to be at least 18 nm wide measured along the M3 run direction.

In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 the attempted repair was a `resize_via_shape` on the M3 shape of cell `VIA_VIA23_1_3_36_36` with axis=y, delta_dbu=-40 (shrinking the M3 shape by 40 dbu in the y direction). The trial was rejected with decision `rejected_net_positive` and delta_total=0: the violation counts in both sampled windows remained unchanged (88 and 35 respectively). Do not shrink the M3 shape of a via cell along the axis perpendicular to M3 length to resolve width violations; this operation produced no DRC improvement for V2 (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

---

## V2.S.1 — Minimum Projection Spacing (18/27/18 nm by Track Relationship)

Rule V2.S.1 enforces projection-based minimum spacing between V2 mask shapes. The spacing values depend on the spatial relationship between the via pairs relative to M3 tracks: same M3 track and parallel aligned cases require 18 nm; parallel not-aligned cases require 27 nm.

No trial in the current history records a repair that directly targeted a V2.S.1 violation. Trial:i02.ug.leaf_0003.02 moved instances horizontally (delta_dbu=[-8,0] and [-36,0]) and touched V2, and was gated in with 2 new violations appearing in crop. Do not assume that horizontal instance shifts resolve V2.S.1 spacing violations; trial:i02.ug.leaf_0003.02 shows that such moves can introduce new violations into the crop region rather than eliminate existing ones.

---

## V2.S.2, V2.S.3, V2.S.4 — Corner-to-Corner Euclidean Spacing

These rules govern diagonal (euclidean) minimum spacing between V2 mask shapes depending on M3 end-cap status:

- V2.S.2: both vias have 5 nm M3 end-cap → 23 nm euclidean
- V2.S.3: neither via has 5 nm M3 end-cap → 30 nm euclidean
- V2.S.4: one via with and one without 5 nm M3 end-cap → 27 nm euclidean

No trial in the current history records a repair directly targeting V2.S.2, V2.S.3, or V2.S.4. These rules are not grounded by successful or failed repair attempts in the available measured records.

---

## V2.M2.EN.1 — M2 Enclosure of V2 (5 nm on Two Opposite Sides)

Rule V2.M2.EN.1 requires M2 to enclose V2 by at least 5 nm on at least two opposite sides.

In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 the operation touched M2 (listed in `touched_layers`) as part of a via-cell M3 reshape. The repair was rejected with no net improvement. Resizing the via shape along the M3 y-axis without a corresponding M2 adjustment did not satisfy enclosure requirements (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). Any operation that reshapes V2 or its parent via cell must preserve or increase M2 enclosure on the two opposite sides.

---

## V2.M3.EN.2 — M3 Enclosure of V2 (5&5 nm or 5&0 nm on Opposite Sides)

Rule V2.M3.EN.2 requires M3 to enclose V2 by at least 5 nm on one pair of opposite sides, with either 5 nm or 0 nm (flush) on the perpendicular pair.

In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 the M3 shape of the via cell was shrunk by 40 dbu in the y-axis (delta_dbu=-40, axis=y). This operation touched M3 and V2 but produced delta_total=0; the enclosure relationship between V2 and M3 was not improved. Do not shrink M3 in the direction that reduces enclosure on an already-marginal side (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

---

## V2.AUX.1 — V2 Must Be Inside M2 and M3

Rule V2.AUX.1 flags any V2 shape not fully inside the intersection of M2 and M3. This is a containment prerequisite; any operation that moves a via cell or resizes M2 or M3 independently risks violating this rule.

Trial:i02.ug.leaf_0003.02 moved instances horizontally (two separate `move_instance` ops with delta_dbu=[-8,0] and [-36,0]) while touching V2, and was accepted (`gated_in`) with 2 new violations appearing in the crop region. Instance movements that shift a via cell but do not correspondingly adjust M2 and M3 boundaries can cause V2 to exit the M2∩M3 intersection, introducing V2.AUX.1 violations; this is consistent with the 2 new in-crop violations observed in trial:i02.ug.leaf_0003.02.

---

## V2.M3.AUX.2 — V2 Width Must Match M3 Width Perpendicular to M3 Length

Rule V2.M3.AUX.2 requires V2 to have exactly the same dimension as M3 in the direction perpendicular to M3's run direction; no part of V2 may protrude beyond M3, and V2 must not be narrower than M3 in that axis.

In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, shrinking the M3 y-extent by 40 dbu without a matching resize of the V2 shape would change the perpendicular-to-length width of M3 relative to V2. This operation yielded delta_total=0 and was rejected (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). Never resize the M3 shape of a via cell without simultaneously resizing the enclosed V2 shape to maintain exact width match perpendicular to M3 length.

---

## GEOMETRY.NONORTHOGONAL — All V2 Edges Must Be Orthogonal

The nonorthogonal block flags any edge on V2 with an angle outside {0°, 90°, 180°, 270°}. No trial in the current history records a nonorthogonal violation on V2 or a repair targeting one. All shape modifications (resize, via shape ops) recorded in the history used axis-aligned deltas (axis=x or axis=y with integer dbu values), consistent with keeping V2 geometry orthogonal. Never introduce diagonal or angled edges when creating or modifying V2 shapes.

---

## Operation-Type Observations Grounded in Measured History

**`resize_via_shape` on M3 (axis=y, shrink):** Observed in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00. Outcome: rejected, delta_total=0. This operation class produced no DRC improvement for V2 in the single measured instance.

**`move_instance` (horizontal, axis=x):** Observed in trial:i02.ug.leaf_0003.02 (two moves: -8 dbu and -36 dbu). Outcome: gated_in with 2 new in-crop violations. Instance moves that shift via-containing cells horizontally can introduce new V2 violations in the crop region even when connectivity is preserved.

**`resize_end` on M1 polygon:** Observed in trial:i02.ug.leaf_0003.02. Touched V2 as a downstream layer. New V2 violations appeared in crop (trial:i02.ug.leaf_0003.02). M1 end resizes in a unit cell propagate effects upward to V2 through the instance stack; inspect V2 spacing and enclosure rules after any M1 end adjustment.