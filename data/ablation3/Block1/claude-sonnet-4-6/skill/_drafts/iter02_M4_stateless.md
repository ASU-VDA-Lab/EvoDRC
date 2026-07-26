Looking at the two measured trial records and the DRC rules, I'll generate the M4 knowledge section body now.

---

## Via-Cell Y-Shrink Resolves V4.M4 and Enclosure Violations

Shrinking the M5 shape in a via cell along the y-axis reduced the total M4-touching violation count by 52 in a single operation (trial:i01.cu.def:VIA_VIA45_1_2_58_58.00). The repair targeted cell `VIA_VIA45_1_2_58_58` with a y-axis delta of −88 dbu applied to the M5 shape; touched layers were M4, M5, and V4. The operation preserved connectivity (`conn_preserved: true`) and was accepted (`decision: applied`).

Apply via-cell y-shrink (reducing the M5 shape extent) when V4.M4.EN.1 or V3.M4.EN.2 enclosure violations cluster inside a single VIA45-family cell: the y-shrink contracts the via landing pad and simultaneously satisfies the 11 nm two-opposite-sides enclosure requirement without introducing new M4 shorts or opens. Do not apply y-shrink beyond what is needed to clear the 11 nm enclosure threshold; the minimum enclosure rules (V3.M4.EN.2 and V4.M4.EN.1) require 11 nm margin on at least two opposite sides, and over-shrink risks violating the remaining enclosure edges.

---

## Batch Instance and Polygon Moves on M4 Tracks

A 57-operation batch combining `move_instance` and `move` (polygon) operations touched M4 among M3, M4, M5, M6, V3, V4, and V5 with zero new M4 violations introduced into crop (trial:i02.ug.whole_design.00). The batch was accepted with decision `gated_in`, reason `conn_preserved`.

Y-axis move deltas in trial:i02.ug.whole_design.00 were predominantly multiples of 24 dbu: values of 24, 48, 72, 96, −24, −48, −72, −96 dbu appeared across the instance moves. This is consistent with M4.AUX.1, which requires M4 horizontal edges to land on a 24 nm grid. Use 24 dbu multiples for y-axis instance and polygon moves to avoid introducing M4.AUX.1 off-grid violations.

A subset of moves in trial:i02.ug.whole_design.00 carried non-24-multiple y-deltas: 16, 32, and −64 dbu (instances i0042, i0176, i0345, i0356, i0493, i0505). These instances were moved by the batch without creating new in-crop M4 violations, indicating that non-24-multiple y-moves are permissible for instances whose M4 shapes do not land on minimum-width routing tracks. Minimum-width M4 tracks must satisfy M4.AUX.2 (centerline at y = 48 + N×192 dbu); moves that leave such tracks off that grid will generate M4.AUX.2 errors. Only move minimum-width M4 polygons in increments that preserve the 192 dbu pitch alignment with 48 dbu offset.

X-axis polygon moves in trial:i02.ug.whole_design.00 used deltas of −16 and +32 dbu on polygons p1142–p1145. No new M4.S.2 or M4.W.5 violations appeared after those moves, confirming that ±16/+32 dbu x-shifts are safe step sizes when the pre-existing horizontal clearance to neighbors is above the 40 nm M4.S.2 minimum and the polygon's own horizontal width exceeds 44 nm (M4.W.5).

---

## Gating Behavior: Connectivity Over Zero-New-Violation Count

The `unit_gate` channel accepted trial:i02.ug.whole_design.00 (`decision: gated_in`) even though 48 new V1.M2.AUX.2 violations were introduced in-crop, because `conn_preserved` was true. The gate does not require zero new cross-layer violations; it requires preserved connectivity. M4 itself contributed zero new violations in that trial. When optimizing M4, cross-layer side-effects on lower-metal AUX rules (such as V1.M2.AUX.2) do not block acceptance through the unit gate provided connectivity is intact.

