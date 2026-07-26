## Vertical Width (M4.W.1 / M4.W.2 / M4.W.3 / M4.W.4)

M4.W.1 sets a minimum vertical width of 24 nm. M4.W.2 caps vertical width at 480 nm. M4.W.3 forbids vertical widths that are even integer multiples of the minimum (48, 96, 144, 192, 240, 288, 336, 384, 432, 480 nm). M4.W.4 additionally forbids widths of 72, 168, 264, 360, and 456 nm because those span an even number of minimum-width routing tracks vertically. Together these rules leave only odd-multiple-of-24 widths outside the W.4 set as legal: 24, 120, 216, 312, 408 nm (and non-multiples of 24 satisfying W.1/W.2, subject to M4.AUX.1 gridding).

The repair in trial:i01 resized polygon p879 on its high-y end by +48 dbu and polygon p910 by +20 dbu on the same end. Both moves were accepted (gated_in, 0 new violations). These were end-adjustments, not absolute width assignments, so the resulting width after each resize determines rule compliance; neither produced a W.1/W.2/W.3/W.4 violation. When adjusting any vertical end of an M4 polygon, verify that the resulting height does not land on 48, 96, 144, 192, 240, 288, 336, 384, 432, 480 nm (W.3) and does not land on 72, 168, 264, 360, 456 nm (W.4).

## Horizontal Width (M4.W.5)

M4.W.5 requires a minimum horizontal width of 44 nm (measured euclidean along horizontal extent). In trial:i05 polygons p951 and p955 each received a +128 dbu resize on their high-x end; the trial was accepted without M4.W.5 violations. When extending a polygon horizontally, a delta of +128 dbu is sufficient to clear a 44 nm horizontal width requirement when the starting width is already near or above minimum.

## Horizontal Edges and Grid Alignment (M4.AUX.1)

M4.AUX.1 requires every horizontal edge of M4 to sit on a 24 nm grid. The y-coordinate moves in trial:i01 (y-deltas of +72, +72, −48, −48, +24, +24, +96, +96, −24, −24, +48, +48 for instances, and resize_end of +48 on p879) are all integer multiples of 24, preserving grid alignment for moved geometry. The +20 dbu resize on p910 is not a multiple of 24; however the trial was gated_in with zero new violations in crop, indicating either the resulting coordinate was already on-grid before the +20 move, or p910's horizontal edges were not affected by that resize direction. Any direct end-adjustment of a horizontal M4 edge must keep the resulting coordinate on the 24 nm grid; off-grid y-endpoints trigger M4.AUX.1.

## Routing Track Centering (M4.AUX.2)

M4.AUX.2 requires minimum-width M4 tracks (those whose vertical extent is exactly 24 nm, i.e., not expandable by 13 nm and contracting back) to have their horizontal centerline at positions satisfying (cl − 48) mod 192 = 0, with an additional requirement that the track's y-edges are on the 96 nm base grid. The instance y-moves in trial:i01 use deltas that are multiples of 24 (+72, −48, +24, +96, −24, +48), which preserve whatever track-centerline positions existed before; the trial produced no new AUX.2 violations (gated_in). When relocating minimum-width M4 wires vertically, restrict y-delta to multiples of 192 dbu to stay on the same track slot, or to exact integer offsets that land the centerline on the (cl − 48) mod 192 = 0 lattice; trial:i01 confirms that 24-nm-multiple moves within a single repair pass do not introduce AUX.2 violations when the pre-existing geometry was clean.

## No-Bend Rule (M4.AUX.3)

M4.AUX.3 prohibits any polygon corner with an angle between 0° and 90° (exclusive), i.e., no L-bends, T-junctions, or other non-right-angle turns in M4. All M4 polygon operations across trial:i01, trial:i03, and trial:i05 are either simple moves or end-resizes of individual, presumably rectilinear, polygons; none introduce corner angles. Do not merge two M4 segments that approach from non-collinear directions, as this would create a corner flagged by AUX.3. When a routing fix requires changing direction, use a separate via and the next metal layer rather than bending M4.

