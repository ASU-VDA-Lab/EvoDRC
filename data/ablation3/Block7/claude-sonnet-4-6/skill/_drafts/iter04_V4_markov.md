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

- V4 instance x-delta equals the associated M5 stripe x-delta exactly. In
  trial:i04.ug.whole_design.00, three M5 stripe groups shifted by +32, -16, and
  -64 dbu respectively; every V4 instance associated with each group carried the
  matching x-component verbatim.

- V4 instance y-delta is independent of the M5 x-shift and is always a nonzero
  integer multiple of 24 dbu drawn from {-72, -48, -24, +24, +48, +72, +96}
  when a y-component is present (trial:i04.ug.whole_design.00). A y-delta of 0
  is valid when no M4 y-repositioning is required for that instance.

- V4 instances with dx=0 and dy≠0 exist when the associated M5 stripe undergoes
  no x-shift but M4 y-adjustment still drives a V4 repositioning
  (trial:i04.ug.whole_design.00). These y-only moves are part of the same repair
  batch and must not be omitted.

- A single repair operation can span multiple M5 stripe groups with distinct
  x-deltas simultaneously. trial:i04.ug.whole_design.00 applied 162 ops across
  three x-groups (+32, -16, -64) plus a y-only group in one committed batch with
  conn_preserved=true and zero new violations introduced (n_new_in_crop=0,
  n_new_out_of_crop=0).


## Case notes (reference-design tail evidence)

Anti-pattern AP-2 (atomic stripe batch): an M5 stripe x-shift and ALL V4
instances associated with that shifted stripe must be applied as one complete
batch. The final diff shows two M5 stripes shifted -88 dbu in x, and all seven
repaired V4 instances also take dx=-88. VIA_VIA34 is NOT part of that x-batch
(it keeps x and re-centers in y with the M4 reshape -- see Family B Step 5).
From a local crop, do not submit a partial stripe migration unless the complete
V4 target set for that stripe is known.

Anti-pattern AP-2 generalizes to multi-group batches: trial:i04.ug.whole_design.00
repaired three x-groups and one y-only group simultaneously without violation.
All V4 instances for all affected M5 stripes must be collected before any ops
are submitted; submitting one group while leaving another stripe's V4 population
unrepaired is not valid.

M5 and M4 are tightly coupled: M5.AUX.1 drives M5 x-shift. That shift forces
V4 x-move. V4 x-move forces a top-level M4 x-extent adjustment (to keep the
MERGED M4 valid around V4). M4.AUX.1 independently forces M4 y-move. V4 must
track both, producing combined deltas such as (-88, -48) or (-88, +120).
Compute the x and y components separately, then sum. trial:i04.ug.whole_design.00
confirms this decomposition holds across simultaneous multi-stripe repairs: x
comes from the stripe group, y comes from M4 repositioning, and the components
are summed per instance.