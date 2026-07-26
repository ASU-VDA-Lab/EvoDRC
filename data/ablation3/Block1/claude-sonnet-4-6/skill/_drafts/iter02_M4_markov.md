## Per-rule recipes

### Family B: M4 on-grid reshape and V3 height matching (M4.AUX.1, V3.M4.AUX.2)

These two rules co-fired on the same M4 polygons in this block; the pairing is specific to this block's geometry and is not universal (seed, reference-design-verified). M4.AUX.1 fires because horizontal edges (y-coordinates) are off the 24 nm (96 dbu) grid. V3.M4.AUX.2 fires because the M4 y-extent does not match the V3 via y-height. In the example block all 7 M4.AUX.1 violations and all 7 V3.M4.AUX.2 violations are cleared by reshaping the same 7 M4 polygons (seed, reference-design-verified).

Family B in three verified facts:
1. Seven M4 polygons were reshaped or narrowed; an eighth M4 reshape at center 432 belongs to Family D, not this family (seed, reference-design-verified).
2. Six of the seven then needed a VIA34 y-move to the new M4 center; the seventh (center 2160) was already on a legal track, so its VIA34 stayed -- but the M4 itself was STILL reshaped (y-height 184->96 with the center fixed at 2160, plus x-narrowing); its VIA45 moved in x only, following M5 (seed, reference-design-verified).
3. Every repaired M4 center satisfies y mod 192 == 48: edge grid (96) AND track parity (192) both hold at each site (seed, reference-design-verified).

Rule semantics:
- M4.AUX.1: M4 horizontal edges are verified on the 24 nm = 96 dbu grid; the seven Family-B polygons each had at least one horizontal edge off this grid before repair and both edges on-grid after repair (seed, reference-design-verified).
- V3.M4.AUX.2: V3 y-extent equals M4 y-extent (both perpendicular to M4 length, which runs in x). The V3 cut's y-extent is 96 dbu = 24 nm (via-cell geometry: the cut is 72x96); the deck's V3.W.1 separately requires a minimum V3 width of 18 nm along the M4 length. After repair, M4 y-height is 96 dbu, matching V3 height (seed, reference-design-verified).

Recipe -- M4 reshape to on-grid height + coordinated via repositioning:

Step 1. For each off-grid M4 polygon, choose the target y for the new M4 CENTER. Two grid constraints stack, both verified across all seven Family-B sites (seed, reference-design-verified):
  (1a) EDGE grid (M4.AUX.1): both new y-edges on the 96-dbu grid; with a 96-dbu height the center falls at k\*96 + 48.
  (1b) TRACK grid (M4.AUX.2): legal track centers satisfy y mod 192 == 48. A center with y mod 192 == 144 is an illegal track even when its edges are on the 96-dbu grid, and is not a valid final target (seed, reference-design-verified).
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

  (The eighth M4 reshape at center 432 belongs to Family D and sits on a legal track (seed, reference-design-verified).) The mod-96-only rule would have selected 1104 for the 1080-site -- a y mod 192 == 144 track -- so 1104 is not a valid candidate. DEFAULT candidate: the NEAREST center with y mod 192 == 48; that default matches 6 of the 7 sites (seed, reference-design-verified). The 1080-site chose 1200 (+120) over the nearest legal 1008 (-72): even among legal tracks the nearest can conflict with other geometry. Confirm with the preview and step by +/-192 to the next legal track if the first choice fails.

Step 2. Derive the edges from the chosen center (seed, reference-design-verified):
  y\_bottom\_new = center\_y - 48, y\_top\_new = center\_y + 48.
  (96-dbu M4 height = V3\_height in ASAP7; verify V3\_height against the PDK via cell before applying.)

