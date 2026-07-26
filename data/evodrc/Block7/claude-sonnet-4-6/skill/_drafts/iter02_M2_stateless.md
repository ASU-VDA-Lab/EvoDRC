## Repair Outcomes

All 37 trials across iteration 1 (i01.ug.Block7_union_row10.00 through i01.ug.leaf_0095.26) and iteration 2 (i02.ug.Block7_union_row12.01 through i02.ug.leaf_0022.10) reached the `gated_in` decision with `conn_preserved=true`. No trial was rejected. The consistent acceptance across both design states demonstrates that preserving connectivity while adjusting instance positions and polygon endpoints is a reliable M2 repair strategy for this design.

## Operation Types and Their Roles

Four operation classes act on M2 geometry: `move_instance`, `resize_end`, `resize`, and `add_polygon` (with `move` used for standalone polygons). These appear in different combinations depending on the severity and character of the violation.

`move_instance` is the primary correction. Trials where only instance moves appear — trial:i01.ug.Block7_union_row11.01 (two moves), trial:i01.ug.leaf_0001.22 (one move of +108 dbu), trial:i02.ug.leaf_0022.10 (one move of +3 dbu), trial:i02.ug.Block7_union_row12.01 (three moves of +36 dbu) — confirm that when polygon geometry is otherwise clean, instance repositioning alone resolves the spacing deficit.

`resize_end` appears alongside `move_instance` when an instance shift cannot bring a polygon endpoint into compliance by itself. Trials trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row14.04, trial:i01.ug.Block7_union_row17.07, trial:i01.ug.Block7_union_row18.08, trial:i01.ug.Block7_union_row24.14, trial:i02.ug.Block7_union_row9.06, trial:i02.ug.Block7_union_row20.04, and trial:i02.ug.Block7_union_row22.05 all pair instance moves with targeted `resize_end` on specific polygon ids. Apply `resize_end` when the polygon tip or side end is the proximate cause of the violation.

`resize` (without end-specification) applies a symmetric or uniform adjustment. Trial:i01.ug.Block7_union_row15.05 resizes polygon p3586 by +160 dbu along x. Trial:i01.ug.Block7_union_row19.09 applies uniform x-resizes to polygons p3619 (+40 dbu), p3654 (-72 dbu), and p3523 (+72 dbu). Trial:i02.ug.Block7_union_row15.03 resizes polygon p3592 by +96 dbu along y. Use `resize` when both ends of a polygon segment must move equally rather than one end being fixed.

`add_polygon` was applied once, in trial:i01.ug.Block7_union_row20.10, inserting a new M2 rectangle defined by points [[5992,22824],[5992,22896],[6048,22896],[6048,22824]], yielding dimensions 56 nm × 72 nm. Both dimensions satisfy M2.W.1 (minimum 18 nm width) and the combined area of 4032 nm² satisfies M2.A.1 (minimum 504 nm²). Apply `add_polygon` only when neither instance repositioning nor endpoint extension resolves the connectivity gap; verify all spacing rules against neighboring polygons before inserting.

## Lateral (X-direction) Move Magnitudes

X-direction moves dominate the history. At 1 dbu = 1 nm, the most frequent single move magnitude is 36 nm, appearing in trial:i01.ug.Block7_union_row11.01, trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row14.04, trial:i01.ug.Block7_union_row15.05, trial:i01.ug.Block7_union_row17.07, trial:i01.ug.Block7_union_row23.13, trial:i02.ug.Block7_union_row12.01, trial:i02.ug.Block7_union_row13.02, trial:i02.ug.Block7_union_row20.04, trial:i02.ug.Block7_union_row22.05, trial:i01.ug.leaf_0002.23, and many others. A 36 nm shift equals twice M2.W.1 (18 nm) and equals M2.S.1 (18 nm side-to-side spacing), making it the canonical minimum correction for a side-edge spacing violation where the full minimum clearance is needed.

40 nm x-moves appear in trial:i01.ug.Block7_union_row19.09 and trial:i01.ug.Block7_union_row9.21. The 40 nm shift exceeds both M2.S.1 (18 nm) and M2.S.2 (25 nm tip-to-side spacing), providing clearance when the violating pair includes a side edge (length >36 nm) adjacent to a tip edge (length ≤36 nm).

