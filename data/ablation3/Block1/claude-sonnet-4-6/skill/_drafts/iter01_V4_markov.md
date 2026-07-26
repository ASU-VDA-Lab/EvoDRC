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

- A y-axis resize_via_shape on a VIA_VIA45 instance (delta_dbu=-88 in y, layer_name=M5)
  reduced total V4-touching DRC violations by 52 (244 -> 192) while preserving
  connectivity (trial:i01.cu.def:VIA_VIA45_1_2_58_58.00). Touched layers were M4,
  M5, and V4, confirming that reshaping the M5 extent of a VIA_VIA45 cell directly
  exercises V4.M4.EN.1, V4.M5.EN.2, and V4.AUX.1 / V4.M5.AUX.2 checks
  simultaneously.


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

A pure y-axis resize on VIA_VIA45 (no x component) is a valid standalone repair
when only the M5 y-extent of the via cell is misaligned: trial:i01.cu.def:VIA_VIA45_1_2_58_58.00
applied delta_dbu=-88 in y with n_ops=1 and achieved a net -52 violation reduction
while keeping connectivity intact. This confirms that x and y corrections are
decomposable -- a y-only resize need not be bundled with an x-shift when no stripe
x-migration is in progress.