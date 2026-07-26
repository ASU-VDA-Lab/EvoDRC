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
M1-VALID position -- observed moves include pure-x deltas of +36, +64, and +128 dbu
(trials i01.ug.leaf_0004.04, i01.ug.Block2_union_row5.02, i01.ug.leaf_0001.03) and
the two-axis examples from the reference design -- or extending the M2-level routing
can clear multiple rules of this family at once. Single via moves that clear exactly
one violation are equally normal (trials i01.ug.leaf_0004.04, i01.ug.leaf_0007.05).

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
  - Observed working deltas: +36 dbu (9 nm) in x is the most frequent
    (trials i01.ug.leaf_0004.04, i01.ug.leaf_0007.05, i01.ug.leaf_0011.06,
    i01.ug.Block2_union_row1.00, i01.ug.Block2_union_row3.01); +64 dbu (16 nm)
    in x for wider separation needs (trial i01.ug.Block2_union_row5.02); +128 dbu
    (32 nm) in x when the enclosure deficit is larger (trial i01.ug.leaf_0001.03).
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
  in this repair ZERO top-level M1 (layer 19) polygons were touched. Two
  observed repair ops:
  (a) move_instance: an ISOLATED landing pad polygon translates by the same
      delta as the via.
  (b) resize_end: a polygon attached to a routing stub is end-extended on the
      axis of motion. The resize_end delta need not equal the via move delta --
      in trial i01.ug.leaf_0001.03 the via moved +128 dbu in x while one
      polygon's high end was extended +184 dbu and another polygon's low end
      was retracted -176 dbu, reflecting the routing geometry at that site.
      The standard case for a +x via move is resize_end axis:x end:high
      (trials i01.ug.Block2_union_row3.01, i01.ug.Block2_union_row5.02,
      i01.ug.leaf_0011.06), extending the trailing edge of the M2 routing
      polygon to maintain coverage at the new via position.
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
Step 7. Upper-metal propagation: when a repair site carries a via stack that
  reaches M4 or higher, the affected upper-metal routing polygon must also be
  adjusted to maintain coverage. Trial i01.ug.leaf_0001.03 touched layers M1,
  M2, M4, and V1 -- the single via move at +128 dbu in x required both an M2
  resize_end (high, +184 dbu) and an M4 resize_end (low, -176 dbu, retracting
  the far end of the M4 stub). Always enumerate ALL metal layers in the via
  stack and verify coverage at each level after a move.

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

Worked example A6 (two-via same-delta move, locus [7288,2268,9648,3132]):
  VIA instances i0159 and i0152 both move +36 dbu in x. No polygon resize ops.
  Connectivity preserved; zero new violations in or out of crop (trial i01.ug.Block2_union_row1.00).
  Pattern: when two vias in the same locus have the same alignment deficit, a
  shared single delta eliminates both violations and needs no polygon extension
  if the M2 stubs are already long enough to cover the new positions.

Worked example A7 (two-via move + one resize_end, locus [3400,4428,5760,5292]):
  VIA instances i0115 and i0103 both move +36 dbu in x; polygon p1040 extended
  +36 dbu on its high-x end (trial i01.ug.Block2_union_row3.01). Touches M1, M2, V1.
  The resize_end is required when at least one M2 routing polygon's high edge no
  longer covers the via at its new position after the +x move.

Worked example A8 (three-via move + two resize_end, locus [3400,6588,8136,7452]):
  VIA instances i0083, i0018, i0034 all move +64 dbu in x; polygons p1059 and
  p1057 each extended +64 dbu on their high-x end (trial i01.ug.Block2_union_row5.02).
  Touches M1, M2, V1. When multiple vias in a row share the same delta, the
  number of required polygon resizes equals the number of M2 routing stubs whose
  high edge falls short of the new via positions.

Worked example A9 (large delta + upper-metal adjustment, locus [4656,2112,5760,3132]):
  VIA instance i0086 moves +128 dbu in x. Polygon p1065 extended +184 dbu on
  high-x end; polygon p957 retracted -176 dbu on low-x end (trial i01.ug.leaf_0001.03).
  Touches M1, M2, M4, V1. The two polygon deltas differ from each other and from
  the via delta (+128), reflecting routing stubs of different lengths at this site.
  The M4-layer involvement confirms Step 7: upper-metal layers must be checked and
  adjusted whenever the via stack reaches them.

Connectivity preservation (Family A): the via's own M1/M2 lands travel with the
instance, so the V1 cut never leaves its lands. Top-level M2 pads/routing are
co-moved or end-extended so the via's M2 land stays merged with its net; the
VIA23 level likewise keeps M2 AND M3 coverage. Via cell definitions are not
touched; only instance placements and top-level M2/M3 polygons change. Upper-metal
layers (M4 and above) must also be verified for coverage when the via stack extends
that high (trial i01.ug.leaf_0001.03).

---

## Repair operation taxonomy

Two primitive ops cover all observed V1 repairs:

**move_instance** -- translate a via instance by a dbu delta. The instance's own
metal lands travel with it. All iteration 1 trials use this for the via itself.
Observed deltas (x-axis only in iteration 1): +36, +64, +128 dbu.

**resize_end** -- extend or retract one end of a routing polygon along a named
axis. Fields: axis (x or y), end (high or low), delta_dbu (signed, positive =
outward). Used to re-cover the via's landing pad at its new position. The resize
delta need not equal the via move delta (trial i01.ug.leaf_0001.03: via +128 x,
polygon high-end +184, different polygon low-end -176). The standard case for a
pure +x via move is resize_end axis:x end:high on the M2 routing polygon
(trials i01.ug.Block2_union_row3.01, i01.ug.Block2_union_row5.02,
i01.ug.leaf_0011.06).

When no polygon's high edge falls short of the new via position, no resize_end is
needed -- the move alone suffices (trials i01.ug.Block2_union_row1.00,
i01.ug.leaf_0004.04, i01.ug.leaf_0007.05).

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

## Iteration 1 measured facts

All 7 trials in iteration 1 (Block2, channel unit_gate) were gated_in with
conn_preserved=true and zero new violations in or out of crop. The full set
demonstrates:

- Pure x-axis moves suffice for all iteration 1 sites; no y component was needed
  at any of the seven loci (trials i01.ug.leaf_0004.04 through i01.ug.Block2_union_row5.02).

- A single +36 dbu move of one instance with no polygon op is the minimal repair
  that appears at two independent sites (trials i01.ug.leaf_0004.04,
  i01.ug.leaf_0007.05), confirming that small-delta pure-move repairs are
  connectivity-safe.

- Multi-via same-delta moves (2 or 3 instances sharing one delta) are valid and
  produce zero new violations (trials i01.ug.Block2_union_row1.00,
  i01.ug.Block2_union_row3.01, i01.ug.Block2_union_row5.02); the number of
  accompanying resize_end ops equals the number of M2 stubs whose high edge does
  not already reach the new via positions.

- resize_end polygon deltas are independent of via move deltas and must be computed
  from the routing geometry at each site, not copied from the via delta
  (trial i01.ug.leaf_0001.03).

- M4 (and by extension any upper-metal layer in the stack) can be a touched layer
  in a V1-level repair (trial i01.ug.leaf_0001.03). The repair remained
  connectivity-preserving, confirming that upper-metal adjustments are within scope.

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