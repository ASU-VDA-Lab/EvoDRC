Writing the updated `[KNOWLEDGE]` body, folding in iteration-3 records and eliminating the rejected hypothesis token.

## Per-rule recipes

### Family B: M4 on-grid reshape and V3 height matching (M4.AUX.1, V3.M4.AUX.2)

These two rules co-fired on the same M4 polygons in this block; the pairing reflects this block's geometry, not a rule-level dependency (seed, reference-design-verified). M4.AUX.1 fires because horizontal edges (y-coordinates) are off the 24 nm (96 dbu) grid. V3.M4.AUX.2 fires because the M4 y-extent does not match the V3 via y-height. In the example block all 7 M4.AUX.1 violations and all 7 V3.M4.AUX.2 violations are cleared by reshaping the same 7 M4 polygons.

Family B in three verified facts (seed, reference-design-verified):
1. Seven M4 polygons were reshaped or narrowed (an eighth M4 reshape at center 432 belongs to Family D, not this family).
2. Six of the seven then needed a VIA34 y-move to the new M4 center; the seventh (center 2160) was already on a legal track, so its VIA34 stayed -- but the M4 itself was STILL reshaped (y-height 184 -> 96 with the center fixed at 2160, plus x-narrowing); its VIA45 moved in x only, following M5.
3. Every repaired M4 center satisfies y mod 192 == 48: edge grid (96) AND track parity (192) held at all seven sites (seed, reference-design-verified).

Rule semantics:
- M4.AUX.1: M4 horizontal edges must lie on the 24 nm = 96 dbu grid (seed, reference-design-verified).
- V3.M4.AUX.2: V3 y-extent must exactly equal M4 y-extent (both perpendicular to M4 length, which runs in x). The V3 cut's y-extent is 96 dbu = 24 nm (via-cell geometry: the cut is 72x96); the deck's V3.W.1 separately requires a minimum V3 width of 18 nm along the M4 length. After repair, M4 y-height is also 96 dbu (seed, reference-design-verified).

Recipe -- M4 reshape to on-grid height + coordinated via repositioning:

Step 1. For each off-grid M4 polygon, choose the target y for the new M4 CENTER. Two grid constraints stack (seed, reference-design-verified):
  (1a) EDGE grid (M4.AUX.1): both new y-edges on the 96-dbu grid, so with a 96-dbu height the center is at k*96 + 48;
  (1b) TRACK grid (M4.AUX.2): the center must lie on a horizontal routing track; legal track centers satisfy y mod 192 == 48 -- every k*96+48 with y mod 192 == 144 is an illegal track even though its edges are on the 96 grid (seed, reference-design-verified).
  Verified -- all seven Family-B sites (old center = old VIA34 y; every new center satisfies y mod 192 == 48) (seed, reference-design-verified):

    old center | new center | VIA34 dy | VIA45 (dx, dy)
    -----------|------------|----------|----------------
       1080    |    1200    |   +120   | (-88, +120)  <- NOT the nearest legal
       2160    |    2160    |     0    | (-88,   0)   <- center already legal;
                                                         M4 still reshaped
                                                         184->96 + x-narrowed
       3240    |    3312    |    +72   | (-88,  +72)
       4320    |    4272    |    -48   | (-88,  -48)
       5400    |    5424    |    +24   | (-88,  +24)
       6480    |    6576    |    +96   | (-88,  +96)  <- distance tie, upward
       7560    |    7536    |    -24   | (-88,  -24)

  (An eighth M4 reshape at center 432 belongs to Family D and also sits on a legal track.) The mod-96-only rule would have selected 1104 for the 1080-site -- an illegal ==144 track -- so 1104 is not a valid final-pair candidate (seed, reference-design-verified). DEFAULT candidate: the NEAREST center with y mod 192 == 48; that default matches 6 of the 7 sites above. The single exception is the 1080-site, which chose 1200 (+120) over the nearest legal 1008 (-72): even among legal tracks the nearest can conflict with other geometry (seed, reference-design-verified). Confirm with the preview and step by +/-192 to the next legal track if it fails (seed, reference-design-verified).

Step 2. Derive the edges from the chosen center (seed, reference-design-verified):
  y_bottom_new = center_y - 48, y_top_new = center_y + 48
  (96-dbu M4 height = V3_height in ASAP7; verify V3_height against the PDK via cell before applying).

