**V4 enclosure: co-resize M4 and V4 in the x-axis within the via cell definition**

V4.M4.EN.1 requires every V4 that lies inside M4 to be enclosed by at least 11 nm on at least two opposite sides. The measured repair is to grow both the M4 via shape and all V4 via shapes in the x-axis together inside the cell definition. Trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 applied x-axis resize_via_shape of +152 dbu to M4 shape_index 0 and to V4 shape_index 0 and shape_index 1 in cell VIA_VIA45_1_2_58_58; the change was accepted with conn_preserved=true and reduced the total design violation count by 16 (from 68 to 52). Growing only one side of the pair was not tested in the recorded history; the recorded fix resizes both conductor layers by the same delta in the same axis.

**M4 polygon end retraction and high-end extension on the x-axis are accepted when connectivity is preserved**

Retracting the low-x end of a standalone M4 polygon does not break the design when connectivity is preserved. Trial:i01.ug.whole_design.00 gated in a resize_end operation that moved the low-x end of M4 polygon p957 by −172 dbu with conn_preserved=true. That same trial's assemble_drops included the VIA_VIA45_1_2_58_58 M4 shape x-resize (+152 dbu, shape_index 0), the same operation later committed in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, confirming that an end-retraction on a routed M4 segment and a co-directional x-growth inside a via cell are compatible.

High-end x-axis extension is also accepted. Trial:i02.ug.whole_design.00 (gated_in, conn_preserved=true, 45 ops, touched_layers includes M4) includes resize_end high-end operations with delta_dbu values of +32, +80, and +116 dbu on routed polygons. The trial covers Block2 / unit_gate and touches M4 among eight other layers simultaneously; all operations in the batch were accepted as a unit.

**X-axis polygon move is recorded in whole-design trials that touch M4**

Trial:i02.ug.whole_design.00 includes "move" operations (op: "move", axis: "x") on polygons p937 and p938, each shifted +32 dbu, alongside move_instance operations on 20 instances and resize_end operations on eight additional routed polygons. The full 45-op batch was gated_in with conn_preserved=true. The polygon layer attribution (which of p937/p938/p958–p965/p1036/p1065 are M4) is not recorded in the ops list, but M4 is confirmed as a touched layer, so x-axis polygon translation is a valid operation type in the repair vocabulary for trials that include M4.

**Combined y-axis move and x-axis resize_end on the same polygon is present in iteration 2 trials touching M4**

Trial:i02.ug.whole_design.00 contains paired sequences where a polygon first receives a y-axis move (delta_dbu values of ±48, ±72, ±96 dbu) and then a resize_end high-end on the x-axis (+32 dbu) — specifically polygons p958 through p965. The batch was accepted with conn_preserved=true. Because polygon-to-layer attribution is absent from the ops record, direct assignment of these y-axis moves to M4 is not yet grounded; the evidence establishes only that such paired sequences are accepted in batches where M4 is among the touched layers. Prescriptive y-axis guidance specific to M4 must wait for a trial that names M4 explicitly per polygon.

**Rules without measured repair operations in iterations 1–2**

No operations correcting M4.W.1–W.5, M4.S.1–S.5, M4.AUX.1–AUX.4, V3.M4.EN.2, or V3.M4.AUX.2 appear in trial:i01.ug.whole_design.00, trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, or trial:i02.ug.whole_design.00. Prescriptive guidance for those rules must wait for measured evidence from later iterations.