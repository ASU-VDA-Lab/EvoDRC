Now I have all the information needed. Let me produce the updated knowledge body, incorporating iteration 5 findings and fixing all hypothesis language.

---

## Per-rule recipes

### Family A: M1-via cluster (V0.M1.AUX.3, M1.S.2, M1.S.6, V1.M1.EN.1)

These four rules often cluster around a VIA_VIA12 instance placed where local M1
geometry fails width-matching, spacing, or enclosure constraints -- a single site
usually fires one to three of them, not necessarily all four. In the 37-violation
example block, 18 of 37 violations belong to this family (seed, reference-design-verified).

Rule semantics (ASAP7 rule deck):
- V0.M1.AUX.3: V0 width perpendicular to M1 length must equal M1 width at the landing
  location; M1 runs horizontally, perpendicular direction is y, so V0 y-extent must equal
  the M1 y-extent there (seed, reference-design-verified).
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
M1-VALID position -- observed moves include pure-x (+136 dbu: seed, reference-design-verified;
trial:i01.ug.whole_design.00), pure-y (+72, -48, +24, +96, -24, +48 dbu:
trial:i01.ug.whole_design.00), pure-x negative (-28 dbu: trial:i01.ug.whole_design.00),
pure-x ±36 dbu (trial:i02.ug.whole_design.00), pure-x +72 dbu
(trial:i04.ug.whole_design.00), and two-axis (e.g. the VIA12 at
(5220,3060) relocated to (5292,2952), delta (+72,-108): seed, reference-design-verified)
-- clears multiple rules of this family at once. A second repair strategy, confirmed
in trial:i05.ug.whole_design.00, is to delete the offending instance and add a
replacement via at a fully valid coordinate instead of sliding the original instance.

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
    but stricter than the rule minimum (seed, reference-design-verified). M1.S.2
    and M1.S.6 are incidentally cleared when the via moves away from the neighbor
    that was causing the tip/corner proximity.
  - Negative deltas are valid: moves in -x (e.g. -28 dbu for i0103 in
    trial:i01.ug.whole_design.00; -36 dbu for i0011 and i0131 in
    trial:i02.ug.whole_design.00) and -y (e.g. -48 dbu for i0112/i0105,
    -24 dbu for i0067/i0070 in trial:i01.ug.whole_design.00) clear violations
    when the conflict is on the positive side.
Step 3. Apply the delta to VIA_VIA12. Alternatively, delete the instance and add
  a replacement via at the target coordinate; this delete+add strategy is confirmed
  as a valid substitute for move_instance (trial:i05.ug.whole_design.00).
Step 4. If a VIA_VIA23 is co-located at the same (x, y) (stacked via), decide
  PER LEVEL -- co-located vias do NOT always travel together (seed, reference-design-verified):
  (a) COUPLED case: if the M2 landing must move with the V1 fix (the M2 polygon
      itself is co-moved), move VIA23 by the same delta (verified: the stacked
      pair at (5652,5220) both moved +64 in x, together with the associated
      TOP-LEVEL M2 pad and M3 routing polygons; the vias' own M1/M2 lands
      travel inside the instances -- no top-level M1 was involved: seed,
      reference-design-verified).
  (b) ANCHOR case: if VIA23's own levels (M2-M3) remain correctly aligned at
      the ORIGINAL coordinate, leave VIA23 in place and move only VIA12
      (verified: VIA12 (3204,1980)->(3340,1980) +136 while the co-located
      VIA23 stayed at (3204,1980) as the M2-M3 anchor: seed, reference-design-verified).
  (c) PARTIAL case: on ONE axis the two vias share the same delta; on the other
      axis their deltas differ (verified: at (6228,2340) both took +8 in y, but
      VIA12 took +36 in x while VIA23 took 0: seed, reference-design-verified).
  Pre-move check (the deciding question): after moving VIA12, does the V2 level
  at the OLD position still need VIA23 there to reach M3, and does VIA23's own
  alignment stay legal? If yes to both -> anchor case, do not move it.
