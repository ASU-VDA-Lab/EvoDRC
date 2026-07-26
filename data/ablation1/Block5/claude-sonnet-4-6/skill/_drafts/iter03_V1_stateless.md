## Repair Operation Patterns

All recorded repairs for layer V1 in this design apply moves exclusively along the x-axis (horizontal). No y-direction delta was observed in any trial across all three iterations (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.Block5_union_row6.01, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05, trial:i02.ug.Block5_union_row6.00, trial:i02.ug.leaf_0002.02, trial:i03.ug.leaf_0002.01). Do not attempt y-axis instance moves for V1 DRC repair in this design context.

All repairs that touched V1 also simultaneously touched M1 and M2 (touched_layers includes all three in every trial). Never repair V1 violations in isolation; always evaluate and adjust enclosing M1 and M2 polygons as part of the same operation set.

## Move Step Sizes

The predominant move delta is 36 dbu in x, observed in trial:i01.ug.Block5_union_row3.00, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05, and trial:i03.ug.leaf_0002.01. A smaller delta of 4 dbu was successfully used in trial:i01.ug.Block5_union_row6.01 for a 2-instance move. Larger deltas of 72 dbu and 104 dbu were also accepted in trial:i02.ug.leaf_0002.02 and trial:i02.ug.Block5_union_row6.00 respectively. Use 36 dbu as the default step; step up to 72 or 104 when a larger spacing gap must be closed (trial:i02.ug.Block5_union_row6.00); step down to 4 dbu only when the violation requires a fine adjustment near the minimum rule threshold (trial:i01.ug.Block5_union_row6.01).

## Opposing-Direction Instance Moves

Spacing violations between two V1 instances on the same or adjacent M2 tracks are resolved by moving both instances away from each other: one in +x, one in -x. In trial:i01.ug.leaf_0002.03, instance i0056 moved +36 dbu and instance i0103 moved -36 dbu; this produced n_new_in_crop=0 and conn_preserved=true. This symmetric divergence doubles the effective gap increase per unit move and avoids displacing the center of the via pair, which reduces the risk of opening new violations elsewhere.

## resize_end Pairing with move_instance

When a move_instance operation shifts a V1 instance (and its enclosing M2 segment) away from adjacent geometry, the M2 polygon's high-x end must be extended to maintain the required M2 enclosure of V1 (V1.M2.EN.2 requires 5 nm enclosure on two opposite sides). In trial:i01.ug.Block5_union_row3.00, instance i0117 moved +36 dbu and M2 polygon p967 received a resize_end of +36 dbu on its high x-end. In trial:i01.ug.leaf_0001.02, instance i0011 moved +36 dbu and p974 received +72 dbu. In trial:i02.ug.Block5_union_row6.00, instances i0025 and i0019 moved +104 dbu and p955 received +20 dbu on the high x-end. Apply a resize_end on the high-x end of the associated M2 polygon whenever an instance is moved in +x; the resize delta need not equal the move delta but must be sufficient to preserve the 5 nm M2 enclosure requirement of V1.M2.EN.2.

## Connectivity Preservation as Gating Criterion

Every trial in this history has conn_preserved=true and decision=gated_in. In trial:i03.ug.leaf_0002.01 (iteration 3), the operation introduced n_new_in_crop=1 (one new violation within the crop region) but the decision remained gated_in because conn_preserved=true. Do not discard a repair candidate solely because it introduces a new in-crop violation; connectivity preservation is the primary acceptance gate. New in-crop violations introduced by a V1 repair become targets for subsequent iterations.

## Iteration Progression and Design State

The design_state hash changed at each iteration boundary: all six iteration-1 trials share design state ef66d47d..., both iteration-2 trials share c5292a28..., and the single iteration-3 trial uses d7ef52f1.... Repairs accumulate across iterations; the violation set entering iteration 3 reflects the residual after iterations 1 and 2 closed their respective violations with n_new_in_crop=0. The one new in-crop violation introduced at trial:i03.ug.leaf_0002.01 (n_new_in_crop=1) represents the remaining open work after three iterations.

## V1.M2.AUX.2 Compliance Under Moves

V1.M2.AUX.2 requires V1 to match M2 width exactly in the direction perpendicular to M2 length. All horizontal (x-axis) moves of V1 instances preserve this constraint automatically because the perpendicular dimension (y-axis) is unchanged. No y-axis resize_end operations appear in any trial, consistent with the rule requiring exact width match rather than enclosure in the perpendicular direction.

## V1.AUX.1 Compliance Under Moves and Resizes

V1.AUX.1 requires V1 to remain inside both M1 and M2 after every operation. All repairs achieved conn_preserved=true with no out-of-crop violations added (n_new_out_of_crop=0 in every trial). The combination of move_instance paired with resize_end on the M2 polygon high-x end (as in trial:i01.ug.Block5_union_row3.00 and trial:i01.ug.leaf_0001.02) maintains V1.AUX.1 by keeping the M2 footprint co-moving with the V1 instance.

## Enclosure Rules Under Resize

V1.M1.EN.1 requires M1 enclosure of V1 of 5 nm and 2 nm on two opposite sides in projection. V1.M2.EN.2 requires M2 enclosure of 5 nm on two opposite sides (either 5&5 or 5&0 in the allowed variants). In trial:i01.ug.Block5_union_row3.00, instance i0131 was also moved +36 dbu alongside i0117, indicating that both the V1 instance and an additional M1/M2-related cell were co-moved to preserve bilateral enclosure. When a V1 instance moves, verify that both the M1 enclosure (V1.M1.EN.1) and M2 enclosure (V1.M2.EN.2) remain satisfied on both opposing sides; if only one enclosing polygon is resized, the trailing side may open a new enclosure violation.