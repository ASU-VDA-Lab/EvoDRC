## Per-rule recipes

### Family B: M4 on-grid reshape and V3 height matching (M4.AUX.1, V3.M4.AUX.2)

These two rules co-fired on the same M4 polygons in this block; do not assume
the pairing is universal. M4.AUX.1 fires because horizontal edges
(y-coordinates) are off the 24 nm (96 dbu) grid. V3.M4.AUX.2 fires because the
M4 y-extent does not match the V3 via y-height. In the example block all 7
M4.AUX.1 violations and all 7 V3.M4.AUX.2 violations are cleared by reshaping
the same 7 M4 polygons.

Family B in three verified facts:
1. Seven M4 polygons were reshaped or narrowed (an eighth M4 reshape at center
   432 belongs to Family D, not this family).
2. Six of the seven then needed a VIA34 y-move to the new M4 center; the
   seventh (center 2160) was already on a legal track, so its VIA34 stayed --
   but the M4 itself was STILL reshaped (y-height 184 -> 96 with the center
   fixed at 2160, plus x-narrowing); its VIA45 moved in x only, following M5.
3. Every repaired M4 center satisfies y mod 192 == 48: edge grid (96) AND
   track parity (192) must BOTH hold.

Rule semantics:
- M4.AUX.1: M4 horizontal edges must lie on the 24 nm = 96 dbu grid.
- V3.M4.AUX.2: V3 y-extent must exactly equal M4 y-extent (both perpendicular to
  M4 length, which runs in x). The V3 cut's y-extent is 96 dbu = 24 nm
  (via-cell geometry: the cut is 72x96); the deck's V3.W.1 separately requires
  a minimum V3 width of 18 nm along the M4 length. After repair, M4 y-height is
  also 96 dbu.

Recipe -- M4 reshape to on-grid height + coordinated via repositioning:

Step 1. For each off-grid M4 polygon, choose the target y for the new M4
  CENTER. Two grid constraints stack:
  (1a) EDGE grid (M4.AUX.1): both new y-edges on the 96-dbu grid, so with a
       96-dbu height the center is at k*96 + 48;
  (1b) TRACK grid (M4.AUX.2): the center must lie on a horizontal ROUTING
       TRACK, and legal track centers satisfy y mod 192 == 48 -- every k*96+48
       with the wrong parity (y mod 192 == 144) is an ILLEGAL track even though
       its edges are on the 96 grid.
  Verified -- all seven Family-B sites (old center = old VIA34 y; every new
  center satisfies y mod 192 == 48):

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

  (An eighth M4 reshape at center 432 belongs to Family D and also sits on a
  legal track.) The mod-96-only rule would have selected 1104 for the 1080-site
  -- an illegal ==144 track -- so 1104 is not a valid final-pair candidate.
  DEFAULT candidate: the NEAREST center with y mod 192 == 48; that default
  matches 6 of the 7 sites above. The single exception is the 1080-site, which
  chose 1200 (+120) over the nearest legal 1008 (-72): even among legal tracks
  the nearest can conflict with other geometry. Confirm with the preview and
  step by +/-192 to the next legal track if it fails.
Step 2. Derive the edges from the chosen center:
  y_bottom_new = center_y - 48, y_top_new = center_y + 48
  (96-dbu M4 height = V3_height in ASAP7; verify V3_height against the PDK via
  cell before applying).
Step 3. Optionally adjust x-extent: if the VIA_VIA45 (V4, between M4 and M5) has
  shifted in x due to Family C (-> see M5.md) (M5 grid fix), adjust the top-level M4 x-extent so
  the MERGED M4 geometry (top-level polygon unioned with the via cell's own M4
  land) remains valid around the shifted VIA45 -- the DRC checks merged metal,
  so the top-level polygon does not have to supply the enclosure alone.
