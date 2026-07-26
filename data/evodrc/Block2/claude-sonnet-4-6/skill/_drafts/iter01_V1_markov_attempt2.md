## Per-rule recipes

### Family A: M1-via cluster (V0.M1.AUX.3, M1.S.2, M1.S.6, V1.M1.EN.1)

These four rules often cluster around a VIA_VIA12 instance placed where local M1 geometry fails width-matching, spacing, or enclosure constraints -- a single site usually fires one to three of them, not necessarily all four. In the 37-violation example block, 18 of 37 violations belong to this family (seed).

Rule semantics (ASAP7 rule deck):
- V0.M1.AUX.3: V0 y-extent must equal the M1 y-extent at the landing location (seed).
- V1.M1.EN.1 (deck hgood/vgood construction; description "5 & 2 nm"): on ONE pair of opposite sides -- either the x-pair or the y-pair -- BOTH sides must be >= 2 nm (8 dbu) AND at least ONE of the two >= 5 nm (20 dbu). Fires when NEITHER pair achieves this on the merged M1 (seed).
- M1.S.2: Tip-to-side spacing >= 25 nm (100 dbu) when one edge is <= 36 nm and the other > 36 nm (seed).
- M1.S.6: Corner-to-corner spacing >= 20 nm (80 dbu) (seed).

Root cause pattern: A VIA_VIA12 (cell = M1 land + M2 land + V1 cut; it does NOT contain V0 -- V0 (layer 18) is the std-cell contact level below, and V0.M1.AUX.3 is checked on the MERGED M1 around it) is placed at a coordinate where the merged M1 has an edge mismatch or insufficient extension. Moving the via to a nearby M1-VALID position -- observed moves include pure-x, pure-y, and two-axis -- or extending the M2-level routing can clear multiple rules of this family at once. Multi-instance crops where every affected via takes the same delta are normal: three instances all moved +64 x in a single repair (trial:i01.ug.Block2_union_row5.02); two instances both moved +36 x in another (trial:i01.ug.Block2_union_row1.00).

Recipe -- Co-lateral via-and-pad slide:

Step 1. For each violation in this family, locate the VIA_VIA12 instance whose bounding box overlaps or abuts the violation bbox (seed).

Step 2. Determine the required lateral delta: the via's new position must satisfy V0 y-extent == M1 y-extent at the landing point (V0.M1.AUX.3), and on ONE pair of opposite sides achieve BOTH sides >= 8 dbu AND at least one >= 20 dbu (V1.M1.EN.1). The repairs in the reference design aimed for >= 20 dbu on BOTH x-sides -- a conservative working target, sufficient but stricter than the rule minimum. M1.S.2 and M1.S.6 clear incidentally when the via moves away from the neighbor causing tip/corner proximity (seed, trial:i01.ug.leaf_0004.04, trial:i01.ug.leaf_0007.05).

Step 3. Apply the delta to VIA_VIA12. Pure x-axis moves (y-delta = 0) are sufficient in many sites; iteration 1 repairs used x-only deltas of 36, 64, and 128 dbu across all seven accepted trials (trial:i01.ug.Block2_union_row1.00, trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0001.03).

Step 4. If a VIA_VIA23 is co-located at the same (x, y) (stacked via), decide PER LEVEL -- co-located vias do NOT always travel together (seed):
  (a) COUPLED case: if the M2 landing must move with the V1 fix (the M2 polygon itself is co-moved), move VIA23 by the same delta (seed, verified: the stacked pair at (5652,5220) both moved +64 in x, together with the associated top-level M2 pad and M3 routing polygons).
  (b) ANCHOR case: if VIA23's own levels (M2-M3) remain correctly aligned at the ORIGINAL coordinate, leave VIA23 in place and move only VIA12 (seed, verified: VIA12 (3204,1980)->(3340,1980) +136 while the co-located VIA23 stayed at (3204,1980) as the M2-M3 anchor).
  (c) PARTIAL case: the two may share one axis and split the other (seed, verified: at (6228,2340) both took +8 in y, but VIA12 took +36 in x while VIA23 took 0).
  Pre-move check: after moving VIA12, if the V2 level at the OLD position still needs VIA23 there to reach M3 AND VIA23's own alignment stays legal, that is the anchor case -- do not move VIA23 (seed).