Step 3. Optionally adjust x-extent: if the VIA_VIA45 (V4, between M4 and M5) has shifted in x due to an M5 grid fix, adjust the top-level M4 x-extent so the MERGED M4 geometry (top-level polygon unioned with the via cell's own M4 land) remains valid around the shifted VIA45 -- the DRC checks merged metal, so the top-level polygon does not have to supply the enclosure alone (seed, reference-design-verified).

Step 4. Reshape the M4 polygon to (x_left, y_bottom_new, x_right, y_top_new) (seed, reference-design-verified). An alternative to full reshape is a single-edge resize_end operation: move only the offending y-edge to the on-grid target position, leaving the opposite edge fixed (trial:i02.ug.leaf_0004.03). Both ops are valid; resize_end is the appropriate choice when only one horizontal edge is off-grid and the shape height after the move satisfies M4.W.1/W.2/W.3/W.4.

Step 5. Move each VIA_VIA34 instance in y to the CENTER of the new M4 y-extent: new_y_VIA34 = (y_bottom_new + y_top_new) / 2 (seed, reference-design-verified). Verified on all SIX VIA34 y-moves in the reference run: targets 1200, 3312, 4272, 5424, 6576, 7536 -- each exactly the center of its repaired M4; the seventh Family-B site (center 2160, unchanged) needed NO VIA34 move. The y-DELTA of VIA34 does NOT equal the M4 bottom-edge shift -- in worked example B1 the bottom edge moved +164 while VIA34 moved +120; only the centering formula reproduces the verified outcome (seed, reference-design-verified).
  VIA_VIA34 keeps its x unchanged in the M5-stripe flow: it binds M3-M4 and M4 does not move in x (verified: all six stripe-site VIA34 kept x -- 1480 stayed 1480, 1864 stayed 1864 -- adjusting y only) (seed, reference-design-verified). The M5/VIA45 x-shift applies to VIA45, not to VIA34 (seed, reference-design-verified). Scope note: one other VIA34 at (5652,8304) DID move +64 in x -- but as part of the Family-A column repair at x=5652, not as part of any stripe batch (seed, reference-design-verified).
  When resize_end is used instead of a full reshape, the VIA34 y-delta equals the resize_end delta_dbu value in full (not half), because the via tracks the resulting net shift of the polygon's y-center (trial:i02.ug.leaf_0004.03).

Step 6. Move VIA_VIA45: x follows the M5 stripe x-shift; y moves only when the associated M4 landing's y-center changed. VIA45 delta = (stripe_dx, new_M4_center_y - old_via_y), where the y term equals zero when the M4 center is unchanged. The stripe x-shift is design- and stripe-specific: the reference run used -88 dbu for all 7 VIA45 (seed, reference-design-verified); a distinct repair used +32 dbu (trial:i02.ug.leaf_0004.03, trial:i03.ug.leaf_0002.01). Do not treat -88 as a universal constant -- derive the x-shift from the specific M5 stripe correction being applied.

Pure-instance repair -- y-axis: When M4 polygon edges are already on-grid and the only defect is a via misplaced in y relative to the M4 center (e.g., after an earlier partial correction), the repair consists entirely of move_instance ops in y with no polygon reshape. All 6 ops in trial:i02.ug.leaf_0003.02 are move_instance in y only (three instance pairs: dy=-48, +96, +48 across touched layers M3, M4, M5, V3, V4), and produce zero new violations in crop (n_new_in_crop=0) (trial:i02.ug.leaf_0003.02).

Pure-instance repair -- x-axis: When M4 polygon edges are already on-grid and the defect requires a via repositioned in x, the repair is a single move_instance in x with no polygon reshape. In trial:i03.ug.leaf_0001.00 one instance (i0132) is moved delta_dbu=[-16,0] on a locus touching M3, M4, and V3; n_new_in_crop=1, conn_preserved=true, gated_in (trial:i03.ug.leaf_0001.00). The axis of a pure-instance via repair is determined by the direction of the misalignment: y-axis misalignment follows the y-centering rule (Step 5); x-axis misalignment is corrected by an x-only move sized to close the offset.

Worked example B1 (M4.AUX.1 + V3.M4.AUX.2 on the M4 at (1388,988,1572,1172)):
  M4 BEFORE (1388,988,1572,1172): y_bottom=988, y_top=1172.
    988 mod 96 = 28 (off-grid); 1172 mod 96 = 20 (off-grid).
    Height = 184 dbu != 96 dbu (V3 height). Both rules fire.
  M4 AFTER (1388,1152,1572,1248): y_bottom=1152=12*96, y_top=1248=13*96. On-grid.
    Height = 96 dbu = V3 height. Both rules clear.
  VIA34 repositions from y=1080 to y=1200 (delta +120 dbu = 30 nm).
  VIA45 repositions from (1480,1080) to (1392,1200): delta (-88,+120) dbu.

Worked example B2 (right-column M4 polygon at (1772,2068,1956,2252)):
  M4 BEFORE (1772,2068,1956,2252): y-height=184 dbu != 96 (V3 height), y-edges off-grid (2068 mod 96 = 52, 2252 mod 96 = 44) -- the rule-backed defects. x-width 184 is NOT itself illegal (B1's repaired M4 keeps x-width 184 in the 0-violation final state); this site additionally narrows x for site-specific coverage geometry, see the note below.
  M4 AFTER (1816,2112,1912,2208): x-width=96 dbu, y-height=96 dbu.
  Note x also narrows: left x 1772->1816 (+44), right x 1956->1912 (-44). The top-level M4's x-center stays at 1864 -- it is NOT centered on the new VIA45 position (x=1776 after the -88 M5 shift). Coverage of the shifted VIA45 is provided by the MERGED M4 geometry: the via cell's own M4 land plus this narrowed top-level polygon remain electrically and DRC-valid together.
  VIA34 at (1864,4320) in a neighboring segment repositions to (1864,4272).

Geometry preservation (Family B): M4 is reshaped at the same local routing site (seed, reference-design-verified). VIA34 re-centers on the repaired M4 y-extent (centering rule, Step 5), keeping the merged M4 (top-level + via cell's own land) valid around V3. VIA45 follows the M5 x-shift, and additionally moves to the new M4 center in y when that center changed. The M4 x-narrowing is sized so the MERGED M4 (top-level polygon + the VIA45 cell's own M4 land) stays valid and connected around V4 (seed, reference-design-verified). The shifted via's CENTER can lie outside the top-level polygon (verified at the 2160 site: via at x=1776, top-level M4 at 1816-1912, merged overlap 1816-1868) (seed, reference-design-verified).

Gating: repairs introducing n_new_in_crop > 0 are accepted (decision: gated_in) when conn_preserved is true; crop-local new violations are tolerated in exchange for preserving connectivity. Confirmed at: trial:i02.ug.leaf_0004.03 (n_new_in_crop=2, gated_in), trial:i03.ug.leaf_0001.00 (n_new_in_crop=1, gated_in), trial:i03.ug.leaf_0002.01 (n_new_in_crop=6, gated_in).

---

### Family D: M4 parallel run length (M4.S.5)

Rule semantics:
- M4.S.5: Minimum parallel run length between two M4 polygons on adjacent tracks is 44 nm = 176 dbu (seed, reference-design-verified).

Root cause: One M4 polygon had a left edge at x=3592 that was too close to the start of the parallel overlap region with a neighbor on the adjacent track, leaving < 176 dbu of parallel run. The violation marker was only 4 dbu (1 nm) wide, indicating a marginal deficiency (seed, reference-design-verified).

Recipe -- Left-edge extension + neighbor offset:

Step 1. Identify the two M4 polygons with insufficient parallel overlap.
Step 2. Extend the nearer polygon's left edge leftward by delta_extend such that the resulting parallel overlap >= 176 dbu; choose delta_extend to be the minimum needed (minimal-delta discipline) (seed, reference-design-verified).
Step 3. If the extension would violate M4-to-M4 spacing with a neighboring polygon on the same track (horizontal spacing >= 40 nm = 160 dbu, M4.S.2), move that neighbor in x (away) by a compensating delta (seed, reference-design-verified).

Worked example D1 (M4.S.5 at [3592,480,3596,576]):
  Violating M4 polygon BEFORE (3592,384,3700,480): left edge at x=3592.
  Adjacent-track partner: the M4 land (3412,576,3596,672) of a via cell instance at (3504,624) (its M4 land spans +/-92 in x, +/-48 in y around the instance origin). Parallel-run overlap BEFORE = [3592,3596] = 4 dbu.
  Same polygon AFTER (3420,384,3700,480): left edge at x=3420 (moved -172 dbu = 43 nm leftward). Overlap becomes [3420,3596] = 176 dbu -- exactly the M4.S.5 threshold (the partner's left edge 3412 lies just beyond 3420).
  Same-track neighbor (196x96 dbu at (3120,384), right edge 3316) moved to (3052,384), delta -68 dbu: the extension had cut the tip gap to 3420-3316 = 104 dbu < 160 dbu (40 nm, M4.S.2 horizontal spacing); the move restores 3420-3248 = 172 dbu (12 above the minimum; -56 would have met 160 exactly -- the reference repair kept margin here) (seed, reference-design-verified).

Geometry preservation (Family D): the extension enlarges an existing M4 shape, and the nearby M4 polygon is shifted away by -68 dbu. No via co-move appears in the final diff for this M4.S.5 repair (seed, reference-design-verified).

---

### Family E: Via cell definition geometry resize (V4 and M4 land reshape in x)

In trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, the repair target was the DEFINITION of cell VIA_VIA45_1_2_58_58, not any via instance. Five operations reshaped the cell's internal geometry in x across layers V4 and M4, clearing 18 DRC violations (delta_total -18, spanning windows leaf_0018 and leaf_0019) across locus [1728,2068,11016,10892] (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01).

Measured operations (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01):
- V4 shape_index 0: move x -116 dbu, then resize x +384 dbu.
- V4 shape_index 1: move x +116 dbu, then resize x +384 dbu.
- M4 shape_index 0: resize x +152 dbu.

The two V4 shapes moved symmetrically outward (-116 and +116 dbu) and were each enlarged +384 dbu in x. The M4 land was widened +152 dbu in x. Connectivity was preserved throughout (conn_preserved: true) (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01).

Because the repair modifies the cell definition rather than individual instances, every instance of VIA_VIA45_1_2_58_58 in the design inherits the corrected geometry from a single edit. The Family-B and Family-D repairs move or resize top-level polygon instances or via instances -- the cell-definition path is distinct and propagates globally (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01).

---

### Family F: M5 stripe x-shift (M5.AUX.1 / M4 coupling)

An M5 stripe correction moves the M5 polygon and all associated via instances (VIA45, and any other instances bound to that stripe) by a uniform x-delta. The stripe-bound instances touching M4/V4 follow. Two measured stripe x-shifts exist: -88 dbu (seed, reference-design-verified) and +32 dbu (trial:i02.ug.leaf_0004.03, trial:i03.ug.leaf_0002.01). In trial:i03.ug.leaf_0002.01 the repair is 1 M5 polygon move + 5 instance moves, all delta [+32,0], touching M4/M5/V4, producing n_new_in_crop=6, conn_preserved=true, gated_in (trial:i03.ug.leaf_0002.01). The +32 stripe shift is therefore confirmed across two independent trials on the same design state.

The stripe x-delta is stripe-specific and must be derived from the M5.AUX.2 track-center constraint (center_x mod 192 == 48) applied to the specific stripe being corrected. Do not import -88 or +32 from prior repairs without verifying the target stripe's grid offset (trial:i02.ug.leaf_0004.03, trial:i03.ug.leaf_0002.01).

---

## Final-pair measured facts (reference-design tail evidence)

Provenance: these facts come from the final-pair comparison of the reference design's initial layout against its repaired final layout, plus the BEFORE and AFTER DRC reports. Every coordinate and delta cited in this document is quoted inline from that pair; the layout files themselves are not needed and are not shipped with this skill.

- M5.AUX.1 is resolved by coordinate snapping (x-shift of the stripe), with the M5.AUX.2 track parity (center_x mod 192 == 48) picking the snap direction. The M4 grid fixes combine y-edge snapping (M4.AUX.1), height normalization to the V3 height, track parity (center_y mod 192 == 48, M4.AUX.2), and coupled VIA34/VIA45 moves. No object add/delete was needed in either of these cases -- a property of these repairs, not a universal rule (seed, reference-design-verified).


## Case notes (reference-design tail evidence)

M5 and M4 are tightly coupled: an M5 grid fix drives an M5 x-shift, which forces a VIA45 x-move, which forces a top-level M4 x-extent adjustment (to keep the MERGED M4 valid around V4). M4.AUX.1 independently forces M4 y-move. VIA45 tracks both shifts, producing combined deltas such as (-88, -48) or (-88, +120) in the reference run (seed, reference-design-verified) and (+32, +72) or (+32, -72) in trial:i02.ug.leaf_0004.03. Compute the x and y components separately, then sum (seed, reference-design-verified). The x-shift magnitude is stripe-specific: -88 and +32 are both measured values (seed, reference-design-verified, trial:i02.ug.leaf_0004.03, trial:i03.ug.leaf_0002.01).

M4.S.5 is margin-sensitive: the violation marker was 4 dbu (1 nm) wide. The fix applied a 172 dbu extension -- a 43x multiple of the apparent gap. This is because M4.S.5 checks parallel run length (the longitudinal extent of overlap between two tracks), not point spacing. Fixing a marginal parallel-run deficit requires a substantially larger metal extension than the violation marker size suggests (seed, reference-design-verified).