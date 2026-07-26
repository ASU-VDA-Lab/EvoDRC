## V2 Rule Behavior Observed in Measured History

### V2.M3.EN.2: M3 enclosure failures are the dominant V2 violation source

V2.M3.EN.2 requires M3 to enclose V2 by 5 nm on two opposite sides (5 & 5 nm or 5 & 0 nm). Both iter-2 unit-gate trials that touched V2 introduced exactly six new V2.M3.EN.2 violations each: trial:i02.ug.leaf_0003.02 reported `"V2.M3.EN.2":6` in `new_in_crop_by_rule`, and trial:i02.ug.leaf_0004.03 likewise reported `"V2.M3.EN.2":6`. In both cases the bulk of the op-set was lateral M3/V2/V3/V4/V5 moves across the crop boundary, and the trials were accepted (gated_in, conn_preserved) because the net violation count did not worsen — but these results confirm that moving M3 polygons without simultaneously repositioning V2 cuts, or vice versa, consistently produces V2.M3.EN.2 errors. Do not move M3 shapes independently of their associated V2 cuts unless the resulting M3-to-V2 enclosure on both end-cap sides is verified to remain ≥ 5 nm.

### V2.M3.AUX.2: M3 width and V2 cut width must remain matched perpendicular to M3 length

V2.M3.AUX.2 requires that V2 exactly spans the full M3 width in the direction perpendicular to the M3 run. In trial:i03.ug.leaf_0003.02 the repair comment for polygon p1543 explicitly states: "Shrink p1543 right edge from 13876 to 13868 … All V2 cuts inside p1543 have rightmost edge at x=13860 < 13868 so V2.M3.AUX.2 alignment is preserved." This shows that a resize of an M3 end is safe with respect to V2.M3.AUX.2 only when all V2 shapes inside that M3 polygon already lie fully within the new M3 boundary. When M3 is grown, the V2 cuts must be extended to match the new M3 width; when M3 is shrunk, the V2 cuts must not protrude past the new edge.

### Resizing V2 shapes in the via cell definition: grow along y, pair with M2 and M3

The only cu_pool trial that was applied for V2 (trial:i03.cu.def:VIA_VIA23_1_3_36_36.00) grew all three V2 shapes in cell VIA_VIA23_1_3_36_36 by +64 dbu (16 nm) along the y-axis, simultaneously growing the M2 shape by +64 dbu y and the M3 shape by +24 dbu y. This reduced the violation count by 12 (leaf_0002: 93 → 81). The earlier cu_pool trial on the same cell definition (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00) attempted only a −40 dbu y shrink of the M3 shape with no V2 or M2 adjustment and was rejected (delta_total = 0, decision = rejected_net_positive). The contrast between these two outcomes establishes that shrinking M3 alone in a via cell definition does not relieve V2-related violations, while growing V2 (and correspondingly M2 and M3) does. When resizing V2 shapes inside a via cell, always extend M2 by the same amount to maintain V2.M2.EN.1 enclosure, and extend M3 by at least enough to preserve V2.M3.EN.2 and V2.M3.AUX.2.

### Connectivity must be evaluated before committing any V2-touching resize

trial:i01.ug.leaf_0034.12 included a resize_via_shape on M3 (axis=y, delta=−40 dbu) inside VIA_VIA23_1_3_36_36, along with M2/M3/M4/V1/V2 polygon resizes and instance moves. The trial was gated_out with `conn_broken` and `n_new_out_of_crop: 0`, meaning the violation count did not worsen but connectivity was severed. V2-touching operations that shrink M3 or reposition V2 instances reduce the M3-to-M2 overlap area; verify that the VIA cell's M2 land still overlaps its parent M2 bus segment and that the M3 land still reaches the parent M3 wire before committing.

### V2.W.1: Minimum 18 nm V2 width along M3 length constrains shrink headroom

V2.W.1 sets 18 nm as the minimum V2 dimension along the M3 run direction. The successful grow in trial:i03.cu.def:VIA_VIA23_1_3_36_36.00 added 64 dbu = 16 nm per shape along y (the M3 run direction), which is permissible because it widens V2, not narrows it. Shrinking V2 along the M3 length direction is not supported by any successful trial in this history and risks violating V2.W.1 if the resulting dimension falls below 18 nm.

### V2.S.1 / V2.S.2 / V2.S.3 / V2.S.4: No spacing violations recorded; no prescriptive guidance grounded in this history

None of the history records report new V2.S.1, V2.S.2, V2.S.3, or V2.S.4 violations in `new_in_crop_by_rule`, and none of the accepted repairs targeted those rules. No measured citation supports prescriptive guidance on spacing-rule repair strategies for V2 at this time.

### V2.AUX.1: V2 must remain inside both M2 and M3

V2.AUX.1 is structurally enforced by the paired grow approach validated in trial:i03.cu.def:VIA_VIA23_1_3_36_36.00, where M2 and M3 were extended whenever V2 was extended to ensure V2 stayed inside both metals. Any op that repositions V2 without a corresponding adjustment to both its enclosing M2 and M3 shapes risks introducing V2.AUX.1 violations.