Step 4. Reshape the M4 polygon to (x_left, y_bottom_new, x_right, y_top_new).
Step 5. Move each VIA_VIA34 instance in y to the CENTER of the new M4 y-extent:
  new_y_VIA34 = (y_bottom_new + y_top_new) / 2.
  (Verified on all SIX VIA34 y-moves: targets 1200, 3312, 4272, 5424, 6576,
  7536 -- each exactly the center of its repaired M4; the seventh Family-B site
  (center 2160, unchanged) needed NO VIA34 move. NOTE: the y-DELTA of VIA34 does
  NOT equal the M4 bottom-edge shift -- in the worked example B1 the bottom edge
  moved +164 while VIA34 moved +120; only the centering rule reproduces the
  verified outcome.)
  VIA_VIA34 keeps its x unchanged IN THIS M5-STRIPE FLOW: it binds M3-M4 and
  M4 does not move in x (verified: all six stripe-site VIA34 kept x -- 1480
  stayed 1480, 1864 stayed 1864 -- adjusting y only). Do NOT apply the M5/VIA45
  x-shift to VIA34. Scope note: one other VIA34 at (5652,8304) DID move +64 in
  x -- but as part of the Family-A column repair at x=5652 (the same +64 taken by
  the co-located VIA12/VIA23 instances and their associated top-level M2/M3
  polygons), not as part of any stripe batch.
Step 6. Move VIA_VIA45: x ALWAYS follows the M5 stripe shift (all 7 repaired
  VIA45 took the same -88 dx); y moves ONLY IF the associated M4 landing's
  y-center changed (6 of 7 did; the (1864,2160) site kept dy=0 because its M4
  center was already correct). VIA45 delta = (delta_x_from_M5,
  new_M4_center_y - old_via_y, which may be 0).

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

