## Per-rule recipes

### Family B: M4 on-grid reshape and V3 height matching (M4.AUX.1, V3.M4.AUX.2)

These two rules co-fired on the same M4 polygons in this block; the co-firing is a property of this block's geometry, not a universal constraint of the rules (seed, reference-design-verified). M4.AUX.1 fires because horizontal edges (y-coordinates) are off the 24 nm (96 dbu) grid. V3.M4.AUX.2 fires because the M4 y-extent does not match the V3 via y-height. In the example block all 7 M4.AUX.1 violations and all 7 V3.M4.AUX.2 violations are cleared by reshaping the same 7 M4 polygons (seed, reference-design-verified).

Family B in three verified facts:
1. Seven M4 polygons were reshaped or narrowed (an eighth M4 reshape at center 432 belongs to Family D, not this family) (seed, reference-design-verified).
2. Six of the seven then needed a VIA34 y-move to the new M4 center; the seventh (center 2160) was already on a legal track, so its VIA34 stayed -- but the M4 itself was STILL reshaped (y-height 184 -> 96 with the center fixed at 2160, plus x-narrowing); its VIA45 moved in x only, following M5 (seed, reference-design-verified).
3. Every repaired M4 center satisfies y mod 192 == 48: the 96-dbu edge-grid constraint and the 192-dbu track-parity constraint both apply and both hold in all seven measured repairs (seed, reference-design-verified).

Rule semantics:
- M4.AUX.1: M4 horizontal edges must lie on the 24 nm = 96 dbu grid. All seven pre-repair M4 polygons had off-grid y-edges; all seven post-repair polygons have on-grid y-edges (seed, reference-design-verified).
- V3.M4.AUX.2: V3 y-extent must exactly equal M4 y-extent. The V3 cut's y-extent is 96 dbu = 24 nm (via-cell geometry: the cut is 72x96). After repair, M4 y-height is also 96 dbu, matching V3 (seed, reference-design-verified).

Recipe -- M4 reshape to on-grid height + coordinated via repositioning:

Step 1. For each off-grid M4 polygon, choose the target y for the new M4 CENTER. Two grid constraints stack, and both must hold (seed, reference-design-verified):
  (1a) EDGE grid: both new y-edges on the 96-dbu grid. With a 96-dbu height the center lies at k*96 + 48 (seed, reference-design-verified).
  (1b) TRACK grid: legal track centers satisfy y mod 192 == 48. Every k*96+48 with y mod 192 == 144 is an illegal track even though its edges are on the 96-dbu grid (seed, reference-design-verified).
  All seven Family-B repaired centers satisfy y mod 192 == 48 (seed, reference-design-verified):

    old center | new center | VIA34 dy | VIA45 (dx, dy)
    -----------|------------|----------|----------------
       1080    |    1200    |   +120   | (-88, +120)
       2160    |    2160    |     0    | (-88,   0)
       3240    |    3312    |    +72   | (-88,  +72)
       4320    |    4272    |    -48   | (-88,  -48)
       5400    |    5424    |    +24   | (-88,  +24)
       6480    |    6576    |    +96   | (-88,  +96)
       7560    |    7536    |    -24   | (-88,  -24)

  An eighth M4 reshape at center 432 belongs to Family D and sits on a legal track (seed, reference-design-verified). The mod-96-only rule would select 1104 for the 1080-site -- 1104 mod 192 == 144, an illegal track -- so 1104 is not a valid candidate. The DEFAULT candidate is the nearest center with y mod 192 == 48; that default matches 6 of the 7 sites. The 1080-site chose 1200 (+120) over the nearest legal 1008 (-72) because the nearest legal track conflicted with existing geometry. Confirm with the layout preview and step by +/-192 to the next legal track if the nearest legal candidate fails (seed, reference-design-verified).

Step 2. Derive the new edges from the chosen center (seed, reference-design-verified):
  y_bottom_new = center_y - 48, y_top_new = center_y + 48.
  (96-dbu M4 height = V3_height in ASAP7; verify V3_height against the PDK via cell before applying.)

