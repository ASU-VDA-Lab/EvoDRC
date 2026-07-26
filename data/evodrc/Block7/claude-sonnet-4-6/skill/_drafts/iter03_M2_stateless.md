## Gate Behavior and Acceptance Criterion

Every trial in this layer's history carried `decision: gated_in` with `conn_preserved: true`. Connectivity preservation is the sufficient condition for acceptance regardless of in-crop violation count. trial:i01.ug.Block7_union_row21.11 introduced 9 new in-crop violations and was accepted. trial:i01.ug.Block7_union_row22.12, trial:i01.ug.Block7_union_row24.14, and trial:i01.ug.leaf_0002.23 each introduced 2 new in-crop violations and were accepted. trial:i01.ug.Block7_union_row13.03, trial:i01.ug.Block7_union_row19.09, trial:i01.ug.Block7_union_row20.10, trial:i01.ug.Block7_union_row4.16, trial:i01.ug.Block7_union_row5.17, trial:i01.ug.leaf_0008.24, trial:i01.ug.leaf_0024.25, trial:i03.ug.leaf_0008.06 each introduced 1. trial:i02.ug.leaf_0017.09, trial:i02.ug.leaf_0022.10, trial:i03.ug.leaf_0001.03, and trial:i03.ug.leaf_0007.05 each introduced 3. All were accepted because `conn_preserved: true`. Never trade away connectivity to reduce `n_new_in_crop`.

The `n_new_out_of_crop` field is 0 in every trial in this history. Repairs must not push violations outside the crop boundary; all trials demonstrate that the operation sets chosen are tight enough to contain effects within the locus window.

## Primary Repair Operation: move_instance

`move_instance` is the dominant operation for M2 repair and appears in every trial without exception. Many trials achieve full repair with `move_instance` as the only operation: trial:i01.ug.leaf_0001.22 (1 op, delta [108,0]), trial:i01.ug.Block7_union_row11.01 (2 ops, both `move_instance`), trial:i01.ug.Block7_union_row22.12 (1 op, delta [4,0]), trial:i02.ug.leaf_0017.09 (1 op, delta [0,48]), trial:i02.ug.leaf_0022.10 (1 op, delta [3,0]), trial:i03.ug.Block7_union_row20.02 (1 op, delta [36,0]), and trial:i03.ug.leaf_0008.06 (1 op, delta [108,0]).

Moving a cell instance propagates the displacement to all M2 geometry within it along with the V1 vias that land on those segments. This simultaneously resolves M2 spacing violations (M2.S.1, M2.S.2, M2.S.3, M2.S.4, M2.S.5, M2.S.6, M2.S.7) and preserves V1.M2.EN.2 and V1.M2.AUX.2 enclosure without requiring separate polygon edits on the via layer.

## Displacement Quantization

The canonical x-axis step is 36 dbu. It appears as the sole or dominant displacement magnitude in trial:i01.ug.Block7_union_row11.01, trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row14.04, trial:i01.ug.Block7_union_row15.05, trial:i01.ug.Block7_union_row16.06, trial:i01.ug.Block7_union_row17.07, trial:i01.ug.Block7_union_row18.08, trial:i01.ug.Block7_union_row21.11, trial:i01.ug.Block7_union_row23.13, trial:i01.ug.Block7_union_row3.15, trial:i01.ug.Block7_union_row4.16, trial:i01.ug.Block7_union_row5.17, trial:i01.ug.Block7_union_row6.18, trial:i01.ug.Block7_union_row8.20, trial:i01.ug.Block7_union_row9.21, trial:i01.ug.leaf_0002.23, trial:i02.ug.Block7_union_row12.01, trial:i02.ug.Block7_union_row13.02, trial:i02.ug.Block7_union_row22.05, trial:i03.ug.Block7_union_row13.01, trial:i03.ug.Block7_union_row20.02, and others. 72 dbu (double step) appears in trial:i01.ug.Block7_union_row18.08, trial:i01.ug.Block7_union_row19.09, trial:i01.ug.Block7_union_row23.13, trial:i02.ug.Block7_union_row20.04. 108 dbu (triple step) appears in trial:i01.ug.Block7_union_row7.19, trial:i01.ug.leaf_0001.22, trial:i03.ug.leaf_0008.06. Use multiples of 36 dbu as the default x-axis displacement unit.

Sub-36 or non-multiple displacements are used for residual near-miss corrections. trial:i02.ug.leaf_0022.10 uses 3 dbu; trial:i01.ug.Block7_union_row22.12 uses 4 dbu; trial:i01.ug.Block7_union_row6.18 uses 28 dbu; trial:i01.ug.Block7_union_row10.00 uses 52 dbu; trial:i01.ug.Block7_union_row24.14 uses 64 dbu. In every case where a fine displacement appears, at least one standard-multiple move is also present in the same trial or in a prior iteration's repair of the same unit, confirming these are residual trims rather than primary corrections.

## resize_end: Adjusting Polygon Tips

