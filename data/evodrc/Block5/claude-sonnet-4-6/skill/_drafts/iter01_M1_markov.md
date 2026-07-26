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
M1-VALID position -- observed moves include pure-x deltas of 4, 36, 108, and 112
dbu (trial:i01.ug.leaf_0006.05, trial:i01.ug.leaf_0001.02, trial:i01.ug.Block5_union_row3.00,
trial:i01.ug.Block5_union_row6.01, trial:i01.ug.leaf_0005.04) and two-axis moves
(e.g. the VIA12 at (5220,3060) relocated to (5292,2952), delta (+72,-108)) -- or
extending the M2-level routing can clear multiple rules of this family at once.

Iteration-1 evidence reinforces: all six repaired loci in iteration 1 used
x-axis-only via moves (y-delta = 0 throughout); all preserved connectivity
(trial:i01.ug.Block5_union_row3.00, trial:i01.ug.Block5_union_row6.01,
trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04,
trial:i01.ug.leaf_0006.05). This does not exclude y-moves (the seed A4 example
used a pure-y delta), but x-axis moves are sufficient in many sites and should
be tried first when the violation is in the x-proximity.

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
    for >= 20 dbu on BOTH x-sides -- a conservative working target, sufficient
    but stricter than the rule minimum. M1.S.2 and M1.S.6 are incidentally
    cleared when the via moves away from the neighbor that was causing the
    tip/corner proximity.
  - Very small x-deltas are sometimes sufficient: a move of 4 dbu (1 nm) cleared
    the violation at locus [3832,6588,5328,7452] (trial:i01.ug.leaf_0006.05).
    Do not default to large moves when the geometry is close to legal.
Step 3. Apply the delta to VIA_VIA12. When two instances at the same locus are
  both contributing to the violation, they may need to move in OPPOSITE x-directions
  (divergent pair): +36 dbu on one instance and -36 dbu on another cleared the
  locus [3520,4428,4464,6372] (trial:i01.ug.leaf_0002.03). In that case each via
  moves to the legal M1 region on its respective side; connectivity is preserved
  because each via's own lands travel with the instance.
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
  in this repair ZERO top-level M1 (layer 19) polygons were touched. Two
  adjustment operations are observed:
  (a) Move: the polygon translates by the same delta as the via (observed: seed
      examples A1, A3; also iteration-1 moves in trial:i01.ug.Block5_union_row3.00
      and trial:i01.ug.leaf_0001.02 where n_ops = 1 or 2 move_instance ops only).
  (b) Resize: one axis of the polygon is expanded by a scalar delta_dbu to reach
      the new via position (observed: trial:i01.ug.Block5_union_row6.01, where
      polygon p955 was resized +256 dbu on axis x and polygon p971 was resized
      +328 dbu on axis x, each larger than the accompanying +108 dbu via moves).
      The resize delta need not equal the via delta; it must be large enough that
      the polygon fully covers the via's land at its new coordinate.
  Never break metal continuity in the process.
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

Worked example A6 (divergent-pair x-moves, delta +36 / -36 dbu, trial:i01.ug.leaf_0002.03):
  Two instances at locus [3520,4428,4464,6372]: i0056 moves (+36,0), i0103 moves (-36,0).
  These opposite-direction x-moves space the two vias apart to clear the shared violation.
  Connectivity preserved; no polygon resize ops required at this locus (n_ops = 2,
  both move_instance). Touched layers: M1, M2, V1.

Worked example A7 (two-instance co-move +108 dbu x, with resize, trial:i01.ug.Block5_union_row6.01):
  Locus [5776,7668,8352,8532]: i0025 and i0019 each move (+108,0).
  Polygon p955 resized +256 dbu on axis x; polygon p971 resized +328 dbu on axis x.
  Resize deltas (256, 328) substantially exceed the via move delta (108) -- the
  polygons must span both old and new via positions to maintain continuous coverage.
  Touched layers: M1, M2, V1.

Connectivity preservation (Family A): the via's own M1/M2 lands travel with the
instance, so the V1 cut never leaves its lands. Top-level M2 pads/routing are
co-moved or resized so the via's M2 land stays merged with its net; the
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
  co-moved or resized to maintain coverage.

- A single via move can simultaneously clear violations under 3 different rules
  (confirmed by the A3 example: one VIA12 move clears V0.M1.AUX.3, V1.M1.EN.1,
  and M1.S.2 at once).

- Polygon coverage adjustment uses either move (same delta as the via) or resize
  (axis-aligned scalar expansion, delta >= via delta). Resize deltas can be
  substantially larger than the via move delta (trial:i01.ug.Block5_union_row6.01:
  +256 and +328 dbu resize vs +108 dbu via move).

- Very small x-moves (4 dbu = 1 nm) are sufficient to resolve some violations
  (trial:i01.ug.leaf_0006.05). Use the minimum move that achieves legal geometry;
  do not default to large displacements.

- Two co-locus instances can be moved in opposite x-directions (divergent pair:
  +36 and -36 dbu) to clear a shared violation without any polygon resize
  (trial:i01.ug.leaf_0002.03).

- All six iteration-1 repairs used x-axis-only via moves (y-delta = 0) and all
  preserved connectivity with zero new violations inside or outside the crop
  (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.Block5_union_row6.01,
  trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03,
  trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05).


## Case notes (reference-design tail evidence)

Multi-rule single-fix frequency: in the seed block, 3 out of 12 VIA12 moves each cleared
violations from 2-3 distinct rules. When spatial clustering shows overlapping violation
bboxes from different rules at the same location, treat them as one compound fix.
A single rule can also double-report one physical site through deck rule variants:
the two M1.S.6 markers [6408,3457,6480,3499] and [6405,3464,6483,3492] outline the
same corner pair, so marker count can exceed physical site count.

Iteration-1 op-count distribution: 4 of 6 repairs used 1-2 move_instance ops only;
1 used 4 ops (2 move_instance + 2 resize); 1 used 2 move_instance ops with opposite
signs. When n_ops is low and touched_layers are M1/M2/V1 only, the via move alone
carries the fix and no M3-level edits are required.