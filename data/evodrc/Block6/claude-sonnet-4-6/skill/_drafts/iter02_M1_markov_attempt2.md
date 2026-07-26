## Per-rule recipes

### Family A: M1-via cluster (V0.M1.AUX.3, M1.S.2, M1.S.6, V1.M1.EN.1)

These four rules often cluster around a VIA_VIA12 instance placed where local M1
geometry fails width-matching, spacing, or enclosure constraints -- a single site
usually fires one to three of them, not all four (seed; the 37-violation example
block has 18 of 37 violations in this family spread across sites with 1-3 rules
each, not four simultaneously per site -- treat each clustered site individually
rather than assuming all four fire together).

Rule semantics (ASAP7 rule deck):
- V0.M1.AUX.3: The V0 y-extent must equal the M1 y-extent at the landing
  location (seed). Moves that realign the via with a correctly-sized M1 region
  clear this rule: in trial:i02.ug.Block6_union_row4.00 and
  trial:i02.ug.Block6_union_row8.02 multiple via instances were relocated in x
  and zero new violations were introduced, confirming that aligning to existing
  M1 geometry is the repair mechanism.
- V1.M1.EN.1 (deck hgood/vgood construction; description "5 & 2 nm"): on ONE
  pair of opposite sides -- either the x-pair or the y-pair -- BOTH sides must
  be >= 2 nm (8 dbu) AND at least ONE of the two >= 5 nm (20 dbu). Fires when
  NEITHER pair achieves this on the merged M1 (seed).
- M1.S.2: Tip-to-side spacing >= 25 nm (100 dbu) when one edge is <= 36 nm and
  the other > 36 nm (seed).
- M1.S.6: Corner-to-corner spacing >= 20 nm (80 dbu) (seed).

Root cause pattern: A VIA_VIA12 (cell = M1 land + M2 land + V1 cut; it does NOT
contain V0 -- V0 (layer 18) is the std-cell contact level below) is placed at a
coordinate where the merged M1 has an edge mismatch or insufficient extension.
Moving the via to a nearby M1-valid position or extending the M2-level routing
can clear multiple rules of this family at once (seed; examples A2 and A3 each
clear 3 rules with one via move; A1 and A4 each clear one rule -- both outcomes
are confirmed and neither is unusual).

Recipe -- Co-lateral via-and-pad slide:

Step 1. For each violation in this family, locate the VIA_VIA12 instance whose
  bounding box overlaps or abuts the violation bbox.
Step 2. Determine the required lateral delta:
  - The new position must satisfy: V0 y-extent == M1 y-extent at landing point
    for V0.M1.AUX.3 (seed). For V1.M1.EN.1 the deck requires, on ONE pair of
    opposite sides (x-pair or y-pair): BOTH sides >= 8 dbu (2 nm) AND at least
    one of them >= 20 dbu (5 nm). The VIA_VIA12 cell's own M1 land supplies
    exactly 8 dbu on both y-sides (land y = +/-44 vs cut +/-36) but 0 on x, so
    the merged M1 must either lift ONE y-side to >= 20 dbu, or give the x-pair
    (>= 8 dbu one side, >= 20 dbu the other). The repairs in this case aimed for
    >= 20 dbu on BOTH x-sides -- a conservative working target, sufficient but
    stricter than the rule minimum (seed). M1.S.2 and M1.S.6 are incidentally
    cleared when the via moves away from the neighbor causing tip/corner
    proximity (seed).
  - Iteration 2 confirms that pure x-moves achieve this: all four iteration-2
    trials used delta_dbu[1]=0 (trial:i02.ug.Block6_union_row4.00,
    trial:i02.ug.Block6_union_row7.01, trial:i02.ug.Block6_union_row8.02,
    trial:i02.ug.leaf_0004.04), and all four passed with zero new violations.
Step 3. Apply the delta to VIA_VIA12.
Step 4. If a VIA_VIA23 is co-located at the same (x, y) (stacked via), decide
  PER LEVEL -- co-located vias do NOT always travel together (seed):
  (a) COUPLED case: if the M2 landing must move with the V1 fix (the M2 polygon
      itself is co-moved), move VIA23 by the same delta (verified: the stacked
      pair at (5652,5220) both moved +64 in x, together with the associated
      TOP-LEVEL M2 pad and M3 routing polygons; the vias' own M1/M2 lands
      travel inside the instances -- no top-level M1 was involved) (seed).
  (b) ANCHOR case: if VIA23's own levels (M2-M3) remain correctly aligned at
      the ORIGINAL coordinate, leave VIA23 in place and move only VIA12
      (verified: VIA12 (3204,1980)->(3340,1980) +136 while the co-located
      VIA23 stayed at (3204,1980) as the M2-M3 anchor) (seed).
  (c) PARTIAL case: the two may share one axis and split the other (verified:
      at (6228,2340) both took +8 in y, but VIA12 took +36 in x while VIA23
      took 0) (seed).
  Pre-move check (the deciding question): after moving VIA12, does the V2 level
  at the OLD position still need VIA23 there to reach M3, and does VIA23's own
  alignment stay legal? If yes to both -> anchor case, leave it (seed).
