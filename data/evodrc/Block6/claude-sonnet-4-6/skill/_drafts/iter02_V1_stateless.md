## Coordinate Axis

All V1-affecting operations across the full twelve-trial history use the X axis exclusively. Every `move_instance` op carries delta_dbu of the form `[X, 0]` with zero Y displacement (trial:i01.ug.Block6_union_row3.00, trial:i01.ug.Block6_union_row5.01, trial:i01.ug.Block6_union_row7.02, trial:i01.ug.Block6_union_row8.03, trial:i01.ug.leaf_0001.04, trial:i01.ug.leaf_0011.05, trial:i01.ug.leaf_0015.06, trial:i01.ug.leaf_0018.07, trial:i02.ug.Block6_union_row4.00, trial:i02.ug.Block6_union_row7.01, trial:i02.ug.Block6_union_row8.02, trial:i02.ug.leaf_0004.04). Every `resize_end` op in the history also uses `axis:x`. Do not apply Y-axis displacements or Y-axis resizes to V1-containing units.

## Operation Pairing: move_instance and resize_end on M2

When a trial includes both `move_instance` and `resize_end` ops, the resize always acts on an M2 polygon, not on V1 directly. V1 polygons travel with their parent instances and are never directly resized. The M2 polygon end is extended in the same direction as the instance translation: `end:high` when the move is in +X (trial:i01.ug.leaf_0001.04, trial:i01.ug.leaf_0015.06, trial:i01.ug.Block6_union_row5.01, trial:i01.ug.Block6_union_row7.02 for instance i0093, trial:i02.ug.Block6_union_row4.00), and `end:low` when the move is in -X (trial:i01.ug.Block6_union_row7.02 for instance i0074, which moved [-36,0] while p1920 was resized with end:low by 56 dbu). Apply resize_end on M2 whenever a V1-carrying instance is translated, so that V1.M2.EN.2 enclosure and V1.M2.AUX.2 width alignment remain satisfied.

## M2 Resize Delta Offset

In trials where the co-moved instances all share the same displacement magnitude, the resize delta equals that magnitude plus 20 dbu. Confirmed cases:

- trial:i01.ug.leaf_0001.04: single instance i0404 moved 112 dbu; p2016 resized 132 dbu (+20).
- trial:i01.ug.leaf_0015.06: two instances i0213 and i0204 each moved 28 dbu; p1923 resized 48 dbu (+20).
- trial:i01.ug.Block6_union_row7.02: instance i0093 moved 104 dbu in +X; p1903 resized 124 dbu at end:high (+20). Instance i0074 moved 36 dbu in -X; p1920 resized 56 dbu at end:low (+20).

In trial:i02.ug.Block6_union_row4.00 where two instances moved different distances (i0319 by 56 dbu, i0410 by 112 dbu), p2020 was resized 132 dbu, consistent with the +20 offset applied to the larger move (112+20=132).

In trial:i01.ug.Block6_union_row5.01, four instances each moved 36 dbu while p2072 was resized 92 dbu, a 56-dbu offset that departs from the predominant +20 pattern. The geometry of p2072 and the four co-moved instances differs from the single-driver cases above; the resize delta in that trial reflects a larger required M2 extension than the +20 baseline.

## Multi-Instance Moves

Multiple instances sharing a V1.S.x spacing conflict are moved together in a single trial. trial:i01.ug.Block6_union_row3.00 moved three instances (i0471, i0324, i0481) by an identical [72,0] delta. trial:i01.ug.Block6_union_row5.01 moved four instances (i0015, i0459, i0437, i0446) by the same [36,0] delta alongside a resize. trial:i01.ug.leaf_0015.06 moved two instances (i0213, i0204) by the same [28,0] delta with one resize_end. Move all instances that are part of the same spacing violation in the same trial; displacing only a subset while neighbors remain in place does not resolve inter-instance spacing rules (V1.S.1, V1.S.2, V1.S.3, V1.S.4).

## Iterative Refinement: Coarse Move Followed by Fine Trim

Some instances require adjustment across consecutive iterations. Instance i0093 (unit Block6_union_row7) was moved 104 dbu in trial:i01.ug.Block6_union_row7.02 (iter 1) and then adjusted by a residual 4 dbu in trial:i02.ug.Block6_union_row7.01 (iter 2). Instance i0213 was moved 28 dbu in trial:i01.ug.leaf_0015.06 (iter 1) and then trimmed by 8 dbu in trial:i02.ug.Block6_union_row8.02 (iter 2). The fine-trim deltas (4 dbu and 8 dbu) are the smallest move magnitudes in the entire history and appear exclusively in iteration 2. A large displacement in iteration 1 resolves the primary violation; iteration 2 corrects the remaining sub-grid offset introduced by the coarse relocation.

## Move Magnitude Range

Observed instance move magnitudes: 4, 8, 28, 36, 56, 72, 104, and 112 dbu. The two smallest values (4 dbu in trial:i02.ug.Block6_union_row7.01; 8 dbu in trial:i02.ug.Block6_union_row8.02) are both iter-2 fine-trim adjustments on previously relocated instances. The largest values (104 and 112 dbu) appear in iter-1 primary repairs (trial:i01.ug.Block6_union_row7.02 and trial:i01.ug.leaf_0001.04, trial:i02.ug.Block6_union_row4.00).

## Connectivity and DRC Clean Outcome

All twelve trials report `conn_preserved: true`, `n_new_in_crop: 0`, and `n_new_out_of_crop: 0`. The combination of co-moving V1-carrying instances in X and extending the trailing M2 polygon end by move_delta + 20 dbu (or larger when multiple differing-magnitude moves share one M2 end, as in trial:i01.ug.Block6_union_row5.01) preserves both electrical connectivity and DRC cleanliness throughout the block.