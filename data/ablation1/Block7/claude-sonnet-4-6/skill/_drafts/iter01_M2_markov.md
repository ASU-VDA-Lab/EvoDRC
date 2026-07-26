**Repair character of iteration 1 (all trials gated_in, conn_preserved)**

All 26 trials accepted in iteration 1 carry `decision: "gated_in"` and `conn_preserved: true` with `n_new_out_of_crop: 0`. Connectivity preservation is the binding acceptance criterion: trials trial:i01.ug.Block7_union_row13.03, trial:i01.ug.Block7_union_row19.09, trial:i01.ug.Block7_union_row21.11, trial:i01.ug.Block7_union_row22.12, trial:i01.ug.Block7_union_row24.14, trial:i01.ug.Block7_union_row4.16, trial:i01.ug.Block7_union_row5.17, trial:i01.ug.leaf_0002.23, and trial:i01.ug.leaf_0008.24 were each accepted despite introducing 1–9 new in-crop violations, because connectivity was preserved and no new out-of-crop violations appeared.

**Primary repair operator: move_instance on the x axis**

`move_instance` in the x direction is the dominant single-layer M2 repair operator across all 26 trials. The most frequent x displacement is ±36 dbu, appearing in trials trial:i01.ug.Block7_union_row10.00, trial:i01.ug.Block7_union_row11.01, trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row14.04, trial:i01.ug.Block7_union_row15.05, trial:i01.ug.Block7_union_row16.06, trial:i01.ug.Block7_union_row18.08, trial:i01.ug.Block7_union_row20.10, trial:i01.ug.Block7_union_row22.12, trial:i01.ug.Block7_union_row23.13, trial:i01.ug.Block7_union_row24.14, trial:i01.ug.Block7_union_row4.16, trial:i01.ug.Block7_union_row5.17, trial:i01.ug.Block7_union_row8.20, trial:i01.ug.Block7_union_row9.21. Other observed x displacements are 28 dbu (trial:i01.ug.Block7_union_row6.18, trial:i01.ug.Block7_union_row4.16), 40 dbu (trial:i01.ug.Block7_union_row13.03, trial:i01.ug.Block7_union_row7.19, trial:i01.ug.leaf_0008.24), 44 dbu (trial:i01.ug.Block7_union_row23.13), 56 dbu (trial:i01.ug.Block7_union_row9.21), 64 dbu (trial:i01.ug.Block7_union_row8.20), 72 dbu (trial:i01.ug.leaf_0002.23, trial:i01.ug.leaf_0095.26), 108 dbu (trial:i01.ug.Block7_union_row7.19, trial:i01.ug.Block7_union_row9.21, trial:i01.ug.leaf_0008.24), and minor nudges of 4 dbu (trial:i01.ug.Block7_union_row10.00 one of four ops, trial:i01.ug.Block7_union_row21.11 sole op, trial:i01.ug.leaf_0001.22 sole op).

**Bilateral (opposing-direction) moves resolve spacing by splitting displacement**

Several trials move different instances in opposite x directions within a single repair step, distributing the required clearance across two polygons rather than loading all displacement onto one side. trial:i01.ug.Block7_union_row16.06 moves i0407 and i0928 by −36 dbu and i0320 by +40 dbu. trial:i01.ug.Block7_union_row19.09 moves i0771 by +37 dbu and i0026 and i0294 by −37 dbu. trial:i01.ug.Block7_union_row20.10 moves i0753 by −44 dbu and i0600, i0142 by +36 dbu and i0263 by +40 dbu. This bilateral pattern appears whenever local congestion makes a unidirectional move of the full required distance infeasible within the repair locus.

**resize_end augments move_instance when polygon extent must change independently of instance placement**

