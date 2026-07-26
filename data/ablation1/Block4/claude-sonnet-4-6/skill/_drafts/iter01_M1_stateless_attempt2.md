Based on the 10 measured trial records and the DRC rules, here is the [KNOWLEDGE] section body:

---

## Operation patterns observed on M1

All ten recorded trials on M1 were accepted (`gated_in`) with `conn_preserved=true` and zero net new violations inside or outside the crop window (`n_new_in_crop=0`, `n_new_out_of_crop=0`). The complete set of M1-touching operations across the history is: `move_instance`, `move` (polygon-level, axis-locked to x), and `resize_end` (high-end extension, x-axis). No y-axis polygon moves and no low-end resizes appear in the measured records.

## Instance moves: dominant and safe when connectivity is preserved

The most common operation applied to M1 is `move_instance` with an x-axis delta. Single-instance x-moves were confirmed clean in trial:i01.ug.Block4_union_row1.00 (+36 dbu), trial:i01.ug.Block4_union_row10.01 (+12 dbu), trial:i01.ug.leaf_0020.09 (+36 dbu), and trial:i01.ug.leaf_0021.10 (+36 dbu x, +44 dbu y). Multi-instance moves—where several instances sharing the locus are shifted by the same x delta—also cleared all M1 checks: three instances moved together in trial:i01.ug.Block4_union_row6.05 (+36 dbu each), and four instances in trial:i01.ug.Block4_union_row5.04 (three at +37, one at −36 dbu). Apply `move_instance` when the move preserves connectivity; the measured record shows it consistently produces zero new M1 violations in that condition.

## Mixed instance-move and polygon-move operations

When a crop contains both a standard cell instance and loose M1 polygons (not fully captured inside an instance boundary), the repair requires moving both the instance and the polygon. In trial:i01.ug.Block4_union_row2.02 three operations were applied together: two `move_instance` calls (+108 dbu on i0250, +28 dbu on i0163) and a single polygon x-move of +16 dbu on p1548. In trial:i01.ug.Block4_union_row7.06 two `move_instance` calls (−28 dbu each on i0158 and i0124) were combined with x-axis moves of −28 dbu on two polygons (p1596, p1477) plus a `resize_end` (high end, +172 dbu) on p1395. Both trials cleared all M1 rules. Move loose M1 polygons by the same x delta as their co-located instances when the polygons are within the same locus; the record in trial:i01.ug.Block4_union_row2.02 and trial:i01.ug.Block4_union_row7.06 shows this pairing achieves zero new violations.

## High-end resize_end on M1 polygons

`resize_end` with `end=high` on the x-axis was used in two trials. In trial:i01.ug.leaf_0008.08 p1604 was extended +92 dbu at its high end alongside a +36 dbu instance move of i0274; in trial:i01.ug.Block4_union_row7.06 p1395 was extended +172 dbu at its high end as part of a five-operation bundle. Both trials were accepted with zero new M1 violations. Extend the high end of an M1 polygon when the locus requires lengthening a segment to restore or maintain enclosure of a via; the measured outcomes in trial:i01.ug.leaf_0008.08 and trial:i01.ug.Block4_union_row7.06 confirm this is safe under the full M1 rule set when connectivity is preserved.

## Enclosure rules for V0 and V1 (V0.M1.EN.1, V0.M1.AUX.3, V1.M1.EN.1)

Rule V0.M1.EN.1 requires M1 to enclose V0 by at least 5 nm on two opposite sides (either 5 & 5 nm or 5 & 0 nm in projection). Rule V1.M1.EN.1 requires M1 to enclose V1 by 5 nm on one pair of opposite sides and 2 nm on the other pair. Rule V0.M1.AUX.3 requires V0 to match M1 width exactly in the direction perpendicular to M1's run (no V0 edge may lie off a coincident M1 edge). Every accepted trial touched both M1 and V1 layers simultaneously (trial:i01.ug.Block4_union_row1.00 through trial:i01.ug.leaf_0021.10), confirming that M1 and its enclosing-via geometry are always co-moved. Keep V0 and V1 geometry co-moved with M1 during any translate or resize operation; the consistent pattern across all ten measured trials of touching M1 together with V1 (and in trial:i01.ug.Block4_union_row7.06 also V2) and achieving zero new enclosure violations demonstrates this pairing is necessary for clean results.

## Spacing rules (M1.S.1 through M1.S.6)

M1.S.1 sets an 18 nm minimum side-to-side spacing for edges longer than 36 nm. M1.S.2 sets a 25 nm minimum tip-to-side spacing (projection) when one edge is a tip (≤ 36 nm) and the other is a side (> 36 nm). M1.S.3 sets a 27 nm minimum tip-to-tip spacing when both edges are between 24 and 36 nm. M1.S.4 and M1.S.5 set a 31 nm minimum for tip-to-tip encounters involving edges below 24 nm. M1.S.6 sets a 20 nm minimum corner-to-corner spacing. The x-axis deltas in the measured trials range from −36 dbu to +108 dbu (trial:i01.ug.Block4_union_row2.02 at +108 dbu on i0250) without producing new spacing violations, demonstrating that moves of at least one M1 grid step resolve spacing violations in these loci. The accepted delta of −36 dbu in trial:i01.ug.Block4_union_row5.04 (on i0341 while three neighbors moved +37 dbu) shows that relative displacement between adjacent instances is also a valid repair strategy under M1.S.1.

## Width and area rules (M1.W.1, M1.A.1)

M1.W.1 requires a minimum M1 width of 18 nm. M1.A.1 requires a minimum M1 area of 504 nm². The `resize_end` operations in trial:i01.ug.leaf_0008.08 (+92 dbu) and trial:i01.ug.Block4_union_row7.06 (+172 dbu) both extended M1 segments and were accepted, showing that lengthening an M1 polygon at its high end increases area and does not introduce W.1 or A.1 violations. No shrink or narrow operation appears in the measured history; avoid reducing M1 width below 18 nm or area below 504 nm² because no measured trial validates any such reduction.

## Redundant island rule (M1.R.0)

M1.R.0 flags an M1 polygon that encloses exactly one small V0 via and lies near a large empty M1 region (≥ 500 nm wide, area > 2.5 µm², expanded by 400 nm). All ten trials produced zero new M1.R.0 violations, consistent with all accepted operations being multi-polygon or multi-instance moves that preserve the broader M1 fill context rather than isolating single-via islands.

## Non-orthogonal geometry (GEOMETRY.NONORTHOGONAL)

The nonorthogonal check fires on any M1 edge with an angle not in {0°, 90°, 180°, 270°}. All M1 polygon operations in the measured history are axis-locked: `move` operations specify `axis: "x"`, and `resize_end` operations are applied to the high x-axis end only. No diagonal or rotated shape was introduced in any trial. Apply only axis-aligned x or y translations and end-extensions to M1; all ten measured trials confirm that axis-locked operations leave M1 free of nonorthogonal edges.

## Multi-layer coordination

Five of the ten trials touched only M1, M2, and V1. Trial:i01.ug.Block4_union_row7.06 additionally touched M3, M4, and V2, reflecting that a resize extending an M1 segment by +172 dbu required corresponding adjustments on the layers above. When an M1 resize propagates upward through the via stack, move or resize the affected M2–Mx and V1–Vx geometry in the same operation bundle; trial:i01.ug.Block4_union_row7.06 demonstrates this five-operation bundle clears all rules simultaneously.