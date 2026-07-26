## Repair Operation Patterns

All accepted trials across iterations 1 and 2 used strictly orthogonal, X-axis-only operations on M2-touching units and were accepted with zero new DRC violations (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.Block5_union_row6.01, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05, trial:i02.ug.Block5_union_row6.00, trial:i02.ug.leaf_0001.01, trial:i02.ug.leaf_0002.02). No Y-axis displacements or diagonal moves appeared in any accepted trial, consistent with the GEOMETRY.NONORTHOGONAL constraint that forbids non-axis-aligned edges on M2.

Y-axis resize operations on via-cell shapes were tried in two cu_pool trials and both were rejected with net-positive or zero-improvement outcomes (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00, trial:i02.cu.def:VIA_VIA23_1_3_36_36.01). Do not apply Y-axis resize operations when attempting to reduce M2 violation counts; the measured record shows these fail to produce net improvement.

## move_instance

`move_instance` is the dominant repair operation. Confirmed accepted X-axis move deltas across both iterations: +4 dbu (trial:i01.ug.Block5_union_row6.01), +8 dbu (trial:i02.ug.leaf_0001.01), +36 dbu (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05), +72 dbu (trial:i02.ug.leaf_0002.02), and +104 dbu (trial:i02.ug.Block5_union_row6.00). Apply `move_instance` in the +X direction first when resolving M2 spacing or enclosure violations; all measured step sizes from +4 through +104 dbu have been accepted in appropriate loci without introducing new violations.

Moving two instances by the same delta in the same direction in a single trial is confirmed valid: trial:i02.ug.Block5_union_row6.00 applied +104 dbu to both i0025 and i0019 simultaneously and was accepted. When two adjacent instances both participate in a spacing conflict and must move in opposite directions, apply bidirectional instance spreading: trial:i01.ug.leaf_0002.03 applied +36 dbu to i0056 and -36 dbu to i0103 in a single accepted trial.

The +36 dbu step size is larger than the strictest tip-to-tip spacing requirement (31 nm for M2.S.4 and M2.S.5), making it a reliable step size for resolving both side-to-side and tip-to-tip violations in one operation without undershooting. Smaller deltas (+4, +8 dbu) were sufficient at their specific loci but the history does not establish them as generally safe for tip-to-tip violations.

## resize_end

`resize_end` on the `x` axis, `high` end, has been accepted in three trials alongside `move_instance`. trial:i01.ug.Block5_union_row3.00 extended polygon p967 by 36 dbu at its high-X end while moving two instances by +36 dbu. trial:i01.ug.leaf_0001.02 extended polygon p974 by 72 dbu at its high-X end while moving one instance by +36 dbu. trial:i02.ug.Block5_union_row6.00 extended polygon p955 by 20 dbu at its high-X end while moving two instances by +104 dbu each. All three were accepted with no new violations.

The resize delta does not need to match the instance move delta: trial:i02.ug.Block5_union_row6.00 accepted a 20 dbu resize paired with a 104 dbu instance move. Apply `resize_end` on the high-X end when a polygon must be lengthened to restore V1 or V2 enclosure after an instance is displaced; the appropriate resize magnitude is determined by the enclosure gap introduced, not by the instance move distance.

## Operation Counts per Trial

Accepted trials ranged from 1 to 3 operations. Single-operation trials: trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05, trial:i02.ug.leaf_0002.02. Two-operation trials: trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i02.ug.leaf_0001.01. Three-operation trials: trial:i01.ug.Block5_union_row3.00, trial:i02.ug.Block5_union_row6.00. Compound multi-op repairs that mix `move_instance` and `resize_end` are confirmed acceptable. Do not limit repairs to single-operation trials.

## Touched Layer Combinations

Two layer combinations have been confirmed across accepted trials. The M1+M2+V1 combination was touched in trial:i01.ug.Block5_union_row3.00, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05, trial:i02.ug.leaf_0002.02, and trial:i02.ug.Block5_union_row6.00. The M2+M3+V2 combination was touched in trial:i01.ug.Block5_union_row6.01 and trial:i02.ug.leaf_0001.01. Both combinations are confirmed safe for `move_instance`-based repairs. The rejected cu_pool trials touched M2+M3+V2 and M2+M3+M4+V2+V3 respectively, but those rejections are attributable to Y-axis operation type, not to the layer combination itself.

## Connectivity Preservation

Every accepted trial reported `conn_preserved: true` and `n_new_in_crop: 0, n_new_out_of_crop: 0`. Keeping `move_instance` deltas consistent across all instances sharing a net (moving all connected instances by the same vector, or pairing opposing moves as in trial:i01.ug.leaf_0002.03) preserves connectivity. Resize operations that extend a polygon toward the displaced instance (rather than away) also preserve net connectivity, as confirmed by trial:i01.ug.Block5_union_row3.00, trial:i01.ug.leaf_0001.02, and trial:i02.ug.Block5_union_row6.00.

## Enclosure Rules (V1.M2.EN.2, V1.M2.AUX.2, V2.M2.EN.1)

The enclosure rules V1.M2.EN.2 (5 nm minimum enclosure of V1 by M2 on two opposite sides) and V1.M2.AUX.2 (V1 width must match M2 width perpendicular to M2 length) impose a tight coupling between M2 polygon extent and V1 placement. The `resize_end` operations in trial:i01.ug.Block5_union_row3.00 (+36 dbu), trial:i01.ug.leaf_0001.02 (+72 dbu), and trial:i02.ug.Block5_union_row6.00 (+20 dbu) all extended M2 in the same direction as the accompanying instance moves, confirming that extending M2 toward the displaced V1 is the correct direction to satisfy V1.M2.EN.2 without creating new violations. Do not move an instance away from an M2 polygon endpoint without either also moving the polygon or extending it; the accepted trials show that paired `move_instance` + `resize_end` sequences resolve this coupling cleanly.

## Spacing Rule Context

M2 side-to-side spacing (M2.S.1) requires 18 nm minimum between edges longer than 36 nm. Tip-to-side (M2.S.2) requires 25 nm. Tip-to-tip rules vary by tip width: both edges >= 24 nm and <= 36 nm require 27 nm (M2.S.3); mixed wide/narrow tips require 31 nm (M2.S.5); both tips < 24 nm require 31 nm (M2.S.4). Corner-to-corner Euclidian spacing must be >= 20 nm (M2.S.6). The compound rule M2.S.7 forbids any 18 nm tip-to-tip gap co-located with a side spacing <= 32 nm unless parallel run length is >= 35 nm. The observed +36 dbu move magnitude is larger than the strictest tip-to-tip spacing requirement (31 nm), making it a reliable step size for resolving both side-to-side and tip-to-tip violations in one operation without undershooting.