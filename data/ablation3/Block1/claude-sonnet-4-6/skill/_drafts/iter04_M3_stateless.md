## M3 Geometry Rules Summary

M3.W.1 requires minimum polygon width of 18 nm. M3.S.1 requires minimum side-to-side spacing of 18 nm when both edges exceed 36 nm. Tip-to-side spacing (M3.S.2) rises to 25 nm when one edge is ≤ 36 nm and the other is > 36 nm. Tip-to-tip spacing is governed by three overlapping rules: M3.S.3 (27 nm, both tips 24–36 nm), M3.S.4 (31 nm, both tips < 24 nm), and M3.S.5 (31 nm, one tip 24–36 nm and the other < 24 nm). M3.S.6 adds a 20 nm Euclidean corner-to-corner floor independent of edge classification. M3.A.1 sets minimum polygon area at 504 nm².

## Via Enclosure on M3

V2.M3.EN.2 requires that each V2 be enclosed by M3 on at least two opposite sides by 5 nm (either 5 & 5 or 5 & 0 in projection). V2.M3.AUX.2 additionally requires that V2 width exactly match the M3 width in the direction perpendicular to the M3 run; V2 must share two coincident edges with M3 in that direction. V3.M3.EN.1 requires V3 to be enclosed by M3 by 5 nm on at least one pair of opposite sides (the via must fit inside m3.sized(-5 nm, 0) or inside m3.sized(0, -5 nm)).

## Via Shape Resize on M3: net_positive rejection

Shrinking the M3 enclosure shape of via cell VIA_VIA23_1_3_36_36 in the y-axis by 40 dbu (resize_via_shape, delta_dbu = -40) produced delta_total = 0 in the cu_pool evaluation and was rejected as net_positive (trial:i04.cu.def:VIA_VIA23_1_3_36_36.00). The same op was dropped at assemble time in the unit_gate trial for the same reason (trial:i04.ug.whole_design.00). Do not apply negative y-axis resize_via_shape to VIA_VIA23_1_3_36_36's M3 shapes: the recorded outcome is zero DRC benefit and outright rejection by the cu_pool gate.

## M3 Polygon End Extension: accepted without new violations

Extending the high-end of M3 polygons along the x-axis by 128–192 dbu (p1214 +172, p1178 +192, p1211 +172, p1216 +128) and extending the high-end along the y-axis by 9 dbu (p1543 +9, p1458 +9), together with retracting the low-end of p1301 along x by +48 dbu (moving the low edge inward), were all accepted by unit_gate with zero new in-crop DRC violations and connectivity preserved (trial:i04.ug.whole_design.00). End-extension of M3 polygons in this magnitude range is a viable repair move for enclosure deficits.

## Instance and Polygon Moves Touching M3: collateral coupling

A large move-only trial touching M3, M4, M5, M6, V3, V4, and V5 (57 ops comprising polygon moves of ±16/32/64 dbu on p1142–p1145 and p1561–p1563, plus 54 instance moves ranging from ±16 to ±96 dbu) was accepted by unit_gate with connectivity preserved and no new M3-rule violations introduced (trial:i02.ug.whole_design.00). The only new in-crop violations created were 48 counts of V1.M2.AUX.2, which is not an M3 rule. Moving M3-touching instances at these grid steps does not inherently trigger M3.W.1, M3.S.*, or M3.A.1 violations when the moves are uniform across coupled nets.