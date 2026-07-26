## Per-rule recipes

### Family A: M1-via cluster (V0.M1.AUX.3, M1.S.2, M1.S.6, V1.M1.EN.1)

These four rules often cluster around a VIA_VIA12 instance placed where local M1
geometry fails width-matching, spacing, or enclosure constraints -- a single site
usually fires one to three of them, not necessarily all four. In the 37-violation
example block, 18 of 37 violations belong to this family.

Rule semantics (ASAP7 rule deck):
- V0.M1.AUX.3: The V0 y-extent must equal the M1 y-extent at the landing location
  (seed, reference-design-verified). M1 runs horizontally; perpendicular direction
  is y.
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
M1-VALID position -- observed moves include pure-x, pure-y (e.g. (0,+68)) and
two-axis (e.g. the VIA12 at (5220,3060) relocated to (5292,2952), delta
(+72,-108)) -- or extending the M2-level routing (see below)
can clear multiple rules of this family at once (the multi-rule examples below
-- A2, A3, A5 -- clear 2-3 rules per move; A1 and A4 each clear ONE rule, which
is equally normal; do not assume all four always clear together).

Recipe -- Co-lateral via-and-pad slide:

Step 1. For each violation in this family, locate the VIA_VIA12 instance whose
  bounding box overlaps or abuts the violation bbox.
Step 2. Determine the required lateral delta:
  - The new position must satisfy the V0.M1.AUX.3 width-match condition
    (seed, reference-design-verified). For V1.M1.EN.1 the deck requires, on ONE
    pair of opposite sides (x-pair or y-pair): BOTH sides >= 8 dbu (2 nm) AND
    at least one of them >= 20 dbu (5 nm). The VIA_VIA12 cell's own M1 land
    supplies exactly 8 dbu on both y-sides (land y = +/-44 vs cut +/-36) but 0
    on x, so the merged M1 must either lift ONE y-side to >= 20 dbu, or give the
    x-pair (>= 8 dbu one side, >= 20 dbu the other). The repairs in this case
    aimed for >= 20 dbu on BOTH x-sides -- a conservative working target,
    sufficient but stricter than the rule minimum. M1.S.2 and M1.S.6 are
    incidentally cleared when the via moves away from the neighbor that was
    causing the tip/corner proximity.
  - Deltas may be positive or negative in x. Negative-x moves are confirmed at
    -28, -36, and -108 dbu (trials: i01.ug.Block4_union_row7.06,
    i01.ug.Block4_union_row3.03, i01.ug.Block4_union_row10.01). The minimum
    confirmed delta magnitude is 28 dbu (7 nm); the most common small step is
    36 dbu (9 nm) (trials: i01.ug.Block4_union_row2.02,
    i01.ug.Block4_union_row6.05, i01.ug.leaf_0008.08, i01.ug.leaf_0020.09,
    i01.ug.leaf_0021.10).
Step 3. Apply the delta to VIA_VIA12.
Step 4. If a VIA_VIA23 is co-located at the same (x, y) (stacked via), decide
  PER LEVEL -- co-located vias do NOT always travel together:
  (a) COUPLED case: if the M2 landing must move with the V1 fix (the M2 polygon
      itself is co-moved), move VIA23 by the same delta (verified: the stacked
      pair at (5652,5220) both moved +64 in x, together with the associated
      TOP-LEVEL M2 pad and M3 routing polygons; the vias' own M1/M2 lands
      travel inside the instances -- no top-level M1 was involved).
  (b) ANCHOR case: if VIA23's own levels (M2-M3) remain correctly aligned at
      the ORIGINAL coordinate, leave VIA23 in place and move only VIA12
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
  in the seed repairs ZERO top-level M1 (layer 19) polygons were touched. Three
  coverage ops are confirmed:
  (a) resize_end: extend the high or low end of an existing polygon's axis by a
      dbu delta. For a positive-x move, extend the polygon's high-x end
      (trial: i01.ug.Block4_union_row2.02, p1548 high+56; p1569 high+92). For a
      negative-x move, extend the low-x end (trial: i01.ug.Block4_union_row10.01,
      p1589 low+72). The resize delta need not equal the instance delta
      (e.g., i0153 +108 dbu but p1595 high+164 dbu in trial
      i01.ug.Block4_union_row7.06; i0041 -108 dbu but p1589 low+72 dbu in trial
      i01.ug.Block4_union_row10.01).
  (b) add_polygon: add a new M2 polygon at the via's new landing position when no
      existing polygon can be extended to reach it (trial:
      i01.ug.Block4_union_row1.00, two new M2 polygons added at y=3024..3096
      after i0265 moved +112 and i0325 moved +36).
  (c) co-move: translate the polygon by the same delta as the via (seed,
      reference-design-verified).
  An ISOLATED landing pad can simply move by the same delta; a pad attached to
  (or part of) a routing stub is typically reshaped or end-extended instead.
  Never break metal continuity in the process.
  Some via moves require no metal op at all when the via's new landing already
  lies within existing M2 coverage (confirmed at 36 dbu single-instance moves:
  trials i01.ug.leaf_0008.08, i01.ug.leaf_0020.09, i01.ug.leaf_0021.10,
  i01.ug.Block4_union_row6.05, i01.ug.Block4_union_row3.03).
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
Step 7. When the repair touches_layers includes M4, verify that M4-level routing
  polygons at the affected site also maintain coverage. resize_end on M4 polygons
  is confirmed at high-end extensions of 64 and 172 dbu (trials:
  i01.ug.Block4_union_row10.01, p1379 x low+64; i01.ug.Block4_union_row7.06,
  p1395 x high+172). Apply the same extend-vs-co-move decision as for M2/M3.

