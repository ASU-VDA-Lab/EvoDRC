**M3.S.2 and M3.S.4 Violation Mechanism: Bulk Y-Resize**

The only measured M3 spacing violations arose from a single bulk operation in trial:i02.ug.leaf_0045.20, where 39 M3 polygons each received a symmetric y-resize of -64 dbu simultaneously. That trial reported 10 new M3.S.2 violations (tip-to-side, 25 nm minimum) and 1 new M3.S.4 violation (narrow-tip-to-narrow-tip, 31 nm minimum) among 150 total new in-crop violations. The mechanism is straightforward: reducing the y-extent of a polygon shortens its top and bottom edges. Edges that previously exceeded 36 nm become tips (≤36 nm), invoking the stricter tip-based spacing rules M3.S.2 and M3.S.4 rather than the side-to-side rule M3.S.1 (18 nm). Edges that further fall below 24 nm become narrow tips, invoking M3.S.4 (31 nm) or M3.S.5 (31 nm mixed). Do not issue a -64 dbu (or comparable magnitude) symmetric y-resize across a large population of M3 polygons without per-polygon edge-length checks; trial:i02.ug.leaf_0045.20 demonstrates this reliably produces M3.S.2 and M3.S.4 violations at scale.

By contrast, a single-polygon M3 resize — the y=-20 dbu resize_end on p2328 in trial:i02.ug.leaf_0009.12, the only other M3-only single-polygon resize in the record — was gated_in with 1 new in-crop violation and preserves connectivity. The per-rule breakdown is not available for that trial, so the violation type cannot be identified; however, the operation did not produce the cascade of M3 spacing failures seen in the bulk case.

**Via Cell M3 Shape Shrinkage Is Net-Positive and Must Be Avoided**

In trial:i02.cu.def:VIA_VIA23_1_3_36_36.00, a resize_via_shape operation shrinking the M3 layer shape in cell VIA_VIA23_1_3_36_36 by -40 dbu in y was rejected at the cu_pool gate with decision rejected_net_positive and delta_total=0. The same operation appears in the assemble_drops list of trial:i02.ug.leaf_0045.20 with reason cu_pool:rejected_net_positive, confirming the harness excluded it before that trial's assembled repair was committed. The M3 shape inside a via cell is sized to satisfy V2.M3.EN.2 (minimum 5 nm enclosure of V2 by M3 on two opposite sides) and V2.M3.AUX.2 (M3 must match V2 width in the perpendicular direction); a negative y-resize risks narrowing or eliminating the enclosure margin on the top or bottom edge, causing V2 to protrude outside M3. Do not apply negative y-delta resize_via_shape operations to M3 shapes within via cells; trial:i02.cu.def:VIA_VIA23_1_3_36_36.00 shows that -40 dbu in y on VIA_VIA23_1_3_36_36 is net-positive and will be rejected.

**Instance i1358 Has Zero Net Displacement Across Iterations 2–5**

Instance i1358 (touching M2, M3, V2) appears in four consecutive trials with displacement vectors that cancel to zero:

- trial:i02.ug.leaf_0010.13: moved [0, -36] dbu — gated_in, 0 new violations
- trial:i03.ug.leaf_0002.07: moved [0, +36] dbu — gated_in, 0 new violations (reversal in y)
- trial:i04.ug.leaf_0002.02: moved [-36, 0] dbu — gated_in, 0 new violations
- trial:i05.ug.leaf_0001.01: moved [+36, 0] dbu — gated_in, 0 new violations (reversal in x)

The net displacement of i1358 after all four moves is [0, 0]. None of these four moves introduced M3 violations (0 new in-crop each), but they also failed to make lasting progress: each move was undone in the next iteration. Both the +36 and -36 displacements in x, and both the +36 and -36 displacements in y, have been explored and accepted individually without producing new M3 violations; however, because each direction is subsequently reversed, isolated movement of i1358 alone does not resolve the underlying constraint. Further single-instance perturbation of i1358 without co-moving the surrounding M3 context is not expected to yield a net repair.

**Row-Level M3 Polygon p3631 Oscillates in Y with Zero Net Displacement**

Polygon p3631, located in the Block7_union_row17 locus (y ≈ 19548–20412 dbu), was moved +57 dbu in y in trial:i02.ug.Block7_union_row17.02 (gated_in, 0 new violations) and then returned -57 dbu in y in trial:i03.ug.Block7_union_row17.02 (gated_in, 0 new violations). Net y-displacement is zero. Both trials also moved associated instances i0794 and i0810 by the same delta, and iter-3 included additional instance moves and a resize_end on p2594 that were not present in iter-2. No M3 violations were introduced in either direction, indicating p3631's width and spacing to adjacent M3 geometries are not the binding constraint at either +57 or -57 dbu y-offset. The oscillation is driven by inter-layer coupling (M1, M2, V1, V2 are also touched in both trials); the row-17 locus was not revisited in iterations 4–5.

**Unit Gate Accepts Small New-In-Crop Violation Counts When Connectivity Is Preserved**

The unit_gate channel (channel="unit_gate") accepted trials with 1–4 new in-crop violations provided conn_preserved=true. Trials accepted with non-zero new in-crop counts include trial:i01.ug.Block7_union_row13.03 (1 new), trial:i01.ug.Block7_union_row19.09 (1 new), trial:i01.ug.Block7_union_row9.21 (1 new), trial:i01.ug.leaf_0024.25 (1 new), trial:i02.ug.leaf_0009.12 (1 new), trial:i02.ug.leaf_0032.17 (4 new), trial:i03.ug.Block7_union_row19.03 (1 new), trial:i04.ug.leaf_0007.05 (4 new), and trial:i04.ug.leaf_0008.06 (4 new). The high-water mark was trial:i02.ug.leaf_0045.20, accepted with 150 new in-crop violations (including M3.S.2: 10, M3.S.4: 1) because conn_preserved=true. There is no observed rejection from the unit_gate channel based solely on new-in-crop M3 violation count when connectivity is maintained.

**No M3.W.1 or M3.A.1 Violations Observed**

Neither M3.W.1 (18 nm minimum width) nor M3.A.1 (504 nm² minimum area) appears in any per-rule breakdown across all five iterations. The 39 M3 polygons that each received a -64 dbu symmetric y-resize in trial:i02.ug.leaf_0045.20 produced no M3.W.1 or M3.A.1 violations, indicating those polygons retained sufficient y-dimension and area after the resize. M3.S.6 (20 nm euclidean corner-to-corner spacing) also does not appear in any violation breakdown; the tested operations have not produced corner-proximity failures on M3.

**M3.S.3 and M3.S.5 Not Yet Triggered**

M3.S.3 (wide-tip-to-wide-tip, 27 nm, for tips between 24–36 nm) and M3.S.5 (wide-tip to narrow-tip, 31 nm, mixed) do not appear in any per-rule violation breakdown across the five measured iterations. All observed tip-based M3 violations fall under M3.S.2 and M3.S.4. This reflects the geometry of the resized polygons: the -64 dbu bulk resize in trial:i02.ug.leaf_0045.20 converted edges to tips in ranges that triggered S.2 and S.4 but not S.3 or S.5.