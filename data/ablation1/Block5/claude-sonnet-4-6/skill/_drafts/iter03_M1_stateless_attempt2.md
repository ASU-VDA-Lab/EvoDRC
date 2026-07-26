## Trial Acceptance and Connectivity

All nine trials in the measured history received a `gated_in` decision with `conn_preserved: true` (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.Block5_union_row6.01, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05, trial:i02.ug.Block5_union_row6.00, trial:i02.ug.leaf_0002.02, trial:i03.ug.leaf_0002.01). No trial in the measured history was rejected.

## Co-Modified Layers

Every trial in the history touched layers M1, M2, and V1 together; no trial modified M1 in isolation (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.Block5_union_row6.01, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05, trial:i02.ug.Block5_union_row6.00, trial:i02.ug.leaf_0002.02, trial:i03.ug.leaf_0002.01).

## Move Direction

All `move_instance` deltas use x-displacement only. No y-direction move appears in any trial record (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.Block5_union_row6.01, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05, trial:i02.ug.Block5_union_row6.00, trial:i02.ug.leaf_0002.02, trial:i03.ug.leaf_0002.01).

## Move Delta Magnitudes

The following x-displacement values are recorded across all accepted trials: +4 dbu (trial:i01.ug.Block5_union_row6.01, two instances); +36 dbu (trial:i01.ug.Block5_union_row3.00 applied to two instances, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03 for instance i0056, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05, trial:i03.ug.leaf_0002.01); -36 dbu (trial:i01.ug.leaf_0002.03 for instance i0103); +72 dbu (trial:i02.ug.leaf_0002.02); +104 dbu (trial:i02.ug.Block5_union_row6.00 applied to two instances). The +36 dbu step is the value recorded most frequently, appearing in six of the nine trials.

Opposing moves within a single operation set—one instance shifted +36 dbu and another shifted -36 dbu in the same trial—were accepted (trial:i01.ug.leaf_0002.03).

## Resize Operations

Three `resize_end` operations are recorded. All three used `axis: x` and `end: high`, with the following per-polygon deltas: +36 dbu on polygon p967 (trial:i01.ug.Block5_union_row3.00); +72 dbu on polygon p974 (trial:i01.ug.leaf_0001.02); +20 dbu on polygon p955 (trial:i02.ug.Block5_union_row6.00). All three produced `n_new_in_crop: 0` and `n_new_out_of_crop: 0` and were accepted. When extending an M1 polygon, apply `resize_end` on the x-axis high end, following trial:i01.ug.Block5_union_row3.00, trial:i01.ug.leaf_0001.02, and trial:i02.ug.Block5_union_row6.00.

## Multi-Iteration Unit Repairs

Unit `Block5_union_row6` required repair across two iterations. Iteration 1 applied two +4 dbu moves (trial:i01.ug.Block5_union_row6.01); iteration 2 applied two +104 dbu moves plus a +20 dbu `resize_end` on polygon p955 (trial:i02.ug.Block5_union_row6.00). The iteration-2 repair therefore used a move delta 26× larger than iteration 1 and added a resize step not present in iteration 1.

Unit `leaf_0002` required repair in all three iterations: a +36/-36 dbu opposing-move pair in iteration 1 (trial:i01.ug.leaf_0002.03); a +72 dbu move in iteration 2 (trial:i02.ug.leaf_0002.02); a +36 dbu move in iteration 3 (trial:i03.ug.leaf_0002.01). Do not treat a single-iteration repair of `leaf_0002` as complete; the unit required further correction in every subsequent iteration, as shown in trial:i01.ug.leaf_0002.03, trial:i02.ug.leaf_0002.02, and trial:i03.ug.leaf_0002.01.

## Residual Violation Introduced in Iteration 3

Trial:i03.ug.leaf_0002.01 is the only record with `n_new_in_crop: 1`; all other trials recorded `n_new_in_crop: 0`. Despite this nonzero value, the trial was accepted (`gated_in`, `conn_preserved: true`). Future repairs targeting `leaf_0002` must address the one residual in-crop violation introduced by trial:i03.ug.leaf_0002.01.

## Design State Progression

Three distinct `design_state` hashes appear in the history: `ef66d47d...` for all six iteration-1 trials, `c5292a28...` for the two iteration-2 trials, and `d7ef52f1...` for the single iteration-3 trial. Each state transition confirms that committed operations from one iteration altered M1 (and co-layer) geometry before the next iteration executed.