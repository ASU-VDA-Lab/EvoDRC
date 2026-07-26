## Repair Channel Outcomes

All nine unit-gate (`unit_gate` channel) trials that touched M2 were accepted with `decision: gated_in`; every one reports `conn_preserved: true`, `n_new_in_crop: 0`, and `n_new_out_of_crop: 0` (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.Block5_union_row6.01, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05, trial:i02.ug.Block5_union_row6.00, trial:i02.ug.leaf_0001.01, trial:i02.ug.leaf_0002.02). Both `cu_pool` channel trials that touched M2 were rejected (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00, trial:i02.cu.def:VIA_VIA23_1_3_36_36.01).

## Effective Repair Operations on M2

### X-Direction Instance Moves

Moving instances in the positive-x direction is the dominant effective repair action on M2. Every gated-in trial used one or more `move_instance` ops with positive `delta_dbu[0]`. Accepted x-moves span a range of 4 dbu to 104 dbu:

- 4 dbu per instance (trial:i01.ug.Block5_union_row6.01)
- 8 dbu per instance (trial:i02.ug.leaf_0001.01)
- 36 dbu per instance (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05)
- 72 dbu per instance (trial:i02.ug.leaf_0002.02)
- 104 dbu per instance (trial:i02.ug.Block5_union_row6.00)

Opposing-direction moves are also accepted when two instances in the same locus are moved in equal and opposite x-directions; trial:i01.ug.leaf_0002.03 moved i0056 by +36 dbu and i0103 by -36 dbu, both gated in with no new violations.

### X-High Resize-End Operations

Resizing the high-x end of an M2 polygon accompanies instance moves in several gated-in trials. Accepted resize magnitudes are: +36 dbu on polygon p967 (trial:i01.ug.Block5_union_row3.00), +72 dbu on polygon p974 (trial:i01.ug.leaf_0001.02), and +20 dbu on polygon p955 (trial:i02.ug.Block5_union_row6.00). All resize-end ops used `axis: x` and `end: high`, extending the wire in the same direction as the accompanying instance moves. No resize-end ops on `end: low` or on `axis: y` appear in the accepted M2 trials.

## Ineffective Repair Operations on M2

### Y-Direction Via Shape Resizing (cu_pool)

Shrinking M3 via shapes in the y-direction while touching M2 and V2 did not reduce M2 violations. Trial:i02.cu.def:VIA_VIA23_1_3_36_36.00 applied a single y-shrink of -40 dbu to the M3 shape of cell VIA_VIA23_1_3_36_36 and was rejected with `delta_total: 0` (no improvement across any window). Trial:i02.cu.def:VIA_VIA23_1_3_36_36.01 applied ten coordinated y-shrink ops across M3, V3, and M2 polygons (p893, p892, p891 each shrunk -32 dbu on both low and high ends) and was rejected with `decision: rejected_net_positive` and a net worsening of +5 violations globally (leaf_0005 rose from 20 to 28; leaf_0006 fell from 16 to 13, insufficient to offset). Avoid cu_pool via shape resizes in y as a strategy for resolving M2 spacing or width violations.

## Iteration-to-Iteration Move Magnitude Escalation

When a locus requires re-repair across iterations, move magnitudes increase. The unit Block5_union_row6 was repaired in both iterations: iter-1 moved i0025 and i0019 by +4 dbu each (trial:i01.ug.Block5_union_row6.01, gated in); iter-2 moved the same instances by +104 dbu each and added a +20 dbu resize-end on p955 (trial:i02.ug.Block5_union_row6.00, gated in). Unit leaf_0002 was repaired in both iterations with different loci: iter-1 used a +36 dbu move on i0056 (trial:i01.ug.leaf_0002.03); iter-2 moved i0017 by +72 dbu (trial:i02.ug.leaf_0002.02). Apply larger displacements when a prior smaller move on the same unit did not fully resolve violations by the next iteration.

## Co-Touched Layer Patterns

M2 violations are repaired jointly with adjacent metal and via layers. In seven of the nine gated-in trials, M2 repairs also touched M1 and V1 (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.Block5_union_row6.01, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05, trial:i02.ug.Block5_union_row6.00, trial:i02.ug.leaf_0002.02). In the remaining iter-2 unit-gate trial, M2 was repaired jointly with M3 and V2 (trial:i02.ug.leaf_0001.01). The cu_pool trials also touched M2 alongside M3 and V2 (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00, trial:i02.cu.def:VIA_VIA23_1_3_36_36.01), with trial:i02.cu.def:VIA_VIA23_1_3_36_36.01 additionally touching M4 and V3. Instance moves that co-displace M1 and V1 alongside M2 do not introduce new violations within the crop window, per all seven gated-in trials covering that stack.

## Design State and Iteration Boundary

All iter-1 trials share design state `ef66d47d838616255ced092ce8405c19a7101183e938e23fc839e77c033c8cfa`. All iter-2 trials share design state `c5292a284ad4664e01a2ba178591aa00c357719b470d7c2a01f1938996893820`. The design state change confirms that iter-1 repairs were committed to the layout before iter-2 trials ran. Iter-2 repairs operate on a modified geometry baseline that reflects all iter-1 gated-in changes.

## Locus Scope and Multi-Instance Coordination

Accepted repairs coordinate moves across two or more instances within the same locus. Trial:i01.ug.Block5_union_row3.00 moved i0117 and i0131 by the same +36 dbu delta; trial:i01.ug.Block5_union_row6.01 moved i0025 and i0019 by the same +4 dbu delta; trial:i02.ug.Block5_union_row6.00 moved i0025 and i0019 together by +104 dbu. When coordinating instance pairs, applying equal x-displacements to both instances in the same locus consistently yields zero new violations (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.Block5_union_row6.01, trial:i02.ug.Block5_union_row6.00, trial:i02.ug.leaf_0001.01).