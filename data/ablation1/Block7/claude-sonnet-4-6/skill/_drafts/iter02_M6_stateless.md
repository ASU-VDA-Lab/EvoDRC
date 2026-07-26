## Via-cell M6 vertical sizing and V5 co-adjustment

The only applied trial in this layer's history, trial:i02.cu.def:VIA_VIA56_2_2_66_58.01, targeted cell `VIA_VIA56_2_2_66_58` and produced a net reduction of 39 DRC violations across four windows (unit:Block7_union_row21 −1, unit:leaf_0038 −2, unit:leaf_0045 −18, unit:leaf_0046 −18). The fix touched M5, M6, and V5 through 9 operations. All M6 work consisted of a single `resize_via_shape` on shape index 0 in the y-axis by −384 dbu (vertical shrink). The V5 work consisted of four shapes each receiving a paired move and resize: shapes 0 and 1 moved by −132 dbu and resized +128 dbu in y; shapes 2 and 3 moved by +132 dbu and resized +128 dbu in y.

### M6 vertical width and its prohibited-value rules

Rules M6.W.1 through M6.W.4 constrain the y-extent of M6 polygons. M6.W.1 sets a 32 nm floor; M6.W.2 sets a 640 nm ceiling; M6.W.3 prohibits exact even-integer multiples of 32 nm (64, 128, 192, 256, 320, 384, 448, 512, 576, 640 nm); M6.W.4 additionally prohibits widths that span an even number of minimum-width routing tracks vertically (96, 224, 352, 480, 608 nm). In trial:i02.cu.def:VIA_VIA56_2_2_66_58.01 the M6 shape was shrunk by exactly 384 dbu in y, and the result was accepted with conn_preserved=true and a 39-violation reduction. Applying a vertical resize of −384 dbu (or any value that moves the resulting width away from all prohibited M6.W.3 and M6.W.4 values while remaining within [32, 640] nm) is a confirmed effective first operation for this cell class.

Do not leave the M6 y-extent at any value enumerated in M6.W.3 (64, 128, 192, 256, 320, 384, 448, 512, 576, 640 nm) or M6.W.4 (96, 224, 352, 480, 608 nm). Only the range of widths that are neither below 32 nm, above 640 nm, an even-multiple of 32 nm, nor a track-spanning even-multiple are legal. After the −384 dbu resize in trial:i02.cu.def:VIA_VIA56_2_2_66_58.01 the fix passed, confirming the resulting width is in a legal zone.

### V5 enclosure and width-matching must be co-adjusted with every M6 y-resize

Rules V5.M6.EN.2 and V5.M6.AUX.2 jointly require that V5 shapes inside M6 maintain at least 11 nm enclosure on two opposite sides and that the V5 width perpendicular to M6 length exactly matches the M6 width in that direction. In trial:i02.cu.def:VIA_VIA56_2_2_66_58.01, every change to the M6 y-extent was accompanied by coordinated V5 moves and resizes in the same axis. Specifically, the outer V5 pair (shapes 2 and 3) was moved +132 dbu inward and the inner pair (shapes 0 and 1) was moved −132 dbu inward, while all four shapes were resized +128 dbu in y to compensate. Performing an M6 y-resize without simultaneously adjusting V5 positions and sizes will leave V5.M6.EN.2 and V5.M6.AUX.2 unsatisfied; the success of trial:i02.cu.def:VIA_VIA56_2_2_66_58.01 rests on both the M6 operation and all eight V5 operations being applied as a single atomic set.

### Routing-track alignment of minimum-width M6

Rule M6.AUX.2 requires that minimum-width (nominally 32 nm vertical) M6 tracks have their centerline at offsets satisfying a 256 dbu pitch with a 64 dbu phase offset from the origin, conditioned on the polygon's bottom and top edges aligning to a 128 dbu base grid. Rule M6.AUX.1 requires all horizontal M6 edges to lie on a 32 nm grid. These grid constraints are design-wide and were not violated after the y-resize in trial:i02.cu.def:VIA_VIA56_2_2_66_58.01 (conn_preserved=true, no remaining violation entries attributed to M6.AUX.1 or M6.AUX.2 in the delta). When resizing M6 shapes in y, snap both the bottom and top edges to the 32 nm horizontal grid (M6.AUX.1) and verify the centerline satisfies the 256 dbu pitch / 64 dbu offset condition (M6.AUX.2) if the result is a minimum-width track.

### No-bend and non-orthogonal constraints

Rule M6.AUX.3 prohibits any corner vertex in an M6 polygon whose interior angle is between 0° and 90° (i.e., M6 may not bend). Rule M6.GEOMETRY.NONORTHOGONAL prohibits any edge at a non-90°-aligned angle. The single operation on M6 in trial:i02.cu.def:VIA_VIA56_2_2_66_58.01 was a uniform y-resize of a rectangular via shape, which cannot introduce bends or non-orthogonal edges. Restrict M6 operations to pure horizontal/vertical resizes and translations; do not introduce intermediate vertices or diagonal moves.

### M6 horizontal spacing rules governing adjacent tracks

Rules M6.S.1 through M6.S.5 govern spacing. M6.S.2 requires 40 nm horizontal spacing between M6 edges. M6.S.3 requires 40 nm tip-to-tip spacing for shapes on adjacent tracks with no shared parallel run length. M6.S.4 requires 40 nm tip-to-tip spacing for shapes that do share a parallel run length. M6.S.5 requires that any parallel run length between adjacent M6 shapes on adjacent tracks be at least 44 nm. The y-resize in trial:i02.cu.def:VIA_VIA56_2_2_66_58.01 altered the vertical extent of an M6 shape, which affects the tip position along the horizontal axis and therefore the parallel run length seen by neighboring shapes. The 39-violation reduction confirms that the post-resize y-extent did not create new M6.S.3, M6.S.4, or M6.S.5 violations, but neighboring M6 shapes must be checked after any y-resize that changes the tip position.

### Wide M6 and routing-track interaction (M6.AUX.4)

Rule M6.AUX.4 prohibits a wide M6 polygon (wider than minimum-width in y) from having its horizontal outer edges co-planar with a minimum-width routing track's edge. The M6 shape in trial:i02.cu.def:VIA_VIA56_2_2_66_58.01 was resized by −384 dbu, a change large enough to move the outer y-edges away from any prior coincidence with routing-track edges. No M6.AUX.4 violations appear in the remaining delta after the fix, consistent with the resize having cleared any such coincidence. When shrinking or growing a wide M6 shape in y, confirm the resulting top and bottom edges do not land on any minimum-width routing-track edge position.

### V6 enclosure

Rule V6.M6.EN.1 requires that V6 shapes inside M6 maintain at least 11 nm enclosure on two opposite sides. trial:i02.cu.def:VIA_VIA56_2_2_66_58.01 did not include V6 operations, and no V6-attributed violations appear in the window deltas. For VIA56 cells that carry V6 above M6, a y-resize of M6 must be verified against V6.M6.EN.1 in the same way that V5 enclosure was verified via the V5 co-adjustment operations recorded in this trial.