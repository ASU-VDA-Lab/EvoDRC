The history and rules are already provided inline. I have exactly one trial: `trial:i01.ug.leaf_0010.07`. I'll write the knowledge section now, making prescriptive claims only where this trial provides direct grounding.

---

## M4 Rule Reference

The following summarizes what each active DRC rule checks. These are factual rule descriptions; prescriptive repair guidance follows in the sections below.

**Width rules (vertical / Y-axis)**

- **M4.W.1** — minimum vertical (Y-direction) width is 24 nm.
- **M4.W.2** — maximum vertical width is 480 nm.
- **M4.W.3** — vertical width must not be an even integer multiple of 24 nm. Forbidden widths: 48, 96, 144, 192, 240, 288, 336, 384, 432, 480 nm.
- **M4.W.4** — vertical widths that cause the polygon to span an even number of minimum-width routing tracks are not allowed. Forbidden widths: 72, 168, 264, 360, 456 nm. Note that these values are already excluded by M4.W.3 (they are all odd multiples of 24 nm that equal an even number of track pitches under the 36 nm track model), so a shape that passes M4.W.3 may still need to be checked explicitly against this list.
- **M4.W.5** — minimum horizontal (X-direction) width is 44 nm.

**Spacing rules**

- **M4.S.1** — minimum vertical spacing between any two M4 polygon edges is 24 nm, measured by projection and by Euclidean distance.
- **M4.S.2** — minimum horizontal spacing between vertical edges of any two M4 polygons is 40 nm.
- **M4.S.3** — tip-to-tip spacing on adjacent tracks where the two shapes do not share a parallel run length: minimum 40 nm.
- **M4.S.4** — tip-to-tip spacing on adjacent tracks where the two shapes do share a parallel run length: minimum 40 nm.
- **M4.S.5** — when two M4 shapes on adjacent tracks have a vertical gap of 24–25 nm and face each other, their parallel run length must be at least 44 nm.

**Grid and topology rules**

- **M4.AUX.1** — every horizontal (Y-constant) edge of M4 must lie on the 24 nm Y-grid (i.e., Y coordinate divisible by 24 nm in database units).
- **M4.AUX.2** — minimum-width M4 tracks (those not surviving a ±13 nm Y-erosion) must have their centerlines at Y positions satisfying `(cl_dbu − 48) mod 192 == 0`, where `cl_dbu` is the centerline in database units.
- **M4.AUX.3** — M4 polygons may not contain any corner whose interior angle is between 0° and 90° (inclusive); M4 routing must remain strictly rectilinear with no bends.
- **M4.AUX.4** — for wide M4 polygons (those surviving a ±13 nm Y-erosion), the outer horizontal edges must not coincide with any routing-track edge derived from the set of narrow (minimum-width) M4 tracks present in the same horizontal band.

**Via enclosure rules**

- **V3.M4.EN.2** — M4 must enclose every V3 via by at least 11 nm on at least two opposite sides.
- **V3.M4.AUX.2** — V3 must be fully inside M4, and the V3 width perpendicular to the M4 length direction must exactly equal the M4 width in that direction (i.e., the via must be flush with both edges of the bar).
- **V4.M4.EN.1** — M4 must enclose every V4 via by at least 11 nm on at least two opposite sides.

**Non-orthogonal geometry**

- **M4.GEOMETRY.NONORTHOGONAL** — all M4 polygon edges must be axis-aligned (0° or 90°). Any edge at an angle between 1° and 89° or 91° and 179° (including negatives) is a violation.

---

## Observed Repair Behavior

**Single confirmed trial: `trial:i01.ug.leaf_0010.07`**

The only measured repair in this layer's history is `trial:i01.ug.leaf_0010.07` (unit `leaf_0010`, iteration 1, channel `unit_gate`). This trial moved six instances using exclusively Y-axis displacements: four instances moved by +72 dbu, two by +24 dbu, and two by −24 dbu (trial:i01.ug.leaf_0010.07). All delta values are exact multiples of 24 dbu. The trial was accepted (`gated_in`) with `conn_preserved = true` and introduced 3 new in-crop violations while producing 0 new out-of-crop violations (trial:i01.ug.leaf_0010.07).

---

## Prescriptive Repair Guidance

**Y-axis moves must use multiples of 24 dbu.**
Every Y-axis instance displacement applied in the one measured repair was a multiple of 24 dbu (trial:i01.ug.leaf_0010.07). This is the minimum step that keeps M4 horizontal edges on the M4.AUX.1 grid. Moves smaller than 24 dbu, or moves that are not integer multiples of 24 dbu, will place horizontal edges off-grid and trigger M4.AUX.1 violations.

**Connectivity preservation is required for acceptance.**
The trial was accepted under the `gated_in` decision because `conn_preserved = true` (trial:i01.ug.leaf_0010.07). A repair that breaks connectivity is not eligible for acceptance regardless of DRC improvement.

**New in-crop violations are tolerated when connectivity is preserved.**
The accepted trial introduced 3 new in-crop DRC violations while keeping `conn_preserved = true` (trial:i01.ug.leaf_0010.07). The scoring function does not require zero new violations inside the crop; net improvement or acceptable trade-off with intact connectivity suffices for `gated_in`.

**Multi-layer coupling: Y moves on M4 also perturb M3, M5, V3, and V4.**
The repair touched layers M3, M4, M5, V3, and V4 simultaneously (trial:i01.ug.leaf_0010.07). Any Y displacement of an instance that carries M4 geometry will co-displace attached vias (V3, V4) and the neighboring metal layers (M3, M5). Via enclosure rules V3.M4.EN.2, V3.M4.AUX.2, and V4.M4.EN.1 must be re-evaluated after every Y move because the via and metal move together, but their enclosure relationship relative to the opposite metal layer (M3 for V3, M5 for V4) changes.