**Repair Acceptance Criterion**

Every trial in the M1 history carries `decision:"gated_in"` with `conn_preserved:true` and `reason:"conn_preserved"`. This is uniform across all 37 records from iter 1 and iter 2 (trial:i01.ug.Block7_union_row10.00 through trial:i02.ug.leaf_0022.10). Connectivity preservation is the gating condition for acceptance; n_new_in_crop does not block acceptance when connectivity is preserved.

Trials accepted with nonzero n_new_in_crop include: trial:i01.ug.Block7_union_row21.11 (9 new in crop), trial:i01.ug.Block7_union_row22.12 (2), trial:i01.ug.Block7_union_row24.14 (2), trial:i01.ug.leaf_0002.23 (2), trial:i02.ug.leaf_0017.09 (3), trial:i02.ug.leaf_0022.10 (3), trial:i01.ug.Block7_union_row13.03 (1), trial:i01.ug.Block7_union_row19.09 (1), trial:i01.ug.Block7_union_row4.16 (1), trial:i01.ug.Block7_union_row5.17 (1), trial:i01.ug.leaf_0024.25 (1). All are gated in under reason:"conn_preserved".

**Operation Types on M1**

Two operation types directly modify M1 geometry: `move_instance` and `resize_end` (or `resize`). `move_instance` appears in every accepted trial, including single-operation trials such as trial:i01.ug.leaf_0001.22, trial:i01.ug.Block7_union_row22.12, and trial:i02.ug.leaf_0017.09. `resize_end` on the x-axis appears in the majority of multi-operation trials where M1 polygon geometry requires adjustment after instance displacement (trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row14.04, trial:i01.ug.Block7_union_row24.14, trial:i02.ug.Block7_union_row9.06, trial:i02.ug.Block7_union_row20.04). Full-polygon `resize` (shifting both ends by the same amount) appears in trial:i01.ug.Block7_union_row15.05 and trial:i01.ug.Block7_union_row19.09.

**Co-modification of M1, M2, and V1**

In every accepted trial, `touched_layers` includes M1, M2, and V1 together. This holds even in the simplest single-operation trials: trial:i01.ug.Block7_union_row22.12 (1 op, move_instance [4,0]), trial:i01.ug.leaf_0001.22 (1 op, move_instance [108,0]), trial:i02.ug.leaf_0017.09 (1 op, move_instance [0,48]), and trial:i02.ug.leaf_0022.10 (1 op, move_instance [3,0]). Do not isolate M1 polygon edits from V1 co-modification; accepted repairs always include V1 in the touched set as part of the same operation set (trial:i01.ug.Block7_union_row11.01, trial:i01.ug.Block7_union_row6.18, trial:i02.ug.Block7_union_row12.01).

A subset of trials also touches M3 and V2: trial:i01.ug.Block7_union_row16.06, trial:i01.ug.leaf_0095.26, and trial:i02.ug.leaf_0014.08. These are the trials in which y-axis instance displacements propagate across multiple metal layers.

**Pairing move_instance with resize_end**

When instance movement is combined with polygon end extension in the same operation set, the resize_end addresses enclosure at the M1 polygon boundary affected by the instance shift. Always pair resize_end with the associated move_instance operations in the same operation set whenever the instance displacement shifts a polygon end relative to the via it must enclose (trial:i01.ug.Block7_union_row3.15, trial:i01.ug.Block7_union_row7.19, trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row14.04, trial:i01.ug.Block7_union_row24.14, trial:i02.ug.Block7_union_row9.06, trial:i02.ug.Block7_union_row20.04).

Specific examples of this pairing:
- trial:i01.ug.Block7_union_row3.15: i1623 moved [-36,0]; p3384 extended resize_end low+56.
- trial:i01.ug.Block7_union_row7.19: i1446 moved [108,0]; p3317 extended resize_end high+128.
- trial:i02.ug.Block7_union_row9.06: i1150 moved [56,0]; p3683 extended resize_end high+112.
- trial:i01.ug.Block7_union_row14.04: i0874 moved [36,0] with p3200 resize_end high+72; i0915 moved [36,0] with p3215 resize_end high+56.
- trial:i01.ug.Block7_union_row13.03: p3526 receives both resize_end low+56 and resize_end high+100 alongside instance moves of [136,0].

**resize_end Direction and Magnitude**

resize_end operations on M1 polygons use both "high" and "low" end targets along the x-axis.

