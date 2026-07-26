Now I have both files. The new record is trial `i04.ug.whole_design.00`: a 20-op whole-design x-only repair touching V1 alongside M1, M2, M4, M5, M6, V4, V5. It is `gated_in`, `conn_preserved=true`, zero new violations. Key patterns: 9 instances plus 1 polygon all move +80 dbu x as a synchronized group; three other subgroups move at -96, +96, -48 dbu x; three polygons are resized +10 dbu x. Nothing in this record contradicts the seed knowledge. I'll fold in the new observations as a measured addendum.

(seed, reference-design-verified)
<!-- migrated from repair_skill_v0.md (md5 4c50681f3667b5cf80cd134b67b23d8e) by migrate_seed_v0.py; family slice(s): A -->

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

Connectivity preservation (Family A): the via's own M1/M2 lands travel with the
instance, so the V1 cut never leaves its lands. Top-level M2 pads/routing are
co-moved or end-extended so the via's M2 land stays merged with its net; the
VIA23 level likewise keeps M2 AND M3 coverage. Via cell definitions are not
touched; only instance placements and top-level M2/M3 polygons change.

---


## Whole-design compound repair (iteration 4 measured facts)

Trial i04.ug.whole_design.00 (Block6, unit_gate channel, locus [0,0,16944,16944],
decision gated_in, conn_preserved=true, n_new_in_crop=0, n_new_out_of_crop=0)
demonstrates a larger repair scope where V1 is one of eight touched layers
(M1, M2, M4, M5, M6, V1, V4, V5) within a single 20-op pass.

**All moves are pure x-axis.** Every instance move and polygon operation in
trial:i04.ug.whole_design.00 carries a zero y-component. The repair addresses
x-direction constraint violations exclusively; no y perturbation was needed or
applied.

**Synchronized group shift.** Nine instances (i0025, i0040, i0108, i0126, i0409,
i0412, i0530, i0031, i0538) plus one polygon (p1684) all move +80 dbu in x in
trial:i04.ug.whole_design.00. Moving a row or column of V1-touching instances by
a common delta is a valid repair mode; the group-shift does not require
individually distinct deltas per site.

**Mixed-sign moves within one pass.** The same trial applies -96, +96, and -48 dbu
x-moves to separate instance subgroups (i0112, i0152, i0074 at -96; i0319, i0213
at +96; i0015, i0471 at -48) in addition to the +80 group. A single repair pass
can simultaneously push some V1-touching instances in +x and others in -x without
violating connectivity, provided metal coverage is maintained at every moved via's
new position (trial:i04.ug.whole_design.00, conn_preserved=true).

**Small polygon resize as coverage trim.** Three polygons (p1990, p1923, p1920) are
each resized +10 dbu (2.5 nm) in x in trial:i04.ug.whole_design.00. This is a
coverage-trim variant of the extend operation documented in Family A Step 6: the
resize is small enough to re-establish edge coincidence between a moved instance
land and its host metal polygon without translating the polygon. Use a resize when
the metal polygon edge needs only a minor reach adjustment; use a larger extend or
full co-move when the via relocates far enough that the polygon edge must travel a
meaningful distance.

**V1 repairs co-occur with upper-metal-stack changes.** In trial:i04.ug.whole_design.00
the touched layer list includes M4, M5, M6, V4, and V5 alongside V1, M1, M2.
V1-level violations at the bottom of a stacked via column can couple upward: fixing
V1 enclosure or spacing may require repositioning vias and routing at M4-M6 levels
to preserve vertical connectivity through the stack. Confirm coverage at every metal
level above V1 that is part of the same net path, not just at the immediate M2 land.

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