52 nm moves appear in trial:i01.ug.Block7_union_row10.00 and trial:i01.ug.Block7_union_row14.04. 56 nm moves appear in trial:i01.ug.Block7_union_row3.15 (via resize_end) and trial:i01.ug.Block7_union_row8.20.

72 nm x-moves appear in trial:i01.ug.Block7_union_row18.08, trial:i01.ug.Block7_union_row23.13, trial:i01.ug.Block7_union_row19.09, and trial:i02.ug.Block7_union_row20.04. A 72 nm shift is four times M2.S.1, appropriate when a wide cluster of instances must clear a local spacing zone to avoid cascading violations.

108 nm x-moves appear in trial:i01.ug.leaf_0001.22, trial:i01.ug.leaf_0008.24, trial:i01.ug.Block7_union_row7.19, and trial:i01.ug.Block7_union_row14.04. 136 nm moves appear in trial:i01.ug.Block7_union_row13.03 and trial:i01.ug.Block7_union_row15.05. These large displacements are applied when an instance must clear a compound violation zone involving multiple overlapping spacing rules or must make room for a substantial polygon extension.

Negative x-moves are applied when the repair target is to the left: -36 nm in trial:i01.ug.Block7_union_row16.06, trial:i01.ug.Block7_union_row13.02 (-72 nm), trial:i01.ug.Block7_union_row18.08 (-72 nm), and trial:i01.ug.leaf_0024.25 (-24 nm and -108 nm). Negative moves serve the same DRC purpose as positive moves; direction is determined by which neighboring polygon creates the violation and whether moving in the positive direction would create new violations against the far neighbor.

## Resize_end Magnitudes and Axis

The minimum effective x-axis resize_end magnitude observed is +56 nm, appearing on polygon p3273 (trial:i01.ug.Block7_union_row12.02), p3384 (trial:i01.ug.Block7_union_row3.15), p3526 (trial:i01.ug.Block7_union_row13.03 low end), p3187 (trial:i01.ug.Block7_union_row17.07), p3430 (trial:i01.ug.Block7_union_row8.20), and p3048 (trial:i02.ug.Block7_union_row20.04). A 56 nm resize clears M2.S.3 (27 nm tip-to-tip, both edges 24–36 nm), M2.S.4 (31 nm tip-to-tip, both edges <24 nm), and M2.S.5 (31 nm mixed tip-to-tip) with margin. Apply 56 nm as the minimum resize_end for tip-spacing violations.

Larger resize_end deltas are used when the polygon requires a longer extension: +60 nm on p3532 (trial:i01.ug.Block7_union_row18.08), +72 nm on p3200 (trial:i01.ug.Block7_union_row14.04), +92 nm on p3737 and p3746 (trial:i01.ug.Block7_union_row5.17) and on p3527 (trial:i02.ug.Block7_union_row22.05), +100 nm on p3526 high end (trial:i01.ug.Block7_union_row13.03), +112 nm on p3683 (trial:i02.ug.Block7_union_row9.06), +120 nm on p3635 (trial:i01.ug.Block7_union_row24.14), +128 nm on p3317 (trial:i01.ug.Block7_union_row7.19) and p3564 (trial:i01.ug.Block7_union_row24.14), +136 nm on p3058 (trial:i01.ug.Block7_union_row24.14), +160 nm on p3586 (trial:i01.ug.Block7_union_row15.05), +192 nm on p3525 (trial:i01.ug.Block7_union_row13.03), and +308 nm on p3286 (trial:i01.ug.Block7_union_row10.00).

The +308 nm resize_end on p3286 (trial:i01.ug.Block7_union_row10.00) is the largest polygon extension observed. Extensions of this magnitude are consistent with M2.S.7, which requires parallel run length ≥35 nm when side-to-side spacing is ≤32 nm. When a short M2 segment falls into a side-constrained region, extending its endpoint by a large delta is the mechanism for achieving compliant run length.

A single y-axis resize_end appears: +96 nm on p3592 along y in trial:i02.ug.Block7_union_row15.03, accompanied by a -84 nm y-move of instance i1062. This combination — vertical polygon growth paired with an instance shift — indicates a case where a vertically oriented M2 segment needed span extension while its driving instance was repositioned.

## Vertical (Y-direction) Moves

