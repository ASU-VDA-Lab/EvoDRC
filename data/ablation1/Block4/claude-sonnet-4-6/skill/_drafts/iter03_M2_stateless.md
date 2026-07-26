## M2 Repair Patterns -- Block4, Iterations 1-3

### Horizontal (X-axis) Instance Moves Are Safe on M2

Move-instance operations with a purely horizontal delta introduce zero new M2 violations when applied to units whose touched layers include M2. This holds across a wide range of delta magnitudes: +12 dbu (trial:i01.ug.Block4_union_row10.01), +28 dbu (trial:i01.ug.Block4_union_row2.02), +36 dbu (trial:i01.ug.Block4_union_row1.00, trial:i01.ug.Block4_union_row6.05, trial:i01.ug.leaf_0020.09, trial:i01.ug.leaf_0021.10, trial:i03.ug.leaf_0001.01), +37 dbu (trial:i01.ug.Block4_union_row5.04), +72 dbu (trial:i02.ug.Block4_union_row1.00), +96 dbu and +108 dbu (trial:i02.ug.Block4_union_row10.01), -28 dbu (trial:i02.ug.Block4_union_row3.02), -36 dbu (trial:i01.ug.Block4_union_row5.04 for one instance in a multi-move op), and +108 dbu (trial:i02.ug.Block4_union_row7.03). Multi-instance horizontal moves in the same crop also produce zero new M2 violations (trial:i01.ug.Block4_union_row5.04 moved four instances; trial:i01.ug.Block4_union_row6.05 moved three). Do not avoid horizontal instance moves on M2-touching units out of M2 DRC concern; the measured record shows no case where a purely horizontal instance move on M2 introduced a violation.

### X-axis Polygon Resize and Direct Polygon Moves Are Safe

Extending an M2 polygon's high-x end (resize_end, high, axis=x) produces zero new M2 violations at all measured delta sizes: +16 dbu (trial:i01.ug.Block4_union_row10.01, trial:i02.ug.Block4_union_row10.01), +52 dbu (trial:i02.ug.Block4_union_row7.03), +92 dbu (trial:i01.ug.leaf_0008.08), +172 dbu (trial:i01.ug.Block4_union_row7.06). A direct polygon move (move, axis=x) of +16 dbu also produced zero new M2 violations (trial:i01.ug.Block4_union_row2.02). Apply horizontal polygon resize or move operations on M2 freely when widening or repositioning a metal segment along its length; none of these triggered M2.W.1, M2.S.1, M2.S.2, M2.S.3, M2.S.4, M2.S.5, M2.S.6, M2.S.7, M2.S.8, or M2.A.1 in the measured history.

### Vertical (Y-axis) Instance Moves Are the Primary Source of M2 Tip-Spacing Violations

Move-instance operations with a non-zero Y delta are the only source of M2 rule violations observed across all three iterations. A delta of [0, -44] dbu introduced one new M2.S.2 violation (trial:i02.ug.leaf_0008.04). A delta of [0, -36] dbu introduced one new M2.S.7 violation (trial:i02.ug.leaf_0013.06). A delta of [0, -64] dbu introduced n_new_in_crop=2 (trial:i03.ug.leaf_0004.02; per-rule breakdown not present in the record, but this is the same unit locus and same instance class as the prior Y-move trials). The delta of [36, 44] dbu in trial:i01.ug.leaf_0021.10 (iteration 1) produced zero new violations; the distinguishing factor is that later iterations had already compacted the layout, making Y-displacement more likely to close spacing below the M2 tip-side and tip-tip thresholds.

**M2.S.2 (tip-to-side, 25 nm minimum):** Triggered by a downward instance move of 44 dbu in a locus containing M2 tips near longer side edges (trial:i02.ug.leaf_0008.04). This violation is driven by Y-compression that brings a short M2 edge (<=36 nm, classified as a tip) within 25 nm of a longer edge (>36 nm, classified as a side).

**M2.S.7 (tip-to-tip 18 nm gap co-located with side spacing <=32 nm):** Triggered by a downward instance move of 36 dbu (trial:i02.ug.leaf_0013.06). The rule fires when an 18 nm tip-to-tip separation coincides with side-to-side spacing <=32 nm and parallel run length <35 nm. Vertical movement that reduces the pitch between two M2 tracks can simultaneously create the 18 nm tip gap condition and violate the run-length floor.

