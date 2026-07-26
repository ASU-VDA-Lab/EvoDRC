## Operation patterns on M1

The dominant repair primitive across all 26 recorded units is `move_instance`. The most common lateral x-displacement is 36 dbu, observed in trials trial:i01.ug.Block7_union_row10.00, trial:i01.ug.Block7_union_row11.01, trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row15.05, trial:i01.ug.Block7_union_row18.08, trial:i01.ug.Block7_union_row20.10, trial:i01.ug.Block7_union_row22.12, trial:i01.ug.Block7_union_row23.13, trial:i01.ug.Block7_union_row24.14, trial:i01.ug.Block7_union_row4.16, trial:i01.ug.Block7_union_row5.17, trial:i01.ug.Block7_union_row8.20, trial:i01.ug.Block7_union_row9.21. The 36 dbu step equals the sum of the M1.W.1 minimum width (18 nm) and the M1.S.1 minimum side-to-side spacing (18 nm), placing it at exactly one minimum M1 wire pitch. Use 36 dbu as the default lateral step for M1 instance repositioning (trial:i01.ug.Block7_union_row11.01, trial:i01.ug.Block7_union_row15.05, trial:i01.ug.Block7_union_row18.08).

Negative x-displacements of -36 dbu are applied when a shift toward lower x resolves the violation: trial:i01.ug.Block7_union_row10.00 (instances i1811, i1180), trial:i01.ug.Block7_union_row16.06 (instances i0407, i0928), trial:i01.ug.Block7_union_row5.17 (instance i1518), trial:i01.ug.Block7_union_row9.21 (instance i1891). The same 36 dbu pitch grid applies in both directions.

Larger x-displacements—40 (trial:i01.ug.Block7_union_row16.06 instance i0320, trial:i01.ug.Block7_union_row7.19 instance i1442), 56 (trial:i01.ug.Block7_union_row9.21 instances i1168, i1271), 64 (trial:i01.ug.Block7_union_row8.20 instances i1405, i1921), 72 (trial:i01.ug.leaf_0002.23 instance i1646, trial:i01.ug.leaf_0095.26 instance i0175), and 108 dbu (trial:i01.ug.Block7_union_row7.19 instance i1446, trial:i01.ug.Block7_union_row9.21 instance i1117)—occur when multiple wire tracks or wider M1.S.1/M1.S.2 gaps need to be cleared in the same operation.

A single instance of the `move` polygon operation (not `resize_end`) was applied directly to polygon p2720 in trial:i01.ug.Block7_union_row9.21 with axis=x delta=+56 dbu, translating the entire polygon rather than stretching an endpoint.

## resize_end on M1 polygons

`resize_end` operations stretch or retract a single endpoint of an M1 polygon and consistently accompany `move_instance` calls in the same trial. Apply `resize_end` on the M1 polygon end nearest the moved instance to maintain enclosure of any V0 or V1 via that instance carries (trial:i01.ug.Block7_union_row3.15, trial:i01.ug.leaf_0008.24, trial:i01.ug.Block7_union_row24.14).

Observed axis=x end=high (extending the high-x endpoint) delta values:
- 4 dbu: trial:i01.ug.Block7_union_row13.03 (p3526)
- 16 dbu: trial:i01.ug.Block7_union_row7.19 (p3317)
- 36 dbu: trial:i01.ug.Block7_union_row24.14 (p3058), trial:i01.ug.leaf_0024.25 (p3538)
- 48 dbu: trial:i01.ug.Block7_union_row14.04 (p3200)
- 49 dbu: trial:i01.ug.Block7_union_row3.15 (p3379)
- 50 dbu: trial:i01.ug.Block7_union_row10.00 (p3305)
- 52 dbu: trial:i01.ug.leaf_0024.25 (p3706, end=low)
- 56 dbu: trial:i01.ug.Block7_union_row12.02 (p3273)
- 128 dbu: trial:i01.ug.leaf_0002.23 (p3695)
- 164 dbu: trial:i01.ug.leaf_0008.24 (p3771)

Non-multiples of 36 (49, 50, 52 dbu) arise when the enclosure margin demanded by V0.M1.EN.1 (5 nm minimum on two opposite sides) or V1.M1.EN.1 (5 nm + 2 nm on two opposite sides) dictates a fine adjustment rather than a pitch-aligned step: trial:i01.ug.Block7_union_row3.15 (resize +49 after instance move -36), trial:i01.ug.Block7_union_row10.00 (resize +50 alongside mixed ±36 moves).

