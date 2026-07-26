## Repair Operation Patterns

All M2-touching repairs in this dataset used two operation types: `move_instance` and `resize_end`. Every `move_instance` op carried a displacement vector with zero y-component (`delta_dbu = [X, 0]`), confining all observed instance shifts to the x-axis (trial:i01.ug.Block6_union_row3.00, trial:i01.ug.Block6_union_row5.01, trial:i01.ug.Block6_union_row7.02, trial:i01.ug.Block6_union_row8.03, trial:i01.ug.leaf_0001.04, trial:i01.ug.leaf_0011.05, trial:i01.ug.leaf_0015.06, trial:i01.ug.leaf_0018.07, trial:i02.ug.Block6_union_row4.00, trial:i02.ug.Block6_union_row7.01, trial:i02.ug.Block6_union_row8.02, trial:i02.ug.leaf_0004.04, trial:i03.ug.leaf_0001.00). All `resize_end` operations also targeted `axis:x` (trial:i01.ug.Block6_union_row5.01, trial:i01.ug.Block6_union_row7.02, trial:i01.ug.leaf_0001.04, trial:i01.ug.leaf_0015.06, trial:i02.ug.Block6_union_row4.00).

## Move-Instance Displacement Magnitudes

Observed x-axis displacement magnitudes for `move_instance` range from 4 dbu (trial:i02.ug.Block6_union_row7.01) to 112 dbu (trial:i01.ug.leaf_0001.04). Intermediate values include 8 dbu (trial:i02.ug.Block6_union_row8.02), 28 dbu (trial:i01.ug.leaf_0015.06), 36 dbu (trial:i01.ug.Block6_union_row5.01, trial:i01.ug.Block6_union_row8.03, trial:i01.ug.leaf_0011.05, trial:i01.ug.leaf_0018.07, trial:i03.ug.leaf_0001.00), 72 dbu (trial:i01.ug.Block6_union_row3.00, trial:i02.ug.leaf_0004.04), and 104 dbu (trial:i01.ug.Block6_union_row7.02). Small displacements of 4-8 dbu are sufficient for some repairs without introducing new violations, as confirmed by the zero-new-violation outcomes in trial:i02.ug.Block6_union_row7.01 and trial:i02.ug.Block6_union_row8.02.

## Resize-End Magnitudes and End Selection

`resize_end` operations on axis:x used the following delta values: 48 dbu at `end:high` (trial:i01.ug.leaf_0015.06), 56 dbu at `end:low` (trial:i01.ug.Block6_union_row7.02), 92 dbu at `end:high` (trial:i01.ug.Block6_union_row5.01), 124 dbu at `end:high` (trial:i01.ug.Block6_union_row7.02), 132 dbu at `end:high` (trial:i01.ug.leaf_0001.04, trial:i02.ug.Block6_union_row4.00). Both `end:high` and `end:low` adjustments appear together within a single successful repair (trial:i01.ug.Block6_union_row7.02).

## Connectivity Preservation Under unit_gate

Every trial in the `unit_gate` channel reached `decision: gated_in`, preserved connectivity (`conn_preserved: true`), and introduced zero new violations in the crop region (`n_new_in_crop: 0`, `n_new_out_of_crop: 0`), spanning trial:i01.ug.Block6_union_row3.00 through trial:i03.ug.leaf_0001.00 across iterations 1, 2, and 3.

## Via Shape Adjustment via cu_pool

The `cu_pool` channel applied via-shape adjustments to cell `VIA_VIA23_1_3_36_36` on layer V2, which also modified M2 geometry (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). This trial reduced total violations by 78 (delta_total: -78), with reductions of 42 in unit leaf_0019 (from 139 to 97) and 36 in unit leaf_0020 (from 154 to 118). All via ops in that trial targeted axis:x and combined `move_via_shape` and `resize_via_shape` on three shape indices.

## V1 Enclosure Interaction

V1.M2.EN.2 requires M2 to enclose V1 by at least 5 nm on two opposite sides; V1.M2.AUX.2 requires V1 width to match M2 width in the direction perpendicular to M2 length. All unit_gate trials that shifted instances on x-axis simultaneously listed M1, M2, and V1 as touched layers (trial:i01.ug.Block6_union_row3.00, trial:i01.ug.Block6_union_row5.01, trial:i01.ug.Block6_union_row7.02, trial:i01.ug.Block6_union_row8.03, trial:i01.ug.leaf_0001.04, trial:i01.ug.leaf_0011.05, trial:i01.ug.leaf_0015.06, trial:i01.ug.leaf_0018.07, trial:i02.ug.Block6_union_row4.00, trial:i02.ug.Block6_union_row7.01, trial:i02.ug.Block6_union_row8.02, trial:i02.ug.leaf_0004.04, trial:i03.ug.leaf_0001.00), confirming that V1 positions track M2 during instance moves and that enclosure and width-match constraints are satisfied jointly by the instance-level move.

## M2.S.7 Combined Constraint Context

M2.S.7 forbids co-location of an 18 nm tip-to-tip gap with side-to-side spacing <= 32 nm and requires parallel run length >= 35 nm when side spacing <= 32 nm. The larger `resize_end` extensions of 92-132 dbu at `end:high` observed in trial:i01.ug.Block6_union_row5.01, trial:i01.ug.leaf_0001.04, trial:i01.ug.Block6_union_row7.02, and trial:i02.ug.Block6_union_row4.00 lengthen the horizontal polygon extent, increasing parallel run length. Smaller extensions of 48-56 dbu (trial:i01.ug.leaf_0015.06, trial:i01.ug.Block6_union_row7.02) appear paired with concurrent instance moves rather than standing alone.

## Multi-Instance Co-Movement

Several repairs moved multiple instances by identical displacements within the same trial: three instances each shifted 72 dbu (trial:i01.ug.Block6_union_row3.00), four instances each shifted 36 dbu before a single resize_end (trial:i01.ug.Block6_union_row5.01), and two instances each shifted 28 dbu flanking a resize_end (trial:i01.ug.leaf_0015.06). In each of these trials the outcome was `gated_in` with zero new violations, showing that equal co-displacement of related instances is compatible with M2 spacing and enclosure rules.

## Iteration Progression and Residual Correction

Iteration 1 addressed eight unit_gate units and one cu_pool target (trial:i01.ug.Block6_union_row3.00 through trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). Iteration 2 revisited two units from iteration 1 -- Block6_union_row7 (trial:i02.ug.Block6_union_row7.01) and Block6_union_row8 (trial:i02.ug.Block6_union_row8.02) -- with smaller displacements of 4 dbu and 8-36 dbu respectively, indicating residual violations remained after the first-pass moves of 104 dbu and 36 dbu. Iteration 3 applied a 36 dbu move to leaf_0001 (trial:i03.ug.leaf_0001.00), a unit that had received a 112 dbu move plus 132 dbu resize in iteration 1 (trial:i01.ug.leaf_0001.04), confirming that multi-iteration refinement with successively smaller adjustments is a documented trajectory for this design's M2 repairs.