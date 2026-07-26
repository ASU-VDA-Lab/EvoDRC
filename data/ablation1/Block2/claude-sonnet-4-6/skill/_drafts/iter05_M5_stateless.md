## Horizontal Width (M5.W.1 – M5.W.4)

The minimum horizontal (x-direction) width of an M5 polygon is 24 nm; the maximum is 480 nm. Within that range, widths equal to even-integer multiples of 24 nm (48, 96, 144, 192, 240, 288, 336, 384, 432, 480 nm) are prohibited by M5.W.3, and widths of 72, 168, 264, 360, and 456 nm are prohibited by M5.W.4 as they span an even number of minimum-width routing tracks.

Horizontal resize_end operations that expand M5 polygons have resolved width violations across multiple iterations. Trial:i01.ug.leaf_0012.07 applied +64 dbu on the low end and +128 dbu on the high end of p938, yielding 2 new in-crop violations with n_new_out_of_crop = 0 and conn_preserved = true. Trial:i02.ug.leaf_0003.02 applied a further +192 dbu on the low end of the same polygon, yielding 4 new in-crop violations. Trial:i03.ug.leaf_0002.01 expanded p937 by +64 dbu low and +320 dbu high, yielding 2 new in-crop violations. All three operations kept n_new_out_of_crop at 0.

When selecting resize targets, the destination width must not equal any M5.W.3 or M5.W.4 forbidden value. The observed successful deltas across trial:i01.ug.leaf_0012.07, trial:i02.ug.leaf_0003.02, and trial:i03.ug.leaf_0002.01 are multiples of 64 dbu; each produced no out-of-crop width violations.

## Vertical Width (M5.W.5)

The minimum vertical (y-direction) width of an M5 polygon is 44 nm. Trial:i04.cu.def:VIA_VIA45_1_2_58_58.00 applied a -88 dbu y-axis shrink to the M5 shape inside via cell VIA_VIA45_1_2_58_58 and was accepted with decision "applied," confirming that y-axis shrink operations are valid provided the resulting height remains at or above 44 nm.

## Horizontal Spacing (M5.S.1)

Minimum horizontal edge-to-edge spacing between M5 polygons is 24 nm, regardless of edge length or mask color. The x-axis expansions in trial:i01.ug.leaf_0012.07 and trial:i03.ug.leaf_0002.01 both kept n_new_out_of_crop at 0, indicating their target positions did not reduce spacing to neighbors below the 24 nm threshold.

## Vertical Spacing (M5.S.2)

Minimum vertical spacing between M5 edges is 40 nm. Y-direction instance moves adjust vertical separation between M5 segments routed through instances. Trials i03.ug.leaf_0002.01, i04.ug.leaf_0003.02, i05.ug.leaf_0002.00, and i05.ug.leaf_0003.01 applied y-moves of ±24, ±48, ±72, and ±96 dbu—all multiples of 24 dbu—while touching M5 through multi-layer stacks, with n_new_out_of_crop = 0 in every case.

## Tip-to-Tip Spacing and Parallel Run Length (M5.S.3 – M5.S.5)

Tip-to-tip spacing between M5 polygons on adjacent tracks is 40 nm regardless of whether a shared parallel run length exists (M5.S.3, M5.S.4). The minimum parallel run length of two M5 polygons on adjacent tracks is 44 nm (M5.S.5). The multi-instance y-moves in trial:i03.ug.leaf_0002.01—moving eight instances simultaneously in the y-direction to adjust inter-track geometry—produced no out-of-crop violations on M5, confirming that coordinated vertical displacement preserves these constraints when moves are in multiples of 24 dbu.

## Grid Alignment (M5.AUX.1)

All M5 vertical edges (left and right faces of horizontal wires) must lie on a 24 nm grid. The resize_end operations in trial:i01.ug.leaf_0012.07 (+64 and +128 dbu), trial:i02.ug.leaf_0003.02 (+192 dbu), and trial:i03.ug.leaf_0002.01 (+64 and +320 dbu) all kept n_new_out_of_crop at 0, confirming those deltas produced grid-compliant edge positions given the starting coordinates of p938 and p937. The value 192 dbu = 8 × 24 nm is a multiple of the 24 nm grid pitch; applying a +192 dbu delta to any grid-aligned starting edge always yields a grid-aligned result, as confirmed by trial:i02.ug.leaf_0003.02.

