**Acceptance criterion**

Accept a trial when conn_preserved is true and n_new_out_of_crop equals zero; new violations confined to the crop (n_new_in_crop > 0) do not block acceptance. trial:i01.ug.Block7_union_row21.11 carries n_new_in_crop=9 and is accepted; trial:i01.ug.Block7_union_row13.03 carries n_new_in_crop=1 and is accepted. All 27 iteration-1 trials satisfy this criterion and are gated in.

**Operation vocabulary**

M2 repair trials use three polygon-level operation types: move_instance, resize_end, and polygon move (op:"move"). trial:i01.ug.Block7_union_row9.21 applies resize_end (p3300, axis x, end low, delta -36 dbu) and a polygon move (p2720, axis x, delta +56 dbu) within the same accepted 9-op trial, confirming both are valid on M2 polygons. Apply resize_end when one endpoint of an M2 polygon must shift independently of instance translation. Apply the polygon move op when the entire M2 polygon must translate.

**resize_end paired with move_instance**

When a move_instance alone cannot satisfy M2 width, spacing, or via-enclosure rules because the polygon boundary must shift beyond what instance placement controls, apply resize_end on the relevant M2 polygon in the same trial as the move_instance ops. trial:i01.ug.Block7_union_row10.00 pairs move_instance [+4, 0] dbu with resize_end +50 dbu on p3305 (axis x, end high). trial:i01.ug.leaf_0002.23 pairs move_instance [+72, 0] dbu with resize_end +128 dbu on p3695 (axis x, end high). trial:i01.ug.leaf_0008.24 pairs two move_instance ops with resize_end +164 dbu on p3771 (axis x, end high). trial:i01.ug.Block7_union_row12.02 applies resize_end on both x (p3273, +56 dbu, end high) and y (p3694, +8 dbu end high and -8 dbu end low) alongside five move_instance ops. trial:i01.ug.Block7_union_row3.15 pairs move_instance [-36, 0] with resize_end +49 dbu on p3379 (axis x, end high). trial:i01.ug.leaf_0024.25 combines move_instance [+72, +44] with resize_end on p3538 (axis x, +36 dbu end high; axis y, +44 dbu end high) and resize_end on p3706 (axis x, +52 dbu end low).

**resize_end delta is set independently of move_instance delta**

The resize_end delta and the paired move_instance delta are chosen independently to satisfy DRC rule clearances; they need not be equal and need not both be multiples of the same grid. trial:i01.ug.Block7_union_row10.00 uses move_instance +4 dbu x alongside resize_end +50 dbu x. trial:i01.ug.Block7_union_row3.15 uses move_instance -36 dbu x alongside resize_end +49 dbu x. Set each delta to the value that closes the specific DRC violation, not to a fixed step.

**Move step sizes**

The dominant x-axis move_instance step is ±36 dbu, used across the majority of accepted trials: trial:i01.ug.Block7_union_row11.01, trial:i01.ug.Block7_union_row15.05, trial:i01.ug.Block7_union_row16.06, trial:i01.ug.Block7_union_row18.08, trial:i01.ug.Block7_union_row20.10, trial:i01.ug.Block7_union_row22.12, trial:i01.ug.Block7_union_row23.13, trial:i01.ug.Block7_union_row24.14, and others. Fine-tuning moves of ±4 dbu are also accepted: trial:i01.ug.Block7_union_row10.00 (move_instance +4 dbu x) and trial:i01.ug.leaf_0001.22 (move_instance +4 dbu x). Larger moves (64, 72, 108 dbu x) are used when instances must clear a wider gap: trial:i01.ug.Block7_union_row7.19 (move_instance +108 dbu x on i1446), trial:i01.ug.Block7_union_row8.20 (move_instance +64 dbu x on i1405 and i1921), trial:i01.ug.Block7_union_row9.21 (move_instance +108 dbu x on i1117). Y-axis moves of 8 to 64 dbu are accepted when vertical adjustment is required: trial:i01.ug.Block7_union_row12.02 (±8 dbu y), trial:i01.ug.Block7_union_row14.04 (+64 dbu y on i0894 and i0920).

**Opposing moves within one crop**

Trials that move instances in opposite x directions within the same crop are accepted. trial:i01.ug.Block7_union_row16.06 moves i0407 and i0928 by -36 dbu x while moving i0320 by +40 dbu x. trial:i01.ug.Block7_union_row20.10 moves i0753 by -44 dbu x and i0263 by +40 dbu x. trial:i01.ug.Block7_union_row19.09 moves i0771 by +37 dbu x while moving i0026 and i0294 by -37 dbu x. Use opposing moves within a crop to open spacing simultaneously on two sides of an M2 DRC hotspot.

**Multi-layer crop scope**

All 27 accepted trials touch M1, M2, and V1 as a minimum layer set. Do not restrict M2 repair crops to M2 alone; always include M1 and V1. Trials requiring additional M3 and V2 edits tend to have higher op counts: trial:i01.ug.Block7_union_row12.02 (9 ops, touches M3 and V2), trial:i01.ug.Block7_union_row9.21 (9 ops, touches M3 and V2), trial:i01.ug.Block7_union_row14.04 (8 ops, touches M3 and V2). trial:i01.ug.Block7_union_row13.03 and trial:i01.ug.Block7_union_row19.09 also touch M3 and V2 with 5 ops each.