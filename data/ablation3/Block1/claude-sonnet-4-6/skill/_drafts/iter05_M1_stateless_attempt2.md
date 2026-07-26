**Observed operation types and outcomes**

Both recorded trials operated on the whole design locus [0, 0, 16032, 16032] via the `unit_gate` channel and were accepted with `conn_preserved` and zero new DRC violations introduced (n_new_in_crop = 0, n_new_out_of_crop = 0) in trial:i03.ug.whole_design.00 and trial:i05.ug.whole_design.00. M1 was a touched layer in both cases alongside M2 and V1.

**Instance moves on M1**

Trial:i03.ug.whole_design.00 applied 32 `move_instance` operations, all along the x-axis. The dominant delta was +64 dbu; two instances (i0455, i0079) were moved -64 dbu. No `resize_end` operations were used in that trial. The result was accepted with no new violations. When all moves are uniform multiples of the M1 grid pitch and connectivity is preserved, pure move-only repairs are sufficient to resolve spacing and enclosure violations without polygon resizing, as confirmed by trial:i03.ug.whole_design.00.

Trial:i05.ug.whole_design.00 used a mixed strategy: 17 `move_instance` operations with x-deltas of +48, +44, or +36 dbu, combined with 5 `resize_end` operations on M1 polygons (p1255, p1270, p1295, p1309, p1320), each extending the high x-end by 44 dbu. Three instances (i0433, i0082, i0258) were moved in the negative x direction (-72, -72, -64 dbu respectively). This mixed move-and-resize trial was also accepted with conn_preserved and zero new violations (trial:i05.ug.whole_design.00).

**resize_end on M1 polygons**

The only `resize_end` operations observed in this layer's history extend the high end of the x-axis by 44 dbu on specific M1 polygons. This operation type was applied exclusively at the same iteration as non-uniform instance moves (trial:i05.ug.whole_design.00). Do not apply `resize_end` to an M1 polygon unless the associated instance group requires a non-uniform x-delta that would otherwise leave the M1 tip underenclosing a via; in trial:i05.ug.whole_design.00, the five resized polygons all paired with instance moves of 44 dbu while adjacent instances moved 48 dbu, indicating the resize compensates for the 4 dbu shortfall at the M1 high edge to maintain V0 or V1 enclosure under rules V0.M1.EN.1 and V1.M1.EN.1.

**Via enclosure (V0.M1.EN.1 and V1.M1.EN.1)**

Rule V0.M1.EN.1 requires M1 to enclose V0 by at least 5 nm on two opposite sides (5 & 5 nm or 5 & 0 nm). Rule V1.M1.EN.1 requires M1 to enclose V1 by at least 5 nm on one side and 2 nm on the opposite side. Both trials touched V1 alongside M1, and both were accepted without new violations. When moving instances that carry M1 shapes enclosing vias, the move delta must be chosen so the post-move M1 geometry maintains the required enclosure margins. Trial:i05.ug.whole_design.00 shows that where a uniform instance move would underenclose a via, a `resize_end` on the M1 polygon at the high x-end by the difference (44 dbu in that case) restores compliant enclosure.

**M1 width and spacing**

Rule M1.W.1 sets the minimum M1 width at 18 nm. Rule M1.S.1 sets minimum side-to-side spacing at 18 nm when both edges are longer than 36 nm. Rules M1.S.2 through M1.S.6 set progressively tighter tip-to-side and tip-to-tip spacing requirements (25 nm, 27 nm, 31 nm) depending on edge length category, and M1.S.6 requires 20 nm corner-to-corner spacing. The accepted results in trial:i03.ug.whole_design.00 and trial:i05.ug.whole_design.00 confirm that the chosen move deltas (multiples of 64 dbu or combinations of 36/44/48 dbu) did not violate any spacing rule after adjustment. When selecting a move delta, verify that the resulting gap to adjacent M1 polygons does not fall below 18 nm (side-to-side) or the applicable tip spacing threshold; both trials demonstrate that grid-aligned moves in the range of 36-72 dbu achieve this on this design.

**M1 area rule**

Rule M1.A.1 requires a minimum M1 polygon area of 504 nm-sq. A `resize_end` that extends an M1 polygon at one end increases area and does not risk violating M1.A.1. Moves alone do not change polygon area. Neither trial introduced an M1.A.1 violation (trial:i03.ug.whole_design.00, trial:i05.ug.whole_design.00).

**V0.M1.AUX.3 width-match constraint**

Rule V0.M1.AUX.3 requires that the V0 width equals the M1 width in the direction perpendicular to M1 length. Moving M1 instances without resizing the M1 polygon preserves the relative V0-to-M1 width relationship. Applying `resize_end` only along the M1 length axis (x, high end) does not affect the perpendicular M1 width, so V0.M1.AUX.3 compliance is maintained under the operations used in trial:i05.ug.whole_design.00.

**M1.R.0 redundant island avoidance**

Rule M1.R.0 flags M1 polygons that enclose exactly one small V0 via and sit within 400 nm of a large empty M1 region. Neither trial produced an M1.R.0 violation. Moving M1 islands together with their contained via instances, as done uniformly in trial:i03.ug.whole_design.00, avoids creating new isolation conditions that would trigger M1.R.0.

**Nonorthogonal geometry**

All move and resize_end operations in both trials are axis-aligned (x-axis only). No diagonal edges are introduced. This satisfies the GEOMETRY.NONORTHOGONAL rule that applies to M1, as confirmed by the accepted outcomes in trial:i03.ug.whole_design.00 and trial:i05.ug.whole_design.00. Do not use move or resize deltas with nonzero y-components simultaneously with nonzero x-components in a single operation, as this would produce diagonal edges on M1 polygons.

**Connectivity preservation**

Both trials were gated in on the basis of `conn_preserved`. The `unit_gate` channel enforces connectivity before committing any repair. When a proposed set of M1 moves would break a net connection, the gate rejects the trial. The history shows that coordinating moves of all instances in a net (including those that must move in the negative direction, as i0455 and i0079 in trial:i03.ug.whole_design.00, and i0433, i0082, i0258 in trial:i05.ug.whole_design.00) is necessary for conn_preserved acceptance; moving only a subset of a net's instances risks disconnecting M1 to V0/V1 paths.