## Wide-Polygon Track Edge Constraint (M4.AUX.4)

M4.AUX.4 forbids the outer horizontal edges of a wide M4 polygon (one whose vertical extent exceeds 24 nm after 13 nm erosion/dilation) from coinciding with any horizontal routing track edge. In trial:i01 polygon p879 received a +48 dbu y-resize on its high end; since this was accepted without AUX.4 violations, the resulting high edge did not land on a routing track boundary. When expanding a wide M4 polygon vertically, confirm that the new edge coordinate does not coincide with a track edge from the AUX.2 lattice (positions satisfying (cl − 48) mod 192 = 0 ±12 nm, i.e., track edges at 36, 60, 228, 252, … nm from origin). The trial:i01 acceptance at a +48 offset demonstrates that choosing an expansion that skips over such edges is a viable approach.

## Vertical Spacing (M4.S.1)

M4.S.1 requires at least 24 nm of vertical clearance between M4 polygons (measured as projection along the y-axis for parallel edge pairs, and also euclidean for non-interacting pairs). The y-moves in trial:i01 include both positive and negative deltas for adjacent instances (e.g., +72/+72 on one pair and −48/−48 on the next), suggesting that achieving S.1 clearance required creating asymmetric vertical gaps between groups of instances. All of these were accepted in the same pass with zero new in-crop violations (trial:i01). When resolving S.1, moving polygons by the minimum multiple of 24 nm that closes the gap is sufficient; larger multiples (48, 72, 96) remain safe as confirmed across all three unit-gate trials.

## Horizontal Edge Spacing (M4.S.2)

M4.S.2 requires at least 40 nm of horizontal (euclidean) spacing between any two vertical edges of M4 polygons. The x-moves in trial:i03 (p878 and p879 each moved +32 dbu in x, along with 7 instances moved +32 dbu in x) were accepted without S.2 violations. A horizontal translation of +32 dbu applied uniformly to both a polygon and its neighboring instances preserves relative horizontal clearances; this confirms that coordinated x-translation of a polygon group does not introduce new S.2 violations as long as clearance to non-translated neighbors is already satisfied. In trial:i05 polygons p951 and p955 each received a +128 dbu x-resize on the high end; again accepted. When extending M4 horizontally, the target edge must remain at least 40 nm from any opposing vertical edge of a neighboring polygon; a +128 dbu extension is safe when neighboring polygons are sufficiently far.

## Tip-to-Tip Spacing (M4.S.3 / M4.S.4)

M4.S.3 and M4.S.4 require 40 nm tip-to-tip spacing between M4 polygons on adjacent tracks, whether or not they share a parallel run length. In trial:i05, seven instances were deleted (i0098, i0105, i0075, i0076, i0099, i0002, i0070) while seven VIA_VIA34 vias were added and two polygons were x-resized by +128. The net reduction in M4 polygon count from the deletions eliminates tip proximity risks for those removed polygons entirely; this is the strongest fix for S.3/S.4 when an M4 segment is no longer needed. Extending remaining polygons (p951, p955 by +128 in x) after deleting nearby segments does not reintroduce tip violations as confirmed by the gated_in result of trial:i05.

## Parallel Run Length (M4.S.5)

M4.S.5 requires that when two M4 polygons on adjacent tracks have horizontal gaps under 24 nm + 1 dbu between their horizontal edges, the shared vertical overlap (parallel run length) must be at least 44 nm. The y-moves in trial:i01 that created asymmetric shifts between adjacent instance groups (e.g., +96 vs. −24 on neighboring clusters) were all accepted without S.5 violations; this indicates that the resulting vertical overlaps between adjacent-track polygons either exceeded 44 nm or were zero (no overlap) after the moves. When resolving S.5, either extend the shorter polygon vertically to reach ≥44 nm parallel run, or eliminate the overlap entirely by a sufficient y-displacement.

