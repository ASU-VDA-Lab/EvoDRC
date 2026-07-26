The records are already provided inline. I have everything needed to produce the corrected body.

---

## Per-rule recipes

### Family A: M1-via cluster (V0.M1.AUX.3, M1.S.2, M1.S.6, V1.M1.EN.1)

These four rules often cluster around a VIA_VIA12 instance placed where local M1 geometry fails width-matching, spacing, or enclosure constraints -- a single site usually fires one to three of them, not necessarily all four. In the 37-violation example block, 18 of 37 violations belong to this family (seed).

Rule semantics (ASAP7 rule deck). V0.M1.AUX.3: the V0 y-extent must equal the M1 y-extent at the landing location; M1 runs horizontally so the perpendicular direction is y (seed). V1.M1.EN.1 (deck hgood/vgood construction): on ONE pair of opposite sides -- either the x-pair or the y-pair -- BOTH sides must be >= 2 nm (8 dbu) AND at least ONE of the two >= 5 nm (20 dbu); fires when NEITHER pair achieves this on the merged M1 (seed). M1.S.2: tip-to-side spacing >= 25 nm (100 dbu) when one edge is <= 36 nm and the other > 36 nm (seed). M1.S.6: corner-to-corner spacing >= 20 nm (80 dbu) (seed).

Root cause pattern: a VIA_VIA12 (cell = M1 land + M2 land + V1 cut; it does NOT contain V0 -- V0 is the std-cell contact level below, and V0.M1.AUX.3 is checked on the MERGED M1 around it) is placed at a coordinate where the merged M1 has an edge mismatch or insufficient extension. Moving the via to a nearby M1-VALID position, or extending the M2-level routing, can clear multiple rules of this family at once (reference-design-verified). A pure-x delta of +72 dbu on a single VIA_VIA12 instance touching M1/M2/V1 introduced zero new violations and preserved connectivity (trial:i02.ug.leaf_0001.00).

**Recipe -- Co-lateral via-and-pad slide** (reference-design-verified):

Step 1. For each violation in this family, locate the VIA_VIA12 instance whose bounding box overlaps or abuts the violation bbox (seed).

Step 2. Determine the required lateral delta. On ONE pair of opposite sides (x-pair or y-pair) the merged M1 must satisfy: BOTH sides >= 8 dbu (2 nm) AND at least one >= 20 dbu (5 nm). The VIA_VIA12 cell's own M1 land supplies exactly 8 dbu on both y-sides (land y = +/-44 vs cut +/-36) but 0 on x, so the merged M1 must either lift one y-side to >= 20 dbu, or give the x-pair the required coverage. The repairs in this block aimed for >= 20 dbu on BOTH x-sides -- a conservative working target, sufficient but stricter than the rule minimum. M1.S.2 and M1.S.6 are incidentally cleared when the via moves away from the neighbor causing the tip/corner proximity (reference-design-verified).

Step 3. Apply the delta to VIA_VIA12. A single move_instance on the relevant via instance with a pure-x delta is sufficient when M2/V1 layers travel with the instance (trial:i02.ug.leaf_0001.00).

Step 4. If a VIA_VIA23 is co-located at the same (x, y) (stacked via), decide per level -- co-located vias do NOT always travel together (reference-design-verified):
- COUPLED case: if the M2 landing must move with the V1 fix, move VIA23 by the same delta (reference-design-verified).
- ANCHOR case: if VIA23's M2-M3 levels remain correctly aligned at the ORIGINAL coordinate, leave VIA23 in place and move only VIA12 (reference-design-verified).
- PARTIAL case: the two may share one axis and split the other (reference-design-verified).

The deciding question before any VIA23 move: after moving VIA12, does the V2 level at the OLD position still need VIA23 there to reach M3, and does VIA23's own alignment stay legal? If yes to both, use the anchor case (reference-design-verified).

Step 5. Re-establish landing coverage at the via's NEW position. The via's own M1/M2 lands travel inside the instance; what may need editing are the top-level M2 (layer 20) landing/routing polygons (and M3 for the VIA23 level). In this repair zero top-level M1 (layer 19) polygons were touched. An isolated landing pad can simply move by the same delta; a pad attached to a routing stub is typically reshaped or end-extended instead, and its delta need not equal the via's. Never break metal continuity in the process (reference-design-verified). Enclosure is checked on MERGED metal; a via move that brings the instance's own M1 land into contact with existing M1 at the new position closes V1.M1.EN.1 without any top-level M1 edit (reference-design-verified).

Step 6. After any VIA23 move, BOTH levels need coverage. If VIA23 now falls outside the M2 routing polygon, move or extend the M2 polygon to cover it; likewise verify the M3 side still covers the via at its new location. Two modes are observed on whichever affected level: co-move (polygon translates by the same delta as the via) and extend (one edge is stretched to reach the new via position) (reference-design-verified).

**Compound repairs: resize_end + multiple move_instance** (trial:i02.ug.leaf_0003.02): a 3-op repair touching M1/M2/M3/V1/V2 -- one resize_end (axis x, high end, -8 dbu on polygon p1410, group_D) combined with two move_instance ops (i0238 delta (-8,0) in group_D; i0213 delta (-36,0)) -- introduced 2 new in-crop violations but was accepted because conn_preserved=true. When a repair spans V1 and V2 levels and touches M2/M3 routing, the gate criterion is connectivity preservation, not zero new violations within the crop window (trial:i02.ug.leaf_0003.02).

---

### Worked examples (seed, reference-design-verified)

