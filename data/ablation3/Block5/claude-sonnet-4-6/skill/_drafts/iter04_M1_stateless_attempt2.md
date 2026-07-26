**Rule summary**

V0.M1.EN.1 requires M1 to enclose V0 by at least 5 nm on two opposite sides; the deck's projection check also accepts a 5 nm / 0 nm pattern where one axis has full enclosure and the opposite axis is flush. V0.M1.AUX.3 requires every V0 edge to be coincident with an M1 edge in the direction perpendicular to M1 length; any V0 edge not sharing that coincidence triggers the rule. M1.W.1 enforces a minimum M1 width of 18 nm. M1.S.1 enforces 18 nm side-to-side spacing when both interacting edges exceed 36 nm. M1.S.2 enforces 25 nm tip-to-side spacing when one edge is ≤ 36 nm and the other exceeds 36 nm. M1.S.3 enforces 27 nm tip-to-tip spacing when both edges are between 24 nm and 36 nm. M1.S.4 enforces 31 nm tip-to-tip spacing when both edges are < 24 nm. M1.S.5 enforces 31 nm tip-to-tip spacing when one edge is in the 24–36 nm range and the other is < 24 nm. M1.S.6 enforces a 20 nm corner-to-corner spacing between M1 polygons. M1.A.1 requires each M1 polygon area to be at least 504 nm². M1.R.0 flags M1 islands enclosing exactly one small V0 when those islands fall within 400 nm of a large empty M1 region (≥ 500 nm wide, area > 2.5 µm²). V1.M1.EN.1 requires M1 to enclose V1 by at least 5 nm on one axis and at least 2 nm on the other. All M1 edges must be orthogonal; any edge at a non-zero, non-right angle triggers GEOMETRY.NONORTHOGONAL.

**Observed repair operations and outcomes**

All three completed trials that touched M1 were accepted with decision gated_in and conn_preserved=true, with zero net new violations introduced in crop: trial:i01.ug.whole_design.00, trial:i02.ug.whole_design.00, trial:i04.ug.whole_design.00.

Instance moves (move_instance) are the primary repair primitive used on M1 across the history. Every accepted trial that touched M1 included at least one move_instance operation: trial:i01.ug.whole_design.00 (19 ops, including instance moves on i0012, i0103, i0061, i0104 among others), trial:i02.ug.whole_design.00 (7 ops, all move_instance on i0011, i0017, i0019, i0025, i0056, i0111, i0131), and trial:i04.ug.whole_design.00 (6 ops, all move_instance on i0012, i0117, i0131, i0017, i0019, i0011). All three were accepted.

In addition to instance moves, trial:i01.ug.whole_design.00 applied resize_end operations on M1 polygons p879 and p910 along the y-axis (high end) and a move operation on p910 along the x-axis; the trial was accepted with no new violations introduced in crop. These polygon-level operations, combined with instance moves, resolved violations without breaking connectivity.

**Connectivity constraint**

Every accepted M1 repair preserved connectivity. trial:i01.ug.whole_design.00, trial:i02.ug.whole_design.00, and trial:i04.ug.whole_design.00 all record conn_preserved=true. Repairs to M1 must not break net connections; the gating mechanism accepted only trials where this condition held.

**Assemble drops**

trial:i04.ug.whole_design.00 recorded assemble_drops exclusively for M3 and V2 operations (resize_via_shape and resize ops in group v2m3aux2_fix); the M1 operations in that trial — all instance moves — required no drops and reached an accepted state without modification.