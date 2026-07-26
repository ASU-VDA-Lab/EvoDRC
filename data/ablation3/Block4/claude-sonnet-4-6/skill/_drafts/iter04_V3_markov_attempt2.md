## Per-rule recipes

### Family B: M4 on-grid reshape and V3 height matching (M4.AUX.1, V3.M4.AUX.2)

These two rules co-fired on the same M4 polygons in this block; the pairing is specific to this block and is not universal across all blocks (seed, reference-design-verified). M4.AUX.1 fires because horizontal edges (y-coordinates) are off the 24 nm (96 dbu) grid. V3.M4.AUX.2 fires because the M4 y-extent does not match the V3 via y-height. In the example block all 7 M4.AUX.1 violations and all 7 V3.M4.AUX.2 violations are cleared by reshaping the same 7 M4 polygons.

Family B in three verified facts:
1. Seven M4 polygons were reshaped or narrowed (an eighth M4 reshape at center 432 belongs to Family D (-> see M4.md), not this family).
2. Six of the seven then needed a VIA34 y-move to the new M4 center; the seventh (center 2160) was already on a legal track, so its VIA34 stayed -- but the M4 itself was STILL reshaped (y-height 184 -> 96 with the center fixed at 2160, plus x-narrowing); its VIA45 moved in x only, following M5.
3. Every repaired M4 center satisfies y mod 192 == 48: edge grid (96) AND track parity (192) are required by both M4.AUX.1 and M4.AUX.2 respectively, verified at all seven Family-B sites (seed, reference-design-verified).

Rule semantics:
- M4.AUX.1: M4 horizontal edges are required to lie on the 24 nm = 96 dbu grid; seven off-grid M4 polygons were confirmed as violations before repair and cleared after (seed, reference-design-verified).
- V3.M4.AUX.2: V3 y-extent must exactly equal M4 y-extent (both perpendicular to M4 length, which runs in x). The V3 cut's y-extent is 96 dbu = 24 nm (via-cell geometry: the cut is 72x96); the deck's V3.W.1 separately requires a minimum V3 width of 18 nm along the M4 length. After repair, M4 y-height is also 96 dbu (seed, reference-design-verified).

Recipe -- M4 reshape to on-grid height + coordinated via repositioning:

Step 1. For each off-grid M4 polygon, choose the target y for the new M4 CENTER. Two grid constraints stack:
  (1a) EDGE grid (M4.AUX.1): both new y-edges on the 96-dbu grid, so with a 96-dbu height the center is at k*96 + 48 (seed, reference-design-verified).
  (1b) TRACK grid (M4.AUX.2): the center is required to lie on a horizontal routing track; legal track centers satisfy y mod 192 == 48 -- every k*96+48 with the wrong parity (y mod 192 == 144) is an illegal track even though its edges are on the 96 grid (seed, reference-design-verified).
  Verified -- all seven Family-B sites (old center = old VIA34 y; every new center satisfies y mod 192 == 48):

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

  (An eighth M4 reshape at center 432 belongs to Family D (-> see M4.md) and also sits on a legal track.) The mod-96-only rule would have selected 1104 for the 1080-site -- an illegal ==144 track -- so 1104 is not a valid final-pair candidate. DEFAULT candidate: the NEAREST center with y mod 192 == 48; that default matches 6 of the 7 sites above. The single exception is the 1080-site, which chose 1200 (+120) over the nearest legal 1008 (-72): even among legal tracks the nearest can conflict with other geometry. Confirm with the preview and step by +/-192 to the next legal track if it fails (seed, reference-design-verified).

Step 2. Derive the edges from the chosen center:
  y_bottom_new = center_y - 48, y_top_new = center_y + 48
  (96-dbu M4 height = V3_height in ASAP7; verify V3_height against the PDK via cell before applying).