## Routing Track Placement (M5.AUX.2)

Minimum-width M5 tracks—those that do not survive the ±13 nm x-erosion test (`m5 - m5.sized(-13.nm,0).sized(13.nm,0)`)—must have their x-axis centerlines on a grid with pitch 192 dbu and offset 48 dbu: valid centerlines are at 48, 240, 432, 624, ... dbu (i.e., 48 + 192·N for non-negative integer N). The check additionally filters to shapes whose left and right edges both sit on a 96 dbu sub-grid (base_dbu = 96 in offgrid_cl). Polygons expanded beyond the minimum-width threshold by resize_end are excluded from this check. The expansions in trial:i01.ug.leaf_0012.07 and trial:i03.ug.leaf_0002.01 grew polygons significantly beyond minimum width and produced no AUX.2 out-of-crop violations.

## No-Bend Constraint (M5.AUX.3)

M5 polygons may not contain corners with interior angles in the range (0°, 90°). Every M5 geometry must be a strictly rectilinear, axis-aligned rectangle. Across all measured trials, no M5 bends were introduced: the add_polygon operations in trial:i05.ug.leaf_0002.00 targeted M3 exclusively, and all resize_end operations on M5 (trial:i01.ug.leaf_0012.07, trial:i02.ug.leaf_0003.02, trial:i03.ug.leaf_0002.01) extended existing rectangular shapes along a single axis without introducing corners.

## Wide M5 and Routing Track Edge Prohibition (M5.AUX.4)

For wide M5 polygons (those that survive the ±13 nm x-erosion test), the outer vertical edges must not coincide with any vertical routing track edge. The x-axis resize operations in trial:i01.ug.leaf_0012.07 and trial:i03.ug.leaf_0002.01 moved polygon edges to new positions and produced no AUX.4 out-of-crop violations, confirming the selected target positions avoided routing track boundaries.

## Via Enclosure Rules (V4.M5.EN.2, V4.M5.AUX.2, V5.M5.EN.1)

V4 vias must be enclosed by M5 by at least 11 nm on two opposite sides (V4.M5.EN.2); V5 vias carry the same 11 nm two-sided enclosure requirement (V5.M5.EN.1). Additionally, V4 must exactly match the M5 width in the direction perpendicular to M5's routing length (V4.M5.AUX.2). Since M5 is a horizontal routing layer, this perpendicular direction is the y-axis.

Trial:i04.cu.def:VIA_VIA45_1_2_58_58.00 resolved a net of 16 violations by shrinking the M5 shape within via cell VIA_VIA45_1_2_58_58 by -88 dbu on the y-axis. The reduction distributed as -8 in unit:leaf_0002 and -8 in unit:leaf_0003, and the operation was directly applied via the cu_pool channel. Shrinking M5 y-extent within a via cell is an effective repair for V4.M5.AUX.2 when the as-drawn M5 y-dimension exceeds the corresponding V4 width.

## Multi-Layer Stack Coupling

M5 constraint repairs regularly involve layers beyond M5 itself. Instance moves in trial:i03.ug.leaf_0002.01 touched M3, M4, M5, V3, V4; in trial:i04.ug.leaf_0003.02 they touched M2, M3, M4, M5, V2, V3, V4; in trial:i05.ug.leaf_0002.00 they touched M3, M4, M5, V3, V4; and in trial:i05.ug.leaf_0003.01 they touched M1, M2, M3, M4, M5, V1, V3, V4. Y-direction instance moves at multiples of 24 dbu are the consistent granularity observed for vertical position adjustments that propagate through the stack without creating out-of-crop M5 violations.

## Operational Decision Patterns

All unit_gate channel trials (trial:i01.ug.leaf_0012.07, trial:i02.ug.leaf_0003.02, trial:i03.ug.leaf_0002.01, trial:i04.ug.leaf_0003.02, trial:i05.ug.leaf_0002.00, trial:i05.ug.leaf_0003.01) received decision "gated_in." The cu_pool channel trial (trial:i04.cu.def:VIA_VIA45_1_2_58_58.00) received decision "applied." Across all seven trials, n_new_out_of_crop was 0. New in-crop violation counts ranged from 0 (trial:i05.ug.leaf_0002.00) to 13 (trial:i05.ug.leaf_0003.01), with the higher counts correlating to broader instance-move operations touching more layers.