## Per-rule recipes

### Family B: M4 on-grid reshape and V3 height matching (M4.AUX.1, V3.M4.AUX.2)

These two rules co-fired on the same M4 polygons in this block (seed); the pairing is block-specific and is not guaranteed to recur (seed). M4.AUX.1 fires because horizontal edges (y-coordinates) are off the 24 nm (96 dbu) grid. V3.M4.AUX.2 fires because the M4 y-extent does not match the V3 via y-height. In the example block all 7 M4.AUX.1 violations and all 7 V3.M4.AUX.2 violations are cleared by reshaping the same 7 M4 polygons (seed).

Family B in three verified facts:
1. Seven M4 polygons were reshaped or narrowed (an eighth M4 reshape at center 432 belongs to Family D (-> see M4.md), not this family) (seed).
2. Six of the seven then needed a VIA34 y-move to the new M4 center; the seventh (center 2160) was already on a legal track, so its VIA34 stayed -- but the M4 itself was still reshaped (y-height 184 -> 96 with the center fixed at 2160, plus x-narrowing); its VIA45 moved in x only, following M5 (seed).
3. Every repaired M4 center satisfies y mod 192 == 48: edge grid (96) and track parity (192) both hold for all seven verified sites (seed).

Rule semantics:
- M4.AUX.1: M4 horizontal edges must lie on the 24 nm = 96 dbu grid (seed).
- V3.M4.AUX.2: V3 y-extent must exactly equal M4 y-extent, both perpendicular to M4 length (seed). The V3 cut's y-extent is 96 dbu = 24 nm (via-cell geometry: the cut is 72x96). The deck's V3.W.1 separately requires a minimum V3 width of 18 nm along the M4 length. After repair, M4 y-height is 96 dbu (seed).

Recipe -- M4 reshape to on-grid height + coordinated via repositioning:

Step 1. For each off-grid M4 polygon, choose the target y for the new M4 CENTER. Two grid constraints stack (seed):
  (1a) EDGE grid (M4.AUX.1): both new y-edges must land on the 96-dbu grid, so with a 96-dbu height the center is at k*96 + 48 (seed).
  (1b) TRACK grid (M4.AUX.2): the center must land on a legal horizontal routing track; measured track centers satisfy y mod 192 == 48 -- every k*96+48 with y mod 192 == 144 is an illegal track even though its edges are on the 96-dbu grid (seed).
  Verified -- all seven Family-B sites (old center = old VIA34 y; every new center satisfies y mod 192 == 48) (seed):

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

  (An eighth M4 reshape at center 432 belongs to Family D (-> see M4.md) and sits on a legal track (seed).) The mod-96-only rule would have selected 1104 for the 1080-site -- an illegal ==144 track -- so 1104 is not a valid final-pair candidate (seed).
  DEFAULT candidate: the nearest center with y mod 192 == 48; that default matches 6 of the 7 sites above. The 1080-site chose 1200 (+120) over the nearest legal 1008 (-72): even among legal tracks the nearest can conflict with other geometry (seed). Confirm with the preview and advance by +/-192 to the next legal track if the default conflicts (seed).

Step 2. Derive the edges from the chosen center:
  y_bottom_new = center_y - 48, y_top_new = center_y + 48
  (96-dbu M4 height = V3_height in ASAP7; verify V3_height against the PDK via cell before applying) (seed).

