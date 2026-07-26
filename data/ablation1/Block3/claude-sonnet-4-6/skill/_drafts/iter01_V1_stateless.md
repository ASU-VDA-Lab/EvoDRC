## Repair Operation Patterns

All 10 trials in iteration 1 for layer V1 were accepted (`decision: gated_in`, `conn_preserved: true`) with zero new in-crop violations and zero new out-of-crop violations (`n_new_in_crop: 0`, `n_new_out_of_crop: 0`) across trial:i01.ug.Block3_union_row1.00 through trial:i01.ug.leaf_0013.09. Every repair used the `unit_gate` channel. No rejected trials exist in the measured record for this iteration.

## Move Direction and Granularity

All `move_instance` operations applied displacement exclusively along the x-axis; the y-component of every delta is 0 across all trials. Accepted x-deltas are +36 dbu (trial:i01.ug.Block3_union_row2.01, trial:i01.ug.Block3_union_row5.02, trial:i01.ug.leaf_0006.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0008.06, trial:i01.ug.leaf_0009.07, trial:i01.ug.leaf_0012.08), +108 dbu (trial:i01.ug.Block3_union_row1.00 for instances i0246 and i0205), and -36 dbu (trial:i01.ug.leaf_0013.09). No sub-36 dbu displacements and no y-axis moves appear anywhere in the accepted record; do not attempt them.

Mixed deltas within a single trial are accepted: trial:i01.ug.Block3_union_row1.00 moves i0233 by +36 dbu while moving i0246 and i0205 by +108 dbu each, all with zero new violations.

## Multi-Instance Moves

Simultaneous moves of 2 to 4 instances within one locus are the dominant repair pattern and all preserved connectivity:

- 2 instances: trial:i01.ug.Block3_union_row2.01, trial:i01.ug.leaf_0006.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0012.08, trial:i01.ug.leaf_0013.09
- 3 instances: trial:i01.ug.Block3_union_row1.00, trial:i01.ug.Block3_union_row5.02, trial:i01.ug.leaf_0008.06
- 4 instances: trial:i01.ug.Block3_union_row8.03

Coordinating moves of multiple instances within the same locus is safe; the engine accepted every such trial without introducing new violations.

## resize_end Combined with move_instance

trial:i01.ug.leaf_0008.06 is the only trial that includes a `resize_end` operation. It extends polygon p1261 along the x-axis high end by +36 dbu alongside two `move_instance` ops (+36 dbu each for i0239 and i0047). This three-operation mix was accepted with zero new violations. No trial applies `resize_end` in isolation; in the measured record it is always paired with at least one `move_instance` within the same trial.

## V1 Layer Co-Movement with M1 and M2

Every trial lists `touched_layers: ["M1", "M2", "V1"]`. No trial touches V1 alone. Moving the full via stack (V1 together with its enclosing M1 and M2 geometry) is the exclusive repair strategy in the measured record. This is consistent with V1.AUX.1, which requires V1 to reside inside both M1 and M2, and V1.M2.AUX.2, which requires V1 width to match M2 width perpendicular to M2 length: displacing V1 independently of its metal would violate those rules. Always move V1 together with the instance that owns its M1 and M2 segments, as done in trial:i01.ug.Block3_union_row1.00 through trial:i01.ug.leaf_0013.09.

## Locus Size

Accepted repair loci range from narrow sub-cell crops (~650 × 164 dbu, trial:i01.ug.leaf_0009.07 at locus [6480,6208,7164,6372]) to wide row-spanning extents (~3656 × 864 dbu, trial:i01.ug.Block3_union_row1.00 at locus [6856,2268,10512,3132]). Locus area does not limit acceptance in the measured record; the engine accepted all sizes.

## Connectivity Constraint

`conn_preserved: true` holds for every accepted trial without exception. The `unit_gate` channel enforces connectivity before committing. Plan multi-instance moves so that all nets remain intact; this outcome was achieved in every trial from trial:i01.ug.Block3_union_row1.00 through trial:i01.ug.leaf_0013.09.