## Per-rule recipes

### Family A: M1-via cluster (V0.M1.AUX.3, M1.S.2, M1.S.6, V1.M1.EN.1)

These four rules often cluster around a VIA_VIA12 instance placed where local M1 geometry fails width-matching, spacing, or enclosure constraints (seed); a single site usually fires one to three of them -- the multi-rule examples (A2, A3, A5) clear 2-3 rules per move while A1 and A4 each clear one. In the 37-violation example block, 18 of 37 violations belong to this family. A single rule can also double-report one physical site through deck rule variants: the two M1.S.6 markers [6408,3457,6480,3499] and [6405,3464,6483,3492] outline the same corner pair, so marker count can exceed physical site count (seed).

Rule semantics (seed, reference-design-verified): V0.M1.AUX.3 -- V0 must exactly match M1 width perpendicular to M1 length; M1 runs horizontally so the perpendicular direction is y, and the V0 y-extent must equal the M1 y-extent at the landing location. V1.M1.EN.1 (deck hgood/vgood construction; description "5 & 2 nm") -- on ONE pair of opposite sides (x-pair or y-pair) BOTH sides must be >= 2 nm (8 dbu) AND at least ONE of the two >= 5 nm (20 dbu); fires when NEITHER pair achieves this on the merged M1. M1.S.2 -- tip-to-side spacing >= 25 nm (100 dbu) when one edge is <= 36 nm and the other > 36 nm. M1.S.6 -- corner-to-corner spacing >= 20 nm (80 dbu).

Root cause pattern (reference-design-verified): A VIA_VIA12 (cell = M1 land + M2 land + V1 cut; it does NOT contain V0 -- V0 (layer 18) is the std-cell contact level below, and V0.M1.AUX.3 is checked on the MERGED M1 around it) is placed at a coordinate where the merged M1 has an edge mismatch or insufficient extension. Moving the via to a nearby M1-VALID position -- observed moves include pure-x (A2, A3, A6), pure-y (A4: delta (0,+68)), and two-axis (A5: delta (+36,+8) for VIA12) -- or extending the M2-level routing clears violations from multiple rules at once.

---

Recipe -- Co-lateral via-and-pad slide:

Step 1 (seed). For each violation in this family, locate the VIA_VIA12 instance whose bounding box overlaps or abuts the violation bbox.

Step 2 (seed). Determine the required lateral delta. The new position must satisfy: V0 y-extent == M1 y-extent at landing point (V0.M1.AUX.3). For V1.M1.EN.1 the deck requires, on ONE pair of opposite sides (x-pair or y-pair): BOTH sides >= 8 dbu (2 nm) AND at least one of them >= 20 dbu (5 nm). The VIA_VIA12 cell's own M1 land supplies exactly 8 dbu on both y-sides (land y = +/-44 vs cut +/-36) but 0 on x, so the merged M1 must either lift ONE y-side to >= 20 dbu, or give the x-pair (>= 8 dbu one side, >= 20 dbu the other). The repairs aimed for >= 20 dbu on BOTH x-sides -- a conservative working target, sufficient but stricter than the rule minimum. M1.S.2 and M1.S.6 are incidentally cleared when the via moves away from the neighbor causing the tip/corner proximity.

Step 3 (seed). Apply the delta to VIA_VIA12.

