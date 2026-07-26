Working from the prompt-provided records only. Synthesizing the update now.

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
M1-VALID position -- observed moves include pure-x (trial:i01.ug.leaf_0008.08,
trial:i01.ug.leaf_0020.09, trial:i01.ug.leaf_0021.10, and the reference-design
examples), negative-x (trial:i01.ug.Block4_union_row3.03 i0170 -36 dbu,
trial:i01.ug.Block4_union_row5.04 i0341 -36 dbu, trial:i01.ug.Block4_union_row10.01
i0041 -108 dbu), and two-axis (e.g. VIA12 at (5220,3060) -> (5292,2952) from the
reference design) -- or extending the routing polygons above it can clear multiple
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
  - The minimum observed non-zero delta magnitude is 28 dbu (trial:i01.ug.Block4_union_row7.06
    i0158 -28x); the most frequent single quantum is 36 dbu (9 nm), appearing
    in 9 of 10 iteration-1 trials as the delta for at least one instance move.
    Larger deltas (64, 108, 112, 136 dbu) appear when a single via must move
    clear of a wider conflict zone.
  - Moves are exclusively in the x-axis in iteration 1 (all 10 trials have
    delta_dbu[1]=0); y-axis moves appear in the reference-design tail (example A4
    delta (0,+68)).
Step 3. Apply the delta to VIA_VIA12. When a locus contains multiple conflicting
  vias, they may move in OPPOSITE x-directions to spread apart
  (trial:i01.ug.Block4_union_row3.03: i0170 -36x, i0292 +36x), or independently
  by different magnitudes (trial:i01.ug.Block4_union_row7.06: four moves at
  +108, -28, +36, +36 dbu in x).
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
  in the reference-design repair ZERO top-level M1 (layer 19) polygons were
  touched. Three coverage operations are observed:
  (a) resize_end high: the high end of an existing polygon is stretched to reach
      the via's new position (trial:i01.ug.Block4_union_row2.02: p1548 x-high
      +56, p1569 x-high +92 after via moves of +36x each; trial:i01.ug.Block4_union_row5.04:
      p1608 and p1593 x-high +120 after via moves of +64x).
  (b) resize_end low: the low end of an existing polygon is stretched toward the
      via's new position (trial:i01.ug.Block4_union_row10.01: p1589 x-low +72,
      p1379 x-low +64).
  (c) add_polygon: a new M2 polygon is inserted to cover the via's M2 land at its
      new position (trial:i01.ug.Block4_union_row1.00: two new M2 polygons added,
      192x72 dbu at (9252,3024)-(9444,3096) and 92x72 dbu at (12132,3024)-(12224,3096),
      one per moved via). Use add_polygon when no existing polygon can reach the
      new position without creating a conflict or when the via has moved into a
      gap with no adjacent routing stub to extend.
  The polygon extension delta need not equal the via's move delta: via +36x but
  polygon extends +56 or +92 (trial:i01.ug.Block4_union_row2.02); via +64x but
  polygon extends +120 (trial:i01.ug.Block4_union_row5.04). The extension must
  reach the via's M2 land bounding box, which sets the lower bound; additional
  margin is acceptable. When no polygon edit is needed (isolated via with adequate
  surrounding M2), a single move_instance op suffices with no polygon ops
  (trial:i01.ug.leaf_0008.08, trial:i01.ug.leaf_0020.09, trial:i01.ug.leaf_0021.10,
  all single-op +36x moves, conn_preserved=true, n_new_in_crop=0).
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
Step 7. When the repair chain extends above M2 (e.g. the via stack is part of a
  taller routing column), M4 polygons may also require end-extension.
  trial:i01.ug.Block4_union_row7.06 extends p1395 x-high +172 on M4; trial:i01.ug.Block4_union_row10.01
  extends p1379 x-low +64 on M4. Check touched_layers in the repair record: when
  M4 appears, at least one M4 polygon end was stretched. The same resize_end
  (high or low) logic applies at M4 as at M2/M3.

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
co-moved or end-extended (or a new M2 polygon is added, per Step 5(c)) so the
via's M2 land stays merged with its net; the VIA23 level likewise keeps M2 AND
M3 coverage. When the stack reaches M4, M4 polygon ends are also extended
(trial:i01.ug.Block4_union_row7.06, trial:i01.ug.Block4_union_row10.01). Via
cell definitions are not touched; only instance placements and top-level routing
polygons change.

---


## Final-pair measured facts (reference-design tail evidence)

Provenance: these facts come from the final-pair comparison of the reference
design's initial layout against its repaired final layout, plus the BEFORE and
AFTER DRC reports. Every coordinate and delta cited in this document is quoted
inline from that pair; the layout files themselves are not needed and are not
shipped with this skill.

