## M3.S.2 — Tip-to-Side Spacing (25 nm minimum)

M3.S.2 violations arise when a short tip edge (<=36 nm) approaches a long side edge (>36 nm) with less than 25 nm projected separation. Two violations (v0014 and v0015) were present entering iteration 3 and were cleared by endpoint-shrink operations in trial:i03.ug.leaf_0003.02. Two new M3.S.2 violations were introduced in trial:i01.ug.leaf_0035.13 (per_rule new_in_crop M3.S.2: 2) by uniform y-axis shrinks of 64 dbu applied to 12 M3 polygons; those shrinks reduced polygon height and exposed tip edges that had previously been covered by longer side edges. Two additional M3.S.2 violations were introduced in each of trial:i02.ug.leaf_0003.02 and trial:i02.ug.leaf_0004.03 (per_rule M3.S.2: 2 in each) by lateral via-instance moves of 32 dbu and -16 dbu that shifted M3 landing pads relative to adjacent M3 geometry.

**Fix pattern — shrink the high end of the M3 polygon:** For v0014, the right edge of polygon p1543 was moved from x=13876 to x=13868 (resize_end, axis=x, end=high, delta_dbu=-8), opening the projected gap to the neighboring polygon left edge at x=13968 to exactly 100 dbu = 25 nm (trial:i03.ug.leaf_0003.02). The polygon width remained at 72 dbu = 18 nm, preserving M3.W.1 compliance.

**Two-part fix when a VIA23 land shares the resized edge:** For v0015, shrinking the right edge of p1458 by 8 dbu was insufficient alone because VIA_VIA23_1_3_36_36 instance i0180 carried an M3 land whose right edge would otherwise protrude beyond the resized polygon boundary. The complete fix paired the polygon resize with a dx=-40 dbu move of instance i0180, so that the VIA23 M3 land right edge also landed at x=3068, co-located with the resized polygon right edge (trial:i03.ug.leaf_0003.02). Both ops were tagged group="m3s2_left" in that trial.

Do not apply a single-polygon endpoint shrink for M3.S.2 when a VIA23 instance's M3 land shares that edge; both the polygon and the VIA23 instance must be adjusted together, as demonstrated in trial:i03.ug.leaf_0003.02.

## V2.M3.EN.2 — V2 Enclosure by M3 (5 nm on two opposite sides)

V2.M3.EN.2 violations are introduced by lateral x-axis shifts of via-instance stacks that carry M3 landing pads. Both trial:i02.ug.leaf_0003.02 and trial:i02.ug.leaf_0004.03 each introduced 6 new V2.M3.EN.2 violations (per_rule new_in_crop V2.M3.EN.2: 6 in each) following instance moves of ±32 dbu and ±16 dbu in x on VIA stacks that touch M3.

**Shrinking the VIA23 M3 via shape does not resolve V2.M3.EN.2:** The cu_pool trial i01.cu.def:VIA_VIA23_1_3_36_36.00 proposed resize_via_shape axis=y delta=-40 dbu on the M3 shape of cell VIA_VIA23_1_3_36_36 and was rejected with decision=rejected_net_positive (delta_total=0; violation counts in unit:leaf_0034 and unit:leaf_0035 both unchanged). Reducing the M3 landing pad in that direction fails to restore enclosure margin.

**Growing the VIA23 M3 via shape reduces V2.M3.EN.2 violations:** The cu_pool trial i03.cu.def:VIA_VIA23_1_3_36_36.00 applied resize_via_shape axis=y delta=+24 dbu on the M3 shape of the same cell (alongside +64 dbu grows on the three V2 shapes and the M2 shape) and received decision=applied, reducing the violation count in unit:leaf_0002 from 93 to 81 (delta=-12, trial:i03.cu.def:VIA_VIA23_1_3_36_36.00). The M3 shape grow was assembled as part of a coordinated multi-shape grow; the delta=-40 attempt was tried and failed before the delta=+24 attempt succeeded.

## V2.M3.AUX.2 — V2 Width Must Match M3 Width

When resizing the endpoint of an M3 polygon that contains embedded V2 cuts, verify that all V2 cut edges remain strictly inside the new M3 boundary. In trial:i03.ug.leaf_0003.02, the right edge of p1543 was moved inward from x=13876 to x=13868; the rightmost V2 cut edge inside p1543 was at x=13860, which is less than 13868, so V2.M3.AUX.2 alignment was preserved. An endpoint resize that moves the M3 boundary inward past any existing V2 edge would violate V2.M3.AUX.2. Always check the positions of V2 edges relative to the intended new M3 boundary before committing a resize_end operation.

