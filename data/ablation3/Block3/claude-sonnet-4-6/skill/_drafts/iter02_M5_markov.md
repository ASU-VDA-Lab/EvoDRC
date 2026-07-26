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
  A stripe in the other phase (r == 184) would instead take +8. A stripe with
  r == 160 takes delta_x = +32 (the alternative -160 is larger in magnitude)
  as confirmed by trial:i02.ug.whole_design.00.
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

Worked example C3 (M5 polygons p1059 and p1060, iteration 2, positive delta):
  Both polygons had r = x_left mod 192 = 160. Nearest candidates: -(160) = -160
  or +(192-160) = +32; the +32 candidate is smaller in magnitude. Applied
  delta_x = +32 dbu to both polygons (trial:i02.ug.whole_design.00). Nine VIA
  instances co-moved +32 in x with independent y adjustments (e.g., i0173
  [+32,+72], i0078 [+32,+48], i0163 [+32,0]). Result: conn_preserved=true,
  no new in-crop violations, no new out-of-crop violations, gated_in.
  This confirms positive deltas are valid when they are the smaller-magnitude
  path to a legal (mod 192 == 0) position.

Geometry preservation (Family C): M5 polygon moves as a rigid body in the final
pair. VIA45 co-moves, maintaining full overlap with M5. M4 is also reshaped
(Family B (-> see M4.md / V3.md)) to maintain overlap from below.

### Cell-definition shape modifications are not effective

Attempting to resize or translate V4 or M4 shapes directly inside the
VIA_VIA45 cell *definition* (ops: move_via_shape, resize_via_shape on
cell_name VIA_VIA45_1_2_58_58) did not reduce violations and was rejected
as cu_pool:rejected_net_positive (trial:i02.cu.def:VIA_VIA45_1_2_58_58.00).
The correct repair mechanism is instance-level moves (move_instance ops on
the VIA45 placement instances), not cell-definition edits. Do not attempt to
fix V4.M5.EN.2 or V4.M5.AUX.2 by resizing the via cut or M4 land inside the
cell definition.

### Y-only VIA instance moves in multi-polygon repair

When a whole-design trial repairs multiple M5 polygons in one pass, some VIA
instances that are NOT associated with the x-shifted M5 polygons receive y-only
moves (delta_x = 0, delta_y != 0). In trial:i02.ug.whole_design.00, seven
instances (e.g., i0151 [0,+72], i0096 [0,-24], i0088 [0,-72]) moved only in y
while nine others co-moved in x. These y-only moves correspond to M4/V3 grid
fixes (Family B) on tracks that were already correctly positioned in x.
Compute x and y correction components independently and sum; the same trial can
mix x+y and y-only instance moves.

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
  (M4.AUX.1), height
  normalization to the V3 height, track parity (center_y mod 192 == 48,
  M4.AUX.2), and the coupled VIA34/VIA45 moves. No object add/delete was needed
  in either of these cases -- a property of these repairs, not a universal
  rule.

- Positive x deltas (+32, confirmed trial:i02.ug.whole_design.00) and negative
  x deltas (-88, seed) are both valid snap directions; direction is determined
  solely by which candidate has smaller magnitude among {-r, +(192-r)}.

- Resizing or moving via-cut or M4-land shapes inside a VIA_VIA45 cell
  definition does not reduce DRC violations (trial:i02.cu.def:VIA_VIA45_1_2_58_58.00).
  Only instance-level placement moves are effective.


## Case notes (reference-design tail evidence)

M5 and M4 are tightly coupled: M5.AUX.1 drives M5 x-shift. That shift forces
VIA45 x-move. VIA45 x-move forces a top-level M4 x-extent adjustment (to keep
the MERGED M4 valid around V4). M4.AUX.1 independently forces M4 y-move. VIA45
must track both, producing combined deltas such as (-88, -48) or (-88, +120)
or (+32, +72). Compute the x and y components separately, then sum.