Low-end extensions: trial:i01.ug.Block7_union_row17.07 (p3187, low+56), trial:i01.ug.Block7_union_row3.15 (p3384, low+56), trial:i01.ug.Block7_union_row8.20 (p3430, low+56), trial:i01.ug.Block7_union_row13.03 (p3526, low+56), trial:i01.ug.Block7_union_row18.08 (p3096, low+92).

High-end extensions: trial:i01.ug.Block7_union_row12.02 (p3273, high+56), trial:i01.ug.Block7_union_row14.04 (p3200, high+72; p3215, high+56), trial:i01.ug.Block7_union_row5.17 (p3737, high+92; p3746, high+92), trial:i01.ug.Block7_union_row24.14 (p3058, high+136; p3635, high+120; p3564, high+128), trial:i02.ug.Block7_union_row20.04 (p3048, high+56), trial:i02.ug.Block7_union_row22.05 (p3527, high+92), trial:i02.ug.Block7_union_row9.06 (p3683, high+112).

A delta of 56 dbu is the most frequently observed resize_end magnitude, appearing in both low-end corrections (trial:i01.ug.Block7_union_row17.07, trial:i01.ug.Block7_union_row3.15, trial:i01.ug.Block7_union_row8.20, trial:i01.ug.Block7_union_row13.03) and high-end corrections (trial:i01.ug.Block7_union_row12.02, trial:i02.ug.Block7_union_row20.04). Larger extension magnitudes (92, 112, 120, 128, 136 dbu) correspond to trials with larger instance displacement magnitudes (trial:i01.ug.Block7_union_row7.19 with [108,0] and high+128; trial:i01.ug.Block7_union_row24.14 with [136,0] and high+136; trial:i02.ug.Block7_union_row9.06 with [56,0] and high+112).

**Uniform Polygon Shift: Use resize Instead of resize_end**

Use the `resize` operation (not `resize_end`) when the M1 polygon must translate uniformly along its length to match the instance displacement. trial:i01.ug.Block7_union_row15.05 applies resize +160 on p3586 alongside move_instance of i0913 by [136,0]. trial:i01.ug.Block7_union_row19.09 applies resize +40 on p3619 with move_instance of i0771 by [40,0]; resize -72 on p3654 with move_instance of i0026 by [-72,0]; and resize +72 on p3523 with move_instance of i0418 by [72,0]. trial:i02.ug.Block7_union_row15.03 applies resize +96 on p3592 (y-axis) alongside a move_instance of i1062 by [0,-84].

**Y-Axis Operations**

Y-axis corrections appear in five trials. Apply the polygon y-translation or resize_end at a magnitude that matches the instance y-displacement when both address the same M1 polygon:

- trial:i01.ug.Block7_union_row16.06: two instances moved [0,-12]; polygon p3516 translated y=-12. The polygon magnitude equals the instance magnitude.
- trial:i02.ug.leaf_0014.08: two instances moved [0,-12]; polygon p3515 translated y=-12. The polygon magnitude again equals the instance magnitude.
- trial:i01.ug.leaf_0095.26: two instances moved [0,+48]; p3537 extended resize_end high+48 (y); p2432 extended resize_end high+68 (y). The p3537 magnitude matches the instance magnitude; p2432 receives a larger extension.
- trial:i02.ug.Block7_union_row15.03: i1062 moved [0,-84]; p3592 resized +96 (y-axis). The polygon resize magnitude (96) exceeds the instance displacement (84) in absolute value, extending farther than the instance shift.
- trial:i02.ug.leaf_0017.09: single move_instance of i0949 by [0,+48] only; no polygon geometry operation.

Y-axis corrections also trigger M3 and V2 in touched_layers (trial:i01.ug.Block7_union_row16.06, trial:i01.ug.leaf_0095.26, trial:i02.ug.leaf_0014.08), unlike x-axis-only corrections which touch only M1, M2, V1.

**Multi-Instance Coordination**

