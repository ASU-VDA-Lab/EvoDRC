**M2 width, spacing, and area requirements**

M2.W.1 sets the minimum polygon width at 18 nm. M2.S.1 governs side-to-side spacing between edges longer than 36 nm: minimum 18 nm. M2.S.2 sets tip-to-side spacing at 25 nm when the tip edge is <= 36 nm and the adjacent edge is > 36 nm. Tip-to-tip spacing is tiered: M2.S.3 enforces 27 nm when both tips measure 24-36 nm; M2.S.4 enforces 31 nm when both tips are < 24 nm; M2.S.5 enforces 31 nm when one tip is 24-36 nm and the other is below 24 nm. M2.S.6 enforces a 20 nm euclidian corner-to-corner spacing. M2.A.1 sets the minimum polygon area at 504 nm-sq.

**M2.S.7 and M2.S.8: tip-to-tip context constraints**

M2.S.7 prohibits an 18 nm tip-to-tip gap co-located with side-to-side spacing <= 32 nm; when side spacing falls at or below 32 nm the parallel run length must be >= 35 nm. M2.S.8 requires euclidian separation of at least 80 nm between centers of tip-to-tip gaps on different M2 tracks, where each gap center is derived by shrinking the 18 nm gap region 8.5 nm per side.

**Via enclosure: V1**

V1.M2.EN.2 requires M2 to enclose V1 by >= 5 nm on two opposite sides (either 5 & 5 nm or 5 & 0 nm configurations). V1.M2.AUX.2 additionally requires V1 to match M2 width in the direction perpendicular to the M2 length, with V1 sharing coincident edges with M2 on at least two opposite sides. Both constraints tie V1 placement and sizing tightly to the enclosing M2 shape.

**Via enclosure: V2**

V2.M2.EN.1 requires M2 to enclose V2 by >= 5 nm on at least two opposite sides, checked via sized(-5 nm, 0) and sized(0, -5 nm) tests. The accepted cu_pool repair trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 resolved 8 violations in the leaf_0012 window by shrinking the y-extent of four M2 polygons (p965, p964, p963, p962) by -64 dbu each, simultaneous with a -40 dbu y-adjustment to the M3 via cell shape. Apply y-axis resizes to M2 polygons in the cu_pool channel when co-adjusting a via stack to satisfy V2.M2.EN.1, as demonstrated in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00.

**unit_gate channel: motion is x-axis only**

All seven accepted unit_gate trials that touched M2 applied instance moves exclusively along the x-axis with a zero y-component: [36,0] in trial:i01.ug.Block2_union_row1.00, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.leaf_0004.04, trial:i01.ug.leaf_0007.05, and trial:i01.ug.leaf_0011.06; [64,0] in trial:i01.ug.Block2_union_row5.02; and [128,0] in trial:i01.ug.leaf_0001.03. Apply x-direction displacement only when constructing unit_gate M2 repairs (trial:i01.ug.Block2_union_row1.00, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0001.03, trial:i01.ug.leaf_0004.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0011.06).

**unit_gate channel: M2 resize_end operations**

Every resize_end op on an M2 polygon in an accepted unit_gate trial uses axis="x" and a positive delta_dbu: +36 on polygon p1040 high end (trial:i01.ug.Block2_union_row3.01); +64 on polygons p1059 and p1057 high ends (trial:i01.ug.Block2_union_row5.02); +184 on polygon p1065 high end and +176 on polygon p957 low end (trial:i01.ug.leaf_0001.03); +36 on polygon p1052 high end (trial:i01.ug.leaf_0011.06). Use only positive delta_dbu values for x-axis resize_end ops on M2 polygons in unit_gate repairs (trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0001.03, trial:i01.ug.leaf_0011.06).

**Connectivity and crop-window integrity**

All eight trials carried conn_preserved=true and reported n_new_in_crop=0, n_new_out_of_crop=0 (trial:i01.ug.Block2_union_row1.00, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0001.03, trial:i01.ug.leaf_0004.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0011.06, trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). Preserve connectivity and avoid introducing new violations outside the repair crop window when moving or resizing M2 polygons (trial:i01.ug.Block2_union_row1.00, trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

**Non-orthogonal geometry**

The NONORTHOGONAL rule flags any M2 edge not at exactly 0 or 90 degrees. All move_instance and resize_end operations in the measured history (trial:i01.ug.Block2_union_row1.00 through trial:i01.cu.def:VIA_VIA23_1_3_36_36.00) produce strictly rectilinear geometry, consistent with this constraint. Do not generate diagonal edges on M2 during any repair operation (trial:i01.ug.Block2_union_row1.00, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0001.03, trial:i01.ug.leaf_0004.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0011.06, trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).