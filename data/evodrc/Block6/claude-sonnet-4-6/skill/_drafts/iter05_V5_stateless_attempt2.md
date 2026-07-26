## Cell VIA_VIA56_2_2_66_58: The Only Directly Repaired Via Cell

Both cu_pool repairs in the measured history target `VIA_VIA56_2_2_66_58`. In trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 and trial:i04.cu.def:VIA_VIA56_2_2_66_58.00, all V5 shape-level operations (move_via_shape and resize_via_shape) are confined to this single cell definition. No other via cell received direct V5 shape edits.

## X-Axis Pair-Move With Uniform Resize (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02)

In trial:i01.cu.def:VIA_VIA56_2_2_66_58.02, shape_index 0 and 2 move −116 dbu in x and shape_index 1 and 3 move +116 dbu in x; all four shapes are then resized +320 dbu in x. Decision is "applied", total violation delta is −16 (leaf_0019: −8, leaf_0020: −8), conn_preserved. Shape pairs 0/2 and 1/3 move in opposite x-directions while all four shapes grow in x by the same magnitude.

## Y-Axis Pair-Move With Large Resize (trial:i04.cu.def:VIA_VIA56_2_2_66_58.00)

In trial:i04.cu.def:VIA_VIA56_2_2_66_58.00, shape_index 0 and 1 move −132 dbu in y and shape_index 2 and 3 move +132 dbu in y; all four shapes are resized +512 dbu in y. M5/M6 context polygons p2109 and p2108 move −64 dbu and −112 dbu in y in the same group. Decision is "applied", total violation delta is −14 (leaf_0002: −14, leaf_0003: 0), conn_preserved. The +512 dbu y-resize is the largest single resize magnitude in the measured history; it exceeds the +320 dbu x-resize of trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 by 192 dbu.

## V5 Shapes Always Moved and Resized Together in One Group

In trial:i01.cu.def:VIA_VIA56_2_2_66_58.02, all four V5 shapes receive both a move_via_shape and a resize_via_shape in the same operation group. In trial:i04.cu.def:VIA_VIA56_2_2_66_58.00, all four V5 shapes again receive both a move and a resize alongside M5/M6 polygon moves in the same group. No measured repair applies a resize_via_shape to V5 without an accompanying move_via_shape, or a move without an accompanying resize.

## M5 and M6 Must Be Included in Every V5 Operation Group

V5.AUX.1 requires V5 to remain inside M5 and M6. Every trial that operates on V5 shapes also modifies M5 and M6 in the same operation group: trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 lists touched_layers M5, M6, V5; trial:i04.cu.def:VIA_VIA56_2_2_66_58.00 lists M4, M5, M6, V4, V5; trial:i03.ug.leaf_0003.02 lists M4, M5, M6, V4, V5; trial:i05.ug.leaf_0002.01 lists M1, M2, M5, M6, V1, V5. No repair in the measured record alters V5 geometry without co-moving M5 and M6 in the same group.

## V5.M6.AUX.2: V5 Must Be Resized to Match M6 Width After M6 Geometry Changes

V5.M6.AUX.2 requires V5 to exactly match M6's width along the direction perpendicular to M6's length. In trial:i04.cu.def:VIA_VIA56_2_2_66_58.00, M5/M6 context polygons move in y (−64 and −112 dbu) while V5 shapes are simultaneously resized +512 dbu in y in the same group. In trial:i01.cu.def:VIA_VIA56_2_2_66_58.02, M5 and M6 are in touched_layers while V5 shapes are resized +320 dbu in x. Both trials record decision "applied" with net violation reductions and conn_preserved, showing that V5 resizes must accompany any M6 geometry change that alters the width dimension perpendicular to M6 length.

## V5.M5.EN.1 and V5.M6.EN.2: 11 nm Enclosure on Two Opposite Sides

V5.M5.EN.1 and V5.M6.EN.2 each require 11 nm enclosure on at least two opposite sides. Both trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 and trial:i04.cu.def:VIA_VIA56_2_2_66_58.00 combine shape moves with shape resizes in the same group and achieve net violation decreases. In trial:i01.cu.def:VIA_VIA56_2_2_66_58.02, the +320 dbu x-resize applied to all four shapes increases their x-extent following the ±116 dbu pair moves. In trial:i04.cu.def:VIA_VIA56_2_2_66_58.00, the +512 dbu y-resize applied to all four shapes increases their y-extent following the ±132 dbu pair moves. In both cases M5 and M6 are present in touched_layers.

## Spacing Rules V5.S.1, V5.S.2, V5.S.3: 33 nm Minimum on All Metrics

V5.S.1 and V5.S.2 enforce 33 nm minimum projected spacing; V5.S.3 enforces 33 nm minimum euclidean corner-to-corner spacing. In trial:i01.cu.def:VIA_VIA56_2_2_66_58.02, shape pairs move in opposite x-directions (−116 and +116 dbu), altering inter-shape separation within the via array, while a uniform +320 dbu x-resize adjusts each shape's x-extent. In trial:i04.cu.def:VIA_VIA56_2_2_66_58.00, the same axis-paired pattern applies in y (±132 dbu moves, +512 dbu resize). Both trials achieve net violation reductions with conn_preserved.

## Width Rule V5.W.1: 24 nm Minimum Width

V5.W.1 requires minimum 24 nm width. In trial:i01.cu.def:VIA_VIA56_2_2_66_58.02, the +320 dbu x-resize grows all four V5 shapes in x. In trial:i04.cu.def:VIA_VIA56_2_2_66_58.00, the +512 dbu y-resize grows all four V5 shapes in y. Both trials record decision "applied" with net violation reductions.

## Unit-Gate Channel: Polygon Endpoint Extension and Instance Co-Movement

trial:i03.ug.leaf_0003.02 and trial:i05.ug.leaf_0002.01 operate via the unit_gate channel and modify V5 through instance-level moves rather than direct shape operations. In trial:i03.ug.leaf_0003.02, polygon p1683 and eight instances move +32 dbu in x; polygon p1682 and eight instances move −16 dbu in x. In trial:i05.ug.leaf_0002.01, polygon ends are extended in x (+168 dbu for p2086, +132 dbu for p1946, +100 dbu for p2046) and via instances are moved (+136,0 for i0159; −28,0 for i0112; 0,+24 for i0384 and i0528). Both trials record decision "gated_in" with zero new violations out of crop and conn_preserved; trial:i03.ug.leaf_0003.02 brings 26 new violations into crop and trial:i05.ug.leaf_0002.01 brings 22.

## Connectivity Preservation Across All Trials

All four measured trials record conn_preserved: true. This holds for both cu_pool decisions "applied" (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02, trial:i04.cu.def:VIA_VIA56_2_2_66_58.00) and unit_gate decisions "gated_in" (trial:i03.ug.leaf_0003.02, trial:i05.ug.leaf_0002.01). The two gated_in trials both record zero new violations out of crop.