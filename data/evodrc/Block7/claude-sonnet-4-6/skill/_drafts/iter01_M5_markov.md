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

### Family D: VIA_VIA45 via-cell internal repair (V4/M5 shape adjustment)

This family covers cases where the via cell VIA_VIA45_1_2_58_58 itself
requires internal geometry corrections at locus [1728,2068,28728,28172], as
distinct from the whole-instance x-shift in Family C.

**Winning strategy (trial:i01.cu.def:VIA_VIA45_1_2_58_58.00, applied, delta_total=-156):**
Expand V4 in x on both sub-shapes, combined with an x-resize of M5 within the
via cell:

- V4 shape 0: move x by -116 dbu, then resize x by +232 dbu (net: left edge
  shifts -116, right edge shifts +116 relative to original).
- V4 shape 1: move x by +116 dbu, then resize x by +232 dbu (net: left edge
  shifts +116, right edge shifts +116... wait, symmetric expansion toward each
  other's outside edges).
- M5 shape 0 (within via cell): resize x by -152 dbu (shrink).

All five ops touch only M4, M5, V4 within the cell; conn_preserved=true
(trial:i01.cu.def:VIA_VIA45_1_2_58_58.00). This pattern resolves V4 enclosure
and width-match violations (V4.M5.EN.2, V4.M5.AUX.2) that arise from the
via-cell geometry at this locus.

**Losing strategy (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, lost_tournament, delta_total=-156):**
A single y-resize of M5 by -88 dbu within VIA_VIA45_1_2_58_58 achieves the
same violation count reduction (delta_total=-156) but lost the tournament
(trial:i01.cu.def:VIA_VIA45_1_2_58_58.01). Do not use a y-only M5 shrink as the
sole repair for this via cell; it produces equal violation reduction but is
dominated by the V4 x-expand + M5 x-resize approach, implying it introduces
secondary violations (e.g. M5.W.5 minimum vertical width, or M5.S.2/M5.S.4
vertical spacing) that the tournament scorer penalizes.

**Rule:** For VIA_VIA45_1_2_58_58 via-cell repairs, always prefer expanding V4
in x (paired move+resize on each V4 sub-shape) combined with x-resizing M5,
over any y-only resize of M5 (trial:i01.cu.def:VIA_VIA45_1_2_58_58.00 vs
trial:i01.cu.def:VIA_VIA45_1_2_58_58.01).

---

### Family E: VIA_VIA56 y-adjustment touching M5 (V5/M5/M6 via cell)

Trial trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 (applied, delta_total=-80) repairs
VIA_VIA56_2_2_66_58 by moving and resizing all four V5 sub-shapes in y
(each: move by ±132 dbu, resize by +512 dbu). M5 appears in touched_layers but
no M5 operations are emitted (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02). M5 is
affected passively through the via cell's layer stack but requires no direct
shape editing in this repair pattern. Do not inject M5 shape edits when
repairing V5 y-enclosure issues in VIA_VIA56_2_2_66_58; the V5-only adjustment
is sufficient and conn_preserved=true confirms it maintains M5 connectivity.

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
- VIA_VIA45_1_2_58_58 internal repair at locus [1728,2068,28728,28172] requires
  expanding V4 in x across both sub-shapes and shrinking M5 in x within the via
  cell (trial:i01.cu.def:VIA_VIA45_1_2_58_58.00). A y-only M5 shrink achieves
  the same raw violation delta but loses the tournament
  (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01).
- VIA_VIA56_2_2_66_58 V5 y-adjustments list M5 as a touched layer but emit zero
  M5 ops; M5 requires no direct edits in this repair
  (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02).

## Case notes (reference-design tail evidence)

M5 and M4 are tightly coupled: M5.AUX.1 drives M5 x-shift. That shift forces
VIA45 x-move. VIA45 x-move forces a top-level M4 x-extent adjustment (to keep
the MERGED M4 valid around V4). M4.AUX.1 independently forces M4 y-move. VIA45
must track both, producing combined deltas such as (-88, -48) or (-88, +120).
Compute the x and y components separately, then sum.

Within-cell VIA_VIA45 repairs (Family D) are distinct from whole-instance
shifts (Family C): the former modify V4 and M5 geometry inside the cell
definition; the latter translate the entire instance in x to satisfy M5.AUX.1
and M5.AUX.2. Both can be necessary in the same design region and must be
applied independently.