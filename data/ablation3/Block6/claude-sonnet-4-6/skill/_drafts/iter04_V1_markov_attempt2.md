## Per-rule recipes

### Family A: M1-via cluster (V0.M1.AUX.3, M1.S.2, M1.S.6, V1.M1.EN.1)

These four rules often cluster around a VIA_VIA12 instance placed where local M1 geometry fails width-matching, spacing, or enclosure constraints -- a single site usually fires one to three of them, not necessarily all four; in the 37-violation example block, 18 of 37 violations belong to this family (seed).

Rule semantics (ASAP7 rule deck). V0.M1.AUX.3: the V0 y-extent must equal the M1 y-extent at the landing location; M1 runs horizontally and perpendicular direction is y (seed). V1.M1.EN.1 (deck hgood/vgood; "5 & 2 nm"): on ONE pair of opposite sides -- either the x-pair or the y-pair -- BOTH sides must be >= 2 nm (8 dbu) AND at least ONE >= 5 nm (20 dbu); fires when NEITHER pair achieves this on the merged M1 (seed). M1.S.2: tip-to-side spacing >= 25 nm (100 dbu) when one edge is <= 36 nm and the other > 36 nm (seed). M1.S.6: corner-to-corner spacing >= 20 nm (80 dbu) (seed).

Root cause pattern: a VIA_VIA12 (cell = M1 land + M2 land + V1 cut; it does NOT contain V0 -- V0 (layer 18) is the std-cell contact level below, and V0.M1.AUX.3 is checked on the MERGED M1 around it) is placed at a coordinate where the merged M1 has an edge mismatch or insufficient extension. Moving the via to a nearby M1-VALID position -- observed moves include pure-x, pure-y (e.g. (0,+68)) and two-axis (e.g. the VIA12 at (5220,3060) relocated to (5292,2952), delta (+72,-108)) -- or extending the M2-level routing can clear multiple rules of this family at once. Worked examples A1 and A4 each clear ONE rule; A2, A3, A5 clear 2-3 rules per move; the four rules do not always clear together (seed).

Recipe -- Co-lateral via-and-pad slide:

Step 1. For each violation in this family, locate the VIA_VIA12 instance whose bounding box overlaps or abuts the violation bbox (seed).

Step 2. Determine the required lateral delta. The new position must place the V0 y-extent equal to the M1 y-extent at the landing point (V0.M1.AUX.3). For V1.M1.EN.1 the deck requires, on ONE pair of opposite sides (x-pair or y-pair): BOTH sides >= 8 dbu (2 nm) AND at least one of them >= 20 dbu (5 nm). The VIA_VIA12 cell's own M1 land supplies exactly 8 dbu on both y-sides (land y = +/-44 vs cut +/-36) but 0 on x, so the merged M1 needs either one y-side lifted to >= 20 dbu, or the x-pair given >= 8/20 dbu. The repairs in this case targeted >= 20 dbu on BOTH x-sides -- sufficient but stricter than the rule minimum. M1.S.2 and M1.S.6 are incidentally cleared when the via moves away from the neighbor causing tip/corner proximity (seed).

Step 3. Apply the delta to VIA_VIA12 (seed).

Step 4. If a VIA_VIA23 is co-located at the same (x, y) (stacked via), decide PER LEVEL -- co-located vias do NOT always travel together (seed):
  (a) COUPLED case: if the M2 landing moves with the V1 fix, move VIA23 by the same delta; the stacked pair at (5652,5220) both moved +64 in x, together with the associated TOP-LEVEL M2 pad and M3 routing polygons (seed).
  (b) ANCHOR case: if VIA23's own levels (M2-M3) remain correctly aligned at the ORIGINAL coordinate, leave VIA23 in place and move only VIA12; the VIA12 at (3204,1980) moved to (3340,1980) +136 while the co-located VIA23 stayed at (3204,1980) (seed).
  (c) PARTIAL case: the two may share one axis and split the other; at (6228,2340) both took +8 in y, but VIA12 took +36 in x while VIA23 took 0 (seed).
  The deciding question: after moving VIA12, does the V2 level at the OLD position still need VIA23 there to reach M3, and does VIA23's own alignment stay legal? If yes to both, VIA23 stays at the original coordinate (seed).

