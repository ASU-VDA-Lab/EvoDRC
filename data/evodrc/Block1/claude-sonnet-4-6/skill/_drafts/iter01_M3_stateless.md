## Via Shape Shrinks on M3 (y-axis)

Shrinking the M3 shape inside VIA_VIA23_1_3_36_36 by -40 dbu along the y-axis produced a cu_pool delta_total of 0 and was rejected (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). The same operation was subsequently dropped during unit-gate assembly with the explicit reason `cu_pool:rejected_net_positive` (trial:i01.ug.leaf_0035.13, assemble_drops). Do not resubmit this via shape resize: it contributes nothing to violation count reduction and will be rejected at the cu_pool gate.

## Symmetric y-Axis Resize of M3 Polygon Bodies

Applying a uniform -64 dbu y-axis resize across a group of M3 polygons (12 polygons: p1501, p1493, p1491, p1460, p1459, p1458, p1543, p1538, p1535, p1420, p1435, p1434) preserved connectivity and was gated in (trial:i01.ug.leaf_0035.13). However, this operation introduced 2 new M3.S.2 violations (tip-to-side spacing below the 25 nm minimum). When shortening M3 polygon bodies along y, verify that the newly exposed tip edges (≤ 36 nm length) remain at least 25 nm from any adjacent side edge longer than 36 nm; the measured outcome shows that a -64 dbu body shrink is not guaranteed to be M3.S.2-clean (trial:i01.ug.leaf_0035.13).

## Connectivity Must Be Preserved; Instance Moves + End Resizes That Break Nets Are Rejected

A compound operation combining a y-axis via shape resize, polygon end resizes (including -4 dbu and +192 dbu and +100 dbu moves on right edges of p1214, p1178, p1255), and lateral instance moves (72–136 dbu in x for six instances) broke connectivity and was gated out with reason `conn_broken` (trial:i01.ug.leaf_0034.12). Never apply end-resize or instance-move combinations that sever net connectivity; the gating mechanism rejects them unconditionally regardless of DRC improvement (trial:i01.ug.leaf_0034.12).

## M3.S.2 Tip-to-Side Spacing Risk When Shortening Polygon Bodies

M3.S.2 requires a minimum 25 nm separation between a tip edge (≤ 36 nm) and a side edge (> 36 nm) measured by projection. The only gated-in M3-touching operation in the measured history (trial:i01.ug.leaf_0035.13) introduced 2 new M3.S.2 violations as a direct consequence of y-axis body shrinkage. When reducing polygon height, the shortened end creates or reveals tip edges that may violate the 25 nm tip-to-side rule against neighboring polygon sides. Verify M3.S.2 clearance after any operation that reduces polygon extent along an axis (trial:i01.ug.leaf_0035.13).

## V2 Enclosure Constraints on M3

V2.M3.EN.2 requires M3 to enclose V2 by at least 5 nm on two opposite sides (or 5 nm on one side and flush on the other). V2.M3.AUX.2 further requires V2 to exactly match M3 width in the direction perpendicular to M3 length. The rejected via shape shrink (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00) operated on M3 shapes inside VIA_VIA23_1_3_36_36 along the y-axis; although the operation was rejected for net-positive delta rather than a V2 enclosure error, any y-axis reduction of the M3 enclosing shape inside a V2 cell risks violating V2.M3.EN.2 or V2.M3.AUX.2. Do not shrink the M3 component of a via cell along the enclosure axis without confirming that the remaining M3 extent still satisfies the 5 nm two-sided enclosure requirement (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).