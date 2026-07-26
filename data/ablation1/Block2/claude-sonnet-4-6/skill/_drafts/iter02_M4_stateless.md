## Repair Patterns

**Via replacement with M4 end resize accepted.** In trial:i02.ug.leaf_0001.00, a four-operation repair on locus [4656, 2112, 5760, 3132] was accepted with `conn_preserved=true` and `decision=gated_in`. The repair combined: deleting polygon p1101, deleting via instance i0086, adding a new VIA_VIA12 at origin [5472, 2340], and applying a `resize_end` on polygon p957 (axis x, end low, delta 172 dbu). All touched layers were M1, M2, M4, and V1. When a via instance must be repositioned to satisfy enclosure or alignment rules on M4, pair the via delete-and-reinsert with a coordinated M4 end resize on the same axis as the via relocation (trial:i02.ug.leaf_0001.00).

**Horizontal end resize of 172 dbu (172 nm) on M4 cleared DRC in context.** The `resize_end` on axis x, end low, by 172 dbu was part of a repair set accepted without new violations in trial:i02.ug.leaf_0001.00. A delta of 172 nm on the horizontal axis satisfies M4.W.5 (minimum horizontal width 44 nm) and M4.S.2 (minimum horizontal spacing 40 nm) provided the resulting geometry respects those minimums; the accepted trial confirms this delta did not introduce new horizontal-dimension violations in that context.

## Via Enclosure (V3.M4.EN.2, V4.M4.EN.1)

**Enclosure violations are repaired by moving the via rather than expanding M4 alone.** In trial:i02.ug.leaf_0001.00, the via instance i0086 was deleted and a replacement VIA_VIA12 was inserted at a new origin [5472, 2340], rather than purely growing the M4 polygon. This delete-and-reinsert approach for via repositioning, combined with an M4 end resize, produced a connectivity-preserving accepted result (trial:i02.ug.leaf_0001.00). When V3.M4.EN.2 or V4.M4.EN.1 fires, prefer repositioning the via to a location already enclosed on two opposite sides by existing M4 geometry over expanding M4, especially when M4 expansion would risk violating M4.W.2 (maximum vertical width 480 nm), M4.W.3, or M4.W.4 width-quantization rules.

## Width Rules (M4.W.1 – M4.W.5)

**Vertical width must not equal an even integer multiple of 24 nm (M4.W.3) and must not span an even number of routing tracks (M4.W.4).** No repair in the measured history targeted these rules directly, so no prescriptive resize strategy is grounded yet. Do not introduce vertical width changes without first verifying the result falls outside the forbidden multiples (48, 96, 144, 192, 240, 288, 336, 384, 432, 480 nm for M4.W.3; 72, 168, 264, 360, 456 nm for M4.W.4).

**Horizontal width minimum is 44 nm (M4.W.5).** The accepted horizontal resize in trial:i02.ug.leaf_0001.00 (172 nm delta) left the polygon above this floor. Never resize the low x-end of an M4 polygon inward by an amount that would reduce horizontal extent below 44 nm.

## Spacing Rules (M4.S.1 – M4.S.5)

**Horizontal edge spacing minimum is 40 nm (M4.S.2).** The accepted repair in trial:i02.ug.leaf_0001.00 involved horizontal motion on M4; no M4.S.2 violation was introduced, confirming that a 172 nm inward end-move on x did not close horizontal edge separation below 40 nm in that geometry. When applying any x-axis `resize_end`, verify the resulting horizontal gap to the nearest M4 neighbor edge remains ≥ 40 nm.

**Vertical spacing minimum is 24 nm (M4.S.1).** No vertical spacing violation was introduced in trial:i02.ug.leaf_0001.00. No prescriptive guidance beyond compliance with the 24 nm floor is grounded in the current history.

## Routing Track Alignment (M4.AUX.1, M4.AUX.2)

**M4 horizontal edges must lie on a 24 nm grid (M4.AUX.1).** No M4.AUX.1 violation appeared in trial:i02.ug.leaf_0001.00. Snap all M4 y-coordinates to multiples of 24 nm whenever performing vertical resizes or polygon insertions.

**Minimum-width M4 tracks must center on the horizontal routing grid: pitch 192 nm, offset 48 nm from origin (M4.AUX.2).** No M4.AUX.2 violation appeared in trial:i02.ug.leaf_0001.00. When creating or moving a minimum-width M4 segment (vertical extent < 26 nm after the ±13 nm erosion test in the rule), place its centerline at y = 48 + 192·k (dbu) for integer k.

## No-Bend Constraint (M4.AUX.3)

**M4 may not bend.** M4.AUX.3 forbids any corner with an interior angle between 0° and 90°. No bend violations appeared in trial:i02.ug.leaf_0001.00. Do not introduce L-shaped or non-rectilinear M4 polygons; keep all M4 shapes as axis-aligned rectangles. The resize_end operation applied in trial:i02.ug.leaf_0001.00 adjusted one end of a rectangle without introducing bends, which is the correct geometry class for M4 repairs.

## Wide M4 / Routing Track Edge Constraint (M4.AUX.4)

**A wide M4 polygon's horizontal edge may not touch a minimum-width routing track edge (M4.AUX.4).** No M4.AUX.4 violation appeared in trial:i02.ug.leaf_0001.00. When inserting or resizing wide M4 polygons (those that survive the ±13 nm vertical erosion test in the rule), ensure their horizontal edges do not fall on the centerlines of minimum-width M4 routing tracks in the same horizontal band.

## General Repair Strategy

**Coordinate multi-layer repairs atomically.** The only accepted repair in the measured history (trial:i02.ug.leaf_0001.00) touched four layers (M1, M2, M4, V1) in a single committed set of four operations. Isolated single-layer edits were not used. When an M4 DRC violation co-occurs with a via misplacement, bundle the via delete, via reinsert, and M4 resize into one atomic repair set to preserve connectivity (trial:i02.ug.leaf_0001.00).