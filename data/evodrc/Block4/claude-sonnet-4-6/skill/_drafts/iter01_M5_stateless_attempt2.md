**Shape geometry**

Rule M5.AUX.3 fires on M5 corners whose interior angle is between 0° and 90°, meaning any bend in an M5 polygon triggers this rule. Rule M5.GEOMETRY.NONORTHOGONAL fires on any M5 edge with angle outside {0°, 90°, 180°, 270°}. In trial:i01.ug.leaf_0025.11, the repair operated by moving instances with no change to M5 polygon outlines, consistent with the requirement that M5 shapes remain rectilinear and bend-free.

**Horizontal width**

Rule M5.W.1 fires when the horizontal width (measured by projection along the Y axis, using 90° edges) is less than 24 nm. Rule M5.W.2 fires when the horizontal width exceeds 480 nm, detected by a ±240 nm horizontal erosion/expansion cycle. Rule M5.W.3 fires when the horizontal width is an even integer multiple of the 24 nm minimum: 48, 96, 144, 192, 240, 288, 336, 384, 432, or 480 nm. Rule M5.W.4 fires when the horizontal width is 72, 168, 264, 360, or 456 nm, which represent widths spanning an even number of minimum-width routing tracks. Any horizontal width that equals one of the M5.W.3 or M5.W.4 forbidden values produces a violation regardless of other geometry.

**Vertical width**

Rule M5.W.5 fires when the Euclidean width measured along 0° edges is less than 44 nm.

**Horizontal spacing**

Rule M5.S.1 fires on two M5 polygons whose horizontal (90° edge) spacing is less than 24 nm by projection, or whose spacing is less than 1 nm by Euclidean distance. Rule M5.S.3 fires on tip-to-tip spacing below 40 nm between polygons on adjacent tracks that share no parallel run length; it uses a 48 nm horizontal dilation to identify adjacent-track polygons before checking tip spacing. Rule M5.S.4 fires on tip-to-tip spacing below 40 nm between polygons that do share a parallel run length; it extends horizontal edges ±30 nm in the tip direction, removes interior area, and checks enclosing distance to facing horizontal edges.

**Vertical spacing**

Rule M5.S.2 fires when the spacing between two M5 polygons measured along 0° edges is less than 40 nm. Rule M5.S.5 fires when two adjacent-track M5 polygons with a 24 nm horizontal gap (identified by the gap's bbox width) have a parallel run length below 44 nm along the 0° direction.

**Grid alignment**

Rule M5.AUX.1 fires when any merged M5 polygon has a vertex not on the 24 nm horizontal grid (x-coordinate not a multiple of 24 nm). Rule M5.AUX.2 applies specifically to minimum-width M5 segments, defined as the difference between the raw M5 layer and its ±13 nm horizontal erosion/re-expansion. For these segments, their x-axis centerline must satisfy (cl − 48) mod 192 == 0 when the segment's horizontal extent is a multiple of 96 dbu; off-track centerlines fire M5.AUX.2.

**Wide metal and routing track interaction**

Rule M5.AUX.4 fires when the vertical (90°) outer edges of a wide M5 polygon — one that survives the ±13 nm horizontal erosion/re-expansion — fall within the vertical projection bands of any separate minimum-width M5 segment's vertical edges. The minimum-width segment set used for this check excludes segments that are spatially connected to wide polygons.

**Via enclosure**

Rule V4.M5.EN.2 fires on a V4 via inside M5 that lacks at least 11 nm of M5 enclosure on two opposite sides (both horizontal and vertical enclosure are checked simultaneously). Rule V4.M5.AUX.2 fires when a V4 via does not exactly match M5 width in the direction perpendicular to M5's length; it is satisfied only when at least two coincident edges exist between the via perimeter and the M5 boundary. Rule V5.M5.EN.1 fires on a V5 via inside M5 that lacks 11 nm enclosure on at least two opposite sides, using the same two-sided check as V4.M5.EN.2.

**Repair history**

Trial trial:i01.ug.leaf_0025.11 (Block4, channel unit_gate) applied two instance moves — i0234 and i0305, each shifted [0, 64] dbu in Y — touching M5, M6, and V5 layers. The operation was accepted (gated_in) because connectivity was preserved (conn_preserved=true) and no new violations appeared outside the crop boundary (n_new_out_of_crop=0), even though 9 new violations appeared inside the crop window. Operations on M5-touching instances proceed to acceptance when connectivity is preserved and all new violations remain within the crop boundary (trial:i01.ug.leaf_0025.11).