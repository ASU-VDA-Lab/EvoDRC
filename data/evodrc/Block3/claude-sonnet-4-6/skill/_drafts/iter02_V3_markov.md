Now I have both the current knowledge and the new records fully in mind. Producing the updated body:

---

(seed, reference-design-verified)

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
   432 belongs to Family D (-> see M4.md), not this family).
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

  (An eighth M4 reshape at center 432 belongs to Family D (-> see M4.md) and also sits on a
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
Step 6. Move VIA_VIA45: x follows the M5 stripe shift at the site (see M5 stripe
  shift note below); y moves ONLY IF the associated M4 landing's y-center changed
  (6 of 7 did in the reference design; the (1864,2160) site kept dy=0 because its
  M4 center was already correct). VIA45 delta = (delta_x_from_M5,
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

### Iteration-2 extension A: y-only via repositioning without polygon reshape (V3.M4.AUX.2)

When the M4/V3 alignment error is small enough that no polygon edge needs to
move, a set of y-only instance moves resolves the violation without any
resize_end or reshape op. In trial:i02.ug.leaf_0003.02 six instances spanning
M3, M4, M5, V3, and V4 were repositioned with y-only deltas drawn from
{-48, +48, +96} dbu; n_new_in_crop=0 and conn_preserved=true confirm a clean,
zero-regression repair. The deltas arrive in matched pairs -- two instances
sharing the same dy in each pair -- consistent with (VIA34, VIA45) pairs that
share a landing track requiring the same y-centering correction.

This form of repair is distinct from the full Family B recipe: no polygon is
touched, x coordinates are unchanged for all six instances, and the op list
contains only move_instance entries (trial:i02.ug.leaf_0003.02). Apply this
lighter repair first when the only defect is V3 (or via) y-misalignment
relative to an already-on-grid M4; escalate to the full Family B recipe only
when M4 polygon edges are themselves off-grid.

---

### Iteration-2 extension B: M4 edge extension with coordinated via pairs (V3.M4.AUX.2, M4.AUX.1)

M4 polygon repair does not require full reshape of the bounding box. Individual
y-edges can be extended with resize_end ops while the opposing edge stays fixed,
provided a via is repositioned to re-center on the updated M4 y-extent. In
trial:i02.ug.leaf_0004.03 four M4 polygons each received a single-edge y
extension: p1104 high end +72 dbu, p1103 high end +24 dbu, p1102 low end 24 dbu
downward, p1101 low end 72 dbu downward; these are four independent sites, not
a single polygon receiving four edits. The direction of each associated via move
(trial:i02.ug.leaf_0004.03) matches the edge extension direction:

  polygon | edge moved | delta  | paired via dy
  --------|-----------|--------|---------------
  p1104   | high (top)| +72    | +72
  p1103   | high (top)| +24    | +24
  p1102   | low (bot) | -24    | -24
  p1101   | low (bot) | -72    | -72

Each site produces two instance moves: one at [0, dy] (VIA34-pattern, x
unchanged) and one at [+32, dy] (VIA45-pattern, following an M5 x-shift of +32
dbu at this unit). A fifth polygon p1059 shifted +32 dbu in x, confirming an
M5 stripe shift of +32 dbu drives the [+32, dy] component of the VIA45 moves
(trial:i02.ug.leaf_0004.03). Trial:i02.ug.leaf_0004.03 produced n_new_in_crop=2
but was gated_in because conn_preserved=true; the gating logic accepts new
in-crop violations when connectivity is preserved.

**M5 x-shift magnitude is site-specific.** The reference design (seed) has two
M5 stripes each shifting -88 dbu. In trial:i02.ug.leaf_0004.03 the shift is
+32 dbu (a different unit, Block3/leaf_0004). Do not assume -88; read the M5
stripe delta from the actual repair context and apply it uniformly to all VIA45
instances on that stripe.

---

## Final-pair measured facts (reference-design tail evidence)

Provenance: these facts come from the final-pair comparison of the reference
design's initial layout against its repaired final layout, plus the BEFORE and
AFTER DRC reports. Every coordinate and delta cited in this section is quoted
inline from that pair; the layout files themselves are not needed and are not
shipped with this skill.

- M5.AUX.1 is resolved by coordinate snapping (x-shift of the stripe), with the
  M5.AUX.2 track parity (center_x mod 192 == 48) picking the snap direction.
  The M4 grid fixes are NOT mere snapping: they combine y-edge snapping
  (M4.AUX.1), height normalization to the V3 height, track parity
  (center_y mod 192 == 48, M4.AUX.2), and the coupled VIA34/VIA45 moves. No
  object add/delete was needed in either of these cases -- a property of these
  repairs, not a universal rule.


## Case notes

Anti-pattern AP-2 (atomic stripe batch): an M5 stripe x-shift and ALL VIA_VIA45
instances associated with that shifted stripe must be applied as one complete
batch. The reference design (seed) shows two M5 stripes shifted -88 dbu in x,
and all seven repaired VIA45 instances also take dx=-88; trial:i02.ug.leaf_0004.03
confirms the same structural rule with a +32 dbu stripe shift -- one polygon
(p1059) shifts +32 in x and every VIA45 in that unit takes the same +32 dx
component. VIA_VIA34 is NOT part of that x-batch (it keeps x and re-centers in
y with the M4 reshape or edge extension -- see Family B Step 5 and Iteration-2
extension B above). From a local crop, do not submit a partial stripe migration
unless the complete VIA45 target set for that stripe is known.

Gating observation: a repair with n_new_in_crop > 0 is accepted as gated_in
when conn_preserved=true (trial:i02.ug.leaf_0004.03, n_new_in_crop=2). The
gate does not require zero new violations when connectivity is intact.