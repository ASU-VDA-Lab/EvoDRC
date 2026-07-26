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
M1-VALID position -- observed moves include pure-x (e.g. trial:i01.ug.Block6_union_row3.00,
trial:i01.ug.Block6_union_row8.03, trial:i01.ug.leaf_0011.05, trial:i01.ug.leaf_0018.07),
pure-y (e.g. the VIA12 at (5364,5724) relocated to (5364,5792), delta (0,+68)), and
two-axis (e.g. the VIA12 at (5220,3060) relocated to (5292,2952), delta (+72,-108)) --
or extending the M2-level routing can clear multiple rules of this family at once
(the multi-rule examples below -- A2, A3, A5 -- clear 2-3 rules per move; A1 and A4
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
Step 3. Apply the delta to VIA_VIA12. Multiple VIA_VIA12 instances within the
  same repair locus may require the SAME delta and should all be moved together
  (trial:i01.ug.Block6_union_row3.00 moved 3 instances by [+72,0]; trial:i01.ug.Block6_union_row5.01
  moved 4 instances by [+36,0]; trial:i01.ug.leaf_0015.06 moved 2 instances by [+28,0]).
  Not all instances in a locus necessarily move: trial:i01.ug.Block6_union_row7.02
  moved i0093 by [+104,0] and i0074 by [-36,0] -- opposite directions -- within
  the same repair window.
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
  When no polygon resize is needed, the instance move alone suffices (trial:i01.ug.Block6_union_row8.03
  single move [+36,0] no polygon op; trial:i01.ug.leaf_0011.05 single move [+36,0] no polygon op;
  trial:i01.ug.leaf_0018.07 single move [+36,0] no polygon op). When coverage must be
  extended, use resize_end:
  - end="high" with delta_dbu N: the high-x (or high-y) edge of the polygon
    extends by N dbu in the positive direction (trial:i01.ug.Block6_union_row5.01:
    p2072 high-x end +92 while instances moved +36; trial:i01.ug.leaf_0001.04:
    p2016 high-x end +132 while instance moved +112; trial:i01.ug.leaf_0015.06:
    p1923 high-x end +48 while instances moved +28).
  - end="low" with delta_dbu N: the low-x (or low-y) edge extends by N dbu
    in the negative direction, i.e., leftward (trial:i01.ug.Block6_union_row7.02:
    p1920 low-x end +56 while instance i0074 moved -36 in x).
  An ISOLATED landing pad can simply move by the same delta; a pad attached to
  (or part of) a routing stub is typically reshaped or end-extended instead,
  and its extension delta need not equal the via's (observed: the via at (6228,2340)
  moved (+36,+8) while its M2 pad moved (+92,+8); trial:i01.ug.Block6_union_row7.02
  instance +104 but polygon high end +124). Never break metal continuity in the process.
  The polygon extension magnitude consistently meets or exceeds the instance move
  magnitude: across all iteration-1 resize_end ops, |polygon_delta| >= |instance_delta|
  (trial:i01.ug.Block6_union_row5.01: 92 >= 36; trial:i01.ug.Block6_union_row7.02:
  124 >= 104 and 56 >= 36; trial:i01.ug.leaf_0001.04: 132 >= 112;
  trial:i01.ug.leaf_0015.06: 48 >= 28).
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

Worked example B1 (iteration-1, three-instance co-move, delta [+72,0]):
  Locus [5992,4428,9648,5292] (Block6_union_row3). Three instances i0471, i0324,
  i0481 each moved by [+72,0] dbu. No polygon resize required. All layers M1,
  M2, V1 affected through the instance lands alone (trial:i01.ug.Block6_union_row3.00).

Worked example B2 (iteration-1, four-instance co-move + high-end polygon extend):
  Locus [6856,6588,14832,7452] (Block6_union_row5). Four instances i0015, i0459,
  i0437, i0446 each moved by [+36,0] dbu. Polygon p2072 high-x end extended
  by +92 dbu (larger than the instance delta) to maintain M2 routing coverage.
  (trial:i01.ug.Block6_union_row5.01).

Worked example B3 (iteration-1, bidirectional moves within one locus):
  Locus [8368,8748,14400,9612] (Block6_union_row7). Two instances moved in
  OPPOSITE x-directions within the same repair window:
  - i0093 moved [+104,0]; polygon p1903 high-x end extended +124 dbu.
  - i0074 moved [-36,0]; polygon p1920 low-x end extended +56 dbu (leftward).
  Both connectivity checks passed (trial:i01.ug.Block6_union_row7.02).

Worked example B4 (iteration-1, leaf cell, instance + high-end extend):
  Locus [10096,3348,10944,4212] (leaf_0001). Instance i0404 moved [+112,0];
  polygon p2016 high-x end extended +132 dbu. Excess of 20 dbu matches the
  5 nm enclosure requirement (trial:i01.ug.leaf_0001.04).

Worked example B5 (iteration-1, leaf cell, two-instance co-move + extend):
  Locus [3088,9828,4680,11744] (leaf_0015). Two instances i0213 and i0204 each
  moved [+28,0]; polygon p1923 high-x end extended +48 dbu (trial:i01.ug.leaf_0015.06).

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

- When multiple instances within a locus require the same delta, all are moved
  together in a single repair op (trial:i01.ug.Block6_union_row3.00: 3 instances;
  trial:i01.ug.Block6_union_row5.01: 4 instances; trial:i01.ug.leaf_0015.06: 2 instances).

- Instances within the same repair locus can move in opposite directions
  (trial:i01.ug.Block6_union_row7.02: i0093 +104 vs i0074 -36 in x); the associated
  polygon for each instance extends toward that instance's new position.

- Single-instance moves with no polygon resize are valid and sufficient when the
  via's own lands fully re-establish coverage at the new position
  (trial:i01.ug.Block6_union_row8.03, trial:i01.ug.leaf_0011.05, trial:i01.ug.leaf_0018.07:
  all single-instance [+36,0] moves, no polygon op, conn_preserved=true).

- When a polygon end-extension is needed, its magnitude meets or exceeds the
  corresponding instance delta in absolute value across all measured cases
  (trial:i01.ug.Block6_union_row5.01: |92| >= |36|; trial:i01.ug.Block6_union_row7.02:
  |124| >= |104| and |56| >= |36|; trial:i01.ug.leaf_0001.04: |132| >= |112|;
  trial:i01.ug.leaf_0015.06: |48| >= |28|). In four of these five cases the
  excess is exactly 20 dbu (5 nm), matching the V1.M1.EN.1 enclosure minimum.

- All iteration-1 accepted repairs introduced zero new violations inside the crop
  window and zero outside it (n_new_in_crop=0, n_new_out_of_crop=0 across all 8
  trial:i01.* records).


## Case notes (reference-design tail evidence)

Multi-rule single-fix frequency: in this block, 3 out of 12 VIA12 moves each cleared
violations from 2-3 distinct rules. When spatial clustering shows overlapping violation
bboxes from different rules at the same location, treat them as one compound fix.
A single rule can also double-report one physical site through deck rule variants:
the two M1.S.6 markers [6408,3457,6480,3499] and [6405,3464,6483,3492] outline the
same corner pair, so marker count can exceed physical site count.

Multi-instance locus frequency (iteration 1): 5 of 8 accepted repairs moved more than
one instance. The maximum observed was 4 instances co-moved at the same delta
(trial:i01.ug.Block6_union_row5.01). When a locus bbox spans a wide x-range
(e.g. >7000 dbu wide in trial:i01.ug.Block6_union_row5.01 and trial:i01.ug.Block6_union_row7.02)
expect multiple instances to be involved.