Geometry preservation (Family B): M4 is reshaped at the same local routing
site. VIA34 re-centers on the repaired M4 y-extent (centering rule, Step 5),
keeping the merged M4 (top-level + via cell's own land) valid around V3.

VIA45 always follows the M5 x-shift, and additionally moves to the new M4
center in y when that center changed. The M4 x-narrowing is sized so the
MERGED M4 (top-level polygon + the VIA45 cell's own M4 land) stays valid and
connected around V4. Note the shifted via's CENTER may lie outside the
top-level polygon (verified at the 2160 site: via at x=1776, top-level M4 at
1816-1912, merged overlap 1816-1868).

---

### Family D: M4 parallel run length (M4.S.5)

Rule semantics:
- M4.S.5: Minimum parallel run length between two M4 polygons on adjacent tracks
  is 44 nm = 176 dbu.

Root cause: One M4 polygon had a left edge at x=3592 that was too close to the
start of the parallel overlap region with a neighbor on the adjacent track,
leaving < 176 dbu of parallel run. The violation marker was only 4 dbu (1 nm)
wide, indicating a marginal deficiency.

Recipe -- Left-edge extension + neighbor offset:

Step 1. Identify the two M4 polygons with insufficient parallel overlap.
Step 2. Extend the nearer polygon's left edge leftward by delta_extend such that
  the resulting parallel overlap >= 176 dbu. Choose delta_extend to be the minimum
  needed (minimal-delta discipline).
Step 3. If the extension would violate M4-to-M4 spacing with a neighboring polygon
  on the same track (horizontal spacing >= 40 nm = 160 dbu, M4.S.2), move that
  neighbor in x (away) by a compensating delta.

Worked example D1 (M4.S.5 at [3592,480,3596,576]):
  Violating M4 polygon BEFORE (3592,384,3700,480): left edge at x=3592.
  Adjacent-track partner: the M4 land (3412,576,3596,672) of a via cell
  instance at (3504,624) (its M4 land spans +/-92 in x, +/-48 in y around the
  instance origin). Parallel-run overlap BEFORE = [3592,3596] = 4 dbu.
  Same polygon AFTER (3420,384,3700,480): left edge at x=3420 (moved -172 dbu
  = 43 nm leftward). Overlap becomes [3420,3596] = 176 dbu -- exactly the
  M4.S.5 threshold (the partner's left edge 3412 lies just beyond 3420).
  Same-track neighbor (196x96 dbu at (3120,384), right edge 3316) moved to
  (3052,384), delta -68 dbu: the extension had cut the tip gap to
  3420-3316 = 104 dbu < 160 dbu (40 nm, M4.S.2 horizontal spacing); the move
  restores 3420-3248 = 172 dbu (12 above the minimum; -56 would have met 160
  exactly -- the reference repair kept margin here).

Geometry preservation (Family D): the extension enlarges an existing M4 shape,
and the nearby M4 polygon is shifted away by -68 dbu. No via co-move appears in
the final diff for this M4.S.5 repair.

---

### Family E: M4 x-extent resize in unit-gate repairs (iteration 1)

In trial i01.ug.leaf_0001.03, two M4 polygon edges were adjusted in x: p1065
high-end (right edge) extended +184 dbu, p957 low-end (left edge) extended +176
dbu. A via instance (i0086) moved +128 dbu in x simultaneously. Layers touched
were M1, M2, M4, V1; zero new violations were introduced and
conn_preserved=true. The locus [4656,2112,5760,3132] is a distinct region from
the Family-B and Family-D sites (trial i01.ug.leaf_0001.03). This demonstrates
that M4 x-extent adjustments can occur independently of y-grid repairs, driven
by connectivity or spacing requirements at a specific gate site, without
triggering M4.AUX.1 or V3.M4.AUX.2.

---

### Via instance y-repositioning (iteration 1, M4/M5/V3/V4 coupling)

In trial i01.ug.leaf_0012.07, four via instances were repositioned in y within
locus [1728,2068,10368,8732]: i0097 and i0092 each moved -48 dbu; i0064 and
i0072 each moved +96 dbu. Layers touched were M3, M4, M5, V3, V4. The repair
was gated_in with conn_preserved=true, accepting 2 new V1.M1.EN.1 violations as
debt. The via y-moves are distinct from the Family-B x-unchanged / y-center rule
(those were VIA34/VIA45 repositioning following an M4 y-reshape); these are
top-level via instance moves that reposition the via cell's M4 and M5 lands
together, without reshaping the top-level M4 polygon itself.

---

### VIA_VIA45 cell-definition M4 land resize (cu_pool channel, iteration 1)

The cu_pool channel applies cell-definition-level shape resizes that affect all
instances of a named via cell. In trial i01.cu.def:VIA_VIA45_1_2_58_58.01, the
M4 landing shape (shape_index 0) inside VIA_VIA45_1_2_58_58 was widened +152
dbu in x, and both V4 cut shapes (shape_index 0 and 1) were also widened +152
dbu in x. This single cell-definition op reduced total violations by 16 across
two units (8 fewer in leaf_0012, 8 fewer in leaf_0013). When this op is applied
via cu_pool first, subsequent unit_gate trials show it in their assemble_drops
with reason "cu_pool:applied" rather than re-executing it (trial
i01.ug.leaf_0012.07). The M4 shape resize within a via cell definition is
therefore a valid repair mode distinct from reshaping top-level M4 polygons: it
widens the M4 land that is part of the via cell, and the cu_pool applies it
globally to all instances of that cell definition.

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
  (M4.AUX.1), height normalization to the V3 height, track parity (center_y mod
  192 == 48, M4.AUX.2), and the coupled VIA34/VIA45 moves. No object add/delete
  was needed in either of these cases -- a property of these repairs, not a
  universal rule.

---

## Case notes (reference-design tail evidence)

M5 and M4 are tightly coupled: M5.AUX.1 drives M5 x-shift. That shift forces
VIA45 x-move. VIA45 x-move forces a top-level M4 x-extent adjustment (to keep
the MERGED M4 valid around V4). M4.AUX.1 independently forces M4 y-move. VIA45
must track both, producing combined deltas such as (-88, -48) or (-88, +120).
Compute the x and y components separately, then sum.

M4.S.5 is margin-sensitive: the violation marker was 4 dbu (1 nm) wide. The fix
applied a 172 dbu extension -- a 43x multiple of the apparent gap. This is because
M4.S.5 checks parallel run length (the longitudinal extent of overlap between two
tracks), not point spacing. Fixing a marginal parallel-run deficit may require a
substantially larger metal extension than the violation marker size suggests.

In Block2 iteration 1, two repair channels operate on M4: unit_gate reshapes
individual top-level polygons and repositions via instances (trials
i01.ug.leaf_0001.03, i01.ug.leaf_0012.07); cu_pool resizes via cell definitions
globally (trial i01.cu.def:VIA_VIA45_1_2_58_58.01). Cu_pool ops are applied to
the cell definition before unit_gate ops run; unit_gate drops any op already
covered by cu_pool with reason "cu_pool:applied".