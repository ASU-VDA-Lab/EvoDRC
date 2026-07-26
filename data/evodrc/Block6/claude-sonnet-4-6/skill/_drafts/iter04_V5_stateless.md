**Repair target and cell identity**

All measured V5 repairs in this design block target cell `VIA_VIA56_2_2_66_58`. Both applied trials (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 and trial:i04.cu.def:VIA_VIA56_2_2_66_58.00) address this cell exclusively through direct via shape operations. Repairs to this cell consistently touch M5, M6, and V5 together; trial:i04.cu.def:VIA_VIA56_2_2_66_58.00 also moves M4, M5, M6, and V4 polygons and instances alongside V5 shape adjustments.

**Shape operation structure: paired antisymmetric moves plus uniform resize**

In both applied trials the four V5 shapes in `VIA_VIA56_2_2_66_58` are operated on as two antisymmetric pairs followed by a uniform resize applied to all four shapes.

In trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 the x-axis repair moves shape_index 0 and 2 by −116 dbu and shape_index 1 and 3 by +116 dbu, then resizes all four shapes by +320 dbu along x. The result was −16 total violations (−8 in unit:leaf_0019, −8 in unit:leaf_0020).

In trial:i04.cu.def:VIA_VIA56_2_2_66_58.00 the y-axis repair moves shape_index 0 and 1 by −132 dbu and shape_index 2 and 3 by +132 dbu, then resizes all four shapes by +512 dbu along y. The result was −14 total violations (−14 in unit:leaf_0002, 0 in unit:leaf_0003).

Apply the paired antisymmetric move pattern to all four shapes simultaneously; no applied trial in this history operates on a subset of the four shapes.

**Do not operate on a single axis in isolation when M5/M6 geometry is also being adjusted.** Trial:i04.cu.def:VIA_VIA56_2_2_66_58.00 couples y-axis V5 moves and resizes with x-axis polygon moves and instance translations spanning M4, M5, M6, V4, and V5 together within the same repair group. The −14 violation reduction is attributable to the coordinated multi-layer operation; neither the V5 shape changes nor the M5/M6 moves are recorded as producing results in isolation.

**Resize magnitudes differ by axis.** The x-axis uniform resize applied in trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 was +320 dbu per shape. The y-axis uniform resize applied in trial:i04.cu.def:VIA_VIA56_2_2_66_58.00 was +512 dbu per shape. Apply the resize magnitude that matches the axis being repaired; do not substitute the x-axis value when correcting y-axis enclosure or vice versa.

**V5.AUX.1 and V5.M6.AUX.2 coupling**

V5.AUX.1 fires when any V5 shape is not fully inside both M5 and M6. V5.M6.AUX.2 fires when the V5 width along the direction perpendicular to M6 length does not exactly match the M6 width in that direction. Both applied trials include resize operations on V5 shapes in the same axis as the enclosing metal is being adjusted: trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 resizes V5 in x while touching M5 and M6; trial:i04.cu.def:VIA_VIA56_2_2_66_58.00 resizes V5 in y while moving M5/M6 polygons and instances. Resize V5 shapes to re-match M6 width along the perpendicular axis whenever M6 geometry changes; failure to do so leaves V5.M6.AUX.2 open.

**V5.M5.EN.1 and V5.M6.EN.2 enclosure**

Both rules require 11 nm enclosure on at least two opposite sides. The uniform +320 dbu x-resize in trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 and the uniform +512 dbu y-resize in trial:i04.cu.def:VIA_VIA56_2_2_66_58.00 were each applied together with antisymmetric shape moves, and both produced net violation reductions. Resize must accompany any antisymmetric shape moves; move-only operations on V5 shapes without a corresponding resize are not recorded as an applied solution in this layer's history.

**Spacing rules V5.S.1, V5.S.2, V5.S.3**

All three spacing rules enforce a 33 nm minimum, measured by projection (V5.S.1, V5.S.2) or Euclidean corner-to-corner distance (V5.S.3). No trial in this history applied a spacing-only fix to V5. The antisymmetric paired moves in trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 (±116 dbu in x) and trial:i04.cu.def:VIA_VIA56_2_2_66_58.00 (±132 dbu in y) adjust inter-shape separation within the via cell. After any shape move, verify that the resulting projected and Euclidean spacing between every pair of V5 shapes meets the 33 nm floor before committing the repair.

**Unit-gate moves introduce new V5 violations**

Trial:i03.ug.leaf_0003.02 was gated_in rather than applied because it introduced 26 new violations inside the crop window (0 outside) while V5 was a touched layer. Bulk instance translations that move V5 shapes indirectly—without targeted shape-level resize operations to restore enclosure—create new V5.M5.EN.1, V5.M6.EN.2, or spacing violations. Do not rely on unit-gate instance moves alone to close V5 DRC; follow with targeted shape-level adjustments to V5 as demonstrated in trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 and trial:i04.cu.def:VIA_VIA56_2_2_66_58.00.

**Violation window locality**

Both applied trials record violations distributed across two unit windows simultaneously (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02: leaf_0019 and leaf_0020; trial:i04.cu.def:VIA_VIA56_2_2_66_58.00: leaf_0002 and leaf_0003). The same via cell produces violation counts in multiple unit windows when instances straddle window boundaries or adjacent instances overlap window extents. Address all four shapes of the cell in a single grouped repair operation rather than targeting individual windows separately.

**Width rule V5.W.1**

V5.W.1 sets a 24 nm minimum width for V5 shapes along the M6 length direction. No V5.W.1 violation appears explicitly in the recorded history, but the resize operations in both applied trials expand V5 shapes and never shrink them (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02: +320 dbu in x; trial:i04.cu.def:VIA_VIA56_2_2_66_58.00: +512 dbu in y). Never apply a resize delta that reduces V5 shape width along the M6 length direction below 24 nm; the observed resize magnitudes are consistent with maintaining this floor.

**Connection preservation**

Both applied trials (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 and trial:i04.cu.def:VIA_VIA56_2_2_66_58.00) record `conn_preserved: true`. The antisymmetric-move-plus-uniform-resize pattern, applied to all four shapes of the via cell together and coordinated with the enclosing M5/M6 geometry, preserved connectivity in every successful repair. Trial:i03.ug.leaf_0003.02 also records `conn_preserved: true` but was gated_in due to new violations, not connectivity loss; connectivity loss has not been observed in this layer's history.