## M5 Width Rules

M5.W.1 sets the minimum horizontal width at 24 nm; M5.W.5 sets the minimum vertical width at 44 nm. M5.W.2 caps horizontal width at 480 nm. M5.W.3 and M5.W.4 prohibit horizontal widths that are even integer multiples of the 24 nm minimum (48, 96, 144, 192, 240, 288, 336, 384, 432, 480 nm) and widths that span an even number of minimum-width routing tracks (72, 168, 264, 360, 456 nm by projection check). These prohibited widths arise from the double-patterning track structure and must not be introduced when resizing M5 polygons or via landing shapes.

## M5 Spacing Rules

M5.S.1 enforces a minimum horizontal spacing of 24 nm (projection, perpendicular edges) with a global 1 dbu floor from the euclidean check. M5.S.2 enforces a minimum vertical spacing of 40 nm between parallel horizontal edges. M5.S.3 covers tip-to-tip spacing of 40 nm for polygons on adjacent tracks that share no parallel run length; M5.S.4 covers the same 40 nm requirement for polygons that do share a parallel run length. M5.S.5 requires a parallel run length of at least 44 nm when two polygons occupy adjacent tracks.

## M5 Grid and Track Alignment (M5.AUX.1, M5.AUX.2)

M5 vertical edges must lie on a 24 nm x-grid (M5.AUX.1). In trial:i04.ug.leaf_0002.01 the m5_align group repositioned M5 polygon p1341 by +32 dbu on the x-axis as part of a coordinated alignment sweep; this move is the direct corrective action for off-grid vertical edges and was applied jointly to the polygon and to five instances in the same group.

Minimum-width M5 tracks (polygons that do not survive a ±13 nm horizontal erosion/dilation) must be centered on vertical routing tracks at a 192 dbu pitch with a 48 dbu offset from the origin (M5.AUX.2). In trial:i04.ug.leaf_0002.01 the m5_align group moved five instances by x=+32 dbu simultaneously with the polygon move, demonstrating that routing-track alignment corrections must be applied to every M5 geometry in the connected group; applying the x-shift to only a subset of geometries would reintroduce spacing or track-occupancy violations.

## M5 No-Bend Rule (M5.AUX.3)

M5 polygons may not contain bends; any corner with an interior angle between 0° and 90° triggers M5.AUX.3. All M5 operations in the measured history act on rectilinear wire segments or rectangular via landing pads; no bends are introduced by the observed repair operations.

## Wide M5 and Routing-Track Edge Rule (M5.AUX.4)

Wide M5 polygons (surviving ±13 nm horizontal erosion/dilation) must not have their outer vertical edges coincide with any minimum-width routing track edge. In trial:i04.cu.def:VIA_VIA56_2_1_66_58.00 and trial:i04.cu.def:VIA_VIA56_2_2_66_58.01, the M5 via landing was extended by 160 dbu along the y-axis only; the routing-track-facing vertical edges were not shifted, leaving the x-extent of the wide landing unchanged. Use y-axis resize rather than x-repositioning when extending M5 via landings in VIA56-family cells so that the outer vertical edges remain on their current x-coordinates.

## Via Cell Repairs Involving M5 (VIA56)

In trial:i04.cu.def:VIA_VIA56_2_1_66_58.00, the M5 shape inside VIA_VIA56_2_1_66_58 was extended by +160 dbu on y, and each of the two V5 shapes was moved by ∓132 dbu then enlarged by +512 dbu on y; the net violation reduction was −2. In trial:i04.cu.def:VIA_VIA56_2_2_66_58.01, the same M5 resize (+160 dbu on y) was applied to VIA_VIA56_2_2_66_58, with four V5 shapes each moved by ∓132 dbu and enlarged by +512 dbu on y; the net reduction was −4. Apply the +160 dbu y-extension to the M5 shape in conjunction with the ±132 dbu V5 center shift and +512 dbu V5 y-resize when resolving V5 enclosure violations (V5.M5.EN.1) in VIA56-family cells.

## Via Cell Repairs Involving M5 and V4 (VIA45)

In trial:i05.cu.def:VIA_VIA45_1_2_58_58.01, V4 shapes in VIA_VIA45_1_2_58_58 were shifted by ±116 dbu and each enlarged by +384 dbu along x, while the M4 shape was extended by +152 dbu on x; M5 is listed in touched_layers. This single operation produced the largest violation reduction in the history: −38 total (leaf_0001: 74→46; leaf_0002: 29→19). Widening V4 along x to satisfy V4.M5.EN.2 — which requires V4 to be enclosed by M5 on two opposite sides by at least 11 nm — is the primary driver of this reduction; use the ±116 dbu center-shift plus +384 dbu x-resize on V4 shapes when enclosure on either opposite side is insufficient, as measured in trial:i05.cu.def:VIA_VIA45_1_2_58_58.01.

V4.M5.AUX.2 requires V4 to match M5 width exactly along the direction perpendicular to M5 length. When V4 is widened on x as in trial:i05.cu.def:VIA_VIA45_1_2_58_58.01, resize M4 on the same axis (+152 dbu in that trial) in the same operation; resizing V4 without resizing M4 breaks the co-width requirement at the M4/V4 interface.

## Instance Move Discipline

Instance moves along y in multiples of 64 dbu (trial:i01.ug.leaf_0025.11, delta [0,64]) and 24 dbu (trial:i04.ug.leaf_0002.01, deltas [0,24] and [0,−24]) are the observed y-direction increments for M5-touching instances. A 64 dbu y-move can introduce up to 9 new violations within the crop region even when connectivity is preserved (trial:i01.ug.leaf_0025.11, n_new_in_crop=9, decision gated_in); gate y-moves of this magnitude against the new in-crop violation count before committing.