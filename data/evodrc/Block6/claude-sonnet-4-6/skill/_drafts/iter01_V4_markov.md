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
(it keeps x and re-centers in y with the M4 reshape -- see Family B (-> see M4.md / V3.md) Step 5).
From a local crop, do not submit a partial stripe migration unless the complete
VIA45 target set for that stripe is known.

M5 and M4 are tightly coupled: M5.AUX.1 drives M5 x-shift. That shift forces
VIA45 x-move. VIA45 x-move forces a top-level M4 x-extent adjustment (to keep
the MERGED M4 valid around V4). M4.AUX.1 independently forces M4 y-move. VIA45
must track both, producing combined deltas such as (-88, -48) or (-88, +120).
Compute the x and y components separately, then sum.


## Iteration 1 measured facts (cu_pool channel, Block6)

**Dual-V4-shape symmetric expansion pattern.**
In cell `VIA_VIA45_1_2_58_58`, two V4 shapes were repaired by moving them in
opposite x directions (shape\_0: dx=-116 dbu, shape\_1: dx=+116 dbu) while
simultaneously resizing both by +384 dbu in x, and resizing the M4 shape by
+152 dbu in x (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01). This 5-op batch
reduced violations by 52 across windows `unit:leaf_0019` (-28) and
`unit:leaf_0020` (-24), and conn\_preserved=true confirms connectivity is
maintained through this expansion sequence. Do not split the V4 move ops from
the V4 resize ops or the M4 resize op; the full 5-op set must apply atomically.

**M4 resize accompanies V4 x-expansion.**
When V4 shapes inside a VIA_VIA45 cell are expanded in x (resize +384 dbu per
shape, trial:i01.cu.def:VIA_VIA45_1_2_58_58.01), M4 must also be resized in x
(+152 dbu on shape\_0 in the same trial) to maintain V4.M4.EN.1 enclosure on
both opposite sides. The M4 resize delta is not equal to the V4 resize delta;
compute it independently from the resulting enclosure gap on each side.

**Opposite-direction V4 moves center the expansion.**
The ±116 dbu symmetric x-move (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01) keeps
the V4 shape pair geometrically centered while satisfying V4.M5.AUX.2 (V4 width
must match M5 width perpendicular to M5 length) and V4.W.1 (minimum width
24 nm). Apply the two V4 moves with equal magnitude and opposite sign; asymmetric
moves risk re-introducing V4.M5.AUX.2 violations.