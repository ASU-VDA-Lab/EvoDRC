## M3 Repair Patterns — Iteration 1

### Move operations on M3 polygons can introduce new violations even when connectivity is preserved

A lateral move of polygon p910 by +8 dbu on the x-axis was gated out rather than applied because it introduced 3 new DRC violations inside the crop region (trial:i01.ug.leaf_0010.07). Connectivity was preserved across the operation, yet the net change was negative. Do not treat connectivity preservation as a sufficient acceptance criterion for M3 moves; the solver must also confirm that no new violations appear in-crop before committing the change.

### Chain fixes that resize M3 via-cell shapes on the y-axis are an effective violation-reduction strategy

A chain_fix that resized the M3 shape (shape_index 0) in cell VIA_VIA34_1_2_58_52 by +48 dbu on the y-axis — coordinated with matching resizes on V3, V4, and M4 shapes in the same via cell — was applied and yielded a net reduction of 13 violations across two windows (leaf_0009: −7, leaf_0010: −6) (trial:i01.cu.def:VIA_VIA34_1_2_58_52.00). The M3 resize delta (+48 dbu) was smaller than the corresponding V3/V4 resize deltas (+88 dbu each), confirming that M3 and via-layer deltas in a chain fix do not need to be uniform. Apply the M3 portion of a via-cell chain fix as a coordinated set touching M3, the adjacent via layers, and the upper metal together; partial application of only the M3 component was not observed and is not validated by the measured record.

### M3 via-cell resize targets V3.M3.EN.1 and related via enclosure rules

The successfully applied chain fix operated on cell VIA_VIA34_1_2_58_52, a V3-to-M3 via structure. Rule V3.M3.EN.1 requires M3 to enclose V3 by at least 5 nm on two opposite sides; a y-axis expansion of the M3 shape directly increases the available enclosure margin in the perpendicular direction. The +48 dbu y-resize in trial:i01.cu.def:VIA_VIA34_1_2_58_52.00 is consistent with correcting an enclosure shortfall under V3.M3.EN.1. When diagnosing violations in via cells that contact M3, prioritize enclosure checks (V3.M3.EN.1, V2.M3.EN.2, V2.M3.AUX.2) before spacing or width checks.

### Small x-axis nudges on M3 wires in unit-gate context are a violation source, not a fix

The only unit-gate channel attempt recorded for M3 in iteration 1 moved a single polygon by 8 dbu on x and was blocked (trial:i01.ug.leaf_0010.07). The 3 new in-crop violations introduced by this move indicate that an 8 dbu shift is insufficient to clear the offending edge from its neighbor while simultaneously staying clear of geometry on the other side. When the unit-gate channel proposes a small-delta M3 move, verify that the resulting side-to-side clearance satisfies M3.S.1 (minimum 18 nm between long edges) and that tip-to-side and tip-to-tip rules (M3.S.2: 25 nm, M3.S.3: 27 nm, M3.S.4/M3.S.5: 31 nm) are not violated on the opposite side before accepting. The gated_in outcome in trial:i01.ug.leaf_0010.07 shows the move passed connectivity checks but failed the new-violation gate, so the gate check is the binding constraint for this move class.