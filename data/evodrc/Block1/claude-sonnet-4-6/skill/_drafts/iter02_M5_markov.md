## Per-rule recipes

### Family C: M5 off-grid vertical edges (M5.AUX.1)

Rule semantics (seed, reference-design-verified): M5.AUX.1 checks that M5 vertical edges (x-coordinates) land on the 24 nm = 96 dbu grid. M5.AUX.2 (latent partner) checks that minimum-width M5 tracks have their centerline on a legal vertical routing track: center_x mod 192 == 48. The deck evaluates M5.AUX.2 only for polygons whose x-edges already sit on the 96 grid; polygons failing M5.AUX.1 are skipped, leaving the track constraint dormant. A wrong-phase mod-96 snap surfaces M5.AUX.2 as a new violation. This double-grid structure matches M4/Family B (-> see M4.md / V3.md).

Root cause pattern (seed, reference-design-verified): both changed M5 polygons (96 dbu wide = minimum width) had x_left at residual 88 both mod 96 and mod 192. Snapping by -88 puts the edges on the 96 grid AND the centerline at center_x mod 192 == 48. Snapping by +8 fixes M5.AUX.1 but lands the centerline at 144 mod 192 -- an illegal track that surfaces a dormant M5.AUX.2. Legal positions repeat every 192 dbu; the nearest candidates were -88 and +104; -88 is the smaller magnitude.

Non-compliant x-deltas introduce new M5.AUX.1 violations: in trial:i02.ug.leaf_0004.03, polygon x-moves of +32 dbu (p1143) and -16 dbu (p1142) introduced 12 new M5.AUX.1 violations. Neither +32 nor -16 is a multiple of 96 dbu, so edges that were previously on-grid land off-grid after the move. Any M5 polygon x-move with delta_dbu not divisible by 96 will introduce M5.AUX.1 violations for every off-grid edge produced.

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

### Family C3: M5 polygon y-axis resize_end (top-level polygons)

Trial trial:i02.ug.leaf_0002.01 applied a resize_end operation to polygon p1154 on the y-axis, low end, delta_dbu +44, in the unit_gate channel, locus [4180,14548,4364,14732]. The operation was paired with a move_instance of i0181 by [-76, 0] (x-shift of an associated VIA45 instance). Touched layers: M4, M5, V4. Decision: gated_in; conn_preserved: true; n_new_in_crop: 0; n_new_out_of_crop: 0.

This establishes resize_end as a valid repair op on top-level M5 (or M4) polygons on the y-axis, distinct from the cell-definition resize_via_shape of Family C2. A low-end resize with positive delta raises the bottom edge of the polygon. The +44 dbu value does not correspond to any obvious grid multiple; the clean zero-violation outcome (trial:i02.ug.leaf_0002.01) confirms it was a fine-tuning correction within an already-legal y-range rather than a grid-snap operation.

The paired VIA45 x-move of -76 dbu in trial:i02.ug.leaf_0002.01 is a non-88 instance delta, confirming that VIA instance x-moves need not equal -88 outside the r==88 scenarios of Family C; the magnitude is determined by the local geometry of each repair site.

---

### V4.M5.AUX.2 introduction from M5 x-shifts

V4.M5.AUX.2 requires V4 to have exactly the same width as M5 perpendicular to M5's length. When M5 polygon x-moves apply non-96-aligned deltas, the M5 edge positions change while the V4 (placed inside the cell or at top level) may not shift by the same amount. Trial trial:i02.ug.leaf_0003.02 introduced 4 new V4.M5.AUX.2 violations alongside M5 polygon x-moves of +32 (p1145, p1143) and -16 (p1144, p1142). These moves broke the coincidence of V4 edges with M5 edges required by the rule. The assemble result for leaf_0003 accepted the debt (gated_in, conn_preserved: true).

To avoid introducing V4.M5.AUX.2 violations when shifting M5 polygons in x, the associated V4 instances must receive the identical x-delta, or the M5 x-move must be a multiple of 96 dbu that preserves edge coincidence.

---

### M5.AUX.3 introduction from compound-vector instance moves

M5.AUX.3 prohibits M5 from bending (no corners with angles between 0 and 90 degrees). Trial trial:i02.ug.leaf_0004.03 introduced 38 new M5.AUX.3 violations alongside instance moves that included y-components (e.g., [32,32], [32,72], [32,24], [-16,32], [-16,72], [-16,24], etc.). When a VIA45 instance is moved by a compound [dx, dy] vector, the M5 land within or above the cell shifts relative to the surrounding M5 routing, potentially creating apparent bends at the connection point between the repositioned via land and the static M5 stripe. These 38 violations were accepted as debt (gated_in, conn_preserved: true, n_new_in_crop: 47 total).