`resize_end` operations on the x-high end are used alongside `move_instance` when an M2 polygon tip must be extended or retracted to satisfy tip-spacing rules (M2.S.2, M2.S.3, M2.S.4, M2.S.5) independently of the instance anchor. Observed resize_end x-high deltas: 49 dbu (trial:i01.ug.Block7_union_row3.15), 56 dbu (trial:i01.ug.Block7_union_row12.02), 4 dbu (trial:i01.ug.Block7_union_row13.03), 36 dbu (trial:i01.ug.Block7_union_row24.14, trial:i01.ug.leaf_0024.25), 48 dbu (trial:i01.ug.Block7_union_row14.04), 128 dbu (trial:i01.ug.leaf_0002.23), 164 dbu (trial:i01.ug.leaf_0008.24), 16 dbu (trial:i01.ug.Block7_union_row7.19), 52 dbu (trial:i01.ug.leaf_0024.25 x-low end). One x-low shrink of −36 dbu appears in trial:i01.ug.Block7_union_row9.21. One full polygon move (`op: "move"`) of 56 dbu in x appears on p2720 in trial:i01.ug.Block7_union_row9.21.

**Y-axis moves and y-axis resize_end are secondary but occur in multi-layer repairs**

Y-axis `move_instance` displacements appear in trials that also touch M3 and V2: +64 dbu and −12 dbu in trial:i01.ug.Block7_union_row14.04, −52 dbu in trial:i01.ug.Block7_union_row19.09, +44 dbu in trial:i01.ug.Block7_union_row23.13 and trial:i01.ug.leaf_0024.25, +8 dbu in trial:i01.ug.Block7_union_row12.02, and a combined +72/+44 dbu diagonal move in trial:i01.ug.leaf_0024.25. Y-axis `resize_end` (high: +8, −8, +44, +20; values in dbu) appear in trial:i01.ug.Block7_union_row12.02 and trial:i01.ug.leaf_0024.25. Y moves are never the sole repair action on M2.

**Multi-layer vertical coupling: M2 repairs routinely propagate into M1, V1, and sometimes M3, V2**

Every trial in iteration 1 lists M1 and V1 in `touched_layers` alongside M2. Trials that also touch M3 and V2 are trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row13.03, trial:i01.ug.Block7_union_row14.04, trial:i01.ug.Block7_union_row19.09, trial:i01.ug.Block7_union_row9.21, and trial:i01.ug.leaf_0024.25. M2 repairs should account for downstream via enclosure rules V1.M2.EN.2 and V1.M2.AUX.2 and for V2.M2.EN.1 when M3/V2 are also touched.

**Small nudge moves (4 dbu) can generate large violation counts in dense regions**

A single `move_instance` of 4 dbu on i0100 (trial:i01.ug.Block7_union_row21.11) introduced 9 new in-crop violations while resolving the target violation and preserving connectivity. A 4 dbu move on i1486 (trial:i01.ug.leaf_0001.22) introduced zero new violations. This contrast establishes that 4 dbu is a valid step size but its impact is strongly locus-dependent; use it only when the local M2 track density permits.

**Large moves (108 dbu and above) are necessary when standard 36 dbu steps produce insufficient clearance**

Moves of 108 dbu on single instances appear in trial:i01.ug.Block7_union_row7.19 (i1446) and trial:i01.ug.Block7_union_row9.21 (i1117) and trial:i01.ug.leaf_0008.24 (i1968), each accepted without new out-of-crop violations. The 164 dbu resize_end in trial:i01.ug.leaf_0008.24 is the largest single geometric delta observed in iteration 1. These large displacements do not inherently disqualify a repair so long as connectivity is maintained.

**Op count range and its interpretation**

Single-op repairs appear in trial:i01.ug.Block7_union_row6.18 (28 dbu x-move) and trial:i01.ug.Block7_union_row21.11 (4 dbu x-move) and trial:i01.ug.leaf_0001.22 (4 dbu x-move), establishing that one-op solutions exist for isolated violations. The maximum observed is 9 ops in trial:i01.ug.Block7_union_row12.02 and trial:i01.ug.Block7_union_row9.21, both touching M1, M2, M3, V1, V2. Op count correlates with the number of stacked layers touched, not with the magnitude of individual displacements.