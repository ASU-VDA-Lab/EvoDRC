## M6 Vertical Dimension Repairs via resize_end

The unit_gate channel repairs M6 vertical dimension violations (M6.W.1 min 32 nm, M6.W.2 max 640 nm, M6.W.3/M6.W.4 forbidden width multiples) using `resize_end` operations on the y-axis. Trial i01.ug.leaf_0020.09 applied four such operations: p2107 low end +96 dbu, high end +32 dbu; p2106 low end +16 dbu, high end +112 dbu. All four deltas are multiples of 16 dbu. The decision was `gated_in` with `conn_preserved`; 55 new in-crop violations were introduced and accepted.

Because the unit_gate channel accepts changes that add in-crop violations when connectivity is preserved (trial i01.ug.leaf_0020.09, 55 new violations accepted; trial i03.ug.leaf_0003.02, 26 new violations accepted), a `gated_in` outcome does not certify that the resize step is DRC-clean. Always evaluate whether the target end position satisfies M6.AUX.1 (horizontal edges on 32 nm grid) and, for minimum-width tracks, M6.AUX.2 (track centerline pitch 256 dbu, offset 64 dbu) before committing the step as a final repair.

## M6.AUX.1 Grid Compliance for resize_end Targets

M6.AUX.1 requires all M6 horizontal edges to lie on a 32 nm grid. Resize_end deltas of 32 dbu and 96 dbu (trial i01.ug.leaf_0020.09, p2107) are multiples of 32 dbu and therefore preserve grid alignment of horizontal edges that were already on-grid. The delta of 16 dbu (p2106 low end, trial i01.ug.leaf_0020.09) is a half-grid step; any edge moved by 16 dbu from an on-grid position lands off-grid and will trigger M6.AUX.1. The delta of 112 dbu (p2106 high end, trial i01.ug.leaf_0020.09) is also not a multiple of 32 dbu (112 = 3×32 + 16); the same off-grid risk applies unless the starting edge was itself offset by 16 dbu. The presence of 55 new in-crop violations following trial i01.ug.leaf_0020.09 is consistent with these off-grid displacements triggering M6.AUX.1 or other width rules.

## M6.AUX.2 Routing Track Alignment

M6.AUX.2 constrains minimum-width M6 tracks: their centerlines must satisfy the grid `(center - 64) mod 256 == 0`. Any `resize_end` step that shifts both ends asymmetrically alters the centerline. Trial i01.ug.leaf_0020.09 moved p2107's low end by +96 and high end by +32, shifting the centerline by (96−32)/2 = 32 dbu. The 32 dbu shift is not a multiple of 256 dbu and will move a previously on-grid centerline off the AUX.2 track grid unless the pre-operation center was already offset such that the post-operation center lands on a valid grid point. The 55 new in-crop violations accepted in trial i01.ug.leaf_0020.09 encompass this class of secondary violation.

## V5 Via Cell Repairs for V5.M6.EN.2 and V5.M6.AUX.2

V5.M6.EN.2 requires M6 to enclose V5 by at least 11 nm on two opposite sides. V5.M6.AUX.2 requires the V5 width in the direction perpendicular to M6 length to exactly match the M6 width on that axis. Trial i01.cu.def:VIA_VIA56_2_2_66_58.02 addressed these by editing the via cell definition `VIA_VIA56_2_2_66_58` at the `cu_pool` channel: four V5 shapes were moved ±116 dbu on the x-axis (shapes 0 and 2 moved −116, shapes 1 and 3 moved +116) and then each resized by +320 dbu on x. This operation reduced total violations by 16 (−8 in leaf_0019, −8 in leaf_0020) and was recorded as `applied`.

Because a via cell definition edit propagates to all instances of that cell, the cu_pool channel targets enclosure repairs at the cell level when the violation is systematic across multiple instantiation sites. Trial i01.cu.def:VIA_VIA56_2_2_66_58.02 achieved simultaneous improvement in two units (leaf_0019 and leaf_0020) from a single 8-operation patch, confirming that cell-level edits are the correct repair vehicle when the same via definition is responsible for repeated violations across units.

The x-axis resize of +320 dbu per shape expands each V5 shape's horizontal extent. Combined with the ±116 dbu lateral spread of the pair, the net horizontal coverage of the via cluster increases. The 11 nm enclosure margin required by V5.M6.EN.2 corresponds to 11 dbu; the 320 dbu resize is well in excess of that margin, indicating the operation also targets V5.M6.AUX.2 width-match compliance or pre-existing slack deficits accumulated across multiple prior iterations. Trial i01.cu.def:VIA_VIA56_2_2_66_58.02 is the only cu_pool operation in the measured history and is the reference point for via enclosure repair magnitude on this design.