**Example W1** (V0.M1.AUX.3 at [5580,5220,5652,5292]): VIA12 at (5652,5220), delta (+64,0) dbu. VIA12 moves to (5716,5220); VIA23 co-moves same delta. M2 landing pad (92x72 dbu, layer 20) moves (5560,5184)->(5624,5184) same delta. M3 routing polygon (72x3156 dbu, layer 30) moves (5616,5184)->(5680,5184) same delta (reference-design-verified).

**Example W2** (multi-rule single-move, delta +136 dbu x): VIA12 at (3204,1980) moves to (3340,1980). Clears V0.M1.AUX.3 at [3204,1980,3276,2052], V1.M1.EN.1 at [3168,1944,3240,2016], M1.S.2 at [3072,1936,3168,2024]. M2 routing polygon (layer 20, at (2880,1944)-(3240,2016)) extended: right edge from x=3240 to x=3336 (+96 dbu = 24 nm). No top-level M1 polygon was edited: V1.M1.EN.1 closes because the relocated via's own M1 land merges with M1 already present at the new position (reference-design-verified).

**Example W3** (three-rule single-move, delta +136 dbu x): VIA12 at (2340,3060) moves to (2476,3060). Clears V0.M1.AUX.3 at [2340,3060,2412,3132], V1.M1.EN.1 at [2304,3024,2376,3096], M1.S.2 at [2208,3016,2304,3104] (reference-design-verified).

**Example W4** (V1.M1.EN.1 + M3 extend, delta (0,+68) dbu): VIA12 at (5364,5724) moves to (5364,5792); VIA23 co-moves same. Clears V1.M1.EN.1 at [5328,5688,5400,5760]. M3 polygon (layer 30, at (5328,4896)-(5400,5760)) top edge extended from y=5760 to y=5816 (reference-design-verified).

**Example W5** (M1.S.2 + V1.M1.EN.1, coordinated multi-object, partial via split): M2 polygon (92x72 dbu, layer 20) at (6136,2304) moves to (6228,2312), delta (+92,+8). VIA12 at (6228,2340) moves to (6264,2348), delta (+36,+8). VIA23 at (6228,2340) moves to (6228,2348), delta (0,+8). Clears M1.S.2 at [6120,2296,6192,2384] and V1.M1.EN.1 at [6192,2304,6264,2376]. VIA12 and VIA23 were co-located before the repair; the repair split them in x (+36 vs 0) while both shared the +8 y-delta -- the PARTIAL case. Co-location before a repair does not imply co-movement during it (reference-design-verified).

**Example W6** (single move_instance +72 dbu x, leaf_0001): VIA instance i0250 at locus [5344,3348,6192,4212], delta (+72,0) dbu, touching M1/M2/V1. Introduced 0 new violations. Conn_preserved=true. Gated in (trial:i02.ug.leaf_0001.00).

**Example W7** (3-op compound repair, leaf_0003): resize_end on p1410 (axis x, high end, -8 dbu, group_D) + move_instance i0238 (-8,0, group_D) + move_instance i0213 (-36,0), touching M1/M2/M3/V1/V2, locus [1728,3148,12960,11972]. Introduced 2 new in-crop violations; accepted because conn_preserved=true (trial:i02.ug.leaf_0003.02).

---

## Connectivity preservation

Moving via instances without touching cell definitions is sufficient to clear V0.M1.AUX.3, V1.M1.EN.1, M1.S.2, and M1.S.6, provided metal polygons are co-moved or extended to maintain coverage (reference-design-verified). A pure-x single-instance move on a V1-touching repair can preserve connectivity with zero new violations (trial:i02.ug.leaf_0001.00). A compound 3-op repair spanning V1/V2 and M1/M2/M3 may introduce in-crop violations and still be accepted when connectivity is preserved (trial:i02.ug.leaf_0003.02).

---

## Measured facts summary

- A single via move can simultaneously clear violations under 3 different rules (reference-design-verified, trial:i02.ug.leaf_0001.00 confirms the single-op pattern extends to iteration 2).
- A resize_end + multi-move repair touching 5 layers (M1/M2/M3/V1/V2) with 3 ops and a locus spanning nearly the full design extent was gated in when conn_preserved=true, even with 2 new in-crop violations (trial:i02.ug.leaf_0003.02).
- A single rule can double-report one physical site through deck rule variants: the two M1.S.6 markers [6408,3457,6480,3499] and [6405,3464,6483,3492] outline the same corner pair, so marker count can exceed physical site count (reference-design-verified).

---

## Case notes

Stacked via movement is a per-level decision, not a co-movement law. Verified modes from the final diff: COUPLED (the (5652,5220) pair moved together, +64 x), ANCHOR (VIA23 at (3204,1980) stayed while its VIA12 moved +136 x), PARTIAL (the (6228,2340) pair shared +8 y but split in x, +36 vs 0) (reference-design-verified). Blindly moving every co-located VIA23 with its VIA12 contradicts the clean final pair; check the anchor condition per level before co-moving (reference-design-verified).

Multi-rule single-fix frequency: in the reference block, 3 out of 12 VIA12 moves each cleared violations from 2-3 distinct rules. Overlapping violation bboxes from different rules at the same location signal a compound fix (reference-design-verified).

Gate criterion for compound multi-layer repairs: when a repair spans V1 and adjacent via levels (V2) and touches M2/M3 routing, the acceptance gate is connectivity preservation, not zero new in-crop violations (trial:i02.ug.leaf_0003.02).

Group-tagged ops travel together: in trial:i02.ug.leaf_0003.02, both the resize_end on p1410 and the move_instance on i0238 share group_D; the independent move on i0213 carries no group tag. Use group membership to identify which polygon and instance ops are coordinated on the same net segment.