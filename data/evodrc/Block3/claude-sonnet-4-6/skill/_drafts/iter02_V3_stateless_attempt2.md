**Multi-layer operation bundles**

Both accepted repairs applied operations across M3, M4, M5, V3, and V4 simultaneously within a single bundle (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03). Move V3 instances together with their enclosing M3, M4, and adjacent via/metal layers in the same bundle; no accepted repair in the recorded history applies V3 moves in isolation (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03).

**Polygon moves and instance moves must share a bundle**

trial:i02.ug.leaf_0004.03 included a direct polygon move on p1059 (+32 dbu along x) alongside eight instance moves in a single 13-op bundle, and was accepted (decision: gated_in, conn_preserved: true). Apply X-axis polygon shifts in the same operation bundle as the accompanying instance moves (trial:i02.ug.leaf_0004.03); no accepted trial separates polygon coordinate edits from their paired instance moves.

**Y-axis movements in multiples of 48 dbu**

trial:i02.ug.leaf_0003.02 moved six instances in Y by values that are exact multiples of 48 dbu (deltas: -48, -48, +96, +96, +48, +48 dbu), producing zero new violations inside or outside the crop window (n_new_in_crop: 0, n_new_out_of_crop: 0, decision: gated_in). The symmetric pairing of instance moves in that repair maintained V3.M3.EN.1 enclosure (minimum 5 nm on two opposite sides) and V3.M4.EN.2 enclosure (minimum 11 nm on two opposite sides) by moving the full enclosing metal stack together.

**Mixed axis movements and polygon resizes in a single bundle**

trial:i02.ug.leaf_0004.03 combined four operation categories in one 13-op bundle: Y-only instance moves (i0151 [0,+72], i0192 [0,+24], i0096 [0,-24], i0088 [0,-72]), XY instance moves (i0173 [+32,+72], i0147 [+32,+24], i0083 [+32,-24], i0085 [+32,-72]), an X-axis polygon move on p1059 (+32 dbu), and resize_end operations extending or contracting the y-ends of four M3 polygons (p1104 high end +72, p1103 high end +24, p1102 low end +24, p1101 low end +72). The resize_end operations on the M3 polygons preserve the enclosure margin required by V3.M3.EN.1 as instances shift. Submit all four operation categories together; trial:i02.ug.leaf_0004.03 confirms this mixed bundle is accepted.

**Connectivity gating overrides new in-crop violation counts**

Both recorded repairs were accepted on the basis of conn_preserved: true (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03). trial:i02.ug.leaf_0003.02 introduced no new violations (n_new_in_crop: 0, n_new_out_of_crop: 0). trial:i02.ug.leaf_0004.03 introduced 2 new in-crop violations and zero new out-of-crop violations but was still accepted (decision: gated_in) because connectivity was preserved. Preserve connectivity when building repair bundles; the gating criterion accepts new in-crop violations when conn_preserved is true (trial:i02.ug.leaf_0004.03).