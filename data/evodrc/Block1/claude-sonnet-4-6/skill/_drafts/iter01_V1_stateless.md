## Effective Repair Operations

All eleven accepted trials (trial:i01.ug.Block1_union_row1.00 through trial:i01.ug.leaf_0031.11) repaired V1-touching loci exclusively with `move_instance` operations, paired in the majority of multi-instance cases with `resize_end` adjustments to M2 polygon endpoints. No trial in this history used a `resize_via_shape` on a V1 cell and remained accepted.

Move deltas are always along the x-axis only (y-component zero in every accepted op), consistent with V1 instances residing on horizontal M2 tracks. Do not apply y-axis moves to V1 instances; the full accepted set confirms x-only displacement is the correct displacement axis (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row10.01, trial:i01.ug.Block1_union_row3.03, trial:i01.ug.Block1_union_row4.04, trial:i01.ug.Block1_union_row5.05, trial:i01.ug.Block1_union_row6.06, trial:i01.ug.Block1_union_row8.07, trial:i01.ug.Block1_union_row9.08, trial:i01.ug.leaf_0004.09, trial:i01.ug.leaf_0020.10, trial:i01.ug.leaf_0031.11).

Move magnitudes across accepted trials span from 8 dbu to 192 dbu (resize_end extent), with the most frequent granularity being multiples of 4 dbu. Single-instance loci use the smallest deltas (36 dbu in trial:i01.ug.leaf_0004.09, 36 dbu in trial:i01.ug.leaf_0031.11, -56 dbu in trial:i01.ug.leaf_0020.10). Multi-instance loci accept mixed positive and negative moves within the same repair set, including negative x-moves such as -36 dbu (trial:i01.ug.Block1_union_row5.05) and -64 dbu (trial:i01.ug.Block1_union_row8.07) and -72 dbu (trial:i01.ug.Block1_union_row6.06).

## M2 Endpoint Resize Must Accompany Via Moves

When a V1 instance is moved along x, the M2 polygon that encloses it requires a corresponding `resize_end` on its `high` or `low` x-edge to preserve the enclosure required by V1.M2.EN.2 and the width-matching required by V1.M2.AUX.2. In every accepted trial that moved more than one instance or moved an instance by a substantial delta, at least one `resize_end` on an M2 polygon co-occurred (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row5.05, trial:i01.ug.Block1_union_row6.06, trial:i01.ug.Block1_union_row8.07). Trials with small single-instance moves and no resize_end (trial:i01.ug.leaf_0004.09, trial:i01.ug.leaf_0020.10, trial:i01.ug.leaf_0031.11) produced zero new violations in crop, indicating the via motion was small enough that existing M2 geometry still satisfied enclosure. Do not omit M2 resize_end operations when the via displacement exceeds the M2 end-cap slack available under V1.M2.EN.2.

## Gating Criterion: Connectivity, Not Zero New Violations

The accept/reject decision is based on `conn_preserved`, not on `n_new_in_crop`. Three accepted trials introduced new violations within the crop: trial:i01.ug.Block1_union_row1.00 (4 new), trial:i01.ug.Block1_union_row6.06 (1 new), and trial:i01.ug.leaf_0031.11 (4 new). All were accepted because connectivity was preserved. Do not treat non-zero `n_new_in_crop` alone as a rejection criterion; preserve net connectivity above all else.

## Multi-Layer Scope Tied to Connectivity Failure

The sole rejected trial (trial:i01.ug.leaf_0034.12, gated_out, conn_broken) is the only trial in this history that simultaneously touched M3, M4, V2, and V1, performed a `resize_via_shape` on an M3-tier via cell, and used large polygon resize_end deltas (192 dbu, 100 dbu). It produced 89 new violations in crop and broke connectivity. All accepted trials confined their V1-layer repairs to M1, M2, and V1 only, with no tier-crossing via reshaping. Restrict V1 repair operations to M1/V1/M2 and avoid co-modifying higher-tier objects (M3+, V2+) in the same repair set.

## Spacing and Enclosure Context

V1.S.1 distinguishes same-track spacing (18 nm), non-aligned parallel-track spacing (27 nm), and aligned parallel-track spacing (18 nm). The mask construction in V1.S.1 extends around end-cap geometry, meaning via displacement must be evaluated in mask space, not bare via space. The accepted move deltas (e.g., 36 dbu, 72 dbu, 108 dbu at 1 dbu = 1 nm scale) are consistent with opening spacing violations of 18-27 nm by shifting vias by increments that equal or exceed the violation margin, as observed across trial:i01.ug.Block1_union_row1.00 through trial:i01.ug.leaf_0031.11.

V1.M2.AUX.2 requires the via to match M2 width perpendicular to the M2 run direction. Because all moves in accepted trials are along x (the M2 run direction), the perpendicular (y) dimension of the via is never altered, keeping V1.M2.AUX.2 compliance intact without additional action (trial:i01.ug.Block1_union_row1.00 through trial:i01.ug.leaf_0031.11).

V1.M1.EN.1 requires M1 to enclose V1 by 5 nm and 2 nm on opposite sides. Instance moves that shift V1 also shift M1 (since V1 and M1 belong to the same cell instances in all observed cases), so M1 enclosure is automatically maintained by instance-level moves without separate M1 polygon edits. This pattern is consistent across all accepted multi-instance trials (trial:i01.ug.Block1_union_row5.05, trial:i01.ug.Block1_union_row6.06, trial:i01.ug.Block1_union_row8.07).