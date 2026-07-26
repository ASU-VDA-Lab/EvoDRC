## Per-rule recipes

### Family A: M1-via cluster (V0.M1.AUX.3, M1.S.2, M1.S.6, V1.M1.EN.1)

These four rules often cluster around a VIA_VIA12 instance placed where local M1 geometry fails width-matching, spacing, or enclosure constraints. A single site fires one to three of them -- not necessarily all four (seed). In the 37-violation example block, 18 of 37 violations belong to this family.

Rule semantics (ASAP7 rule deck):
- V0.M1.AUX.3: V0 y-extent matches M1 y-extent at the landing location; mismatch triggers the rule (seed).
- V1.M1.EN.1 (deck hgood/vgood construction; description "5 & 2 nm"): on ONE pair of opposite sides -- either the x-pair or the y-pair -- BOTH sides are checked for >= 2 nm (8 dbu) with at least ONE of the two needing >= 5 nm (20 dbu); the rule fires when NEITHER pair achieves this on the merged M1 (seed).
- M1.S.2: Tip-to-side spacing >= 25 nm (100 dbu) when one edge is <= 36 nm and the other > 36 nm.
- M1.S.6: Corner-to-corner spacing >= 20 nm (80 dbu).

Root cause pattern: A VIA_VIA12 is placed at a coordinate where the merged M1 has an edge mismatch or insufficient extension. Moving the via to a nearby M1-valid position or extending the M2-level routing can clear multiple rules at once; examples A2, A3, A5 each clear 2-3 rules per move and A1 and A4 each clear one rule (seed).

Recipe -- co-lateral via-and-pad slide (seed):

Step 1. For each violation in this family, locate the VIA_VIA12 instance whose bounding box overlaps or abuts the violation bbox.

Step 2. Determine the required lateral delta. V0.M1.AUX.3 ties V0 y-extent to M1 y-extent at the landing point; the new position satisfies this when the via lands on a region where M1 already has the matching width (seed). For V1.M1.EN.1, on ONE pair of opposite sides (x-pair or y-pair): BOTH sides >= 8 dbu AND at least one >= 20 dbu; the VIA_VIA12 cell's own M1 land supplies exactly 8 dbu on both y-sides (land y = +/-44 vs cut +/-36) but 0 on x, so the merged M1 needs either ONE y-side lifted to >= 20 dbu, or the x-pair to have >= 8 dbu on one side and >= 20 dbu on the other; the repairs targeted >= 20 dbu on BOTH x-sides, a conservative but sufficient target (seed). M1.S.2 and M1.S.6 clear incidentally when the via moves away from the proximity source (seed).

Step 3. Move the VIA_VIA12 instance by the determined delta (seed).

Step 4. For a co-located VIA_VIA23 (stacked via), the decision is per-level -- co-located vias do not always travel together (seed). Three verified modes:
  (a) COUPLED: if the M2 landing moves with the V1 fix, move VIA23 by the same delta. Verified: the stacked pair at (5652,5220) both moved +64 in x, together with the associated top-level M2 pad and M3 routing polygons (seed).
  (b) ANCHOR: if VIA23's M2-M3 levels remain correctly aligned at the original coordinate, leave VIA23 in place and move only VIA12. Verified: VIA12 (3204,1980)->(3340,1980) +136 x while co-located VIA23 stayed at (3204,1980) (seed).
  (c) PARTIAL: the two share one axis and split the other. Verified: at (6228,2340) both took +8 in y, but VIA12 took +36 in x while VIA23 took 0 (seed).
  Deciding question: after moving VIA12, does the V2 level at the OLD position still need VIA23 there to reach M3, and does VIA23's own alignment remain legal? If yes to both -- anchor case (seed). Co-location before a repair does not imply co-movement during it.

Step 5. Re-establish landing coverage at the via's new position. The via's own M1/M2 lands travel inside the instance; top-level M2 (layer 20) pads and routing polygons -- and M3 for the VIA23 level (Step 6) -- may need editing; zero top-level M1 (layer 19) polygons were touched in the reference-design repairs (seed). An isolated landing pad moves by the same delta; a pad attached to routing is reshaped or end-extended, with deltas that need not equal the via's (verified: the via at (6228,2340) moved (+36,+8) while its M2 pad moved (+92,+8); seed). Metal continuity is preserved throughout (seed).

Step 6. After any VIA23 move, BOTH levels (M2 and M3) require coverage at the via's new location (seed). Two verified modes:
  (a) Co-move: the polygon translates by the same delta as the via. Observed on both an M2 pad and an M3 routing polygon in example A1 (seed).
  (b) Extend: one edge is stretched to reach the new via position. Observed on M2 in example A2 and on M3 in example A4 (seed).
  Enclosure is checked on MERGED metal; the extent of a single polygon alone does not determine the enclosure result (seed).

Worked example A1 (V0.M1.AUX.3 at [5580,5220,5652,5292]):
  Via at (5652,5220); violation at boundary where V0 width != M1 width.
  Delta: (+64, 0) dbu = 16 nm in +x.
  VIA12 moves (5652,5220)->(5716,5220); VIA23 co-moves same delta.
  M2 landing pad polygon (92x72 dbu, layer 20 = M2) moves (5560,5184)->(5624,5184), same delta.
  M3 routing polygon (72x3156 dbu, layer 30 = M3) moves (5616,5184)->(5680,5184), same delta.

