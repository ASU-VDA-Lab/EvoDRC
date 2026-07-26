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
  (seed, reference-design-verified)


## Case notes (reference-design tail evidence)

Anti-pattern AP-2 (atomic stripe batch): an M5 stripe x-shift and all VIA_VIA45
instances associated with that shifted stripe must be applied as one complete
batch (seed, reference-design-verified). The final diff shows two M5 stripes shifted -88 dbu in x,
and all seven repaired VIA45 instances also take dx=-88. VIA_VIA34 is NOT part of
that x-batch (it keeps x and re-centers in y with the M4 reshape -- see Family B
(-> see M4.md / V3.md) Step 5). From a local crop, do not submit a partial stripe
migration unless the complete VIA45 target set for that stripe is known
(seed, reference-design-verified).

M5 and M4 are tightly coupled: M5.AUX.1 drives M5 x-shift. That shift forces
VIA45 x-move. VIA45 x-move forces a top-level M4 x-extent adjustment (to keep
the MERGED M4 valid around V4). M4.AUX.1 independently forces M4 y-move. VIA45
must track both x and y components separately and then sum them, producing
combined deltas such as (-88, -48) or (-88, +120) (seed, reference-design-verified).


## Iteration 1 measured facts

Trial i01.cu.def:VIA_VIA45_1_2_58_58.01 applied a single `resize_via_shape` op
(axis=y, delta_dbu=-88) to the M5 shape inside cell VIA_VIA45_1_2_58_58, locus
[1728, 2068, 14256, 14132], touching layers M4, M5, and V4. The repair reduced
the total DRC violation count by 52 across two leaf windows (unit:leaf_0034
-26, unit:leaf_0035 -26). Connection preservation was confirmed (conn_preserved=true).

The y-axis resize of the M5 shape within a VIA_VIA45 cell is a valid repair
operation for V4-region violations: trial i01.cu.def:VIA_VIA45_1_2_58_58.01
shows a net DRC reduction of 52 from one such op, with no connectivity loss.
When M5, M4, and V4 layers are all touched by a single via-shape resize, the
enclosure and spacing rules for V4 (V4.M4.EN.1, V4.M5.EN.2, V4.AUX.1,
V4.M5.AUX.2) must all be checked after the resize; trial
i01.cu.def:VIA_VIA45_1_2_58_58.01 confirms that a y-shrink of -88 dbu on M5
within a VIA_VIA45_1_2_58_58 instance satisfies this combined check in its
locus region.