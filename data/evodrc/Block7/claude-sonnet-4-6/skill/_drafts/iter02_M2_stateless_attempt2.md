**Repair operations observed on M2**

All 37 trials in the measured history received `gated_in` decisions with `conn_preserved:true`. The following operation types appear on M2.

**move_instance**

`move_instance` is applied in every trial. The primary direction is the x-axis. Signed delta magnitudes span −108 to +136 dbu in iter 1 and −96 to +72 dbu in iter 2 (trial:i01.ug.Block7_union_row10.00, trial:i01.ug.Block7_union_row24.14, trial:i02.ug.Block7_union_row15.03, trial:i02.ug.Block7_union_row13.02). Multiple instances are moved together within a single trial rather than adjusting a single element in isolation: trial:i01.ug.Block7_union_row14.04 moves eleven instances, and trial:i01.ug.Block7_union_row18.08 moves six instances alongside two polygon operations.

y-axis instance moves occur only in trials whose `touched_layers` includes M3 and V2: trial:i01.ug.Block7_union_row16.06 ([0,−12] dbu, touching M1/M2/M3/V1/V2), trial:i02.ug.leaf_0001.07 ([0,−57] dbu, touching M2/M3/V2), trial:i02.ug.leaf_0014.08 ([0,−12] dbu, touching M1/M2/M3/V1/V2), and trial:i01.ug.leaf_0095.26 ([0,+48] dbu, touching M1/M2/M3/V1/V2). No y-axis instance move appears in any trial whose `touched_layers` is limited to M1/M2/V1.

**resize_end**

`resize_end` modifies one tip end of an M2 polygon edge along a single axis. Every recorded `resize_end` operation acts along the x-axis; none acts along y in any trial (trial:i01.ug.Block7_union_row10.00, trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row13.03, trial:i01.ug.Block7_union_row14.04, trial:i01.ug.Block7_union_row15.05, trial:i01.ug.Block7_union_row17.07, trial:i01.ug.Block7_union_row18.08, trial:i01.ug.Block7_union_row19.09, trial:i01.ug.Block7_union_row3.15, trial:i01.ug.Block7_union_row5.17, trial:i01.ug.Block7_union_row7.19, trial:i01.ug.Block7_union_row8.20, trial:i02.ug.Block7_union_row9.06, trial:i02.ug.Block7_union_row20.04, trial:i02.ug.Block7_union_row22.05). The `end` field is "high" or "low", selecting which tip of the polygon is adjusted.

In trial:i01.ug.Block7_union_row8.20, `resize_end` on the "low" end (+56 dbu) co-occurred with a move_instance in the opposite direction (−36 dbu), preserving overall M2 footprint while shifting the violation-side tip outward. In trial:i01.ug.Block7_union_row17.07, `resize_end` on the "low" end (+56 dbu) co-occurred with instance moves in the +x direction, showing that tip extension and instance translation compose within the same repair step. The end chosen ("high" or "low") must correspond to the tip edge that needs extension away from the adjacent polygon causing the spacing violation (trial:i01.ug.Block7_union_row3.15, trial:i01.ug.Block7_union_row8.20).

**resize (both ends, symmetric)**

`resize` expands both ends of an M2 polygon by the same amount along a specified axis. It appears in two trials: trial:i01.ug.Block7_union_row15.05 (axis x, +160 dbu on p3586) and trial:i02.ug.Block7_union_row15.03 (axis y, +96 dbu on p3592). Apply `resize` when both ends of a segment must expand equally rather than a single tip requiring adjustment (trial:i01.ug.Block7_union_row15.05, trial:i02.ug.Block7_union_row15.03).

The y-axis `resize` in trial:i02.ug.Block7_union_row15.03 co-occurred with an instance move of [0,−84] dbu and touched only M1/M2/V1. This is the only y-axis M2 polygon expansion observed in a trial whose `touched_layers` does not include M3 or V2.

**add_polygon**

A single `add_polygon` on M2 appears in trial:i01.ug.Block7_union_row20.10, inserting a rectangle at [[5992,22824],[5992,22896],[6048,22896],[6048,22824]] with a 56 × 72 dbu bounding box (area = 4032 nm²). This is well above the M2.A.1 minimum of 504 nm². The same trial also moved one instance by [−36,0] dbu. Do not add M2 polygons with area < 504 nm², which triggers M2.A.1; trial:i01.ug.Block7_union_row20.10 shows the minimum practical polygon geometry used in this design.

**Polygon move (op: move)**

