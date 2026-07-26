## Operation Patterns

**X-direction moves dominate accepted repairs.** Every trial from iteration 1 through iteration 3 that touched V1 used positive x-direction moves of 36, 72, or 108 dbu, or a paired x-resize. All nine iteration-1 trials that applied pure x-moves recorded zero new in-crop violations (trial:i01.ug.Block3_union_row1.00, trial:i01.ug.Block3_union_row2.01, trial:i01.ug.Block3_union_row5.02, trial:i01.ug.Block3_union_row8.03, trial:i01.ug.leaf_0006.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0008.06, trial:i01.ug.leaf_0009.07, trial:i01.ug.leaf_0012.08). A single x-only move in the negative direction (-36,0) was also accepted without new violations (trial:i01.ug.leaf_0013.09).

**Y-direction moves introduce new violations.** The only trial that produced new in-crop violations (n_new_in_crop=10) was trial:i03.ug.leaf_0003.02, which applied (0,-96) deltas to two instances. All three trials containing a y-component of -96 dbu belong to this record. This trial was still accepted because connectivity was preserved, but the 10 new violations indicate that vertical displacement of V1-touching instances conflicts with V1.S.1 or V1.S.3 spacing constraints, which operate on projected vertical edges. Do not apply y-only moves to instances in a V1-dense region without evaluating spacing headroom along both M2 tracks and perpendicular directions.

## Move Granularity

**Use 36 dbu as the base x-step.** Accepted x-move deltas are 36, 72 (=2×36), and 108 (=3×36) dbu (trial:i01.ug.Block3_union_row1.00, trial:i02.ug.leaf_0001.00, trial:i01.ug.Block3_union_row8.03). A delta of 73 dbu was applied in trial:i03.ug.leaf_0001.00; this deviates from the 36-dbu grid by 1 dbu and is the only non-multiple-of-36 x-move in the history. Prefer grid-aligned multiples of 36 dbu to avoid sub-grid V1 edge positions that can trigger V1.M2.AUX.2 (V1 width must match M2 width perpendicular to M2 length) or V1.W.1 (minimum V1 width 18 nm).

## Resize-End Pairing

**Pair resize_end (axis=x, end=high) with the associated instance move whenever a V1-attached M2 polygon must be extended.** Three trials show this pattern directly:

- trial:i01.ug.leaf_0008.06: move_instance i0047 by (+36,0) and resize_end polygon p1261 by delta_dbu=36 on x-high.
- trial:i02.ug.leaf_0001.00: move_instance i0047 by (+72,0) and resize_end polygon p1261 by delta_dbu=72 on x-high.
- trial:i03.ug.leaf_0001.00: move_instance i0239 by (+73,0) and resize_end polygon p1226 by delta_dbu=130 on x-high.

In all three cases the resize delta equals or exceeds the move delta (36≥36, 72≥72, 130>73). The resize-end delta must be at least as large as the move delta to prevent the M2 enclosure from pulling away from the moved V1 and violating V1.M2.EN.2 (minimum enclosure of V1 by M2 on two opposite sides). When the instance move and the resize are unequal (as in trial:i03.ug.leaf_0001.00 at 73 vs 130), the extra resize extension provides additional M2 overlap and is still accepted.

**Target the correct polygon per iteration.** Iterations 1 and 2 both targeted polygon p1261 alongside instance i0047; iteration 3 targeted polygon p1226 alongside instance i0239. This shift corresponds to a change in design state ("8472bf..." → "bd3ea9...") after the iteration-2 commit, demonstrating that each successive state may require a different polygon to be resized to satisfy V1.M2.EN.2 or V1.M2.AUX.2.

## Multi-Instance Coordination

**Move multiple instances together with coordinated but not necessarily equal deltas.** Accepted trials apply heterogeneous deltas within the same repair step: trial:i01.ug.Block3_union_row1.00 moves i0233 by +36, i0246 by +108, and i0205 by +108. trial:i01.ug.Block3_union_row8.03 moves three instances by +36 and one by +108. Mixed deltas within a single trial are accepted without producing new violations, provided connectivity is maintained and the resulting geometry satisfies V1.S.1 spacing (minimum 18 nm same-track, 27 nm parallel-track, 18 nm aligned) and V1.M1.EN.1 (M1 must enclose V1 by 5 & 2 nm on opposite sides). Trials with 2–4 ops in a single crop region all cleared the crop-violation budget (trial:i01.ug.leaf_0008.06 at 3 ops, trial:i01.ug.Block3_union_row8.03 at 4 ops).

## Iterative Refinement Across Design States

**Each iteration commits a winning trial and advances the design state; subsequent iterations operate on the updated geometry.** Iteration 1 ran all 10 trials against state "fa7319...". Iteration 2 ran one trial against "8472bf...", the state after the iteration-1 commit. Iteration 3 ran two trials against "bd3ea9...". The increasing resize deltas (36 → 72 → 130) on the x-high end of M2 polygons across these iterations reflect a repair that has not yet fully closed the enclosure gap; each iteration requires a larger resize because the V1 instance and its M2 polygon are being incrementally repositioned (trial:i01.ug.leaf_0008.06, trial:i02.ug.leaf_0001.00, trial:i03.ug.leaf_0001.00). Continue increasing the resize delta in subsequent iterations if V1.M2.EN.2 or V1.M2.AUX.2 violations persist in this unit.

## Connectivity as the Acceptance Gate

**conn_preserved=true is the decisive acceptance criterion; new in-crop violations do not block gating.** All 13 trials carry conn_preserved=true and were accepted with decision="gated_in", including trial:i03.ug.leaf_0003.02 which introduced 10 new violations. Prioritize operations that preserve net connectivity when choosing between move candidates. However, operations producing new in-crop violations (like the y-moves in trial:i03.ug.leaf_0003.02) accumulate violations that future iterations must resolve, so prefer zero-new-violation moves when available (as demonstrated by all iteration-1 and iteration-2 trials except trial:i03.ug.leaf_0003.02).

## Layer Scope

**V1 violations are co-located with M1 and M2 geometry; repairs always touch all three layers simultaneously.** Every trial that involved V1 listed "M1", "M2", and "V1" in touched_layers. Trial:i03.ug.leaf_0003.02 additionally touched M3, M4, M5, V3, and V4 due to the wider locus, but V1-specific rules (V1.AUX.1: V1 must be inside M1 and M2; V1.M2.AUX.2: V1 width matches M2 perpendicular width) require that any polygon resize or instance move affecting V1 also updates the enclosing M1 and M2 shapes. Never move a V1 instance without verifying that its enclosing M1 and M2 polygons follow the move.