**V2 Geometry**

The NONORTHOGONAL rule checks every V2 edge and flags those whose angle falls in [1°..89°], [91°..179°], [-179°..-91°], or [-89°..-1°]. All five recorded operations across the measured history use strictly axis-aligned delta_dbu values (single-axis moves or resizes): trial:i01.ug.Block4_union_row7.06, trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, trial:i01.cu.def:VIA_VIA23_1_3_36_36.01, trial:i03.cu.def:VIA_VIA23_1_3_36_36.00, and trial:i04.ug.leaf_0003.01. No diagonal or tilted operations appear anywhere in the history.

V2.W.1 requires V2 width along the M3 length direction to be at least 18 nm.

**V2 Spacing**

V2.S.1 enforces minimum spacing between V2 mask geometries: 18 nm on the same M3 track, 27 nm between parallel non-aligned tracks, 18 nm between parallel aligned tracks. The mask is constructed from v2_nec and v2_wec subclasses based on M3 end-cap presence and extends M3 coincident edges by 5 nm before clipping to non-M3 regions.

V2.S.2 enforces 23 nm euclidean corner-to-corner between two v2_wec instances (both with a 5 nm M3 end-cap). V2.S.3 enforces 30 nm euclidean corner-to-corner between two v2_nec instances (both without a 5 nm M3 end-cap). V2.S.4 enforces 27 nm euclidean corner-to-corner between one v2_wec and one v2_nec instance.

Moving V2 shape_index 1 by +144 dbu in x (trial:i03.cu.def:VIA_VIA23_1_3_36_36.00) was applied and reduced the violation count by 17. That operation touched only V2 and did not resize M2 or M3 shapes, showing that lateral repositioning of a V2 shape alone is sufficient when the enclosure geometry of M2 and M3 is already compliant and only the inter-via spacing is violated.

**Co-resizing M3 and All Associated V2 Polygons**

When M3 enclosure or spacing violations require shrinking the via cell geometry in one axis, resize M3 and all associated V2 and M2 polygons together in the same operation (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). In that trial, the M3 shape (shape_index 0) was resized by -40 dbu in y and all twelve V2/M2 polygons (p1411 through p1422) were each resized by -64 dbu in y within a single 13-op commit; the result was applied with a delta_total of -24 violations. The competing trial (trial:i01.cu.def:VIA_VIA23_1_3_36_36.01) used only the M3 resize (-40 dbu in y, 1 op) and left all V2 polygons unchanged; it lost the tournament with a delta_total of 0. Do not resize M3 alone when changing via cell height: trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 vs. trial:i01.cu.def:VIA_VIA23_1_3_36_36.01 show the full co-resize achieves -24 violations and the M3-only resize achieves zero.

**V2 Enclosure by M3 (V2.M3.EN.2 and V2.M3.AUX.2)**

V2.M3.EN.2 requires M3 to enclose V2 by at least 5 nm on two opposite sides, with one allowed zero end-cap (pattern 5 & 0 nm). V2.M3.AUX.2 requires V2 to exactly match M3 width in the direction perpendicular to M3 length; any overhang or gap triggers the rule. In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, the equal-magnitude resizes of M3 (-40 dbu) and the twelve V2/M2 shapes (-64 dbu) operated on cell def:VIA_VIA23_1_3_36_36 and achieved compliance by shrinking the cell uniformly so V2 remained flush within M3 after the resize.

**V2 Enclosure by M2 (V2.M2.EN.1)**

V2.M2.EN.1 requires M2 to enclose V2 by at least 5 nm on two opposite sides. The twelve polygons (p1411–p1422) co-resized in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 span both V2 and M2 geometry in the via cell; their joint -64 dbu y-resize maintained M2 enclosure relative to the resized V2 shapes.

**V2.AUX.1: V2 Must Lie Inside M2 ∩ M3**

V2.AUX.1 reports any V2 polygon not fully inside both M2 and M3. All applied operations in the history maintained this containment: trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 co-moved all shapes; trial:i03.cu.def:VIA_VIA23_1_3_36_36.00 moved only V2 by +144 dbu in x without resizing M2 or M3, which is only safe when the M2 and M3 boundaries already provide clearance to absorb the lateral shift.

**Unit-Gate Operations Involving V2**

In trial:i01.ug.Block4_union_row7.06, instances i0158 and i0124 were moved by [-28, 0] dbu, polygons p1596 and p1477 were moved -28 dbu in x, and polygon p1395 received a +172 dbu resize on its high-x end. All touched layers including V2 were updated together; the trial was gated in with n_new_in_crop = 0 and n_new_out_of_crop = 0.

In trial:i04.ug.leaf_0003.01, instance i0238 was moved by [-8, 0] dbu and polygon p1410 received a -8 dbu resize on its high-x end, touching M2, M3, and V2. The trial was gated in with conn_preserved = true despite n_new_in_crop = 2; the unit gate accepted the two new in-crop violations because connectivity was preserved.