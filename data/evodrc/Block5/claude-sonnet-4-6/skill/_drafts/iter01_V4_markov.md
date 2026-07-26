(seed, reference-design-verified)
<!-- migrated from repair_skill_v0.md (md5 4c50681f3667b5cf80cd134b67b23d8e) by migrate_seed_v0.py; family slice(s): none (tail evidence only) -->


## Final-pair measured facts (reference-design tail evidence)

Provenance: these facts come from the final-pair comparison of the reference
design's initial layout against its repaired final layout, plus the BEFORE and
AFTER DRC reports. Every coordinate and delta cited in this document is quoted
inline from that pair; the layout files themselves are not needed and are not
shipped with this skill.

- M5.AUX.1 is resolved by coordinate snapping (x-shift of the stripe), with the
  M5.AUX.2 track parity (center_x mod 192 == 48) picking the snap direction.
  The M4 grid fixes are NOT mere snapping: they combine y-edge snapping
  (M4.AUX.1), height
  normalization to the V3 height, track parity (center_y mod 192 == 48,
  M4.AUX.2), and the coupled VIA34/VIA45 moves. No object add/delete was needed
  in either of these cases -- a property of these repairs, not a universal
  rule.


## Case notes (reference-design tail evidence)

Anti-pattern AP-2 (atomic stripe batch): an M5 stripe x-shift and ALL VIA_VIA45
instances associated with that shifted stripe must be applied as one complete
batch. The final diff shows two M5 stripes shifted -88 dbu in x, and all seven
repaired VIA45 instances also take dx=-88. VIA_VIA34 is NOT part of that x-batch
(it keeps x and re-centers in y with the M4 reshape -- see Family B (-> see M4.md / V3.md) Step 5).
From a local crop, do not submit a partial stripe migration unless the complete
VIA45 target set for that stripe is known.

M5 and M4 are tightly coupled: M5.AUX.1 drives M5 x-shift. That shift forces
VIA45 x-move. VIA45 x-move forces a top-level M4 x-extent adjustment (to keep
the MERGED M4 valid around V4). M4.AUX.1 independently forces M4 y-move. VIA45
must track both, producing combined deltas such as (-88, -48) or (-88, +120).
Compute the x and y components separately, then sum.


## Iteration 1 measured facts (trial:i01.ug.leaf_0010.07)

Trial i01.ug.leaf_0010.07 (Block5, unit_gate, locus [1728,3148,9072,7652], design state ef66d47d) produced a 6-op pure-y repair touching layers M3, M4, M5, V3, V4 with connectivity preserved and decision gated_in.

**V4 repairs are not always x-driven.** The seed evidence established x-shifts as the primary V4 delta (from M5 stripe migration). Trial:i01.ug.leaf_0010.07 shows a repair in which all six move_instance ops carry dx=0; the entire correction is in y. Do not assume dx!=0 when diagnosing V4 violations -- y-only repairs are a confirmed repair shape.

**Multi-instance V4 repairs use heterogeneous y-deltas within one batch.** In trial:i01.ug.leaf_0010.07 the six ops split into three delta magnitudes: two instances at +72 dbu, two at +24 dbu, and two at -24 dbu. All six are applied in the same atomic batch (n_ops=6, single trial). Do not reduce a multi-instance V4 repair to a uniform delta; resolve each instance's delta independently before committing the batch.

**V4 y-repair spans the full M3-M5 stack.** Touched layers for trial:i01.ug.leaf_0010.07 are M3, M4, M5, V3, V4 -- no layer in that range is skipped. When a V4 y-move is required, compute whether the enclosing M4 and M5 geometry must also shift (V4.AUX.1 requires V4 inside both M4 and M5; V4.M4.EN.1 and V4.M5.EN.2 require 11 nm enclosure on opposite sides). The M3/V3 involvement confirms the correction propagates downward through the stack as well.

**n_new_in_crop=3 with n_new_out_of_crop=0 is a gated_in acceptance criterion.** Trial:i01.ug.leaf_0010.07 was accepted (decision=gated_in) despite introducing 3 new violations inside the crop window, because all 3 are contained within the crop (n_new_out_of_crop=0) and connectivity is preserved. Do not reject a repair solely because in-crop violation count rises; gate on out-of-crop count and connectivity preservation.