## Per-rule recipes

### Family A: M1-via cluster (V0.M1.AUX.3, M1.S.2, M1.S.6, V1.M1.EN.1)

These four rules often cluster around a VIA_VIA12 instance placed where local M1 geometry fails width-matching, spacing, or enclosure constraints -- a single site usually fires one to three of them, not necessarily all four. In the 37-violation example block, 18 of 37 violations belong to this family.

Rule semantics (ASAP7 rule deck):
- V0.M1.AUX.3: V0 y-extent must equal M1 y-extent at the landing location (seed, reference-design-verified). M1 runs horizontally; perpendicular direction is y. Fires when a VIA_VIA12 is placed where V0 width does not match the surrounding M1 width (seed, reference-design-verified).
- V1.M1.EN.1 (deck hgood/vgood construction; description "5 & 2 nm"): on ONE pair of opposite sides -- either the x-pair or the y-pair -- BOTH sides must be >= 2 nm (8 dbu) AND at least ONE of the two >= 5 nm (20 dbu). Fires when NEITHER pair achieves this on the merged M1.
- M1.S.2: Tip-to-side spacing >= 25 nm (100 dbu) when one edge is <= 36 nm and the other > 36 nm.
- M1.S.6: Corner-to-corner spacing >= 20 nm (80 dbu).

Root cause pattern: A VIA_VIA12 (cell = M1 land + M2 land + V1 cut; it does NOT contain V0 -- V0 (layer 18) is the std-cell contact level below, and V0.M1.AUX.3 is checked on the MERGED M1 around it) is placed at a coordinate where the merged M1 has an edge mismatch or insufficient extension. Moving the via to a nearby M1-VALID position -- observed moves include pure-x (trial:i01.ug.Block3_union_row1.00, trial:i01.ug.Block3_union_row2.01), negative-x (trial:i01.ug.leaf_0013.09, delta -36 dbu; trial:i02.ug.leaf_0001.00, delta -36 dbu; trial:i03.ug.leaf_0003.02, delta -36 dbu), and two-axis (e.g. the VIA12 at (5220,3060) relocated to (5292,2952), delta (+72,-108); seed, reference-design-verified) -- or extending the M2-level routing can clear multiple rules of this family at once (multi-rule examples A2, A3, A5 clear 2-3 rules per move; A1 and A4 each clear ONE rule; do not assume all four always clear together).

Recipe -- Co-lateral via-and-pad slide:

Step 1. For each violation in this family, locate the VIA_VIA12 instance whose bounding box overlaps or abuts the violation bbox.
Step 2. Determine the required lateral delta:
  - The new position must satisfy: V0 y-extent == M1 y-extent at the landing point (V0.M1.AUX.3; seed, reference-design-verified). For V1.M1.EN.1 the deck requires, on ONE pair of opposite sides (x-pair or y-pair): BOTH sides >= 8 dbu (2 nm) AND at least one of them >= 20 dbu (5 nm). The VIA_VIA12 cell's own M1 land supplies exactly 8 dbu on both y-sides (land y = +/-44 vs cut +/-36) but 0 on x, so the merged M1 must either lift ONE y-side to >= 20 dbu, or give the x-pair (>= 8 dbu one side, >= 20 dbu the other). The repairs in this case aimed for >= 20 dbu on BOTH x-sides -- a conservative working target sufficient but stricter than the rule minimum. M1.S.2 and M1.S.6 are incidentally cleared when the via moves away from the neighbor causing the tip/corner proximity.
