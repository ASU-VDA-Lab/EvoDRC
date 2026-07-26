## Move Step Quanta

The dominant instance-move step is 36 dbu. It appears across the majority of accepted trials: trial:i01.ug.Block7_union_row11.01 (two instances each +36 x), trial:i01.ug.Block7_union_row12.02 (+36 for i1208), trial:i01.ug.Block7_union_row17.07 (four moves of +36 x), trial:i02.ug.Block7_union_row12.01 (three moves of +36 x), trial:i03.ug.Block7_union_row13.01 (two moves of +36 x), trial:i03.ug.Block7_union_row20.02 (one move of +36 x). Multiples of 36 appear when the spacing gap is larger: +72 for three instances in trial:i01.ug.Block7_union_row18.08, +108 in trial:i01.ug.leaf_0001.22, -108 in trial:i01.ug.leaf_0024.25 and trial:i04.ug.leaf_0004.03 (-56), +136 in trial:i01.ug.Block7_union_row15.05 and trial:i01.ug.Block7_union_row24.14.

Avoid move steps smaller than 36 dbu. Trial:i01.ug.Block7_union_row22.12 applies a +4 dbu move and records n_new_in_crop:2. Trial:i02.ug.leaf_0022.10 applies a +3 dbu move and records n_new_in_crop:3. Both were gated_in only because conn_preserved was true and n_new_out_of_crop was 0; the sub-36-dbu moves introduced new M1 violations in each case.

Move steps of 40 dbu appear without introducing violations when applied uniformly across all instances in the row. Trial:i01.ug.Block7_union_row9.21 moves five instances simultaneously by +40 dbu each and records n_new_in_crop:0. Trial:i01.ug.Block7_union_row7.19 applies +40 for i1442 alongside +108 for i1446 with n_new_in_crop:0.

## Coordinated Multi-Instance Moves

When a repair shifts M1 routing through a shared locus, all affected instances are moved by a consistent delta in the same trial. Trial:i01.ug.Block7_union_row9.21 moves five instances each +40 dbu with n_new_in_crop:0. Trial:i01.ug.Block7_union_row6.18 moves six instances by +28 to +36 dbu with n_new_in_crop:0. Trial:i01.ug.Block7_union_row14.04 applies eleven operations across nine instances and two polygon resizes with n_new_in_crop:0. Trial:i01.ug.Block7_union_row23.13 moves six instances by -36 to +108 dbu with n_new_in_crop:0.

Single-instance moves over wide loci produce the highest new-violation counts. Trial:i04.ug.leaf_0006.05 spans a locus of x=[1728,28728], y=[2068,28172] — approximately the full block extent — and a single instance move of -108 dbu yields n_new_in_crop:173. Trial:i04.ug.leaf_0007.06 spans x=[1728,28728], y=[3148,27092] and a single instance move of (0,+48) yields n_new_in_crop:48. By contrast, trial:i01.ug.Block7_union_row11.01 uses a narrow locus (x=[15928,26496], y=[13068,13932]) with two coordinated +36 moves and produces n_new_in_crop:0.

## resize_end Paired with move_instance

When a move_instance shifts an M1 polygon end relative to an underlying V0 or V1, a resize_end on the affected polygon corrects the enclosure gap. The pairing is consistent across multiple trials:

- trial:i01.ug.Block7_union_row3.15: move_instance -36 on i1891, then resize_end +56 low-x on p3430 (n_new_in_crop:0).
- trial:i01.ug.Block7_union_row17.07: move_instance +36 on four instances, then resize_end +56 low-x on p3187 (n_new_in_crop:0).
- trial:i02.ug.Block7_union_row9.06: move_instance +56 on i1150, then resize_end +112 high-x on p3683 (n_new_in_crop:0).
- trial:i01.ug.Block7_union_row8.20: move_instance -36 on i1891, then resize_end +56 low-x on p3430 (n_new_in_crop:0).
- trial:i01.ug.Block7_union_row24.14: move_instance +136 on i0215, then resize_end +136 high-x on p3058; move_instance +64 on i0561, then resize_end +120 high-x on p3635; resize_end +128 high-x on p3564 (n_new_in_crop:2, gated_in).

