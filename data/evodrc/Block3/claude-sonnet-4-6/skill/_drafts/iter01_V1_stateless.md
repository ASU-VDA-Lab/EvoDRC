## Observed Repair Patterns

All ten trials recorded in this iteration share `decision: "gated_in"` with `n_new_in_crop: 0` and `n_new_out_of_crop: 0`, meaning every repair accepted into the design introduced zero net new DRC violations in the crop window and preserved full connectivity. This clean acceptance rate across all trials in trial:i01.ug.Block3_union_row1.00 through trial:i01.ug.leaf_0013.09 establishes that the repair strategies applied here are safe for V1 under the measured conditions.

## Dominant Repair Operation: Coupled Instance Move + M2 High-End Extension

The most frequently applied repair pattern pairs a `move_instance` displacement in the positive-x direction with a `resize_end` on axis x (end: high) applied to the M2 polygon that hosts the affected V1. This paired pattern appears in trial:i01.ug.Block3_union_row1.00 (three such pairs: instance moved +136 dbu with M2 end extended +192 dbu each), trial:i01.ug.Block3_union_row5.02 (instance moved +36 dbu, M2 end extended +36 dbu), trial:i01.ug.Block3_union_row8.03 (four pairs with instance moves of +108/+72/+72/+72 dbu and M2 end extensions of +164/+128/+128/+92 dbu), trial:i01.ug.leaf_0007.05 (two pairs: +36 move / +56 extension each), trial:i01.ug.leaf_0008.06 (+136 move / +92 extension, also including a y-axis extension of +20 dbu), and trial:i01.ug.leaf_0012.08 (+72 move / +108 extension).

The M2 high-end extension delta must never be assumed to equal the instance move delta. Across these trials the extension consistently equals or exceeds the move: in trial:i01.ug.Block3_union_row1.00 the extension exceeded the move by 56 dbu; in trial:i01.ug.Block3_union_row8.03 the largest pair had a 56 dbu surplus; in trial:i01.ug.leaf_0007.05 the surplus was 20 dbu; in trial:i01.ug.leaf_0012.08 the surplus was 36 dbu. Do not truncate the M2 end extension to match the via displacement; always extend by enough to satisfy V1.M2.EN.2 enclosure at the new via location.

## Move-Only Repairs (No M2 Extension Required)

Four trials used `move_instance` exclusively without any accompanying `resize_end`: trial:i01.ug.Block3_union_row2.01 (two instances moved +36 dbu each), trial:i01.ug.leaf_0006.04 (two instances moved +36 dbu each), trial:i01.ug.leaf_0009.07 (one instance moved +36 dbu), and trial:i01.ug.leaf_0013.09 (one instance moved -36 dbu). All four were accepted cleanly. This confirms that when the hosting M2 already provides adequate enclosure after the via displacement—or when the displacement is small enough that the existing M2 overhang absorbs it—no M2 resize is needed. The -36 dbu move in trial:i01.ug.leaf_0013.09 demonstrates that negative-x displacement is also valid and accepted without new violations, so the repair direction is not constrained to positive-x only.

## Y-Axis M2 Adjustment

Trial:i01.ug.leaf_0008.06 included a `resize_end` on axis y (end: high, delta +20 dbu) in addition to the x-direction move and extension. This trial also touched layer M3 (the only trial in this iteration to do so). The repair was accepted with no new violations. This establishes that M2 end adjustments in the y-direction are sometimes required alongside x-direction moves; both axes must be checked when the displaced via approaches an M2 boundary in y. V1.M2.EN.2 applies in both projection axes and either or both may need extension depending on which M2 edge is deficient after the move.

## Connectivity Preservation Across All Multi-Layer Repairs

Every trial touched at minimum M1, M2, and V1 simultaneously (trial:i01.ug.leaf_0008.06 additionally touched M3). `conn_preserved: true` was recorded for all ten trials. Repairs that co-move a V1-containing instance must also adjust the hosting M2 polygon end and, where relevant, any connected M1 geometry to maintain V1.AUX.1 (V1 must remain inside both M1 and M2) and V1.M2.AUX.2 (V1 width must match M2 width perpendicular to M2 length). The clean connectivity record across all trials in trial:i01.ug.Block3_union_row1.00 through trial:i01.ug.leaf_0013.09 confirms that coupling instance moves with layer adjustments on M1 and M2 does not break net connectivity when executed as shown.

## Locus Size and Operation Count

The number of operations per trial ranged from 1 (trial:i01.ug.leaf_0009.07) to 8 (trial:i01.ug.Block3_union_row8.03), with locus crop areas varying from a small ~684×164 dbu window (trial:i01.ug.leaf_0009.07) to a large ~3088×6264 dbu window (trial:i01.ug.leaf_0006.04). Large loci with more instances required more paired operations but produced equally clean outcomes. Do not limit the number of coupled move+resize pairs in a single repair; trial:i01.ug.Block3_union_row1.00 used six operations across three instance-polygon pairs and was accepted without new violations.

## Summary of Safe Repair Primitives for V1

Based exclusively on the measured record, the following primitives are confirmed safe under V1 DRC rules:

- Move a V1-hosting instance in +x or -x, with or without a companion M2 high-end resize, provided V1.M2.EN.2 enclosure is satisfied at the new position (trial:i01.ug.Block3_union_row2.01, trial:i01.ug.leaf_0006.04, trial:i01.ug.leaf_0009.07, trial:i01.ug.leaf_0013.09 for move-only; trial:i01.ug.Block3_union_row1.00, trial:i01.ug.Block3_union_row5.02, trial:i01.ug.Block3_union_row8.03, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0012.08 for paired move+resize).
- Extend the M2 high-end in x by a delta that meets or exceeds the instance move delta to cover the new via position plus the minimum enclosure margin required by V1.M2.EN.2 (trial:i01.ug.Block3_union_row1.00, trial:i01.ug.Block3_union_row8.03).
- Extend M2 in y when the via displacement threatens the y-direction enclosure, as confirmed by trial:i01.ug.leaf_0008.06.
- Apply multiple paired operations within a single repair locus when multiple instances and polygons are affected; scaling to 8 operations in one accepted trial (trial:i01.ug.Block3_union_row8.03) is within the measured safe range.