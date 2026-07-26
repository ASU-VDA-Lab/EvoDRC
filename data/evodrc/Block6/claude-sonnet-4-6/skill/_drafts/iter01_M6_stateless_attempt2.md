## V5.M6 Enclosure Rules (V5.M6.EN.2, V5.M6.AUX.2)

V5.M6.EN.2 fires when a V5 via lies inside an M6 polygon but the M6 polygon does not extend at least 11 nm beyond the via on both members of at least one pair of opposite sides (checked independently in x and in y). V5.M6.AUX.2 fires when either the V5 is not fully inside M6, or the V5 width perpendicular to the M6 length direction does not exactly match the M6 width in that direction (the check uses coincident-edge counting: a V5 inside M6 passes only when it shares at least 2 edges with the M6 boundary).

Trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 repaired active V5.M6.EN.2 / V5.M6.AUX.2 violations on cell VIA_VIA56_2_2_66_58 by applying two sequential operation types per V5 shape: first move each of the four V5 shapes along x by ±116 dbu (shapes 0 and 2 moved −116 dbu, shapes 1 and 3 moved +116 dbu) to redistribute them within the M6 footprint, then resize each shape by +320 dbu in x to fill the M6 width exactly. The repair was applied with conn_preserved true and reduced violations by a net −16 across units leaf_0019 (−8) and leaf_0020 (−8). Use the paired move-then-resize sequence — moving V5 shapes outward along x to increase enclosure margins, then widening in x to match M6 width — when V5.M6.EN.2 or V5.M6.AUX.2 violations are present on this cell class (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02).

## V6.M6 Enclosure (V6.M6.EN.1)

V6.M6.EN.1 has the same enclosure geometry as V5.M6.EN.2: V6 must be enclosed by M6 with at least 11 nm margin on two opposite sides. The rule structure is identical; the same enclosure strategy applies.

## M6 Width Rules (M6.W.1–M6.W.5)

M6.W.1 sets a minimum vertical (y-direction) width of 32 nm; M6.W.5 sets a minimum horizontal (x-direction) width of 44 nm. M6.W.2 caps vertical width at 640 nm. M6.W.3 forbids vertical widths that are exact even-integer multiples of 32 nm: 64, 128, 192, 256, 320, 384, 448, 512, 576, and 640 nm are all disallowed. M6.W.4 additionally forbids vertical widths of 96, 224, 352, 480, and 608 nm, which correspond to spans covering an even number of minimum-width routing tracks. The combined set of forbidden vertical widths is: 64, 96, 128, 192, 224, 256, 320, 352, 384, 448, 480, 512, 576, 608, 640 nm.

Trial:i01.ug.leaf_0020.09 performed y-axis end-resizes on two M6 polygons within locus [1728, 3148, 15336, 14608]: p2107 had its low end moved +96 dbu and its high end moved +32 dbu; p2106 had its low end moved +16 dbu and its high end moved +112 dbu. The operation was gated_in with 55 new in-crop violations; the decision was not applied. This outcome shows that applying y-axis resize deltas without checking that the resulting vertical span avoids all M6.W.3 and M6.W.4 forbidden values introduces violations rather than clearing them. Resize deltas on M6 y-edges must be chosen so the post-resize vertical span does not land on any of the forbidden widths enumerated by M6.W.3 and M6.W.4 (trial:i01.ug.leaf_0020.09).

## M6 Spacing Rules (M6.S.1–M6.S.5)

M6.S.1: minimum vertical spacing between any two M6 polygon edges is 32 nm, regardless of edge length or mask color. M6.S.2: minimum horizontal spacing between any two M6 polygon edges is 40 nm. M6.S.3: minimum tip-to-tip spacing between M6 polygons on adjacent tracks that do not share a parallel run length is 40 nm. M6.S.4: minimum tip-to-tip spacing between M6 polygons on adjacent tracks that do share a parallel run length is 40 nm. M6.S.5: when two M6 polygons on adjacent tracks share a parallel run, the run length must be at least 44 nm.

In trial:i01.ug.leaf_0020.09, expanding p2106's high end by +112 dbu and p2107's high end by +32 dbu in the same locus reduced vertical clearance to any M6 neighbor immediately above those polygons. The 55 in-crop violations and gated_in outcome demonstrate that extending M6 polygon ends in y without verifying the residual vertical gap to adjacent M6 edges introduces M6.S.1 violations. Do not extend M6 y-ends unless the post-resize gap to every adjacent M6 polygon edge is verified to be ≥ 32 nm (trial:i01.ug.leaf_0020.09).

## M6 Grid and Track Rules (M6.AUX.1, M6.AUX.2, M6.AUX.4)

M6.AUX.1 requires all M6 horizontal edges to lie on a 32 nm vertical grid (y-coordinate mod 32 nm = 0). M6.AUX.2 identifies minimum-width 1x M6 tracks — those polygons that do not survive a vertical erosion and re-dilation of 17 nm — and checks that each such track's centerline satisfies (center_y − 64 nm) mod 256 nm = 0; tracks whose centerlines fall off this routing grid violate AUX.2. M6.AUX.4 checks that wide M6 polygon (surviving the ±17 nm vertical erosion/re-dilation) horizontal outside edges do not lie on any 1x-track band centerline.

In trial:i01.ug.leaf_0020.09, the low-end resize on p2106 was +16 dbu (16 nm), which is not a multiple of 32 nm. If p2106's low edge was previously on the 32 nm grid, the post-resize edge position is no longer grid-aligned, directly triggering M6.AUX.1. The same 16 dbu shift displaces the polygon centerline by 8 nm, which can also move a 1x-track centerline off the (center_y − 64) mod 256 = 0 grid, triggering M6.AUX.2. The gated_in result with 55 new in-crop violations is consistent with both mechanisms activating simultaneously. Resize deltas on M6 horizontal (y-axis) edges must be multiples of 32 nm to remain on the M6.AUX.1 grid; for 1x-track M6 segments, the chosen delta must additionally keep the post-resize centerline at a y value satisfying (center_y − 64) mod 256 = 0 (trial:i01.ug.leaf_0020.09).

## M6 No-Bend Rule (M6.AUX.3)

M6.AUX.3 fires on any M6 polygon edge that is adjacent to a corner whose interior angle is not 90° (i.e., any bend from horizontal to non-horizontal or vice versa). M6 geometry must remain strictly rectilinear; T-shapes, L-shapes with non-right angles, or any polygon carrying a corner with a 0°–90° angular sweep at an interior point are non-compliant.

## Non-Orthogonal Geometry (M6.GEOMETRY.NONORTHOGONAL)

All M6 edges must be at exactly 0° or 90°. Edges with angles in the ranges 1°–89°, 91°–179°, −179°–−91°, or −89°–−1° trigger the NONORTHOGONAL rule. This applies to every edge of every M6 polygon, including any small rounding artifacts.