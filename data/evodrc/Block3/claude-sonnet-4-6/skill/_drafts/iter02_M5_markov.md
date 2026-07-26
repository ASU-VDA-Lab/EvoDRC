## Per-rule recipes

### Family C: M5 off-grid vertical edges (M5.AUX.1)

Rule semantics:
- M5.AUX.1: M5 vertical edges (x-coordinates) must lie on the 24 nm = 96 dbu grid.
- M5.AUX.2 (latent partner): minimum-width M5 tracks must ALSO have their
  centerline on a legal vertical routing track: center_x mod 192 == 48. The
  deck evaluates this check ONLY for polygons whose x-edges already sit on the
  96 grid (off-grid polygons are skipped), so a stripe currently failing
  M5.AUX.1 reports NO M5.AUX.2 violation -- the track constraint is dormant,
  and a wrong-phase mod-96 snap surfaces it as a NEW violation. This is the
  same double-grid structure as M4 in Family B (-> see M4.md / V3.md).

Root cause pattern: a minimum-width M5 stripe (96 dbu wide) with x_left at a
residual r = x_left mod 192 that is neither 0 mod 96 (M5.AUX.1) nor placing
the centerline at 48 mod 192 (M5.AUX.2). Two confirmed residues across
iterations: r=88 (seed, reference-design-verified) and r=160 (trial:i02.ug.leaf_0004.03).

Recipe -- Uniform x-shift to snap M5 to grid:

Step 1. Compute the TRACK residual r = x_left mod 192 (in dbu). For a
  minimum-width (96 dbu) stripe the legal positions are x_left == 0 mod 192:
  that puts both edges on the 96 grid (M5.AUX.1) and the centerline at
  center_x mod 192 == 48 (M5.AUX.2). The two NEAREST legal candidates are
  delta_x = -r and delta_x = +(192 - r); take the smaller magnitude.
  - r=88: delta_x = -88 (nearest; +104 is legal but larger; +8 is NOT legal --
    it lands centerline at 144 mod 192, an illegal track) (seed, reference-design-verified).
  - r=160: delta_x = +32 (nearest; -160 is legal but larger) (trial:i02.ug.leaf_0004.03).
  - r=184: delta_x = +8 (nearest; -184 is legal but larger) (seed, reference-design-verified).
  Legality repeats every 192 dbu.

Step 2. Shift the M5 polygon by delta_x in x; y is unchanged.

Step 3. For every VIA_VIA45 instance associated with this M5 polygon, apply the
  same delta_x. This keeps V4 centered inside M5. In trial:i02.ug.leaf_0004.03
  four VIA instance pairs each received x-component +32, matching the M5 polygon
  shift exactly.

