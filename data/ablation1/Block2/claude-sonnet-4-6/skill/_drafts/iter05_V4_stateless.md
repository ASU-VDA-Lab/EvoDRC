## Effective Repair Operations

**Via cell M5 resize is the only applied direct V4 repair in the measured history.** In trial:i04.cu.def:VIA_VIA45_1_2_58_58.00, a `resize_via_shape` on cell `def:VIA_VIA45_1_2_58_58` shrank the M5 shape by 88 dbu on the Y-axis. This reduced total V4 violations by 16 across two units simultaneously (−8 in unit leaf_0002, −8 in unit leaf_0003), with connectivity fully preserved. Because the operation targets the cell definition rather than an instance, one edit propagates to every placed instance of that cell. Use cell-level `resize_via_shape` on M5 when V4.M5.AUX.2 violations are widespread across multiple units sharing the same via cell.

---

## V4.M5.AUX.2: Exact Width Match Perpendicular to M5 Length

V4.M5.AUX.2 requires that V4 share exactly two coincident edge pairs with M5 on the sides perpendicular to M5 routing length — V4 must not be narrower or wider than M5 in that cross-direction. The confirmed repair is to shrink the overwide M5 shape in the via cell definition. In trial:i04.cu.def:VIA_VIA45_1_2_58_58.00, shrinking M5 by 88 dbu on Y within cell `def:VIA_VIA45_1_2_58_58` eliminated 16 violations. Do not widen V4 to match an overwide M5: that would propagate to V4.W.1 and spacing rules. Resize M5 to match the existing V4 extent.

---

## V4.AUX.1: V4 Must Be Inside Both M4 and M5

V4.AUX.1 fires when V4 is not fully contained within the intersection of M4 and M5. The M5 shrink in trial:i04.cu.def:VIA_VIA45_1_2_58_58.00 reduced violations rather than increased them, confirming that the pre-repair condition was M5 overextension (V4.M5.AUX.2), not M5 underextension causing V4.AUX.1. When performing any M5 resize that contracts M5, verify that the post-repair M5 boundary still fully covers V4 on all four sides; otherwise V4.AUX.1 fires on the newly exposed edges.

The polygon p937 X-axis resize in trial:i03.ug.leaf_0002.01 extended an enclosing M4 or M5 shape on both X ends (low end +64 dbu, high end +320 dbu), alongside eight instance moves, and was gated_in with two new in-crop violations. The asymmetric extension — the high-X end required 320 dbu versus 64 dbu on the low-X end — indicates that V4 extended substantially beyond the metal boundary on the high-X side before the repair. When V4.AUX.1 or V4.M4.EN.1 fires on one side only, the required metal extension is directionally asymmetric; do not apply a symmetric resize.

---

## V4.M4.EN.1 and V4.M5.EN.2: Enclosure on Two Opposite Sides

Both rules require at least 11 nm enclosure on two opposite sides of V4 by the enclosing metal (M4 for V4.M4.EN.1, M5 for V4.M5.EN.2). Instance moves along Y address enclosure asymmetries between the top and bottom edges of V4 relative to M4/M5. All four unit-gate trials (trial:i03.ug.leaf_0002.01, trial:i04.ug.leaf_0003.02, trial:i05.ug.leaf_0002.00, trial:i05.ug.leaf_0003.01) use Y-axis displacements in multiples of 24 dbu and all preserve connectivity (conn_preserved: true) with zero out-of-crop violations. Y-axis instance moves at 24-dbu granularity are the measured safe increment for repositioning V4 within its enclosing metal patches without exporting new violations outside the repair locus.

Move magnitudes in the observed range are 24, 48, 72, and 96 dbu (trial:i03.ug.leaf_0002.01 uses all four). Moves are applied in symmetric pairs — when one group of instances moves +72 dbu, a complementary group moves −72 dbu — preserving the relative via pitch and preventing new spacing violations (trial:i03.ug.leaf_0002.01).

---

## V4.S.1, V4.S.2, V4.S.3: Spacing Constraints

All three spacing rules require a 33 nm projection or Euclidean gap between V4 instances. No trial in the measured history records a spacing violation as its explicit repair target, but the symmetric paired instance displacement pattern across all unit-gate trials — moving subsets of instances in opposite Y directions — keeps inter-via pitch constant when vias are redistributed within a unit (trial:i03.ug.leaf_0002.01, trial:i05.ug.leaf_0003.01). Do not apply unpaired or asymmetric Y displacements to a group of vias on the same net without verifying that the resulting projection separation satisfies the 33 nm floor.

---

## M3 Bridge Polygons Suppress New In-Crop Violations During Instance Moves

In trial:i05.ug.leaf_0002.00, five instance moves (Y displacements of −48 to −96 dbu) were paired with three `add_polygon` operations on M3, each at X span [1948, 2308] dbu with Y heights of 48, 96, and 48 dbu respectively. This combination achieved n_new_in_crop = 0 despite touching V3 and V4 across five moved instances. In trial:i05.ug.leaf_0003.01, five comparable instance moves (Y displacements of ±24 dbu, no M3 additions) produced n_new_in_crop = 13, with V4 among the touched layers. When instance moves open M3 routing gaps that break the metal continuity connecting moved vias, adding M3 bridge polygons at the displacement seam prevents the creation of new violations.

---

## Non-Orthogonal Geometry

No GEOMETRY.NONORTHOGONAL violation appears in any history record for V4. Every measured V4-touching operation — instance moves, polygon resizes, via shape resizes, and polygon additions — uses exclusively axis-aligned rectangles and orthogonal edges (trial:i03.ug.leaf_0002.01, trial:i04.ug.leaf_0003.02, trial:i04.cu.def:VIA_VIA45_1_2_58_58.00, trial:i05.ug.leaf_0002.00, trial:i05.ug.leaf_0003.01). Do not introduce non-axis-aligned edges on V4 or its enclosing M4/M5 shapes; the NONORTHOGONAL rule applies to every drawing layer including V4.

---

## Operation Pattern Summary

The single proven applied fix for V4 violations is `resize_via_shape` on M5 within a via cell definition, targeting cell `def:VIA_VIA45_1_2_58_58` (trial:i04.cu.def:VIA_VIA45_1_2_58_58.00). All other V4-touching repairs in the history are unit-gate gated-in trials that reposition instances in Y at 24-dbu increments; these are accepted by the gating channel as connectivity-preserving candidates but have not yet been committed as standalone applied repairs. Use via-cell M5 resizes for V4.M5.AUX.2 violations and paired symmetric Y instance moves at 24-dbu granularity for V4.M4.EN.1/V4.M5.EN.2 enclosure deficiencies; always add M3 bridge polygons when instance displacement exceeds 48 dbu and M3 routes span the moved instances.