Y-direction corrections appear in six trials. Trials trial:i01.ug.Block7_union_row16.06 and trial:i02.ug.leaf_0014.08 both apply -12 nm y-moves: trial:i01.ug.Block7_union_row16.06 moves instances i0336 and i0308 each by [0,-12] and moves polygon p3516 by -12 nm along y; trial:i02.ug.leaf_0014.08 moves instances i0519 and i0524 by [0,-12] and moves polygon p3515 by -12 nm along y. Both trials touch M1, M2, M3, V1, and V2. The -12 nm correction resolves minor vertical enclosure mismatches, consistent with marginal V1.M2.EN.2 or V2.M2.EN.1 deficits.

Trial:i02.ug.leaf_0001.07 moves instance i1643 and polygon p3383 each by -57 nm along y, touching M2, M3, and V2 (no M1 or V1). This larger 57 nm shift corrects a more substantial vertical enclosure deficit or spacing issue on the M2/M3/V2 stack in the leaf_0001 region.

Trial:i01.ug.Block7_union_row19.09 moves instance i0949 by [0,-48]. Trial:i01.ug.leaf_0095.26 moves instances i0177 and i0184 each by [0,+48], applies resize_end +68 nm on p2432 along y (high end), and resize_end +48 nm on p3537 along y (high end), touching M1, M2, M3, V1, and V2. Trial:i02.ug.Block7_union_row15.03 moves instance i1062 by [0,-84] and resizes p3592 along y by +96 nm.

Apply y-direction moves when the violation involves vertical enclosure of V1 by M2 (V1.M2.EN.2: 5 nm on two opposite sides) or vertical enclosure of V2 by M2 (V2.M2.EN.1: 5 nm on at least two opposite sides). Apply the y-move simultaneously to all affected instances and polygons in the local stack to maintain alignment across layers.

## Multi-layer Coordination

When touched_layers includes M3 and V2, the repair applies y-direction moves rather than (or in addition to) x-direction moves. Trials trial:i01.ug.Block7_union_row16.06, trial:i01.ug.leaf_0095.26, trial:i02.ug.leaf_0001.07, and trial:i02.ug.leaf_0014.08 all touch M2+M3+V2 and all include y-direction corrections. Move the M2 segment, V2 via, and M3 segment in the same direction and by the same magnitude in a single operation set — do not move M2 in isolation from its connected V2 and M3 elements. Trial:i02.ug.leaf_0001.07 demonstrates this: both instance i1643 and polygon p3383 receive exactly -57 nm y. Trial:i02.ug.leaf_0014.08 demonstrates the same pattern with -12 nm applied uniformly to instances i0519, i0524, and polygon p3515.

## Connectivity Preservation

All 37 trials achieve conn_preserved=true (trial:i01.ug.Block7_union_row10.00 through trial:i02.ug.leaf_0022.10). Do not apply any move or resize that breaks a net connection through V1 or V2. V1.M2.EN.2 requires 5 nm enclosure on two opposite sides of every V1 via. V1.M2.AUX.2 requires V1 width to equal M2 width in the direction perpendicular to M2 length. V2.M2.EN.1 requires 5 nm enclosure on at least two opposite sides of every V2 via.

All resize_end operations observed in the history extend polygon ends (positive delta in all cases: trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row13.03, trial:i01.ug.Block7_union_row14.04, trial:i01.ug.Block7_union_row17.07, trial:i01.ug.Block7_union_row18.08, trial:i01.ug.Block7_union_row24.14, trial:i02.ug.Block7_union_row9.06, trial:i02.ug.Block7_union_row20.04, trial:i02.ug.Block7_union_row22.05, and others). No shrinking of a polygon endpoint appears anywhere in the measured history. Shrinking an M2 endpoint risks pulling the polygon edge past a V1 or V2 via, dropping enclosure below 5 nm and breaking connectivity.

## n_new_in_crop Behavior

