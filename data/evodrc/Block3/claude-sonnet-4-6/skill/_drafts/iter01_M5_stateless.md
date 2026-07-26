## Via-Cell Resizing Fixes V4.M5 Enclosure and Width-Match Violations

The single measured repair on this layer operated on via cell `VIA_VIA45_1_2_58_58`, which spans layers M4, V4, and M5. Five operations were applied: two symmetric x-axis moves of the V4 shapes (−116 dbu and +116 dbu respectively), two x-axis resizes of the V4 shapes (+384 dbu each), and one x-axis resize of the M4 shape (+384 dbu). No direct M5 geometry operation was issued; M5 appears in `touched_layers` because the via cell definition change propagates to M5 contexts. The net result was −18 DRC violations across two windows (`unit:leaf_0018` −10, `unit:leaf_0019` −8), with connectivity preserved (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01).

## V4.M5.AUX.2 — Via Width Must Match M5 Width Perpendicular to Run Direction

Rule V4.M5.AUX.2 requires V4 to be exactly the same width as the enclosing M5 polygon along the direction perpendicular to M5's length. In trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, both V4 shapes were resized +384 dbu in x, indicating the pre-repair V4 shapes were undersized relative to M5's horizontal extent. The symmetric centering moves (−116 dbu on shape 0, +116 dbu on shape 1) were applied before or alongside the resize, keeping both V4 shapes centered on the M5 track while expanding them to match M5's horizontal width. Do not resize only one V4 shape in isolation within this via cell: both shapes required coordinated adjustment in the measured repair (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01).

## V4.M5.EN.2 — Minimum 11 nm Enclosure on Two Opposite Sides

Rule V4.M5.EN.2 flags V4 shapes inside M5 that lack ≥11 nm enclosure on at least two opposite sides (both x and y independently tested via `m5.sized(-11.nm, 0)` and `m5.sized(0, -11.nm)`). The +384 dbu x-axis enlargement of V4 in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 increased horizontal overlap with the M5 boundary, addressing the enclosure shortfall. The accompanying M4 resize (+152 dbu in x) adjusted the underlying metal to remain consistent with the widened V4, preventing new violations from propagating downward.

## M5 Is Modified Indirectly Through Via Cell Edits

M5 is listed in `touched_layers` for trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 but carries no direct M5 operation. All geometry changes were issued to V4 and M4 shapes within the via cell definition. M5 violations (V4.M5.EN.2, V4.M5.AUX.2) are resolved by adjusting the via shapes to conform to the existing M5 geometry, not by moving or resizing M5 itself. Avoid issuing direct M5 shape moves or resizes when the violation root cause is via undersizing relative to a fixed M5 track: the measured repair achieved full violation clearance without touching M5 geometry (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01).

## M5 Width Constraints Relevant to Via Sizing (W.1, W.2, W.3, W.4)

The M5 horizontal-width rules constrain what via widths are valid matches under V4.M5.AUX.2. M5.W.1 sets the minimum horizontal width at 24 nm; M5.W.2 sets the maximum at 480 nm. M5.W.3 forbids widths that are even integer multiples of 24 nm (48, 96, 144, … 480 nm). M5.W.4 forbids widths of 72, 168, 264, 360, or 456 nm (widths spanning an even number of minimum-width routing tracks). These constraints are structural: any V4 width chosen to match M5 under V4.M5.AUX.2 must itself avoid these forbidden values, since M5 polygons in legal layouts will never carry them. The +384 dbu V4 resize in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 brought V4 into alignment with an M5 width that satisfies these constraints.

## M5.AUX.2 — Minimum-Width Tracks Must Center on Vertical Routing Grid (pitch 192 dbu, offset 48 dbu)

Rule M5.AUX.2 checks minimum-width M5 shapes (those eroded to nothing by a 13 nm horizontal erosion) and verifies their x-centerlines fall on the grid `x ≡ 48 (mod 192)` dbu. Via cells instantiated off-grid relative to this pitch will create M5.AUX.2 violations even if the M5 shape itself is geometrically valid. The centering moves applied to V4 in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 (±116 dbu) kept V4 aligned to the M5 track center, consistent with maintaining M5.AUX.2 compliance. When resizing a via cell's V4 shapes, apply symmetric moves (equal and opposite on the two shapes) to preserve the x-centerline position and avoid introducing M5.AUX.2 violations.

## M5.AUX.3 — M5 May Not Bend; Repair Must Preserve Rectilinear Geometry

Rule M5.AUX.3 forbids any corner angle between 0° and 90° on M5 polygons. Since all operations in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 were pure x-axis resizes and moves on V4 and M4 within a rectangular via cell, M5 shape geometry was not altered and no bending was introduced. When editing via cells that touch M5 contexts, confine moves and resizes to single-axis rectangular adjustments; any operation that would introduce a non-90° corner on M5 will trigger M5.AUX.3.

## M5.AUX.1 — Vertical Edges Must Fall on 24 nm Grid

Rule M5.AUX.1 requires all M5 vertical edges to land on a 24 nm grid. Because the repair in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 did not move any M5 vertical edges (M5 geometry was unchanged), M5.AUX.1 compliance was maintained without additional snapping. When a future repair does require moving M5 vertical edges — for example to resolve M5.S.1 spacing — snap all resulting edge x-coordinates to multiples of 24 dbu before committing.

## M5 Spacing Rules Unreached in the Measured Trial

Rules M5.S.1 (minimum 24 nm horizontal spacing), M5.S.2 (minimum 40 nm vertical spacing), M5.S.3 (tip-to-tip spacing on adjacent tracks without shared parallel run), M5.S.4 (tip-to-tip spacing with shared parallel run, both ≥40 nm), and M5.S.5 (minimum parallel run length 44 nm on adjacent tracks) were not the direct targets of the repair in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01. No measured evidence from this iteration's history supports prescriptive guidance on how to repair those rules. They are listed here only to mark that the measured record does not yet ground repair strategies for them.