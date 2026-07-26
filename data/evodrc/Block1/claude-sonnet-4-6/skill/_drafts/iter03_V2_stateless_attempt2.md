## V2.M3.AUX.2 — Width Matching Perpendicular to M3 Length

Rule V2.M3.AUX.2 requires V2 to be exactly the same width as M3 in the direction perpendicular to M3 length. In trial:i03.ug.leaf_0003.02, when the right edge of M3 polygon p1543 was shrunk by 8 dbu (axis x), the repair was committed only after verifying that "All V2 cuts inside p1543 have rightmost edge at x=13860 < 13868 so V2.M3.AUX.2 alignment is preserved." Before committing any M3 edge resize that changes M3 width perpendicular to its length, every V2 cut inside the affected M3 polygon must be verified to remain co-extensive with M3 in that axis; if it does not, the V2 shape must be resized by the same delta in the same axis (trial:i03.ug.leaf_0003.02).

## V2.AUX.1 — V2 Must Remain Inside Both M2 and M3

Rule V2.AUX.1 flags any V2 shape not fully contained within the intersection of M2 and M3. In trial:i03.cu.def:VIA_VIA23_1_3_36_36.00, all three V2 shapes of cell VIA_VIA23_1_3_36_36 were grown +64 dbu in Y (shape_index 0, 1, 2), the enclosing M2 shape was grown +64 dbu in Y, and the M3 shape was grown +24 dbu in Y in the same commit. Co-resizing M2 and M3 together with V2 is what kept V2 inside both metal layers and prevented V2.AUX.1 violations in that applied repair (trial:i03.cu.def:VIA_VIA23_1_3_36_36.00).

## V2.M3.EN.2 — M3 Enclosure of V2

Rule V2.M3.EN.2 requires M3 to enclose V2 by at least 5 nm on two opposite sides (5 & 5 nm or 5 & 0 nm). In trial:i02.ug.leaf_0003.02 and trial:i02.ug.leaf_0004.03, large multi-instance move operations touching M3 and V2 each introduced 6 new V2.M3.EN.2 violations within the crop window despite being gated in. This shows that moving V2-containing via instances or adjacent M3 segments without maintaining enclosure margins produces V2.M3.EN.2 hits. In trial:i03.cu.def:VIA_VIA23_1_3_36_36.00, the successful applied repair extended the M3 shape by +24 dbu in Y alongside V2 extensions of +64 dbu in Y, preserving adequate M3 enclosure and achieving a net −12 violation count.

## V2.M2.EN.1 — M2 Enclosure of V2

Rule V2.M2.EN.1 requires M2 to enclose V2 by at least 5 nm on at least two opposite sides. In trial:i03.cu.def:VIA_VIA23_1_3_36_36.00, the M2 shape of VIA_VIA23_1_3_36_36 was grown +64 dbu in Y simultaneously with all three V2 shapes being grown +64 dbu in Y. Growing M2 by the same delta as V2 in the same axis maintained the enclosure margin required by V2.M2.EN.1 in that applied repair.

## Connectivity Gating on V2-Touching Operations

Operations that resize V2 or its enclosing M3 can break net connectivity, causing the entire repair to be discarded regardless of violation count reduction. In trial:i01.ug.leaf_0034.12, a set of ops including a Y-axis M3 resize of −40 dbu inside cell VIA_VIA23_1_3_36_36 was gated out with decision "gated_out" and reason "conn_broken," discarding an 89-violation reduction. The same Y-axis M3 resize of −40 dbu on the same cell, submitted via the cu_pool channel in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, yielded delta_total = 0 and was rejected as "rejected_net_positive," confirming the −40 dbu M3 shrink on this cell produces no net benefit. By contrast, trial:i03.cu.def:VIA_VIA23_1_3_36_36.00 applied a +64 dbu Y-axis growth on V2 and coordinated +64 dbu on M2 and +24 dbu on M3, achieving a −12 net reduction with conn_preserved = true. Connectivity must be evaluated before committing any V2-touching resize; trial:i01.ug.leaf_0034.12 shows that a violation-count reduction as large as 89 is irrelevant when connectivity is broken.

## V2.W.1 — Minimum Width Along M3 Length

Rule V2.W.1 sets a minimum V2 width of 18 nm along the M3 length direction. In trial:i03.cu.def:VIA_VIA23_1_3_36_36.00, V2 shapes were grown in the Y axis (+64 dbu per shape) and no V2.W.1 violations appear in the delta breakdown of that applied repair. In trial:i01.ug.leaf_0034.12, a Y-axis M3 resize of −40 dbu on the same cell type was attempted; the trial was gated out for connectivity reasons, not width violations, indicating the shrink did not itself reduce V2 below the 18 nm floor in that instance.

## V2.S.1 Through V2.S.4 — Spacing Observations

Rules V2.S.1 through V2.S.4 govern minimum separations between V2 instances under various M3 end-cap configurations (projection and euclidean thresholds from 16.4 nm to 30 nm). No trials in this history record any new V2.S.1, V2.S.2, V2.S.3, or V2.S.4 violations introduced or resolved. In trial:i02.ug.leaf_0003.02 and trial:i02.ug.leaf_0004.03, lateral instance moves of ±16 dbu and ±32 dbu in X across dozens of via instances produced no V2 spacing hits in the per-rule breakdown; the only new V2-related violations were V2.M3.EN.2 (6 each). In trial:i03.cu.def:VIA_VIA23_1_3_36_36.00, growing V2 shapes by +64 dbu in Y also produced no V2 spacing violations. The V2 spacing rules have not been the active constraint in any trial in this history.