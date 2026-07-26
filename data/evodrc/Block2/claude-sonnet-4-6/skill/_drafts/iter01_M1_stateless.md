Looking at the DRC rules and history, I'll now generate the knowledge section body.

## M1 Repair Strategies — Iteration 1 Observations

### Repair Axis and Direction

Every accepted M1 repair in this iteration applied displacement exclusively along the x-axis. All seven trials (trial:i01.ug.Block2_union_row1.00, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0001.03, trial:i01.ug.leaf_0004.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0011.06) used `delta_dbu` vectors of the form `[N, 0]`, with zero y-component. No accepted repair displaced any instance in the y direction. All polygon resize operations were likewise restricted to `axis="x"` (trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0001.03, trial:i01.ug.leaf_0011.06).

### Move-Only vs. Move + Resize Combinations

Three trials resolved M1 violations using move_instance operations alone, without any polygon resize: trial:i01.ug.Block2_union_row1.00 (2 instances moved +36 dbu x), trial:i01.ug.leaf_0004.04 (1 instance moved +36 dbu x), and trial:i01.ug.leaf_0007.05 (1 instance moved +36 dbu x). These were accepted with zero new violations introduced (n_new_in_crop=0, n_new_out_of_crop=0).

Four trials required a combination of move_instance and resize_end operations: trial:i01.ug.Block2_union_row3.01 added a single resize_end (axis=x, end=high, delta=36 dbu) alongside two instance moves; trial:i01.ug.Block2_union_row5.02 added two resize_end operations (both axis=x, end=high, delta=64 dbu) alongside two instance moves; trial:i01.ug.leaf_0001.03 added two resize_end operations with differing deltas (axis=x, end=high, delta=184 dbu; axis=x, end=low, delta=176 dbu) alongside one instance move; trial:i01.ug.leaf_0011.06 added one resize_end (axis=x, end=high, delta=36 dbu) alongside one instance move. All four were accepted with zero new violations.

Apply resize_end operations when a polygon endpoint requires independent adjustment beyond what instance movement alone provides, as demonstrated in trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0001.03, and trial:i01.ug.leaf_0011.06. Both the `end=high` (right/top x edge) and `end=low` (left/bottom x edge) directions produced accepted outcomes (trial:i01.ug.leaf_0001.03 used both simultaneously on different polygons).

### Effective Move Deltas

The most common accepted move delta was 36 dbu, used in trial:i01.ug.Block2_union_row1.00, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.leaf_0004.04, trial:i01.ug.leaf_0007.05, and trial:i01.ug.leaf_0011.06. A delta of 64 dbu was used for both instance moves and polygon resizes in trial:i01.ug.Block2_union_row5.02. The largest instance move delta (128 dbu) and the largest polygon resize deltas (184 dbu high end, 176 dbu low end) appeared in trial:i01.ug.leaf_0001.03, which was the only repair that also touched layer M4. All delta values produced accepted, connectivity-preserving outcomes.

Prefer the smallest delta that resolves the violation: 36 dbu satisfied repairs in five of seven trials (trial:i01.ug.Block2_union_row1.00, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.leaf_0004.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0011.06). Use larger deltas only when geometry context requires it, as in trial:i01.ug.Block2_union_row5.02 (64 dbu) and trial:i01.ug.leaf_0001.03 (up to 184 dbu).

### Connectivity Preservation

Every accepted repair preserved connectivity (conn_preserved=true in all seven trials). No accepted repair introduced any new violations inside or outside the crop window (n_new_in_crop=0, n_new_out_of_crop=0 in all seven trials). Repairs that touch M1 alongside V1 must preserve the V0.M1.EN.1 enclosure relationship (5 nm on two opposite sides, or 5 & 0 nm) and the V1.M1.EN.1 enclosure relationship (5 & 2 nm); all trials that moved instances touching V1 alongside M1 were accepted without introducing enclosure regressions (trial:i01.ug.Block2_union_row1.00, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0001.03, trial:i01.ug.leaf_0004.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0011.06).

### Co-Moved Layer Coupling

M1 was never repaired in isolation in this iteration. Every trial co-touched at least M2 and V1 alongside M1. trial:i01.ug.leaf_0001.03 additionally touched M4. When moving M1 instances, always verify that co-moved instances on M2 and V1 remain within their respective DRC constraints, as all accepted trials confirmed zero new violations across all touched layers.

### V0.M1.AUX.3 and Width Consistency

Rule V0.M1.AUX.3 requires V0 to be exactly the same width as M1 in the direction perpendicular to M1 length. Resize operations on M1 polygons must not alter the M1 dimension in the perpendicular direction to V0, or they risk introducing V0.M1.AUX.3 violations. All resize_end operations in this iteration targeted the x-axis only (trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0001.03, trial:i01.ug.leaf_0011.06), and all were accepted without V0.M1.AUX.3 regressions.

### Asymmetric Polygon End Adjustments

When a single M1 polygon repair requires extending both ends by different amounts, use separate resize_end operations with individually specified deltas for each end. trial:i01.ug.leaf_0001.03 demonstrated this with polygon p1065 (end=high, delta=184 dbu) and polygon p957 (end=low, delta=176 dbu) within the same repair operation, and both were accepted. The asymmetry in deltas (184 vs 176 dbu) indicates that the two ends faced different spacing or enclosure margins, and matching the resize to each end's individual geometric need is correct.

### Op Count and Repair Scope

Accepted repairs ranged from 1 op (trial:i01.ug.leaf_0004.04, trial:i01.ug.leaf_0007.05) to 5 ops (trial:i01.ug.Block2_union_row5.02). Higher op counts corresponded to wider crop loci with more affected instances and polygons, not necessarily harder violations. The decision gate accepted all repairs regardless of op count, confirming that multi-op bundles within a single unit are valid when all changes are coherent and connectivity is preserved (trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0001.03).