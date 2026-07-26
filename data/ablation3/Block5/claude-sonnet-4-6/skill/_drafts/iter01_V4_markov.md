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


## Iteration 1 measured facts

Provenance: trial i01.ug.whole_design.00 (Block5, channel unit_gate, design state ef66d47d).

**Multi-layer batches including V4 are accepted when connectivity is preserved.**
trial:i01.ug.whole_design.00 produced 19 ops touching M1, M2, M3, M4, M5, V1, V2, V3, V4 in a single batch; the decision was gated_in with conn_preserved=true and zero new violations (n_new_in_crop=0, n_new_out_of_crop=0). Do not decompose a V4-inclusive repair into layer-isolated sub-batches when the instances form a coupled stack -- trial:i01.ug.whole_design.00 confirms whole-design batches pass intact.

**V4 y-moves in the accepted batch are multiples of 24 dbu.**
In trial:i01.ug.whole_design.00 the instance y-deltas are +72, +72, -48, -48, +24, +24, +96, +96, -24, -24, +48, +48 dbu -- every value divisible by 24. Do not apply fractional or non-24-aligned y-moves to V4 stacks; all accepted evidence uses 24-dbu granularity.

**Paired instance moves indicate coupled via-stack repositioning.**
In trial:i01.ug.whole_design.00 each non-zero y-delta appears exactly twice (two instances per delta value), consistent with two via instances per routing track moving together. Move V4 instances in matched pairs when they share a routing track; moving one without the other was not observed in any accepted trial.

**x-moves for V4-adjacent instances co-occur with polygon reshape on the same axis.**
In trial:i01.ug.whole_design.00, instances i0061 and i0104 take dx=+8; polygon p910 simultaneously takes a move of +8 on x and a resize_end of +20 on the y-high edge. This confirms the pattern from the reference-design tail: a V4 x-shift must be accompanied by a containing M4 or M5 polygon reshape to maintain V4.M4.EN.1 and V4.M5.EN.2 enclosure -- trial:i01.ug.whole_design.00 shows dx=+8 dbu paired with x-polygon-move of +8 and y-high resize of +20.

**Polygon p879 receives a y-high resize of +48 dbu independent of any x-move.**
trial:i01.ug.whole_design.00 shows resize_end on p879 (axis y, end high, delta +48) with no associated x-shift on that polygon. This confirms that enclosure corrections along y can be applied as standalone resize_end operations without requiring an x-component when V4 is shifted only in y.