The resize_end delta is not constrained to 36 dbu. Observed resize_end amounts in successful trials include 52, 56, 60, 72, 92, 112, 120, 128, 136, 160, 192 dbu, because the endpoint position is determined by the enclosure gap to the via, not by the instance placement grid.

## Adjusting Both Ends of an M1 Polygon in One Trial

When an M1 polygon must correct enclosure at both ends simultaneously, low-end and high-end resize_end operations appear in the same trial. Trial:i01.ug.Block7_union_row13.03 applies resize_end low-x -56 and resize_end high-x +100 to polygon p3526, and also resize_end high-x +192 on p3525, in a single trial (n_new_in_crop:1, gated_in). Trial:i03.ug.leaf_0007.05 applies resize_end low-x +72, resize_end low-y -48, and resize_end high-y -48 to polygon p3592 in one trial. Trial:i01.ug.Block7_union_row10.00 applies resize_end high-x +308 on p3286 and resize_end low-x +180 and resize_end high-x +56 on p3751 across the same trial.

## Uniform resize Operations

Uniform resize operations (op:"resize", no "end" field) that move both ends equally appear in three trials. Trial:i01.ug.Block7_union_row15.05 applies resize x +160 on p3586. Trial:i01.ug.Block7_union_row19.09 applies resize x +40 on p3619, resize x -72 on p3654, and resize x +72 on p3523 within the same trial — two polygons grow and one shrinks. Trial:i02.ug.Block7_union_row15.03 applies resize y +96 on p3592 (n_new_in_crop:0). Polygon p3592 recurs across iterations: it receives resize y +96 in trial:i02.ug.Block7_union_row15.03 and then resize_end low-x +72, resize_end low-y -48, resize_end high-y -48 in trial:i03.ug.leaf_0007.05, showing that a uniform resize in one iteration can be followed by asymmetric endpoint corrections in a subsequent iteration.

## Y-Direction Move Quanta

Y-direction moves on M1 polygons and instances appear in two distinct step sizes.

**12 dbu y-step**: Trial:i01.ug.Block7_union_row16.06 moves two instances by (0,-12) and translates polygon p3516 by y -12 (n_new_in_crop:0, touched layers M1, M2, M3, V1, V2). Trial:i02.ug.leaf_0014.08 moves two instances by (0,-12) and translates polygon p3515 by y -12 (n_new_in_crop:0, touched layers M1, M2, M3, V1, V2). Both 12-dbu y-step trials produce zero new violations.

**48 dbu y-step**: Trial:i01.ug.leaf_0095.26 moves two instances by (0,+48) and applies resize_end +68 high-y on p2432 and resize_end +48 high-y on p3537 (n_new_in_crop:0). Trial:i03.ug.leaf_0011.07 moves two instances by (0,-48) with one offset by an additional x=-16, and applies resize_end -48 high-y on p3537 (n_new_in_crop:0, touched layers M1, M2, M3, V1, V2). Trial:i04.ug.leaf_0007.06 applies (0,+48) to a single instance over a full-block locus and yields n_new_in_crop:48 (gated_in, conn_preserved). Trial:i01.ug.Block7_union_row19.09 applies (0,-48) to i0949 as part of a mixed x/y multi-instance repair (n_new_in_crop:1).

The 12-dbu y step is consistently zero-violation. The 48-dbu y step produces no new violations when at least two instances and a polygon resize are coordinated in a narrow locus (trial:i01.ug.leaf_0095.26, trial:i03.ug.leaf_0011.07), but produces n_new_in_crop:48 when applied as a single-instance wide-locus move (trial:i04.ug.leaf_0007.06).

## Polygon-Level Moves (op:"move")