Avoid Y-axis instance moves on M2-touching units unless the locus geometry is verified to have sufficient margin in both M2.S.2 and M2.S.7 parameters (tip-to-side >=25 nm, and any 18 nm tip gap has accompanying side spacing >32 nm or run length >=35 nm).

### M2.S.2 and V1.M2.EN.2 Co-occur on Vertical Moves

The same [0, -44] dbu move that introduced M2.S.2 also introduced one V1.M2.EN.2 violation (trial:i02.ug.leaf_0008.04). This co-occurrence is structurally explained: a downward instance shift that brings an M2 tip too close to a neighboring side edge simultaneously narrows M2 enclosure of the V1 via on that edge. When M2.S.2 appears after a Y-axis move, check V1.M2.EN.2 on the same clip before scoring the repair; the two violations share the same geometric root.

### Multi-Op M2 Polygon Y-Resize Combined With Via Adjustments Clears Via-Related M2 Violations

In the cu_pool channel, the VIA_VIA23_1_3_36_36 cell was repaired in iteration 1 by bundling eleven M2 polygon y-axis resizes (-64 dbu each) together with a V2 via-shape resize and an M3 via-shape resize, achieving delta_total=-24 (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, decision=applied). A competing trial that applied only the M3 via-shape resize without the M2 polygon resizes achieved delta_total=0 and lost the tournament (trial:i01.cu.def:VIA_VIA23_1_3_36_36.01, decision=lost_tournament). Apply bundled M2 polygon resizes together with via layer adjustments rather than adjusting the via layer alone; the single-via-op approach failed to reduce any violations whereas the bundled approach reduced 24.

In iteration 3, moving the V2 via shape laterally by x+144 dbu on the same cell (touching M2/M3/V2) reduced total violations by 17 (trial:i03.cu.def:VIA_VIA23_1_3_36_36.00, decision=applied). A lateral V2 repositioning that shifts the via center along the M2 track can resolve M2 enclosure violations (V2.M2.EN.1 requires >=5 nm enclosure on two opposite sides) without any direct M2 polygon edit. Use V2 lateral moves as a first option for V2.M2.EN.1 violations before attempting M2 polygon reshape.

### Gating Behavior: conn_preserved Overrides New In-Crop Violation Count

All trials with n_new_in_crop>0 were still accepted (decision=gated_in) when conn_preserved=true. The two trials that introduced M2 violations -- trial:i02.ug.leaf_0008.04 (M2.S.2+1, V1.M2.EN.2+1) and trial:i02.ug.leaf_0013.06 (M2.S.7+1) -- were both gated_in because connectivity was preserved. The gating channel does not reject a trial solely on the basis of introducing new DRC violations when the connectivity criterion is met. This means M2 violation introduction during a conn_preserved repair attempt is not automatically fatal; the repair is accepted and the new violations become debt for subsequent iterations.

### Assemble Conflict Drops: Competing Y-Moves on the Same Instance

When two units in the same iteration both propose a Y-axis move on the same instance (i0038), the assemble stage drops one op from each unit's merged solution to resolve the conflict (trial:i02.ug.leaf_0008.04 dropped the [0,-44] move attributed to leaf_0013; trial:i02.ug.leaf_0013.06 dropped the [0,-36] move attributed to leaf_0008). Both units remained gated_in despite the drops because conn_preserved was still satisfied by their remaining ops. When multiple units in the same crop locus claim the same instance for a Y-axis move, only one direction can win in the assembled solution; the losing move is silently dropped without failing the gate. Design repair sequences so that Y-axis instance moves targeted at M2 tip-spacing violations are not simultaneously claimed by overlapping units.

### No M2.W.1, M2.A.1, M2.S.3, M2.S.4, M2.S.5, M2.S.6, or M2.S.8 Violations Observed

Across all 21 recorded trials in iterations 1-3, none of the measured decisions report new violations of M2.W.1 (minimum width 18 nm), M2.A.1 (minimum area 504 nm^2), M2.S.3 (wide-tip-to-wide-tip 27 nm), M2.S.4 (narrow-tip-to-narrow-tip 31 nm), M2.S.5 (wide-tip-to-narrow-tip 31 nm), M2.S.6 (corner-to-corner 20 nm), or M2.S.8 (diagonal gap center spacing 80 nm). No prescriptive guidance on those rules is grounded by the current measured history; rely on the rule text alone for those constraints until violations are observed.