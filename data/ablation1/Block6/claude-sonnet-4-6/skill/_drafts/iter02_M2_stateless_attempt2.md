## Operation outcomes and gate decisions

All seventeen trials touching M2 across iterations 1–2 were accepted by the connectivity gate (conn_preserved=true). Fourteen of those produced zero new in-crop violations on M2 or any other layer. Three trials introduced new violations yet were still accepted because connectivity was preserved: trial:i02.ug.leaf_0004.03 (1 new M2.S.2), trial:i02.ug.leaf_0010.07 (1 new M2.S.4 and 1 new M2.S.7, plus violations on other layers), and one via-pool attempt was rejected outright on net-positive grounds: trial:i02.cu.def:VIA_VIA23_1_3_36_36.00 (delta=0, no improvement).

## Move magnitudes and safe x-axis step sizes

Horizontal-only single-instance moves in the range +4 to +104 dbu were consistently clean across both iterations. trial:i01.ug.leaf_0001.05 (+4 dbu), trial:i01.ug.leaf_0011.06 (+36 dbu), trial:i01.ug.leaf_0018.08 (+36 dbu), trial:i02.ug.leaf_0001.01 (+104 dbu), and trial:i02.ug.leaf_0005.04 (+104 dbu) all produced zero new M2 violations. Multi-instance horizontal moves were equally clean when all moves were axis-aligned and the full set of conflicting moves was retained: trial:i01.ug.Block6_union_row4.01 (+36 and +4 dbu), trial:i02.ug.Block6_union_row7.00 (+96 and +36 dbu). These results establish that pure x-axis displacement in grid steps up to at least 104 dbu does not by itself create M2 width, spacing, or tip violations.

## Grouped move-plus-resize operations

Combining a move_instance with a resize_end on the same polygon within a single trial is demonstrated safe when the two operations share a group tag and operate on the same axis. trial:i02.ug.leaf_0008.05 moved i0213 by +28 dbu in x and simultaneously extended polygon p1923 high-x end by +28 dbu (group "v0042_i0213_p1923"), producing zero new M2 violations. The same pattern appeared at larger magnitude in trial:i01.ug.leaf_0015.07 (move +28 dbu, resize_end +48 dbu on p1923 high-x) and in trial:i02.ug.leaf_0003.02 (move +104 dbu, resize_end +128 dbu on p2020 high-x), both clean. When a polygon must be stretched to follow an instance, the resize_end should target the same edge direction as the move displacement; all three successful cases used the high-x end for a positive-x move.

## M2.S.1 (side-to-side spacing, 18 nm)

No trial produced a new M2.S.1 violation. The consistent absence across 17 diverse operation sets, including large lateral moves and polygon stretches, indicates that the side-to-side spacing margin is generally not the binding constraint in this design context.

## M2.S.2 (tip-to-side spacing, 25 nm)

One new M2.S.2 violation was introduced in trial:i02.ug.leaf_0004.03. That trial applied a diagonal move to i0015 (+36 dbu in x, -48 dbu in y), combined with two further instance moves. Critically, the assemble stage dropped a conflicting op for i0015 that had been claimed simultaneously by leaf_0004 and leaf_0010, leaving the geometry in a partially resolved state. The resulting new M2.S.2 count of 1 indicates that diagonal displacement (non-zero delta on both x and y simultaneously) can close the tip-to-side gap when one polygon's tip approaches a neighboring polygon's long side after the move. Avoid combined x+y displacement for a single instance when a dropped-conflict flag is present in assemble_drops; the incomplete resolution leaves nearby M2 tips without their expected clearance from the long-edge neighbor (trial:i02.ug.leaf_0004.03).

## M2.S.3 and M2.S.5 (wide-tip-to-tip and wide/narrow-tip spacing)

No trials produced new M2.S.3 or M2.S.5 violations. These rules activate only when both tip edges fall in the 24–36 nm range (M2.S.3) or one tip is in that range and the other is narrower (M2.S.5). The absence of violations across both iterations is consistent with the design using tip geometries that do not frequently fall in this intermediate range.

## M2.S.4 (narrow tip-to-tip spacing, 31 nm, both tips < 24 nm)

One new M2.S.4 violation was introduced in trial:i02.ug.leaf_0010.07, alongside one new M2.S.7 and 75 additional violations on other layers (M1.A.1, V1.M1.EN.1, V1.S.2). That trial operated on five instances across a very large locus (1728,3148 to 15336,14608), including a y-axis move of -40 dbu for i0015 and i0471 and three further x-axis adjustments. An assemble_drop conflict was present: a y=-40 move for i0015 had been dropped from the leaf_0004 trial and was instead applied here via leaf_0010. The co-occurrence of M2.S.4 and M2.S.7 in the same trial suggests that a y-axis displacement of -40 dbu (approximately 2 grid steps in the y pitch) brought narrow M2 tips into mutual proximity at the 31 nm threshold. Do not apply y-axis displacements to instances whose M2 tips were near the 31 nm limit, particularly when those instances have been subject to prior dropped-conflict ops (trial:i02.ug.leaf_0010.07).