The gating rule accepts a repair when conn_preserved=true regardless of n_new_in_crop. Trials with n_new_in_crop > 0 that were still gated_in: trial:i01.ug.Block7_union_row13.03 (n=1), trial:i01.ug.Block7_union_row19.09 (n=1), trial:i01.ug.Block7_union_row21.11 (n=9), trial:i01.ug.Block7_union_row22.12 (n=2), trial:i01.ug.Block7_union_row24.14 (n=2), trial:i01.ug.Block7_union_row4.16 (n=1), trial:i01.ug.Block7_union_row5.17 (n=1), trial:i01.ug.leaf_0002.23 (n=2), trial:i01.ug.leaf_0024.25 (n=1), trial:i02.ug.leaf_0017.09 (n=3), trial:i02.ug.leaf_0022.10 (n=3). New in-crop violations introduced by a repair are carried forward for resolution in subsequent iterations. Connectivity preservation outweighs new spacing violations in the acceptance criterion.

The n_new_in_crop=9 case (trial:i01.ug.Block7_union_row21.11) involved only two instance moves of +36 nm each, which shifts a large number of downstream polygon relationships and can ripple new violations into the crop window. Large n_new_in_crop values do not indicate that the operations were wrong; they reflect that dense regions generate many secondary interactions when instances are displaced.

## M2.S.7 Parallel Run Length

M2.S.7 forbids a tip-to-tip gap of 18 nm co-located with a side-to-side spacing ≤32 nm, and requires parallel run length ≥35 nm when side spacing is ≤32 nm. The very large resize_end deltas — +192 nm on p3525 (trial:i01.ug.Block7_union_row13.03), +308 nm on p3286 (trial:i01.ug.Block7_union_row10.00) — are consistent with forcing a short M2 stub into the ≥35 nm run-length window. When a polygon segment is adjacent to a neighbor within 32 nm, extend the polygon end by at least enough to achieve 35 nm of overlap length with that neighbor.

## M2.A.1 Area Compliance

The only `add_polygon` in the history (trial:i01.ug.Block7_union_row20.10) uses 56 nm × 72 nm = 4032 nm², which exceeds M2.A.1 (504 nm²) by nearly 8×. A minimum-width square of 18 nm × 18 nm = 324 nm² fails M2.A.1. A rectangle of at least ~22.5 nm × 22.5 nm is the minimum that satisfies M2.A.1 alone, but it would also need to satisfy M2.W.1 on both sides. Use 56 nm × 72 nm or larger as the reference patch size when adding M2 geometry, since this is the only measured example.

## M2.S.6 Corner-to-Corner Spacing

M2.S.6 requires 20 nm Euclidean corner-to-corner spacing, which is stricter than the 18 nm projection-based M2.S.1 side spacing. The 4 nm instance move in trial:i01.ug.Block7_union_row22.12 (instance i0132, n_new_in_crop=2 accepted) and the 3 nm instance move in trial:i02.ug.leaf_0022.10 (instance i0100, n_new_in_crop=3 accepted) are sub-36 nm fine-grain moves. Both introduced new crop violations, indicating that a 3–4 nm nudge shifts one corner pair past the 20 nm Euclidean threshold while creating marginal violations elsewhere. Sub-4 nm moves are effective for targeted M2.S.6 corner clearance but generate secondary violations for subsequent iterations.

## Summary of Prescriptive Repair Actions

Apply a 36 nm x-direction instance move as the default first correction for M2.S.1 side-to-side spacing violations (trial:i01.ug.Block7_union_row11.01, trial:i02.ug.Block7_union_row12.01, and numerous others). Apply 40 nm when the violating pair involves a tip edge ≤36 nm abutting a side edge >36 nm, targeting M2.S.2 (trial:i01.ug.Block7_union_row9.21). Apply 56 nm resize_end as the minimum polygon tip extension to clear M2.S.3, M2.S.4, and M2.S.5 (trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row3.15, trial:i02.ug.Block7_union_row20.04). Apply 92–308 nm resize_end when run-length constraints under M2.S.7 require substantial polygon growth (trial:i01.ug.Block7_union_row13.03, trial:i01.ug.Block7_union_row10.00, trial:i01.ug.Block7_union_row24.14). Apply y-direction moves uniformly across all co-located instances and polygons when vertical enclosure deficits arise in M2+M3+V2 stacks (trial:i01.ug.Block7_union_row16.06, trial:i02.ug.leaf_0001.07, trial:i02.ug.leaf_0014.08). Insert an `add_polygon` patch of at least 56 nm × 72 nm when no existing polygon can bridge an M2 connectivity gap (trial:i01.ug.Block7_union_row20.10).