Step 5. Re-establish LANDING coverage at the via's NEW position -- the requirement is coverage, not a particular op. The via's own M1/M2 lands travel inside the instance; what may need editing are the TOP-LEVEL M2 (layer 20) landing/routing polygons (and M3 for the VIA23 level, Step 6) -- in this repair ZERO top-level M1 (layer 19) polygons were touched. An ISOLATED landing pad translates by the same delta; a pad attached to or part of a routing stub is typically reshaped or end-extended instead, and its deltas need not equal the via's (observed: the via at (6228,2340) moved (+36,+8) while its M2 pad moved (+92,+8)). Metal continuity must not be broken in the process (seed).

Step 6. VIA_VIA23 is the M2-M3 via: after any VIA23 move, BOTH levels need coverage. If it now falls outside the M2 routing polygon (layer M2), move or extend the M2 polygon to cover it; the M3 side must also cover the via at its new location (seed). Two observed modes:
  (a) Co-move: the polygon translates by the same delta as the via; observed on both an M2 pad and an M3 routing polygon in worked example A1 (seed).
  (b) Extend: one edge is stretched to reach the new via position; observed on M2 in example A2 and on M3 in example A4 (seed).

Worked example A1 (V0.M1.AUX.3 at [5580,5220,5652,5292]) (seed):
  Via at (5652,5220); violation at boundary where V0 width != M1 width.
  Delta: (+64, 0) dbu = 16 nm in +x.
  VIA12 moves (5652,5220)->(5716,5220); VIA23 co-moves same delta.
  M2 landing pad polygon (92x72 dbu, layer 20 = M2) moves (5560,5184)->(5624,5184), same delta (this is VIA23's lower land level / VIA12's upper).
  M3 routing polygon (72x3156 dbu, layer 30 = M3) moves (5616,5184)->(5680,5184), same delta (VIA23's upper level).

Worked example A2 (multi-rule single-move, delta +136 dbu in x) (seed):
  VIA12 at (3204,1980) moves to (3340,1980).
  This single move clears:
    V0.M1.AUX.3 at [3204,1980,3276,2052]
    V1.M1.EN.1 at [3168,1944,3240,2016]
    M1.S.2 at [3072,1936,3168,2024] -- the marker ends exactly at the old M1 land's left edge (3168, land y 1936..2024); the +136 move carries the land away from the tip-to-side conflict.
  M2 routing polygon (layer 20 = M2, at (2880,1944)-(3240,2016)) extended: right edge from x=3240 to x=3336 (+96 dbu = 24 nm). NO top-level M1 polygon was edited: the V1.M1.EN.1 side closes because the RELOCATED via's own M1 land merges with the M1 already present at the new position. Enclosure is checked on MERGED metal; re-deriving enclosure from any single polygon alone gives an incorrect result (reference-design-verified).

Worked example A3 (three-rule single-move, delta +136 dbu in x) (seed):
  VIA12 at (2340,3060) moves to (2476,3060).
  This single move clears:
    V0.M1.AUX.3 at [2340,3060,2412,3132]
    V1.M1.EN.1 at [2304,3024,2376,3096]
    M1.S.2 at [2208,3016,2304,3104]

Worked example A4 (V1.M1.EN.1 + M2 extend, delta (0,+68) dbu) (seed):
  VIA12 at (5364,5724) moves to (5364,5792); VIA23 co-moves same.
  Clears V1.M1.EN.1 at [5328,5688,5400,5760].
  M3 polygon (layer 30 = M3, at (5328,4896)-(5400,5760)) TOP edge extended from y=5760 to y=5816 to cover the via's M3 level at its new y (VIA23 is M2-M3).

Worked example A5 (M1.S.2 + V1.M1.EN.1 near x=6228, coordinated multi-object) (seed):
  M2 polygon (92x72 dbu, layer 20 = M2) at (6136,2304) moves to (6228,2312), delta (+92,+8).
  VIA12 at (6228,2340) moves to (6264,2348), delta (+36,+8).
  VIA23 at (6228,2340) moves to (6228,2348), delta (0,+8).
  Clears M1.S.2 at [6120,2296,6192,2384] and V1.M1.EN.1 at [6192,2304,6264,2376].
  VIA12 and VIA23 were co-located at (6228,2340) before the repair; the repair split them in x (+36 vs 0) while both shared the +8 y-delta -- PARTIAL case of Step 4(c). Co-location before a repair does not imply co-movement during it.

Connectivity preservation (Family A): the via's own M1/M2 lands travel with the instance, so the V1 cut never leaves its lands. Top-level M2 pads/routing are co-moved or end-extended so the via's M2 land stays merged with its net; the VIA23 level likewise keeps M2 AND M3 coverage. Via cell definitions are not touched; only instance placements and top-level M2/M3 polygons change (seed).

---

## Whole-design repair pass (iteration 4)

Trial i04.ug.whole_design.00 is a 20-op whole-design repair touching layers M1, M2, M4, M5, M6, V1, V4, V5; it was accepted with connectivity preserved and zero new violations introduced (trial:i04.ug.whole_design.00).

The 20 ops comprised 17 instance moves and 3 polygon resizes (p1920, p1923, p1990). All instance move deltas were x-axis only: groups at +80 dbu (9 instances: i0025, i0040, i0108, i0126, i0409, i0412, i0530, i0031, i0538), -96 dbu (3 instances: i0112, i0152, i0074), +96 dbu (2 instances: i0319, i0213), and -48 dbu (2 instances: i0015, i0471). The 3 polygon resizes each used axis x with delta 10 dbu (trial:i04.ug.whole_design.00).

Polygon resize ops (op="resize") on top-level metal polygons are a valid repair primitive alongside instance moves; the combination preserved connectivity across all 8 touched layers in this pass (trial:i04.ug.whole_design.00).

---

## Final-pair measured facts (reference-design tail evidence)

Provenance: these facts come from the final-pair comparison of the reference design's initial layout against its repaired final layout, plus the BEFORE and AFTER DRC reports (seed).

- Moving via instances without touching cell definitions is sufficient to clear V0.M1.AUX.3, V1.M1.EN.1, M1.S.2, and M1.S.6, provided metal polygons are co-moved or extended to maintain coverage (seed).

- A single via move can simultaneously clear violations under 3 different rules; one VIA12 move clears V0.M1.AUX.3, V1.M1.EN.1, and M1.S.2 at once, as confirmed by example A3 (seed).


## Case notes (reference-design tail evidence)

Stacked via movement is a PER-LEVEL decision, not a co-movement law. Verified modes from the final diff: COUPLED (the (5652,5220) pair moved together, +64 x), ANCHOR (VIA23 at (3204,1980) stayed while its VIA12 moved +136 x -- the VIA23 remains the M2-M3 anchor at the old position), PARTIAL (the (6228,2340) pair shared +8 y but split in x, +36 vs 0). Blindly moving every co-located VIA23 with its VIA12 contradicts the clean final pair; the anchor check must run before co-movement proceeds (reference-design-verified).

Multi-rule single-fix frequency: in this block, 3 out of 12 VIA12 moves each cleared violations from 2-3 distinct rules. When spatial clustering shows overlapping violation bboxes from different rules at the same location, treat them as one compound fix. A single rule can also double-report one physical site through deck rule variants: the two M1.S.6 markers [6408,3457,6480,3499] and [6405,3464,6483,3492] outline the same corner pair, so marker count can exceed physical site count (seed).