Now I have all the data needed. Composing the knowledge section strictly from the three measured records.

---

## V2.M3.EN.2 Is the Only Rule Observed to Accumulate New Violations on M3

Across all three trials in the history, V2.M3.EN.2 is the sole DRC rule recorded as generating new in-crop violations that involve the M3 layer. In trial:i02.ug.whole_design.00, the per-rule breakdown reports 10 new in-crop V2.M3.EN.2 violations introduced by the unit_gate move set. No other M3-relevant rule (M3.W.1, M3.S.1–M3.S.6, M3.A.1, V2.M3.AUX.2, V3.M3.EN.1, M3.GEOMETRY.NONORTHOGONAL) appears in any violation count in the recorded history. Do not treat the absence of M3.S.*, M3.W.1, M3.A.1, and V3.M3.EN.1 findings as confirmed-clean: the history records no explicit clean sweep; those rules simply produced no entries in the deltas fields across any of the three trials.

## V2.M3.EN.2: Two-Sided Enclosure Requires 5 nm on Both Opposite Sides or 5 nm on One Side and 0 nm (Flush Edge) on the Other

The rule uses projection-mode enclosure checks in both horizontal and vertical directions. A V2 via is compliant only when M3 provides at least 5 nm of projection enclosure on one full pair of opposite edges (left+right or top+bottom). A flush condition on one side of a pair (0 nm extension, i.e., the M3 edge coincides with the V2 edge to within 1 dbu) satisfies the 5 & 0 nm option — the rule's second sub-check detects the case where the enclosure at projection is present on one side but absent (flush) on the other. Extend M3 to provide the required enclosure on at least one full axis; the orthogonal axis is unconstrained by this rule.

## Via Cell cu_pool Repair: Widen V2 in X to Satisfy M3 Enclosure

The only repair recorded as applied (decision: applied) across the history is trial:i02.cu.def:VIA_VIA23_1_3_36_36.00, a cu_pool operation targeting cell def:VIA_VIA23_1_3_36_36. That repair widened three V2 shapes in the x-direction by +288 dbu each while shifting them to rebalance their positions (shape_index 0 shifted x -144 then widened +288; shape_index 2 shifted x +144 then widened +288; shape_index 1 widened +288 in place). The touched layers were M2, M3, and V2. This 5-op set reduced the total design-wide violation count from 159 to 81, a delta of -78, and was the only trial accepted by the applied channel in the recorded history (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00).

The V2 shape expansions in that cell are X-axis symmetric: the outer two shapes are shifted outward by half the resize amount (144 dbu out, then widened 288 dbu) so the new outer edge displacement equals the full resize. Apply symmetric widening around the via array center when correcting V2.M3.EN.2 failures in a via cell with multiple shapes in a row — this is the pattern the solver applied in trial:i02.cu.def:VIA_VIA23_1_3_36_36.00.

## V2.M3.AUX.2 Constraint on Via Cell Repairs

V2.M3.AUX.2 requires V2 to match the M3 width exactly in the direction perpendicular to the M3 run direction (i.e., the V2 transverse width must equal the M3 transverse width, with V2 edges coinciding with M3 edges on both sides). In trial:i02.cu.def:VIA_VIA23_1_3_36_36.00 the V2 shapes were widened in X while M3 was also in the touched layer list, confirming that M3 must be co-adjusted when V2 shapes change width to keep V2.M3.AUX.2 satisfied. Do not resize V2 in a direction without ensuring the enclosing M3 edge tracks accordingly in that same direction.

## M3 Polygon Resize Operations Are Axis-Specific and May Be Partially Reversed Across Iterations

In trial:i02.ug.whole_design.00, three M3 polygons received resize_end operations extending the high x-end by +20 dbu each (p1831, p1786, p1806), with additional y-axis resize_end operations (p1831: y low +24; p1786: y high +72; p1806: y high +24). In trial:i05.ug.whole_design.00, the same three polygons (p1831, p1786, p1806) received resize_end operations of -20 dbu on the x-high end, exactly cancelling the x-axis extension from iter 2. The y-axis resize_end values applied in iter 2 were not reversed in iter 5. The net effect across both trials is that the x-extent of p1831, p1786, and p1806 returns to its pre-iter-2 state, while the y-extent retains the iter-2 changes (trial:i02.ug.whole_design.00, trial:i05.ug.whole_design.00).

This pattern demonstrates that x and y resize operations on the same polygon can be independently reverted. When diagnosing enclosure failures introduced by a unit_gate move, check whether a prior resize was subsequently reversed on only one axis — the remaining axis extension is still in effect.