Two trials include a `move` operation that translates an entire M2 polygon without resizing. In trial:i02.ug.leaf_0001.07, polygon p3383 moves [0,−57] dbu (y-axis, touching M2/M3/V2); the polygon y-delta matches the instance y-delta on i1643 exactly (−57 dbu), preserving the relative position of the M2 polygon over its via context. In trial:i01.ug.Block7_union_row16.06, polygon p3516 moves [0,−12] dbu (y-axis, touching M1/M2/M3/V1/V2), matching the −12 dbu instance moves in the same trial. When using polygon `move` in a y-direction, match the polygon delta to the associated instance delta to maintain via alignment (trial:i02.ug.leaf_0001.07, trial:i01.ug.Block7_union_row16.06).

**Spacing rules and observed repair magnitudes**

M2.W.1 sets the minimum M2 width at 18 nm. All `resize` and `resize_end` deltas in the history are positive (extending, not narrowing), consistent with repairs that open spacing rather than compress width (trial:i01.ug.Block7_union_row10.00 through trial:i02.ug.Block7_union_row22.05).

M2.S.1 requires ≥ 18 nm side-to-side spacing between edges longer than 36 nm. M2.S.2 requires ≥ 25 nm tip-to-side spacing when the tip edge is ≤ 36 nm and the opposing side edge is > 36 nm. M2.S.3 requires ≥ 27 nm tip-to-tip spacing when both tips are 24–36 nm. M2.S.4 requires ≥ 31 nm tip-to-tip spacing when both tips are < 24 nm. M2.S.5 requires ≥ 31 nm between a mixed narrow/wide tip pair (one < 24 nm, one 24–36 nm). M2.S.6 requires ≥ 20 nm euclidean corner-to-corner spacing for polygon pairs not already caught by projection-based rules.

Move magnitudes of 36–72 dbu appear across the majority of trials and provide clearance that satisfies M2.S.1 and M2.S.6 simultaneously when adjacent M2 polygons are on neighboring tracks (trial:i01.ug.Block7_union_row11.01, trial:i01.ug.Block7_union_row6.18, trial:i01.ug.Block7_union_row9.21, trial:i02.ug.Block7_union_row12.01). The larger resize_end correction of +308 dbu on p3286 in trial:i01.ug.Block7_union_row10.00 demonstrates that substantially larger adjustments are applied when the violating geometry requires repositioning across a wider span.

M2.S.7 forbids 18 nm tip-to-tip gaps that are co-located with side-to-side spacing ≤ 32 nm; parallel run length must be ≥ 35 nm when side spacing ≤ 32 nm. The symmetric push/pull pattern in trial:i01.ug.Block7_union_row19.09 — two instances and one polygon moved by +72 dbu while another instance and polygon moved by −72 dbu — opens spacing on both sides simultaneously and avoids introducing new violations on the opposite side that would re-trigger M2.S.7.

M2.S.8 requires ≥ 80 nm euclidean center-to-center spacing between tip-to-tip gaps on different M2 tracks (gaps found by shrinking each 18 nm tip-to-tip region by 8.5 nm per side). Repositioning by large x-deltas (e.g., the +308 dbu in trial:i01.ug.Block7_union_row10.00) is consistent with clearing the 80 nm diagonal distance required by M2.S.8 in addition to in-track spacing rules.

**Via enclosure constraints**

V1.M2.EN.2 requires M2 to enclose V1 by ≥ 5 nm on two opposite sides; the 5 & 0 nm variant is also compliant. V1.M2.AUX.2 requires V1 to exactly match the M2 width in the direction perpendicular to M2 length. V2.M2.EN.1 requires M2 to enclose V2 by ≥ 5 nm on at least two opposite sides.

All trials that touch V1 achieved `conn_preserved:true`, confirming that the combined move_instance and polygon operations maintained valid via enclosure throughout. In trial:i02.ug.leaf_0001.07 (touching M2/M3/V2), the y-polygon move on p3383 (−57 dbu) exactly matched the instance move on i1643 (−57 dbu), keeping the M2 polygon centered over the via and preserving V2.M2.EN.1 enclosure. In trial:i01.ug.leaf_0095.26 (touching M1/M2/M3/V1/V2), y-direction resize_end operations extended p2432 by +68 dbu ("high" end) and p3537 by +48 dbu ("high" end) while instance moves shifted the associated instances by +48 dbu, extending M2 coverage in the y-direction without reducing enclosure on the opposite side. Move the polygon and the associated instance by matching y-deltas when the repair goal is to reposition the M2/via stack without changing enclosure geometry (trial:i02.ug.leaf_0001.07, trial:i02.ug.leaf_0014.08).

**Geometry constraint**

All M2 geometry must be orthogonal (GEOMETRY.NONORTHOGONAL rule). Every operation in the measured history acts along the x or y axis only; no non-90° edges are introduced in any trial (trial:i01.ug.Block7_union_row10.00 through trial:i02.ug.leaf_0022.10). The add_polygon in trial:i01.ug.Block7_union_row20.10 uses a rectangle defined by axis-aligned corner coordinates, consistent with this constraint.