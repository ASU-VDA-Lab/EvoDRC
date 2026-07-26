## Per-rule recipes

### Family A: M1-via cluster (V0.M1.AUX.3, M1.S.2, M1.S.6, V1.M1.EN.1)

These four rules often cluster around a VIA_VIA12 instance placed where local M1
geometry fails width-matching, spacing, or enclosure constraints -- a single site
usually fires one to three of them, not necessarily all four. In the 37-violation
example block, 18 of 37 violations belong to this family.

Rule semantics (ASAP7 rule deck):
- V0.M1.AUX.3: V0 must exactly match M1 width perpendicular to M1 length. M1 runs
  horizontally; perpendicular direction is y. The V0 y-extent must equal the M1
  y-extent at the landing location.
- V1.M1.EN.1 (deck hgood/vgood construction; description "5 & 2 nm"): on ONE
  pair of opposite sides -- either the x-pair or the y-pair -- BOTH sides must
  be >= 2 nm (8 dbu) AND at least ONE of the two >= 5 nm (20 dbu). Fires when
  NEITHER pair achieves this on the merged M1.
- M1.S.2: Tip-to-side spacing >= 25 nm (100 dbu) when one edge is <= 36 nm and
  the other > 36 nm.
- M1.S.6: Corner-to-corner spacing >= 20 nm (80 dbu).

Root cause pattern: A VIA_VIA12 (cell = M1 land + M2 land + V1 cut; it does NOT
contain V0 -- V0 (layer 18) is the std-cell contact level below, and V0.M1.AUX.3
is checked on the MERGED M1 around it) is placed at a coordinate where the merged
M1 has an edge mismatch or insufficient extension. Moving the via to a nearby
M1-VALID position -- observed moves include pure-x (all gated-in iteration 1 trials
use x-only deltas with dy=0) and two-axis (e.g. the VIA12 at (5220,3060) relocated
to (5292,2952), delta (+72,-108) in the seed) -- or extending the M2-level routing
can clear multiple rules of this family at once.

Recipe -- Co-lateral via-and-pad slide:

Step 1. For each violation in this family, locate the VIA_VIA12 instance whose
  bounding box overlaps or abuts the violation bbox.
Step 2. Determine the required lateral delta:
  - The new position must satisfy: V0 y-extent == M1 y-extent at landing point
    (V0.M1.AUX.3). For V1.M1.EN.1 the deck requires, on ONE pair of opposite
    sides (x-pair or y-pair): BOTH sides >= 8 dbu (2 nm) AND at least one of
    them >= 20 dbu (5 nm). The VIA_VIA12 cell's own M1 land supplies exactly
    8 dbu on both y-sides (land y = +/-44 vs cut +/-36) but 0 on x, so the
    merged M1 must either lift ONE y-side to >= 20 dbu, or give the x-pair
    (>= 8 dbu one side, >= 20 dbu the other). The repairs in this case aimed
    for >= 20 dbu on BOTH x-sides -- a CONSERVATIVE working target, sufficient
    but stricter than the rule minimum. M1.S.2 and M1.S.6 are incidentally
    cleared when the via moves away from the neighbor that was causing the
    tip/corner proximity.
  - Both +x and -x directions are valid: iteration 1 confirms negative x deltas
    clear violations when the via needs to move away from a right-side conflict
    (trial:i01.ug.Block1_union_row5.05 with delta -36, trial:i01.ug.Block1_union_row6.06
    with delta -72, trial:i01.ug.leaf_0020.10 with delta -56).
Step 3. Apply the delta to VIA_VIA12. Multiple vias in the same locus may each
  require different deltas, including opposing directions within the same fix
  (trial:i01.ug.Block1_union_row6.06 applies +72 to four instances and -72 to
  one within the same locus; trial:i01.ug.Block1_union_row8.07 applies +64, +136,
  -64, +136, +64 to five instances in one locus).