## M2.S.6 (corner-to-corner spacing, 20 nm)

No trial produced a new M2.S.6 violation. The euclidian corner check is more permissive than the projection-based spacing rules in most rectilinear configurations, and none of the move or resize operations in the history closed corners below 20 nm.

## M2.S.7 (18 nm tip-to-tip co-located with ≤32 nm side spacing)

One new M2.S.7 violation was introduced in trial:i02.ug.leaf_0010.07, co-occurring with M2.S.4. M2.S.7 fires when a near-tip gap of approximately 18 nm (vertical edge spacing just above the 18 nm threshold) coincides with a short parallel run where the side-to-side spacing is ≤32 nm. The co-violation with M2.S.4 (both edges < 24 nm) in the same trial confirms that the y-axis shift of -40 dbu compressed a tip region where the bounding side wires were already within the 32 nm proximity window. When the side-to-side spacing between adjacent M2 tracks is known to be ≤32 nm, any y-axis displacement that shortens the parallel run length below 35 nm or introduces an 18 nm tip gap in that corridor violates M2.S.7. Avoid y-axis moves for instances in dense side-spacing corridors (trial:i02.ug.leaf_0010.07).

## M2.S.8 (diagonal gap-center spacing, 80 nm)

No trial produced a new M2.S.8 violation. This rule checks euclidian distance between shrunk representations of 18 nm tip-to-tip gaps on different tracks and is not triggered by any operation in the history.

## M2.A.1 (minimum area, 504 nm²)

No trial produced a new M2.A.1 violation. The resize_end operations applied (ranging from +28 to +128 dbu) all extended polygons, so area only increased or was unchanged. Shrinking operations on M2 polygons were not observed in the history; the area floor has not been tested under contraction.

## V1.M2.EN.2 and V1.M2.AUX.2 (V1 enclosure by M2)

No trial produced new V1.M2.EN.2 or V1.M2.AUX.2 violations. All move_instance and resize_end operations that touched M2 and V1 simultaneously (trial:i01.ug.Block6_union_row7.03, trial:i01.ug.Block6_union_row8.04, trial:i01.ug.leaf_0015.07, trial:i02.ug.Block6_union_row7.00, trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0008.05) preserved enclosure. The pattern across these trials is that moving an instance as a whole keeps all contained V1 shapes co-displaced with their enclosing M2, maintaining the relative enclosure. Stretching the high-x end of an M2 polygon while simultaneously moving the attached instance does not create an enclosure deficit provided the V1 remains inside the stretched M2 boundary.

## V2.M2.EN.1 (V2 enclosure by M2, 5 nm)

trial:i02.cu.def:VIA_VIA23_1_3_36_36.00 applied a y-axis shrink of -40 dbu to a via cell shape on M3 (layer M3, shape_index 0) inside the VIA_VIA23_1_3_36_36 cell definition, touching layers M2, M3, and V2. The trial was rejected because the net delta across both monitored windows was zero: neither leaf_0009 nor leaf_0010 saw any violation count change. Resizing the M3 shape of a via cell without adjusting the M2 landing or the V2 shape produces no net improvement to V2.M2.EN.1 compliance; any enclosure gain on one edge is offset by loss on another, or the V2 geometry is not the limiting dimension. Do not apply isolated via-cell M3 shape shrinks as a repair strategy for M2-related via enclosure violations without verifying that the corresponding M2 and V2 shapes are also adjusted (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00).

## Assemble-drop conflicts and secondary violations

Both trials with assemble_drops introduced new M2 violations: trial:i02.ug.leaf_0004.03 (1 new M2.S.2) and trial:i02.ug.leaf_0010.07 (1 new M2.S.4, 1 new M2.S.7). In contrast, all trials without assemble_drops produced zero new M2 violations regardless of operation count or displacement magnitude. The presence of an assemble_drops entry is a reliable predictor of residual M2 geometric stress: when a move intended for one unit is dropped because another unit claimed the same instance, the partial move set leaves local M2 geometries in a configuration that neither repair intended, creating violations the individual unit repairs would have avoided. Treat any trial with a non-empty assemble_drops as a candidate for re-examination in the next iteration.

## Large locus, multi-op trials

trial:i02.ug.leaf_0010.07 is the largest-scope trial in the history (locus spanning most of the block, 5 ops, 77 total new violations across layers). Despite the large violation count, the trial was accepted because conn_preserved=true. The M2-specific violations (M2.S.4 and M2.S.7) were a small fraction of the total, dominated by M1.A.1 and V1.M1.EN.1 violations. This indicates that large multi-instance ops introduced primarily through y-axis moves stress M1 and V1 more than M2, but M2 narrow-tip and compound-tip rules are still at risk when y displacements compress inter-track gaps.