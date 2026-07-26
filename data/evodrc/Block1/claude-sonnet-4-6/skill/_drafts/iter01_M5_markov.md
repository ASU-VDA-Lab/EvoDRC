Now I have everything needed. The new record (trial `i01.cu.def:VIA_VIA45_1_2_58_58.01`) introduces a distinct repair mechanism — `resize_via_shape` on M5, axis y, within a VIA45 cell definition — not seen in the seed. I'll fold it in as a new section without contradicting any existing seed facts.

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

### Family D: M5 y-extent resize within VIA45 cell definition

A distinct repair class operates on the M5 shape stored inside the VIA45 cell
definition rather than on the top-level M5 polygon or via instance placement.
The operation type is `resize_via_shape` with axis `y`; it modifies the cell
definition directly, so every placed instance of that cell inherits the change.
Layers M4, M5, and V4 are all touched by this operation (trial
i01.cu.def:VIA_VIA45_1_2_58_58.01).

Measured record (trial i01.cu.def:VIA_VIA45_1_2_58_58.01):
- Target cell: VIA_VIA45_1_2_58_58 (cell definition, not a single instance).
- Op: resize_via_shape, layer M5, axis y, delta_dbu -88 (reduction in y-extent).
- Decision: applied. Connectivity preserved.
- Violation delta: -52 total; -26 in unit:leaf_0034 (182 -> 156), -26 in
  unit:leaf_0035 (113 -> 87). The equal reduction per leaf confirms the fix
  propagates uniformly to all instances of the modified cell definition.
- Locus [1728, 2068, 14256, 14132] spans a large bounding box consistent with
  a cell used at many placement sites across the design.

Key operational facts established by this record:

1. Cell-definition edits are the correct target when the same M5 shape
   error recurs at every instance of a VIA45 cell. Editing the definition once
   propagates to all sites and produces a uniform per-leaf violation reduction
   (trial i01.cu.def:VIA_VIA45_1_2_58_58.01).

2. A -88 dbu y-resize on M5 within VIA45 is sufficient to clear the set of
   violations flagged against this cell, with connectivity intact (trial
   i01.cu.def:VIA_VIA45_1_2_58_58.01). No additional x-move or instance
   relocation was needed for this record.

3. M4 is a touched layer in this operation even though the op descriptor names
   only M5 (trial i01.cu.def:VIA_VIA45_1_2_58_58.01). The M5 y-resize inside
   VIA45 propagates geometry constraints to M4 because the via cell bundles M4,
   M5, and V4 shapes together. After a cell-definition edit, the MERGED M4
   around each instance must be re-verified just as it is after an x-shift
   (Family C Step 4).

Recipe -- M5 y-resize in VIA45 cell definition:

Step 1. Identify that the VIA45 cell definition contains an M5 shape whose
  y-extent needs correction. The signal is a uniform violation reduction pattern
  across many leaf windows when the same cell name is the target.
Step 2. Apply `resize_via_shape` to the M5 shape in the cell definition, axis y,
  with the computed delta_dbu. The -88 dbu value established in trial
  i01.cu.def:VIA_VIA45_1_2_58_58.01 is a concrete reference point.
Step 3. After the cell definition is updated, verify all instances: check MERGED
  M4 enclosure around V4 at every placement site, since M4 is a co-touched
  layer (trial i01.cu.def:VIA_VIA45_1_2_58_58.01).
Step 4. Confirm connectivity is preserved across all instances before committing.

---


## Final-pair measured facts (reference-design tail evidence)

Provenance: these facts come from the final-pair comparison of the reference
design's initial layout against its repaired final layout, plus the BEFORE and
AFTER DRC reports, and from iteration-1 measured records. Every coordinate and
delta cited in this document is quoted inline from those sources.

- M5.AUX.1 is resolved by coordinate snapping (x-shift of the stripe), with the
  M5.AUX.2 track parity (center_x mod 192 == 48) picking the snap direction.
  The M4 grid fixes are NOT mere snapping: they combine y-edge snapping
  (M4.AUX.1), height normalization to the V3 height, track parity
  (center_y mod 192 == 48, M4.AUX.2), and the coupled VIA34/VIA45 moves. No
  object add/delete was needed in either of these cases -- a property of these
  repairs, not a universal rule.

- A `resize_via_shape` op targeting M5 within a VIA45 cell definition (axis y,
  delta -88 dbu) was applied in iteration 1 and cleared 52 violations across
  2 leaf windows with connectivity preserved (trial
  i01.cu.def:VIA_VIA45_1_2_58_58.01). This is structurally distinct from the
  Family C x-shift: it edits a cell definition rather than moving an instance,
  and it acts on the y-axis rather than x.


## Case notes

M5 and M4 are tightly coupled: M5.AUX.1 drives M5 x-shift. That shift forces
VIA45 x-move. VIA45 x-move forces a top-level M4 x-extent adjustment (to keep
the MERGED M4 valid around V4). M4.AUX.1 independently forces M4 y-move. VIA45
must track both, producing combined deltas such as (-88, -48) or (-88, +120).
Compute the x and y components separately, then sum.

Two structurally separate repair channels exist for M5/VIA45 issues: (A) the
Family C instance-level x-shift for M5.AUX.1 off-grid errors, and (B) the
Family D cell-definition y-resize for M5 shape errors shared across all
instances of a VIA45 cell. Both channels touch M4 as a co-affected layer and
require post-repair verification of the MERGED M4 at every V4 site. Select the
channel by target type: instance placement error -> Family C; shared cell
definition error -> Family D (trial i01.cu.def:VIA_VIA45_1_2_58_58.01).