Step 5. Re-establish LANDING coverage at the via's NEW position -- the
  requirement is coverage, not a particular op. The via's own M1/M2 lands
  travel inside the instance; the editing targets at the top level are the M2
  (layer 20) landing/routing polygons (and M3 for the VIA23 level, Step 6) --
  in repairs confined to M1/V1/M2 layers, no top-level M1 (layer 19) polygons
  need to be touched (seed, reference-design-verified; trial:i02.ug.whole_design.00).
  When violation sites are confined to M1 and V1, and all repaired instances carry
  their own M2 lands inside the cell, instance moves alone are sufficient -- no
  separate polygon coverage ops are required (trial:i02.ug.whole_design.00;
  trial:i04.ug.whole_design.00).
  When routing stubs at M2 or higher extend beyond the instance boundary, co-move
  or end-extend them: an ISOLATED landing pad can simply move by the same delta;
  a pad attached to a routing stub is typically reshaped or end-extended instead,
  and its deltas need not equal the via's (observed: the via at (6228,2340) moved
  (+36,+8) while its M2 pad moved (+92,+8): seed, reference-design-verified).
  When an instance move is paired with a resize_end on a routing polygon, the resize
  delta is independent of the move delta: i0111 and i0025 each moved +72 dbu in x
  while their associated polygons p951 and p955 each received a +128 dbu x-high
  resize_end (trial:i05.ug.whole_design.00).
  Never break metal continuity (seed, reference-design-verified; trial:i01.ug.whole_design.00).
Step 6. VIA_VIA23 is the M2-M3 via: after any VIA23 move, BOTH levels need
  coverage. If it now falls outside the M2 routing polygon (layer M2), move or
  extend the M2 polygon to cover it; likewise verify the M3 side still covers
  the via at its new location (M3 coverage loss is a connectivity break that
  window DRC does not reliably detect: seed, reference-design-verified).
  Two modes are observed, on WHICHEVER affected level (top-level M2 or M3):
  (a) Co-move: the polygon translates by the same delta as the via (observed on
      both an M2 pad and an M3 routing polygon in worked example A1: seed,
      reference-design-verified).
  (b) Extend: one edge is stretched to reach the new via position (observed on
      M2 in example A2, on M3 in example A4: seed, reference-design-verified;
      confirmed by resize_end ops on p879 (+48 dbu, y-high) and p910 (+20 dbu,
      y-high) in trial:i01.ug.whole_design.00; and on x-axis by p951 (+128 dbu,
      x-high) and p955 (+128 dbu, x-high) in trial:i05.ug.whole_design.00).
Step 7. Higher metal layers (M4, M5) and their vias (V3, V4) require coverage
  adjustment when routing at those levels abuts the repair site; apply the
  co-move-or-extend logic per level (trial:i01.ug.whole_design.00).
  When only M1, M2, and V1 are in the touched-layers set, no M3+ polygon ops are
  included in the repair pass (trial:i02.ug.whole_design.00; trial:i04.ug.whole_design.00).
  However, M1/M2/V1-only instance moves can introduce V2.M3.EN.2 violations as
  in-crop side effects -- 6 such violations arose in trial:i04.ug.whole_design.00
  from 6 pure-x instance moves. These are accepted as in-crop debt for a subsequent
  M3-layer repair pass; the M3 resize ops that address them (VIA23 shape y-resize,
  polygons p891-p897 y-resize -64 dbu each) appear in the assemble_drops record
  and are not applied inline (trial:i04.ug.whole_design.00).

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
  land at its new x. No top-level M1 polygon was edited: the V1.M1.EN.1 side
  closes because the RELOCATED via's own M1 land merges with the M1 already
  present at the new position (seed, reference-design-verified). Enclosure is
  checked on MERGED metal; derive enclosure from the merged polygon at the new
  position, not from any single pre-merge polygon alone (seed, reference-design-verified).

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
  does not imply co-movement during it (seed, reference-design-verified).

Connectivity preservation (Family A): the via's own M1/M2 lands travel with the
instance, so the V1 cut never leaves its lands. Top-level M2 pads/routing are
co-moved or end-extended so the via's M2 land stays merged with its net; the
VIA23 level likewise keeps M2 AND M3 coverage (seed, reference-design-verified;
trial:i01.ug.whole_design.00). Via cell definitions are not touched; only instance
placements and top-level routing polygons change.

---

## Measured facts from iteration 1 (trial:i01.ug.whole_design.00)

Provenance: whole_design unit, 19 operations, conn_preserved=true, gated_in.
Layers touched: M1, M2, M3, M4, M5, V1, V2, V3, V4.

