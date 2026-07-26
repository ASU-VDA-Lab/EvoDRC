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
M1-VALID position -- observed moves include pure-x (the dominant direction across
all iteration 1 trials: i01.ug.Block3_union_row1.00, .row2.01, .row5.02,
.row8.03, .leaf_0006.04, .leaf_0007.05, .leaf_0008.06, .leaf_0009.07, .leaf_0012.08),
negative-x (i01.ug.leaf_0013.09: delta -36 dbu), and two-axis (e.g. the VIA12 at
(5220,3060) relocated to (5292,2952), delta (+72,-108)) -- or extending the
M2-level routing (see below) can clear multiple rules of this family at once (the
multi-rule examples below -- A2, A3, A5 -- clear 2-3 rules per move; A1 and A4
each clear ONE rule, which is equally normal; do not assume all four always clear
together).

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
  - The delta need not be positive. Negative-x moves are valid and observed
    (i01.ug.leaf_0013.09: single move_instance delta [-36,0], conn_preserved,
    zero new violations).
  - Within a single repair block, different vias receive different deltas:
    in i01.ug.Block3_union_row8.03, inst i0017 moved +108 dbu while i0016,
    i0019, and i0021 each moved +72 dbu. Choose the delta per instance
    based on its own local geometry, not a block-wide constant.
Step 3. Apply the delta to VIA_VIA12.
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
  in this repair ZERO top-level M1 (layer 19) polygons were touched. An
  ISOLATED landing pad can simply move by the same delta; a pad attached to
  (or part of) a routing stub is typically reshaped or end-extended instead,
  and its deltas need not equal the via's (observed: the via at (6228,2340)
  moved (+36,+8) while its M2 pad moved (+92,+8)). The M2 resize_end delta
  is NOT a fixed multiple of the via delta -- it is site-specific and depends
  on how far the polygon's current high end is from the via's new land
  position. Measured differences (resize_end delta minus via move delta):
  +56 dbu (i01.ug.Block3_union_row1.00, i01.ug.Block3_union_row8.03 p1266/p1267),
  +36 dbu (i01.ug.leaf_0012.08), +20 dbu (i01.ug.Block3_union_row8.03 p1257,
  i01.ug.leaf_0007.05), 0 dbu (i01.ug.Block3_union_row5.02), and even -44 dbu
  (i01.ug.leaf_0008.06: via moved +136, M2 p1261 extended only +92) -- the M2
  polygon already reached partway past the old via position in that case.
  Determine the resize_end delta by computing the gap between the polygon's
  current high edge and the via's new land edge; do not copy the via delta. Never
  break metal continuity in the process.
  A single move_instance with NO polygon edit is sufficient when the via's new
  landing position already lies under an existing M2 polygon (observed:
  i01.ug.Block3_union_row2.01 with 2 moves and 0 resizes;
  i01.ug.leaf_0006.04 with 2 moves and 0 resizes;
  i01.ug.leaf_0009.07 with 1 move and 0 resizes;
  i01.ug.leaf_0013.09 with 1 move and 0 resizes -- all conn_preserved, zero
  new violations).
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
  M3 y-direction extension is also required when a y-axis polygon resize (not
  a via move) adjusts M3 geometry: in i01.ug.leaf_0008.06, polygon p1159
  received a resize_end y high +20 dbu alongside via moves in x, and M3 was
  among the touched layers.

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

Connectivity preservation (Family A): the via's own M1/M2 lands travel with the
instance, so the V1 cut never leaves its lands. Top-level M2 pads/routing are
co-moved or end-extended so the via's M2 land stays merged with its net; the
VIA23 level likewise keeps M2 AND M3 coverage. Via cell definitions are not
touched; only instance placements and top-level M2/M3 polygons change.

---


## Iteration 1 measured records (Block3, unit_gate channel)

All 10 trials in iteration 1 (trial_ids i01.ug.Block3_union_row1.00 through
i01.ug.leaf_0013.09) were gated_in with conn_preserved=true and zero new
violations (n_new_in_crop=0, n_new_out_of_crop=0). All moves are x-axis only
(delta_dbu[1]=0 in every move_instance op), except i01.ug.leaf_0008.06 which
also includes a y-direction polygon resize (p1159 resize_end y high +20 dbu).
Touched layers across all trials: M1, M2, V1 (all trials), plus M3 (leaf_0008
only).