Low-end retraction (axis=x end=low) occurs in trial:i01.ug.Block7_union_row9.21 (delta=-36 on p3300) and trial:i01.ug.leaf_0024.25 (delta=+52 on p3706 with end=low, advancing the low endpoint inward). Apply end=low retraction when the low-x edge of an M1 polygon must be pulled back to clear an M1.S.1 or M1.S.2 spacing violation after adjacent instances shift.

Y-axis `resize_end` calls appear in three trials:
- trial:i01.ug.Block7_union_row12.02: p3694 receives both end=high delta=+8 and end=low delta=-8, symmetrically widening the polygon by 8 dbu on each side.
- trial:i01.ug.Block7_union_row14.04: p3576 receives end=high delta=+64.
- trial:i01.ug.leaf_0024.25: p3538 receives end=high delta=+44 (in addition to an x-axis resize), and p2333 receives end=high delta=+20.

## Enclosure repair (V0.M1.EN.1, V0.M1.AUX.3, V1.M1.EN.1)

When a `move_instance` relocates an instance that contains a V0 or V1 via, the enclosing M1 polygon must be extended by a matching `resize_end` to satisfy V0.M1.EN.1 (5 nm enclosure on two opposite sides) and V1.M1.EN.1 (5 nm + 2 nm on two opposite sides). The pattern is: move the instance, then extend the high (or low) end of the M1 runner by a delta that covers the displacement plus any remaining enclosure shortfall (trial:i01.ug.Block7_union_row3.15: instance i1623 moved -36, M1 polygon p3379 high end extended +49; trial:i01.ug.leaf_0008.24: instance i1968 moved +108, M1 polygon p3771 high end extended +164; trial:i01.ug.leaf_0002.23: instance i1646 moved +72, M1 polygon p3695 high end extended +128).

The symmetric y-axis resize in trial:i01.ug.Block7_union_row12.02 (p3694: +8 high, -8 low) represents a V0.M1.AUX.3 repair: V0.M1.AUX.3 requires the V0 via width to equal the M1 width in the perpendicular direction, so the M1 polygon must be widened equally on both sides to coplanar-match the via without translation of the polygon center.

## Gate acceptance criterion

All 26 trials in this iteration were accepted (decision=gated_in). The gate requires conn_preserved=true; it does not require n_new_in_crop=0. Trials accepted with nonzero in-crop new violations: trial:i01.ug.Block7_union_row13.03 (1 new), trial:i01.ug.Block7_union_row19.09 (1 new), trial:i01.ug.Block7_union_row21.11 (9 new), trial:i01.ug.Block7_union_row22.12 (2 new), trial:i01.ug.Block7_union_row24.14 (2 new), trial:i01.ug.Block7_union_row4.16 (1 new), trial:i01.ug.Block7_union_row5.17 (1 new), trial:i01.ug.leaf_0002.23 (2 new), trial:i01.ug.leaf_0008.24 (1 new), trial:i01.ug.leaf_0024.25 (1 new). No trial produced any out-of-crop new violations (n_new_out_of_crop=0 in all records). Do not discard a candidate repair solely on the basis of n_new_in_crop > 0; accept it when conn_preserved=true and n_new_out_of_crop=0 (trial:i01.ug.Block7_union_row21.11).

## Multi-layer scope

Every trial touches M1, M2, and V1 simultaneously; M1 repairs cannot be planned without accounting for M2 and V1 effects in the same locus. A subset of trials also touches M3 and V2: trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row13.03, trial:i01.ug.Block7_union_row14.04, trial:i01.ug.Block7_union_row19.09, trial:i01.ug.Block7_union_row9.21. Trial trial:i01.ug.leaf_0024.25 touches M1, M2, M3, V1 but not V2. When M3 appears in touched_layers, expect that M1 resize_end deltas may be larger than one pitch, as the operation chain must propagate enclosure fixes upward through multiple metal layers.

## Single-operation repairs

Two trials use exactly one operation: trial:i01.ug.Block7_union_row6.18 (move i1473 by +28 x, zero new violations) and trial:i01.ug.Block7_union_row21.11 (move i0100 by +4 x, 9 new in-crop violations accepted). A +4 dbu nudge is sufficient to clear an M1 violation when the initial geometry is only marginally short of the minimum—trial:i01.ug.Block7_union_row21.11 confirms that even a 4 dbu move is accepted when connectivity is preserved, despite the larger collateral violation count.