- Instance pairs consistently move together at identical deltas in this pass:
  (i0113,i0099) at (0,+72); (i0112,i0105) at (0,-48); (i0001,i0002) at (0,+24);
  (i0073,i0075) at (0,+96); (i0067,i0070) at (0,-24); (i0062,i0076) at (0,+48);
  (i0061,i0104) at (+8,0). Treat spatially co-located paired instances as a single
  coupled move unit within a given pass (trial:i01.ug.whole_design.00). This
  pairing relationship does not persist across passes: six of these partner instances
  (i0105, i0075, i0076, i0099, i0002, i0070) are individually deleted in iter 5
  without their former pair partners (trial:i05.ug.whole_design.00).

- Negative deltas clear violations as readily as positive ones: -28 dbu in x
  (i0103) and -48/-24 dbu in y are among the 19 confirmed ops
  (trial:i01.ug.whole_design.00).

- Polygon coverage ops at higher levels use resize_end (stretch one end) and move:
  p879 y-high end extended +48 dbu; p910 moved +8 in x then y-high end extended
  +20 dbu (trial:i01.ug.whole_design.00).

- Higher metal layers (M4, M5) and their vias (V3, V4) required adjustment in the
  same repair pass; the co-move-or-extend logic applies at every affected level
  (trial:i01.ug.whole_design.00).

---

## Measured facts from iteration 2 (trial:i02.ug.whole_design.00)

Provenance: whole_design unit, 7 operations, conn_preserved=true, gated_in.
Layers touched: M1, M2, V1 only.

- All 7 ops are move_instance with pure-x deltas of ±36 dbu (9 nm): i0011 at
  (-36,0), i0017/i0019/i0025/i0056/i0111 each at (+36,0), i0131 at (-36,0)
  (trial:i02.ug.whole_design.00).

- A single repair pass can contain both +x and -x moves simultaneously: two
  instances moved -36 while five moved +36, confirming that direction is
  determined per-instance by the local conflict geometry, not by a global
  direction convention (trial:i02.ug.whole_design.00).

- When the touched-layer set is limited to M1, M2, and V1, no separate polygon
  coverage operations are required beyond the instance moves: the instances'
  internal M1 and M2 lands suffice to restore coverage, and no M3+ levels need
  adjustment (trial:i02.ug.whole_design.00).

- The ±36 dbu (9 nm) x-step is a confirmed repair quantum in addition to the
  previously recorded ±136, ±64, +8, ±72, ±48, ±24, ±96 dbu values
  (trial:i02.ug.whole_design.00).

---

## Measured facts from iteration 4 (trial:i04.ug.whole_design.00)

Provenance: whole_design unit, 6 operations, conn_preserved=true, gated_in.
Layers touched: M1, M2, V1 only.

- All 6 ops are move_instance with pure-x deltas: i0012 at (-36,0), i0117 at
  (+36,0), i0131/i0017/i0019/i0011 each at (+72,0)
  (trial:i04.ug.whole_design.00).

- +72 dbu (18 nm) in x is a confirmed repair quantum; four instances shared this
  delta in a single pass (trial:i04.ug.whole_design.00). The confirmed pure-x
  repair quanta now include: ±28, ±36, +64, +72, +136 dbu (trial:i01.ug.whole_design.00;
  trial:i02.ug.whole_design.00; trial:i04.ug.whole_design.00; seed,
  reference-design-verified).

- A single pass can mix three distinct x-deltas (-36, +36, +72) simultaneously,
  confirming that delta magnitude and direction are determined per-instance by local
  conflict geometry (trial:i04.ug.whole_design.00).

- Instance IDs i0011, i0017, i0019, i0131 each appear in both iter 2 and iter 4
  with different deltas (i0131: -36 in iter 2, +72 in iter 4; i0011: -36 in iter 2,
  +72 in iter 4). The same instance can be repositioned in multiple passes across
  iterations as the accumulated design state changes (trial:i02.ug.whole_design.00;
  trial:i04.ug.whole_design.00).

- The M1/M2/V1-only move set introduced 6 new in-crop V2.M3.EN.2 violations as a
  side effect. The assemble_drops record for this trial contains the M3-level ops
  that address them -- VIA_VIA23_1_3_36_36 M3-shape y-axis resize -40 dbu, and
  polygons p891 through p897 y-axis resize -64 dbu each -- but those ops were
  dropped from this assembly (reason: cu_pool:applied) and deferred. The pass
  gated_in with these violations present as in-crop debt
  (trial:i04.ug.whole_design.00).