Step 3. Optionally adjust x-extent: if the VIA_VIA45 (V4, between M4 and M5) has shifted in x due to Family C (-> see M5.md) (M5 grid fix), adjust the top-level M4 x-extent so the MERGED M4 geometry (top-level polygon unioned with the via cell's own M4 land) remains valid around the shifted VIA45 -- the DRC checks merged metal, so the top-level polygon does not have to supply the enclosure alone.

Step 4. Reshape the M4 polygon to (x_left, y_bottom_new, x_right, y_top_new).

Step 5. Re-center each VIA_VIA34 instance in y to the CENTER of its own new M4 y-extent:
  new_y_VIA34 = (y_bottom_new + y_top_new) / 2.
  (Verified on all SIX VIA34 y-moves: targets 1200, 3312, 4272, 5424, 6576, 7536 -- each exactly the center of its repaired M4; the seventh Family-B site (center 2160, unchanged) needed NO VIA34 move (seed, reference-design-verified). The y-delta applied to each VIA34 is site-specific; it is NOT equal to the M4 bottom-edge shift -- in worked example B1 the bottom edge moved +164 while VIA34 moved +120 (seed, reference-design-verified). Trial i04.ug.whole_design.00 independently confirms the per-site pattern: 25 ops include 7 distinct via y-deltas (+72, -48, +24, -24, +48, -72, -48) applied individually, not a uniform batch delta across all instances.)
  VIA_VIA34 keeps its x unchanged IN THIS M5-STRIPE FLOW: it binds M3-M4 and M4 does not move in x (verified: all six stripe-site VIA34 kept x -- 1480 stayed 1480, 1864 stayed 1864 -- adjusting y only (seed, reference-design-verified)). The M5/VIA45 x-shift is not applied to VIA34 (seed, reference-design-verified). Scope note: one other VIA34 at (5652,8304) DID move +64 in x -- but as part of the Family-A column repair at x=5652 (the same +64 taken by the co-located VIA12/VIA23 instances and their associated top-level M2/M3 polygons), not as part of any stripe batch.

Step 6. Move VIA_VIA45: x ALWAYS follows the M5 stripe shift (all 7 repaired VIA45 took the same -88 dx (seed, reference-design-verified)); y moves ONLY IF the associated M4 landing's y-center changed (6 of 7 did; the (1864,2160) site kept dy=0 because its M4 center was already correct). VIA45 delta = (delta_x_from_M5, new_M4_center_y - old_via_y, which may be 0).

Worked example B1 (M4.AUX.1 + V3.M4.AUX.2 on the M4 at (1388,988,1572,1172)):
  M4 BEFORE (1388,988,1572,1172): y_bottom=988, y_top=1172.
    988 mod 96 = 28 (off-grid); 1172 mod 96 = 20 (off-grid).
    Height = 184 dbu != 96 dbu (V3 height). Both rules fire.
  M4 AFTER (1388,1152,1572,1248): y_bottom=1152=12*96, y_top=1248=13*96. On-grid.
    Height = 96 dbu = V3 height. Both rules clear.
  VIA34 repositions from y=1080 to y=1200 (delta +120 dbu = 30 nm).
  VIA45 repositions from (1480,1080) to (1392,1200): delta (-88,+120) dbu.

Worked example B2 (right-column M4 polygon at (1772,2068,1956,2252)):
  M4 BEFORE (1772,2068,1956,2252): y-height=184 dbu != 96 (V3 height), y-edges
  off-grid (2068 mod 96 = 52, 2252 mod 96 = 44) -- the rule-backed defects.
  x-width 184 is NOT itself illegal (B1's repaired M4 keeps x-width 184 in the
  0-violation final state); this site additionally narrows x for site-specific
  coverage geometry, see the note below.
  M4 AFTER (1816,2112,1912,2208): x-width=96 dbu, y-height=96 dbu.
  Note x also narrows: left x 1772->1816 (+44), right x 1956->1912 (-44). The
  top-level M4's x-center stays at 1864 -- it is NOT centered on the new VIA45
  position (x=1776 after the -88 M5 shift). Coverage of the shifted VIA45 is
  provided by the MERGED M4 geometry: the via cell's own M4 land plus this
  narrowed top-level polygon remain electrically and DRC-valid together.
  VIA34 at (1864,4320) in a neighboring segment repositions to (1864,4272).

Geometry preservation (Family B): M4 is reshaped at the same local routing site. VIA34 re-centers on the repaired M4 y-extent (centering rule, Step 5), keeping the merged M4 (top-level + via cell's own land) valid around V3 (seed, reference-design-verified).

VIA45 always follows the M5 x-shift, and additionally moves to the new M4 center in y when that center changed. The M4 x-narrowing is sized so the MERGED M4 (top-level polygon + the VIA45 cell's own M4 land) stays valid and connected around V4. At the 2160 site the shifted via's CENTER lies outside the top-level polygon -- verified: via at x=1776, top-level M4 at 1816-1912, merged overlap 1816-1868 (seed, reference-design-verified).

---

## Final-pair measured facts (reference-design tail evidence)

Provenance: these facts come from the final-pair comparison of the reference design's initial layout against its repaired final layout, plus the BEFORE and AFTER DRC reports. Every coordinate and delta cited in this document is quoted inline from that pair; the layout files themselves are not needed and are not shipped with this skill.

- M5.AUX.1 is resolved by coordinate snapping (x-shift of the stripe), with the M5.AUX.2 track parity (center_x mod 192 == 48) picking the snap direction. The M4 grid fixes are NOT mere snapping: they combine y-edge snapping (M4.AUX.1), height normalization to the V3 height, track parity (center_y mod 192 == 48, M4.AUX.2), and the coupled VIA34/VIA45 moves. No object add/delete was needed in either of these cases -- a property of these repairs, not a universal rule (seed, reference-design-verified).

## Case notes (reference-design tail evidence)

Anti-pattern AP-2 (atomic stripe batch): an M5 stripe x-shift and ALL VIA_VIA45 instances associated with that shifted stripe are applied as one complete batch -- confirmed by the final diff showing two M5 stripes shifted -88 dbu in x and all seven repaired VIA45 instances also taking dx=-88 (seed, reference-design-verified). VIA_VIA34 is NOT part of that x-batch (it keeps x and re-centers in y with the M4 reshape -- see Family B Step 5 (seed, reference-design-verified)). From a local crop, a partial stripe migration must not be submitted unless the complete VIA45 target set for that stripe is known (seed, reference-design-verified).

Trial i04.ug.whole_design.00 (Block4, whole_design, conn_preserved=true) adds corroborating evidence across layers M3, M4, M5, V3, V4: 3 polygon x-resizes and 22 via instance moves with 7 distinct y-deltas (+72, -48, +24, -24, +48, -72, -48) confirm that V3/VIA34 instances receive independent per-site centering moves, not a single uniform delta applied to all instances in the batch.