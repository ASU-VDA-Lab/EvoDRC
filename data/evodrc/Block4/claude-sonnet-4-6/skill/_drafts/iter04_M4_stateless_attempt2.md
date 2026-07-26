## X-Axis Resize Operations on M4

Single-polygon x-axis `resize_end` operations on M4 that respect horizontal width and spacing rules are accepted. In trial:i01.ug.leaf_0001.07, resizing M4 polygon p1374 on its high-x end by 96 dbu was accepted (gated_in, M4 the only touched layer). Multi-polygon x-axis resize sets are similarly accepted: trial:i01.ug.Block4_union_row10.01 applied x-axis resize deltas of 128, 72, 92, and 64 dbu to four M4 polygons (gated_in), and trial:i01.ug.Block4_union_row7.06 applied deltas of 164, 92, 56, and 172 dbu to four M4 polygons (gated_in). The governing horizontal constraints are M4.W.5 (minimum horizontal width 44 nm) and M4.S.2 (minimum horizontal spacing between vertical edges 40 nm); the accepted deltas in all three trials are consistent with those bounds being satisfied.

## Y-Axis Instance Move Increments

Use y-axis move deltas that are multiples of 24 dbu when repositioning instances whose footprints touch M4. In trial:i04.ug.leaf_0002.01, eleven instance moves with y-deltas drawn from {0, +24, -24, +72} dbu — all multiples of 24 — were accepted (gated_in) across layers M3, M4, M5, V3, and V4. The 24 dbu increment matches the M4.AUX.1 grid (M4 horizontal edges must lie on a 24 nm grid); moves in 24 dbu multiples preserve that alignment for any M4 horizontal edge that moves with the instance group.

## V3 Via Shape Resizing When M4 Is in the Affected Layer Set

Do not shrink V3 via shapes in the y-direction when M4 is among the affected layers. In trial:i01.cu.def:VIA_VIA34_1_2_58_52.01, compressing the M3 shape of VIA_VIA34_1_2_58_52 by -64 dbu in y and each of its two V3 shapes by -24 dbu in y increased total DRC violations by 34 (windows: leaf_0025 +24, leaf_0026 +10), resulting in rejection (rejected_net_positive). The affected layer set included M4. The relevant rules are V3.M4.EN.2, which requires at least 11 nm enclosure of V3 by M4 on two opposite sides in both x and y, and V3.M4.AUX.2, which requires V3 to exactly match M4 width along the direction perpendicular to M4 length; reducing V3 vertical extent without corresponding M4 adjustment directly risks violating both.

## M4 Vertical Width Constraints (M4.W.1 – M4.W.4)

M4.W.1 sets a 24 nm minimum vertical width. M4.W.2 caps vertical width at 480 nm (any polygon that survives a ±240 nm y-erosion cycle flags). M4.W.3 prohibits vertical widths that are exact even-integer multiples of the 24 nm minimum: 48, 96, 144, 192, 240, 288, 336, 384, 432, and 480 nm are all forbidden. M4.W.4 additionally prohibits 72, 168, 264, 360, and 456 nm — widths corresponding to a polygon spanning an even number of minimum-width routing tracks vertically. The combined forbidden set from M4.W.3 and M4.W.4 covers every multiple of 24 nm from 48 nm through 480 nm, so valid widths in that range are non-multiples of 24 nm that also fall outside the M4.W.4 set (e.g., 25 nm, 36 nm are valid; 48 nm is not). The only safe minimum-width choice is exactly 24 nm.

## M4 Horizontal Width Constraint (M4.W.5)

M4.W.5 requires a minimum horizontal (x-direction) width of 44 nm as measured by euclidean check on 90°-angle edges. The accepted x-resize deltas in trial:i01.ug.leaf_0001.07, trial:i01.ug.Block4_union_row10.01, and trial:i01.ug.Block4_union_row7.06 are all consistent with the resulting polygon horizontal spans remaining at or above 44 nm.

## M4 Spacing Constraints (M4.S.1 – M4.S.5)

M4.S.1 requires 24 nm minimum vertical spacing between M4 polygon edges (projection and euclidean). M4.S.2 requires 40 nm minimum horizontal spacing between vertical M4 edges. M4.S.3 and M4.S.4 each require 40 nm tip-to-tip spacing between M4 polygons on adjacent tracks, whether or not they share a parallel run length. M4.S.5 requires a minimum parallel run length of 44 nm for M4 segments on adjacent tracks when a gap of less than 24 nm + 1 dbu exists between their horizontal edges.

## Track Alignment (M4.AUX.1 and M4.AUX.2)

M4.AUX.1 requires all M4 horizontal edges to lie on a 24 nm (24 dbu) y-grid. M4.AUX.2 requires that minimum-width M4 tracks (those with vertical extent < 26 nm after ±13 nm y-erosion) have their centerlines on the grid y = 48 + n × 192 dbu. The y-move increments of ±24 and +72 dbu in trial:i04.ug.leaf_0002.01 (gated_in) maintain M4.AUX.1 compliance for any instance whose M4 horizontal edges were already on-grid before the move.

## No-Bend Rule (M4.AUX.3)

M4.AUX.3 prohibits M4 from bending: any M4 polygon corner with an interior angle in the 0°–90° range flags. All M4 operations in trial:i01.ug.leaf_0001.07, trial:i01.ug.Block4_union_row10.01, and trial:i01.ug.Block4_union_row7.06 were x-axis `resize_end` operations on axis-aligned polygons; none introduced off-axis corners, and all were accepted.

## Wide M4 Polygon Edge Placement (M4.AUX.4)

M4.AUX.4 prohibits the outside horizontal edges of wide M4 polygons (those that survive ±13 nm y-erosion, i.e., height > 26 nm) from coinciding with any routing track edge. The routing track edges are the top and bottom boundaries of the 24 nm-wide bands centered at y = 48 + n × 192 dbu (i.e., at y = 36 + n × 192 and y = 60 + n × 192 dbu). Wide M4 edge positions must avoid those y-coordinates. No trial in the current history directly exercises this rule for wide polygons, so the constraint is derived from the rule text alone; new wide-M4 geometry should be validated explicitly.

## V4 Enclosure by M4 (V4.M4.EN.1)

V4.M4.EN.1 requires M4 to enclose V4 by at least 11 nm on at least two opposite sides in both x and y. In trial:i04.ug.leaf_0002.01, a group of eleven instance moves with a uniform x-offset of +32 dbu and y-offsets of {0, +24, -24, +72} dbu touching M4 and V4 together was accepted (gated_in). Moving M4-connected instances and their associated V4 instances by the same x-delta preserved the relative enclosure geometry; the trial outcome confirms that coordinated group moves do not inherently break V4.M4.EN.1.

## V3 Enclosure by M4 (V3.M4.EN.2 and V3.M4.AUX.2)

V3.M4.EN.2 requires M4 to enclose V3 by at least 11 nm on at least two opposite sides. V3.M4.AUX.2 requires V3 to be exactly the same width as M4 in the direction perpendicular to M4 length, with at least two V3 edges coincident with M4 edges; V3 not inside M4, or inside M4 but without two coincident edges, flags. The rejection in trial:i01.cu.def:VIA_VIA34_1_2_58_52.01 — where V3 shapes were compressed vertically while M4 was in the touched-layer set — confirms that independently shrinking V3 in y without matching M4 adjustment is a net-positive violation move against these rules.