Pure x-only instance moves (dy=0) do not produce M5.AUX.3 violations by themselves when the M5 routing is horizontal-only. Compound moves with nonzero y introduce the bend risk. The Family C recipe (Step 3) specifies a pure x-shift for VIA45 co-moves, which avoids M5.AUX.3 exposure.

Trial trial:i02.ug.leaf_0004.03 also introduced 12 new M5.W.5 violations (minimum vertical width 44 nm) from the y-moves of polygon p1561 (+32 dbu) and the instance moves with y-components. A y-shift of +32 dbu is below the 44 nm = 176 dbu minimum vertical width threshold for vertical sections; the violations arise where the repositioned geometry narrows a vertical M5 segment below 176 dbu.

---

## Inter-leaf assembly conflict handling

Trials leaf_0003.02 and leaf_0004.03 (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03) operated on overlapping loci within the unit_gate channel and produced assemble_drops for shared instances and polygons. Three drop reasons were observed:

- external_conflict_dropped: both leaves claimed the same instance with different delta vectors; the conflicting leaf's op is dropped in favor of the leaf that committed first (leaf_0003 won for the i02.ug.leaf_0003.02 result; leaf_0004's conflicting ops were dropped).
- cross_crop_first_wins: a polygon (p1143, p1142, p1561) straddled both crop windows; the first-committed leaf's move was applied and the second leaf's move for the same polygon was dropped.
- external_duplicate: both leaves proposed the same [dx,dy] for the same instance (e.g., i0348 +32x, i0323 +32x); the duplicate op is silently dropped since the net effect is identical.

Drops do not prevent gated_in status if conn_preserved remains true for the surviving ops (trial:i02.ug.leaf_0003.02: 26 drops, still gated_in; trial:i02.ug.leaf_0004.03: 41 drops, still gated_in).

---

## Final-pair measured facts (reference-design tail evidence)

Provenance (seed, reference-design-verified): these facts come from the final-pair comparison of the reference design's initial layout against its repaired final layout, plus the BEFORE and AFTER DRC reports. Every coordinate and delta cited in this document is quoted from that pair; the layout files themselves are not needed and are not shipped with this skill.

- M5.AUX.1 is resolved by coordinate snapping (x-shift of the stripe), with M5.AUX.2 track parity (center_x mod 192 == 48) picking the snap direction (seed, reference-design-verified).
- The M4 grid fixes combine y-edge snapping (M4.AUX.1), height normalization to the V3 height, track parity (center_y mod 192 == 48, M4.AUX.2), and the coupled VIA34/VIA45 moves. No object add/delete was needed in the seed pair -- a property of those repairs, not a universal rule (seed, reference-design-verified).
- Resizing the M5 shape inside a via cell definition on the y-axis by -88 dbu reduced combined window violations by 52 across two leaf windows with conn_preserved true (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01).
- A resize_end op on a top-level polygon (y-axis, low end, +44 dbu) combined with a VIA45 x-move of -76 dbu produced zero new violations with conn_preserved true (trial:i02.ug.leaf_0002.01).
- M5 polygon x-moves of +32 or -16 dbu (not multiples of 96) introduced 12 new M5.AUX.1 and 4 new V4.M5.AUX.2 violations in trials trial:i02.ug.leaf_0004.03 and trial:i02.ug.leaf_0003.02 respectively; both were accepted as debt with conn_preserved true.
- Compound-vector instance moves with nonzero y-components introduced 38 new M5.AUX.3 violations and 12 new M5.W.5 violations in trial:i02.ug.leaf_0004.03; accepted as debt with conn_preserved true.

---

## Case notes

M5 and M4 are tightly coupled (seed, reference-design-verified): M5.AUX.1 drives M5 x-shift. That shift forces VIA45 x-move. VIA45 x-move forces a top-level M4 x-extent adjustment (to keep the MERGED M4 valid around V4). M4.AUX.1 independently forces M4 y-move. VIA45 tracks both, producing combined deltas such as (-88, -48) or (-88, +120); the x and y components are computed separately and summed.

M5 shapes inside via cell definitions are also repair targets on the y-axis: in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 a y-axis resize of -88 dbu was applied to the M5 shape in VIA_VIA45_1_2_58_58, reducing violations by 52 across the cu_pool channel without breaking connectivity.

Top-level M5 polygon y-extent is also adjustable via resize_end: trial:i02.ug.leaf_0002.01 confirms a low-end y-resize of +44 dbu on a top-level polygon produces no new violations when the associated VIA45 instance x-move is correctly paired.

The gated_in + conn_preserved + n_new_in_crop > 0 outcome is a valid assembler state: violations introduced within the crop that do not break connectivity are accepted as repair debt to be resolved in subsequent iterations. Trials trial:i02.ug.leaf_0003.02 (80 new in-crop) and trial:i02.ug.leaf_0004.03 (47 new in-crop) both reached this state with multi-layer edits spanning M2 through M6 and V2 through V5.