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

### Multi-leaf via conflict resolution (iteration 2 evidence)

When two repair leaves independently compute conflicting repositioning moves for
the same VIA34 instance, the assembler drops BOTH moves and leaves the instance
at its pre-repair position. Measured in trial:i02.ug.leaf_0003.02 and
trial:i02.ug.leaf_0004.03: instance i0345 was claimed by leaf_0003 as [+32,-96]
dbu and by leaf_0004 as [+32,+32] dbu; both were tagged external_conflict_dropped
and neither move was committed. Instance i0505 underwent the same bilateral
cancellation (leaf_0003 proposed [-16,-96], leaf_0004 proposed [-16,+32]).
The assembled design state remained conn_preserved=true and gated_in for both
trials despite these drops, confirming that partial via repositioning (some
instances moved, some left stationary) is legal when connectivity is preserved.

This means: in a multi-leaf repair run, a VIA34 whose correct y-target is
disputed between overlapping crop regions will NOT be repositioned. The M4
polygon edge fixes and M5 x-shifts in those same trials are still committed via
their own (undisputed) polygon-move ops. The result is an M4 geometry that is
now on-grid in y-height but whose associated VIA34 has NOT been re-centered --
a partial-repair state that may leave residual V3.M4.AUX.2 or M4-enclosure
violations in the conflict zone. Any follow-on iteration must detect and resolve
the un-moved VIA34 instances independently (trial:i02.ug.leaf_0003.02,
trial:i02.ug.leaf_0004.03).

---

### Combined-axis via instance moves (iteration 2 evidence)

Via instances that fall under BOTH an M5 stripe x-shift and an M4 center y-change
receive a single atomic [dx, dy] move rather than two separate passes.
Measured in trial:i02.ug.leaf_0003.02: instances i0356 ([+32,-64] dbu),
i0176 ([+32,-112] dbu), i0493 ([-16,-64] dbu), and i0042 ([-16,-112] dbu) each
took simultaneous x and y repositioning in one op. The x-component (+32 or -16)
follows the M5 stripe shift for that column; the y-component (-64, -112) equals
the change in the corresponding M4 y-center. These instances were not in conflict
with leaf_0004 and their moves were committed without drops. No new V3.*
violations appeared in-crop for either trial despite the via moves
(trial:i02.ug.leaf_0003.02 new_in_crop_by_rule contains no V3 entry;
trial:i02.ug.leaf_0004.03 likewise), confirming that atomically combined
x+y repositioning of VIA34 instances keeps V3 DRC-clean when the target M4
center and M5 stripe position are both correctly resolved.

---

### Cross-crop polygon priority (iteration 2 evidence)

For polygon edge moves that span two overlapping crop regions, the first-processed
leaf takes the move and the second is dropped with reason cross_crop_first_wins.
In trial:i02.ug.leaf_0004.03, polygon p1143 (x-move +32), p1142 (x-move -16),
and p1561 (y-move +32) were each dropped because leaf_0003 already committed
the same polygons. This is distinct from external_conflict_dropped: a
cross_crop_first_wins drop means the two leaves proposed the SAME polygon but the
conflict resolution did not evaluate whether the y-deltas agreed -- it simply
deferred to the first claimant. The leaf_0003 ops for p1561 (y delta=-96) and the
leaf_0004 attempt (y delta=+32) had opposite signs; the assembled result applied
only the leaf_0003 value. When polygon moves cross crop boundaries, only the
first-processed leaf's delta is applied regardless of the second leaf's computed
value (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03).

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
  (M4.AUX.1), height normalization to the V3 height, track parity
  (center_y mod 192 == 48, M4.AUX.2), and the coupled VIA34/VIA45 moves. No
  object add/delete was needed in either of these cases -- a property of these
  repairs, not a universal rule.


## Case notes (reference-design tail evidence)

Anti-pattern AP-2 (atomic stripe batch): an M5 stripe x-shift and ALL VIA_VIA45
instances associated with that shifted stripe must be applied as one complete
batch. The final diff shows two M5 stripes shifted -88 dbu in x, and all seven
repaired VIA45 instances also take dx=-88. VIA_VIA34 is NOT part of that x-batch
(it keeps x and re-centers in y with the M4 reshape -- see Family B Step 5).
From a local crop, do not submit a partial stripe migration unless the complete
VIA45 target set for that stripe is known.

Anti-pattern AP-3 (partial via repositioning from bilateral conflict): when a
VIA34 instance is claimed by two overlapping leaves with conflicting y-deltas,
the assembler cancels BOTH moves. The resulting layout has the M4 polygon
on-grid but the VIA34 un-centered. Do not treat a gated_in / conn_preserved
result as proof that all via repositioning succeeded; inspect the assemble_drops
list for external_conflict_dropped entries on via instances and schedule a
follow-on repair pass for any that were bilaterally cancelled
(trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03).