Do not treat a `gated_in` result as equivalent to `applied`: `gated_in` records a debt of new cross-layer violations that a later iteration must resolve. In trial:i02.ug.whole_design.00 the debt fields show no out-of-crop bounding-box escapes for M4, meaning the 48 new V1.M2.AUX.2 violations remain inside the crop window and are candidates for repair in subsequent iterations.

---

## M4 Width and Spacing Grid Constraints Relevant to Repair Moves

The following constraints are directly load-bearing when sizing or repositioning M4 shapes. All prescriptive guidance below is grounded in observations from trial:i01.cu.def:VIA_VIA45_1_2_58_58.00 and trial:i02.ug.whole_design.00.

**Vertical (y-axis) width:** M4.W.1 sets a 24 nm floor; M4.W.2 sets a 480 nm ceiling. M4.W.3 and M4.W.4 forbid vertical widths that are even-integer multiples of 24 nm (48, 96, 144, 192, 240, 288, 336, 384, 432, 480 nm) and also forbid widths of 72, 168, 264, 360, 456 nm (M4.W.4, the even-track-count set). When the via-cell y-shrink in trial:i01.cu.def:VIA_VIA45_1_2_58_58.00 adjusted M5 by −88 dbu, the resulting M4 landing geometry was accepted without M4.W.3 or M4.W.4 flags, confirming that the repair kept the vertical extent outside the forbidden even-multiple set.

**Horizontal (x-axis) width:** M4.W.5 requires at least 44 nm. The x-polygon moves of −16/+32 dbu in trial:i02.ug.whole_design.00 did not generate M4.W.5 violations, establishing that the pre-existing polygon widths exceeded 44 nm with margin sufficient to absorb those shifts.

**Vertical spacing:** M4.S.1 requires 24 nm minimum vertical spacing (projection metric). **Horizontal spacing:** M4.S.2 requires 40 nm minimum horizontal spacing (euclidian on vertical edges). **Tip-to-tip spacing:** M4.S.3 and M4.S.4 both require 40 nm tip-to-tip spacing between polygons on adjacent tracks, whether or not they share a parallel run length. **Parallel run length:** M4.S.5 requires a minimum parallel run of 44 nm when two M4 polygons are within 24 nm vertically. None of these spacing rules fired as new violations after the moves in trial:i02.ug.whole_design.00, consistent with the batch preserving inter-polygon clearances.

**No bends:** M4.AUX.3 prohibits any corner with angle in the 0°–90° interior range. All M4 shapes must remain strictly rectilinear. The move operations in trial:i02.ug.whole_design.00 translated existing shapes without rotating or reshaping them, which is the correct approach for avoiding M4.AUX.3.

**Wide-polygon track alignment:** M4.AUX.4 prohibits the outside horizontal edge of a wide M4 polygon (one taller than 24 nm after erosion) from touching a routing-track edge. Keep wide M4 polygon boundaries clear of the 192 dbu-pitch routing track lines when repositioning in y.

**Non-orthogonal geometry:** The global GEOMETRY.NONORTHOGONAL rule applies to M4. All move and resize operations must produce axis-aligned (0° or 90°) edges only. The via-cell y-shrink in trial:i01.cu.def:VIA_VIA45_1_2_58_58.00 and all polygon moves in trial:i02.ug.whole_design.00 operated strictly on rectilinear shapes, and no NONORTHOGONAL violations appeared on M4 in either trial.

---

## V3.M4.AUX.2 and V4.M4 Width-Match Constraint

V3.M4.AUX.2 requires each V3 via to be exactly the same width as M4 in the direction perpendicular to the M4 length. When the via-cell y-shrink of trial:i01.cu.def:VIA_VIA45_1_2_58_58.00 reduced M5, the M4 dimension in that cell was implicitly validated as already satisfying the V3.M4.AUX.2 width-match (the trial was accepted without that rule appearing as a new violation). Maintain exact width matching between V3/V4 vias and the underlying M4 polygon in the perpendicular direction whenever resizing M4 in a via cell; any M4 width adjustment that does not propagate identically to the adjacent via shape will introduce a V3.M4.AUX.2 or equivalent AUX violation.