Step 3. Adjust x-extent if VIA_VIA45 has shifted in x due to the M5 grid fix: resize the top-level M4 x-extent so the MERGED M4 geometry (top-level polygon unioned with the via cell's own M4 land) remains valid around the shifted VIA45. The DRC checks merged metal, so the top-level polygon need not supply the enclosure alone (seed, reference-design-verified).

Step 4. Reshape the M4 polygon to (x_left, y_bottom_new, x_right, y_top_new) (seed, reference-design-verified).

Step 5. Move each VIA_VIA34 instance in y to the center of the new M4 y-extent: new_y_VIA34 = (y_bottom_new + y_top_new) / 2 (seed, reference-design-verified). Verified on all six VIA34 y-moves: targets 1200, 3312, 4272, 5424, 6576, 7536 -- each exactly the center of its repaired M4. The seventh Family-B site (center 2160, unchanged) needed no VIA34 move. The y-DELTA of VIA34 does NOT equal the M4 bottom-edge shift -- in worked example B1 the bottom edge moved +164 while VIA34 moved +120; only the centering formula reproduces the measured outcome (seed, reference-design-verified).

VIA_VIA34 repositioning may be accomplished either by move_instance or by delete_instance + add_via at the new origin; iteration 5 used the delete+add form for seven VIA34s and achieved the same y-centering result (trial:i05.ug.whole_design.00). Both forms place the VIA34 origin at the new M4 center y; use whichever the repair channel supports.

VIA_VIA34 keeps its x unchanged in the M5-stripe flow (seed, reference-design-verified): it binds M3-M4 and M4 does not move in x; all six stripe-site VIA34 kept x -- 1480 stayed 1480, 1864 stayed 1864 -- adjusting y only. One other VIA34 at (5652,8304) moved +64 in x, but as part of the Family-A column repair at x=5652 (the same +64 taken by the co-located VIA12/VIA23 instances and their associated M2/M3 polygons), not the stripe batch. Do not apply the M5/VIA45 x-shift to VIA34 (seed, reference-design-verified).

In repair passes not driven by M5-stripe x-shift, VIA34 x-columns are fixed by the M4 column geometry. Iteration 5 placed VIA34 instances at x=2200 (four sites: y=2160, 4272, 6576, 8688) and x=2968 (three sites: y=3312, 5424, 7536); all y-values satisfy y mod 192 == 48, and the x-positions were determined by the M4 column layout, not by an M5 shift (trial:i05.ug.whole_design.00).

Step 6. Move VIA_VIA45: x follows the M5 stripe shift (all 7 repaired VIA45 took dx = -88); y moves only if the M4 center changed (6 of 7 did; the (1864,2160) site kept dy=0 because its M4 center was already correct). VIA45 delta = (dx_from_M5_shift, new_M4_center_y - old_via_y) -- compute x and y components separately, then sum (seed, reference-design-verified).

Worked example B1 (M4.AUX.1 + V3.M4.AUX.2 on the M4 at (1388,988,1572,1172)):
  M4 BEFORE (1388,988,1572,1172): y_bottom=988, y_top=1172.
    988 mod 96 = 28 (off-grid); 1172 mod 96 = 20 (off-grid).
    Height = 184 dbu != 96 dbu (V3 height). Both rules fire.
  M4 AFTER (1388,1152,1572,1248): y_bottom=1152=12*96, y_top=1248=13*96. On-grid.
    Height = 96 dbu = V3 height. Both rules clear.
  VIA34 repositions from y=1080 to y=1200 (delta +120 dbu = 30 nm).
  VIA45 repositions from (1480,1080) to (1392,1200): delta (-88,+120) dbu.

Worked example B2 (right-column M4 polygon at (1772,2068,1956,2252)):
  M4 BEFORE (1772,2068,1956,2252): y-height=184 dbu != 96 (V3 height), y-edges off-grid (2068 mod 96 = 52, 2252 mod 96 = 44).
  x-width 184 is NOT itself illegal (B1's repaired M4 keeps x-width 184 in the 0-violation final state); this site additionally narrows x for site-specific coverage geometry.
  M4 AFTER (1816,2112,1912,2208): x-width=96 dbu, y-height=96 dbu.
  x also narrows: left x 1772->1816 (+44), right x 1956->1912 (-44). The top-level M4 x-center stays at 1864 -- it is NOT centered on the new VIA45 position (x=1776 after the -88 M5 shift). Coverage of the shifted VIA45 is provided by the MERGED M4 geometry: the via cell's own M4 land plus this narrowed top-level polygon remain valid together (seed, reference-design-verified).
  VIA34 at (1864,4320) in a neighboring segment repositions to (1864,4272).

Geometry preservation (Family B): M4 is reshaped at the same local routing site. VIA34 re-centers on the repaired M4 y-extent, keeping the merged M4 (top-level + via cell's own land) valid around V3. VIA45 follows the M5 x-shift, and additionally moves to the new M4 center in y when that center changed. The M4 x-narrowing is sized so the MERGED M4 (top-level polygon + the VIA45 cell's own M4 land) stays valid and connected around V4. At the 2160 site, the shifted via center (x=1776) lies outside the top-level M4 polygon (1816-1912); the merged overlap is 1816-1868 (seed, reference-design-verified).

---

### Family D: M4 parallel run length (M4.S.5)

Rule semantics: M4.S.5 requires a minimum parallel run length between two M4 polygons on adjacent tracks of 44 nm = 176 dbu (seed, reference-design-verified).

Root cause: One M4 polygon had a left edge at x=3592 that was too close to the start of the parallel overlap region with a neighbor on the adjacent track, leaving < 176 dbu of parallel run. The violation marker was only 4 dbu (1 nm) wide (seed, reference-design-verified).

Recipe -- left-edge extension + neighbor offset:

Step 1. Identify the two M4 polygons with insufficient parallel overlap (seed, reference-design-verified).
Step 2. Extend the nearer polygon's left edge leftward by the minimum delta_extend such that the resulting parallel overlap >= 176 dbu (seed, reference-design-verified).
Step 3. If the extension reduces the M4-to-M4 gap with a same-track neighbor below 40 nm = 160 dbu (M4.S.2), move that neighbor in x by a compensating delta to restore the gap (seed, reference-design-verified).

Worked example D1 (M4.S.5 at [3592,480,3596,576]):
  Violating M4 polygon BEFORE (3592,384,3700,480): left edge at x=3592.
  Adjacent-track partner: the M4 land (3412,576,3596,672) of a via cell instance at (3504,624) (its M4 land spans +/-92 in x, +/-48 in y around the instance origin). Parallel-run overlap BEFORE = [3592,3596] = 4 dbu.
  Same polygon AFTER (3420,384,3700,480): left edge at x=3420 (moved -172 dbu = 43 nm leftward). Overlap becomes [3420,3596] = 176 dbu -- exactly the M4.S.5 threshold (the partner's left edge 3412 lies just beyond 3420).
  Same-track neighbor (196x96 dbu at (3120,384), right edge 3316) moved to (3052,384), delta -68 dbu: the extension had cut the tip gap to 3420-3316 = 104 dbu < 160 dbu; the move restores 3420-3248 = 172 dbu (seed, reference-design-verified).

Geometry preservation (Family D): the extension enlarges an existing M4 shape, and the nearby M4 polygon is shifted away by -68 dbu. No via co-move appears in the final diff for this M4.S.5 repair (seed, reference-design-verified).

---

## Multi-layer repair records

### Trial i01.ug.whole_design.00

Trial i01.ug.whole_design.00 (Block5, channel unit_gate, 19 ops, conn_preserved=true) repaired violations across layers M1-M5 and V1-V4 in a single pass (trial:i01.ug.whole_design.00). M4 was among the touched layers. The repair included 14 via/cell instance moves (y-only, x-only, or combined), two polygon resize-end operations (p879: y high end +48 dbu; p910: x +8 dbu plus y high end +20 dbu), and two instance x-moves of +8 dbu (i0061, i0104) (trial:i01.ug.whole_design.00). The +48 dbu y-extension of p879 is a half-pitch step in y (48 = 96/2), consistent with snapping a y-edge by one half-interval toward the 96-dbu grid. Connectivity was preserved across all 19 ops (trial:i01.ug.whole_design.00).

### Trial i03.cu.def:VIA_VIA45_1_2_58_58.00 and i03.ug.whole_design.00

These two trials from iteration 3 address the same M4/M5/V4 violation set in a coordinated two-channel sequence (trial:i03.cu.def:VIA_VIA45_1_2_58_58.00, trial:i03.ug.whole_design.00).

**cu_pool step** (trial:i03.cu.def:VIA_VIA45_1_2_58_58.00): 1 op, conn_preserved=true. Applies a resize_via_shape on cell definition VIA_VIA45_1_2_58_58, axis y, delta -88 dbu (trial:i03.cu.def:VIA_VIA45_1_2_58_58.00). This is a cell-definition-level operation, not an instance move; it modifies the via cell's internal shape and therefore affects every placed instance of that cell simultaneously. The repair reduced the violation count by 15 (47 -> 32) across layers M4, M5, V4 (trial:i03.cu.def:VIA_VIA45_1_2_58_58.00).

**unit_gate step** (trial:i03.ug.whole_design.00): 9 ops, conn_preserved=true, decision=gated_in. Operations are all x-moves of +32 dbu: two M4/M5 polygon moves (p878, p879) and seven instance moves (i0001, i0062, i0067, i0073, i0112, i0113, i0114), touching layers M4, M5, V4 (trial:i03.ug.whole_design.00). The assemble_drops field records that the resize_via_shape(axis=y, delta=-88) op for VIA_VIA45_1_2_58_58 was dropped from the unit_gate assembly because cu_pool had already applied it (trial:i03.ug.whole_design.00).

Two distinct x-shift magnitudes appear in iteration 3 data: the +32 dbu polygon/instance x-moves in the unit_gate step differ from the -88 dbu delta seen in Family-B VIA45 instance moves. These are separate repair components operating on different geometry groups within the same pass (trial:i03.ug.whole_design.00).

The resize_via_shape op (axis=y, delta=-88) modifies the cell definition, not a placed instance. When cu_pool applies such a cell-definition op, the unit_gate assembler detects it as already applied and drops it from the unit_gate bundle to prevent double-application (trial:i03.cu.def:VIA_VIA45_1_2_58_58.00, trial:i03.ug.whole_design.00).

### Trial i05.ug.whole_design.00

Trial i05.ug.whole_design.00 (Block5, channel unit_gate, 19 ops, conn_preserved=true, decision=gated_in) repaired M4/V3 violations without involving M5 or V4 (trial:i05.ug.whole_design.00). touched_layers = M1, M2, M3, M4, V1, V3.

The 19 ops break into four groups (trial:i05.ug.whole_design.00):

1. **Two M4 polygon right-edge extensions**: resize_end on p951 and p955, axis=x, end=high, delta=+128 dbu each. These extend the high-x edge of two M4 polygons by 128 dbu to provide M4 coverage for the newly placed VIA34 instances in adjacent columns.

2. **Three instance x-moves**: i0111 (+72, 0), i0025 (+72, 0), i0012 (-36, 0). All are x-only moves with no y component.

3. **Seven delete_instance ops**: i0098, i0105, i0075, i0076, i0099, i0002, i0070. These remove the pre-existing VIA_VIA34 instances at their old (y-off-center) positions.

4. **Seven add_via ops** (cell VIA_VIA34) at the following origins:
   - x=2200 column: (2200,2160), (2200,4272), (2200,6576), (2200,8688)
   - x=2968 column: (2968,3312), (2968,5424), (2968,7536)

All seven placed VIA34 y-coordinates satisfy y mod 192 == 48, confirming they lie on legal M4 routing track centers (trial:i05.ug.whole_design.00). The y-values 3312, 4272, 5424, 6576, 7536 match the Family-B repaired center table; y=2160 is the no-y-move Family-B site; y=8688 is a new confirmed legal track (8688 mod 192 = 48). The delete+add_via approach achieves VIA34 repositioning equivalently to move_instance; the new origin's y-coordinate equals the target M4 center in both methods (trial:i05.ug.whole_design.00).

This trial establishes that M4/V3 repair passes can occur independently of M5 and V4: touched_layers in i05 excludes M5 and V4, in contrast to i03 (M4, M5, V4) and i01 (M1-M5, V1-V4). When the M4 violation set does not require M5 stripe movement, the repair is confined to M4, V3, and their coupled via layers (trial:i05.ug.whole_design.00).

---

## Final-pair measured facts (reference-design tail evidence)

These facts come from the final-pair comparison of the reference design's initial layout against its repaired final layout, plus the BEFORE and AFTER DRC reports (seed, reference-design-verified).

- M5.AUX.1 is resolved by coordinate snapping (x-shift of the stripe), with M5.AUX.2 track parity (center_x mod 192 == 48) picking the snap direction. The M4 grid fixes combine y-edge snapping (M4.AUX.1), height normalization to the V3 height, track parity (center_y mod 192 == 48, M4.AUX.2), and the coupled VIA34/VIA45 moves. No object add/delete was needed in either of these cases -- a property of these specific repairs (seed, reference-design-verified).

---

## Case notes

M5 and M4 are tightly coupled in the stripe-repair flow: M5.AUX.1 drives the M5 x-shift, which forces VIA45 x-move, which forces a top-level M4 x-extent adjustment to keep the MERGED M4 valid around V4. M4.AUX.1 independently forces M4 y-move. VIA45 tracks both x and y components; the seven-site table above shows the resulting combined deltas (seed, reference-design-verified). In trial:i01.ug.whole_design.00, 19 ops spanning M1-M5 and V1-V4 were applied in a single connected pass that preserved all connectivity (trial:i01.ug.whole_design.00).

M4/V3 repairs that are not driven by M5-stripe movement run without M5 or V4 involvement. In trial:i05.ug.whole_design.00, 7 VIA34 delete+add pairs and 2 M4 polygon right-edge extensions (+128 dbu) cleared the M4.AUX.1 / V3.M4.AUX.2 violation set within touched_layers = {M1, M2, M3, M4, V1, V3} (trial:i05.ug.whole_design.00). Do not assume M5 is always co-involved in M4 repairs.

M4 polygon x-extent extension (resize_end axis=x end=high) is a valid M4 repair operation distinct from x-narrowing. Narrowing (B2 example) reduces x to accommodate a shifted VIA45 in the M5-stripe flow; extension (+128 dbu in i05) enlarges x to cover newly placed VIA34 instances at adjacent column positions. Both operate on MERGED M4 coverage validity (seed, reference-design-verified; trial:i05.ug.whole_design.00).

M4.S.5 is margin-sensitive: the violation marker was 4 dbu (1 nm) wide. The fix applied a 172 dbu extension -- a 43x multiple of the apparent gap -- because M4.S.5 measures parallel run length (the longitudinal extent of overlap), not point spacing. A marginal parallel-run deficit requires a substantially larger metal extension than the violation marker size indicates (seed, reference-design-verified).

The cu_pool channel handles cell-definition-level repairs (resize_via_shape) before the unit_gate pass; the unit_gate assembler's assemble_drops mechanism removes already-applied cell-definition ops to prevent reapplication. In iteration 3, the resize_via_shape(VIA_VIA45_1_2_58_58, y, -88 dbu) reduced violations by 15 before the unit_gate +32 dbu x-move group was assembled (trial:i03.cu.def:VIA_VIA45_1_2_58_58.00, trial:i03.ug.whole_design.00).