- Moving via instances without touching cell definitions is sufficient to clear
  V0.M1.AUX.3, V1.M1.EN.1, M1.S.2, and M1.S.6, provided metal polygons are
  co-moved or extended (or added) to maintain coverage.

- A single via move can simultaneously clear violations under 3 different rules
  (confirmed by the A3 example: one VIA12 move clears V0.M1.AUX.3, V1.M1.EN.1,
  and M1.S.2 at once).


## Iteration 1 measured facts (Block4, unit_gate channel)

Provenance: all 10 trials below are `gated_in` with `conn_preserved=true` and
`n_new_in_crop=0`/`n_new_out_of_crop=0` from the Block4 design state
d279330089d1cc7ae7faf9a64991c183a651656d2a44f921bf86d5225ab3dacd, iteration 1.

- The minimum observed non-zero move magnitude is 28 dbu (trial:i01.ug.Block4_union_row7.06
  i0158 -28x). The most frequent quantum is 36 dbu (9 nm): it appears as at least
  one instance's delta in 9 of 10 trials (all except trial:i01.ug.Block4_union_row5.04
  where the minimum delta is 64 dbu).

- Single-op repairs (one move_instance, no polygon edits) are sufficient for
  isolated violations: trial:i01.ug.leaf_0008.08 (i0274 +36x), trial:i01.ug.leaf_0020.09
  (i0101 +36x), and trial:i01.ug.leaf_0021.10 (i0038 +36x) each clear their
  locus with a single +36 dbu x-move touching M1, M2, V1 but requiring no
  polygon op.

- Negative x-deltas are valid repair directions. trial:i01.ug.Block4_union_row3.03
  moves i0170 -36x; trial:i01.ug.Block4_union_row5.04 moves i0341 -36x;
  trial:i01.ug.Block4_union_row10.01 moves i0041 -108x; trial:i01.ug.Block4_union_row7.06
  moves i0158 -28x.

- Two vias within the same locus can move in opposite x-directions to spread apart.
  trial:i01.ug.Block4_union_row3.03: i0170 -36x and i0292 +36x, 2 ops total, no
  polygon edits, conn_preserved=true.

- `add_polygon` on M2 is a valid alternative to `resize_end` when no existing
  routing stub can be extended to the via's new position. trial:i01.ug.Block4_union_row1.00:
  after moves of i0265 +112x and i0325 +36x, two new M2 polygons are inserted
  (192x72 dbu at (9252,3024)-(9444,3096) and 92x72 dbu at (12132,3024)-(12224,3096)).
  The new polygon height of 72 dbu matches the via's M2 land height.

- Polygon resize_end delta is independent of the via move delta; the extension
  must reach the via's M2 land at its new position. trial:i01.ug.Block4_union_row2.02:
  both vias move +36x, but p1548 extends x-high +56 and p1569 extends x-high +92.
  trial:i01.ug.Block4_union_row5.04: vias move +64x, but p1608 and p1593 each
  extend x-high +120.

- resize_end on the low end of a polygon is observed. trial:i01.ug.Block4_union_row10.01:
  p1589 x-low +72 and p1379 x-low +64.

- When `touched_layers` includes M4, at least one M4 polygon end requires
  extension. trial:i01.ug.Block4_union_row7.06 (8 ops, M1/M2/M4/V1): p1395
  x-high +172 on M4 alongside three M2 resize_end ops. trial:i01.ug.Block4_union_row10.01
  (7 ops, M1/M2/M4/V1): p1379 x-low +64 on M4. In both cases the M4 extension
  is a single resize_end op.

- Multi-via loci (3-4 vias per crop) are common for row-level violations.
  trial:i01.ug.Block4_union_row5.04 moves 4 vias (+64, +64, +64, -36 dbu in x)
  with 2 resize_end polygon ops. trial:i01.ug.Block4_union_row6.05 moves 3 vias
  all at +36x with no polygon ops. trial:i01.ug.Block4_union_row7.06 moves 4 vias
  with 4 resize_end ops.

- All iteration-1 instance moves are x-axis only (delta_dbu[1]=0 in every trial).
  y-axis-only and two-axis moves are present only in the reference-design tail
  (examples A4 and A5).


## Case notes (reference-design tail evidence)

Multi-rule single-fix frequency: in this block, 3 out of 12 VIA12 moves each cleared
violations from 2-3 distinct rules. When spatial clustering shows overlapping violation
bboxes from different rules at the same location, treat them as one compound fix.
A single rule can also double-report one physical site through deck rule variants:
the two M1.S.6 markers [6408,3457,6480,3499] and [6405,3464,6483,3492] outline the
same corner pair, so marker count can exceed physical site count.