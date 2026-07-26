**M2 Geometry: NONORTHOGONAL**

The GEOMETRY.NONORTHOGONAL rule flags any M2 edge not at 0° or 90°. All M2 operations recorded in trial:i03.ug.whole_design.00, trial:i04.ug.whole_design.00, and trial:i05.ug.whole_design.00 used axis-aligned deltas exclusively — instance moves as [x, 0] vectors and resize_end operations on axis x or y — with no non-orthogonal shape manipulations appearing anywhere in the history.

**M2.W.1 – Minimum Width**

M2.W.1 requires a minimum width of 18 nm for all M2 polygons.

**M2.S.1 through M2.S.6 – Spacing Thresholds**

M2.S.1 sets an 18 nm minimum side-to-side spacing when both facing edges exceed 36 nm. M2.S.2 sets a 25 nm minimum tip-to-side spacing when one edge is ≤36 nm and the other exceeds 36 nm. M2.S.3 sets a 27 nm minimum tip-to-tip spacing when both edges fall in the 24–36 nm range. M2.S.4 sets a 31 nm minimum tip-to-tip spacing when both edges are <24 nm. M2.S.5 sets a 31 nm minimum between a 24–36 nm edge and a <24 nm edge. M2.S.6 requires a minimum 20 nm euclidean corner-to-corner spacing between M2 polygons.

In trial:i04.ug.whole_design.00, polygons p1178, p1211, p1214, and p1216 had their high-x end extended (by 192 dbu, 172 dbu, 172 dbu, and 128 dbu respectively), polygon p1301 had its low-x end extended by 48 dbu, and polygons p1543 and p1458 each had their high-y end extended by 9 dbu; that trial was accepted (gated_in, n_new_in_crop=0). In trial:i05.ug.whole_design.00, polygons p1255, p1270, p1295, p1309, and p1320 each had their high-x end extended by 44 dbu; that trial was also accepted (gated_in, n_new_in_crop=0). Extending an M2 polygon end along the x-axis increases the length of the tip edge, shifting its classification across the 36 nm and 24 nm thresholds that determine which of M2.S.2 through M2.S.5 applies, and increases the tip-to-adjacent-polygon clearance.

**M2.S.7 – Tip-to-Tip / Side-to-Side Co-location**

M2.S.7 forbids an 18 nm tip-to-tip gap co-located with a side-to-side spacing of ≤32 nm, and requires a parallel run length of ≥35 nm whenever the side-to-side spacing is ≤32 nm.

**M2.S.8 – Diagonal Gap Spacing**

M2.S.8 requires the euclidean distance between centers of 18 nm tip-to-tip gaps on different M2 tracks to be ≥80 nm. Gap centers are computed by shrinking each 18 nm tip-to-tip gap region by 8.5 nm per side; the projection-distance check is then compared against the euclidean result, and any gap pair whose euclidean spacing falls below 80 nm but is not caught by the projection check is the violation.

**M2.A.1 – Minimum Area**

M2.A.1 requires a minimum M2 polygon area of 504 nm². All polygon end-extensions recorded in trial:i04.ug.whole_design.00 and trial:i05.ug.whole_design.00 increase polygon area, leaving M2.A.1 consistent with the accepted outcome in both trials.

**V1.M2.EN.2 – V1 Enclosure by M2**

V1.M2.EN.2 requires M2 to enclose V1 by at least 5 nm on two opposite sides; both the 5 & 5 nm and 5 & 0 nm patterns are valid, but the zero-enclosure side must be flush with the V1 edge (the second-edge projection check in the rule). V1 was touched alongside M2 in trial:i03.ug.whole_design.00 and trial:i05.ug.whole_design.00; both trials resolved violations via move_instance operations (uniform 64 dbu horizontal displacement across 32 instances in trial:i03; mixed 36–48 dbu positive and 64–72 dbu negative horizontal displacements across 22 operations in trial:i05), and both were accepted with conn_preserved=true and n_new_in_crop=0.

**V1.M2.AUX.2 – V1 Width Match**

V1.M2.AUX.2 requires V1 to exactly match the M2 width in the direction perpendicular to M2 length, and requires two coincident V1-M2 edges in that direction. The instance-level moves in trial:i03.ug.whole_design.00 and trial:i05.ug.whole_design.00 shift M2 and the V1 via together as a unit, leaving the V1-to-M2 width relationship unchanged; both trials were accepted with conn_preserved=true.

**V2.M2.EN.1 – V2 Enclosure by M2**

V2.M2.EN.1 requires M2 to enclose V2 by at least 5 nm on at least two opposite sides. A cu_pool trial (trial:i04.cu.def:VIA_VIA23_1_3_36_36.00) attempted to shrink the M3 shape of VIA_VIA23_1_3_36_36 by 40 dbu in the negative-y direction, an operation that touched M2 and V2; it was rejected with decision rejected_net_positive and delta_total=0 (no net reduction in violations). That rejected operation was dropped from the assembled unit_gate trial (trial:i04.ug.whole_design.00 lists it in assemble_drops with reason cu_pool:rejected_net_positive). The accepted repair in trial:i04.ug.whole_design.00 extended M2 polygon ends without modifying via cell shapes and was accepted with conn_preserved=true and n_new_in_crop=0.

**Connectivity and Acceptance Criteria**

All three accepted trials (trial:i03.ug.whole_design.00, trial:i04.ug.whole_design.00, trial:i05.ug.whole_design.00) carry conn_preserved=true and n_new_in_crop=0, confirming that accepted M2 repairs must preserve net connectivity and must not introduce new in-crop violations. trial:i04.cu.def:VIA_VIA23_1_3_36_36.00 was rejected under rejected_net_positive with delta_total=0, confirming that a via-shape operation touching M2-adjacent layers is not accepted when it yields no net reduction in violations even if it introduces no new ones.