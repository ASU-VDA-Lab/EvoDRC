**Repair operation types used for M3 violations**

All six accepted trials used combinations of `move_instance` and `resize_end` operations to resolve M3 DRC violations (trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row13.03, trial:i01.ug.Block7_union_row14.04, trial:i01.ug.Block7_union_row19.09, trial:i01.ug.Block7_union_row9.21, trial:i01.ug.leaf_0024.25). trial:i01.ug.Block7_union_row9.21 additionally applied a direct polygon `move` op on p2720. No repair in this iteration used a single operation type alone.

**Acceptance gating**

All six trials were gated_in with `conn_preserved: true`. Trials with `n_new_in_crop: 1` were still accepted when connectivity was preserved (trial:i01.ug.Block7_union_row13.03, trial:i01.ug.Block7_union_row19.09, trial:i01.ug.leaf_0024.25). No trial introduced out-of-crop violations (`n_new_out_of_crop: 0` across all six trials). Do not reject a repair candidate solely because it introduces one new in-crop violation, provided connectivity is preserved.

**Instance move magnitudes observed**

X-axis moves ranged from 28 dbu (trial:i01.ug.Block7_union_row14.04) to 108 dbu (trial:i01.ug.Block7_union_row9.21). Y-axis moves ranged from -52 dbu (trial:i01.ug.Block7_union_row19.09) to +64 dbu (trial:i01.ug.Block7_union_row14.04). Moves of 36–40 dbu in X recurred across multiple trials (trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row13.03, trial:i01.ug.Block7_union_row9.21). Within a single repair, different instances may receive different delta magnitudes: trial:i01.ug.Block7_union_row9.21 moved instances by 36, 56, and 108 dbu in X within the same op sequence.

**resize_end magnitudes observed**

Polygon end resize deltas ranged from 4 dbu in X (trial:i01.ug.Block7_union_row13.03, p3526 high-end) to 64 dbu in Y (trial:i01.ug.Block7_union_row14.04, p3576 high-end). Apply resize_end to individual polygon edges rather than uniform scaling: trial:i01.ug.Block7_union_row9.21 resized only the low-end of p3300 by -36 dbu X while moving other instances by larger amounts. Both axes may be resized on the same polygon in one repair: trial:i01.ug.leaf_0024.25 applied resize_end +36 dbu X high-end and +44 dbu Y high-end to p3538.

**Multi-layer co-repair**

Every accepted repair touched M3 alongside M1, M2, and V1 at minimum. Five of six trials also touched V2 (trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row13.03, trial:i01.ug.Block7_union_row14.04, trial:i01.ug.Block7_union_row19.09, trial:i01.ug.Block7_union_row9.21). Resolving M3 violations requires coordinating moves across connected lower layers simultaneously; a repair that adjusts M3 geometry without also moving the attached V2/V1/M2/M1 instances does not appear in any accepted trial.

**Op count**

Accepted repairs used 5 to 9 total operations. The minimum observed was 5 ops (trial:i01.ug.Block7_union_row13.03, trial:i01.ug.Block7_union_row19.09); the maximum was 9 ops (trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row9.21). Larger locus areas did not strictly require more ops: trial:i01.ug.Block7_union_row9.21 with locus width ~15 kdbu used 9 ops, while trial:i01.ug.Block7_union_row19.09 with locus width ~20 kdbu used only 5 ops.