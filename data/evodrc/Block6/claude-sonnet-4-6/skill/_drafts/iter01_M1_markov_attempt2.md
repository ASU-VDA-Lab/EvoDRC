## Per-rule recipes

### Family A: M1-via cluster (V0.M1.AUX.3, M1.S.2, M1.S.6, V1.M1.EN.1)

These four rules often cluster around a VIA_VIA12 instance placed where local M1 geometry fails width-matching, spacing, or enclosure constraints -- a single site usually fires one to three of them, not necessarily all four. In the 37-violation example block, 18 of 37 violations belong to this family (seed, reference-design-verified).

Rule semantics (ASAP7 rule deck) (seed, reference-design-verified): V0.M1.AUX.3: V0 must exactly match M1 width perpendicular to M1 length. M1 runs horizontally; perpendicular direction is y. The V0 y-extent must equal the M1 y-extent at the landing location. V1.M1.EN.1 (deck hgood/vgood construction; description "5 & 2 nm"): on ONE pair of opposite sides -- either the x-pair or the y-pair -- BOTH sides must be >= 2 nm (8 dbu) AND at least ONE of the two >= 5 nm (20 dbu). Fires when NEITHER pair achieves this on the merged M1. M1.S.2: Tip-to-side spacing >= 25 nm (100 dbu) when one edge is <= 36 nm and the other > 36 nm. M1.S.6: Corner-to-corner spacing >= 20 nm (80 dbu).

Root cause pattern: A VIA_VIA12 (cell = M1 land + M2 land + V1 cut; it does NOT contain V0 -- V0 (layer 18) is the std-cell contact level below, and V0.M1.AUX.3 is checked on the MERGED M1 around it) is placed at a coordinate where the merged M1 has an edge mismatch or insufficient extension. Moving the via to a nearby M1-VALID position -- observed moves include pure-x, pure-y (e.g. (0,+68)) and two-axis (e.g. the VIA12 at (5220,3060) relocated to (5292,2952), delta (+72,-108)) -- or extending the M2-level routing (see Step 5 below) can clear multiple rules of this family at once (seed, reference-design-verified).

Recipe -- Co-lateral via-and-pad slide:

Step 1. For each violation in this family, locate the VIA_VIA12 instance whose bounding box overlaps or abuts the violation bbox.

Step 2. Determine the required lateral delta. The new position must satisfy: V0 y-extent == M1 y-extent at landing point (V0.M1.AUX.3); for V1.M1.EN.1 the deck requires, on ONE pair of opposite sides (x-pair or y-pair): BOTH sides >= 8 dbu (2 nm) AND at least one of them >= 20 dbu (5 nm). The VIA_VIA12 cell's own M1 land supplies exactly 8 dbu on both y-sides (land y = +/-44 vs cut +/-36) but 0 on x, so the merged M1 must either lift ONE y-side to >= 20 dbu, or give the x-pair (>= 8 dbu one side, >= 20 dbu the other). The repairs in this case aimed for >= 20 dbu on BOTH x-sides -- a CONSERVATIVE working target, sufficient but stricter than the rule minimum. M1.S.2 and M1.S.6 are incidentally cleared when the via moves away from the neighbor causing the tip/corner proximity (seed, reference-design-verified).

Step 3. Apply the delta to VIA_VIA12. Multiple instances requiring the same delta may be moved simultaneously in a single crop: trial:i01.ug.Block6_union_row3.00 moves instances i0471, i0324, i0481 each +72 dbu in x; trial:i01.ug.Block6_union_row5.01 moves instances i0015, i0459, i0437, i0446 each +36 dbu in x. Within one repair crop, different instances may move in opposite x-directions without breaking connectivity: trial:i01.ug.Block6_union_row7.02 moves i0093 at +104 dbu and i0074 at -36 dbu in the same crop.

