Looking at the DRC rules and 4 measured history records to synthesize grounded M4 knowledge.

## Grid and Track Alignment

M4.AUX.1 requires all M4 horizontal edges to lie on a 24 nm (1 dbu = 1 nm assumed throughout this document) vertical grid. Every accepted instance move in the recorded history uses vertical (y-axis) deltas that are exact multiples of 24 dbu: ±24 dbu and ±72 dbu in trial:i03.ug.leaf_0002.01, and ±24 dbu in trial:i04.ug.leaf_0003.02. Do not apply y-axis deltas that are not multiples of 24 dbu to instances whose footprints contain minimum-width M4 wires; doing so will introduce M4.AUX.1 violations.

M4.AUX.2 requires minimum-width M4 tracks to center on horizontal routing tracks at a pitch of 192 dbu with an offset of 48 dbu from the origin (centerlines at y = 48, 240, 432, 624, … dbu). The ±72 dbu moves in trial:i03.ug.leaf_0002.01 shift track centerlines by exactly 3 × 24 dbu, preserving membership on the 192 dbu pitch grid without re-checking the offset. The ±24 dbu moves in trial:i04.ug.leaf_0003.02 shift by 1 × 24 dbu; this moves a wire from one allowed centerline to an adjacent allowed centerline only when the destination also satisfies (y − 48) mod 192 = 0. Before applying any y-delta to a min-width M4 track, verify the destination centerline satisfies the AUX.2 formula.

## Width Rules

M4.W.1 sets a minimum vertical (y-direction) width of 24 nm. M4.W.2 caps it at 480 nm. M4.W.3 forbids vertical widths that are even integer multiples of 24 nm (i.e., 48, 96, 144, 192, 240, 288, 336, 384, 432, 480 nm are all forbidden). M4.W.4 adds a separate prohibition on widths of 72, 168, 264, 360, and 456 nm. Together, the only compliant vertical widths from 24 nm to 480 nm are those that are odd multiples of 24 nm but not equal to 3×, 7×, 11×, 15×, or 19× 24 nm: specifically 24 nm (1×), 120 nm (5×), 216 nm (9×), 312 nm (13×), 408 nm (17×). When resizing an M4 polygon's y-extent, target one of these widths explicitly; do not rely on incremental adjustment that may pass through a forbidden multiple. The instance moves in trial:i03.ug.leaf_0002.01 and trial:i04.ug.leaf_0003.02 shift whole instances rather than reshaping individual polygons, which preserves pre-existing compliant widths without recalculating them.

M4.W.5 sets a minimum horizontal (x-direction) width of 44 nm. The x-axis end resize of polygon p957 by +172 dbu (low end) in trial:i02.ug.leaf_0001.00 produced zero new in-crop violations, consistent with the resize widening a polygon that was already at or above 44 nm. The x-axis end resizes of polygon p937 (+64 dbu low end, +320 dbu high end) in trial:i03.ug.leaf_0002.01 produced 2 new in-crop violations; those violations were accepted because connectivity was preserved, but they represent a cost to carry forward. When extending a polygon's x-extent, confirm the resulting horizontal width does not fall below 44 nm at any cross-section, particularly at narrow jogs.

## Spacing Rules

M4.S.1 requires a minimum vertical spacing of 24 nm between any two M4 polygon edges. M4.S.2 requires a minimum horizontal spacing of 40 nm between vertical M4 edges. M4.S.3 and M4.S.4 each require a 40 nm tip-to-tip spacing between M4 polygons on adjacent tracks, regardless of whether they share a parallel run length. M4.S.5 requires that when two M4 polygons on adjacent tracks do run in parallel, their parallel run length is at least 44 nm.

The y-axis instance moves in trial:i03.ug.leaf_0002.01 (±24, ±72 dbu) and trial:i04.ug.leaf_0003.02 (±24 dbu) adjusted inter-polygon vertical spacing without introducing M4.S.1 violations in those moves' own loci. A ±24 dbu move changes the gap between a moved M4 edge and a fixed neighboring M4 edge by exactly 24 dbu; if the pre-move gap is at the 24 nm minimum, a −24 dbu move will collapse it to zero and cause an M4.S.1 violation. Always check the gap to the nearest fixed M4 edge before applying a y-delta.

## No-Bend and No-Offgrid Constraints

M4.AUX.3 forbids any M4 polygon that contains a 0°–90° corner, i.e., M4 may not bend. All shapes must be axis-aligned rectangles or orthogonal rectilinear polygons without interior 90° bends. The operations recorded in the history (instance moves, x-end resizes, and via-shape resizes) do not add bends; they translate existing geometry or extend rectangular ends. Do not introduce L-shapes or T-shapes when constructing new M4 geometry; these will fail AUX.3 regardless of width or spacing compliance.

The GEOMETRY.NONORTHOGONAL rule fires on any M4 edge whose angle is not 0° or 90°. All M4 polygon edges must be strictly horizontal or strictly vertical. This constraint is consistent across all history records, none of which introduced non-orthogonal M4 edges.

## Via Enclosure Requirements

V3.M4.EN.2 requires M4 to enclose V3 by at least 11 nm on two opposite sides. V3.M4.AUX.2 further requires that V3's width perpendicular to the M4 wire direction exactly matches the M4 width in that direction (no overhang, no underrun). V4.M4.EN.1 requires M4 to enclose V4 by at least 11 nm on two opposite sides.

The via-shape resize in trial:i04.cu.def:VIA_VIA45_1_2_58_58.00 shrank the M5 shape within cell VIA_VIA45_1_2_58_58 by 88 dbu on the y-axis (low end), which indirectly reduced M4-touching violation counts by 8 in both affected windows (unit:leaf_0002 and unit:leaf_0003). The M4 improvement from adjusting a via cell's internal M5 shape indicates that enclosure and exact-width constraints on the via cell were the binding violations; resizing the landing shape resolved them without moving the via origin. When M4 enclosure violations are localized to a repeated via cell, prefer resizing the cell's internal M5 or V4 shape over moving all via instances, as trial:i04.cu demonstrates this yields consistent improvement across multiple sites simultaneously.

## Multi-Layer Coupling

Every trial that touched M4 also touched at least one neighboring routing or via layer. Trial:i02.ug.leaf_0001.00 co-modified M1, M2, and V1 alongside M4. Trial:i03.ug.leaf_0002.01 co-modified M3, M5, V3, and V4. Trial:i04.ug.leaf_0003.02 co-modified M2, M3, M5, V2, V3, and V4. Trial:i04.cu.def:VIA_VIA45_1_2_58_58.00 co-modified M5 and V4. No trial isolated M4 as the only modified layer. This pattern reflects the AUX.2 exact-width constraint and the enclosure constraints: changing M4 geometry propagates requirements to the via layers above and below it, and vice versa. Plan M4 repairs as coupled M3/M4/V3/M4/M5/V4 operations; isolated M4 edits risk introducing enclosure or exact-width violations on the adjacent via layers.

## Operation Ordering and Acceptance Criteria

All four recorded trials were accepted (three as gated_in, one as applied). The gated_in decisions required conn_preserved=true in every case. Trials that introduced new in-crop violations (n_new_in_crop=2 in trial:i03.ug.leaf_0002.01 and trial:i04.ug.leaf_0003.02) were still accepted when connectivity was preserved, indicating that a small increase in local violation count is tolerable if the net delta across windows is negative or neutral. Trial:i04.cu.def:VIA_VIA45_1_2_58_58.00 achieved delta_total=−16 by addressing violations shared across two units in a single via-cell edit, which is the most leverage-efficient repair recorded for M4.