**Coupled-layer operations**

All eight accepted trials touch M1, M2, and V1 together as a unit — no trial moves V1 geometry in isolation (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.Block5_union_row6.01, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05, trial:i02.ug.Block5_union_row6.00, trial:i02.ug.leaf_0002.02). Move V1 only as part of a coupled M1+M2+V1 instance move to preserve the stack intersection that V1.AUX.1 requires.

**Move direction**

All accepted move_instance operations displace instances along the x-axis only (trial:i01.ug.Block5_union_row3.00 through trial:i02.ug.leaf_0002.02). No accepted trial includes a y-axis displacement.

**Move magnitudes and iteration**

Accepted x-axis displacements are +4, +36, +72, and +104 dbu in the positive direction and −36 dbu in the negative direction. The same unit Block5_union_row6 used a +4 dbu move in iteration 1 (trial:i01.ug.Block5_union_row6.01) and required +104 dbu plus an M2 resize in iteration 2 (trial:i02.ug.Block5_union_row6.00), because the design state changed between iterations and the V1.S.1 / V1.S.2 / V1.S.3 / V1.S.4 spacing violations at that locus required greater separation. Apply larger displacements in later iterations when the same locus returns with a changed design state (trial:i02.ug.Block5_union_row6.00 vs. trial:i01.ug.Block5_union_row6.01).

**Opposing-direction moves**

When two V1 clusters are too close to satisfy inter-via spacing rules, moving them in opposite directions along x separates them without displacing the combined centroid. In trial:i01.ug.leaf_0002.03, instances i0056 (+36 dbu) and i0103 (−36 dbu) were moved symmetrically apart, resolving V1.S.1 through V1.S.4 spacing violations. Use opposing moves when both clusters have room to shift within their respective M1 and M2 enclosures, as confirmed by conn_preserved=true in trial:i01.ug.leaf_0002.03.

**M2 resize_end on the x high end**

Three accepted trials combine instance moves with a resize_end on the x high end of an M2 polygon: trial:i01.ug.Block5_union_row3.00 (polygon p967, +36 dbu), trial:i01.ug.leaf_0001.02 (polygon p974, +72 dbu), and trial:i02.ug.Block5_union_row6.00 (polygon p955, +20 dbu). All resize deltas are positive extensions; no accepted trial shrinks an M2 polygon (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.leaf_0001.02, trial:i02.ug.Block5_union_row6.00). Extend the M2 high-x end when shifting V1 toward the high-x side would otherwise leave the trailing M2 edge short of the V1.M2.EN.2 or V1.M2.AUX.2 requirement. Avoid negative resize_end deltas; none appear in any accepted trial (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.leaf_0001.02, trial:i02.ug.Block5_union_row6.00).

**Connectivity preservation**

All eight trials report conn_preserved=true with n_new_in_crop=0 and n_new_out_of_crop=0 (trial:i01.ug.Block5_union_row3.00 through trial:i02.ug.leaf_0002.02). Move M1, M2, and V1 as a fully coupled set to maintain the M1∩M2 intersection that V1.AUX.1 requires and to avoid creating new out-of-crop violations.

**Rule-specific notes**

V1.W.1 (minimum width 18 nm along M2 length): All resize operations in accepted trials are extensions with positive delta_dbu (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.leaf_0001.02, trial:i02.ug.Block5_union_row6.00). Avoid any resize that narrows V1 or M2 width, since no contraction appears in any accepted trial.

V1.S.1 / V1.S.2 / V1.S.3 / V1.S.4 (spacing between V1 instances across mask categories): x-axis instance moves are the primary mechanism for increasing inter-via separation (trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05, trial:i01.ug.Block5_union_row6.01). The spacing rules operate on expanded V1 masks that include M2 end-cap extensions, so even a small move can bring masks into compliance when the violation margin is small — a +4 dbu move resolved the iteration-1 Block5_union_row6 violations (trial:i01.ug.Block5_union_row6.01).

V1.M1.EN.1 (M1 enclosure of V1: 5 & 2 nm on opposite sides): Instance moves carry M1 and V1 together, preserving enclosure geometry (trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05). No accepted trial required an independent M1 resize to repair enclosure.

V1.M2.EN.2 (M2 enclosure of V1: 5 & 5 nm or 5 & 0 nm on opposite sides) and V1.M2.AUX.2 (V1 width must equal M2 width perpendicular to M2 length): The resize_end operations extending M2 at the x high end restore M2 coverage after V1 is shifted toward the high-x edge (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.leaf_0001.02, trial:i02.ug.Block5_union_row6.00). Apply a resize_end to the M2 polygon at the trailing edge whenever an x-high instance move would leave insufficient enclosure on that side, as all three resize-bearing accepted trials demonstrate.