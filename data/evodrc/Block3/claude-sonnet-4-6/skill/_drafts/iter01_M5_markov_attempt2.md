## Per-rule recipes

### Family C: M5 off-grid vertical edges (M5.AUX.1)

Rule semantics: M5.AUX.1 requires M5 vertical edges (x-coordinates) to lie on the 24 nm = 96 dbu grid (seed). M5.AUX.2 (latent partner): minimum-width M5 tracks must ALSO have their centerline on a legal vertical routing track: center_x mod 192 == 48. The deck evaluates this check ONLY for polygons whose x-edges already sit on the 96 grid (off-grid polygons are skipped), so a stripe currently failing M5.AUX.1 reports NO M5.AUX.2 violation -- the track constraint is dormant, and a wrong-phase mod-96 snap surfaces it as a NEW violation. This is the same double-grid structure as M4 in Family B (seed).

Root cause pattern (reference-design-verified): both changed M5 polygons (96 dbu wide = minimum width) had x_left at residual 88 both mod 96 and mod 192. Snapping by -88 puts the edges on the 96 grid AND the centerline on a legal track (center_x mod 192 == 48). Snapping by +8 would also fix M5.AUX.1, but lands the centerline at 144 mod 192 -- an illegal track that surfaces a dormant M5.AUX.2. The full-deck legal positions repeat every 192 dbu; the nearest candidates were -88 and +104, and -88 is the smaller.

Recipe -- Uniform x-shift to snap M5 to grid:

Step 1. Compute the TRACK residual r = x_left mod 192 (in dbu). For a minimum-width (96 dbu) stripe the legal positions are x_left == 0 mod 192: that puts both edges on the 96 grid (M5.AUX.1) and the centerline at center_x mod 192 == 48 (M5.AUX.2). The two NEAREST legal candidates are delta_x = -r and delta_x = +(192 - r); take the smaller magnitude (reference-design-verified). In the reference pair both stripes had r == 88, so delta_x = -88 (+104 is legal but larger; a plain mod-96 snap of +8 is NOT legal -- it lands the centerline on an illegal 144-phase track). A stripe in the other phase (r == 184) would instead take +8 (reference-design-verified).

Step 2. Shift the M5 polygon by delta_x in x; y is unchanged (reference-design-verified).

Step 3. For every VIA_VIA45 instance associated with this M5 polygon, apply the same delta_x to keep V4 centered inside M5 (reference-design-verified).

Step 4. Because VIA45 x-position changed, check the MERGED M4 around it. If the merged M4 (top-level polygon + via cell's own M4 land) is no longer valid or connected at the new x, adjust the top-level M4 x-extent (ties to Family B Step 3). Containment of V4 is a property of the MERGED M4; the top-level polygon alone need not fully contain the via (reference-design-verified).

Worked example C1 (M5 polygon at x=1816-1912, 2 of the 4 M5.AUX.1 violations):
  M5 BEFORE x=1816-1912. r = 1816 mod 192 = 88; edges off the 96 grid, and the
  centerline (1864, at 136 mod 192) is also off-track but dormant while M5.AUX.1 fails.
  M5 AFTER x=1728-1824. 1728=18*96, 1824=19*96; centerline 1776 = 9*192 + 48.
  Delta: -88 dbu in x. M5 y unchanged.
  All VIA45 at this M5 shift by -88 in x.
  Violation [1816,1832,1912,6572] cleared.
  Violation [1816,6388,1912,6572] also cleared.

Worked example C2 (M5 polygon at x=1432-1528, 2 violations):
  M5 BEFORE x=1432-1528. r = 1432 mod 192 = 88 -- same phase as C1, same -88 snap.
  M5 AFTER x=1344-1440. 1344=14*96, 1440=15*96; centerline 1392 = 7*192 + 48.
  Violations at [1432,988,1528,1172] and [1432,7468,1528,7652] cleared.

Geometry preservation (reference-design-verified): M5 polygon moves as a rigid body. VIA45 co-moves, maintaining full overlap with M5. M4 is also reshaped (Family B) to maintain overlap from below.

---

### Family D: VIA_VIA45 cell-internal V4 and M4 resize (V4.M5.AUX.2 / V4.M5.EN.2)

In trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 (Block3, locus [1728,2068,11016,10892]), 18 violations were cleared by modifying the VIA_VIA45_1_2_58_58 cell definition directly rather than moving an instance. Apply a symmetric outward move pair to the two V4 shapes: shape 0 moved -116 dbu in x and resized +384 dbu in x; shape 1 moved +116 dbu in x and resized +384 dbu in x (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01). Widen the M4 shape in the same cell by +152 dbu in x (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01). Connectivity was preserved; violations fell by 18 (-10 in leaf_0018, -8 in leaf_0019).

The locus x-left of 1728 dbu in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 coincides with the post-snap M5 x-left from example C1 (1728 dbu), confirming that cell-internal V4/M4 repairs operate in the same x-band as the surrounding M5 polygon after the Family C snap; check the cell definition after any M5 x-shift to determine whether V4 coverage rules now require a cell-level resize (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01).

---

## Final-pair measured facts (reference-design tail evidence)

Provenance: these facts come from the final-pair comparison of the reference design's initial layout against its repaired final layout, plus the BEFORE and AFTER DRC reports. Every coordinate and delta cited in this document is quoted inline from that pair; the layout files themselves are not needed and are not shipped with this skill.

- M5.AUX.1 is resolved by coordinate snapping (x-shift of the stripe), with the M5.AUX.2 track parity (center_x mod 192 == 48) picking the snap direction (reference-design-verified). The M4 grid fixes combine y-edge snapping (M4.AUX.1), height normalization to the V3 height, track parity (center_y mod 192 == 48, M4.AUX.2), and the coupled VIA34/VIA45 moves. No object add/delete was needed in either of those cases (reference-design-verified).

---

## Case notes

M5 and M4 are tightly coupled (reference-design-verified): M5.AUX.1 drives M5 x-shift; that shift forces VIA45 x-move; VIA45 x-move forces a top-level M4 x-extent adjustment (to keep the MERGED M4 valid around V4); M4.AUX.1 independently forces M4 y-move. Compute the x and y correction components separately, then sum them; VIA45 must track both components, producing combined deltas such as (-88, -48) or (-88, +120) (reference-design-verified). In addition, cell-definition-level repairs to V4 shapes may be required independently of instance-level shifts, as measured in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01.