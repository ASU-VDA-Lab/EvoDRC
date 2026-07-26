## Repair Pattern: Symmetric x-axis Resize with Centering Moves

The single recorded repair on cell VIA_VIA23_1_3_36_36 applied five V2 operations, all on the x-axis: shape 0 moved −144 dbu then resized +288 dbu; shape 1 resized +288 dbu without a move; shape 2 moved +144 dbu then resized +288 dbu (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). The outer shapes (0 and 2) moved symmetrically outward from center while all three shapes expanded by the same 288 dbu increment on x. The repair reduced violations by 15 in window unit:leaf_0018 (32→17) and by 12 in window unit:leaf_0019 (35→23), for a net reduction of 27; decision recorded "applied" and conn_preserved recorded true (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

## V2.W.1: Width Deficiency Corrected by x-axis Resize

V2.W.1 requires minimum V2 width of 18 nm along the M3 length direction. All five ops in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 acted exclusively on the x-axis, and each of the three V2 shapes received a +288 dbu resize on that axis. Apply x-axis resize—paired with a symmetric centering move for non-center shapes—to resolve V2.W.1 violations on this cell type (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

## Co-Modification of M2 and M3 Alongside V2 Operations

The touched_layers field in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 lists M2, M3, and V2, while the ops array contains only V2-layer entries. The repair system applied concurrent changes to M2 and M3 during the same transaction as the V2 x-axis resizes. Do not treat V2 width changes in isolation from M2 and M3: the accepted repair co-modified all three layers and preserved connectivity (conn_preserved: true, trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

## V2.M3.AUX.2: M3 Width Must Be Updated with V2

V2.M3.AUX.2 requires V2 to exactly match M3 width perpendicular to M3 length. M3 is listed in touched_layers alongside the x-axis V2 resizes, confirming that M3 width was adjusted in the same transaction (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). Resize M3 to match V2 when resizing V2 along the width axis; the applied repair demonstrates this co-update is required for the repair to be accepted (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

## V2.M2.EN.1 and V2.M3.EN.2: Enclosure Maintained via Co-modification

V2.M2.EN.1 requires M2 to enclose V2 by at least 5 nm on two opposite sides; V2.M3.EN.2 requires M3 to enclose V2 on two opposite sides by 5 & 5 nm or 5 & 0 nm. M2 is listed in touched_layers alongside the V2 x-axis expansion, confirming enclosure was maintained by co-expanding M2 (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). Expand the enclosing M2 and M3 shapes when expanding V2; the accepted repair demonstrates this co-modification is required to satisfy enclosure rules (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

## V2.AUX.1: Containment Preserved Through Co-modification

V2.AUX.1 requires V2 to be fully inside both M2 and M3. M2 and M3 are listed in touched_layers for the repair that expanded V2 along x, and the result was accepted with decision "applied" and conn_preserved true (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). Expand M2 and M3 to maintain containment when increasing V2 size; the applied repair confirms co-modification of the enclosing layers is the mechanism by which V2.AUX.1 compliance is sustained after a V2 resize (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

## V2.S.1 through V2.S.4: Spacing Headroom Must Be Confirmed Before x-axis Expansion

V2.S.1 governs spacing between V2 instances (18–27 nm depending on track alignment); V2.S.2, V2.S.3, and V2.S.4 govern corner-to-corner separations (23 nm, 30 nm, and 27 nm respectively) based on end-cap configuration. The x-axis expansion of three V2 shapes in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 moved outer via edges outward, and the repair was accepted at locus [1728, 2068, 11016, 10892] with a net reduction of 27 violations. Verify spacing clearance to neighboring V2 instances before applying x-axis resizes, since outward edge movement reduces the projection-measured and euclidean separations that V2.S.1 through V2.S.4 check (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

## NONORTHOGONAL Constraint: Use Only Axis-aligned Operations

The NONORTHOGONAL rule flags any non-90-degree edges on V2. All five operations in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 applied axis-aligned (x-axis) moves and resizes exclusively, and the repair was accepted without triggering NONORTHOGONAL violations. Apply only axis-aligned moves and resizes to V2 shapes to avoid NONORTHOGONAL errors (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).