Step 4 (seed). If a VIA_VIA23 is co-located at the same (x, y) (stacked via), decide PER LEVEL -- co-located vias do NOT always travel together: (a) COUPLED case: if the M2 landing must move with the V1 fix, move VIA23 by the same delta (verified: the stacked pair at (5652,5220) both moved +64 in x, together with the associated TOP-LEVEL M2 pad and M3 routing polygons; the vias' own M1/M2 lands travel inside the instances -- no top-level M1 was involved). (b) ANCHOR case: if VIA23's own levels (M2-M3) remain correctly aligned at the ORIGINAL coordinate, leave VIA23 in place and move only VIA12 (verified: VIA12 (3204,1980)->(3340,1980) +136 while the co-located VIA23 stayed at (3204,1980) as the M2-M3 anchor). (c) PARTIAL case: the two may share one axis and split the other (verified: at (6228,2340) both took +8 in y, but VIA12 took +36 in x while VIA23 took 0). Deciding question: after moving VIA12, does the V2 level at the OLD position still need VIA23 there to reach M3, and does VIA23's own alignment stay legal? If yes to both, that is the anchor case; the final clean pair shows this anchor pattern explicitly (reference-design-verified).

Step 5 (seed). Re-establish landing coverage at the via's NEW position -- coverage is what the rule checks, not the specific op. The via's own M1/M2 lands travel inside the instance; what may need editing are the TOP-LEVEL M2 (layer 20) landing/routing polygons (and M3 for the VIA23 level, Step 6) -- in this repair ZERO top-level M1 (layer 19) polygons were touched. An ISOLATED landing pad can move by the same delta; a pad attached to a routing stub is reshaped or end-extended instead, and its deltas need not equal the via's (observed: the via at (6228,2340) moved (+36,+8) while its M2 pad moved (+92,+8)). Metal continuity must be maintained: never create a gap in the via's net (reference-design-verified).

Step 6 (seed). VIA_VIA23 is the M2-M3 via: after any VIA23 move, BOTH levels need coverage. If it falls outside the M2 routing polygon (layer M2), move or extend the M2 polygon to cover it; likewise verify the M3 side still covers the via at its new location (M3 coverage loss is a connectivity break the window DRC does not flag). Two observed modes on whichever affected level: (a) Co-move: the polygon translates by the same delta as the via (A1, both M2 pad and M3 routing polygon). (b) Extend: one edge is stretched to reach the new via position (M2 in A2 and in trial:i02.ug.leaf_0001.00; M3 in A4).

---

Worked example A1 (V0.M1.AUX.3 at [5580,5220,5652,5292]) (reference-design-verified):
  Via at (5652,5220); violation at boundary where V0 width != M1 width.
  Delta: (+64, 0) dbu = 16 nm in +x.
  VIA12 moves (5652,5220)->(5716,5220); VIA23 co-moves same delta.
  M2 landing pad polygon (92x72 dbu, layer 20 = M2) moves (5560,5184)->(5624,5184), same delta (this is VIA23's lower land level / VIA12's upper).
  M3 routing polygon (72x3156 dbu, layer 30 = M3) moves (5616,5184)->(5680,5184), same delta (VIA23's upper level).

Worked example A2 (multi-rule single-move, delta +136 dbu in x) (reference-design-verified):
  VIA12 at (3204,1980) moves to (3340,1980). This single move clears: V0.M1.AUX.3 at [3204,1980,3276,2052]; V1.M1.EN.1 at [3168,1944,3240,2016]; M1.S.2 at [3072,1936,3168,2024] -- the marker ends exactly at the old M1 land's left edge (3168, land y 1936..2024); the +136 move carries the land away from the tip-to-side conflict. M2 routing polygon (layer 20 = M2, at (2880,1944)-(3240,2016)) extended: right edge from x=3240 to x=3336 (+96 dbu = 24 nm) -- this re-covers the via's M2 land at its new x. ZERO top-level M1 polygons were edited: the V1.M1.EN.1 violation closes because the RELOCATED via's own M1 land merges with the M1 already present at the new position. Enclosure is checked on MERGED metal; do not re-derive enclosure from any single polygon alone (reference-design-verified; final state host-verified DRC-clean).

Worked example A3 (three-rule single-move, delta +136 dbu in x) (reference-design-verified):
  VIA12 at (2340,3060) moves to (2476,3060). This single move clears: V0.M1.AUX.3 at [2340,3060,2412,3132]; V1.M1.EN.1 at [2304,3024,2376,3096]; M1.S.2 at [2208,3016,2304,3104].

Worked example A4 (V1.M1.EN.1 + M3 extend, delta (0,+68) dbu) (reference-design-verified):
  VIA12 at (5364,5724) moves to (5364,5792); VIA23 co-moves same delta.
  Clears V1.M1.EN.1 at [5328,5688,5400,5760].
  M3 polygon (layer 30 = M3, at (5328,4896)-(5400,5760)) TOP edge extended from y=5760 to y=5816 to cover the via's M3 level at its new y (VIA23 is M2-M3).

Worked example A5 (M1.S.2 + V1.M1.EN.1 near x=6228, coordinated multi-object) (reference-design-verified):
  M2 polygon (92x72 dbu, layer 20 = M2) at (6136,2304) moves to (6228,2312), delta (+92,+8).
  VIA12 at (6228,2340) moves to (6264,2348), delta (+36,+8).
  VIA23 at (6228,2340) moves to (6228,2348), delta (0,+8).
  Clears M1.S.2 at [6120,2296,6192,2384] and V1.M1.EN.1 at [6192,2304,6264,2376].
  VIA12 and VIA23 were co-located (stacked) before this repair; the repair deliberately split them in x (+36 vs 0) while both shared the +8 y-delta -- the PARTIAL case of Step 4(c). Co-location before a repair does not imply co-movement during it (reference-design-verified).

Worked example A6 (pure-x via move + M2 high-end extension; trial:i02.ug.leaf_0001.00):
  Locus [5344,5508,6192,6372], layers M1, M2, V1.
  Instance i0300 (VIA_VIA12) moved +100 dbu in x.
  M2 polygon p1385: high-x edge extended +60 dbu (resize_end, axis x, end high).
  conn_preserved: true; decision: gated_in.
  Pattern matches Step 6 mode (b) -- extend: the via moves +100 in x while the top-level M2 polygon's high-x edge stretches +60 to maintain overlap with the via's M2 land at its new position. The via delta and the polygon delta differ, consistent with the pattern seen in A2 (+136 via vs +96 M2 extension) and A5 (+36/+8 via vs +92/+8 M2 pad move).

---

## Final-pair measured facts

Moving via instances without touching cell definitions is sufficient to clear V0.M1.AUX.3, V1.M1.EN.1, M1.S.2, and M1.S.6, provided metal polygons are co-moved or extended to maintain coverage (reference-design-verified).

A single via move can simultaneously clear violations under 3 different rules, confirmed by A3: one VIA12 move clears V0.M1.AUX.3, V1.M1.EN.1, and M1.S.2 at once (reference-design-verified).

The via delta and the M2 extension delta need not be equal: differences observed in A2 (+136 vs +96), A5 (+36 via vs +92 M2 pad in x), and trial:i02.ug.leaf_0001.00 (+100 via vs +60 M2 extension).

---

## Case notes

Stacked via movement is a PER-LEVEL decision, not a co-movement law (reference-design-verified). Verified modes from the final diff: COUPLED (the (5652,5220) pair moved together, +64 x), ANCHOR (VIA23 at (3204,1980) stayed while its VIA12 moved +136 x -- the VIA23 remains the M2-M3 anchor at the old position), PARTIAL (the (6228,2340) pair shared +8 y but split in x, +36 vs 0). Anti-pattern AP-1: co-moving every co-located VIA23 with its VIA12 contradicts the clean final pair; always run the anchor check (deciding question in Step 4) before co-moving (reference-design-verified).

Multi-rule single-fix frequency: in this block, 3 out of 12 VIA12 moves each cleared violations from 2-3 distinct rules (reference-design-verified). When spatial clustering shows overlapping violation bboxes from different rules at the same location, treat them as one compound fix.