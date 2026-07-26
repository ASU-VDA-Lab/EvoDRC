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

Anti-pattern AP-2 (atomic stripe batch): an M5 stripe x-shift and all VIA_VIA45
instances associated with that shifted stripe must be applied as one complete
batch (reference-design-verified). The final diff shows two M5 stripes shifted -88 dbu in x,
and all seven repaired VIA45 instances also take dx=-88. VIA_VIA34 is NOT part
of that x-batch (it keeps x and re-centers in y with the M4 reshape -- see
Family B (-> see M4.md / V3.md) Step 5). From a local crop, do not submit a
partial stripe migration unless the complete VIA45 target set for that stripe is
known (reference-design-verified).

M5 and M4 are tightly coupled (reference-design-verified): M5.AUX.1 drives M5
x-shift. That shift forces VIA45 x-move. VIA45 x-move forces a top-level M4
x-extent adjustment (to keep the MERGED M4 valid around V4). M4.AUX.1
independently forces M4 y-move. VIA45 must track both, producing combined deltas
such as (-88, -48) or (-88, +120) (reference-design-verified). Compute the x and y
components separately, then sum.


## Iteration 1 measured facts

trial:i01.ug.whole_design.00 (Block5, unit_gate channel, whole_design locus
0,0,10784,10784, 19 ops, design state ef66d47d) touched V4 in a batch spanning
M1 M2 M3 M4 M5 V1 V2 V3 V4 and achieved conn_preserved=true. The 19 ops
include 14 move_instance operations with mixed-axis deltas (dx values: +136,
-28, +8; dy values: +72, -48, +24, +96, -24, +48), two polygon resize_end
operations (p879: y-high +48; p910: y-high +20), one polygon move (p910: x +8),
and two instance moves that accompany the polygon shift (i0061, i0104: dx=+8).
A repair batch spanning all metal and via layers 1 through 5 with independent
x and y component adjustments applied together preserves connectivity when
structured this way (trial:i01.ug.whole_design.00).