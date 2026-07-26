## M3 Repair Knowledge — Iteration 1

### Via-enclosure violations: shrink M3 metal and via shape together along the perpendicular axis

When a via cell (here VIA_VIA23_1_3_36_36) violates V2.M3.EN.2 or V2.M3.AUX.2, shrinking the M3 via shape and all connected M3 polygons together on the same axis resolves the violation. In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, a y-axis resize of −40 dbu on the M3 component of the via shape and −64 dbu on four adjacent M3 polygons (p894–p897) reduced the total DRC count by 8 (leaf_0009 dropped from 25 to 17 violations). The operation was applied with conn_preserved and touched layers M2, M3, and V2.

Do not resize the M3 via shape without simultaneously resizing the connected M3 routing polygons on the same axis: trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 issued matched resize operations on both the via shape (−40 dbu y) and the four attached polygons (−64 dbu y each) in a single committed group (g1), and the net result was a clean violation reduction with no new violations introduced.

### V2.M3.AUX.2 interaction with via sizing

V2.M3.AUX.2 requires V2 width to exactly match M3 width along the direction perpendicular to the M3 length. The cu_pool fix in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 applied a smaller resize to the via shape (−40 dbu) than to the surrounding M3 polygons (−64 dbu). When planning resizes, the via shape delta and the metal polygon delta need not be equal: the via cell encodes its own geometry, and the two resize magnitudes are chosen independently to satisfy both V2.M3.AUX.2 (width match) and V2.M3.EN.2 (two-sided enclosure).

### Instance moves that touch M3 may introduce new in-crop violations

In trial:i01.ug.leaf_0010.07, moving six instances by amounts between −24 and +72 dbu in y (across cells in leaf_0010) introduced 3 new DRC violations inside the crop window while introducing none outside it. The operation was gated_in rather than unconditionally applied; the gating criterion was conn_preserved=true combined with the reported in-crop delta. When a unit_gate move touches M3 alongside M4, M5, V3, and V4 simultaneously, expect up to 3 new M3-region violations per gate event at this scale of displacement.

### Axis discipline for M3 polygon resizes

Both repair operations in the recorded history acted exclusively on the y-axis. Trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 used axis:"y" for every resize op (via shape and all four polygons). Apply y-axis resizes when the enclosure violation is on the top or bottom edges of the via; choose the axis that aligns with the violated enclosure direction to avoid converting an enclosure violation into a spacing or width violation on the orthogonal edges. No x-axis resize on M3 is recorded in this iteration.

### M3.W.1 and M3.S.* headroom after via-region shrink

The −64 dbu y resize on M3 polygons p894–p897 (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00) did not introduce any M3.W.1 (minimum 18 nm width) or M3.S.1/S.2/S.3/S.4/S.5/S.6 spacing violations: the net violation count went down by 8 and no new violations are reported for that unit. Before shrinking an M3 polygon, verify that the post-resize width remains ≥ 18 nm (M3.W.1) and that the resulting edge positions do not close a side-to-side gap below 18 nm (M3.S.1) or a tip-to-side gap below 25 nm (M3.S.2).

### M3.A.1 area floor after shrink

The minimum M3 polygon area is 504 nm². A y-axis shrink of 64 dbu on four M3 polygons was net-safe in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00. Before committing any resize, confirm that the resulting area of each modified polygon remains above 504 nm² to avoid triggering M3.A.1.

### V3.M3.EN.1 is not implicated by the recorded y-shrink

V3.M3.EN.1 requires ≥ 5 nm enclosure of V3 by M3 on at least one pair of opposite sides. The VIA_VIA23_1_3_36_36 resizes in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 targeted V2-to-M3 enclosure (V2.M3.EN.2, V2.M3.AUX.2) and did not trigger V3.M3.EN.1 violations. Keep V3 enclosure margins in mind when shrinking M3 polygons that simultaneously land over both V2 and V3 vias.