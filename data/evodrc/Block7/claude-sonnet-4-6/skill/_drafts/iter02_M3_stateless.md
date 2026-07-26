## Observed Repair Strategies

All four measured trials on M3 resulted in `decision: gated_in` with `conn_preserved: true` and zero new violations (`n_new_in_crop: 0`, `n_new_out_of_crop: 0`). Every repair that touched M3 also modified V2 (trial:i01.ug.Block7_union_row16.06, trial:i01.ug.leaf_0095.26, trial:i02.ug.leaf_0001.07, trial:i02.ug.leaf_0014.08), confirming that M3 geometry changes must be co-evaluated against V2.M3.EN.2 and V2.M3.AUX.2 constraints, not M3 spacing rules in isolation.

## Move Operations

The dominant repair primitive across both iterations is the coordinated y-axis move: a `move_instance` and a `move` on the associated M3 polygon are issued with the same delta in the same operation batch. This pattern appears in trial:i02.ug.leaf_0001.07 (delta_dbu `[0,-57]` on both `i1643` and `p3383`), trial:i02.ug.leaf_0014.08 (delta_dbu `[0,-12]` on `i0519`, `i0524`, and `p3515`), and trial:i01.ug.Block7_union_row16.06 (delta_dbu `[0,-12]` on `i0336`, `i0308`, and `p3516`). Do not move an M3 polygon without also moving its owning instance by the same delta; all three trials that used this pattern cleared violations without introducing new ones.

X-axis instance moves appear alongside y-axis M3 polygon moves in multi-instance batches (trial:i01.ug.Block7_union_row16.06: `i0928` and `i0407` moved `[-36,0]`, `i0320` moved `[36,0]`; trial:i02.ug.leaf_0014.08: `i0519` and `i0524` moved `[0,-12]`). Apply x-axis moves only to instances, not directly to M3 polygons in those same batches, consistent with the practice observed across all trials.

## Resize Operations

The only measured `resize_end` operations on M3 are y-axis extensions of the high end: `p2432` extended by `+68 dbu` and `p3537` extended by `+48 dbu`, both in trial:i01.ug.leaf_0095.26. Both succeeded without new violations. Apply `resize_end` only on the `high` end along the y-axis when extending an M3 tip; the same trial also included `move_instance` operations (delta `[0,48]` on `i0177` and `i0184`, delta `[36,0]` on `i0175`), confirming that resize on an M3 polygon requires accompanying instance adjustments to maintain V2 enclosure rules.

## V2 Co-dependency

Every trial that touched M3 simultaneously touched V2 (trial:i01.ug.Block7_union_row16.06, trial:i01.ug.leaf_0095.26, trial:i02.ug.leaf_0001.07, trial:i02.ug.leaf_0014.08). Rules V2.M3.EN.2 and V2.M3.AUX.2 require V2 to be fully enclosed by M3 with at least 5 nm on two opposite sides and V2 width to match M3 width in the perpendicular direction. Do not issue an M3 polygon move or resize without verifying V2.M3.EN.2 and V2.M3.AUX.2 clearance after the operation; all four trials satisfied this by batching V2-touching instance moves with the M3 geometry changes.

## Operation Batch Discipline

All successful trials used multi-operation batches (`n_ops` ranging from 2 to 6) where M3 polygon changes and instance moves were submitted together in one atomic batch. Do not split M3 polygon moves from their instance moves across separate batches; the single-batch pattern in all four trials (trial:i01.ug.Block7_union_row16.06, trial:i01.ug.leaf_0095.26, trial:i02.ug.leaf_0001.07, trial:i02.ug.leaf_0014.08) preserved connectivity and produced no out-of-crop new violations.

## Geometry Constraints (Rules Reference)

The minimum M3 width is 18 nm (M3.W.1) and minimum area is 504 nm² (M3.A.1). When resizing M3 tips, ensure that both the width at the tip cross-section and the overall polygon area remain above these thresholds after the delta is applied. The resize deltas used in the only measured resize trial (trial:i01.ug.leaf_0095.26, `+68 dbu` and `+48 dbu`) were both positive extensions, which increase area and do not risk M3.A.1 violations; reductions would require an area check.

Side-to-side spacing (M3.S.1, 18 nm) applies only when both opposing edges exceed 36 nm. Tip-to-side (M3.S.2, 25 nm) and tip-to-tip (M3.S.3/M3.S.4/M3.S.5, 27–31 nm depending on tip widths) thresholds are stricter and govern narrow end geometries. Corner-to-corner euclidean spacing (M3.S.6, 20 nm) activates for cases not covered by projection-based spacing. The measured y-axis move magnitudes (12 dbu, 57 dbu in trial:i02.ug.leaf_0001.07 and trial:i02.ug.leaf_0014.08) resulted in zero new violations, but the records do not expose post-move absolute coordinates, so these deltas are not directly usable as safe spacing margins — they are evidence that the repair strategy class succeeds, not that any specific delta universally suffices.

Non-orthogonal edges are prohibited on M3 (GEOMETRY.NONORTHOGONAL rule). All ops in the measured history are axis-aligned moves and axis-aligned resize_end operations; never apply rotations or diagonal transforms to M3 polygons.