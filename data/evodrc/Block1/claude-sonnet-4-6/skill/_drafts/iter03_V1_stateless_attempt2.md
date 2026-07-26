## Effective operation types

All accepted V1-touching repairs use `move_instance` (translating a VIA12 cell along x), `resize_end` (extending or retracting an M1 or M2 polygon endpoint along x), or combinations of both within a single repair unit. trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row5.05, trial:i01.ug.Block1_union_row6.06, and trial:i03.ug.leaf_0003.02 all mix the two forms and are accepted with conn_preserved=true.

## Minimum displacement discipline

Use the smallest displacement that clears the violation; do not round small required displacements up to larger grid increments when the circuit geometry permits the minimal move. trial:i03.ug.leaf_0003.02 records VIA12 instance moves of dx=+4 dbu (1 nm) each for i0485 and i0188, explicitly stated as clearing M1.S.2 violations ("gap to standard-cell M1 side at x=12144 becomes 100 dbu = 25 nm, clearing M1.S.2 v0011" and "clearing M1.S.2 v0012") without introducing new V1 violations. Those 4 dbu moves were accepted at gated_in.

## Connectivity is the primary acceptance gate

A repair is rejected when connectivity breaks, regardless of DRC improvement. trial:i01.ug.leaf_0034.12 was gated_out (conn_broken) despite touching V1 across a large locus with 10 operations. Every other V1-touching unit in this block was accepted at gated_in with conn_preserved=true (trial:i01.ug.Block1_union_row1.00 through trial:i03.ug.leaf_0003.02). Verify net continuity across all touched layers before committing any V1 repair.

## V1.M2.AUX.2: width-matching after M2 resize

V1 must be exactly the same width as M2 in the direction perpendicular to the M2 run (V1.M2.AUX.2). When an M2 polygon endpoint is retracted by `resize_end`, confirm that no V1 cut inside that segment has an edge beyond the new M2 boundary. trial:i03.ug.leaf_0003.02 records a resize_end of -8 dbu on p1543 and explicitly verifies that "all V2 cuts inside p1543 have rightmost edge at x=13860 < 13868," i.e., the cuts remain strictly inside the shrunk polygon. Apply the same edge-position check to every V1 cut whenever an adjacent M2 end is moved.

## V1.M2.EN.2 and V1.M1.EN.1: enclosure after instance translation

After any `move_instance` on a VIA12 cell, check that M2 encloses V1 by at least 5 nm on one opposing edge pair (V1.M2.EN.2) and that M1 encloses V1 by at least 5 nm on one axis and at least 2 nm on the other (V1.M1.EN.1). trial:i03.ug.leaf_0003.02 moves i0485 by dx=+4 dbu and records explicit overlap bookkeeping: "M2 overlap with p1309 (11808..12312) preserved: VIA12 M2 new left=12244-36=12208 < 12312." The same record verifies i0188 against p1270: "VIA12 M2 new left=2740-36=2704 < 2808." Both checks confirm enclosure is maintained on all sides after the shift; do not accept a move without completing both the M1 and M2 enclosure checks on all four edges.

## V1.AUX.1: V1 must remain inside the M1 and M2 intersection

V1 must lie inside the geometric intersection of M1 and M2 after any move or resize. trial:i03.ug.leaf_0003.02 records the M2 extents and M1 landing regions explicitly for each moved VIA12 before accepting the repair ("M2 bus p1217 spans (1728..14256) so overlap retained"; "VIA23 M3 land spans (2708,13984,3068,14096) and overlaps p1458 new extent (2716..3068) with zero gap at right edges"). Confirm that V1 remains fully inside both layers after every operation.

## V1.W.1: do not narrow V1 below 18 nm

V1 width along the M2 length direction must remain at least 18 nm. No direct resize of a V1 cut dimension appears in the accepted history; all width-changing `resize_end` operations target M1 or M2 polygon endpoints. When a `resize_end` retracts an M2 boundary toward a V1 edge, verify the remaining V1 dimension meets the 18 nm minimum. trial:i01.ug.Block1_union_row5.05 and trial:i01.ug.Block1_union_row6.06 each combine multiple `resize_end` ops on M2 polygons with `move_instance` ops and are accepted without V1.W.1 violations, confirming that coordinated M2 resizes can be safe when V1 geometry is checked.

## V1.S.1 spacing: mask shifts with instance translation

V1 spacing rules evaluate mask geometry derived from V1 instance shape and coincident M2 edges. Translating a VIA12 instance shifts its mask contribution by the same delta. The accepted iter-1 repairs consistently move V1-bearing instances in the positive-x direction (36, 72, 108, 136 dbu in trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row3.03, trial:i01.ug.Block1_union_row4.04, trial:i01.ug.Block1_union_row9.08), opening spacing to neighbors on the approached side while increasing it on the receding side. After any translation, recheck spacing to all V1 neighbors on both sides of the move direction.

## Large-locus units succeed when connectivity is preserved

V1-touching repair units that span a large locus are accepted when connectivity is preserved. trial:i01.ug.Block1_union_row5.05 (locus x-span ~11800 dbu, 7 ops) and trial:i01.ug.Block1_union_row8.07 (locus x-span ~8800 dbu, 7 ops) are both gated_in. The gated_out outcome in trial:i01.ug.leaf_0034.12 (locus spanning nearly the full block, 10 ops) arose from a connectivity break, not from locus size. Locus extent alone does not determine acceptance; connectivity check is decisive.

## M2 endpoint retraction paired with VIA23 relocation

When an M2-connected VIA (VIA23 carrying a V2 cut) must be moved to maintain M3-layer spacing, retract the adjacent M2 polygon endpoint by the same delta so that coincident edges remain coincident and V1.M2.AUX.2 width-match and V1.M2.EN.2 enclosure are preserved on the M2-to-V1 interface. trial:i03.ug.leaf_0003.02 pairs a -8 dbu resize_end on p1458 with a dx=-40 dbu move of VIA23 i0180 and records "VIA23 M3 land spans (2708,13984,3068,14096) and overlaps p1458 new extent (2716..3068) with zero gap at right edges," confirming that the M2 and via landing geometry remain flush after the combined operation.