- When the touched-layer set is limited to M1, M2, and V1, no polygon coverage
  operations are included in the repair pass even when instance moves introduce
  violations at higher layers; those violations are deferred as in-crop debt for
  a subsequent layer-appropriate repair pass (trial:i04.ug.whole_design.00).

---

## Measured facts from iteration 5 (trial:i05.ug.whole_design.00)

Provenance: whole_design unit, 19 operations, conn_preserved=true, gated_in.
Layers touched: M1, M2, M3, M4, V1, V3.
n_new_in_crop=0, n_new_out_of_crop=0 (clean gate).

Three new op types appear: delete_instance, add_via, and resize_end on the x-axis.

- delete_instance is a confirmed repair op: 7 instances deleted (i0098, i0105,
  i0075, i0076, i0099, i0002, i0070). Six of these (i0105, i0075, i0076, i0099,
  i0002, i0070) were the paired-move members from iter 1; deletion after prior moves
  is a valid outcome across passes (trial:i05.ug.whole_design.00).

- add_via VIA_VIA34 is a confirmed repair op: 7 VIA_VIA34 (M3-M4 level) instances
  placed at explicit coordinates ((2200,2160), (2200,4272), (2200,6576), (2200,8688),
  (2968,3312), (2968,5424), (2968,7536)). The count of adds equals the count of
  deletes in this pass; VIA_VIA34 is a distinct via type from the deleted instances
  (trial:i05.ug.whole_design.00).

- resize_end on the x-axis is confirmed: polygons p951 and p955 each receive a
  +128 dbu extension at the high-x end, paired with the +72 dbu x-moves of i0111
  and i0025 respectively. Prior resize_end ops were y-axis only (p879 +48 y-high,
  p910 +20 y-high in trial:i01.ug.whole_design.00); x-axis resize_end is now
  confirmed as a distinct op mode (trial:i05.ug.whole_design.00).

- 128 dbu is a confirmed resize_end delta quantum. The confirmed resize_end deltas
  are now: +20, +48 dbu on y-axis (trial:i01.ug.whole_design.00) and +128 dbu on
  x-axis (trial:i05.ug.whole_design.00).

- Instance IDs i0111 and i0025 moved +72 dbu in x in iter 5 after each moving +36
  dbu in x in iter 2, accumulating net x-displacement across passes. Instance i0012
  moved -36 dbu in x in both iter 4 and iter 5, accumulating -72 dbu net x-displacement
  across those two passes (trial:i02.ug.whole_design.00; trial:i04.ug.whole_design.00;
  trial:i05.ug.whole_design.00).

- The pass gated_in with zero new violations despite a mix of move_instance,
  delete_instance, add_via, and resize_end ops across M1, M2, M3, M4, V1, and V3
  layers, confirming that heterogeneous op combinations achieve a clean gate when
  applied consistently (trial:i05.ug.whole_design.00).

---

## Final-pair measured facts (reference-design tail evidence)

Provenance: these facts come from the final-pair comparison of the reference
design's initial layout against its repaired final layout, plus the BEFORE and
AFTER DRC reports.

- Moving via instances without touching cell definitions is sufficient to clear
  V0.M1.AUX.3, V1.M1.EN.1, M1.S.2, and M1.S.6, provided metal polygons are
  co-moved or extended to maintain coverage (seed, reference-design-verified).

- A single via move can simultaneously clear violations under 3 different rules
  (confirmed by the A3 example: one VIA12 move clears V0.M1.AUX.3, V1.M1.EN.1,
  and M1.S.2 at once: seed, reference-design-verified).

---

## Case notes (reference-design tail evidence)

Multi-rule single-fix frequency: in this block, 3 out of 12 VIA12 moves each cleared
violations from 2-3 distinct rules (seed, reference-design-verified). When spatial
clustering shows overlapping violation bboxes from different rules at the same location,
treat them as one compound fix (seed, reference-design-verified).

A single rule can also double-report one physical site through deck rule variants:
the two M1.S.6 markers [6408,3457,6480,3499] and [6405,3464,6483,3492] outline the
same corner pair, so marker count can exceed physical site count (seed, reference-design-verified).