Enclosure check (MERGED metal): enclosure is assessed on merged M1 at the final
state (seed, reference-design-verified). Enclosure from any single polygon in
isolation does not determine rule outcome; the merged result is authoritative.

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
  present at the new position. The final state is host-verified DRC-clean.

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
touched; only instance placements and top-level M2/M3 polygons change. All 10
iteration-1 trials confirm conn_preserved=true with n_new_in_crop=0 and
n_new_out_of_crop=0 (trials: i01.ug.Block4_union_row1.00,
i01.ug.Block4_union_row10.01, i01.ug.Block4_union_row2.02,
i01.ug.Block4_union_row3.03, i01.ug.Block4_union_row5.04,
i01.ug.Block4_union_row6.05, i01.ug.Block4_union_row7.06,
i01.ug.leaf_0008.08, i01.ug.leaf_0020.09, i01.ug.leaf_0021.10).

---

## Final-pair measured facts (reference-design tail evidence)

Provenance: these facts come from the final-pair comparison of the reference
design's initial layout against its repaired final layout, plus the BEFORE and
AFTER DRC reports. Every coordinate and delta cited in this document is quoted
inline from that pair; the layout files themselves are not needed and are not
shipped with this skill.

- Moving via instances without touching cell definitions is sufficient to clear
  V0.M1.AUX.3, V1.M1.EN.1, M1.S.2, and M1.S.6, provided metal polygons are
  co-moved or extended to maintain coverage (seed, reference-design-verified).

- A single via move can simultaneously clear violations under 3 different rules
  (confirmed by the A3 example: one VIA12 move clears V0.M1.AUX.3, V1.M1.EN.1,
  and M1.S.2 at once).

---

## Iteration-1 measured additions (Block4, unit_gate channel)

All 10 iteration-1 trials were accepted (decision=gated_in) with zero new
violations inside or outside the crop window, confirming the approach generalizes
across Block4 rows and leaf units.

**add_polygon is a valid M2 coverage operation.** When no existing M2 polygon
extends to the via's new landing position, a new M2 polygon is added at that
location (trial: i01.ug.Block4_union_row1.00, two new M2 polygons added with
dimensions 192x72 dbu and 92x72 dbu at y=3024..3096 to cover vias moved +112
and +36 dbu in x respectively). Add_polygon and resize_end are interchangeable
for coverage; the choice depends on whether a nearby polygon's edge can reach
the new landing point.

**Negative-delta moves clear DRC as reliably as positive-delta moves.** Confirmed
negative-x instance moves: -28 dbu (trial: i01.ug.Block4_union_row7.06, i0158),
-36 dbu (trials: i01.ug.Block4_union_row3.03 i0170; i01.ug.Block4_union_row5.04
i0341), -108 dbu (trial: i01.ug.Block4_union_row10.01 i0041). For a negative-x
move, extend the low-x end of the associated M2 polygon; for a positive-x move,
extend the high-x end (trial: i01.ug.Block4_union_row10.01, i0041 -108 dbu ->
p1589 low+72 dbu; i01.ug.Block4_union_row2.02, i0250 +36 dbu -> p1548 high+56
dbu).

**resize_end delta need not equal instance delta.** The polygon edge extension
can be larger or smaller than the via move. Observed ratios in iteration 1:
instance +108, extension +164 (trial: i01.ug.Block4_union_row7.06, i0153/p1595);
instance -108, extension low+72 (trial: i01.ug.Block4_union_row10.01, i0041/p1589);
instance +36, extension +56 or +92 (trials: i01.ug.Block4_union_row2.02).

**M4 polygons require the same coverage maintenance as M2/M3.** When
touched_layers includes M4, resize_end on M4-level polygons is needed to maintain
routing coverage. Confirmed M4 resize_end ops: p1379 x low+64 (trial:
i01.ug.Block4_union_row10.01); p1395 x high+172 (trial:
i01.ug.Block4_union_row7.06). Apply the same end-direction rule as for M2 (high
for positive delta, low for negative delta).

**Many repairs require no metal ops.** Five of ten iteration-1 trials used only
instance moves with zero polygon edits (trials: i01.ug.leaf_0008.08,
i01.ug.leaf_0020.09, i01.ug.leaf_0021.10, i01.ug.Block4_union_row6.05,
i01.ug.Block4_union_row3.03). In these cases the via's new landing position
already falls within existing M2 coverage, so no resize_end or add_polygon is
needed.

**Multiple instances move in the same repair crop.** Up to 4 instance moves per
crop are confirmed (trial: i01.ug.Block4_union_row7.06, 4 moves). Each instance
move is assessed independently for required metal coverage ops; not every move
requires one.

## Case notes (reference-design tail evidence)

Multi-rule single-fix frequency: in the seed block, 3 out of 12 VIA12 moves each
cleared violations from 2-3 distinct rules. When spatial clustering shows
overlapping violation bboxes from different rules at the same location, treat them
as one compound fix.
A single rule can also double-report one physical site through deck rule variants:
the two M1.S.6 markers [6408,3457,6480,3499] and [6405,3464,6483,3492] outline
the same corner pair, so marker count can exceed physical site count.