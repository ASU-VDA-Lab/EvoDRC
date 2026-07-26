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
M1-VALID position -- observed moves include pure-x deltas of 36, 64, and 128 dbu
(trials i01.ug.leaf_0004.04, i01.ug.Block2_union_row5.02, i01.ug.leaf_0001.03)
and two-axis moves (e.g. delta (+72,-108) in seed examples) -- or extending the
M2-level routing can clear multiple rules of this family at once. Multi-rule
clearing (2-3 rules per move) is confirmed in seed examples A2, A3, A5; single-rule
clears are equally valid (seed A1, A4; trials .04 and .05 each have exactly one
instance op and remain DRC-clean).

Recipe -- Co-lateral via-and-pad slide:

Step 1. For each violation in this family, locate the VIA_VIA12 instance whose
  bounding box overlaps or abuts the violation bbox. When multiple instances fall
  within the same locus, move all of them -- trials i01.ug.Block2_union_row1.00
  (2 instances), i01.ug.Block2_union_row3.01 (2 instances), and
  i01.ug.Block2_union_row5.02 (3 instances) each moved all via instances sharing
  a locus by the same delta and all produced zero new violations.

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
  - Iteration 1 confirms 36 dbu (9 nm) as the most frequent x-delta (trials
    .00, .01, .04, .05, .06); 64 dbu appears for wider clearance needs (trial
    .02); 128 dbu for the largest displacement observed (trial .03).

Step 3. Apply the delta to VIA_VIA12. When multiple via instances share a locus,
  apply the SAME delta to all of them simultaneously (trials .00, .01, .02
  confirm this; all produced n_new_in_crop=0).

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
  and its deltas need not equal the via's delta. Polygon resize deltas can
  differ substantially from instance move deltas and can differ from each other:
  trial i01.ug.leaf_0001.03 moved instance i0086 by +128 dbu while p1065 was
  extended +184 (end high) and p957 extended +176 (end low) -- an asymmetric
  three-way delta that produced zero new violations. An end-low resize extends
  the left (or bottom) edge, confirmed by trial .03's p957 operation. Never
  break metal continuity in the process.

Step 6. VIA_VIA23 is the M2-M3 via: after any VIA23 move, BOTH levels need
  coverage. If it now falls outside the M2 routing polygon (layer M2), move or
  extend the M2 polygon to cover it; likewise verify the M3 side still covers
  the via at its new location (M3 coverage loss is a connectivity break the
  window DRC may not flag).
  Two modes are observed, on WHICHEVER affected level (top-level M2 or M3):
  (a) Co-move: the polygon translates by the same delta as the via (observed on
      both an M2 pad and an M3 routing polygon in worked example A1).
  (b) Extend: one edge is stretched to reach the new via position (observed on
      M2 in example A2 and on M3 in example A4, and confirmed by iteration 1
      resize_end operations in trials .01, .02, .03, .06).

Step 7. When the touched_layers set includes M4 (or any metal layer above M2),
  verify that the M4-level polygon(s) affected by the via shift maintain
  continuity and clearance at the new position. Trial i01.ug.leaf_0001.03 is
  the first measured case involving M4; it required two polygon resizes (end
  high and end low on different polygons) with deltas differing from the
  instance move, and produced zero new violations. Do not assume metal polygons
  above M2 are unaffected when a via chain is long.

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


---


## Iteration 1 measured facts (Block2, unit_gate channel)

Provenance: 7 gated-in repairs across 7 units in Block2, iteration 1, all
conn_preserved=true, n_new_in_crop=0, n_new_out_of_crop=0. All citations below
are from this iteration's records.

**Op counts per fix.** Iteration 1 repairs range from 1 to 5 ops:
- 1 op (single move_instance): trials i01.ug.leaf_0004.04 and i01.ug.leaf_0007.05 each
  moved exactly one instance (+36 dbu in x) and cleared all violations in the locus.
- 2 ops: trials i01.ug.Block2_union_row1.00 (2 move_instance) and i01.ug.leaf_0011.06
  (1 move_instance + 1 resize_end) each used 2 ops.
- 3 ops: trials i01.ug.Block2_union_row3.01 (2 move_instance + 1 resize_end) and
  i01.ug.leaf_0001.03 (1 move_instance + 2 resize_end) each used 3 ops.
- 5 ops: trial i01.ug.Block2_union_row5.02 (3 move_instance + 2 resize_end).

**Instance move deltas (iteration 1).** All moves are pure x-axis (y delta = 0 for
every instance in every trial). The 36 dbu (+x) delta is the most common: trials
.00, .01, .02 (all three instances), .04, .05, .06 all use 36 dbu. Larger deltas --
64 dbu (trial .02 additional instances share same 64 dbu value; wait: .02 uses 64 dbu
for all three instances), and 128 dbu (trial .03) -- appear when clearance needs are
wider. Confirmed: 36 dbu is the modal repair step in iteration 1 (trials
i01.ug.Block2_union_row1.00, i01.ug.Block2_union_row3.01, i01.ug.leaf_0004.04,
i01.ug.leaf_0007.05, i01.ug.leaf_0011.06).

**Multiple instances moved together at a common delta.** When a locus contains
multiple VIA_VIA12 instances, all are moved by the same delta in a single repair:
trial i01.ug.Block2_union_row1.00 moves i0159 and i0152 both +36 dbu x;
trial i01.ug.Block2_union_row3.01 moves i0115 and i0103 both +36 dbu x;
trial i01.ug.Block2_union_row5.02 moves i0083, i0018, and i0034 all +64 dbu x.
All produced n_new_in_crop=0.

**Polygon resize directions.** All resize_end operations in iteration 1 are on the
x-axis. end="high" extends the right edge (confirmed: trials .01, .02, .03 p1065,
.06). end="low" extends the left edge (confirmed: trial .03 p957). Both directions
can appear in the same repair (trial .03 uses end="high" on p1065 and end="low" on
p957 simultaneously).

**Asymmetric polygon resize deltas.** Polygon resize deltas do not need to equal
the instance move delta. In trial i01.ug.leaf_0001.03: instance i0086 moves +128 dbu;
polygon p1065 resizes +184 dbu (end high); polygon p957 resizes +176 dbu (end low).
All three deltas are distinct. The repair produced n_new_in_crop=0, confirming that
asymmetric polygon adjustments are correct when coverage geometry requires them.

**M4 involvement.** Trial i01.ug.leaf_0001.03 is the first measured case listing M4
in touched_layers (touched_layers: ["M1","M2","M4","V1"]). Repairs in this unit
required adjusting polygons on M4 in addition to M1/M2, with the two resize_end
operations (+184 and +176) covering the longer routing reach to M4. All other
iteration 1 trials touched only M1, M2, V1.

**All iteration 1 repairs used x-only moves.** No y-axis instance displacement
appears in any of the 7 trials. This contrasts with seed examples A4 (pure y) and A5
(x and y). Both axes remain valid based on the seed evidence; x-only is dominant in
this block's iteration 1 geometry.