Step 4. If a VIA_VIA23 is co-located at the same (x, y) (stacked via), decide
  PER LEVEL -- co-located vias do NOT always travel together:
  (a) COUPLED case: if the M2 landing must move with the V1 fix (the M2 polygon
      itself is co-moved), move VIA23 by the same delta (verified: the stacked
      pair at (5652,5220) both moved +64 in x, together with the associated
      TOP-LEVEL M2 pad and M3 routing polygons; the vias' own M1/M2 lands
      travel inside the instances -- no top-level M1 was involved).
  (b) ANCHOR case: if VIA23's own levels (M2-M3) remain correctly aligned at
      the ORIGINAL coordinate, LEAVE VIA23 in place and move only VIA12
      (verified: VIA12 (3204,1980)->(3340,1980) +136 while the co-located
      VIA23 stayed at (3204,1980) as the M2-M3 anchor).
  (c) PARTIAL case: the two may share one axis and split the other (verified:
      at (6228,2340) both took +8 in y, but VIA12 took +36 in x while VIA23
      took 0).
  Pre-move check (the deciding question): after moving VIA12, does the V2 level
  at the OLD position still need VIA23 there to reach M3, and does VIA23's own
  alignment stay legal? If yes to both -> anchor case, do not move it. The final
  clean pair shows this anchor pattern explicitly: the VIA12 moved while the
  co-located VIA23 stayed at the original M2-M3 landing.
Step 5. Re-establish LANDING coverage at the via's NEW position -- the
  requirement is coverage, not a particular op. The via's own M1/M2 lands
  travel inside the instance; what may need editing are the TOP-LEVEL M2
  (layer 20) landing/routing polygons (and M3 for the VIA23 level, Step 6) --
  in this repair ZERO top-level M1 (layer 19) polygons were touched.
  - A resize_end on the M2 polygon is NOT always required: many gated-in repairs
    move vias without any M2 polygon edit when the existing M2 polygon already
    extends to cover the via's new land position
    (trial:i01.ug.Block1_union_row10.01, trial:i01.ug.Block1_union_row3.03,
    trial:i01.ug.Block1_union_row4.04, trial:i01.ug.Block1_union_row9.08,
    trial:i01.ug.leaf_0004.09, trial:i01.ug.leaf_0020.10). Only extend when
    a gap opens between the M2 polygon edge and the via's new land.
  - When a resize_end IS needed: the extension delta need not equal the via move
    delta. Calculate the required extension from the distance between the M2
    polygon edge and the via's new land boundary. Observed mismatches:
    trial:i01.ug.Block1_union_row5.05 via +136 -> M2 resize_end +156 (+20 extra);
    trial:i01.ug.Block1_union_row8.07 via +136 -> M2 resize_end +192 (+56 extra);
    trial:i01.ug.Block1_union_row6.06 via +72 -> M2 resize_end +128 (+56 extra).
  - Resize_end direction follows via move direction: when the via moves +x, extend
    the high (right) end of the M2 polygon; when the via moves -x, extend the low
    (left) end (trial:i01.ug.Block1_union_row5.05 with via delta -36 paired with
    M2 resize_end end="low" +56).
  - An ISOLATED landing pad can simply move by the same delta; a pad attached to
    (or part of) a routing stub is typically reshaped or end-extended instead,
    and its deltas need not equal the via's (observed: the via at (6228,2340)
    moved (+36,+8) while its M2 pad moved (+92,+8)). Never break metal
    continuity in the process.
Step 6. VIA_VIA23 is the M2-M3 via: after any VIA23 move, BOTH levels need
  coverage. If it now falls outside the M2 routing polygon (layer M2), move or
  extend the M2 polygon to cover it; likewise verify the M3 side still covers
  the via at its new location (M3 coverage loss is a connectivity break the
  window DRC may not flag).
  Two modes are observed, on WHICHEVER affected level (top-level M2 or M3):
  (a) Co-move: the polygon translates by the same delta as the via (observed on
      both an M2 pad and an M3 routing polygon in worked example A1).
  (b) Extend: one edge is stretched to reach the new via position (observed on
      M2 in example A2 and on M3 in example A4).