When a spacing violation is localized to a M2 polygon tip that cannot be resolved by an instance move alone (for example when the tip extends past the instance boundary or violates M2.S.2 or M2.S.7 through projection), apply `resize_end` to adjust that tip directly.

Use `resize_end` with `end: high` to extend the far (high-coordinate) tip:
- trial:i01.ug.Block7_union_row5.17 extends p3737 by +92 dbu and p3746 by +92 dbu.
- trial:i01.ug.Block7_union_row7.19 extends p3317 by +128 dbu.
- trial:i01.ug.Block7_union_row14.04 extends p3200 by +72 dbu and p3215 by +56 dbu.
- trial:i01.ug.Block7_union_row24.14 extends p3058 by +136 dbu, p3635 by +120 dbu, p3564 by +128 dbu.
- trial:i02.ug.Block7_union_row9.06 extends p3683 by +112 dbu.
- trial:i02.ug.Block7_union_row22.05 extends p3527 by +92 dbu.

Use `resize_end` with `end: low` to retract the near (low-coordinate) tip. A 56 dbu retraction on the x low end recurs across multiple trials: trial:i01.ug.Block7_union_row3.15 retracts p3384 by 56 dbu, trial:i01.ug.Block7_union_row8.20 retracts p3430 by 56 dbu, trial:i01.ug.Block7_union_row17.07 retracts p3187 by 56 dbu, trial:i01.ug.Block7_union_row13.03 retracts p3526 by 56 dbu. The 56 dbu retraction is the standard correction magnitude for a tip that over-reaches into a projection spacing zone. trial:i03.ug.leaf_0002.04 applies -88 dbu on the x low end of p3300, a larger retraction used when the tip violation is more severe.

A y-axis resize_end appears in trial:i03.ug.leaf_0002.04, which extends p2720 by +20 dbu on the high y end to satisfy a vertical enclosure requirement on a crop touching M1, M2, M3, V1, V2.

## Symmetric resize Operations

The symmetric `resize` operation (no `end` field) shifts both ends of a polygon axis uniformly and appears when the entire polygon needs to be widened or moved along its length without changing its midpoint position.

- trial:i01.ug.Block7_union_row15.05 applies +160 dbu x-resize to p3586.
- trial:i01.ug.Block7_union_row19.09 applies +40 dbu x-resize to p3619, -72 dbu x-resize to p3654, +72 dbu x-resize to p3523 (three polygons in one trial, representing coordinated width adjustment across multiple M2 wires in a dense crop).
- trial:i02.ug.Block7_union_row15.03 applies +96 dbu y-resize to p3592 after moving instance i0913 by -96 dbu x and instance i1062 by [0,-84].
- trial:i03.ug.leaf_0007.05 applies -48 dbu on the low y end and -48 dbu on the high y end of p3592 (shrinking it by 96 dbu total in y), correcting an oversize that remained after the iter 2 expansion.

## Multi-Instance Coordination Within a Crop

Dense crops require moving multiple instances simultaneously to avoid opening new spacing violations between them while closing the target violation. Never move a single instance when adjacent instances have correlated M2 geometry; always include all geometrically coupled instances in the same repair set.

trial:i01.ug.Block7_union_row14.04 moves 8 instances and resizes 2 polygons (11 total ops) and achieves n_new_in_crop=0. trial:i01.ug.Block7_union_row15.05 moves 7 instances and resizes 1 polygon (8 ops) with n_new_in_crop=0. trial:i01.ug.Block7_union_row19.09 moves 4 instances and resizes 3 polygons (9 ops) with n_new_in_crop=1. trial:i01.ug.Block7_union_row18.08 moves 5 instances and resizes 2 polygon ends (8 ops) with n_new_in_crop=0.

When instances within the same crop move in opposite directions, the opposing displacement creates additional separation on the retreating side while the advancing moves clear violations on the other side. trial:i01.ug.Block7_union_row14.04 moves i0519 by -36 dbu while all other instances move +36 to +108 dbu. trial:i01.ug.Block7_union_row18.08 moves i0428 by -72 dbu while five other instances move +36 to +72 dbu. trial:i01.ug.Block7_union_row23.13 moves i0190 by -36 dbu while four instances move +36 to +108 dbu. Use opposing moves when two M2 wires in the same crop are simultaneously too close together on one side and too close to a third wire on the other side.

## Y-Axis Adjustments and Multi-Layer Coupling

Y-axis moves appear when M2 vertical spacing or V2.M2.EN.1 enclosure requirements drive the correction. They always co-move the instance and its associated polygon by an identical delta.

trial:i01.ug.Block7_union_row16.06 moves instances i0336 and i0308 by [0,-12] and translates M2 polygon p3516 by -12 dbu in y; the trial touches M1, M2, M3, V1, V2, confirming a V2 enclosure cascade. trial:i01.ug.leaf_0095.26 moves instances i0177 and i0184 by [0,+48] and extends p3537 by +48 dbu on the y high end, also touching M1, M2, M3, V1, V2.

