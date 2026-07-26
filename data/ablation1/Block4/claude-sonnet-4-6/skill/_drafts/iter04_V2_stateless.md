**V2 Cell and Group Repair Mechanics**

The only V2 cell instance present in the measured history is `def:VIA_VIA23_1_3_36_36`. All cu_pool repairs on V2 operate against this cell target across multiple design states. V2 violations are co-located with M2 and M3 changes in every recorded trial; no trial touches V2 in isolation (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, trial:i01.cu.def:VIA_VIA23_1_3_36_36.01, trial:i03.cu.def:VIA_VIA23_1_3_36_36.00, trial:i04.ug.leaf_0003.01).

**Group Operations: Resize All Shapes Together or Gain Nothing**

When resolving V2 violations via M3 dimensional change, the repair must resize both the via cell's M3 shape and every connected polygon in the group simultaneously. Trial trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 applied a `resize_via_shape` on M3 axis=y delta=-40 dbu *plus* individual resizes of 12 polygons (p1411 through p1422) each at axis=y delta=-64 dbu; this achieved delta_total=-24 (leaf_0025: 88→64) and was applied. Trial trial:i01.cu.def:VIA_VIA23_1_3_36_36.01 submitted only the single `resize_via_shape` M3 axis=y delta=-40 dbu without the polygon chain; delta_total=0 and the trial lost the tournament. Never submit an M3 via-shape resize for V2 repair without pairing it with the full set of connected polygon resizes in the same group operation.

**Lateral V2 Shift as a High-Yield Alternative**

A lateral (x-axis) translation of a V2 via shape, without any M3 resizing, resolved violations across two windows simultaneously. Trial trial:i03.cu.def:VIA_VIA23_1_3_36_36.00 moved `shape_index=1` of the V2 cell on axis=x by +144 dbu, producing delta_total=-17 (leaf_0006: 63→51, leaf_0007: 33→28) and was applied. This move does not alter M3 or M2 geometry. Apply a lateral V2 shift when violations appear in two adjacent leaf windows; the single move propagates improvement into both.

**V2.M3.AUX.2 and V2.M3.EN.2 Implications for Group Sizing**

V2.M3.AUX.2 requires V2 to match M3 width exactly in the direction perpendicular to M3 length, and V2 must share at least two coincident edges with M3. V2.M3.EN.2 requires M3 to enclose V2 by at least 5 nm on two opposite sides (5&5 or 5&0 is accepted). When an M3 y-axis shrink is applied (as in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00), the polygon group must be sized to keep V2 within M3 boundaries and maintain the required enclosure; the 12-polygon resize at -64 dbu per polygon confirms that coordinated group resizing, not piecemeal edge nudging, is the correct mechanism for maintaining these enclosure and coincidence constraints.

**V2.AUX.1 Constraint on All Moves**

V2.AUX.1 requires every V2 instance to remain fully inside the intersection of M2 and M3. The applied lateral shift in trial:i03.cu.def:VIA_VIA23_1_3_36_36.00 (+144 dbu on x) preserved this containment, as `conn_preserved=true` was recorded and the trial was accepted. Before applying any V2 lateral shift, confirm that the destination position remains inside both M2 and M3 extents; a shift that exits either metal layer will violate V2.AUX.1 even if spacing rules are satisfied.

**M2 Enclosure: V2.M2.EN.1**

V2.M2.EN.1 requires M2 to enclose V2 by at least 5 nm on at least two opposite sides. All repairs touching V2 also touch M2 (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, trial:i01.cu.def:VIA_VIA23_1_3_36_36.01, trial:i03.cu.def:VIA_VIA23_1_3_36_36.00, trial:i04.ug.leaf_0003.01). Any V2 shift or M2 resize must preserve the 5 nm two-sided enclosure; do not resize M2 unilaterally in the direction of a V2 shift without checking the resulting enclosure margin.

**Spacing Rules: WEC vs. NEC Classification Drives Repair Strategy**

V2.S.1 through V2.S.4 all depend on whether a V2 instance is classified as with-end-cap (WEC, meaning at least one edge is coincident with M3 but not all edges) or no-end-cap (NEC, meaning all edges are coincident with M3). The thresholds differ by classification:

- NEC–NEC corner spacing: 30 nm (V2.S.3)
- WEC–WEC corner spacing: 23 nm (V2.S.2)
- WEC–NEC mixed corner spacing: 27 nm (V2.S.4)
- Same-track spacing: 18 nm; parallel unaligned: 27 nm; parallel aligned: 18 nm (V2.S.1)

The group M3 y-shrink in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 and the x-shift in trial:i03.cu.def:VIA_VIA23_1_3_36_36.00 both target the same cell, which operates in an M3-coincident configuration. WEC/NEC status determines the applicable spacing threshold; always determine the end-cap class of both V2 instances involved in a spacing violation before selecting the target clearance for a move or resize.

**Unit-Gate Channel: Connectivity Preservation Gates Acceptance with New Violations**

Trial trial:i04.ug.leaf_0003.01 shows that the unit_gate channel accepts a repair that introduces n_new_in_crop=2 new violations inside the crop window, provided conn_preserved=true. The operations were a move_instance of i0238 by [-8,0] dbu and a resize_end of p1410 on axis=x high-end by -8 dbu, touching M2, M3, and V2. The gate condition in unit_gate is connectivity preservation, not zero new in-crop violations. Do not discard a repair candidate from unit_gate solely because it introduces a small number of new in-crop violations; submit it and let the gate evaluate connectivity.

Trial trial:i01.ug.Block4_union_row7.06 was also gated_in with n_new_in_crop=0, conn_preserved=true, involving a coordinated instance+polygon move on x (delta=-28 dbu for instances i0158 and i0124 and polygons p1596, p1477) plus a resize_end of p1395 on x high by +172 dbu. The combination of coordinated lateral moves at uniform delta with a single compensating end-resize is a proven pattern for connectivity-safe repositioning of V2-adjacent structures.

**NONORTHOGONAL Rule**

All V2 edges must be strictly orthogonal (0° or 90°). No diagonal or off-axis edges are permitted on V2. All resizes and moves in the recorded history maintain axis-aligned operations (axis=x or axis=y; delta values applied orthogonally). Do not introduce any operation that produces a non-axis-aligned V2 edge.