## Final-pair measured facts (reference-design tail evidence)

Provenance: these facts come from the final-pair comparison of the reference design's initial layout against its repaired final layout, plus the BEFORE and AFTER DRC reports. Every coordinate and delta cited in this document is quoted inline from that pair; the layout files themselves are not needed and are not shipped with this skill.

M5.AUX.1 is resolved by coordinate snapping (x-shift of the stripe), with the M5.AUX.2 track parity (center_x mod 192 == 48) picking the snap direction. The M4 grid fixes are NOT mere snapping: they combine y-edge snapping (M4.AUX.1), height normalization to the V3 height, track parity (center_y mod 192 == 48, M4.AUX.2), and the coupled VIA34/VIA45 moves. No object add/delete was needed in either of these cases -- a property of these repairs, not a universal rule. (seed, reference-design-verified)


## Case notes (reference-design tail evidence)

Anti-pattern AP-2 (atomic stripe batch): an M5 stripe x-shift and all VIA_VIA45 instances associated with that shifted stripe are applied as one complete batch in the reference design. The final diff shows two M5 stripes shifted -88 dbu in x, and all seven repaired VIA45 instances also take dx=-88. VIA_VIA34 is NOT part of that x-batch (it keeps x and re-centers in y with the M4 reshape -- see Family B (-> see M4.md / V3.md) Step 5). From a local crop, do not submit a partial stripe migration unless the complete VIA45 target set for that stripe is known. (seed, reference-design-verified)

M5 and M4 are tightly coupled: M5.AUX.1 drives M5 x-shift. That shift forces VIA45 x-move. VIA45 x-move forces a top-level M4 x-extent adjustment (to keep the MERGED M4 valid around V4). M4.AUX.1 independently forces M4 y-move. VIA45 tracks both, producing combined deltas such as (-88, -48) or (-88, +120). Compute the x and y components separately, then sum. (seed, reference-design-verified)


## Iteration 1 measured facts (Block3 / cu_pool)

In trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 (Block3, cu_pool, locus [1728, 2068, 11016, 10892]), a five-operation repair to VIA_VIA45_1_2_58_58 was applied with decision=applied and conn_preserved=true, reducing violations by 18 (delta_total=-18): window leaf_0018 dropped from 32 to 22, and leaf_0019 dropped from 35 to 27.

The five ops in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 follow a two-shape V4 expand pattern on axis x: shape_index=0 is moved by -116 dbu then resized by +384 dbu; shape_index=1 is moved by +116 dbu then resized by +384 dbu. Applying the move before the resize on each shape is the order recorded in the applied sequence.

M4 in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 receives a single resize of +152 dbu on axis x (shape_index=0), widening it in x alongside the V4 expansion. Touched layers for this repair are M4, M5, and V4.


## Iteration 2 measured facts (Block3 / unit_gate)

Both iteration 2 trials are in channel unit_gate and touch layers M3, M4, M5, V3, and V4 -- a broader stack than the iteration 1 cu_pool repair (M4, M5, V4 only). The shared design_state cd809b6a93563afcd62d322c279cdc57aebe33aba6f3e2ea065bbac59782f962 confirms both iteration 2 trials operate on the same design snapshot.

**trial:i02.ug.leaf_0003.02** (Block3, unit_gate, locus [1728, 2068, 11016, 10892], leaf_0003): six move_instance ops, all on axis y only, no polygon resizes. Three distinct y-deltas are applied in instance pairs: i0177 and i0152 move by (0, -48); i0079 and i0102 move by (0, +96); i0078 and i0101 move by (0, +48). Decision is gated_in with conn_preserved=true and n_new_in_crop=0. A pure y-displacement repair -- no x-component, no shape resize -- can satisfy the gating criterion without introducing new in-crop violations.

**trial:i02.ug.leaf_0004.03** (Block3, unit_gate, locus [1728, 3148, 11016, 9812], leaf_0004): thirteen ops following a compound pattern. The first op moves polygon p1059 by +32 dbu on axis x. This is followed by four groups, each consisting of two move_instance ops and one polygon resize_end on axis y. The four groups in sequence: (1) i0151 moves (0, +72), i0173 moves (+32, +72), p1104 high end resized +72; (2) i0192 moves (0, +24), i0147 moves (+32, +24), p1103 high end resized +24; (3) i0096 moves (0, -24), i0083 moves (+32, -24), p1102 low end resized +24; (4) i0088 moves (0, -72), i0085 moves (+32, -72), p1101 low end resized +72. Decision is gated_in with conn_preserved=true but n_new_in_crop=2: gating on conn_preserved passes even when two new in-crop violations are introduced.

The leaf_0004 x-offset of +32 dbu propagates consistently: the polygon p1059 moves +32 in x, and within each of the four subsequent groups exactly one of the two instances carries the +32 dx (the other carries dx=0). Instances that do not ride the polygon x-shift carry only the y-delta. This confirms the x-delta from a polygon move must be tracked per-instance and applied selectively, not broadcast to all instances in the operation set.

The four y-magnitudes in trial:i02.ug.leaf_0004.03 are symmetric around zero: the high-end groups use +72 and +24; the low-end groups mirror with -72 and -24 (expressed as low-end resize of +24 and +72 respectively). The resize_end direction (high vs. low) encodes which edge of the polygon is moved, and the magnitude equals the y-displacement of the co-located instances in that group.

gated_in does not guarantee zero new violations in crop: trial:i02.ug.leaf_0004.03 records n_new_in_crop=2 alongside gated_in. The gating criterion recorded in both iteration 2 trials is conn_preserved, not a zero-new-violation requirement.