Step 4. If a VIA_VIA23 is co-located at the same (x, y) (stacked via), decide PER LEVEL -- co-located vias do NOT always travel together (seed, reference-design-verified): (a) COUPLED case: if the M2 landing must move with the V1 fix, move VIA23 by the same delta (verified: stacked pair at (5652,5220) both moved +64 in x together with the associated TOP-LEVEL M2 pad and M3 routing polygons; the vias' own M1/M2 lands travel inside the instances -- no top-level M1 was involved) (seed, reference-design-verified). (b) ANCHOR case: if VIA23's own levels (M2-M3) remain correctly aligned at the ORIGINAL coordinate, LEAVE VIA23 in place and move only VIA12 (verified: VIA12 (3204,1980)->(3340,1980) +136 while the co-located VIA23 stayed at (3204,1980) as the M2-M3 anchor) (seed, reference-design-verified). (c) PARTIAL case: the two may share one axis and split the other (verified: at (6228,2340) both took +8 in y, but VIA12 took +36 in x while VIA23 took 0) (seed, reference-design-verified). Pre-move check (the deciding question): after moving VIA12, does the V2 level at the OLD position still need VIA23 there to reach M3, and does VIA23's own alignment stay legal? If yes to both -> anchor case, do not move it. Co-location before a repair does not imply co-movement during it (seed, reference-design-verified).

Step 5. Re-establish LANDING coverage at the via's NEW position -- the requirement is coverage, not a particular op (seed, reference-design-verified). The via's own M1/M2 lands travel inside the instance; what may need editing are the TOP-LEVEL M2 (layer 20) landing/routing polygons (and M3 for the VIA23 level, Step 6) -- in the reference-design repairs, ZERO top-level M1 (layer 19) polygons were touched. In all 8 iteration 1 repairs, only M1, M2, and V1 were modified; M3 was not required (trial:i01.ug.Block6_union_row3.00, trial:i01.ug.Block6_union_row5.01, trial:i01.ug.Block6_union_row7.02, trial:i01.ug.Block6_union_row8.03, trial:i01.ug.leaf_0001.04, trial:i01.ug.leaf_0011.05, trial:i01.ug.leaf_0015.06, trial:i01.ug.leaf_0018.07). An ISOLATED landing pad can simply move by the same delta; a pad attached to (or part of) a routing stub is reshaped or end-extended instead, and the resize_end delta need not equal the via's displacement: trial:i01.ug.leaf_0001.04 moves via i0404 by +112 dbu while polygon p2016 resize_end high-x extends +132 dbu; trial:i01.ug.Block6_union_row5.01 moves vias +36 dbu while polygon p2072 resize_end high-x extends +92 dbu; trial:i01.ug.leaf_0015.06 moves instances i0213, i0204 each +28 dbu while polygon p1923 resize_end high-x extends +48 dbu. When moves are bidirectional, polygon end extensions track their respective via (trial:i01.ug.Block6_union_row7.02: polygon p1903 resize_end high-x +124 dbu tracks i0093 at +104, polygon p1920 resize_end low-x +56 dbu tracks i0074 at -36). Never break metal continuity in the process (seed, reference-design-verified).

Step 6. VIA_VIA23 is the M2-M3 via: after any VIA23 move, BOTH levels need coverage (seed, reference-design-verified). If it now falls outside the M2 routing polygon (layer M2), move or extend the M2 polygon to cover it; likewise verify the M3 side still covers the via at its new location. Two modes are observed on whichever affected level (top-level M2 or M3) (seed, reference-design-verified): (a) Co-move: the polygon translates by the same delta as the via. (b) Extend: one edge is stretched to reach the new via position.

Worked example A1 (V0.M1.AUX.3 at [5580,5220,5652,5292]) (seed, reference-design-verified):
  Via at (5652,5220); violation at boundary where V0 width != M1 width.
  Delta: (+64, 0) dbu = 16 nm in +x.
  VIA12 moves (5652,5220)->(5716,5220); VIA23 co-moves same delta.
  M2 landing pad polygon (92x72 dbu, layer 20 = M2) moves (5560,5184)->(5624,5184), same delta.
  M3 routing polygon (72x3156 dbu, layer 30 = M3) moves (5616,5184)->(5680,5184), same delta.

Worked example A2 (multi-rule single-move, delta +136 dbu in x) (seed, reference-design-verified):
  VIA12 at (3204,1980) moves to (3340,1980).
  This single move clears: V0.M1.AUX.3 at [3204,1980,3276,2052]; V1.M1.EN.1 at [3168,1944,3240,2016]; M1.S.2 at [3072,1936,3168,2024] -- the marker ends exactly at the old M1 land's left edge (3168, land y 1936..2024); the +136 move carries the land away from the tip-to-side conflict.
  M2 routing polygon (layer 20 = M2, at (2880,1944)-(3240,2016)) extended: right edge from x=3240 to x=3336 (+96 dbu = 24 nm) -- this re-covers the via's M2 land at its new x.
  NO top-level M1 polygon was edited: the V1.M1.EN.1 side closes because the RELOCATED via's own M1 land merges with the M1 already present at the new position. Enclosure is checked on MERGED metal; do not re-derive enclosure from any single polygon alone (seed, reference-design-verified).

Worked example A3 (three-rule single-move, delta +136 dbu in x) (seed, reference-design-verified):
  VIA12 at (2340,3060) moves to (2476,3060).
  This single move clears: V0.M1.AUX.3 at [2340,3060,2412,3132]; V1.M1.EN.1 at [2304,3024,2376,3096]; M1.S.2 at [2208,3016,2304,3104].

Worked example A4 (V1.M1.EN.1 + M3 extend, delta (0,+68) dbu) (seed, reference-design-verified):
  VIA12 at (5364,5724) moves to (5364,5792); VIA23 co-moves same.
  Clears V1.M1.EN.1 at [5328,5688,5400,5760].
  M3 polygon (layer 30 = M3, at (5328,4896)-(5400,5760)) TOP edge extended from y=5760 to y=5816 to cover the via's M3 level at its new y.

Worked example A5 (M1.S.2 + V1.M1.EN.1 near x=6228, coordinated multi-object) (seed, reference-design-verified):
  M2 polygon (92x72 dbu, layer 20 = M2) at (6136,2304) moves to (6228,2312), delta (+92,+8).
  VIA12 at (6228,2340) moves to (6264,2348), delta (+36,+8).
  VIA23 at (6228,2340) moves to (6228,2348), delta (0,+8).
  Clears M1.S.2 at [6120,2296,6192,2384] and V1.M1.EN.1 at [6192,2304,6264,2376].
  VIA12 and VIA23 were co-located before the repair; the repair split them in x (+36 vs 0) while both shared +8 in y -- the PARTIAL case of Step 4(c).

Connectivity preservation (Family A): the via's own M1/M2 lands travel with the instance, so the V1 cut never leaves its lands (seed, reference-design-verified). Top-level M2 pads/routing are co-moved or end-extended so the via's M2 land stays merged with its net; the VIA23 level likewise keeps M2 AND M3 coverage. Via cell definitions are not touched; only instance placements and top-level M2/M3 polygons change.

---

## Iteration 1 measured records (Block6, unit_gate channel)

### Multi-instance simultaneous moves

Moving multiple via instances by the same delta in a single crop is valid and connectivity-preserving. Three instances moved together at +72 dbu in x (trial:i01.ug.Block6_union_row3.00: i0471, i0324, i0481, locus [5992,4428,9648,5292], zero new violations). Four instances moved together at +36 dbu in x with one polygon resize_end (trial:i01.ug.Block6_union_row5.01: i0015, i0459, i0437, i0446 at +36 dbu, p2072 resize_end high-x +92 dbu, locus [6856,6588,14832,7452], zero new violations).

### Bidirectional moves in one crop

A single repair crop may move different instances in opposite x-directions while preserving connectivity. Trial:i01.ug.Block6_union_row7.02 moves i0093 at +104 dbu and i0074 at -36 dbu within locus [8368,8748,14400,9612]; polygon p1903 resize_end high-x +124 dbu covers i0093's new position and polygon p1920 resize_end low-x +56 dbu covers i0074's new position; zero new violations introduced.

### Single-instance minimum-delta moves

Single-instance moves of +36 dbu (9 nm) in x clear violations in compact loci: trial:i01.ug.Block6_union_row8.03 (i0078, locus [7936,9828,11376,10692]); trial:i01.ug.leaf_0011.05 (i0066, locus [9072,8368,9756,8532]); trial:i01.ug.leaf_0018.07 (i0060, locus [9448,11988,9648,12852]). All three show zero new violations.

### Resize_end delta is independent of instance move delta

The polygon resize_end delta need not equal the instance displacement. Use the extension that re-covers the via's M2 land at its new position, not the via's own delta: trial:i01.ug.leaf_0001.04 moves i0404 by +112 dbu while p2016 resize_end high-x is +132 dbu; trial:i01.ug.Block6_union_row5.01 moves vias +36 dbu while p2072 resize_end high-x is +92 dbu; trial:i01.ug.leaf_0015.06 moves i0213 and i0204 each +28 dbu while p1923 resize_end high-x is +48 dbu. Applying the via delta directly to the polygon end would underextend in each of these cases.

### M3 layer not modified in iteration 1

All 8 iteration 1 repairs touched only M1, M2, and V1; M3 (layer 30) was not modified (trial:i01.ug.Block6_union_row3.00, trial:i01.ug.Block6_union_row5.01, trial:i01.ug.Block6_union_row7.02, trial:i01.ug.Block6_union_row8.03, trial:i01.ug.leaf_0001.04, trial:i01.ug.leaf_0011.05, trial:i01.ug.leaf_0015.06, trial:i01.ug.leaf_0018.07). The seed guidance that VIA23-level changes require M3 coverage checks when VIA23 is moved remains in force (seed, reference-design-verified); the iteration 1 sites did not require VIA23 moves.

---

## Final-pair measured facts (reference-design tail evidence)

Provenance: these facts come from the final-pair comparison of the reference design's initial layout against its repaired final layout, plus the BEFORE and AFTER DRC reports (seed, reference-design-verified). Every coordinate and delta cited in the seed worked examples is quoted inline from that pair.

- Moving via instances without touching cell definitions is sufficient to clear V0.M1.AUX.3, V1.M1.EN.1, M1.S.2, and M1.S.6, provided metal polygons are co-moved or extended to maintain coverage (seed, reference-design-verified; confirmed by all 8 iteration 1 trials: trial:i01.ug.Block6_union_row3.00, trial:i01.ug.Block6_union_row5.01, trial:i01.ug.Block6_union_row7.02, trial:i01.ug.Block6_union_row8.03, trial:i01.ug.leaf_0001.04, trial:i01.ug.leaf_0011.05, trial:i01.ug.leaf_0015.06, trial:i01.ug.leaf_0018.07).

- A single via move can simultaneously clear violations under 3 different rules (seed, reference-design-verified: A3 clears V0.M1.AUX.3, V1.M1.EN.1, and M1.S.2 in one VIA12 move).

- Multiple via instances can be moved together in one repair crop with zero new violations (trial:i01.ug.Block6_union_row3.00: 3 instances; trial:i01.ug.Block6_union_row5.01: 4 instances).

- Instances in the same repair crop may move in opposite x-directions without breaking connectivity, provided each via's M2 landing coverage is maintained by a corresponding polygon resize_end (trial:i01.ug.Block6_union_row7.02: +104 and -36 dbu in x).

---

## Case notes (reference-design tail evidence)

Multi-rule single-fix frequency: in this block, 3 out of 12 VIA12 moves each cleared violations from 2-3 distinct rules (seed, reference-design-verified). When spatial clustering shows overlapping violation bboxes from different rules at the same location, treat them as one compound fix.

A single rule can double-report one physical site through deck rule variants: the two M1.S.6 markers [6408,3457,6480,3499] and [6405,3464,6483,3492] outline the same corner pair, so marker count can exceed physical site count (seed, reference-design-verified).

Multi-instance crops expand the fix pattern: a single crop may move 3-4 instances simultaneously, all at the same delta, as confirmed in trial:i01.ug.Block6_union_row3.00 and trial:i01.ug.Block6_union_row5.01. Treat co-delta-group moves as one logical operation when assessing repair scope.