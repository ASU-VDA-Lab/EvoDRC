**V2.W.1 — Minimum width**

V2 must be at least 18 nm wide along the M3 length direction. The deck enforces this with a direct width check; no measured trial has probed this constraint in isolation, so all fixes must verify the resulting via width independently.

**V2.S.1 — Spacing thresholds depend on M3 end-cap classification**

Spacing between V2 instances is not a single value. The deck computes two mask geometries—one for VIAs whose edges are fully coincident with M3 edges (NEC, no end-cap) and one for all others (WEC, with end-cap)—then enforces three thresholds: 18 nm on the same M3 track, 27 nm between parallel non-aligned tracks, and 18 nm between parallel aligned tracks. Correctly classifying each V2 as NEC or WEC before selecting a repair target is necessary, because a fix that satisfies a WEC–WEC spacing may violate a NEC–NEC or mixed-pair rule.

**V2.S.2, V2.S.3, V2.S.4 — Corner-to-corner euclidean checks**

The deck applies euclidean distance checks specifically to corner-to-corner proximity between V2 instances, filtered to exclude pairs that also have a projection violation. V2.S.2 requires 23 nm corner-to-corner between two WEC instances (euclidean check value 16.4 nm). V2.S.3 requires 30 nm corner-to-corner between two NEC instances (euclidean check value 16.12 nm). V2.S.4 requires 27 nm corner-to-corner between a WEC and a NEC instance (euclidean check value 17.11 nm). Spacing repairs that satisfy the projection threshold may still leave corner violations active.

**M3 y-axis resize does not reduce V2 spacing violations**

In trial:i02.cu.def:VIA_VIA23_1_3_36_36.00, a resize_via_shape operation on the M3 shape within cell VIA_VIA23_1_3_36_36, shrinking the y-axis by 40 dbu, produced delta_total=0 across both measurement windows (unit:leaf_0014 remained at 175 violations, unit:leaf_0015 remained at 113 violations). The trial was rejected as net-positive. Do not use M3 y-axis resize alone to close V2 spacing violations; the v2_mask geometry underlying V2.S.1 is computed from coincident M3 edges, so adjusting M3 shape dimensions without repositioning the V2 relative to other V2 instances leaves the mask-derived spacing unchanged (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00).

**Instance moves in x at ±36 dbu preserve connectivity and do not introduce new V2-layer violations**

In trial:i04.ug.leaf_0002.01, moving instance i0452 by −36 dbu in x within unit leaf_0002 was accepted (decision: gated_in) with conn_preserved=true and n_new_in_crop=0, n_new_out_of_crop=0 on touched layers M2/M3/V2. In trial:i05.ug.leaf_0002.01, moving instance i0451 by +36 dbu in x in the same unit was accepted under the same conditions. Apply instance moves in the x-direction within leaf_0002 with confidence that ±36 dbu displacements do not break connectivity or generate new V2 violations at this locus (trial:i04.ug.leaf_0002.01, trial:i05.ug.leaf_0002.01).

**V2.AUX.1 — Hard containment inside M2 ∩ M3**

V2 must lie entirely inside both M2 and M3. The deck checks this as v2.not_inside(m2 & m3). The two instance move trials (trial:i04.ug.leaf_0002.01, trial:i05.ug.leaf_0002.01) both preserved this constraint (conn_preserved=true, no new violations), confirming that ±36 dbu x-moves of these instances kept all V2 shapes within their enclosing M2 and M3 boundaries. Any repair that shifts a V2 or its parent instance must verify containment after the move; the M3 y-axis resize in trial:i02.cu.def:VIA_VIA23_1_3_36_36.00 also left containment intact (delta_total=0 indicates no new AUX.1 violations were introduced).

**V2.M3.AUX.2 — V2 width must exactly match M3 width perpendicular to M3 length**

The deck requires that V2 width along the axis perpendicular to M3 length exactly equals the M3 width along that axis. This is a coincidence constraint, not a minimum: both undersized and oversized V2 shapes relative to M3 fail. Because the M3 y-axis resize in trial:i02.cu.def:VIA_VIA23_1_3_36_36.00 produced zero delta, the resize either left the V2-to-M3 width relationship intact or the violation set did not include V2.M3.AUX.2 in that locus. Do not resize M3 on an axis that governs V2.M3.AUX.2 without simultaneously adjusting V2 width to match (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00).

**V2.M2.EN.1 — M2 must enclose V2 by at least 5 nm on two opposite sides**

The deck checks this by testing whether V2 extends beyond M2 sized inward by 5 nm on each axis. The two instance move trials (trial:i04.ug.leaf_0002.01, trial:i05.ug.leaf_0002.01) introduced no new violations on touched layers including M2 and V2, confirming that the ±36 dbu x-moves maintained adequate M2 enclosure. Repairs that move V2 or its parent instance in x must verify that M2 enclosure on the horizontal opposite sides remains ≥5 nm.

**V2.M3.EN.2 — M3 must enclose V2 by 5 & 5 nm or 5 & 0 nm on opposite sides**

The deck identifies failing V2 instances by checking whether all four of their edges have at least one opposite-pair direction with ≥5 nm M3 enclosure. The M3 y-axis resize in trial:i02.cu.def:VIA_VIA23_1_3_36_36.00 did not change the violation count, indicating that reducing M3 in y by 40 dbu did not create or resolve V2.M3.EN.2 violations at that locus. The instance moves in trial:i04.ug.leaf_0002.01 and trial:i05.ug.leaf_0002.01 also left enclosure intact. Any repair moving V2 relative to M3 must maintain the 5 & 5 nm or 5 & 0 nm enclosure on two opposite sides.

**NONORTHOGONAL — All V2 edges must be axis-aligned**

V2 edges at any angle other than 0° or 90° trigger a GEOMETRY.NONORTHOGONAL violation. No repair operation on V2 shapes should produce diagonal edges. The resize and move operations observed in the history (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00, trial:i04.ug.leaf_0002.01, trial:i05.ug.leaf_0002.01) all operated on rectangular via shapes and instance placements on a grid, preserving orthogonality.