Step 5. Re-establish LANDING coverage at the via's NEW position. The via's own M1/M2 lands travel inside the instance; what may need editing are the TOP-LEVEL M2 (layer 20) landing/routing polygons and M3 for the VIA23 level -- in the reference-design repair ZERO top-level M1 (layer 19) polygons were touched. An ISOLATED landing pad can simply move by the same delta; a pad attached to a routing stub is typically reshaped or end-extended (resize_end) instead, and its delta need not equal the via's: the via at (6228,2340) moved (+36,+8) while its M2 pad moved (+92,+8) (seed); in iteration 1, a via moved +128 x while its covering polygons were extended +184 and +176 at their respective ends (trial:i01.ug.leaf_0001.03). Never break metal continuity in the process (seed, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.leaf_0011.06).

Step 6. VIA_VIA23 is the M2-M3 via: after any VIA23 move, BOTH levels need coverage. If it now falls outside the M2 routing polygon, move or extend the M2 polygon to cover it; likewise verify the M3 side still covers the via at its new location (seed). When the via stack extends to layers above M3 (e.g., M4), those higher-layer polygons must be adjusted to maintain coverage as well -- M4 was among the touched layers in a three-polygon repair that applied two resize_end ops with deltas differing from the via move delta (trial:i01.ug.leaf_0001.03).
  Two modes are observed, on whichever affected level (top-level M2 or M3):
  (a) Co-move: the polygon translates by the same delta as the via (seed).
  (b) Extend (resize_end): one edge is stretched to reach the new via position; the extension delta on the polygon can differ from the via's move delta (seed, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.leaf_0001.03).