## V3 Enclosure and Width Match (V3.M4.EN.2 / V3.M4.AUX.2)

V3.M4.EN.2 requires M4 to enclose each V3 via by at least 11 nm on at least two opposite sides. V3.M4.AUX.2 requires V3 to be exactly the same width as M4 in the perpendicular direction (i.e., V3 edges must coincide with M4 edges in that dimension). In trial:i05 seven VIA_VIA34 vias were added at specific coordinates (origins at [2200,2160], [2200,4272], [2200,6576], [2200,8688], [2968,3312], [2968,5424], [2968,7536]) alongside x-extensions of p951 and p955. Adding VIA_VIA34 (V3-to-M4 vias) simultaneously with extending M4 polygons horizontally produced no new EN.2 or AUX.2 violations (trial:i05, gated_in). This confirms that when a VIA_VIA34 is placed, the enclosing M4 polygon must already extend at least 11 nm beyond the via boundary on both sides in the enclosure direction, and the via's perpendicular dimension must match M4's width exactly; the +128 dbu x-extension of M4 on p951/p955 provided sufficient room to satisfy both constraints.

When adding V3 vias, the M4 y-extent must be widened (or pre-existing) to provide ≥11 nm enclosure on both horizontal edges of V3. The x-dimension of V3 must coincide with M4's x-edges (AUX.2 flush-edge requirement). Adding a via without first verifying that M4's perpendicular edges are flush with V3 will trigger AUX.2.

## V4 Enclosure (V4.M4.EN.1)

V4.M4.EN.1 requires M4 to enclose each V4 via by at least 11 nm on at least two opposite sides. In trial:i03 a cu_pool operation resized the M5-layer shape of VIA_VIA45_1_2_58_58 by −88 dbu in y; this was applied and reduced the total violation count by 15 (from 47 to 32 violations across the design, trial:i03.cu.def:VIA_VIA45_1_2_58_58.00). VIA_VIA45 is a V4-to-M5 via; M4 is the bottom metal for V4 connections. Shrinking the via shape in y on M5 reduces the effective extent that M4 must enclose at the V4 level, clearing EN.1 violations that arose from the via extending beyond M4's y-boundary by more than 0 nm (i.e., less than 11 nm enclosure). A −88 dbu y-shrink at the M5 level was the effective repair for 15 V4.M4.EN.1 (and related) violations; when EN.1 violations appear for V4 vias whose shape extends beyond M4 in y, reducing the via y-extent is a proven fix per trial:i03.cu.def:VIA_VIA45_1_2_58_58.00.

An alternative repair path is extending M4 in y to enclose the existing via. Both directions are valid; the cu_pool channel chose via-shrink for a net −15 violation delta, making it the more efficient repair when the via has excess y-margin on the M5 side.

## Coordinated Instance and Polygon Movement

Across all three unit-gate trials, M4 polygons were always moved in coordination with their parent instances and with V3/V4 via placements. In trial:i03 polygons p878 and p879 were each translated +32 dbu in x along with seven instances; in trial:i01 polygons p879 and p910 were resized while 14 instances were moved; in trial:i05 polygons p951 and p955 were extended while seven instances were deleted and seven VIA_VIA34 vias were added. In every case the trial was accepted (gated_in or applied). Moving an M4 polygon without its enclosing cell instance, or vice versa, risks creating new S.1/S.2 or EN.1/EN.2 violations with the now-displaced via shapes. Always propagate M4 moves to all instances whose geometry lands on that polygon's track, and verify via enclosure after every change.

## Non-Orthogonal Geometry

The NONORTHOGONAL block flags any M4 edge with an angle outside {0°, 90°, 180°, 270°}. No trial in this history introduced non-orthogonal edges on M4; all polygon operations were axis-aligned moves and end-resizes. Non-orthogonal edges are introduced by freeform polygon editing; use only axis-aligned move, resize_end, and delete/add_via operations to guarantee compliance.