Worked example A1 (V0.M1.AUX.3 at [5580,5220,5652,5292]):
  Via at (5652,5220); violation at boundary where V0 width != M1 width.
  Delta: (+64, 0) dbu = 16 nm in +x.
  VIA12 moves (5652,5220)->(5716,5220); VIA23 co-moves same delta.
  M2 landing pad polygon (92x72 dbu, layer 20 = M2) moves (5560,5184)->(5624,5184),
  same delta (this is VIA23's lower land level / VIA12's upper).
  M3 routing polygon (72x3156 dbu, layer 30 = M3) moves (5616,5184)->(5680,5184),
  same delta (VIA23's upper level).

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
  land at its new x. NO top-level M1 polygon was edited: the V1.M1.EN.1 side
  closes because the RELOCATED via's own M1 land merges with the M1 already
  present at the new position. (Enclosure is checked on MERGED metal; the final
  state is host-verified DRC-clean. Do not re-derive enclosure from any single
  polygon alone.)

Worked example A3 (three-rule single-move, delta +136 dbu in x):
  VIA12 at (2340,3060) moves to (2476,3060).
  This single move clears:
    V0.M1.AUX.3 at [2340,3060,2412,3132]
    V1.M1.EN.1 at [2304,3024,2376,3096]
    M1.S.2 at [2208,3016,2304,3104]

Worked example A4 (V1.M1.EN.1 + M2 extend, delta (0,+68) dbu):
  VIA12 at (5364,5724) moves to (5364,5792); VIA23 co-moves same.
  Clears V1.M1.EN.1 at [5328,5688,5400,5760].
  M3 polygon (layer 30 = M3, at (5328,4896)-(5400,5760)) TOP edge extended from
  y=5760 to y=5816 to cover the via's M3 level at its new y (VIA23 is M2-M3).

Worked example A5 (M1.S.2 + V1.M1.EN.1 near x=6228, coordinated multi-object):
  M2 polygon (92x72 dbu, layer 20 = M2) at (6136,2304) moves to (6228,2312),
  delta (+92,+8).
  VIA12 at (6228,2340) moves to (6264,2348), delta (+36,+8).
  VIA23 at (6228,2340) moves to (6228,2348), delta (0,+8).
  Clears M1.S.2 at [6120,2296,6192,2384] and V1.M1.EN.1 at [6192,2304,6264,2376].
  Note: VIA12 and VIA23 WERE co-located (stacked) at (6228,2340) BEFORE the
  repair; the repair deliberately SPLIT them in x (+36 vs 0) while both shared
  the +8 y-delta -- the PARTIAL case of Step 4(c). Co-location before a repair
  does not imply co-movement during it.

Worked example A6 (iteration 1, large multi-instance fix, row5, 7 ops):
  Locus [2536,6588,14328,7452]. Three vias moved in the same locus with DIFFERENT
  and even opposing x deltas: i0294 +136, i0433 -36, i0313 +36. Four M2 polygons
  resized (p1295 high+156, p1305 low+56, p1366 high+92, p1297 high+48).
  Gating: conn_preserved=true, n_new_out_of_crop=0.
  The -36 move on i0433 was paired with a resize_end on the LOW (left) x end of
  p1305 (+56), confirming that negative-direction moves pair with low-end M2
  extensions (trial:i01.ug.Block1_union_row5.05).

Worked example A7 (iteration 1, largest multi-instance fix, row6, 10 ops):
  Locus [8152,7668,13752,8532]. Five vias in one locus: i0097 +72, i0434 +72,
  i0455 -72, i0436 +72, i0116 +72. Five M2 polygons resized accordingly (p1323
  high+36, p1329 high+128, p1346 low+36, p1325 high+128, p1250 high+92).
  Gating: conn_preserved=true, n_new_in_crop=1 (accepted despite one new in-crop
  violation because n_new_out_of_crop=0, trial:i01.ug.Block1_union_row6.06).
  The -72 move on i0455 paired with resize_end low+36, again confirming opposing
  direction patterns.

Connectivity preservation (Family A): the via's own M1/M2 lands travel with the
instance, so the V1 cut never leaves its lands. Top-level M2 pads/routing are
co-moved or end-extended (only when necessary) so the via's M2 land stays merged
with its net; the VIA23 level likewise keeps M2 AND M3 coverage. Via cell
definitions are not touched; only instance placements and top-level M2/M3 polygons
change.

---

## Forbidden operation: resize_via_shape

Do not use resize_via_shape. The single trial that used it (trial:i01.ug.leaf_0034.12)
modified the M3 layer geometry of a VIA_VIA23_1_3_36_36 cell (y shrink -40 dbu)
and was gated_out with conn_preserved=false and 89 new in-crop violations.
Resizing internal via cell geometry breaks connectivity. All cell definitions are
fixed; only instance placements and top-level routing polygons are legal edit targets.

---

## Gating criterion

A repair is accepted (gated_in) when conn_preserved=true AND n_new_out_of_crop=0.
New violations that fall INSIDE the crop window (n_new_in_crop > 0) do not block
acceptance: trial:i01.ug.Block1_union_row1.00 introduced 4 in-crop violations and
was gated_in; trial:i01.ug.leaf_0031.11 introduced 4 in-crop violations and was
gated_in; trial:i01.ug.Block1_union_row6.06 introduced 1 in-crop violation and was
gated_in. Only out-of-crop new violations and connectivity breaks are disqualifying.

---

## Final-pair measured facts (reference-design tail evidence)

Provenance: these facts come from the final-pair comparison of the reference
design's initial layout against its repaired final layout, plus the BEFORE and
AFTER DRC reports. Every coordinate and delta cited in this document is quoted
inline from that pair; the layout files themselves are not needed and are not
shipped with this skill.

- Moving via instances without touching cell definitions is sufficient to clear
  V0.M1.AUX.3, V1.M1.EN.1, M1.S.2, and M1.S.6, provided metal polygons are
  co-moved or extended to maintain coverage.

- A single via move can simultaneously clear violations under 3 different rules
  (confirmed by the A3 example: one VIA12 move clears V0.M1.AUX.3, V1.M1.EN.1,
  and M1.S.2 at once).

- Iteration 1 confirms that x-only moves (dy=0) suffice to clear V1-layer
  violations in all 11 gated-in trials. Multi-instance loci (up to 5 via moves
  per locus) with per-instance deltas are the normal form for row-scale repairs
  (trial:i01.ug.Block1_union_row6.06 with 5 via moves,
  trial:i01.ug.Block1_union_row5.05 with 3 via moves,
  trial:i01.ug.Block1_union_row8.07 with 5 via moves).

- resize_end delta for M2 polygons need not match the via move delta: use the
  geometric gap between the M2 polygon edge and the via's new land boundary to
  compute the required extension (trial:i01.ug.Block1_union_row8.07 shows +136
  via moves paired with +192 M2 extensions).

---

## Case notes (reference-design tail evidence)

Stacked via movement is a PER-LEVEL decision, not a co-movement law. Verified
modes from the final diff: COUPLED (the (5652,5220) pair moved together, +64 x),
ANCHOR (VIA23 at (3204,1980) stayed while its VIA12 moved +136 x -- the VIA23
remains the M2-M3 anchor at the old position), PARTIAL (the (6228,2340) pair
shared +8 y but split in x, +36 vs 0). Anti-pattern AP-1: blindly moving every
co-located VIA23 with its VIA12 contradicts the clean final pair. Always run the
anchor check before co-moving.

Multi-rule single-fix frequency: in this block, 3 out of 12 VIA12 moves each cleared
violations from 2-3 distinct rules. When spatial clustering shows overlapping violation
bboxes from different rules at the same location, treat them as one compound fix.
A single rule can also double-report one physical site through deck rule variants:
the two M1.S.6 markers [6408,3457,6480,3499] and [6405,3464,6483,3492] outline the
same corner pair, so marker count can exceed physical site count.

Via move direction: both +x and -x are valid repair directions. When a via moves
in -x, the M2 polygon extension (if needed) targets the low (left) end, not the
high end (trial:i01.ug.Block1_union_row5.05). Within a single locus, different
vias can move in opposite x directions simultaneously without breaking connectivity
(trial:i01.ug.Block1_union_row6.06 with +72 and -72 moves in the same locus,
trial:i01.ug.Block1_union_row8.07 with +64, +136, -64, +136, +64).