Step 3. Apply the delta to VIA_VIA12. Pure instance moves with no polygon operations are sufficient when existing metal coverage already extends to the new via position (trial:i01.ug.Block3_union_row2.01, trial:i01.ug.leaf_0006.04, trial:i01.ug.leaf_0009.07, trial:i01.ug.leaf_0013.09, trial:i02.ug.leaf_0001.00, trial:i03.ug.leaf_0003.02). Moves in the negative-x direction are valid where geometry permits (trial:i01.ug.leaf_0013.09, delta (-36,0); trial:i02.ug.leaf_0001.00, delta (-36,0); trial:i03.ug.leaf_0003.02, delta (-36,0)).
Step 4. If a VIA_VIA23 is co-located at the same (x, y) (stacked via), decide PER LEVEL -- co-located vias do NOT always travel together:
  (a) COUPLED case: if the M2 landing must move with the V1 fix (the M2 polygon itself is co-moved), move VIA23 by the same delta (verified: the stacked pair at (5652,5220) both moved +64 in x, together with the associated TOP-LEVEL M2 pad and M3 routing polygons; the vias' own M1/M2 lands travel inside the instances -- no top-level M1 was involved; seed, reference-design-verified).
  (b) ANCHOR case: if VIA23's own levels (M2-M3) remain correctly aligned at the ORIGINAL coordinate, leave VIA23 in place and move only VIA12 (verified: VIA12 (3204,1980)->(3340,1980) +136 while the co-located VIA23 stayed at (3204,1980) as the M2-M3 anchor; seed, reference-design-verified).
  (c) PARTIAL case: the two share one axis and split the other (verified: at (6228,2340) both took +8 in y, but VIA12 took +36 in x while VIA23 took 0; seed, reference-design-verified).
  Pre-move check (the deciding question): after moving VIA12, does the V2 level at the OLD position still need VIA23 there to reach M3, and does VIA23's own alignment stay legal? If yes to both -> anchor case, do not move it (seed, reference-design-verified). The final clean pair shows this anchor pattern explicitly: the VIA12 moved while the co-located VIA23 stayed at the original M2-M3 landing. Blindly co-moving every co-located VIA23 with its VIA12 contradicts the clean final pair (seed, reference-design-verified).
Step 5. Re-establish LANDING coverage at the via's NEW position -- the requirement is coverage, not a particular op. The via's own M1/M2 lands travel inside the instance; what requires editing are the TOP-LEVEL M2 (layer 20) landing/routing polygons (and M3 for the VIA23 level, Step 6) -- in the reference-design repair ZERO top-level M1 (layer 19) polygons were touched (seed, reference-design-verified). An ISOLATED landing pad translates by the same delta; a pad attached to a routing stub is reshaped or end-extended instead, and its delta need not equal the via's delta (trial:i01.ug.Block3_union_row1.00: via delta +136 dbu, M2 resize_end +192 dbu; trial:i01.ug.leaf_0012.08: via delta +72 dbu, M2 resize_end +108 dbu; trial:i01.ug.leaf_0007.05: via delta +36 dbu, M2 resize_end +56 dbu; trial:i02.ug.leaf_0002.01: via delta +104 dbu, M2 resize_end +128 dbu). Metal continuity must be preserved across the edit; discontinuity creates a connectivity break the window DRC will not flag (seed, reference-design-verified).
Step 6. VIA_VIA23 is the M2-M3 via: after any VIA23 move, BOTH levels need coverage. If it now falls outside the M2 routing polygon (layer M2), move or extend the M2 polygon to cover it; likewise verify the M3 side still covers the via at its new location.
  Two modes are observed, on WHICHEVER affected level (top-level M2 or M3):
  (a) Co-move: the polygon translates by the same delta as the via (seed, reference-design-verified; worked example A1).
  (b) Extend: one edge is stretched to reach the new via position (seed, reference-design-verified; worked example A2 on M2, example A4 on M3).

Worked example A1 (V0.M1.AUX.3 at [5580,5220,5652,5292]):
  Via at (5652,5220); violation at boundary where V0 width != M1 width.
  Delta: (+64, 0) dbu = 16 nm in +x.
  VIA12 moves (5652,5220)->(5716,5220); VIA23 co-moves same delta.
  M2 landing pad polygon (92x72 dbu, layer 20 = M2) moves (5560,5184)->(5624,5184), same delta (this is VIA23's lower land level / VIA12's upper).
  M3 routing polygon (72x3156 dbu, layer 30 = M3) moves (5616,5184)->(5680,5184), same delta (VIA23's upper level).

Worked example A2 (multi-rule single-move, delta +136 dbu in x):
  VIA12 at (3204,1980) moves to (3340,1980).
  This single move clears:
    V0.M1.AUX.3 at [3204,1980,3276,2052]
    V1.M1.EN.1 at [3168,1944,3240,2016]
    M1.S.2 at [3072,1936,3168,2024] -- the marker ends exactly at the old M1 land's left edge (3168, land y 1936..2024); the +136 move carries the land away from the tip-to-side conflict.
  M2 routing polygon (layer 20 = M2, at (2880,1944)-(3240,2016)) extended: right edge from x=3240 to x=3336 (+96 dbu = 24 nm) -- this re-covers the via's M2 land at its new x. NO top-level M1 polygon was edited: the V1.M1.EN.1 side closes because the RELOCATED via's own M1 land merges with the M1 already present at the new position. The DRC checks enclosure on MERGED metal; computing enclosure from any single polygon alone produces wrong results (seed, reference-design-verified).

Worked example A3 (three-rule single-move, delta +136 dbu in x):
  VIA12 at (2340,3060) moves to (2476,3060).
  This single move clears:
    V0.M1.AUX.3 at [2340,3060,2412,3132]
    V1.M1.EN.1 at [2304,3024,2376,3096]
    M1.S.2 at [2208,3016,2304,3104]

Worked example A4 (V1.M1.EN.1 + M2 extend, delta (0,+68) dbu):
  VIA12 at (5364,5724) moves to (5364,5792); VIA23 co-moves same.
  Clears V1.M1.EN.1 at [5328,5688,5400,5760].
  M3 polygon (layer 30 = M3, at (5328,4896)-(5400,5760)) TOP edge extended from y=5760 to y=5816 to cover the via's M3 level at its new y (VIA23 is M2-M3).

Worked example A5 (M1.S.2 + V1.M1.EN.1 near x=6228, coordinated multi-object):
  M2 polygon (92x72 dbu, layer 20 = M2) at (6136,2304) moves to (6228,2312), delta (+92,+8).
  VIA12 at (6228,2340) moves to (6264,2348), delta (+36,+8).
  VIA23 at (6228,2340) moves to (6228,2348), delta (0,+8).
  Clears M1.S.2 at [6120,2296,6192,2384] and V1.M1.EN.1 at [6192,2304,6264,2376].
  Note: VIA12 and VIA23 WERE co-located (stacked) at (6228,2340) BEFORE the repair; the repair deliberately SPLIT them in x (+36 vs 0) while both shared the +8 y-delta -- the PARTIAL case of Step 4(c). Co-location before a repair does not imply co-movement during it (seed, reference-design-verified).

Connectivity preservation (Family A): the via's own M1/M2 lands travel with the instance, so the V1 cut stays within its lands (seed, reference-design-verified). Top-level M2 pads/routing are co-moved or end-extended so the via's M2 land stays merged with its net; the VIA23 level likewise keeps M2 AND M3 coverage. Via cell definitions are not touched; only instance placements and top-level M2/M3 polygons change (seed, reference-design-verified).

---

## Iteration 1 measured facts (Block3, channel unit_gate)

All 10 iteration-1 trials were gated_in with conn_preserved=true and zero new violations in-crop or out-of-crop (trial:i01.ug.Block3_union_row1.00 through trial:i01.ug.leaf_0013.09), confirming the Family A repair strategy applies across multiple unit types (union rows and leaf cells) in Block3.

**Pure instance moves**: Six trials across iterations 1-3 succeeded with no polygon operations at all -- trial:i01.ug.Block3_union_row2.01 (2 instances, +36 dbu x), trial:i01.ug.leaf_0006.04 (2 instances, +36 dbu x), trial:i01.ug.leaf_0009.07 (1 instance, +36 dbu x), trial:i01.ug.leaf_0013.09 (1 instance, -36 dbu x), trial:i02.ug.leaf_0001.00 (1 instance, -36 dbu x), trial:i03.ug.leaf_0003.02 (1 instance, -36 dbu x). Pure instance moves are sufficient when the existing routing metal already covers the via's new position without extension.

**Negative-direction move**: trial:i01.ug.leaf_0013.09, trial:i02.ug.leaf_0001.00, and trial:i03.ug.leaf_0003.02 all moved an instance by (-36,0) dbu and were accepted with conn_preserved=true. The direction of via relocation follows geometry, not a fixed-sign convention.

**Asymmetric resize_end**: When a polygon must be extended to cover the new via position, the resize_end delta on the polygon's edge differs from the instance's move delta. Observed pairs across iterations 1-2 -- trial:i01.ug.Block3_union_row1.00: move +136 dbu, resize +192 dbu; trial:i01.ug.leaf_0012.08: move +72 dbu, resize +108 dbu; trial:i01.ug.leaf_0007.05: move +36 dbu, resize +56 dbu; trial:i01.ug.leaf_0008.06 (x-axis pair): move +136 dbu, resize +92 dbu; trial:i02.ug.leaf_0002.01: move +104 dbu, resize +128 dbu. The polygon extension amount is set by the geometry of the original routing stub relative to the via's new position, not by a fixed multiplier of the via delta.

**Multiple instances with different deltas in one locus**: trial:i01.ug.Block3_union_row8.03 moves i0017 by (+108,0) dbu and i0016, i0019, i0021 each by (+72,0) dbu; their paired polygon resize_end values are 164, 128, 128, and 92 dbu respectively. Instances within the same locus are moved to their own required positions; a single delta does not apply uniformly when multiple vias are at different starting positions relative to their constraints.

**M3 involvement**: trial:i01.ug.leaf_0008.06 is the one iteration-1 trial with "M3" in touched_layers. It executes a y-axis polygon resize_end (+20 dbu, high end, polygon p1159) alongside x-axis instance moves of (+4,0) dbu and (+136,0) dbu. M3 coverage extension follows the axis of the via's movement: y-axis extension when the via moves in y (seed, reference-design-verified; worked example A4); x-axis extension when the via moves in x (seed, reference-design-verified; worked example A1). trial:i01.ug.leaf_0008.06 confirms this pattern holds at iteration 1.

**Instance-to-polygon pairing**: Each instance move in the measured data is paired with AT MOST one polygon resize_end (trial:i01.ug.Block3_union_row1.00: 3 moves paired 1:1 with 3 polygons; trial:i01.ug.Block3_union_row8.03: 4 moves paired 1:1 with 4 polygons; trial:i02.ug.leaf_0002.01: 1 move paired with 1 polygon). No trial pairs a single instance move with more than one polygon operation.

---

## Iteration 2 measured facts (Block3, channel unit_gate)

Both iteration-2 trials were gated_in with conn_preserved=true and zero new violations in-crop or out-of-crop (trial:i02.ug.leaf_0001.00, trial:i02.ug.leaf_0002.01), extending the confirmed Family A track record to 12 units across Block3 leaf cells and union rows.

**trial:i02.ug.leaf_0001.00**: Single pure instance move, i0233 by (-36,0) dbu, locus [7276,2268,7704,3132]. Touched layers M1, M2, V1. No polygon operations needed. Confirms pure-move sufficiency at a new leaf cell site, and further confirms negative-x direction validity.

**trial:i02.ug.leaf_0002.01**: Instance move i0239 by (+104,0) dbu paired with polygon p1226 resize_end on the x-axis high end by +128 dbu, locus [9232,5508,10080,6372]. Touched layers M1, M2, V1. Adds a new asymmetric resize_end data point (move +104, resize +128) at a move magnitude distinct from all iteration-1 values, reinforcing that the resize amount is geometry-driven per site.

---

## Iteration 3 measured facts (Block3, channel unit_gate)

**trial:i03.ug.leaf_0003.02**: Single pure instance move, i0099 by (-36,0) dbu, locus [1728,3148,11016,9812]. Touched layers M1, M2, V1. decision=gated_in, conn_preserved=true, n_new_in_crop=10, n_new_out_of_crop=0. No polygon operations were performed. The trial was accepted despite 10 new in-crop violations because conn_preserved=true and n_new_out_of_crop=0 (trial:i03.ug.leaf_0003.02). This establishes that n_new_out_of_crop=0 is the binding out-of-crop gate; n_new_in_crop may be non-zero in an accepted trial (trial:i03.ug.leaf_0003.02). The pure-move pattern at delta (-36,0) dbu and the negative-x direction are confirmed at a third distinct leaf cell site (trial:i03.ug.leaf_0003.02).

---

## Final-pair measured facts (reference-design tail evidence)

Provenance: these facts come from the final-pair comparison of the reference design's initial layout against its repaired final layout, plus the BEFORE and AFTER DRC reports. Every coordinate and delta cited in this document is quoted inline from that pair; the layout files themselves are not needed and are not shipped with this skill.

- Moving via instances without touching cell definitions is sufficient to clear V0.M1.AUX.3, V1.M1.EN.1, M1.S.2, and M1.S.6, provided metal polygons are co-moved or extended to maintain coverage (seed, reference-design-verified).

- A single via move can simultaneously clear violations under 3 different rules (seed, reference-design-verified; the A3 example: one VIA12 move clears V0.M1.AUX.3, V1.M1.EN.1, and M1.S.2 at once).

---

## Case notes

**Stacked via movement is a per-level decision, not a co-movement law** (seed, reference-design-verified). Verified modes from the final diff: COUPLED (the (5652,5220) pair moved together, +64 x), ANCHOR (VIA23 at (3204,1980) stayed while its VIA12 moved +136 x -- the VIA23 remains the M2-M3 anchor at the old position), PARTIAL (the (6228,2340) pair shared +8 y but split in x, +36 vs 0). The anchor-check gate -- after moving VIA12, does the V2 level at the OLD position still need VIA23 there to reach M3, and does VIA23's own alignment stay legal? -- must be evaluated before co-moving any stacked via (seed, reference-design-verified). Blindly co-moving every co-located VIA23 with its VIA12 contradicts the clean final pair (seed, reference-design-verified).

**Multi-rule single-fix frequency**: in the reference-design block, 3 out of 12 VIA12 moves each cleared violations from 2-3 distinct rules (seed, reference-design-verified). When spatial clustering shows overlapping violation bboxes from different rules at the same location, treat them as one compound fix. A single rule can also double-report one physical site through deck rule variants: the two M1.S.6 markers [6408,3457,6480,3499] and [6405,3464,6483,3492] outline the same corner pair, so marker count can exceed physical site count (seed, reference-design-verified).

**Gating criterion**: A trial is gated_in when conn_preserved=true and n_new_out_of_crop=0; n_new_in_crop may be non-zero without blocking acceptance (trial:i03.ug.leaf_0003.02, n_new_in_crop=10, decision=gated_in). Out-of-crop violations are the binding constraint; in-crop new violations are not (trial:i03.ug.leaf_0003.02).

**Cumulative scale**: 13 units repaired across Block3 union rows and leaf cells, 31 total operations (trial:i01.ug.Block3_union_row1.00 through trial:i03.ug.leaf_0003.02). Zero new out-of-crop violations across all 13 trials. Trial:i03.ug.leaf_0003.02 introduced 10 new in-crop violations and was accepted; all 12 prior trials introduced zero new in-crop violations. The Family A strategy generalizes across all unit types tested to date.