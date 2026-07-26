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

## LAYER INDEX
- M1 -> /work/in/knowledge/M1.md  ops:10  updated:iter4
- M2 -> /work/in/knowledge/M2.md  ops:13  updated:iter4
- M3 -> /work/in/knowledge/M3.md  ops:3  updated:iter4
- M4 -> /work/in/knowledge/M4.md  ops:4  updated:iter4
- M5 -> /work/in/knowledge/M5.md  ops:5  updated:iter4
- M6 -> /work/in/knowledge/M6.md  ops:0  updated:seed
- V0 -> /work/in/knowledge/V0.md  ops:0  updated:seed
- V1 -> /work/in/knowledge/V1.md  ops:10  updated:iter4
- V2 -> /work/in/knowledge/V2.md  ops:2  updated:iter4
- V3 -> /work/in/knowledge/V3.md  ops:2  updated:iter4
- V4 -> /work/in/knowledge/V4.md  ops:3  updated:iter4
- V5 -> /work/in/knowledge/V5.md  ops:0  updated:seed

## NAVIGATION
1. Map each violation's rule name to its layers: the layer tokens (M*/V*) in the rule name -- at most 2; both appear in the crop's rule descriptions.
2. Read ONLY those layers' knowledge files at the INDEX paths above.
3. No other knowledge discovery: the INDEX paths are the complete navigation.
