<!-- BEGIN GATING-DOCTRINE v3 (harness-managed ZONE A; the skill distiller NEVER edits this block) -->
## SG0 What this section is
These are the HARD gating rules of the repair harness. They are maintained by the
harness itself (not by the knowledge distiller) and are identical in every
iteration. Everything below this block ("ZONE B") is living knowledge distilled
from experience and may change each iteration; if ZONE B ever appears to
contradict this section, THIS SECTION WINS.

## SG1 Repair-order doctrine: REGIONAL before GLOBAL
Always exhaust REGIONAL fixes first: `move_instance`, guarded `delete_instance`,
and top-level polygon ops (`resize` / `resize_end` / `move` / `delete` /
`add_jog` / `add_polygon`). Their effect stays local to one placement's
neighborhood. A via-structure edit (`resize_via_shape` / `move_via_shape`)
rewrites the SHARED cell definition and re-renders at EVERY placement of that
via type block-wide -- escalate to it ONLY when no regional op can clear the
violation.

## SG2 Universality test (the 100% rule) -- read it off "## Shared-target context"
Every crop prompt carries a harness-computed section
`## Shared-target context (block-wide, input-derived)` listing, for each shared
via definition: total placements, VDD/VSS/CLK/signal ownership split, how many
YOU own, and per-rule violating-placement fractions `V_R/T`.
- A structure edit on definition D motivated by rule R is admissible ONLY when
  the section marks that rule `(=100%)` -- i.e. EVERY placement of D violates R.
  No legal placement context exists, so the defect is in the definition itself.
- ANY smaller fraction (even T-1 of T) proves at least one compliant sibling
  exists -- the definition CAN satisfy the rule in a legal context -- so the
  defect is POSITIONAL: fix by move/delete, or leave the violation unfixed.
- The fraction is per (definition, rule): a def may be 100% for one rule
  (admissible for that rule) and 30% for another (forbidden for that one).
- NEVER infer "all placements violate" from your own window: crops are built
  AROUND violations, so in-window samples are ~100% violating by construction.
  Only the injected block-wide fraction counts.
- Merged-geometry caveat: enclosure/coincidence rules are checked on MERGED
  metal. A definition whose own land under-encloses its cut in ISOLATION can be
  correct-by-design when placed on background metal that supplies the rest.
  Def-only arithmetic showing a shortfall is NOT evidence for a structure edit.

