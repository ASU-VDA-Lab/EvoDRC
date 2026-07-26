## M6 Repair Observations — Iteration 3

**V5 shape adjustments reduce M6-adjacent violations; M6 vertical resize in the same context increases them.**

In the VIA_VIA56_2_2_66_58 cell, reshaping V5 shapes along the y-axis (four move+resize pairs, each delta_dbu=-132 move and +512 resize or +132 move and +512 resize) produced delta_total=-80 and was accepted (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02). The subsequent attempt on the same cell that applied a +128 dbu y-axis resize to M6 alongside a -96 dbu x-axis resize to M5 produced delta_total=+234 and was rejected as net positive (trial:i02.cu.def:VIA_VIA56_2_2_66_58.01). Do not apply positive y-axis resizes to M6 in VIA_VIA56_2_2_66_58 configurations when V5 reshaping has already been the accepted repair path; trial:i02.cu.def:VIA_VIA56_2_2_66_58.01 confirms this combination worsens the violation count.

**Instance and polygon moves touching M6 can be gated in when connectivity is preserved.**

A unit-gate pass in leaf_0013 moved nine instances (delta_dbu values of [32,32], [-16,32], [-64,32], [32,-16], [-16,-16], [-64,-16], [32,64], [-16,64], [-64,64]) and three polygons (p2213 x+32, p2212 x-16, p2211 x-64, p3803 y+32, p3802 y-16, p3801 y+64) across layers including M6, with n_new_in_crop=217, n_new_out_of_crop=0, and conn_preserved=true, resulting in decision gated_in (trial:i03.ug.leaf_0013.09). Polygon moves on M6 in multiples of 16 dbu and 32 dbu are viable when the unit-gate connectivity check passes.

**M6 horizontal edge grid requirement (M6.AUX.1) interacts with all y-axis adjustments.**

M6.AUX.1 requires all horizontal edges to lie on a 32 nm grid. The accepted polygon moves in trial:i03.ug.leaf_0013.09 used y-axis deltas of +32, -16, and +64 dbu; the -16 dbu move lands on a 16 dbu boundary, which would violate M6.AUX.1 if applied to a polygon whose horizontal edges were previously on-grid at 32 nm offsets. Verify grid alignment of any M6 polygon after applying y-axis moves that are not multiples of 32 dbu.

**M6 vertical width constraints (M6.W.1 through M6.W.4) bound the safe range of y-axis resizes.**

M6.W.1 requires vertical width >= 32 nm. M6.W.2 requires vertical width <= 640 nm. M6.W.3 prohibits vertical widths that are even integer multiples of 32 nm (64, 128, 192, 256, 320, 384, 448, 512, 576, 640 nm). M6.W.4 further prohibits widths of 96, 224, 352, 480, and 608 nm. The rejected y-axis resize of +128 dbu applied to M6 in trial:i02.cu.def:VIA_VIA56_2_2_66_58.01 must be evaluated against these constraints for the resulting polygon width; the trial was rejected on net delta grounds before width legality could be the primary driver, but any repair that grows M6 vertically must avoid landing on the W.3 and W.4 forbidden widths.

**V5.M6.EN.2 and V5.M6.AUX.2 impose enclosure and width-match requirements that constrain M6 resizing around V5.**

V5.M6.EN.2 requires M6 to enclose V5 by at least 11 nm on two opposite sides. V5.M6.AUX.2 requires that V5 width along the perpendicular direction exactly match the M6 width. The V5 reshape accepted in trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 operated on four V5 shapes with +512 dbu y-axis resizes; because V5.M6.AUX.2 ties V5 width to M6 width, resizing V5 without matching M6 width could introduce AUX.2 violations. The accepted trial preserved conn_preserved=true and achieved delta_total=-80 by resizing V5 alone, implying M6 width was already compatible with the resized V5 shapes in that configuration.

**M6.AUX.3 prohibits bends; all repair moves must keep M6 polygons rectilinear.**

M6.AUX.3 flags any M6 corner with an interior angle between 0 and 90 degrees. Polygon moves in trial:i03.ug.leaf_0013.09 were pure translations (no reshape), preserving polygon topology and therefore not introducing bends. Any resize operation that creates a non-rectilinear M6 shape will trigger M6.AUX.3.

**M6.AUX.2 track-centering rule applies only to minimum-width M6 segments.**

M6.AUX.2 requires minimum-width (approximately 32 nm vertical) M6 tracks to have their centerlines at positions satisfying (cl - 64) mod 256 == 0 in dbu. Wide segments (those surviving m6.sized(0,-17.nm).sized(0,17.nm)) are exempt from M6.AUX.2 but subject to M6.AUX.4, which prohibits their horizontal edges from coinciding with routing track edges of nearby minimum-width segments. No trial in this history directly tested M6.AUX.2 or M6.AUX.4 violations in isolation; the polygon y-moves in trial:i03.ug.leaf_0013.09 included a -16 dbu delta that could shift a minimum-width track centerline off the required grid.