## Unit-Gate Gating Criterion: Connectivity Preservation Overrides New In-Crop Violation Count

Both unit_gate trials in the history (trial:i02.ug.whole_design.00, trial:i05.ug.whole_design.00) were accepted with decision: gated_in despite the first introducing 10 new V2.M3.EN.2 violations per the per-rule breakdown. In both cases the gating reason recorded is conn_preserved, and n_new_out_of_crop remains 0. The unit_gate channel accepts a trial when connectivity is preserved and no new out-of-crop violations are produced, even when in-crop violations increase (trial:i02.ug.whole_design.00). Do not expect the unit_gate channel to block trials purely on the basis of new in-crop V2.M3.EN.2 counts; the cu_pool channel is the mechanism that resolves these violations separately, as seen in trial:i02.cu.def:VIA_VIA23_1_3_36_36.00.

## X-Axis Instance Moves Are the Dominant Operation Pattern on M3 in Both Accepted Trials

In trial:i02.ug.whole_design.00, M3-touching ops include x-axis moves of polygons p1682 (-16 dbu), p1683 (+32 dbu), and p1685 (+32 dbu), alongside y-axis moves of p2106 (-16 dbu), p2107 (+32 dbu), p2108 (+16 dbu), and p2109 (-64 dbu), plus a large set of instance moves with mixed x/y offsets. In trial:i05.ug.whole_design.00, all direct polygon moves on M3 are in the x-axis only, with magnitudes of 13, 37, 48, -72, and -161 dbu appearing across different polygon IDs (p2047 +48, p2072 +13, p2050 +37, p1911 +37, p2049 +37, p1903 +13, p1914 +37, p1907 +37, p2046 +37, p1927 +37, p1910 +37, p2067 +37, p2020 +13, p1946 +13, p2071 +13, p2030 +37, p2086 +13, p1999 -72, p2019 +13); thirteen additional instances were moved -12 dbu in x (trial:i05.ug.whole_design.00). The -161 dbu instance move on i0066 and the -72 dbu direct polygon move on p1999 in trial:i05.ug.whole_design.00 are the largest x displacements and represent outlier repositions relative to the cluster of +13 and +37 dbu moves.

## M3.S.6 Corner-to-Corner Spacing Requires 20 nm Euclidean, Not Projection

M3.S.6 uses euclidean distance, not projection, catching diagonal proximity that the projection-mode spacing rules miss. No violation of M3.S.6 appears in the history record. Moves in the recorded trials involve small x and y offsets (as small as ±13 dbu, i.e., ~1.3 nm at 0.1 nm/dbu, or ±16 dbu at 1.6 nm) on polygons that were already placed; the absence of M3.S.6 violations following these small moves is consistent with the design having sufficient corner-to-corner clearance before the trials began (trial:i02.ug.whole_design.00, trial:i05.ug.whole_design.00). No measured remediation of M3.S.6 exists in the history.

## Tip Spacing Rules Depend on Edge-Length Classification at 24 nm and 36 nm Thresholds

M3 tip-spacing rules stratify by edge length:

- M3.S.4 (31 nm, tip-to-tip, projection): both edges < 24 nm
- M3.S.5 (31 nm, tip-to-tip, projection): one edge 24–36 nm, one edge < 24 nm
- M3.S.3 (27 nm, tip-to-tip, projection): both edges 24–36 nm
- M3.S.2 (25 nm, tip-to-side, projection): one tip edge ≤ 36 nm, one side edge > 36 nm

The 36 nm boundary is the cutoff separating "tip" from "side" classification; the 24 nm boundary separates "narrow tip" from "wide tip." When resizing M3 polygon ends, crossing either threshold changes which spacing rule governs the resulting edge. In trial:i02.ug.whole_design.00, resize_end ops on p1831, p1786, and p1806 extended the x-high end by +20 dbu and moved y-ends; in trial:i05.ug.whole_design.00, the x-high +20 extension was reversed. No S.2/S.3/S.4/S.5 violations were reported across either trial, so these resizes did not cross a threshold that produced new violations in the measured history.

## All M3 Edges Must Remain Orthogonal

The NONORTHOGONAL block applies globally to M3. All ops in the recorded history are axis-aligned (move or resize_end on a single axis at a time), and no GEOMETRY.NONORTHOGONAL violations appear in any trial's delta records. Polygon moves and resize_end operations must remain strictly axis-aligned; diagonal displacements are not recorded and would violate M3.GEOMETRY.NONORTHOGONAL (trial:i02.ug.whole_design.00, trial:i05.ug.whole_design.00).