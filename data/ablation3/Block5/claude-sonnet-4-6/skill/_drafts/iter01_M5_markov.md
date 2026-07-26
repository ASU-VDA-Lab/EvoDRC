Now I have everything needed. Let me produce the updated knowledge body.

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
Snapping by +8 would also fix M5.AUX.1 for r=88, but lands the centerline at
144 mod 192 -- an illegal track that would surface a dormant M5.AUX.2. The
full-deck legal positions repeat every 192 dbu; the nearest candidates were -88
and +104, and -88 is the smaller. For a stripe with r=184, the nearest legal
candidate is +8, which advances x_left to 0 mod 192 and places the centerline
at 48 mod 192 -- a legal track (seed, reference-design-verified;
trial:i01.ug.whole_design.00 p910).

Recipe -- Uniform x-shift to snap M5 to grid:

Step 1. Compute the TRACK residual r = x_left mod 192 (in dbu). For a
  minimum-width (96 dbu) stripe the legal positions are x_left == 0 mod 192:
  that puts both edges on the 96 grid (M5.AUX.1) and the centerline at
  center_x mod 192 == 48 (M5.AUX.2). The two NEAREST legal candidates are
  delta_x = -r and delta_x = +(192 - r), and legality repeats every 192 dbu;
  take the smaller magnitude. For r=88: delta_x = -88 (+104 is legal but
  larger; a plain mod-96 snap of +8 is NOT legal -- it lands the centerline on
  an illegal 144-phase track). For r=184: delta_x = +8 (-184 is legal but
  larger). (seed, reference-design-verified; trial:i01.ug.whole_design.00)
Step 2. Shift the M5 polygon by delta_x in x. The x-shift alone resolves
  M5.AUX.1 and AUX.2; y is not changed by this specific fix. When other rule
  violations (e.g. vertical width or spacing) are repaired in the same pass, a
  concurrent y-end resize may be applied to the same polygon, as measured in
  trial:i01.ug.whole_design.00 (p910: +8 x-move plus +20 high-y-end resize).
  Treat the x and y components as independent corrections summed together.
Step 3. For every VIA45 instance associated with this M5 polygon, apply the
  same delta_x. This keeps V4 centered inside M5 (seed, reference-design-verified;
  trial:i01.ug.whole_design.00 i0061 and i0104 each move +8 matching p910). A
  concurrent y-resize of M5 that extends its length (high-y end) does not
  require a matching via y-move when the via remains fully within the extended
  polygon.
Step 4. Because VIA45 x-position changed, check the MERGED M4 around it. If the
  merged M4 (top-level polygon + via cell's own M4 land) is no longer valid or
  connected at the new x, adjust the top-level M4 x-extent (ties to Family B
  (-> see M4.md / V3.md) Step 3). Do not require the top-level polygon alone to
  contain the via.

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

Worked example C3 (M5 polygon p910, r=184 phase, trial:i01.ug.whole_design.00):
  r = x_left mod 192 = 184. Nearest legal candidate: delta_x = +8 (192-184).
  Op sequence on p910: move axis=x delta=+8, then resize_end axis=y delta=+20
  end=high. Associated VIA45 instances i0061 and i0104 each move [+8, 0] --
  matching the x-delta, no y-component despite the y-resize on p910.
  The y-resize extends the M5 stripe's high-y edge by 20 dbu; the vias remain
  enclosed within the lengthened polygon so no via y-move is needed.
  conn_preserved=true confirms electrical integrity was maintained.

Geometry preservation (Family C): M5 polygon shifts as a rigid body in x for
the M5.AUX.1/AUX.2 fix (seed, reference-design-verified; trial:i01.ug.whole_design.00).
VIA45 co-moves in x, maintaining full overlap with M5. A concurrent y-end resize
on M5 extends the stripe length without requiring via y-movement when the via
remains within the extended bounds (trial:i01.ug.whole_design.00). M4 is also
reshaped (Family B (-> see M4.md / V3.md)) to maintain overlap from below.

---


## Final-pair measured facts (reference-design tail evidence)

Provenance: seed facts come from the final-pair comparison of the reference
design's initial layout against its repaired final layout, plus the BEFORE and
AFTER DRC reports. Every coordinate and delta cited in this document is quoted
inline from that pair or from the named trial record.

- M5.AUX.1 is resolved by coordinate snapping (x-shift of the stripe), with the
  M5.AUX.2 track parity (center_x mod 192 == 48) picking the snap direction.
  Two measured phases: r=88 → delta=-88 (seed, reference-design-verified);
  r=184 → delta=+8 (trial:i01.ug.whole_design.00, p910).
- A concurrent y-end resize can be applied to the same M5 polygon in the same
  repair pass (trial:i01.ug.whole_design.00, p910: +20 high-y-end). The x and y
  corrections are independent; VIA co-move is required only for the x-component
  when the via remains within the extended y-bounds.
- The M4 grid fixes are NOT mere snapping: they combine y-edge snapping
  (M4.AUX.1), height normalization to the V3 height, track parity (center_y
  mod 192 == 48, M4.AUX.2), and the coupled VIA34/VIA45 moves. No object
  add/delete was needed in the reference-design pair -- a property of those
  repairs, not a universal rule. (seed, reference-design-verified)


## Case notes

M5 and M4 are tightly coupled: M5.AUX.1 drives M5 x-shift. That shift forces
VIA45 x-move. VIA45 x-move forces a top-level M4 x-extent adjustment (to keep
the MERGED M4 valid around V4). M4.AUX.1 independently forces M4 y-move. VIA45
must track both, producing combined deltas such as (-88, -48) or (-88, +120).
Compute the x and y components separately, then sum. (seed, reference-design-verified)

In multi-layer whole-design repairs (trial:i01.ug.whole_design.00, 19 ops
touching M1-M5 and V1-V4), M5 ops appear late in the op sequence after via
instance moves. The M5 x-snap and any concurrent y-resize are still independent
corrections applied to the same polygon object; the op ordering in the record
does not imply causal dependency between them.