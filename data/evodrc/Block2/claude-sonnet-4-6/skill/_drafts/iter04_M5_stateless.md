## Constraints active on M5 and their interaction with observed operations

**Grid and track-centering constraints (M5.AUX.1, M5.AUX.2)**

M5 vertical edges must land on a 24 nm (24 dbu) grid (M5.AUX.1). Minimum-width M5 tracks additionally must have their x-centerlines satisfy `(cl − 48) mod 192 == 0` in dbu units (pitch 192 dbu, offset 48 dbu, base 96 dbu per M5.AUX.2). When moving M5 polygons horizontally, the chosen delta must keep the polygon's centerline on this 192 dbu grid; failing to do so violates AUX.2 for any minimum-width segment. In trial:i02.ug.leaf_0002.01 polygon p938 was moved +32 dbu on x together with associated instances, and no new in-crop or out-of-crop violations were introduced; this is consistent with p938 being a wide (non-minimum-width) M5 shape not subject to the AUX.2 centering check, or starting from a position whose centerline remained compliant after the 32 dbu shift. Do not apply a +32 dbu horizontal offset to a minimum-width M5 track unless the pre-move centerline is known to land on the AUX.2 grid post-move.

**No-bend constraint (M5.AUX.3)**

M5 may not contain corners with interior angle in the range (0°, 90°]; any non-orthogonal edge is also forbidden by the GEOMETRY.NONORTHOGONAL block. All operations in this history that touched M5 — instance moves in trial:i01.ug.leaf_0012.07, trial:i02.ug.leaf_0002.01, trial:i03.ug.leaf_0001.00, trial:i03.ug.leaf_0002.01, trial:i04.ug.leaf_0002.01, and via-cell resize in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 — used axis-aligned translations or uniform shape resizes and produced zero new out-of-crop violations. Do not use any rotation, shear, or non-uniform resize on M5 shapes; every permitted operation is a pure x- or y-aligned move or a uniform per-axis resize.

**Horizontal width rules (M5.W.1 – M5.W.4)**

Minimum horizontal width is 24 nm; maximum is 480 nm (M5.W.1, M5.W.2). Widths equal to any even integer multiple of 24 nm — i.e., 48, 96, 144, 192, 240, 288, 336, 384, 432, 480 nm — are forbidden by M5.W.3. Widths of 72, 168, 264, 360, or 456 nm are additionally forbidden by M5.W.4 because they place the polygon over an even number of minimum-width routing tracks horizontally. When resizing M5 horizontally, verify the result is not in either forbidden set. No trial in this history directly demonstrated a width violation being repaired, but the via-cell resize in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 resized V4 and M4 shapes (not M5 widths) by +152 dbu on x and reduced total violations by 16 across leaf_0012 and leaf_0013 without introducing any M5 out-of-crop errors, which is compatible with the M5 shapes in the via cell already satisfying W.1–W.4.

**Vertical width constraint (M5.W.5)**

Minimum vertical width is 44 nm (44 dbu). All y-direction instance moves in this history — [0,−48], [0,+96] in trial:i01.ug.leaf_0012.07; [0,+48] in trial:i03.ug.leaf_0001.00; [0,+72] and [0,−72] in trial:i03.ug.leaf_0002.01; [0,+36] for i0063 in trial:i04.ug.leaf_0002.01 — produced no new out-of-crop M5 violations. The 36 dbu y-move in trial:i04.ug.leaf_0002.01 is sub-track-pitch and was accompanied by a matching move of polygon p1036; the combination introduced exactly 1 new in-crop violation (not out-of-crop) and preserved connectivity.

**Horizontal spacing (M5.S.1)**

Minimum horizontal spacing is 24 nm regardless of parallel run length or mask color. The projection-based check (M5.S.1, first clause) and the global 1 dbu minimum (M5.S.1, second clause) mean that any horizontal shift of an M5 polygon toward a neighbor must leave at least 24 dbu of clearance. Moves of −64 dbu on x in trial:i04.ug.leaf_0002.01 (polygon p937 plus four instances) introduced 1 new in-crop violation while keeping out-of-crop count at zero; the shift brought some M5 edge closer to a neighbor within the crop window but did not propagate violations outside it.

**Vertical spacing constraints (M5.S.2, M5.S.3, M5.S.4, M5.S.5)**

Minimum vertical edge-to-edge spacing is 40 nm (M5.S.2). Tip-to-tip spacing between polygons on adjacent tracks that do not share a parallel run length is 40 nm (M5.S.3); for polygons that do share a parallel run length, the same 40 nm tip-to-tip minimum applies (M5.S.4). The minimum parallel run length on adjacent tracks is 44 nm (M5.S.5). Y-direction moves of ±48, ±72, ±96 dbu on instances in trial:i01.ug.leaf_0012.07, trial:i03.ug.leaf_0001.00, and trial:i03.ug.leaf_0002.01 all cleared these rules without new out-of-crop violations; those magnitudes exceed the 40 nm vertical spacing minimum, consistent with the moves repositioning shapes to valid track positions rather than closing gaps below threshold.

**Wide M5 and routing track edge constraint (M5.AUX.4)**

Wide M5 polygons (horizontal width > 24 nm after erosion/re-expansion by 13 nm) must not have their vertical edges aligned with a minimum-width routing track's vertical band. When resizing wide M5 shapes, the outer vertical edges must not fall on any AUX.2 track centerline ± half-track-width. No violation of M5.AUX.4 was introduced by any trial in this history.

**V4 enclosure and width matching (V4.M5.EN.2, V4.M5.AUX.2)**

V4 must be enclosed by M5 by at least 11 nm on two opposite sides (V4.M5.EN.2). V4 must exactly match M5 width in the direction perpendicular to the M5 run direction (V4.M5.AUX.2). In trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 both V4 shapes in cell VIA_VIA45_1_2_58_58 were resized +152 dbu on x, and M4 was also resized +152 dbu on x; M5 was in the touched-layers set, confirming that the via cell's M5 shape was affected. The operation was applied via cu_pool with a net −16 violation delta across two windows and zero new out-of-crop violations. When resizing a V4 shape inside a via cell that also contains M5, ensure the M5 shape in the same cell is co-resized as needed to preserve both the 11 nm enclosure (V4.M5.EN.2) and exact perpendicular width match (V4.M5.AUX.2).

**V5 enclosure (V5.M5.EN.1)**

V5 must be enclosed by M5 by at least 11 nm on at least two opposite sides. No V5-touching operations appear in this history; the constraint is structurally identical to V4.M5.EN.2 and the same co-resize discipline applies.

**Connectivity preservation across all M5 operations**

Every operation recorded in this history that touched M5 — trial:i01.ug.leaf_0012.07, trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, trial:i02.ug.leaf_0002.01, trial:i03.ug.leaf_0001.00, trial:i03.ug.leaf_0002.01, trial:i04.ug.leaf_0002.01 — reported `conn_preserved: true` and `n_new_out_of_crop: 0`. Moves that introduced new in-crop violations (1 each in trial:i03.ug.leaf_0002.01, trial:i04.ug.leaf_0002.01) were still accepted because they did not propagate violations outside the crop boundary and preserved connectivity; this indicates the repair engine accepts bounded in-crop growth when out-of-crop count stays at zero and nets are intact.