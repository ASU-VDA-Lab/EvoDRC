## Measured Trial Summary

One repair trial has been recorded for M6 at iteration 1. The trial targeted cell `VIA_VIA56_2_2_66_58` in Block1 and applied a single operation: an x-axis resize of −96 dbu to an M5 via shape (`resize_via_shape`, shape index 0). The touched layers were M5, M6, and V5. The operation produced a delta_total of 0 across the whole-design window (before: 244, after: 244) and was rejected under decision `rejected_net_positive` (trial:i01.cu.def:VIA_VIA56_2_2_66_58.01).

## Repair Guidance Grounded in Measured Data

Do not apply an x-direction shrink of −96 dbu to M5 via shapes inside `VIA_VIA56_2_2_66_58` as a strategy to reduce M6/V5 DRC violations; trial:i01.cu.def:VIA_VIA56_2_2_66_58.01 showed this operation leaves the total violation count unchanged.

The trial touched M6 and V5 simultaneously (trial:i01.cu.def:VIA_VIA56_2_2_66_58.01), confirming that resize operations on M5 within a V5/M6 via cell propagate geometry changes into the M6 layer. Because the delta remained zero after this propagation, avoid treating M5 x-shrinks as a proxy fix for M6-side enclosure or width constraints in this cell (trial:i01.cu.def:VIA_VIA56_2_2_66_58.01).

## Coverage Note

Only one trial exists in this layer's history. No successful repairs, no M6-direct geometry edits, and no y-axis operations have been measured. All rule-specific guidance beyond the above must await additional trial data before prescriptive claims can be grounded.