Step 3. Optionally adjust x-extent: if VIA_VIA45 (V4, between M4 and M5) has shifted in x due to a Family C M5 grid fix, adjust the top-level M4 x-extent so the merged M4 geometry (top-level polygon unioned with the via cell's own M4 land) stays valid around the shifted VIA45 (seed). The DRC checks merged metal, so the top-level polygon need not supply the enclosure alone (seed).

Step 4. Reshape the M4 polygon to (x_left, y_bottom_new, x_right, y_top_new) (seed).

Step 5. Move each VIA_VIA34 instance in y to the center of the new M4 y-extent (seed):
  new_y_VIA34 = (y_bottom_new + y_top_new) / 2.
  Verified on all six VIA34 y-moves: targets 1200, 3312, 4272, 5424, 6576, 7536 -- each exactly the center of its repaired M4; the seventh Family-B site (center 2160, unchanged) needed no VIA34 move (seed). The y-delta of VIA34 does not equal the M4 bottom-edge shift -- in worked example B1 the bottom edge moved +164 while VIA34 moved +120; only the centering rule reproduces the verified outcome (seed).
  VIA_VIA34 keeps its x unchanged in the M5-stripe flow: it binds M3-M4 and M4 does not move in x (verified: all six stripe-site VIA34 kept x -- 1480 stayed 1480, 1864 stayed 1864 -- adjusting y only) (seed). Apply no M5/VIA45 x-shift to VIA34 (seed). Scope note: one other VIA34 at (5652,8304) moved +64 in x -- as part of the Family-A column repair at x=5652 (the same +64 taken by the co-located VIA12/VIA23 instances and their associated top-level M2/M3 polygons), not as part of any stripe batch (seed).

Step 6. Move VIA_VIA45: x always follows the M5 stripe shift (all 7 repaired VIA45 took the same -88 dx) (seed); y moves only if the associated M4 landing's y-center changed (6 of 7 did; the (1864,2160) site kept dy=0 because its M4 center was already correct) (seed). VIA45 delta = (delta_x_from_M5, new_M4_center_y - old_via_y) where the y component is 0 when the center is unchanged (seed).

Worked example B1 (M4.AUX.1 + V3.M4.AUX.2 on the M4 at (1388,988,1572,1172)):
  M4 BEFORE (1388,988,1572,1172): y_bottom=988, y_top=1172.
    988 mod 96 = 28 (off-grid); 1172 mod 96 = 20 (off-grid).
    Height = 184 dbu != 96 dbu (V3 height). Both rules fire.
  M4 AFTER (1388,1152,1572,1248): y_bottom=1152=12*96, y_top=1248=13*96. On-grid.
    Height = 96 dbu = V3 height. Both rules clear.
  VIA34 repositions from y=1080 to y=1200 (delta +120 dbu = 30 nm).
  VIA45 repositions from (1480,1080) to (1392,1200): delta (-88,+120) dbu (seed).

Worked example B2 (right-column M4 polygon at (1772,2068,1956,2252)):
  M4 BEFORE (1772,2068,1956,2252): y-height=184 dbu != 96 (V3 height), y-edges off-grid (2068 mod 96 = 52, 2252 mod 96 = 44).
  x-width 184 is not itself illegal (B1's repaired M4 keeps x-width 184 in the 0-violation final state); this site additionally narrows x for site-specific coverage geometry (seed).
  M4 AFTER (1816,2112,1912,2208): x-width=96 dbu, y-height=96 dbu (seed).
  x also narrows: left x 1772->1816 (+44), right x 1956->1912 (-44). The top-level M4's x-center stays at 1864 -- it is not centered on the new VIA45 position (x=1776 after the -88 M5 shift). Coverage of the shifted VIA45 is provided by the merged M4 geometry: the via cell's own M4 land plus this narrowed top-level polygon remain electrically and DRC-valid together (seed).
  VIA34 at (1864,4320) in a neighboring segment repositions to (1864,4272) (seed).

Geometry preservation (Family B): M4 is reshaped at the same local routing site (seed). VIA34 re-centers on the repaired M4 y-extent (centering rule, Step 5), keeping the merged M4 (top-level + via cell's own land) valid around V3 (seed).

VIA45 always follows the M5 x-shift, and additionally moves to the new M4 center in y when that center changed (seed). The M4 x-narrowing is sized so the merged M4 (top-level polygon + the VIA45 cell's own M4 land) stays valid and connected around V4 (seed). The shifted via's center can lie outside the top-level polygon: at the 2160 site the via is at x=1776, the top-level M4 spans 1816-1912, and the merged overlap is 1816-1868 (seed).

---

## Cross-layer debt observed (iteration 1)

Trial trial:i01.ug.leaf_0012.07 (Block2, unit_gate, leaf_0012) applied four instance moves touching M3, M4, M5, V3, and V4. Connectivity was preserved (conn_preserved=true) and the trial was accepted (gated_in), yet 2 new in-crop V1.M1.EN.1 violations were introduced as debt. A repair touching V3 and M4 layers can propagate new violations to M1 enclosure rules on lower metals (trial:i01.ug.leaf_0012.07).

Via-shape resize operations (resize_via_shape) on VIA_VIA45_1_2_58_58 (V4 and M4 layers, x +152 dbu) and VIA_VIA23_1_3_36_36 (M3 layer, y -40 dbu) were proposed but dropped (assemble_drops, reason: cu_pool:applied), confirming the constraint pool tracked those adjustments as already accounted for (trial:i01.ug.leaf_0012.07). The accepted repair used only instance moves: two instances at (0,-48) in y, two at (0,+96) in y (trial:i01.ug.leaf_0012.07).

---

## Final-pair measured facts (reference-design tail evidence)

Provenance: these facts come from the final-pair comparison of the reference design's initial layout against its repaired final layout, plus the BEFORE and AFTER DRC reports. Every coordinate and delta cited in this section is quoted inline from that pair (reference-design-verified).

- M5.AUX.1 is resolved by coordinate snapping (x-shift of the stripe), with the M5.AUX.2 track parity (center_x mod 192 == 48) picking the snap direction (reference-design-verified). The M4 grid fixes are not mere snapping: they combine y-edge snapping (M4.AUX.1), height normalization to the V3 height, track parity (center_y mod 192 == 48, M4.AUX.2), and the coupled VIA34/VIA45 moves (reference-design-verified). No object add/delete was needed in either of these cases -- a property of these specific repairs, not a universal constraint (reference-design-verified).


## Case notes (reference-design tail evidence)

Anti-pattern AP-2 (atomic stripe batch): an M5 stripe x-shift and all VIA_VIA45 instances tied to that stripe must be applied as one complete batch (seed). The final diff shows two M5 stripes shifted -88 dbu in x, and all seven repaired VIA45 instances also take dx=-88 (seed). VIA_VIA34 is not part of that x-batch (it keeps x and re-centers in y with the M4 reshape -- see Family B Step 5) (seed). From a local crop, submit a stripe migration only when the complete VIA45 target set for that stripe is known (seed).