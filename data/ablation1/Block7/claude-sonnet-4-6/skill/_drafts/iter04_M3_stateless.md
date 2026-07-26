**M3.S.2 and M3.S.4 are the active M3 spacing failure modes in this design state.**

Bulk simultaneous Y-axis shrink of M3 polygons produces M3.S.2 and M3.S.4 violations. In trial i02.ug.leaf_0045.20, 39 M3 polygons were each resized by -64 dbu in Y across the full-block locus (1728,2068)-(28728,28172), generating 10 new M3.S.2 (tip-to-side, 25 nm minimum) violations and 1 new M3.S.4 (narrow-tip-to-tip, both edges <24 nm, 31 nm minimum) violation. The unit_gate channel accepted this operation as gated_in because conn_preserved=true, so all 11 new M3 violations entered the repair queue. Do not apply large-magnitude simultaneous Y-shrinks to many M3 polygons in high-density regions; M3.S.2 and M3.S.4 are the first rules to fail under that pattern.

**Shrinking M3 via-cell shapes does not reduce DRC violations and must be avoided.**

The cu_pool trial i02.cu.def:VIA_VIA23_1_3_36_36.00 applied resize_via_shape with delta_dbu=-40 in Y to the M3 layer of cell VIA_VIA23_1_3_36_36, touching M2/M3/V2. The result was delta_total=0 (rejected as net_positive): across all five monitored unit windows (leaf_0032, leaf_0038, leaf_0041, leaf_0045, leaf_0046), the operation produced zero net DRC improvement. The same op was listed in the assemble_drops of trial i02.ug.leaf_0045.20 with reason cu_pool:rejected_net_positive and was discarded before assembly. Do not use resize_via_shape with negative Y delta on M3 shapes in VIA_VIA23_1_3_36_36; this repair path is confirmed ineffective.

**Translating M3/V2 stacks intact is consistently safe when connectivity is preserved.**

Every trial in the measured history that moved M3-touching instances or polygons without breaking internal stack geometry was gated_in. Trials i02.ug.leaf_0010.13 (instance i1358, move_instance y-36, M2/M3/V2 touched, 0 new violations), i03.ug.leaf_0002.07 (instance i1358, move_instance y+36, M2/M3/V2, 0 new violations), and i04.ug.leaf_0002.02 (instance i1358, move_instance x-36, M2/M3/V2, 0 new violations) all moved the same M2/M3/V2 stack in X and Y across three successive iterations with no new M3 violations. Keeping the relative geometry of via to metal unchanged while translating the stack preserves V2.M3.EN.2 and V2.M3.AUX.2 compliance.

**Selective single-polygon resize_end on M3 produces zero new M3 violations.**

Trials i01.ug.Block7_union_row13.03 (resize_end x+4 on p3526), i01.ug.leaf_0024.25 (resize_end x+36 and y+44 on p3538, y+20 on p2333, x+52 on p3706), and i04.ug.leaf_0001.01 (resize_end x-40 on p3297, x+108 on p3696, y-12 on p2719) all applied targeted resize_end operations to individual M3 polygons and were gated_in with zero new M3 DRC violations. Prefer selective single-polygon resize_end over global multi-polygon resize when correcting M3 width or spacing errors; the global approach (39 polygons, trial i02.ug.leaf_0045.20) generated 11 new M3 violations while selective approaches generated none.

**Y-axis polygon moves on M3 are safe at magnitudes up to at least 68 dbu.**

Polygon p3631 was moved y+57 in trial i02.ug.Block7_union_row17.02, reversed to y-57 in trial i03.ug.Block7_union_row17.02, and then moved y+68 in trial i04.ug.leaf_0007.05, with all three trials gated_in and zero new M3 violations each time. Polygon p3526 was moved y-57 in trial i04.ug.Block7_union_row13.00 (0 new violations). Y-translations of individual M3 polygons at these magnitudes do not introduce M3.S.1, M3.S.2, M3.W.1, or enclosure violations when accompanying instances are co-moved.

**The solver reverses M3 moves across iterations; plan operations with that in mind.**

Instance i1358 moved y-36 in i02.ug.leaf_0010.13 was reversed to y+36 in i03.ug.leaf_0002.07, then shifted x-36 in i04.ug.leaf_0002.02. Polygon p3631 moved y+57 in i02.ug.Block7_union_row17.02 was reversed y-57 in i03.ug.Block7_union_row17.02 before a larger y+68 was applied in i04.ug.leaf_0007.05. Subsequent iterations can and do undo prior M3 moves when the global violation landscape changes; do not treat a single gated_in acceptance as a permanent fix.

**No violations of M3.W.1, M3.S.1, M3.S.3, M3.S.5, M3.S.6, M3.A.1, V3.M3.EN.1, or V2.M3.AUX.2 were recorded in any measured trial.**

Across all 21 history records, the only M3-layer rules appearing in delta per_rule breakdowns are M3.S.2 (10 new violations, trial i02.ug.leaf_0045.20) and M3.S.4 (1 new violation, trial i02.ug.leaf_0045.20). M3.W.1, M3.S.1, M3.S.3, M3.S.5, M3.S.6, M3.A.1, V3.M3.EN.1, and V2.M3.AUX.2 do not appear in any new_in_crop_by_rule or new_out_of_crop_by_rule entry in this design state.