Step 5. Re-establish LANDING coverage at the via's NEW position. The via's own
  M1/M2 lands travel inside the instance; what may need editing are the
  TOP-LEVEL M2 (layer 20) landing/routing polygons (and M3 for the VIA23 level,
  Step 6) -- zero top-level M1 (layer 19) polygons were touched in the seed
  repairs (seed). An ISOLATED landing pad can simply move by the same delta; a
  pad attached to routing is typically reshaped or end-extended, and its deltas
  need not equal the via's (seed; observed: the via at (6228,2340) moved (+36,+8)
  while its M2 pad moved (+92,+8)). In trial:i02.ug.Block6_union_row4.00 the
  single M2 resize_end (axis x, high end, +132 dbu on polygon p2020) combined
  with two via moves (i0319 +56 dbu, i0410 +112 dbu) achieved zero new violations.
  Metal continuity must not be broken in the process (seed).
Step 6. VIA_VIA23 is the M2-M3 via: after any VIA23 move, BOTH levels need
  coverage. Two modes are observed on whichever affected level (seed):
  (a) Co-move: the polygon translates by the same delta as the via (seed; observed
      on both an M2 pad and an M3 routing polygon in example A1).
  (b) Extend: one edge is stretched to reach the new via position (seed; observed
      on M2 in example A2 and on M3 in example A4).

