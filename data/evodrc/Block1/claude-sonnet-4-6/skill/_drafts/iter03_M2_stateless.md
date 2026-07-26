## M2 Repair Knowledge — Layer M2, Iteration 3

### Observed M2 Violations by Rule

**M2.S.3 (tip-to-tip >= 27 nm, both tips 24–36 nm)** was recorded as a new in-crop violation in trial:i02.ug.leaf_0003.02 (count 1) and trial:i02.ug.leaf_0004.03 (count 1). Both trials operated on a large locus spanning nearly the full design height (y: 2068–14132 / 3148–14132 dbu), moving dozens of instances and a small number of M2 polygons simultaneously in the x-axis. The simultaneous displacement of many instances in opposing directions (+32 / −16 dbu) within a single operation set produced tip-to-tip geometry violations that the individual per-instance displacements did not independently create. Neither trial was rejected on connectivity grounds (both conn_preserved, both gated_in), but both left M2.S.3 and M2.S.7 violations in crop.

**M2.S.7 (tip-to-tip at 18 nm co-located with side-to-side <= 32 nm is forbidden)** was similarly recorded once each in trial:i02.ug.leaf_0003.02 and trial:i02.ug.leaf_0004.03. The co-location condition (vertical tip gap near minimum, lateral spacing in the 18–32 nm range) arises when instance displacements in the x-axis bring M2 wire ends into near-contact simultaneously from both dimensions. Avoid committing large fan-out moves (+32 / −16 dbu across many instances in the same locus) without checking that M2 tip-to-side and tip-to-tip spacings at existing minimum margins are not additionally tightened along the orthogonal axis.

### V2.M2.EN.1 and VIA_VIA23 M2 Land Sizing

The cell-definition repair trial:i03.cu.def:VIA_VIA23_1_3_36_36.00 was applied with delta_total −12, reducing 12 violations. Its sole M2 operation was `resize_via_shape` on layer M2, shape_index 0, axis y, delta_dbu +64 (= +16 nm), extending the M2 land in the y-direction. The same commit also extended the V2 shapes by +64 dbu each (three shapes). The matched touched_layers are M2, M3, V2. An earlier attempt on the same cell definition (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00) shrank M3 in y by −40 dbu and was rejected (decision: rejected_net_positive, delta_total 0). The M3-shrink approach did not reduce the V2.M2.EN.1 count; the M2-land-grow approach did. Therefore, for V2.M2.EN.1 failures on a VIA23 cell definition, grow the M2 land along the direction of the enclosure deficit rather than shrinking the via metal above.

V2.M2.EN.1 requires that V2 is enclosed by M2 by at least 5 nm on at least two opposite sides. A +64 dbu (16 nm) extension of the M2 land clears the minimum by a large margin, which confirms the original enclosure was below 5 nm on those sides. When sizing M2 lands on via cell definitions, ensure the extension is at least 5 nm (20 dbu) beyond the V2 shape boundary on each required side.

### VIA12 M2 Overlap Preservation During Instance Moves

In trial:i03.ug.leaf_0003.02, two VIA12 instances (i0485 and i0188) were each displaced +4 dbu (1 nm) in x to clear M1.S.2 violations. The inline comments for both ops explicitly compute that M2 overlap with the connecting M2 bus polygon is preserved after the move:

- i0485: VIA12 M2 new left edge = 12244 − 36 = 12208 dbu; bus polygon p1309 spans x = 11808..12312, so 12208 < 12312 confirms overlap.
- i0188: VIA12 M2 new left edge = 2740 − 36 = 2704 dbu; bus polygon p1270 spans x = 2448..2808, so 2704 < 2808 confirms overlap.

The half-width of the VIA12 M2 land is 36 dbu (9 nm), so the full M2 land width is 72 dbu (18 nm), equal to the M2.W.1 minimum. Moving a VIA12 instance in x shifts both the M2 land and all underlying V1 and M1 lands together. Check that the moved M2 land still overlaps its horizontal M2 bus polygon by at least enough margin to satisfy V1.M2.AUX.2 (V1 must span the full M2 width in the perpendicular direction) and V1.M2.EN.2 (5 nm enclosure on two opposite sides) after the shift.

### Connectivity-Breaking Multi-Layer Moves

Trial:i01.ug.leaf_0034.12 was gated_out (decision: gated_out, reason: conn_broken, 89 new in-crop violations). Its op set combined a resize_via_shape on an M3 layer (axis y, −40 dbu), two resize_end operations on M2 polygons (p1214 right edge −4 dbu; p1255 right edge +100 dbu), and eight instance moves of 72–136 dbu in x. Layers touched were M1, M2, M3, M4, V1, V2. The combination broke connectivity despite the individual M2 polygon adjustments being individually small. Multi-layer operations that simultaneously resize M2 polygons and move instances across a large locus risk severing M2–V1–M1 or M2–V2–M3 connectivity chains even when the individual deltas are modest. The safer decomposition observed in later iterations is to fix one layer at a time (as in trial:i03.ug.leaf_0003.02, which separated M1 via moves from M3 polygon shrinks and preserved M2 overlap explicitly).

### M2 Polygon resize_end Patterns from Iteration 1

All M2 polygon resize_end operations in iteration 1 (trials i01.ug.Block1_union_row1.00 through i01.ug.Block1_union_row8.07) targeted the x-axis exclusively, using the "high" or "low" end designator. Observed delta magnitudes: 36, 48, 56, 92, 100, 128, 136, 156, 192 dbu. All are consistent with snapping to M2 grid positions (multiples of 4 dbu = 1 nm) that satisfy M2.W.1 (minimum width 18 nm = 72 dbu) after resizing. No y-axis M2 polygon resize_end appears in the unit_gate channel across any iteration; y-axis M2 changes observed are confined to cell-definition via-shape resizes (trial:i03.cu.def:VIA_VIA23_1_3_36_36.00). Apply M2 width and spacing corrections preferentially via x-axis resize_end on individual polygon edges rather than instance moves when only one side of a spacing violation is on M2.

### Area Rule M2.A.1

No M2.A.1 (minimum area 504 nm²) violations are recorded in the per_rule breakdowns of any gated trial. Operations that shrink M2 polygon ends (resize_end with negative delta) should verify that the resulting polygon area remains above 504 nm² = 504 dbu² (at 1 dbu = 1 nm). For an 18 nm wide (72 dbu) M2 wire, the minimum length to satisfy M2.A.1 is ceil(504 / 72) = 7 nm (28 dbu). Shrinks observed in the history (e.g., −8 dbu in trial:i03.ug.leaf_0003.02 on M3 polygons that are 72 dbu tall) were applied only where the polygon length remained well above this floor.

### Corner-to-Corner (M2.S.6) and Diagonal Gap (M2.S.8)

Neither M2.S.6 nor M2.S.8 appears in any per_rule violation count across the full history. No repair operation targeting these rules is recorded. Do not apply corrections targeting M2.S.6 or M2.S.8 without a violation record.

### Nonorthogonal Geometry

No M2.GEOMETRY.NONORTHOGONAL violations appear in any trial record. All observed M2 polygon operations (resize_end axis x or y; move_instance in x or y) produce orthogonal geometry. Do not introduce diagonal edges on M2.