trial:i02.ug.leaf_0001.07 moves instance i1643 and polygon p3383 together by [0,-57] dbu in y (touching M2, M3, V2 only). trial:i03.ug.leaf_0001.03 later moves the same instance i1643 and polygon p3383 by [0,+21] dbu in y, a partial reversal that converges to the correct y-position after the iter 2 overshoot. Always move the polygon and instance by the same y-delta when correcting via enclosure on M2/V2 contacts.

trial:i02.ug.leaf_0014.08 moves instances i0519 and i0524 by [0,-12] and translates polygon p3515 by -12 dbu in y (touching M1, M2, M3, V1, V2).

## add_polygon for M2 Patch Geometry

trial:i01.ug.Block7_union_row20.10 adds an M2 polygon with corners [[5992,22824],[5992,22896],[6048,22896],[6048,22824]], a 56 dbu × 72 dbu rectangle, paired with a -36 dbu x-move of instance i0753. The trial was accepted with n_new_in_crop=1 because connectivity was preserved. This is the only add_polygon on M2 in the full history; all other add_polygon operations in this history target M3 (trial:i03.ug.leaf_0002.04). When adding a patch polygon on M2, coordinate its position with any concurrent instance move to prevent the new polygon's tips from creating M2.S.1 or M2.S.2 violations with the repositioned instance geometry.

## Iterative Convergence on Persistent Units

Three units required repair across all three iterations, each converging with monotonically decreasing correction magnitudes:

**leaf_0001**: trial:i01.ug.leaf_0001.22 applied a single +108 dbu x-move (touching M1, M2, V1). trial:i02.ug.leaf_0001.07 applied a -57 dbu y-move on M2, M3, V2. trial:i03.ug.leaf_0001.03 applied a +21 dbu y-correction on the same instance i1643 and polygon p3383, partially reversing the iter 2 displacement and converging to the target position. This overshoot-then-correct pattern across iterations is resolved by applying the smaller correction in the direction opposite the prior delta.

**Block7_union_row13**: trial:i01.ug.Block7_union_row13.03 performed 6 ops including opposing resize_end calls and 3 instance moves (n_new_in_crop=1). trial:i02.ug.Block7_union_row13.02 applied 3 move_instance ops of 36, -72, and +36 dbu (n_new_in_crop=0). trial:i03.ug.Block7_union_row13.01 applied 2 move_instance ops each at +36 dbu (n_new_in_crop=0). Op count decreased 6→3→2.

**Block7_union_row20**: trial:i01.ug.Block7_union_row20.10 combined an add_polygon with a -36 dbu instance move (n_new_in_crop=1). trial:i02.ug.Block7_union_row20.04 moved 2 instances and applied a +56 dbu resize_end (n_new_in_crop=0). trial:i03.ug.Block7_union_row20.02 applied a single +36 dbu move_instance (n_new_in_crop=0). Op count decreased 2→3→1 with the iter 2 increase explained by a previously uncovered adjacent violation.

When a unit appears in successive iterations with shrinking delta magnitudes, apply the minimum viable displacement (36 dbu single move_instance) in the final correction pass, as demonstrated by trial:i03.ug.Block7_union_row13.01 and trial:i03.ug.Block7_union_row20.02.

## M2–V1 and M2–V2 Co-Movement Constraints

Trials touching M1, M2, and V1 (the large majority: trial:i01.ug.Block7_union_row10.00 through trial:i01.ug.Block7_union_row9.21, trial:i02.ug.Block7_union_row12.01 through trial:i02.ug.Block7_union_row9.06, trial:i03.ug.Block7_union_row10.00 through trial:i03.ug.leaf_0008.06) confirm that V1 vias reside within instance boundaries containing M2 geometry. Instance moves carry both M2 and V1 together, preserving V1.M2.EN.2 and V1.M2.AUX.2 automatically. Direct resize_end operations on an M2 polygon (without a matching V1 adjustment) are safe when the V1 via is not at the resized tip; trial:i01.ug.Block7_union_row5.17, trial:i01.ug.Block7_union_row7.19, and trial:i01.ug.Block7_union_row17.07 all apply resize_end without V1 polygon ops and are accepted.

Trials touching M2, M3, and V2 (trial:i02.ug.leaf_0001.07, trial:i03.ug.leaf_0001.03, trial:i01.ug.leaf_0095.26, trial:i01.ug.Block7_union_row16.06, trial:i02.ug.leaf_0014.08, trial:i03.ug.leaf_0011.07) require the instance and the M2/M3 polygon to move by the same y-delta to satisfy V2.M2.EN.1. In every such trial the polygon `move` and `move_instance` deltas are identical (e.g., both -12 dbu in trial:i02.ug.leaf_0014.08; both +21 dbu y in trial:i03.ug.leaf_0001.03; both +48 dbu y in trial:i01.ug.leaf_0095.26 for instance i0177 and polygon p3537). A mismatch between instance and polygon y-displacement breaks the enclosure relationship and must be avoided.