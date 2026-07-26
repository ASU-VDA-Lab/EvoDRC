## Repair Operations Observed

All six gated-in repairs in this iteration used exclusively X-axis move_instance and X-axis resize_end operations; no Y-axis moves or resizes appear in the record. Every repair touched layers M1, M2, and V1 simultaneously (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.Block5_union_row6.01, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05).

## Move Delta Magnitudes

The dominant move step is +36 dbu in x, used in five of the six trials (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05). A smaller step of +4 dbu in x was applied in trial:i01.ug.Block5_union_row6.01, where both instances i0025 and i0019 were shifted by the same small amount. In trial:i01.ug.leaf_0002.03, two instances were moved in opposite directions: i0056 by +36 dbu and i0103 by -36 dbu, distributing the required separation gap symmetrically between them.

## Resize Operations

When a resize_end operation accompanied a move, the resize was always applied to the high end of the x-axis. In trial:i01.ug.Block5_union_row3.00, polygon p967 was extended by 36 dbu at its high-x end after moving instance i0117 by +36 dbu. In trial:i01.ug.leaf_0001.02, polygon p974 was extended by 72 dbu at its high-x end after moving instance i0011 by +36 dbu. No low-end or y-axis resize operations appear in the record.

## Connectivity and Violation Outcomes

All six repairs preserved connectivity (conn_preserved: true) and introduced zero new violations inside or outside the crop window (n_new_in_crop: 0, n_new_out_of_crop: 0 in every trial). The decision was gated_in in all cases (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.Block5_union_row6.01, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05), confirming that X-axis displacement and high-end extension of M2 polygons resolves V1 violations without creating new DRC errors when the move magnitude satisfies the applicable spacing and enclosure rules.

## Operation Count and Co-moves

Single-instance moves sufficed in two trials (trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05). Two-operation repairs were used in three trials: same-direction co-moves of two instances in trial:i01.ug.Block5_union_row6.01; a move paired with a polygon resize in trial:i01.ug.leaf_0001.02; and opposite-direction co-moves of two instances in trial:i01.ug.leaf_0002.03. The three-operation repair in trial:i01.ug.Block5_union_row3.00 combined two instance moves with one polygon resize on a third shape.

## Effective Repair Pattern

Apply X-axis move_instance steps — 36 dbu is the predominant effective magnitude (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05); 4 dbu was sufficient where the violation gap was smaller (trial:i01.ug.Block5_union_row6.01) — and pair the move with a high-end X-axis resize_end on the associated M2 polygon when the polygon boundary must follow the instance (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.leaf_0001.02). Use opposite-direction co-moves to split the required spacing gap between two instances rather than displacing one by the full amount (trial:i01.ug.leaf_0002.03). All successful repairs in this iteration operated exclusively in the horizontal (x) direction and adjusted M1, M2, and V1 as a unit.