Step 3. Optionally adjust x-extent: if VIA_VIA45 (V4, between M4 and M5) has shifted in x due to the M5 grid fix, adjust the top-level M4 x-extent so the MERGED M4 geometry (top-level polygon unioned with the via cell's own M4 land) remains valid around the shifted VIA45 (seed, reference-design-verified). The DRC checks merged metal; the top-level polygon alone is not required to supply the enclosure, as verified at the 2160-site where the shifted via center (x=1776) lies outside the top-level polygon (1816-1912) yet the merged overlap (1816-1868) satisfies enclosure (seed, reference-design-verified).

Step 4. Reshape the M4 polygon to (x\_left, y\_bottom\_new, x\_right, y\_top\_new) (seed, reference-design-verified).

Step 5. Reposition each VIA_VIA34 instance in y to the CENTER of the new M4 y-extent: new\_y\_VIA34 = (y\_bottom\_new + y\_top\_new) / 2 (seed, reference-design-verified). Verified on all six VIA34 y-moves: targets 1200, 3312, 4272, 5424, 6576, 7536 -- each exactly the center of its repaired M4; the seventh Family-B site (center 2160, unchanged) needed no VIA34 move (seed, reference-design-verified). The y-DELTA of VIA34 is NOT equal to the M4 bottom-edge shift: in worked example B1 the bottom edge moved +164 while VIA34 moved +120; the centering formula new\_y = (y\_bottom\_new + y\_top\_new) / 2 is the verified outcome (seed, reference-design-verified).

  VIA_VIA34 keeps its x unchanged in the M5-stripe flow; all six stripe-site VIA34 instances adjusted y only (1480 stayed 1480, 1864 stayed 1864) (seed, reference-design-verified). One VIA34 at (5652,8304) moved +64 in x as part of the Family-A column repair (the same +64 taken by co-located VIA12/VIA23 instances and their associated top-level M2/M3 polygons), not as part of any stripe batch (seed, reference-design-verified). VIA34 and VIA45 have independent repair deltas: VIA34 x is held fixed in the stripe flow while VIA45 x follows the M5 shift; the two y-deltas are both derived from the new M4 center but from different starting y positions (seed, reference-design-verified).

Step 6. Reposition VIA_VIA45: x follows the M5 stripe shift -- all 7 repaired VIA45 took the same -88 dx (seed, reference-design-verified). y changes only when the associated M4 landing's y-center changed -- 6 of 7 sites had y change; the (1864,2160) site kept dy=0 because its M4 center was already at a legal track (seed, reference-design-verified). VIA45 delta = (delta\_x\_from\_M5, new\_M4\_center\_y - old\_via\_y), where the y component equals 0 when the M4 center is unchanged (seed, reference-design-verified).

In iteration 1, resizing the M5-layer shape of VIA_VIA45_1_2_58_58 by -88 dbu in y (touching layers M4, M5, V4) reduced DRC violations by 52 (244→192) (trial:i01.cu.def:VIA_VIA45_1_2_58_58.00). This resize_via_shape operation on the M5 layer in the y axis is a verified repair mechanism for VIA45-coupled violations at this via cell.

Worked example B1 (M4.AUX.1 + V3.M4.AUX.2 on the M4 at (1388,988,1572,1172)) (seed, reference-design-verified):
  M4 BEFORE (1388,988,1572,1172): y\_bottom=988, y\_top=1172.
    988 mod 96 = 28 (off-grid); 1172 mod 96 = 20 (off-grid).
    Height = 184 dbu != 96 dbu (V3 height). Both rules fire.
  M4 AFTER (1388,1152,1572,1248): y\_bottom=1152=12\*96, y\_top=1248=13\*96. On-grid.
    Height = 96 dbu = V3 height. Both rules clear.
  VIA34 repositions from y=1080 to y=1200 (delta +120 dbu = 30 nm).
  VIA45 repositions from (1480,1080) to (1392,1200): delta (-88,+120) dbu.

Worked example B2 (right-column M4 polygon at (1772,2068,1956,2252)) (seed, reference-design-verified):
  M4 BEFORE (1772,2068,1956,2252): y-height=184 dbu != 96 (V3 height), y-edges
  off-grid (2068 mod 96 = 52, 2252 mod 96 = 44).
  x-width 184 is not itself illegal (B1's repaired M4 keeps x-width 184 in the
  0-violation final state); this site additionally narrows x for site-specific
  coverage geometry.
  M4 AFTER (1816,2112,1912,2208): x-width=96 dbu, y-height=96 dbu.
  Note x also narrows: left x 1772->1816 (+44), right x 1956->1912 (-44). The
  top-level M4's x-center stays at 1864 -- not centered on the new VIA45
  position (x=1776 after the -88 M5 shift). Coverage of the shifted VIA45 is
  provided by the MERGED M4 geometry: the via cell's own M4 land plus this
  narrowed top-level polygon remain electrically and DRC-valid together.
  VIA34 at (1864,4320) in a neighboring segment repositions to (1864,4272).

Geometry preservation (Family B): M4 is reshaped at the same local routing site. VIA34 re-centers on the repaired M4 y-extent (centering rule, Step 5), keeping the merged M4 (top-level + via cell's own land) valid around V3 (seed, reference-design-verified). VIA45 follows the M5 x-shift and additionally moves to the new M4 center in y when that center changed. The M4 x-narrowing is sized so the MERGED M4 (top-level polygon + the VIA45 cell's own M4 land) stays valid and connected around V4; the shifted via center can lie outside the top-level polygon -- verified at the 2160 site: via at x=1776, top-level M4 at 1816-1912, merged overlap 1816-1868 (seed, reference-design-verified).

---

### Family D: M4 parallel run length (M4.S.5)

Rule semantics:
- M4.S.5: Minimum parallel run length between two M4 polygons on adjacent tracks is 44 nm = 176 dbu; verified at the D1 site before and after repair (seed, reference-design-verified).

Root cause: One M4 polygon had a left edge at x=3592 that left < 176 dbu of parallel run with a neighbor on the adjacent track. The violation marker was 4 dbu (1 nm) wide, indicating a marginal deficiency (seed, reference-design-verified).

Recipe -- Left-edge extension + neighbor offset (seed, reference-design-verified):

Step 1. Identify the two M4 polygons with insufficient parallel overlap.
Step 2. Extend the nearer polygon's left edge leftward by delta\_extend such that the resulting parallel overlap >= 176 dbu. Minimal-delta discipline: choose the smallest delta\_extend that meets threshold.
Step 3. If the extension reduces the same-track gap to a neighboring polygon below 160 dbu (40 nm, M4.S.2), shift that neighbor in x (away) by a compensating delta.

Worked example D1 (M4.S.5 at [3592,480,3596,576]) (seed, reference-design-verified):
  Violating M4 polygon BEFORE (3592,384,3700,480): left edge at x=3592.
  Adjacent-track partner: the M4 land (3412,576,3596,672) of a via cell instance at (3504,624) (its M4 land spans +/-92 in x, +/-48 in y around the instance origin). Parallel-run overlap BEFORE = [3592,3596] = 4 dbu.
  Same polygon AFTER (3420,384,3700,480): left edge at x=3420 (moved -172 dbu = 43 nm leftward). Overlap becomes [3420,3596] = 176 dbu -- exactly the M4.S.5 threshold.
  Same-track neighbor (196x96 dbu at (3120,384), right edge 3316) moved to (3052,384), delta -68 dbu: the extension had cut the tip gap to 3420-3316 = 104 dbu < 160 dbu (40 nm, M4.S.2 horizontal spacing); the move restores 3420-3248 = 172 dbu (12 above the minimum; -56 would have met 160 exactly -- the reference repair kept margin here).

Geometry preservation (Family D): the extension enlarges an existing M4 shape, and the nearby M4 polygon is shifted away by -68 dbu. No via co-move appears in the final diff for this M4.S.5 repair (seed, reference-design-verified).

---

### Family E: Fine-grained M4 x/y adjustments in whole-design repair (iteration 2)

In the iteration 2 whole-design repair (trial:i02.ug.whole_design.00), M4 polygons received small x-moves of -16 dbu and +32 dbu (two distinct x-column offsets) and small y-moves of +32, +16, and -64 dbu. These magnitudes are distinct from both the large y-relocations in Family B (up to 120 dbu, driven by M4.AUX.1/V3.M4.AUX.2) and the large x-extensions in Family D (172 dbu, driven by M4.S.5). The -16/+32 x-delta pattern and the +32/+16/-64 y-delta pattern therefore constitute a separate finer-grained adjustment class (trial:i02.ug.whole_design.00).

The 57-op repair touched M3, M4, M5, M6, V3, V4, V5 simultaneously, with the majority of ops being instance moves (via cell repositions) carrying mixed x/y components. The x-component of instance moves grouped into three classes: -16 dbu, +32 dbu, and 0 dbu, matching the top-level M4 polygon x-adjustments. The y-components of instance moves ranged across -72, -64, -48, -24, 0, +16, +24, +32, +48, +72, +96 dbu and do not form a single uniform family (trial:i02.ug.whole_design.00).

This repair was accepted (gated_in) on connectivity preservation despite introducing 48 new V1.M2.AUX.2 in-crop violations. A whole-design M4 repair that touches V3/V4/V5 via cells can propagate geometric stress downward into the M1-M3 stack and create secondary lower-metal violations; those secondary violations may be accepted as debt when connectivity is preserved (trial:i02.ug.whole_design.00).

---

## Final-pair measured facts (reference-design tail evidence)

Provenance: these facts come from the final-pair comparison of the reference design's initial layout against its repaired final layout, plus the BEFORE and AFTER DRC reports. Every coordinate and delta cited in this document is quoted from that pair (seed, reference-design-verified).

- M5.AUX.1 is resolved by coordinate snapping (x-shift of the stripe), with M5.AUX.2 track parity (center\_x mod 192 == 48) picking the snap direction (seed, reference-design-verified).
- The M4 grid fixes combine y-edge snapping (M4.AUX.1), height normalization to the V3 height, track parity (center\_y mod 192 == 48, M4.AUX.2), and the coupled VIA34/VIA45 moves. No object add/delete was needed in either of these cases -- a property of these repairs, not a universal rule (seed, reference-design-verified).
- In iteration 1, resizing VIA_VIA45_1_2_58_58's M5-layer shape by -88 dbu in y (touching M4, M5, V4) reduced DRC count by 52 (244→192) (trial:i01.cu.def:VIA_VIA45_1_2_58_58.00).
- In iteration 2, a 57-op whole-design repair on the unit_gate channel adjusted M4 polygons by -16 and +32 dbu in x and by +32, +16, -64 dbu in y, while repositioning via instances across M3-M6; the repair was gated_in with 48 new V1.M2.AUX.2 violations accepted as connectivity-preserved debt (trial:i02.ug.whole_design.00).

---

## Case notes (reference-design tail evidence)

M5 and M4 are tightly coupled (seed, reference-design-verified): M5.AUX.1 drives M5 x-shift; that shift forces VIA45 x-move; VIA45 x-move forces a top-level M4 x-extent adjustment (to keep the MERGED M4 valid around V4); M4.AUX.1 independently forces M4 y-move; VIA45 accumulates both components, producing combined deltas such as (-88, -48) or (-88, +120) -- the x component follows M5 and the y component follows the M4 center change; these are computed separately and summed (seed, reference-design-verified).

M4.S.5 is margin-sensitive: the violation marker was 4 dbu (1 nm) wide and the fix applied a 172 dbu extension -- a 43x multiple of the apparent gap (seed, reference-design-verified). M4.S.5 checks parallel run length (the longitudinal extent of overlap between two tracks), not point spacing; fixing a marginal parallel-run deficit requires a substantially larger metal extension than the violation marker size suggests (seed, reference-design-verified).

Whole-design M4 repairs can create secondary lower-metal violations: in trial:i02.ug.whole_design.00 the repair introduced 48 new V1.M2.AUX.2 violations while clearing M4-layer violations; these were accepted as debt on the basis of connectivity preservation. When evaluating repair candidates that touch both M4 and via stacks (V3, V4, V5), check for downstream M1-M3 rule interactions before declaring the repair clean (trial:i02.ug.whole_design.00).