## SG3 Duties when a structure edit IS admissible (rule at 100%)
1. State in one line why no regional op can work (e.g. "PDN stack via pinned at
   strap crossings; move breaks alignment, delete breaks the power stack").
2. Use the MINIMAL delta that satisfies the rule arithmetic.
3. Predict the effect at ALL T placements -- including the ones your previews
   cannot see (other net / other rows). Say explicitly which part of the
   footprint is outside your preview and why the edit is still uniform-safe.

## SG4 What the harness will do with your patch (environment feedback)
- Regional (in-window) ops are gated per-union: window DRC must not regress and
  block connectivity must hold.
- Every def-level / die-spanning candidate is measured by the harness across a
  COVERAGE set of union windows spanning the whole footprint (union-based DRC,
  combined): it is applied ONLY if the combined DRC amount DROPS and
  connectivity is preserved; identical proposals from several unions are
  deduplicated; competing proposals on the same target are settled by the
  measured result (most-negative wins); if every candidate raises the combined
  amount, none is applied.
- These measured verdicts (applied/rejected, with numbers) are fed back into
  the next iteration's skill document. Treat a recorded REJECTED verdict as a
  hard "do not repeat" unless the design state has changed.
<!-- END GATING-DOCTRINE -->

<!-- migrated from repair_skill_v0.md (md5 4c50681f3667b5cf80cd134b67b23d8e) by migrate_seed_v0.py; the doctrine block above is byte-verbatim seed L3-62; the sections below are the v0 seed's meta/conventions (general, not per-rule) -->

## Layer map (verified against the rule deck's input() declarations)

    V0 = layer 18   M1 = layer 19   V1 = layer 21   M2 = layer 20
    V2 = layer 25   M3 = layer 30   V3 = layer 35   M4 = layer 40
    V4 = layer 45   M5 = layer 50   V5 = layer 55   M6 = layer 60

  The NUMERIC layer is authoritative. Note the non-monotonic pair: M2 is
  layer 20 and V1 is layer 21 -- an easy source of mislabeling.
  Via cell contents (each = two metal lands + one cut):
    VIA_VIA12 = M1(19) + M2(20) lands + V1(21) cut
    VIA_VIA23 = M2(20) + M3(30) lands + V2(25) cut
    VIA_VIA34 = M3(30) + M4(40) lands + V3(35) cut
    VIA_VIA45 = M4(40) + M5(50) lands + V4(45) cut
  In THIS repair, all top-level polygon edits were on layers 20/30/40/50
  (M2/M3/M4/M5); ZERO top-level M1 (layer 19) polygons were changed -- the M1
  level was handled entirely by relocating via instances (their own M1 lands
  travel with them).

## How to read the worked examples

All worked examples (A1-A5, B1-B2, C1-C2, D1) come from ONE reference design: a
small block that was repaired from 37 DRC violations to 0 with connectivity
preserved. Every number needed to follow an example (BEFORE/AFTER boxes,
deltas, rule arithmetic) is quoted inline -- no external layout file is needed,
and none is shipped with this skill; do not search for one. One deliberate
exception: in Family A the destination-side merged-M1 context that fixes each
delta's exact magnitude is not reproduced -- those examples teach the
mechanism, and magnitudes must be derived from your own crop's geometry.
Conventions: 1 nm = 4 dbu; polygon boxes are (x1,y1,x2,y2) = lower-left and
upper-right corners in dbu; the shorthand "WxH dbu at (x,y)" anchors (x,y) at
the polygon's lower-left corner; a via instance coordinate is the instance
origin, which for every VIA_* cell coincides with the center of its cut (all
VIA_* cell shapes are symmetric about the origin).
The examples teach DECISION PATTERNS and rule arithmetic; their absolute
coordinates are specific to the reference design. Never copy an example
coordinate into your own repair -- recompute every delta from your crop's own
geometry with the same arithmetic.

## Op selection & verification workflow

### Binding recipe verbs to the patch grammar

Every action in this document maps to the harness op vocabulary as follows:
- "move/shift a polygon"            -> `move` (polygon op)
- "extend one edge of a polygon"    -> `resize_end` (that edge only)
- "reshape/narrow a polygon"        -> `resize` (or two `resize_end` ops)
- "move a via" / "reposition a via" -> `move_instance` on the VIA_* INSTANCE.
  WARNING: NEVER realize a via move in this document as `move_via_shape` or
  `resize_via_shape` -- those rewrite the SHARED cell definition at every
  placement block-wide and are admissible only under the doctrine's 100%
  universality gate. All 33 via repairs here are instance moves.
A submitted patch must be net non-regressing in its window and connectivity-
preserving; keep exploratory candidates inside your preview sandbox, and put
mutually dependent edits (e.g. a stripe move plus its via
co-moves) in ONE atomic patch -- the gate applies patches all-or-nothing.

### Triage: which family?

Given a violation bbox from the DRC report:
1. Check if a VIA_VIA12 instance center or corner lies within or immediately
   adjacent to the bbox. If yes: Family A.
2. M4.AUX.1: the violation bbox IS the full M4 polygon bbox (e.g. 184x184) --
   match it directly. V3.M4.AUX.2: the bbox is VIA-SIZED (72x96, the V3 cut),
   NOT the full M4 -- locate the V3/VIA34 at that bbox, then work on its
   ENCLOSING M4 polygon. Either -> Family B.
3. Check if an M5 polygon's x-edges are involved and the violation bbox spans nearly
   the full M5 y-length. If yes: Family C.
4. Check if the violation marker is a narrow sliver (few dbu wide) between two M4
   polygons at adjacent y-tracks. If yes: Family D.

Violations from multiple families can be present simultaneously. All four families
were active in the example block.

### Recommended repair order

1. Family C (M5.AUX.1): fix first. M5 moves drive VIA45 x-positions, which in
   turn constrain where M4 must be after Family B reshaping.
2. Family B (M4.AUX.1 + V3.M4.AUX.2): fix second. M4 shapes must accommodate
   both the new VIA45 x-positions (from step 1) and the on-grid y-requirements.
   Compute VIA34 and VIA45 deltas in one pass.
3. Family D (M4.S.5): fix third. M4 endpoint extensions are independent of the
   grid fixes and can be applied after M4 shapes are stable.
4. Family A (M1-via cluster): fix last. M1/via edits are independent of M4/M5
   in this block. Fixing them last avoids needing to revisit M1 if M4/M5 changes
   influence shared routing.

### Pre-edit checks (per object)

Before moving a via instance at position P:
- Confirm the target position P_new does not place the via outside its lower or
  upper metal polygon.
- Confirm P_new does not create a new V0.M1.AUX.3 or V1.M1.EN.1 violation.
- If VIA12 and VIA23 are stacked, run the Step 4 anchor check (coupled /
  anchor / partial); never assume co-movement.

Before reshaping an M4 polygon:
- Compute new y_bottom and y_top; verify both are multiples of 96 dbu.
- Verify new y-height = 96 dbu (or the exact V3 cell height from the PDK).
- Verify the new center satisfies center_y mod 192 == 48 (track parity,
  M4.AUX.2) -- the edge grid alone is NOT sufficient; a center at ==144 has
  on-grid edges but sits on an illegal track.
- Verify VIA34 center will still fall within new M4 bbox after repositioning.

Before shifting M5 polygon:
- Verify delta_x against the TRACK residual: with r = x_left mod 192, delta_x
  is -r or +(192 - r), whichever is smaller in magnitude. Both edges then land
  on the 96-dbu grid AND the centerline lands at center_x mod 192 == 48
  (M5.AUX.2; a plain mod-96 snap can pick the illegal 144 phase).
- Verify all associated VIA45 instances will still be inside M5 after co-move.

### Post-edit checks (per family)

After Family A (M1-via):
  Check M1.S.2, M1.S.6 for all M1 polygons within ~200 dbu of the moved objects.
  Check V1.M1.EN.1 and V0.M1.AUX.3 at the new via position.
  Check level coverage: VIA12's M2 land must merge with top-level M2 routing;
  VIA23 must retain BOTH its M2 and M3 coverage at the new position.

After Family B (M4 reshape):
  Check V3.M4.AUX.2: V3 y-extent should equal the new M4 y-height exactly.
  Check M4.AUX.1: y_bottom and y_top must be multiples of 96.
  Check M4.S.* spacing rules between the reshaped M4 and its neighbors.
  Check V4 enclosure on MERGED M4 (top-level + via cell's own land): valid and
  connected around V4; the top-level polygon alone need not contain the via.

After Family C (M5 shift):
  Check M5.AUX.1: x_left and x_right must be multiples of 96.
  Check V4 enclosure: VIA45 must remain inside M5 on all sides.
  Check M5.S.* spacing to neighboring M5 polygons.

After Family D (M4 extension):
  Check M4.S.5: parallel overlap region now >= 176 dbu.
  Check M4.S.1/S.2/S.3/S.4 spacing between the extended polygon and its neighbors.

### Minimal-delta discipline

Apply the smallest delta that clears the violation threshold:
- Family-A via moves: the nonzero x-components ranged from 36 to 136 dbu
  (9-34 nm); A4's move was pure-y (0,+68); auxiliary y nudges can be much
  smaller (+4 dbu at the VIA12 moved (6228,1836) -> (6228,1840); +8 dbu in
  example A5). Moves need not be single-axis: A5's
  (+36,+8) and the VIA12 relocation (5220,3060) -> (5292,2952) = (+72,-108).
  Judge the delta per axis by the rule arithmetic, not by a typical magnitude.
- M5 shift: -88 dbu (22 nm) was the smallest FULL-DECK-legal delta, not merely
  the M5.AUX.1 residual. +8 dbu would also put the edges on the 96 grid, but
  lands the track centerline at 144 mod 192 and surfaces a dormant M5.AUX.2;
  the nearest legal candidates were -88 and +104. "Smallest delta" always means
  smallest among candidates legal under ALL rules, including checks currently
  dormant (cf. the M4 track-parity trap in Family B Step 1).
- M4.S.5: the 172 dbu left-extension ALONE brings the parallel run to exactly
  the 176 dbu threshold (4 dbu original overlap + 172). The neighbor's -68 dbu
  move restores the 160-dbu (40 nm, M4.S.2) same-track spacing to the newly
  extended edge; it does not contribute to the run length.
- The M2 routing extension (worked example A2) was 96 dbu.
Larger deltas increase the probability of creating new violations in adjacent areas.

---

## Reference-design general notes (seed items naming no mappable rule)

From `Final-pair measured facts`:

BEFORE state: 37 DRC violations across 8 rules in the reference design.
AFTER state: 0 violations under the full ASAP7 deck used by this run (332
unique explicit rule names in `asap7.lydrc`, plus 34 additional per-layer
GEOMETRY.NONORTHOGONAL categories disjoint from those names, for 366 total
categories in the DRC report).
Edit scope: 11 polygon moves, 11 polygon reshapes, 33 via instance moves. Zero
objects added or deleted -- an observed property of THIS repair, not a rule:
the full 37->0 repair was achieved without any add or delete, so none of this
design's violations required one. This does NOT put add/delete out of scope in
general: the repair-order doctrine lists guarded `delete_instance` and
top-level polygon `delete` / `add_jog` / `add_polygon` among the REGIONAL ops,
gated like any regional patch (window non-regression, connectivity preserved).
No such need arose here, so that path was never exercised. Via cell
definitions completely untouched.

What these facts prove:

- The 88 dbu M5 misalignment was systematic (identical offset on both M5 polygons),
  not random jitter in only one polygon.

From `Case notes`:

Via cell definitions were untouched IN THIS CASE: the diff shows every via
cell's shape set unchanged -- every repair was an instance move or a
top-level polygon edit. This does NOT mean definitions are immutable in general:
the gating doctrine admits a definition edit only when the motivating rule is at
(=100%) of that definition's placements (see the doctrine's universality test).
No such situation arose here, so the universality analysis was never exercised.

Off-grid root cause pattern: the 88 dbu (22 nm) M5 grid offset is observed on
both changed M5 polygons in the final pair. The ASAP7 M5 vertical routing grid is
24 nm (96 dbu), and the verified correction shifts these two polygons by -88 dbu
in x. From a local crop, snap only the M5 edges you can justify by their own
residual; do not claim block-wide uniformity from one window.


## LAYER INDEX
- M1 -> /work/in/knowledge/M1.md  ops:0  updated:seed
- M2 -> /work/in/knowledge/M2.md  ops:0  updated:seed
- M3 -> /work/in/knowledge/M3.md  ops:1  updated:iter4
- M4 -> /work/in/knowledge/M4.md  ops:2  updated:iter4
- M5 -> /work/in/knowledge/M5.md  ops:2  updated:iter4
- M6 -> /work/in/knowledge/M6.md  ops:2  updated:iter4
- V0 -> /work/in/knowledge/V0.md  ops:0  updated:seed
- V1 -> /work/in/knowledge/V1.md  ops:0  updated:seed
- V2 -> /work/in/knowledge/V2.md  ops:0  updated:seed
- V3 -> /work/in/knowledge/V3.md  ops:1  updated:iter4
- V4 -> /work/in/knowledge/V4.md  ops:1  updated:iter4
- V5 -> /work/in/knowledge/V5.md  ops:2  updated:iter4

## NAVIGATION
1. Map each violation's rule name to its layers: the layer tokens (M*/V*) in the rule name -- at most 2; both appear in the crop's rule descriptions.
2. Read ONLY those layers' knowledge files at the INDEX paths above.
3. No other knowledge discovery: the INDEX paths are the complete navigation.