Worked example A2 (multi-rule single-move, delta +136 dbu in x):
  VIA12 at (3204,1980) moves to (3340,1980).
  Clears: V0.M1.AUX.3 at [3204,1980,3276,2052], V1.M1.EN.1 at [3168,1944,3240,2016], M1.S.2 at [3072,1936,3168,2024].
  M2 routing polygon (layer 20, at (2880,1944)-(3240,2016)) right edge extended from x=3240 to x=3336 (+96 dbu = 24 nm). No top-level M1 polygon was edited: the V1.M1.EN.1 violation clears because the relocated via's own M1 land merges with the M1 already present at the new position.

Worked example A3 (three-rule single-move, delta +136 dbu in x):
  VIA12 at (2340,3060) moves to (2476,3060).
  Clears: V0.M1.AUX.3 at [2340,3060,2412,3132], V1.M1.EN.1 at [2304,3024,2376,3096], M1.S.2 at [2208,3016,2304,3104].

Worked example A4 (V1.M1.EN.1 + M2 extend, delta (0,+68) dbu):
  VIA12 at (5364,5724) moves to (5364,5792); VIA23 co-moves same delta.
  Clears V1.M1.EN.1 at [5328,5688,5400,5760].
  M3 polygon (layer 30, at (5328,4896)-(5400,5760)) top edge extended from y=5760 to y=5816.

Worked example A5 (M1.S.2 + V1.M1.EN.1 near x=6228, coordinated multi-object):
  M2 polygon (92x72 dbu, layer 20) at (6136,2304) moves to (6228,2312), delta (+92,+8).
  VIA12 at (6228,2340) moves to (6264,2348), delta (+36,+8).
  VIA23 at (6228,2340) moves to (6228,2348), delta (0,+8).
  Clears M1.S.2 at [6120,2296,6192,2384] and V1.M1.EN.1 at [6192,2304,6264,2376].
  VIA12 and VIA23 were co-located before the repair; the repair split them in x (+36 vs 0) while sharing the +8 y-delta -- the PARTIAL case of Step 4(c).

Connectivity preservation (Family A): the via's own M1/M2 lands travel with the instance (seed). Top-level M2 pads/routing are co-moved or end-extended so the via's M2 land stays merged with its net; the VIA23 level keeps M2 AND M3 coverage. Via cell definitions are not touched; only instance placements and top-level M2/M3 polygons change.

---

### Family B: Bulk uniform via slide with M2 end-extension (V1 layer)

trial:i03.ug.whole_design.00 records a 16-op repair over the whole design (locus [0,0,16944,16944]) moving 8 V1 via instances uniformly +96 dbu (+24 nm) in x, with M2 polygon high-x edges extended by resize_end before each paired move_instance. Layers touched: M1, M2, V1. Connectivity preserved (trial:i03.ug.whole_design.00).

resize_end deltas observed in trial:i03.ug.whole_design.00: 116 dbu or 152 dbu, both exceeding the 96 dbu via move delta. The smaller delta (116 dbu) provides 20 dbu of margin past the via's new high-x boundary; the larger (152 dbu) provides 56 dbu. This excess ensures the M2 polygon's extended edge lies beyond the via at its new position, maintaining enclosure (trial:i03.ug.whole_design.00).

Op ordering in trial:i03.ug.whole_design.00: each resize_end precedes its paired move_instance in the op list. This sequencing places the extended M2 coverage at the destination before the via instance is repositioned there. Two of the 8 via moves -- instances i0404 and i0471 -- carry no paired resize_end, establishing that the resize step is needed only when the existing M2 polygon does not already reach the via's destination (trial:i03.ug.whole_design.00).

---

## Final-pair measured facts (reference-design tail evidence)

Provenance: these facts come from the final-pair comparison of the reference design's initial layout against its repaired final layout, plus the BEFORE and AFTER DRC reports. Every coordinate and delta cited from that pair is reference-design-verified.

- Moving via instances without touching cell definitions is sufficient to clear V0.M1.AUX.3, V1.M1.EN.1, M1.S.2, and M1.S.6, provided metal polygons are co-moved or extended to maintain coverage (reference-design-verified).

- A single via move can simultaneously clear violations under 3 different rules (confirmed by example A3: one VIA12 move clears V0.M1.AUX.3, V1.M1.EN.1, and M1.S.2 at once; reference-design-verified).

---

## Case notes (reference-design tail evidence)

Stacked via movement is a per-level decision, not a co-movement law. Verified modes from the final diff: COUPLED (the (5652,5220) pair moved together, +64 x), ANCHOR (VIA23 at (3204,1980) stayed while its VIA12 moved +136 x -- the VIA23 remains the M2-M3 anchor at the old position), PARTIAL (the (6228,2340) pair shared +8 y but split in x, +36 vs 0). The co-movement anti-pattern -- blindly moving every co-located VIA23 with its VIA12 -- contradicts the clean final pair; always run the anchor check before deciding (reference-design-verified).

Multi-rule single-fix frequency: in this block, 3 out of 12 VIA12 moves each cleared violations from 2-3 distinct rules (reference-design-verified). When spatial clustering shows overlapping violation bboxes from different rules at the same location, treating them as one compound fix is grounded in the multi-rule examples A2, A3, A5 (reference-design-verified). A single rule can double-report one physical site through deck rule variants: the two M1.S.6 markers [6408,3457,6480,3499] and [6405,3464,6483,3492] outline the same corner pair, so marker count can exceed physical site count.