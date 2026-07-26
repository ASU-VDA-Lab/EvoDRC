**V4.M5.AUX.2: Fix by shrinking M5 y-dimension to match V4 width**

V4.M5.AUX.2 fires when the M5 shape inside a via cell is wider in the direction perpendicular to M5 routing than the V4 shape it encloses. The confirmed repair is a negative y-axis resize of the M5 via shape to align it with the V4 footprint. A resize of -88 dbu on the M5 shape (shape_index 0) inside VIA_VIA45_1_2_58_58 eliminated 56 violations across two windows and was accepted (trial:i01.cu.def:VIA_VIA45_1_2_58_58.00). Do not attempt to fix V4.M5.AUX.2 by expanding V4 or moving the via cell; the M5 y-shrink to match the existing V4 width is the decisive operation.

**M5 horizontal spacing fixes in via cells: paired asymmetric polygon moves plus via-shape x-shrink**

When M5 routing polygons adjacent to a via cell violate horizontal spacing (M5.S.1 or M5.W rules), the repair pattern that was applied combines asymmetric x-moves on the two flanking M5 polygons with a simultaneous x-shrink of the M5 via shapes. Specifically: one polygon moved +32 dbu, the other -16 dbu on the x-axis, and both M5 via shapes (VIA_VIA45_1_2_58_58 shape_index 0 and VIA_VIA56_2_2_66_58 shape_index 0) were resized by -64 dbu on x, reducing the total violation count by 2 (trial:i05.cu.def:VIA_VIA45_1_2_58_58.00). The asymmetry (32 vs 16 dbu moves) reflects the differing slack available on each side; do not assume symmetric adjustment is required.

**V5/M6 via shape resizing touches M5 indirectly; y-axis grow outperforms x-axis move-and-expand**

Fixes to V5 shapes in VIA_VIA56_2_2_66_58 carry M5 as a touched layer. When two competing strategies were trialed — x-axis move-and-resize of all four V5 shapes (trial:i01.cu.def:VIA_VIA56_2_2_66_58.01) versus y-axis resize of all four V5 shapes by +248 dbu each (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02) — the y-axis grow was applied (-32 delta) and the x-axis strategy lost the tournament (-16 delta). When resolving V5.M5.EN.1 violations or V5/M6 AUX.2 mismatches that propagate M5 violations, prefer y-axis resizing of V5 over x-axis repositioning.

**Unit gate instance moves involve M5 but do not directly target M5 DRC rules**

Bulk instance placements in the unit_gate channel (trial:i04.ug.leaf_0003.01, trial:i05.ug.leaf_0003.01) list M5 as a touched layer because moved cells contain M5 geometry. The violations closed by these moves were M1.A.1, M4.W.5, and V1.M1.EN.1 (trial:i05.ug.leaf_0003.01, assemble_drops context) — none are M5 rules. Do not interpret unit_gate M5 touch as evidence that instance placement resolves M5-specific DRC violations.

**cu_pool M5 ops are not re-applied by unit_gate: assemble_drops prevents double-application**

When cu_pool applies M5 fixes (trial:i05.cu.def:VIA_VIA45_1_2_58_58.00), the same operations appear in assemble_drops for the subsequent unit_gate pass (trial:i05.ug.leaf_0003.01) with reason cu_pool:applied. The four M5 ops — moving p1683 +32 dbu and p1682 -16 dbu on x, plus shrinking VIA_VIA45_1_2_58_58 and VIA_VIA56_2_2_66_58 M5 shapes by -64 dbu on x — are dropped rather than re-executed. Do not schedule M5 polygon or via-shape adjustments in unit_gate if the identical operations have already been committed through cu_pool in the same iteration.

**M5.AUX.2: minimum-width M5 tracks must center on vertical routing grid**

M5.AUX.2 requires that 1x-width M5 tracks (those not surviving a ±13 dbu erosion) have their x-centerlines on the grid defined by pitch 192 dbu with offset 48 dbu. No repair of M5.AUX.2 appears directly in the history, but trial:i05.cu.def:VIA_VIA45_1_2_58_58.00 moves M5 polygons by +32 and -16 dbu on x, values that are multiples of 8 dbu (the finest measured step) but not of 24 dbu; confirm post-move that adjusted polygon centerlines remain on the 192 dbu pitch grid at offset 48 dbu relative to origin before committing horizontal M5 shifts.

**M5.AUX.3: M5 may not bend — avoid any operation that would create a non-rectilinear M5 polygon**

M5.AUX.3 rejects M5 polygons with corners whose interior angle crosses 90 degrees (a bend). No bend-inducing operation appears in the history; all applied M5 ops are axis-aligned resizes and moves of rectangular shapes. When resizing M5 via shapes or moving M5 polygons, ensure the resulting shape remains a simple rectilinear rectangle. Partial-edge resizes that shift only one side of a via shape (as in trial:i01.cu.def:VIA_VIA45_1_2_58_58.00, y-axis resize, and trial:i05.cu.def:VIA_VIA45_1_2_58_58.00, x-axis resize) preserve rectangular geometry and are safe under M5.AUX.3.

**M5.W.3 / M5.W.4: avoid widths that are even multiples of 24 dbu or span even track counts**

M5.W.3 forbids horizontal widths of 48, 96, 144, 192, 240, 288, 336, 384, 432, or 480 dbu. M5.W.4 forbids widths that correspond to spanning an even number of routing tracks (72, 168, 264, 360, 456 dbu). The x-axis M5 via shape resize of -64 dbu applied in trial:i05.cu.def:VIA_VIA45_1_2_58_58.00 reduces width; verify that the resulting width does not land on any M5.W.3 or M5.W.4 forbidden value. The -88 dbu y-axis resize in trial:i01.cu.def:VIA_VIA45_1_2_58_58.00 targets vertical (y-axis) width, which is governed by M5.W.5 (minimum 44 dbu); that resize was accepted, confirming the resulting vertical width remained above 44 dbu.