Worked example A1 (V0.M1.AUX.3 at [5580,5220,5652,5292]):
  Via at (5652,5220); violation at boundary where V0 width != M1 width.
  Delta: (+64, 0) dbu = 16 nm in +x.
  VIA12 moves (5652,5220)->(5716,5220); VIA23 co-moves same delta.
  M2 landing pad polygon (92x72 dbu, layer 20 = M2) moves (5560,5184)->(5624,5184),
  same delta (this is VIA23's lower land level / VIA12's upper).
  M3 routing polygon (72x3156 dbu, layer 30 = M3) moves (5616,5184)->(5680,5184),
  same delta (VIA23's upper level). (seed)

Worked example A2 (multi-rule single-move, delta +136 dbu in x):
  VIA12 at (3204,1980) moves to (3340,1980).
  This single move clears:
    V0.M1.AUX.3 at [3204,1980,3276,2052]
    V1.M1.EN.1 at [3168,1944,3240,2016]
    M1.S.2 at [3072,1936,3168,2024] -- the marker ends exactly at the old M1
      land's left edge (3168, land y 1936..2024); the +136 move carries the
      land away from the tip-to-side conflict.
  M2 routing polygon (layer 20 = M2, at (2880,1944)-(3240,2016)) extended: right
  edge from x=3240 to x=3336 (+96 dbu = 24 nm) -- this re-covers the via's M2
  land at its new x. Zero top-level M1 polygons were edited: the V1.M1.EN.1 side
  closes because the RELOCATED via's own M1 land merges with the M1 already
  present at the new position. Enclosure is checked on MERGED metal; the final
  state is host-verified DRC-clean -- enclosure must not be re-derived from any
  single polygon in isolation (seed). (seed)

Worked example A3 (three-rule single-move, delta +136 dbu in x):
  VIA12 at (2340,3060) moves to (2476,3060).
  This single move clears:
    V0.M1.AUX.3 at [2340,3060,2412,3132]
    V1.M1.EN.1 at [2304,3024,2376,3096]
    M1.S.2 at [2208,3016,2304,3104] (seed)

Worked example A4 (V1.M1.EN.1 + M2 extend, delta (0,+68) dbu):
  VIA12 at (5364,5724) moves to (5364,5792); VIA23 co-moves same.
  Clears V1.M1.EN.1 at [5328,5688,5400,5760].
  M3 polygon (layer 30 = M3, at (5328,4896)-(5400,5760)) TOP edge extended from
  y=5760 to y=5816 to cover the via's M3 level at its new y (VIA23 is M2-M3).
  (seed)

Worked example A5 (M1.S.2 + V1.M1.EN.1 near x=6228, coordinated multi-object):
  M2 polygon (92x72 dbu, layer 20 = M2) at (6136,2304) moves to (6228,2312),
  delta (+92,+8).
  VIA12 at (6228,2340) moves to (6264,2348), delta (+36,+8).
  VIA23 at (6228,2340) moves to (6228,2348), delta (0,+8).
  Clears M1.S.2 at [6120,2296,6192,2384] and V1.M1.EN.1 at [6192,2304,6264,2376].
  Note: VIA12 and VIA23 were co-located (stacked) at (6228,2340) BEFORE the
  repair; the repair deliberately split them in x (+36 vs 0) while both shared
  the +8 y-delta -- the PARTIAL case of Step 4(c). Co-location before a repair
  does not imply co-movement during it (seed).

Connectivity preservation (Family A): the via's own M1/M2 lands travel with the
instance, so the V1 cut never leaves its lands. Top-level M2 pads/routing are
co-moved or end-extended so the via's M2 land stays merged with its net; the
VIA23 level likewise keeps M2 AND M3 coverage. Via cell definitions are not
touched; only instance placements and top-level M2/M3 polygons change (seed;
confirmed across all four iteration-2 trials: trial:i02.ug.Block6_union_row4.00,
trial:i02.ug.Block6_union_row7.01, trial:i02.ug.Block6_union_row8.02,
trial:i02.ug.leaf_0004.04 all report conn_preserved=true, touched_layers M1/M2/V1,
n_new_in_crop=0, n_new_out_of_crop=0).

---

## Iteration 2 measured facts

All four iteration-2 trials were gated_in with conn_preserved=true and zero new
violations in crop.

- Pure x-axis via moves (delta_dbu[1]=0) cleared violations in all four
  iteration-2 trials (trial:i02.ug.Block6_union_row4.00,
  trial:i02.ug.Block6_union_row7.01, trial:i02.ug.Block6_union_row8.02,
  trial:i02.ug.leaf_0004.04). No y-axis delta was needed in any of these cases.

- A via move of only +4 dbu (1 nm) in x is sufficient to clear violations when
  the site geometry places the conflict at that resolution (trial:i02.ug.Block6_union_row7.01,
  single op: move i0093 delta [4,0]).

- Multi-instance repairs within one unit crop succeed with zero new violations:
  trial:i02.ug.Block6_union_row4.00 used 3 ops (move i0319 +56 dbu, move i0410
  +112 dbu, resize_end p2020 x high +132 dbu) across a locus of width ~5264 dbu;
  trial:i02.ug.Block6_union_row8.02 used 2 ops (move i0213 +8 dbu, move i0071
  +36 dbu). Different via instances in the same crop can receive different x-deltas.

- A single resize_end on an M2 polygon (axis x, high end, +132 dbu on p2020)
  combined with two via moves is a confirmed repair pattern when M2 routing
  coverage must be extended after the vias shift (trial:i02.ug.Block6_union_row4.00).

- A single-instance pure x-move of +72 dbu clears the violation at unit leaf_0004
  (trial:i02.ug.leaf_0004.04, one op: move i0446 delta [72,0]).

---

## Final-pair measured facts (reference-design tail evidence)

Provenance: these facts come from the final-pair comparison of the reference
design's initial layout against its repaired final layout, plus the BEFORE and
AFTER DRC reports. Every coordinate and delta cited in this document is quoted
inline from that pair (seed, reference-design-verified).

- Moving via instances without touching cell definitions is sufficient to clear
  V0.M1.AUX.3, V1.M1.EN.1, M1.S.2, and M1.S.6, provided metal polygons are
  co-moved or extended to maintain coverage (seed, reference-design-verified).

- A single via move can simultaneously clear violations under 3 different rules
  (confirmed by example A3: one VIA12 move clears V0.M1.AUX.3, V1.M1.EN.1,
  and M1.S.2 at once) (seed, reference-design-verified).

---

## Case notes (reference-design tail evidence)

Multi-rule single-fix frequency: in this block, 3 out of 12 VIA12 moves each cleared
violations from 2-3 distinct rules (seed, reference-design-verified). When spatial
clustering shows overlapping violation bboxes from different rules at the same
location, treat them as one compound fix. A single rule can also double-report one
physical site through deck rule variants: the two M1.S.6 markers [6408,3457,6480,3499]
and [6405,3464,6483,3492] outline the same corner pair, so marker count can exceed
physical site count (seed, reference-design-verified).