Worked example A1 (V0.M1.AUX.3 at [5580,5220,5652,5292]):
  Via at (5652,5220); violation at boundary where V0 width != M1 width.
  Delta: (+64, 0) dbu = 16 nm in +x.
  VIA12 moves (5652,5220)->(5716,5220); VIA23 co-moves same delta.
  M2 landing pad polygon (92x72 dbu, layer 20 = M2) moves (5560,5184)->(5624,5184), same delta (this is VIA23's lower land level / VIA12's upper).
  M3 routing polygon (72x3156 dbu, layer 30 = M3) moves (5616,5184)->(5680,5184), same delta (VIA23's upper level) (seed).

Worked example A2 (multi-rule single-move, delta +136 dbu in x):
  VIA12 at (3204,1980) moves to (3340,1980).
  This single move clears:
    V0.M1.AUX.3 at [3204,1980,3276,2052]
    V1.M1.EN.1 at [3168,1944,3240,2016]
    M1.S.2 at [3072,1936,3168,2024] -- the marker ends exactly at the old M1 land's left edge (3168, land y 1936..2024); the +136 move carries the land away from the tip-to-side conflict.
  M2 routing polygon (layer 20 = M2, at (2880,1944)-(3240,2016)) extended: right edge from x=3240 to x=3336 (+96 dbu = 24 nm). NO top-level M1 polygon was edited: V1.M1.EN.1 closes because the RELOCATED via's own M1 land merges with the M1 already present at the new position. Enclosure is checked on MERGED metal; the final state is host-verified DRC-clean (seed).

Worked example A3 (three-rule single-move, delta +136 dbu in x):
  VIA12 at (2340,3060) moves to (2476,3060).
  This single move clears:
    V0.M1.AUX.3 at [2340,3060,2412,3132]
    V1.M1.EN.1 at [2304,3024,2376,3096]
    M1.S.2 at [2208,3016,2304,3104] (seed).

Worked example A4 (V1.M1.EN.1 + M3 extend, delta (0,+68) dbu):
  VIA12 at (5364,5724) moves to (5364,5792); VIA23 co-moves same.
  Clears V1.M1.EN.1 at [5328,5688,5400,5760].
  M3 polygon (layer 30 = M3, at (5328,4896)-(5400,5760)) TOP edge extended from y=5760 to y=5816 to cover the via's M3 level at its new y (seed).

Worked example A5 (M1.S.2 + V1.M1.EN.1 near x=6228, coordinated multi-object):
  M2 polygon (92x72 dbu, layer 20 = M2) at (6136,2304) moves to (6228,2312), delta (+92,+8).
  VIA12 at (6228,2340) moves to (6264,2348), delta (+36,+8).
  VIA23 at (6228,2340) moves to (6228,2348), delta (0,+8).
  Clears M1.S.2 at [6120,2296,6192,2384] and V1.M1.EN.1 at [6192,2304,6264,2376].
  VIA12 and VIA23 were co-located (stacked) at (6228,2340) BEFORE the repair; the repair deliberately split them in x (+36 vs 0) while both shared the +8 y-delta -- the PARTIAL case of Step 4(c). Co-location before a repair does not imply co-movement during it (seed).

Connectivity preservation (Family A): the via's own M1/M2 lands travel with the instance, so the V1 cut never leaves its lands. Top-level M2 pads/routing are co-moved or end-extended so the via's M2 land stays merged with its net; the VIA23 level likewise keeps M2 AND M3 coverage. Via cell definitions are not touched; only instance placements and top-level M2/M3 polygons change (seed).

---

## Iteration 1 measured facts

All 7 repairs in iteration 1 were accepted (decision=gated_in, conn_preserved=true, n_new_in_crop=0, n_new_out_of_crop=0) across Block2 rows and leaf cells (trial:i01.ug.Block2_union_row1.00, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0001.03, trial:i01.ug.leaf_0004.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0011.06).

Pure x-axis via moves (y-delta = 0) cleared V1-layer violations in all 7 iteration 1 cases. Observed x-deltas: 36 dbu (trial:i01.ug.Block2_union_row1.00, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.leaf_0004.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0011.06), 64 dbu (trial:i01.ug.Block2_union_row5.02), 128 dbu (trial:i01.ug.leaf_0001.03).

When a crop contains multiple via instances with the same violation pattern, all affected vias move by the same x-delta. Three instances (i0083, i0018, i0034) moved +64 x with two accompanying resize_end ops (trial:i01.ug.Block2_union_row5.02); two instances (i0159, i0152) moved +36 x with no polygon resizes (trial:i01.ug.Block2_union_row1.00).

A single instance move with no polygon resize is sufficient when the via's own lands provide complete coverage at the new position and no routing polygon needs extension. This occurred at n_ops=1 with +36 x (trial:i01.ug.leaf_0004.04, trial:i01.ug.leaf_0007.05).

resize_end op deltas are independent of the via move delta and must match the polygon's own coverage geometry. In trial:i01.ug.leaf_0001.03, the via (i0086) moved +128 x while polygon p1065 extended +184 at its high-x end and polygon p957 extended +176 at its low-x end. That trial also touched M4 in addition to M1, M2, V1 -- the only iteration 1 case where a layer above M3 appeared in touched_layers (trial:i01.ug.leaf_0001.03).

When a resize_end accompanies a via move and the routing polygon edge is adjacent to the via land, the resize_end delta equals the via move delta (trial:i01.ug.Block2_union_row3.01: p1040 extended +36 x alongside a +36 x via move; trial:i01.ug.Block2_union_row5.02: p1059 and p1057 each extended +64 x alongside +64 x via moves; trial:i01.ug.leaf_0011.06: p1052 extended +36 x alongside a +36 x via move).

---

## Final-pair measured facts (reference-design tail evidence)

Provenance: these facts come from the final-pair comparison of the reference design's initial layout against its repaired final layout, plus the BEFORE and AFTER DRC reports. Every coordinate and delta cited in this document is quoted inline from that pair; the layout files themselves are not needed and are not shipped with this skill.

Moving via instances without touching cell definitions is sufficient to clear V0.M1.AUX.3, V1.M1.EN.1, M1.S.2, and M1.S.6, provided metal polygons are co-moved or extended to maintain coverage (seed).

A single via move can simultaneously clear violations under 3 different rules: one VIA12 move clears V0.M1.AUX.3, V1.M1.EN.1, and M1.S.2 at once (seed, trial:i01.ug.Block2_union_row5.02 cleared violations across the same family with a five-operation coordinated fix).

---

## Case notes (reference-design tail evidence)

Stacked via movement is a PER-LEVEL decision, not a co-movement law. Verified modes from the final diff: COUPLED (the (5652,5220) pair moved together, +64 x), ANCHOR (VIA23 at (3204,1980) stayed while its VIA12 moved +136 x -- the VIA23 remains the M2-M3 anchor at the old position), PARTIAL (the (6228,2340) pair shared +8 y but split in x, +36 vs 0). Anti-pattern AP-1: blindly moving every co-located VIA23 with its VIA12 contradicts the clean final pair. The anchor check -- confirming whether VIA23's own alignment stays legal at the original coordinate before co-moving it -- must precede any stacked-via co-move decision (seed).

Multi-rule single-fix frequency: in the reference-design block, 3 out of 12 VIA12 moves each cleared violations from 2-3 distinct rules. When spatial clustering shows overlapping violation bboxes from different rules at the same location, treat them as one compound fix. A single rule can also double-report one physical site through deck rule variants: the two M1.S.6 markers [6408,3457,6480,3499] and [6405,3464,6483,3492] outline the same corner pair, so marker count can exceed physical site count (seed).