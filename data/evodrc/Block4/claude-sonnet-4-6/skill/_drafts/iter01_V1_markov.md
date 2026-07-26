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
M1-VALID position -- observed moves include pure-x (all iteration 1 trials) and
two-axis (e.g. the VIA12 at (5220,3060) relocated to (5292,2952), delta (+72,-108)
from the reference design) -- or extending the M2-level routing can clear multiple
rules of this family at once.

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
  - Minimum observed move delta: 36 dbu (9 nm) in x, confirmed by trial:i01.ug.leaf_0008.08,
    trial:i01.ug.leaf_0020.09, and trial:i01.ug.leaf_0021.10, each with a single
    move_instance (+36,0) that cleared all violations in the crop with zero new
    violations.
  - Negative-x moves are also valid: trial:i01.ug.Block4_union_row10.01 includes
    a move_instance (-108,0) for i0041 and trial:i01.ug.Block4_union_row5.04
    includes move_instance (-36,0) for i0341, both connectivity-preserved with
    zero new violations.
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
  in this repair ZERO top-level M1 (layer 19) polygons were touched. Three
  observed coverage ops on M2:
  (a) RESIZE_END high: extend the high-x edge of an existing M2 polygon to
      reach the via's new position. Observed deltas 56-172 dbu beyond the via
      move delta, e.g. trial:i01.ug.Block4_union_row2.02 via +36, polygon
      high-x +56 and +92; trial:i01.ug.Block4_union_row7.06 via +108, polygon
      high-x +164; trial:i01.ug.Block4_union_row7.06 also +56 and +92 for
      additional vias. The resize delta does not need to equal the via delta.
  (b) RESIZE_END low: retract the low-x edge of an existing M2 polygon in the
      +x direction to reposition coverage after a negative-x via move. Observed
      in trial:i01.ug.Block4_union_row10.01: p1589 low-x end +72 after i0041
      moved -108.
  (c) ADD_POLYGON: insert a new M2 polygon as a landing pad at the via's new
      position. Observed in trial:i01.ug.Block4_union_row1.00: after i0265
      moved +112, a new M2 polygon [[9252,3024],[9444,3024],[9444,3096],[9252,3096]]
      (192x72 dbu) was added; after i0325 moved +36, a new M2 polygon
      [[12132,3024],[12224,3024],[12224,3096],[12132,3096]] (92x72 dbu) was
      added. An isolated via that has no pre-existing polygon in range uses
      add_polygon rather than resize_end.
  An ISOLATED landing pad can simply move by the same delta; a pad attached to
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

---

## Iteration 1 measured patterns (Block4 unit_gate channel)

### Opposite-direction via spread

Two vias in the same locus can be moved in opposite x-directions to open up
spacing. Observed in trial:i01.ug.Block4_union_row3.03: i0170 moved (-36,0) and
i0292 moved (+36,0) within locus [6844,4428,8352,5292], zero new violations, all
touched layers M1/M2/V1, no M2 polygon edits required. This is a distinct repair
mode where the violation is resolved by SPREADING adjacent vias rather than
sliding all in one direction.

### Multi-via cluster fixes with resize_end

When a locus contains multiple vias all requiring x-axis shifts, the standard
pattern is: move each via independently, then extend (resize_end high) the
downstream M2 polygon for each moved via. Observed in trial:i01.ug.Block4_union_row2.02:
two vias each moved +36 dbu, with resize_end high on two M2 polygons by +56 and
+92 dbu respectively. Observed in trial:i01.ug.Block4_union_row5.04: three vias
moved +64 each and one via moved -36, with resize_end high on two M2 polygons
(both +120 dbu). The resize delta consistently exceeds the move delta, providing
margin beyond the minimum coverage requirement.

### M4 touched in multi-level context

Some repairs in this channel report M4 in touched_layers (trial:i01.ug.Block4_union_row10.01,
trial:i01.ug.Block4_union_row7.06). The explicit ops in those trials only show
move_instance and resize_end on M2; M4 is not an op target. M4 appears in
touched_layers as an indication that the net being repaired has M4 connectivity,
not that M4 geometry was directly edited. Do not add M4 ops unless a V3/M4-level
enclosure or spacing rule fires.

### Minimal single-via fixes

The smallest valid repair is a single move_instance with delta (+36,0) dbu and
no polygon edits, confirmed connectivity-preserved in three independent leaf units:
trial:i01.ug.leaf_0008.08 (i0274 +36), trial:i01.ug.leaf_0020.09 (i0101 +36),
trial:i01.ug.leaf_0021.10 (i0038 +36). These sites have sufficient pre-existing
M2 polygon coverage at the destination; no resize_end or add_polygon is needed.
Before adding a polygon edit, verify whether the destination already has M2
coverage from an adjacent polygon that the moved via's land will merge into.

### add_polygon versus resize_end decision

Use add_polygon on M2 when no existing polygon reaches within landing distance
of the via's new position. Use resize_end when an existing polygon's edge can
be extended to cover it. Both ops achieve identical connectivity outcomes
(trial:i01.ug.Block4_union_row1.00 uses add_polygon; trial:i01.ug.Block4_union_row2.02,
trial:i01.ug.Block4_union_row5.04, trial:i01.ug.Block4_union_row7.06 all use
resize_end). The choice is determined by the layout topology at the destination,
not by rule type or via delta magnitude.

### x-axis-only moves in iteration 1

All 10 gated-in fixes in iteration 1 use pure x-axis via moves (y delta = 0 for
every move_instance op). This is consistent with M2 running horizontally and
V1.M1.EN.1 / V0.M1.AUX.3 being satisfiable by x-repositioning alone when the
via's y-position already sits on a valid M1 track center.

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