Step 4. Because VIA45 x-position changed, check the MERGED M4 around it. If the
  merged M4 (top-level polygon + via cell's own M4 land) is no longer valid or
  connected at the new x, adjust the top-level M4 x-extent (ties to Family B (-> see M4.md / V3.md)
  Step 3). Do not require the top-level polygon alone to contain the via.

Worked example C1 (M5 polygon at x=1816-1912, 2 of the 4 M5.AUX.1 violations):
  M5 BEFORE x=1816-1912. r = 1816 mod 192 = 88; edges off the 96 grid, and the
  centerline (1864, at 136 mod 192) is also off-track but dormant while
  M5.AUX.1 fails.
  M5 AFTER x=1728-1824. 1728=18*96, 1824=19*96; centerline 1776 = 9*192 + 48.
  Delta: -88 dbu in x (nearest candidates -88/+104). M5 y unchanged.
  All VIA45 at this M5 shift by -88 in x.
  Violation [1816,1832,1912,6572] cleared (both x-edges were off-grid).
  Violation [1816,6388,1912,6572] also cleared (sub-region of same polygon).
  (seed, reference-design-verified)

Worked example C2 (M5 polygon at x=1432-1528, 2 violations):
  M5 BEFORE x=1432-1528. r = 1432 mod 192 = 88 -- same phase as C1, so the
  same -88 snap applies.
  M5 AFTER x=1344-1440. 1344=14*96, 1440=15*96; centerline 1392 = 7*192 + 48.
  Violations at [1432,988,1528,1172] and [1432,7468,1528,7652] cleared.
  (seed, reference-design-verified)

Worked example C3 (M5 polygon p1059, r=160 phase, trial:i02.ug.leaf_0004.03):
  M5 shift: +32 dbu in x (nearest candidates +32/-160). Four VIA instance pairs
  each received x-component +32. Four M4 polygons (p1101-p1104) received
  simultaneous y-end resizes (+72, +24, -24, -72 on the appropriate ends) to
  maintain M4 enclosure geometry after the coupled VIA moves. The repair was
  accepted with n_new_in_crop=2 because conn_preserved=true; the acceptance gate
  is connectivity preservation, not zero new violations.

Geometry preservation (Family C): M5 polygon moves as a rigid body. VIA45
co-moves with matching x-delta, maintaining full overlap with M5. M4 is also
reshaped (Family B (-> see M4.md / V3.md)) to maintain overlap from below.

---

### Family C-Y: Pure y-axis via-stack adjustment touching M5 layer

Trial:i02.ug.leaf_0003.02 demonstrates a repair that lists M5 in touched_layers
but involves no M5 polygon shape change: all 6 ops are `move_instance` with
y-only deltas ([0,-48], [0,-48], [0,96], [0,96], [0,48], [0,48]) affecting
VIA/metal instances spanning M3, M4, M5, V3, V4. The M5 polygon geometry itself
was not altered; only the via-stack instances co-located with M5 were repositioned
in y. This repair introduced zero new violations (n_new_in_crop=0) and preserved
connectivity (conn_preserved=true, gated_in).

When the repair record lists M5 in touched_layers but contains no polygon-level
ops on M5 (no `move`/`resize_end` with an M5 polygon_id), the M5 contribution is
via instance co-motion only; the AUX.1/AUX.2 grid constraints on M5 vertical
edges are not implicated by y-only instance moves (trial:i02.ug.leaf_0003.02).

---

## Acceptance gate

A repair is accepted ("gated_in") when conn_preserved=true, regardless of
n_new_in_crop (trial:i02.ug.leaf_0004.03 was accepted with n_new_in_crop=2).
Zero new violations is not required for acceptance. When evaluating whether a
proposed repair is safe to commit, check conn_preserved first; new in-crop
violations are a secondary signal that may require a follow-on repair pass.

---

## Final-pair measured facts (reference-design tail evidence)

Provenance: these facts come from the final-pair comparison of the reference
design's initial layout against its repaired final layout, plus the BEFORE and
AFTER DRC reports. Every coordinate and delta cited in this document is quoted
inline from that pair; the layout files themselves are not needed and are not
shipped with this skill.

- M5.AUX.1 is resolved by coordinate snapping (x-shift of the stripe), with the
  M5.AUX.2 track parity (center_x mod 192 == 48) picking the snap direction.
  The M4 grid fixes are NOT mere snapping: they combine y-edge snapping
  (M4.AUX.1), height normalization to the V3 height, track parity (center_y mod
  192 == 48, M4.AUX.2), and the coupled VIA34/VIA45 moves. No object add/delete
  was needed in either of these cases -- a property of these repairs, not a
  universal rule. (seed, reference-design-verified)

- The x-snap formula (delta_x = smaller of -r and +(192-r), where r = x_left mod
  192) is confirmed across two distinct residues: r=88 → delta_x=-88
  (seed, reference-design-verified) and r=160 → delta_x=+32 (trial:i02.ug.leaf_0004.03).

- Multi-stack repairs: a single trial can move multiple VIA instance pairs at
  different y-offsets (four pairs at y-deltas of ±24 and ±72) while applying a
  uniform x-delta (+32) across all of them, with matched M4 y-end resizes per
  stack (trial:i02.ug.leaf_0004.03).

---

## Case notes (reference-design tail evidence)

M5 and M4 are tightly coupled: M5.AUX.1 drives M5 x-shift. That shift forces
VIA45 x-move. VIA45 x-move forces a top-level M4 x-extent adjustment (to keep
the MERGED M4 valid around V4). M4.AUX.1 independently forces M4 y-move. VIA45
must track both, producing combined deltas such as (-88, -48) or (-88, +120) or
(+32, ±24) or (+32, ±72). Compute the x and y components separately, then sum.
(seed, reference-design-verified; x-delta generalized by trial:i02.ug.leaf_0004.03,
y-delta multi-stack pattern confirmed by trial:i02.ug.leaf_0004.03)