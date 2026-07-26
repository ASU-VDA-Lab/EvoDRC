**Effective repair operations observed on M4**

All three accepted repairs on M4 used `resize_end` operations along the x-axis (horizontal direction), adjusting the `high` or `low` end of M4 polygons (trial:i01.ug.Block4_union_row10.01, trial:i01.ug.Block4_union_row7.06, trial:i01.ug.leaf_0001.07). Horizontal end-extension is the dominant and consistently accepted move class for M4 in iteration 1. Move-instance operations on adjacent cells accompanied most multi-op repairs (trial:i01.ug.Block4_union_row10.01, trial:i01.ug.Block4_union_row7.06) to preserve connectivity after polygon resizes.

**Via-cell shrink on adjacent layers causes net-positive DRC outcomes on M4**

The only rejected trial in this iteration (trial:i01.cu.def:VIA_VIA34_1_2_58_52.01) applied `resize_via_shape` to reduce M3 and V3 dimensions inside cell VIA_VIA34_1_2_58_52, and was rejected with `rejected_net_positive`: DRC counts in unit leaf_0025 rose by 24 and in unit leaf_0026 by 10, for a total delta of +34. Although M4 was listed as a touched layer, the shrink was on M3/V3 shapes within the via cell. Do not shrink via-cell enclosure shapes targeting V3.M4.EN.2 or V3.M4.AUX.2 compliance via `resize_via_shape` on M3 or V3 when M4 is involved — the approach propagates new violations into neighboring units (trial:i01.cu.def:VIA_VIA34_1_2_58_52.01).

**M4.W rules: forbidden vertical widths and the 24 nm grid constraint**

M4.W.1 requires vertical width ≥ 24 nm; M4.W.2 caps it at 480 nm. M4.W.3 forbids vertical widths that are exact even-integer multiples of 24 nm (48, 96, 144, 192, 240, 288, 336, 384, 432, 480 nm). M4.W.4 additionally forbids 72, 168, 264, 360, and 456 nm vertical widths. M4.W.5 requires horizontal width ≥ 44 nm. No repair in iteration 1 targeted vertical-width violations directly; horizontal end-resizes were used instead (trial:i01.ug.leaf_0001.07, trial:i01.ug.Block4_union_row10.01, trial:i01.ug.Block4_union_row7.06), and all were accepted without introducing M4.W violations, confirming that x-axis resizes on the horizontal extent do not disturb the vertical-width distribution.

**M4.AUX.1 and M4.AUX.2: grid alignment must be maintained after horizontal resizes**

M4.AUX.1 requires M4 horizontal edges to sit on a 24 nm grid. M4.AUX.2 requires that minimum-width M4 tracks (those not surviving a ±13 nm vertical erosion) lie on routing tracks at a 2N × 192 dbu pitch with a 48 dbu offset. All accepted horizontal resizes preserved these constraints (trial:i01.ug.leaf_0001.07 used a +96 dbu delta; trial:i01.ug.Block4_union_row10.01 used deltas of 128, 72, 92, 64 dbu; trial:i01.ug.Block4_union_row7.06 used 164, 92, 56, 172 dbu). Use resize deltas that are multiples of 24 nm (equivalently, multiples of 1 dbu on the 24 nm grid) to avoid introducing M4.AUX.1 violations. The 96 dbu single-op repair (trial:i01.ug.leaf_0001.07) on p1374 is the simplest confirmed safe delta.

**M4.AUX.3: M4 polygons must remain rectilinear with no bends**

M4.AUX.3 prohibits any corner angle other than 90°. All accepted repairs operated on straight horizontal M4 segments via end-resizes rather than shape splits or polygon merges that could introduce bends (trial:i01.ug.Block4_union_row10.01, trial:i01.ug.Block4_union_row7.06, trial:i01.ug.leaf_0001.07). Never introduce polygon operations that create non-90° junctions or T-shaped merges on M4.

**M4.AUX.4: wide M4 polygon outer edges must not align with routing track edges**

M4.AUX.4 fires when the horizontal edges of a wide M4 polygon (those surviving vertical erosion of 13 nm) align with the horizontal routing track edges defined by minimum-width M4 polygons in the same horizontal band. Horizontal end-resizes that do not alter the vertical extent of wide M4 shapes are safe with respect to this rule, consistent with all accepted trials (trial:i01.ug.Block4_union_row10.01, trial:i01.ug.Block4_union_row7.06, trial:i01.ug.leaf_0001.07), which touched only x-axis extents.

**V3.M4.EN.2 and V3.M4.AUX.2: via enclosure approach**

V3.M4.EN.2 requires M4 to enclose V3 by ≥ 11 nm on at least two opposite sides. V3.M4.AUX.2 requires V3 to match the M4 width exactly along the direction perpendicular to the M4 length. The rejected trial (trial:i01.cu.def:VIA_VIA34_1_2_58_52.01) attempted to fix these by shrinking V3 and M3 via shapes, but the outcome was net-positive DRC. Extending the enclosing M4 polygon horizontally (x-axis resize_end) is the accepted approach, as demonstrated across trial:i01.ug.Block4_union_row10.01 and trial:i01.ug.Block4_union_row7.06.

**Multi-op repair with instance moves**

When M4 polygons are resized to satisfy spacing or enclosure rules, adjacent cell instances frequently require simultaneous displacement to avoid creating new violations on M1, M2, or V1. In trial:i01.ug.Block4_union_row10.01, three `move_instance` ops (i0025 +108 dbu, i0041 −108 dbu, i0120 +36 dbu) accompanied four polygon resizes and the repair was accepted with zero new violations. In trial:i01.ug.Block4_union_row7.06, four `move_instance` ops accompanied four polygon resizes and likewise produced zero new violations. Pair each M4 horizontal end-resize with corresponding instance moves on flanking cells to keep connectivity intact.