When multiple instances within a locus share a common correction direction, accepted trials move them together in the same direction and by the same or closely matched magnitudes. trial:i01.ug.Block7_union_row11.01 moves both i1828 and i1728 by [36,0]. trial:i01.ug.Block7_union_row9.21 moves five instances (i1117, i1398, i1215, i1178, i1885) all by [40,0]. trial:i01.ug.Block7_union_row6.18 moves five instances (i1231, i1264, i1886, i1965, i1907) all by [36,0]. trial:i02.ug.Block7_union_row12.01 moves three instances (i1311, i1320, i1759) all by [36,0]. Move co-located instances together by the same delta when the correction applies uniformly across the group (trial:i01.ug.Block7_union_row9.21, trial:i01.ug.Block7_union_row6.18, trial:i02.ug.Block7_union_row12.01).

**Instance Displacement Magnitudes Observed**

Observed x-axis move_instance delta_dbu values: 3 (trial:i02.ug.leaf_0022.10), 4 (trial:i01.ug.Block7_union_row22.12), 12 (trial:i01.ug.Block7_union_row16.06, negative), 24 (trial:i01.ug.leaf_0024.25, negative), 28 (trial:i01.ug.Block7_union_row6.18), 36 (trial:i01.ug.Block7_union_row11.01 and many others), 40 (trial:i01.ug.Block7_union_row9.21, trial:i01.ug.Block7_union_row19.09), 52 (trial:i01.ug.Block7_union_row10.00), 56 (trial:i02.ug.Block7_union_row9.06), 64 (trial:i01.ug.Block7_union_row24.14), 68 (trial:i01.ug.Block7_union_row4.16), 72 (trial:i01.ug.Block7_union_row14.04, trial:i01.ug.Block7_union_row18.08), 108 (trial:i01.ug.leaf_0001.22, trial:i01.ug.Block7_union_row7.19), 136 (trial:i01.ug.Block7_union_row13.03, trial:i01.ug.Block7_union_row24.14). Negative x-displacements: -24 (trial:i01.ug.leaf_0024.25), -36 (trial:i01.ug.Block7_union_row16.06, trial:i01.ug.Block7_union_row14.04 i0519), -72 (trial:i01.ug.Block7_union_row19.09, trial:i02.ug.Block7_union_row13.02), -96 (trial:i02.ug.Block7_union_row15.03), -108 (trial:i01.ug.leaf_0024.25), -216 (trial:i01.ug.Block7_union_row10.00).

The value 36 dbu is the single most common x-displacement magnitude, present in more than half of all trials.

**op:add_polygon**

trial:i01.ug.Block7_union_row20.10 is the only trial using `add_polygon`. It adds a rectangle on M2 (points [[5992,22824],[5992,22896],[6048,22896],[6048,22824]], 56x72 dbu) paired with move_instance of i0753 by [-36,0]. The result is 0 new violations in crop and gated_in. No add_polygon operation targeting M1 directly appears in any trial.

**Iteration 2 Revisits**

Six units received repair operations in both iter 1 and iter 2, each time with a different operation set and different target instances and polygons:

- Block7_union_row12: trial:i01.ug.Block7_union_row12.02 (3 ops: move+resize_end+move); trial:i02.ug.Block7_union_row12.01 (3 ops: three move_instances).
- Block7_union_row13: trial:i01.ug.Block7_union_row13.03 (6 ops); trial:i02.ug.Block7_union_row13.02 (3 ops).
- Block7_union_row15: trial:i01.ug.Block7_union_row15.05 (8 ops); trial:i02.ug.Block7_union_row15.03 (3 ops, y-axis).
- Block7_union_row20: trial:i01.ug.Block7_union_row20.10 (2 ops, includes add_polygon on M2); trial:i02.ug.Block7_union_row20.04 (3 ops: two moves + resize_end high).
- Block7_union_row22: trial:i01.ug.Block7_union_row22.12 (1 op: move [4,0]); trial:i02.ug.Block7_union_row22.05 (6 ops: moves + resize_end high+92).
- Block7_union_row9: trial:i01.ug.Block7_union_row9.21 (5 ops: five move_instances [40,0]); trial:i02.ug.Block7_union_row9.06 (2 ops: move_instance [56,0] + resize_end high+112).

The iter 2 operations in every revisited unit target instances and polygons not touched in iter 1 of that same unit, confirming that each iteration addresses a distinct residual subset. Do not assume a single-pass repair fully resolves M1 violations in any unit that appears in iter 1; the iter 2 record for that unit addresses remaining violations left after the first pass (trial:i01.ug.Block7_union_row22.12 followed by trial:i02.ug.Block7_union_row22.05; trial:i01.ug.Block7_union_row9.21 followed by trial:i02.ug.Block7_union_row9.06).