Key op patterns observed:

**Multi-via, uniform delta + M2 extend** (i01.ug.Block3_union_row1.00): 3
  VIA12 instances each moved +136 dbu in x; 3 M2 polygons each had resize_end
  x high +192 dbu. The M2 extension (+192) exceeded the via move (+136) by 56
  dbu at every site in this trial.

**Multi-via, uniform delta, no polygon edit** (i01.ug.Block3_union_row2.01,
  i01.ug.leaf_0006.04): pure move_instance only (2 moves each, +36 dbu x).
  No M2 edits needed because the vias' new positions were already covered by
  existing M2 polygons.

**Mixed: some vias get M2 extend, one does not** (i01.ug.Block3_union_row5.02):
  3 instances moved +36 dbu x; only 1 of the 3 had an associated resize_end
  (p1265, x high +36 dbu). The other two vias landed under existing M2 coverage.

**Multi-via, mixed deltas within one block** (i01.ug.Block3_union_row8.03):
  i0017 moved +108 dbu x (M2 p1267 extended +164, delta excess +56);
  i0016 moved +72 dbu x (M2 p1266 extended +128, delta excess +56);
  i0019 moved +72 dbu x (M2 p1269 extended +128, delta excess +56);
  i0021 moved +72 dbu x (M2 p1257 extended +92, delta excess +20).
  Within a single locus, different instances require different deltas; compute
  each independently.

**Single via, no polygon edit** (i01.ug.leaf_0009.07, i01.ug.leaf_0013.09):
  1 move_instance each. leaf_0009: +36 dbu x. leaf_0013: -36 dbu x (negative
  direction confirmed valid). Both conn_preserved with zero new violations.

**Mixed via deltas + y-direction polygon resize + M3 involvement**
  (i01.ug.leaf_0008.06): polygon p1159 resized (y, high, +20 dbu); i0239 moved
  (+4,0) dbu (sub-grid correction); i0047 moved (+136,0) dbu; M2 polygon p1261
  extended x high +92 dbu (less than the +136 via move: the polygon already
  extended past the old via position). M3 touched as a layer. This trial
  confirms that y-direction polygon resizes can coexist with x-direction via
  moves in the same repair, and that M2 resize_end delta can be smaller than
  the via move delta.

**Via + M2 extend, extend delta exceeds via delta by moderate margin**
  (i01.ug.leaf_0007.05, i01.ug.leaf_0012.08):
  leaf_0007: 2 vias +36 dbu x, 2 M2 extends +56 dbu (excess +20 each).
  leaf_0012: 1 via +72 dbu x, 1 M2 extend +108 dbu (excess +36).

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


## Case notes (reference-design tail evidence)

Multi-rule single-fix frequency: in this block, 3 out of 12 VIA12 moves each cleared
violations from 2-3 distinct rules. When spatial clustering shows overlapping violation
bboxes from different rules at the same location, treat them as one compound fix.
A single rule can also double-report one physical site through deck rule variants:
the two M1.S.6 markers [6408,3457,6480,3499] and [6405,3464,6483,3492] outline the
same corner pair, so marker count can exceed physical site count.

## Case notes (iteration 1 measured)

Move granularity: all iteration 1 via moves are multiples of 4 dbu (1 nm), with
the smallest observed delta being 4 dbu (i01.ug.leaf_0008.06 inst i0239) and the
most common being 36 dbu (9 nm) and 72/108/136 dbu (multiples thereof). The 4 dbu
micro-correction coexists with a 136 dbu move in the same trial, confirming that
different instances in a locus can have very different required deltas.

Direction: all 10 iteration 1 trials used x-axis via moves. Y-axis adjustment
appeared only as a polygon resize (p1159 y high +20 dbu in leaf_0008), not as a
via y-move. The reference-design seed examples include y-only via moves (A4:
(0,+68)) and two-axis moves (A5, A1 analogs), so y-direction via moves remain
valid -- iteration 1 simply did not require them in this Block3 locus set.

Negative-direction moves: confirmed valid in x (i01.ug.leaf_0013.09: -36 dbu).
No negative y-direction via moves observed yet; not ruled out.