## M6 Horizontal Position Moves with Instance Co-movement

Trial i03.ug.leaf_0003.02 (iter 3, unit_gate) moved M6 polygon p1683 by +32 dbu on the x-axis and polygon p1682 by −16 dbu on the x-axis. Each polygon move was accompanied by the coordinated move of 8 cell instances: instances i0379, i0366, i0360, i0198, i0136, i0168, i0384, i0173 moved +32 dbu with p1683; instances i0527, i0435, i0411, i0109, i0022, i0026, i0528, i0027 moved −16 dbu with p1682. The operation touched M4, M5, M6, V4, and V5 and was accepted as `gated_in` with `conn_preserved` despite introducing 26 new in-crop violations.

Move M6 polygons on the x-axis only when all co-routed instances on connected layers (V4, M5, V5, and in this design M4) are moved by the same delta, as demonstrated by trial i03.ug.leaf_0003.02. Omitting the instance co-movement would break connectivity and prevent the `conn_preserved` condition from being satisfied, blocking the `gated_in` gate.

A move step of +32 dbu on x aligns with M6.S.1 (32 nm minimum vertical spacing, meaning horizontal neighbor steps of 32 nm preserve spacing parity) and M6.W.1 (32 nm minimum vertical width). A step of −16 dbu on x (p1682, trial i03.ug.leaf_0003.02) is a half-grid step relative to the M6.S.2 (40 nm) and M6.W.5 (44 nm) horizontal rules. Trial i03.ug.leaf_0003.02 introduced 26 new in-crop violations consistent with a −16 dbu step causing horizontal spacing or width violations at adjacent geometry; those violations were accepted only because connectivity was preserved.

## Channel Decision Rules Observed in History

The unit_gate channel accepts ops that introduce new in-crop violations as long as `conn_preserved` is true (trial i01.ug.leaf_0020.09: 55 new violations accepted; trial i03.ug.leaf_0003.02: 26 new violations accepted). Use unit_gate results as connectivity-safe staging steps, not as indicators of DRC improvement.

The cu_pool channel requires a net violation reduction to record `applied` (trial i01.cu.def:VIA_VIA56_2_2_66_58.02: delta_total −16, applied). Apply cu_pool repairs at the via cell definition level when the same enclosure violation is instantiated across multiple units, because the cell edit amortizes the violation reduction across all instances simultaneously.

## Multi-Layer Coupling Requirements

Every M6 repair in the measured history involved simultaneous changes on at least one adjacent layer. Trial i01.cu.def:VIA_VIA56_2_2_66_58.02 touched M5, M6, and V5. Trial i03.ug.leaf_0003.02 touched M4, M5, M6, V4, and V5. Trial i01.ug.leaf_0020.09 touched M6 only, and that isolation was possible because the repair addressed M6 vertical end positions without altering V5 enclosure geometry on the x-axis.

Apply multi-layer co-moves (as in trial i03.ug.leaf_0003.02) whenever an M6 x-axis position change would otherwise disconnect V5 vias from M6 coverage or violate V5.M6.EN.2 by exposing V5 edges that were previously enclosed. The +32/−16 dbu x-axis moves in trial i03.ug.leaf_0003.02 required V4 and V5 co-movement precisely to maintain enclosure continuity across the stack.

## Bend and Non-Orthogonal Geometry

M6.AUX.3 forbids M6 polygon bends (corners with interior angles in 0–90°). The GEOMETRY.NONORTHOGONAL rule forbids non-axis-aligned edges on all drawing layers including M6. All ops in the measured history (resize_end, move, move_instance, move_via_shape, resize_via_shape) are strictly axis-aligned. Apply resize_end only to end edges that are already orthogonal; never introduce diagonal cuts or angled endpoints when adjusting M6 polygon boundaries.

## V6.M6.EN.1 Clearance Preservation

V6.M6.EN.1 requires M6 to enclose V6 by at least 11 nm on at least two opposite sides. No trial in the measured history directly addresses a V6.M6.EN.1 violation, but M6 y-axis resize_end operations (trial i01.ug.leaf_0020.09) alter M6 vertical extent and can reduce or eliminate V6 enclosure if V6 is placed near the resized end. When applying resize_end ops that retract an M6 end (negative delta on low end or positive delta on high end relative to the edge direction), verify that no V6 via shape loses its 11 nm enclosure margin on the retracted side.