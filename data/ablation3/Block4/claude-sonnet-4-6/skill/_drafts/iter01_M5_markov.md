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

Root cause pattern: both changed M5 polygons (96 dbu wide = minimum width) had
x_left at residual 88 both mod 96 and mod 192. Snapping by -88 puts the edges
on the 96 grid AND the centerline on a legal track (center_x mod 192 == 48).
Snapping by +8 would also fix M5.AUX.1, but lands the centerline at 144 mod
192 -- an illegal track that would surface a dormant M5.AUX.2. The full-deck
legal positions repeat every 192 dbu; the nearest candidates were -88 and
+104, and -88 is the smaller.

Recipe -- Uniform x-shift to snap M5 to grid:

Step 1. Compute the TRACK residual r = x_left mod 192 (in dbu). For a
  minimum-width (96 dbu) stripe the legal positions are x_left == 0 mod 192:
  that puts both edges on the 96 grid (M5.AUX.1) and the centerline at
  center_x mod 192 == 48 (M5.AUX.2). The two NEAREST legal candidates are
  delta_x = -r and delta_x = +(192 - r), and legality repeats every 192 dbu;
  take the smaller magnitude. In this pair both stripes
  had r == 88, so delta_x = -88 (+104 is legal but larger; a plain mod-96 snap
  of +8 is NOT legal -- it lands the centerline on an illegal 144-phase track).
  A stripe in the other phase (r == 184) would instead take +8.
Step 2. Shift the M5 polygon by delta_x in x; y is unchanged.
Step 3. For every VIA_VIA45 instance associated with this M5 polygon, apply the
  same delta_x. This keeps V4 centered inside M5.
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

Worked example C2 (M5 polygon at x=1432-1528, 2 violations):
  M5 BEFORE x=1432-1528. r = 1432 mod 192 = 88 -- same phase as C1, so the
  same -88 snap applies.
  M5 AFTER x=1344-1440. 1344=14*96, 1440=15*96; centerline 1392 = 7*192 + 48.
  Violations at [1432,988,1528,1172] and [1432,7468,1528,7652] cleared.

Geometry preservation (Family C): M5 polygon moves as a rigid body in the final
pair. VIA45 co-moves, maintaining full overlap with M5. M4 is also reshaped
(Family B (-> see M4.md / V3.md)) to maintain overlap from below.

---

### Family D: M5 y-shift with coupled V5 shape repair (V5.M5.EN.1 / M5.S.2 / M5.W.5)

This family covers repairs where the M5 polygon is moved in y (rather than x),
requiring co-movement of VIA_VIA56 instances and subsequent independent y-resize
of V5 shapes inside those via cells to restore enclosure. The unit_gate channel
applies the rigid-body M5 move and instance co-moves; V5 shape adjustments are
then handled by the cu_pool channel in separate per-cell trials (trial i01.ug.whole_design.00,
trial i01.cu.def:VIA_VIA56_2_1_66_58.00, trial i01.cu.def:VIA_VIA56_2_2_66_58.01).

Recipe -- y-shift of M5 with VIA56 coupling:

Step 1. Move the M5 polygon rigidly by delta_y in y; x is unchanged.
Step 2. For every VIA_VIA56 instance whose V5 via overlaps this M5 polygon,
  move the instance by the same [0, delta_y]. This preserves M5/M6 connectivity
  through the via (conn_preserved confirmed in trial i01.ug.whole_design.00 for
  delta_y = +64 dbu).
Step 3. After instance co-move, inspect the V5 shapes within each displaced
  VIA_VIA56 cell. If V5.M5.EN.1 (minimum 11 nm = 44 dbu enclosure of V5 by M5
  on two opposite sides) is violated due to the y-shift, apply per-shape
  adjustments via cu_pool:
    - For shapes at the bottom end of the cell: move y by -132 dbu and resize
      (extend) by +512 dbu in y.
    - For shapes at the top end of the cell: move y by +132 dbu and resize by
      +512 dbu in y.
  These operations maintain V5 fully within the M5 enclosure window after the
  shift (trial i01.cu.def:VIA_VIA56_2_1_66_58.00 cleared 2 violations;
  trial i01.cu.def:VIA_VIA56_2_2_66_58.01 cleared 4 violations).
Step 4. The cu_pool V5 shape ops are assembled AFTER the unit_gate rigid-body
  move. The unit_gate assemble stage drops the V5 shape ops (assemble_drops
  records in trial i01.ug.whole_design.00), and cu_pool re-applies them.
  Do not bundle V5 shape resizes into the unit_gate move; treat them as a
  separate cu_pool pass.

Worked example D1 (M5 polygon p1402, instances i0234 and i0305; trial i01.ug.whole_design.00):
  M5 polygon p1402 moved +64 dbu in y.
  VIA_VIA56_2_1_66_58 instance i0234 moved [0, +64].
  VIA_VIA56_2_2_66_58 instance i0305 moved [0, +64].
  V5 shape ops for i0234 dropped at assembly; re-applied by cu_pool
  (trial i01.cu.def:VIA_VIA56_2_1_66_58.00): shape_index=0 move -132 + resize
  +512 in y; shape_index=1 move +132 + resize +512 in y. Net: -2 violations.
  V5 shape ops for i0305 dropped at assembly; re-applied by cu_pool
  (trial i01.cu.def:VIA_VIA56_2_2_66_58.01): shape_index=0 and 1 move -132 +
  resize +512 in y; shape_index=2 and 3 move +132 + resize +512 in y.
  Net: -4 violations. Combined net across all three trials: -6 violations
  (147 -> 143 total, with 4 dropped at unit_gate assembly subsequently
  recovered by cu_pool).

VIA_VIA56 cell variant note: VIA_VIA56_2_1 has 2 V5 shapes (shape_index 0 and
1); VIA_VIA56_2_2 has 4 V5 shapes (shape_index 0-3). Apply the bottom-end move
(-132) to the lower-indexed shapes and the top-end move (+132) to the upper-
indexed shapes within each cell (trial i01.cu.def:VIA_VIA56_2_2_66_58.01 shows
indices 0,1 get -132 and indices 2,3 get +132).

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
  (M4.AUX.1), height normalization to the V3 height, track parity
  (center_y mod 192 == 48, M4.AUX.2), and the coupled VIA34/VIA45 moves. No
  object add/delete was needed in either of these cases -- a property of these
  repairs, not a universal rule.

- M5 y-shifts (+64 dbu measured in trial i01.ug.whole_design.00) require
  co-movement of all VIA_VIA56 instances overlapping the moved polygon; V5
  enclosure repair is then handled separately by cu_pool per via cell. No new
  in-crop violations were introduced by the M5 y-move itself.


## Case notes (reference-design tail evidence)

M5 and M4 are tightly coupled: M5.AUX.1 drives M5 x-shift. That shift forces
VIA45 x-move. VIA45 x-move forces a top-level M4 x-extent adjustment (to keep
the MERGED M4 valid around V4). M4.AUX.1 independently forces M4 y-move. VIA45
must track both, producing combined deltas such as (-88, -48) or (-88, +120).
Compute the x and y components separately, then sum.

M5 y-shifts (Family D) couple upward to V5 via cells rather than downward to M4.
The coupling is asymmetric: the instance co-move is bundled with the M5 rigid-
body move in the unit_gate trial, but the V5 shape resizes inside those cells
are a cu_pool concern applied in subsequent trials. Both steps are required for a
complete repair (trial i01.ug.whole_design.00 plus trials
i01.cu.def:VIA_VIA56_2_1_66_58.00 and i01.cu.def:VIA_VIA56_2_2_66_58.01).