Two trials move individual M1 polygons directly rather than through instance moves. Trial:i01.ug.Block7_union_row16.06 moves polygon p3516 by y -12 (n_new_in_crop:0). Trial:i02.ug.leaf_0014.08 moves polygon p3515 by y -12 (n_new_in_crop:0). Both polygon-level moves are y-axis translations of 12 dbu and appear alongside (0,-12) instance moves within the same trial, coordinating the polygon geometry with the instance positions.

## Iterative Re-Repair: Convergence Pattern

Several units required repair across multiple iterations, with op count and locus width decreasing each time:

- Block7_union_row10: trial:i01.ug.Block7_union_row10.00 (6 ops, locus x-span ~9700 dbu, n_new_in_crop:0); trial:i03.ug.Block7_union_row10.00 (2 ops, locus x-span ~3100 dbu, n_new_in_crop:0).
- Block7_union_row13: trial:i01.ug.Block7_union_row13.03 (6 ops, n_new_in_crop:1); trial:i02.ug.Block7_union_row13.02 (3 ops, n_new_in_crop:0); trial:i03.ug.Block7_union_row13.01 (2 ops, n_new_in_crop:0).
- Block7_union_row20: trial:i01.ug.Block7_union_row20.10 (2 ops, n_new_in_crop:0); trial:i02.ug.Block7_union_row20.04 (3 ops, n_new_in_crop:0); trial:i03.ug.Block7_union_row20.02 (1 op, n_new_in_crop:0).
- leaf_0004: trial:i04.ug.leaf_0004.03 (1 op, -56 x, n_new_in_crop:0); trial:i05.ug.leaf_0004.03 (1 op, (-96,-48), n_new_in_crop:1).

The final iteration on each unit uses fewer operations than earlier iterations, with the locus narrowing to the residual violation site.

## Gate Condition: conn_preserved

All 46 trials in the history are accepted (decision:gated_in) with conn_preserved:true and n_new_out_of_crop:0. The gate accepts trials regardless of n_new_in_crop when connectivity is preserved and no violations escape the crop boundary. Accepted n_new_in_crop values include 0 (the majority), 1 (trial:i01.ug.Block7_union_row13.03, trial:i01.ug.Block7_union_row4.16, trial:i01.ug.Block7_union_row5.17, trial:i03.ug.leaf_0008.06), 2 (trial:i01.ug.Block7_union_row22.12, trial:i01.ug.Block7_union_row24.14), 3 (trial:i02.ug.leaf_0017.09, trial:i02.ug.leaf_0022.10, trial:i03.ug.leaf_0007.05), 9 (trial:i01.ug.Block7_union_row21.11), 48 (trial:i04.ug.leaf_0007.06), and 173 (trial:i04.ug.leaf_0006.05). No trial in the history was rejected.

## add_polygon Operations

Two trials include polygon additions, both on layers above M1. Trial:i01.ug.Block7_union_row20.10 adds an M2 polygon at coordinates [[5992,22824],[5992,22896],[6048,22896],[6048,22824]] (a 56x72 dbu rectangle) alongside one M1 instance move of -36 dbu (n_new_in_crop:0). Trial:i03.ug.leaf_0002.04 adds an M3 polygon at [[11664,11756],[11664,11828],[11908,11828],[11908,11756]] (a 244x72 dbu rectangle) alongside M1 instance moves of +68 and +172 dbu and an M1 resize_end of -88 low-x and +20 high-y on p3300 (n_new_in_crop:0, touched layers M1, M2, M3, V1, V2). No trial in the history adds an M1 polygon via add_polygon.

## Multi-Layer Context

All trials in the history touch at least M1, M2, and V1 together. Eight trials also include M3 and V2: trial:i01.ug.Block7_union_row16.06, trial:i01.ug.leaf_0095.26, trial:i02.ug.leaf_0014.08, trial:i03.ug.leaf_0002.04, trial:i03.ug.leaf_0011.07. These are the same trials that use y-direction moves of 12 or 48 dbu, or that include add_polygon on M3. M1-only geometric changes (move_instance, resize_end, resize, move on M1 polygons) appear in all trials regardless of whether M3/V2 are co-touched; the additional layers do not change the form of M1 operations within the trial.