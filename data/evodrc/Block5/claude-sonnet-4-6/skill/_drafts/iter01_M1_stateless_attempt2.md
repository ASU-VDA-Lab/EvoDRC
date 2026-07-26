## Accepted Operation Patterns

Every trial in the measured history was accepted with `decision: "gated_in"`, `conn_preserved: true`, `n_new_in_crop: 0`, and `n_new_out_of_crop: 0`. All six trials share these outcome fields (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.Block5_union_row6.01, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05). No trial in this history was rejected.

## Operation Types Observed on M1

The only operation types recorded in this history are `move_instance` and `resize` with `axis: "x"`. No `move_instance` with a y-component and no `resize` with `axis: "y"` appear in any trial. All six trials touched layers M1, M2, and V1 together (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.Block5_union_row6.01, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05), confirming that M1 repairs in the unit_gate channel co-move or co-resize V1 and M2 rather than touching M1 in isolation.

## Move Magnitudes Accepted

The following horizontal move magnitudes (x-component of `delta_dbu`) were each accepted with zero new violations:

- 4 dbu: trial:i01.ug.leaf_0006.05
- 36 dbu: trial:i01.ug.Block5_union_row3.00 (both instances), trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03 (one instance at +36, one at -36)
- 108 dbu: trial:i01.ug.Block5_union_row6.01 (both move_instance ops)
- 112 dbu: trial:i01.ug.leaf_0005.04

The 4 dbu move (trial:i01.ug.leaf_0006.05) is the smallest recorded and was accepted, establishing that sub-grid-step micro-adjustments are viable when connectivity is preserved and no new crop violations result.

## Multi-Instance Moves Within a Single Locus

Trials with two or more `move_instance` ops in one repair were accepted when all moved instances shifted in the same direction or in coordinated opposing directions. trial:i01.ug.Block5_union_row3.00 moved two instances by +36 dbu each in the same direction. trial:i01.ug.leaf_0002.03 moved one instance by +36 dbu and a second by -36 dbu within the same locus; this opposing-direction pair was accepted with conn_preserved=true and zero new violations, confirming that counter-directional instance moves are valid when the net connectivity outcome satisfies the acceptance criterion.

## Combined Move-and-Resize Operations

trial:i01.ug.Block5_union_row6.01 is the only trial containing `resize` ops. It used four ops total: two `move_instance` at +108 dbu each and two `resize` on polygons p955 and p971 with `axis: "x"` and `delta_dbu` values of 256 and 328 respectively. This combination was accepted with conn_preserved=true and zero new violations. No other trial uses resize, so the resize+move pairing is documented only for this locus.

## Connectivity Preservation as Gating Criterion

Every accepted trial records `reason: "conn_preserved"` under `deltas` (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.Block5_union_row6.01, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05). Connectivity preservation is thus the recorded gating condition for acceptance in the unit_gate channel. Any M1 repair operation whose `conn_preserved` field is false does not appear as accepted in this history.

## New-Violation Budget in Accepted Trials

Every accepted trial shows `n_new_in_crop: 0` and `n_new_out_of_crop: 0` (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.Block5_union_row6.01, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05). No trial in this history introduced a net-new violation inside or outside the crop boundary and was still accepted. Apply operations that achieve zero new in-crop and zero new out-of-crop violations, as all accepted trials in this history satisfy this condition.

## Channel and Design State

All trials in this history executed in the `unit_gate` channel against design state `ef66d47d838616255ced092ce8405c19a7101183e938e23fc839e77c033c8cfa` (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.Block5_union_row6.01, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05). No trials from other channels or design states appear in this history, so cross-channel or cross-state generalizations are not grounded here.

## Units Involved

Five distinct unit_ids appear across the six trials: Block5_union_row3 (trial:i01.ug.Block5_union_row3.00), Block5_union_row6 (trial:i01.ug.Block5_union_row6.01), leaf_0001 (trial:i01.ug.leaf_0001.02), leaf_0002 (trial:i01.ug.leaf_0002.03), leaf_0005 (trial:i01.ug.leaf_0005.04), leaf_0006 (trial:i01.ug.leaf_0006.05). The move-only pattern (no resize) covers four units; the combined move+resize pattern covers Block5_union_row6 only (trial:i01.ug.Block5_union_row6.01).