## VIA_VIA23_1_3_36_36 Cell-Level M3 Shape Sizing

The cu_pool channel processes VIA_VIA23_1_3_36_36 def-level resizes independently from unit-level fixes. Measured outcomes for the M3 shape of this cell:

- axis=y, delta=-40 dbu: decision=rejected_net_positive, delta_total=0 (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). This same -40 dbu op was also proposed and dropped (reason=cu_pool:rejected_net_positive) inside the unit-gate trial:i01.ug.leaf_0034.12 before being submitted to cu_pool directly.
- axis=y, delta=+24 dbu: decision=applied, delta_total=-12 (trial:i03.cu.def:VIA_VIA23_1_3_36_36.00). This grow was accompanied by +64 dbu y-grows on three V2 shapes and the M2 shape of the same cell.

The M3 shape must grow (positive delta) to improve V2.M3.EN.2 enclosure in this cell; negative-delta shrinks of this shape produce no violation reduction.

## Connectivity Risk from Large M3 Endpoint Resizes

Trial:i01.ug.leaf_0034.12 received decision=gated_out with reason=conn_broken and reported 89 new in-crop violations. That trial's M3 operations included resize_end on p1178 with delta_dbu=+192 and on p1255 with delta_dbu=+100, alongside instance moves across M1, M2, M3, M4, V1, and V2. The combination of large polygon extensions and concurrent instance moves broke routing connectivity. The successful M3 endpoint resizes in trial:i03.ug.leaf_0003.02 used delta_dbu=-8 (2 nm) and are the only M3 endpoint resizes that were accepted across all gated-in trials in this history. Apply large positive endpoint deltas on M3 with caution; trial:i01.ug.leaf_0034.12 demonstrates that +192 dbu and +100 dbu endpoint extensions in a multi-layer op set result in connectivity breakage.

## Cross-Crop Polygon Conflict Resolution for M3

M3 polygons that span a crop boundary are claimed by both neighboring leaves. When two leaves propose conflicting moves for the same polygon, the first-committed leaf's op is accepted and the second is dropped with reason=cross_crop_first_wins. In iteration 2, polygons p1143, p1142, and p1561 were contested by leaf_0003 and leaf_0004. Leaf_0003 committed first; leaf_0004's proposals for those three polygons were dropped (trial:i02.ug.leaf_0004.03 assemble_drops, reason=cross_crop_first_wins). The operations that survived for those polygons were: p1143 +32 dbu in x, p1142 -16 dbu in x, p1561 -96 dbu in y (trial:i02.ug.leaf_0003.02). Instance moves for the same via instance claimed by both leaves are dropped with reason=external_conflict_dropped when the proposed delta vectors differ between leaves, even if both share the same base direction (trial:i02.ug.leaf_0004.03).

## M3.W.1 — Minimum Width Constraint at 18 nm

No M3.W.1 violations were introduced in any gated-in trial. The y-axis resize of -64 dbu (16 nm) applied to 12 M3 polygons in trial:i01.ug.leaf_0035.13 did not generate M3.W.1 violations, indicating those polygons had pre-shrink height well above 18 nm. The endpoint shrink in trial:i03.ug.leaf_0003.02 produced a polygon (p1543) with remaining width of exactly 72 dbu = 18 nm, confirmed in the op comment. No further width reduction on p1543 can be applied without violating M3.W.1.

## Instance-Move Magnitudes Accepted on M3 Stacks

All via-instance moves that touch M3 and were accepted (gated_in) used the following magnitudes: 16 dbu, 32 dbu, 40 dbu, 48 dbu, 64 dbu, 72 dbu, 96 dbu, and 112 dbu. The most frequent pattern is ±32 dbu or -16 dbu in the x-axis (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03, trial:i04.ug.leaf_0003.02). The 48 dbu and 96 dbu y-axis moves in trial:i04.ug.leaf_0002.01 and the 112 dbu y-axis instance move in trial:i02.ug.leaf_0003.02 were all accepted without introducing new M3-specific violations. The 40 dbu x-axis move of instance i0180 in trial:i03.ug.leaf_0003.02 was part of the coordinated M3.S.2 fix.