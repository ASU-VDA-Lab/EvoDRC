## Final-pair measured facts (reference-design tail evidence)

Provenance: these facts come from the final-pair comparison of the reference
design's initial layout against its repaired final layout, plus the BEFORE and
AFTER DRC reports. Every coordinate and delta cited in this document is quoted
inline from that pair; the layout files themselves are not needed and are not
shipped with this skill.

- M5.AUX.1 is resolved by coordinate snapping (x-shift of the stripe), with the
  M5.AUX.2 track parity (center_x mod 192 == 48) picking the snap direction.
  The M4 grid fixes are NOT mere snapping: they combine y-edge snapping
  (M4.AUX.1), height normalization to the V3 height, track parity (center_y
  mod 192 == 48, M4.AUX.2), and the coupled VIA34/VIA45 moves. No object
  add/delete was needed in either of these cases -- a property of these repairs,
  not a universal rule.


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


## V4 repair patterns (iteration 1 measured records)

**Symmetric V4 x-expansion paired with M5 x-shrink (applied pattern).**
For VIA_VIA45_1_2_58_58 at locus [1728, 2068, 28728, 28172], the winning repair
(trial:i01.cu.def:VIA_VIA45_1_2_58_58.00, decision=applied, delta_total=-156)
used a 5-op atomic batch on V4 and M5: V4 shape 0 was moved -116 dbu in x then
resized +232 dbu in x; V4 shape 1 was moved +116 dbu in x then resized +232 dbu
in x; M5 shape 0 was resized -152 dbu in x. Connectivity was preserved
(conn_preserved=true). The net effect is a symmetric outward expansion of each
V4 shape by 116 dbu on the far edge while M5 contracts in x, satisfying
V4.M5.AUX.2 (V4 width must equal M5 width along the perpendicular direction)
and V4.M5.EN.2 (11 nm enclosure on two opposite sides). Apply all five ops as
one indivisible group ("v45-fix") -- partial application leaves V4.M5.AUX.2
unresolved.

**M5 y-resize alone is insufficient.** The alternative trial
(trial:i01.cu.def:VIA_VIA45_1_2_58_58.01) attempted a single M5 resize of -88
dbu in y. It produced the same window deltas as the winning trial but lost the
tournament. Do not substitute a unidimensional M5 y-shrink for the symmetric
V4 x-expansion plus M5 x-shrink sequence when both produce equal DRC delta
counts; the x-axis batch is the correct structural repair.

**V4 shape moves and resizes are always paired per shape.** In
trial:i01.cu.def:VIA_VIA45_1_2_58_58.00, every V4 move_via_shape is immediately
followed by a resize_via_shape on the same shape_index, with resize magnitude
equal to twice the absolute move magnitude (|delta_resize| = 2 × |delta_move| =
232 = 2 × 116). This is the standard pattern for repositioning one edge of a
V4 shape without displacing the opposite edge: move shifts the entire shape,
resize restores the far edge to its original position while extending the near
edge. Apply this paired move+resize idiom whenever a single V4 edge must be
repositioned in isolation.

**Two-window DRC reduction benchmark.** The applied fix for
VIA_VIA45_1_2_58_58 reduced violations by 81 in unit:leaf_0103 (407 → 326) and
75 in unit:leaf_0104 (385 → 310), totalling 156, as recorded in
trial:i01.cu.def:VIA_VIA45_1_2_58_58.00. A repair touching V4, M5, and M4 in
this cell at this locus that yields fewer than 156 fewer violations is
underperforming relative to the measured baseline.