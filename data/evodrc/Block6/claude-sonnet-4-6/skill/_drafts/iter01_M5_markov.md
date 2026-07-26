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
Step 3. For every VIA_VIA45 instance associated with this M5 polygon, the via
  cell definition itself requires internal shape edits -- not merely a rigid
  cell-instance translation. The measured pattern (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01)
  for V4 cuts within the cell is: move shape_index 0 by -116 dbu in x and
  shape_index 1 by +116 dbu in x, then resize both by +384 dbu in x; the M4
  land shape within the same cell is resized +152 dbu in x. These internal
  edits preserve V4.M5.EN.2 and V4.M5.AUX.2 at the new M5 x-position with
  conn_preserved confirmed.
Step 4. For VIA_VIA56 cells (V5 above M5) at the same M5 stripe, internal V5
  cut shapes also require edits: each of the 4 V5 shapes moves ±116 dbu in x
  (alternating -116/-116/+116/+116 pattern) and is resized +320 dbu in x
  (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02, conn_preserved confirmed). M5 and
  M6 lands are touched as part of this via cell repair.
Step 5. Because VIA45 x-position changed, check the MERGED M4 around it. If
  the merged M4 (top-level polygon + via cell's own M4 land) is no longer valid
  or connected at the new x, adjust the top-level M4 x-extent (ties to Family
  B (-> see M4.md / V3.md) Step 3). Do not require the top-level polygon alone
  to contain the via.

Worked example C1 (M5 polygon at x=1816-1912, 2 of the 4 M5.AUX.1 violations):
  M5 BEFORE x=1816-1912. r = 1816 mod 192 = 88; edges off the 96 grid, and the
  centerline (1864, at 136 mod 192) is also off-track but dormant while
  M5.AUX.1 fails.
  M5 AFTER x=1728-1824. 1728=18*96, 1824=19*96; centerline 1776 = 9*192 + 48.
  Delta: -88 dbu in x (nearest candidates -88/+104). M5 y unchanged.
  Follow-on via cell edits at locus [1728,2068,15336,15216]: VIA_VIA45_1_2_58_58
  V4 cuts moved ±116 and resized +384; M4 land resized +152 (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01).
  VIA_VIA56_2_2_66_58 V5 cuts (4 shapes) moved ±116 and resized +320
  (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02). Both applied with delta_total
  reductions of -52 and -16 violations respectively.
  Violation [1816,1832,1912,6572] cleared (both x-edges were off-grid).
  Violation [1816,6388,1912,6572] also cleared (sub-region of same polygon).

Worked example C2 (M5 polygon at x=1432-1528, 2 violations):
  M5 BEFORE x=1432-1528. r = 1432 mod 192 = 88 -- same phase as C1, so the
  same -88 snap applies.
  M5 AFTER x=1344-1440. 1344=14*96, 1440=15*96; centerline 1392 = 7*192 + 48.
  Violations at [1432,988,1528,1172] and [1432,7468,1528,7652] cleared.

Geometry preservation (Family C): M5 polygon moves as a rigid body in the snap
step. Via cells at the moved M5 stripe require internal shape edits (not just
instance translation) for both VIA_VIA45 (below M5) and VIA_VIA56 (above M5),
as confirmed by trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 and
trial:i01.cu.def:VIA_VIA56_2_2_66_58.02. M4 is also reshaped (Family B
(-> see M4.md / V3.md)) to maintain overlap from below.

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
- Via cell repairs after M5 x-shift operate on internal shape geometry within
  the via cell definition, not on cell-instance placement alone. VIA_VIA45
  internal V4 cut moves are ±116 dbu with +384 dbu resize; M4 land within the
  cell resizes +152 dbu (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01).
  VIA_VIA56 internal V5 cut moves are ±116 dbu with +320 dbu resize across
  all 4 cut shapes (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02). Both preserve
  connectivity.


## Case notes (reference-design tail evidence)

M5 and M4 are tightly coupled: M5.AUX.1 drives M5 x-shift. That shift forces
VIA45 internal shape edits (V4 cuts ±116/+384, M4 land +152 within cell).
VIA45 cell changes in turn force a top-level M4 x-extent adjustment (to keep
the MERGED M4 valid around V4). M4.AUX.1 independently forces M4 y-move.
VIA45 must track both, producing combined deltas such as (-88, -48) or
(-88, +120). Compute the x and y components separately, then sum.

M5 also couples upward: M5 x-shift forces VIA_VIA56 internal shape edits (V5
cuts ±116/+320 within cell), touching M5 and M6 lands inside the cell definition
(trial:i01.cu.def:VIA_VIA56_2_2_66_58.02). The total violation delta from these
two via-cell repair operations was -52 and -16 respectively at locus
[1728,2068,15336,15216], confirming that the via cell internal edits are a
necessary second step after the M5 polygon snap.