## Accepted Operation Patterns

All eight accepted trials in this iteration operate exclusively along the x-axis: every `move_instance` delta is of the form `[Δx, 0]` and every `resize_end` uses `axis: "x"`. No y-axis displacement or y-axis resize appears in any accepted record (trial:i01.ug.Block6_union_row3.00, trial:i01.ug.Block6_union_row5.01, trial:i01.ug.Block6_union_row7.02, trial:i01.ug.Block6_union_row8.03, trial:i01.ug.leaf_0001.04, trial:i01.ug.leaf_0011.05, trial:i01.ug.leaf_0015.06, trial:i01.ug.leaf_0018.07). Confine M1-touching moves and resizes to the x-axis when repairing DRC violations in this design state.

## Connectivity Preservation as a Gate

Every accepted trial carries `conn_preserved: true` and `reason: "conn_preserved"` (trial:i01.ug.Block6_union_row3.00 through trial:i01.ug.leaf_0018.07). Operations that break connectivity are rejected before DRC is evaluated; therefore, any candidate move or resize on M1 must be verified for connectivity preservation before committing.

## Zero Net-New Violations Across All Accepted Trials

All eight trials report `n_new_in_crop: 0` and `n_new_out_of_crop: 0`, confirming that the x-axis moves and resizes applied did not introduce new M1.W.1, M1.S.1, M1.S.2, M1.S.3, M1.A.1, V0.M1.EN.1, or V1.M1.EN.1 violations within or outside the repair crop (trial:i01.ug.Block6_union_row3.00, trial:i01.ug.Block6_union_row5.01, trial:i01.ug.Block6_union_row7.02, trial:i01.ug.Block6_union_row8.03, trial:i01.ug.leaf_0001.04, trial:i01.ug.leaf_0011.05, trial:i01.ug.leaf_0015.06, trial:i01.ug.leaf_0018.07). Prefer moves and resizes that keep the enclosing M1 polygon's edges clear of the minimum-enclosure distances required by V0.M1.EN.1 (5 nm on two opposite sides, or 5 nm and 0 nm) and V1.M1.EN.1 (5 nm and 2 nm on opposite sides).

## Move-Instance Magnitude Range

Accepted `move_instance` x-deltas span 28 dbu to 112 dbu in the positive direction, with one accepted negative delta of −36 dbu (trial:i01.ug.Block6_union_row7.02, instance i0074). The observed positive magnitudes are 28 dbu (trial:i01.ug.leaf_0015.06), 36 dbu (trial:i01.ug.Block6_union_row5.01, trial:i01.ug.Block6_union_row8.03, trial:i01.ug.leaf_0011.05, trial:i01.ug.leaf_0018.07), 72 dbu (trial:i01.ug.Block6_union_row3.00), 104 dbu (trial:i01.ug.Block6_union_row7.02, instance i0093), and 112 dbu (trial:i01.ug.leaf_0001.04). All of these remained free of new M1 spacing and width violations, indicating the surrounding M1 geometry had sufficient margin to absorb these displacements without violating M1.S.1 (18 nm side-to-side), M1.S.2 (25 nm tip-to-side), or M1.W.1 (18 nm width).

## Resize-End Magnitude Range and Direction

Accepted `resize_end` operations on x-axis `end: "high"` use deltas of 48 dbu (trial:i01.ug.leaf_0015.06, polygon p1923), 92 dbu (trial:i01.ug.Block6_union_row5.01, polygon p2072), 124 dbu (trial:i01.ug.Block6_union_row7.02, polygon p1903), and 132 dbu (trial:i01.ug.leaf_0001.04, polygon p2016). One `end: "low"` resize is accepted: +56 dbu on polygon p1920 (trial:i01.ug.Block6_union_row7.02). All resize operations extended polygon edges rather than contracting them and introduced no new M1.A.1 (minimum area 504 nm²), M1.S.1, M1.S.2, or M1.S.3 violations, confirming that the polygons were not pushed into neighboring geometry at these magnitudes.

## Combined Move-and-Resize Sequences

Three trials combine `move_instance` and `resize_end` on M1-touching polygons within the same operation set. In trial:i01.ug.Block6_union_row5.01 a 36 dbu instance move accompanies a 92 dbu high-end resize; in trial:i01.ug.Block6_union_row7.02 a +104 dbu move and +124 dbu high-end resize are paired with a −36 dbu move and +56 dbu low-end resize; in trial:i01.ug.leaf_0001.04 a +112 dbu move accompanies a +132 dbu high-end resize. All three produced zero new violations (n_new_in_crop: 0, n_new_out_of_crop: 0). When a move alone is insufficient to resolve enclosure or spacing, apply a coordinated resize on the same or adjacent polygon in the same operation bundle, as demonstrated by these accepted trials.

## V0.M1.EN.1 and V1.M1.EN.1 Enclosure Repair

M1 must enclose V0 by at least 5 nm on two opposite sides (or 5 nm and 0 nm per projection), and must enclose V1 by at least 5 nm and 2 nm on opposite sides. All accepted trials that touch M1 alongside V1 (all eight trials list V1 in `touched_layers`) did so without triggering V0.M1.EN.1 or V1.M1.EN.1 violations (trial:i01.ug.Block6_union_row3.00 through trial:i01.ug.leaf_0018.07). When moving an M1 polygon or instance that contains a via, move the enclosing M1 edge to maintain the required enclosure distance rather than moving the via separately; the accepted trials show that instance moves carry all contained geometry together, preserving enclosure without independent via adjustment.

## M1.AUX.3 Width Alignment

V0.M1.AUX.3 requires V0 to be exactly the same width as M1 along the direction perpendicular to M1 length. All accepted resize operations extend M1 along x only (trial:i01.ug.Block6_union_row5.01, trial:i01.ug.Block6_union_row7.02, trial:i01.ug.leaf_0001.04, trial:i01.ug.leaf_0015.06), which preserves the M1 edge profile perpendicular to the resize direction and avoids introducing V0.M1.AUX.3 violations. Do not resize M1 in a direction that changes its width at the via location without simultaneously adjusting the via or confirming the via edges already coincide with M1 edges.

## Unit-Gate Channel Scope

All eight trials operate through the `unit_gate` channel. The loci span multiple rows and leaf cells (Block6_union_row3, Block6_union_row5, Block6_union_row7, Block6_union_row8, leaf_0001, leaf_0011, leaf_0015, leaf_0018), confirming that x-axis moves and resizes at the magnitudes above are consistent across varied M1 geometries within Block6 at this design state (trial:i01.ug.Block6_union_row3.00 through trial:i01.ug.leaf_0018.07).