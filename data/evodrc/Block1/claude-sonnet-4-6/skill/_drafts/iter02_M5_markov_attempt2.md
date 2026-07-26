## Per-rule recipes

### Family C: M5 off-grid vertical edges (M5.AUX.1)

Rule semantics (seed, reference-design-verified): M5.AUX.1 checks that M5 vertical edges (x-coordinates) land on the 24 nm = 96 dbu grid. M5.AUX.2 (latent partner) checks that minimum-width M5 tracks have their centerline on a legal vertical routing track: center_x mod 192 == 48. The deck evaluates M5.AUX.2 only for polygons whose x-edges already sit on the 96 grid; polygons failing M5.AUX.1 are skipped, leaving the track constraint dormant. A wrong-phase mod-96 snap surfaces M5.AUX.2 as a new violation. This double-grid structure matches M4/Family B (-> see M4.md / V3.md).

Root cause pattern (seed, reference-design-verified): both changed M5 polygons (96 dbu wide = minimum width) had x_left at residual 88 both mod 96 and mod 192. Snapping by -88 puts the edges on the 96 grid AND the centerline at center_x mod 192 == 48. Snapping by +8 fixes M5.AUX.1 but lands the centerline at 144 mod 192 -- an illegal track that surfaces a dormant M5.AUX.2. Legal positions repeat every 192 dbu; the nearest candidates were -88 and +104; -88 is the smaller magnitude.

M5 x-shifts must be exact multiples of 96 dbu. Shifts of +32 or -16 dbu applied to M5 polygons p1143 and p1142 produced 12 new M5.AUX.1 violations in trial:i02.ug.leaf_0004.03 because those deltas do not satisfy (x_left + delta) mod 96 == 0 for either polygon. Any x-move of an M5 polygon that is not a multiple of 96 dbu will break the 24 nm vertical-edge grid.

Recipe -- Uniform x-shift to snap M5 to grid:

Step 1 (seed, reference-design-verified). Compute the TRACK residual r = x_left mod 192 (in dbu). For a minimum-width (96 dbu) stripe, legal positions satisfy x_left == 0 mod 192, putting both edges on the 96 grid (M5.AUX.1) and the centerline at center_x mod 192 == 48 (M5.AUX.2). The two nearest legal candidates are delta_x = -r and delta_x = +(192 - r); take the smaller magnitude. Both stripes in the seed pair had r == 88, giving delta_x = -88 (+104 is legal but larger; a plain mod-96 snap of +8 is NOT legal, landing the centerline on an illegal 144-phase track). A stripe with r == 184 takes +8.

Step 2 (seed, reference-design-verified). Shift the M5 polygon by delta_x in x; y is unchanged.

Step 3 (seed, reference-design-verified). For every VIA_VIA45 instance associated with this M5 polygon, apply the same delta_x. This keeps V4 centered inside M5.

