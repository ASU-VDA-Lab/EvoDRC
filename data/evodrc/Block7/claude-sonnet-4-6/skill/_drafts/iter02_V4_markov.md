## Winning repair pattern: paired V4 move-and-resize on x-axis plus M5 x-axis resize

Trial:i01.cu.def:VIA_VIA45_1_2_58_58.00 (decision: applied, tournament winner) executed five operations on cell VIA_VIA45_1_2_58_58: V4 shape_index 0 moved −116 dbu on x, then resized +232 dbu on x; V4 shape_index 1 moved +116 dbu on x, then resized +232 dbu on x; M5 shape_index 0 resized −152 dbu on x. This sequence reduced violations by 156 across windows leaf_0103 (−81) and leaf_0104 (−75) and was selected as the tournament winner over the competing single-operation trial.

The move magnitude for each V4 shape in trial:i01.cu.def:VIA_VIA45_1_2_58_58.00 is exactly half the resize magnitude (116 dbu move, 232 dbu resize). Apply this 1:2 ratio when constructing paired move-resize operations for V4 on the x-axis.

## Single-operation M5 resizes on x-axis or y-axis are inferior or harmful

Trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 used one operation—M5 shape_index 0 resized −88 dbu on the y-axis—and achieved delta_total of −156 with conn_preserved true, but lost the tournament against trial:i01.cu.def:VIA_VIA45_1_2_58_58.00. A y-axis-only M5 shrink is an inferior repair choice relative to the paired V4 move-resize plus M5 x-resize strategy; do not prefer it when both are available.

Trial:i02.cu.def:VIA_VIA45_1_2_58_58.00 used one operation—M5 shape_index 0 resized +56 dbu on the x-axis (expanding M5 on x) without any paired V4 operations—and produced delta_total of +75, worsening violations across leaf_0029 (+39) and leaf_0030 (+36). This trial was rejected as net_positive. A single M5 x-axis expansion with no paired V4 adjustment increases violations; never apply a positive M5 x-resize without simultaneously adjusting V4 to match, as required by V4.M5.AUX.2.

## Simultaneous V4 and M5 x-axis adjustment satisfies the width-match constraint

Rule V4.M5.AUX.2 requires V4 width to equal M5 width perpendicular to the M5 length direction. Trial:i01.cu.def:VIA_VIA45_1_2_58_58.00 expanded two V4 shapes on x (+232 dbu each) while shrinking M5 on x (−152 dbu), touching both layers together, and reduced violations by 156. Trial:i02.cu.def:VIA_VIA45_1_2_58_58.00 expanded M5 on x (+56 dbu) with no V4 adjustment and increased violations by 75. These two outcomes together confirm that modifying only one layer in isolation violates the width-match constraint and degrades results; adjust V4 and M5 x-dimensions together when V4.M5.AUX.2 is implicated.

## Connectivity is preserved by the paired move-resize approach

Both trial:i01.cu.def:VIA_VIA45_1_2_58_58.00 and trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 report conn_preserved: true, and trial:i02.cu.def:VIA_VIA45_1_2_58_58.00 also reports conn_preserved: true. Connectivity is preserved across all tested single and multi-operation patterns in this cell; however, trial:i02.cu.def:VIA_VIA45_1_2_58_58.00 demonstrates that connectivity preservation alone does not prevent a net-positive violation outcome. Use violation delta, not connectivity alone, as the acceptance criterion.

## Multi-layer scope: M4, M5, and V4 are always co-touched

All three recorded trials—trial:i01.cu.def:VIA_VIA45_1_2_58_58.00, trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, and trial:i02.cu.def:VIA_VIA45_1_2_58_58.00—list touched_layers as M4, M5, and V4, even when explicit ops name only M5. Rule V4.AUX.1 requires V4 to lie inside the intersection of M4 and M5; rule V4.M4.EN.1 requires M4 to enclose V4 by at least 11 nm on two opposite sides; rule V4.M5.EN.2 requires M5 to enclose V4 by at least 11 nm on two opposite sides. Any M5 or V4 dimensional change implicates M4 enclosure margins. Verify M4 enclosure headroom before expanding V4 or M5.

## Spacing rule minimums to respect during repair

Rules V4.S.1, V4.S.2, and V4.S.3 each enforce a 33 nm minimum spacing (projection metric for same-net and different-net cases; Euclidean corner-to-corner for V4.S.3). The x-axis V4 expansions in trial:i01.cu.def:VIA_VIA45_1_2_58_58.00 reduced total violations rather than increasing them, so the 232 dbu resize stayed within the available spacing budget at that locus. The +56 dbu M5 expansion in trial:i02.cu.def:VIA_VIA45_1_2_58_58.00 increased violations, which is consistent with spacing headroom being tighter in the windows affected (leaf_0029, leaf_0030). Do not apply a V4 or M5 x-axis resize larger than the available projection gap to the nearest neighbor, or V4.S.1/V4.S.2/V4.S.3 violations will be introduced.

## Minimum width floor for V4

Rule V4.W.1 sets the minimum V4 width at 24 nm. The resize operations in trial:i01.cu.def:VIA_VIA45_1_2_58_58.00 increased V4 width rather than reducing it, so no V4.W.1 risk arose. When any repair shrinks a V4 shape on either axis, verify the resulting dimension does not fall below 24 nm.