Step 4 (seed, reference-design-verified). Because VIA45 x-position changed, check the MERGED M4 around it. If the merged M4 (top-level polygon + via cell's own M4 land) is no longer valid or connected at the new x, adjust the top-level M4 x-extent (ties to Family B (-> see M4.md / V3.md) Step 3). The top-level M4 polygon alone is not required to contain the via.

Worked example C1 (seed, reference-design-verified) (M5 polygon at x=1816-1912, 2 of the 4 M5.AUX.1 violations):
  M5 BEFORE x=1816-1912. r = 1816 mod 192 = 88; edges off the 96 grid, and the
  centerline (1864, at 136 mod 192) is also off-track but dormant while
  M5.AUX.1 fails.
  M5 AFTER x=1728-1824. 1728=18*96, 1824=19*96; centerline 1776 = 9*192 + 48.
  Delta: -88 dbu in x (nearest candidates -88/+104). M5 y unchanged.
  All VIA45 at this M5 shift by -88 in x.
  Violation [1816,1832,1912,6572] cleared (both x-edges were off-grid).
  Violation [1816,6388,1912,6572] also cleared (sub-region of same polygon).

Worked example C2 (seed, reference-design-verified) (M5 polygon at x=1432-1528, 2 violations):
  M5 BEFORE x=1432-1528. r = 1432 mod 192 = 88 -- same phase as C1, so the
  same -88 snap applies.
  M5 AFTER x=1344-1440. 1344=14*96, 1440=15*96; centerline 1392 = 7*192 + 48.
  Violations at [1432,988,1528,1172] and [1432,7468,1528,7652] cleared.

Geometry preservation, Family C (seed, reference-design-verified): M5 polygon moves as a rigid body. VIA45 co-moves, maintaining full overlap with M5. M4 is also reshaped (Family B (-> see M4.md / V3.md)) to maintain overlap from below.

---

### Family C2: M5 shape y-resize inside via cell definition

Trial trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 performed a resize_via_shape on the M5 shape in cell definition VIA_VIA45_1_2_58_58, axis y, delta_dbu -88. Touched layers: M4, M5, V4. Decision: applied; conn_preserved: true. Combined window violations fell from 295 to 243 (delta -52), split evenly as -26 in leaf_0034 and -26 in leaf_0035. The locus was [1728, 2068, 14256, 14132] in the cu_pool channel.

This operation differs from the Family C x-shift in two respects measured by trial:i01.cu.def:VIA_VIA45_1_2_58_58.01: the target is the M5 shape inside a cell definition rather than a top-level stripe, and the adjustment axis is y rather than x. A cell-definition edit propagates to all instances simultaneously, which accounts for the symmetric two-window violation reduction.

---

### Family C3: Combined M5 y-resize-end and via x-instance-move

Trial trial:i02.ug.leaf_0002.01 applied a move_instance of [-76, 0] dbu on instance i0181 together with a resize_end on M5 polygon p1154 (axis y, delta +44 dbu, end low), touching layers M4, M5, V4. The result was conn_preserved: true with n_new_in_crop=0 and n_new_out_of_crop=0 in the unit_gate channel, locus [4180,14548,4364,14732]. A resize_end on the low (bottom) edge with a positive delta shrinks the polygon's y-extent from below. An x-move of a via instance is not subject to M5.AUX.1 (which checks M5 polygon edge positions, not via instance origins); therefore delta_x=-76 on i0181 introduced no grid violation in trial:i02.ug.leaf_0002.01.

---

### V4.M5.AUX.2: via-instance drops expose enclosure failures

Rule semantics: V4.M5.AUX.2 requires V4 to exactly match M5 width in the direction perpendicular to M5 length. When an M5 polygon shifts in x but the associated V4-carrying via instances are dropped by the assembler due to inter-leaf conflict, V4 no longer aligns with M5's new position and V4.M5.AUX.2 violations result. Trial trial:i02.ug.leaf_0003.02 produced 4 new V4.M5.AUX.2 violations when M5 polygons p1143 (+32 dbu in x) and p1142 (-16 dbu in x) were moved but multiple associated instance moves were dropped as external_conflict_dropped (claimants leaf_0003 and leaf_0004), leaving V4 instances at their prior positions relative to the shifted M5 polygons.

The 26 ops dropped from trial:i02.ug.leaf_0003.02 were all x-only instance moves (deltas [32,0] and [-16,0]); the V4.M5.AUX.2 violations are a direct consequence of those drops, not of the M5 polygon moves themselves. When all associated V4 instance moves survive assembly -- as in the seed Family C examples where no conflict drops occurred -- V4.M5.AUX.2 is not triggered.

---

### M5.AUX.3: via instance moves with y-components violate M5 no-bend rule

Rule M5.AUX.3 prohibits any angle in M5 polygons. Trial trial:i02.ug.leaf_0004.03 introduced 38 new M5.AUX.3 violations. The ops included via instance moves with non-zero y-components alongside their x-components: e.g., i0345 by [32,32], i0363 by [32,72], i0344 by [32,-24], i0102 by [-16,-72]. Moving via instances with y-offsets relative to the M5 stripe to which they belong creates junctions between the via's internal M5 land and the top-level M5 stripe at a non-orthogonal join, violating M5.AUX.3. Pure x-only instance moves (delta_y == 0) that were applied in trial:i02.ug.leaf_0003.02 did not produce M5.AUX.3 violations; the 38 M5.AUX.3 violations in trial:i02.ug.leaf_0004.03 are traceable to the mixed-delta instance ops in that trial.

---

### M5.W.5: y-shrink ops must not reduce vertical width below 44 nm

Rule M5.W.5 requires a minimum vertical width of 44 nm (176 dbu). Trial trial:i02.ug.leaf_0004.03 produced 12 new M5.W.5 violations, coincident with the y-move of polygon p1561 by +32 dbu (moving the bottom edge upward by 32 dbu, shrinking the polygon's vertical extent). When a polygon is near the minimum vertical width before the repair and the low-end y-delta reduces that extent further, M5.W.5 triggers. The clean result in trial:i02.ug.leaf_0002.01 used delta +44 dbu on the low end of p1154 (also shrinking from below), but produced no M5.W.5 violation, indicating the pre-repair height of p1154 left sufficient margin. Verify remaining vertical height (height - |delta_dbu|) >= 176 dbu before applying any low-end y-shrink to an M5 polygon.

---

### Inter-leaf conflict resolution: first-wins and external_conflict_dropped

The assembler resolves competing proposals across leaf windows in two ways measured by trial:i02.ug.leaf_0003.02 and trial:i02.ug.leaf_0004.03:

- **cross_crop_first_wins**: when a polygon op (polygon_id-keyed) is claimed by two leaves and the polygon straddles their boundary, the first leaf's op is accepted; the other leaf's op for the same polygon_id is dropped as cross_crop_first_wins. In trial:i02.ug.leaf_0004.03, ops on p1143, p1142, and p1561 were accepted; the corresponding ops from leaf_0003's view were dropped.
- **external_conflict_dropped**: when two leaves propose moves on the same instance_id with different delta vectors, both are dropped (reason: external_conflict_dropped, claimants list both leaves). In trial:i02.ug.leaf_0003.02, 26 instance moves were dropped on this basis; in trial:i02.ug.leaf_0004.03, the same instances appear in the drops with the leaf_0003 delta, confirming the symmetric drop.
- **external_duplicate**: when two leaves propose the same instance move with identical delta_dbu, only one is kept; the other is dropped as external_duplicate. Duplicate-dropped ops do not generate new violations because the accepted copy still executes.

V4.M5.AUX.2 violations arise specifically from external_conflict_dropped instance moves, not from external_duplicate drops or cross_crop_first_wins polygon drops (trial:i02.ug.leaf_0003.02).

---

## Final-pair measured facts (reference-design tail evidence)

Provenance (seed, reference-design-verified): these facts come from the final-pair comparison of the reference design's initial layout against its repaired final layout, plus the BEFORE and AFTER DRC reports. Every coordinate and delta cited in this document is quoted from that pair; the layout files themselves are not needed and are not shipped with this skill.

- M5.AUX.1 is resolved by coordinate snapping (x-shift of the stripe), with M5.AUX.2 track parity (center_x mod 192 == 48) picking the snap direction (seed, reference-design-verified).
- M5 x-shifts must be multiples of 96 dbu; shifts of +32 or -16 dbu applied to M5 polygons p1143 and p1142 produced 12 new M5.AUX.1 violations (trial:i02.ug.leaf_0004.03).
- When M5 polygon x-shifts are paired with via instance x-moves, V4.M5.AUX.2 is safe; when those instance moves are conflict-dropped by the assembler, 4 V4.M5.AUX.2 violations appear (trial:i02.ug.leaf_0003.02).
- Via instance moves with non-zero y-components produce M5.AUX.3 violations: 38 new violations in trial:i02.ug.leaf_0004.03 from mixed [x,y] instance moves; pure x-only moves in trial:i02.ug.leaf_0003.02 produced no M5.AUX.3 violations.
- A y-axis shrink of M5 via resize_end (low end, +44 dbu) combined with a via x-instance-move (-76 dbu) produced zero new violations with conn_preserved true (trial:i02.ug.leaf_0002.01).
- Resizing the M5 shape inside a via cell definition on the y-axis by -88 dbu reduced violations by 52 across the cu_pool channel without breaking connectivity (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01).
- The M4 grid fixes combine y-edge snapping (M4.AUX.1), height normalization to the V3 height, track parity (center_y mod 192 == 48, M4.AUX.2), and the coupled VIA34/VIA45 moves. No object add/delete was needed in the seed pair -- a property of those repairs, not a universal rule (seed, reference-design-verified).

---

## Case notes

M5 and M4 are tightly coupled (seed, reference-design-verified): M5.AUX.1 drives M5 x-shift. That shift forces VIA45 x-move. VIA45 x-move forces a top-level M4 x-extent adjustment (to keep the MERGED M4 valid around V4). M4.AUX.1 independently forces M4 y-move. VIA45 tracks both, producing combined deltas such as (-88, -48) or (-88, +120); the x and y components are computed separately and summed.

M5 shapes inside via cell definitions are also repair targets on the y-axis: in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 a y-axis resize of -88 dbu was applied to the M5 shape in VIA_VIA45_1_2_58_58, reducing violations by 52 across the cu_pool channel without breaking connectivity.

Via instance moves with y-components must be avoided when the via is embedded in a straight M5 stripe: such moves produce M5.AUX.3 violations (trial:i02.ug.leaf_0004.03). The valid instance-move axes for VIA45 when attached to a horizontal M5 stripe are x-only (y == 0).