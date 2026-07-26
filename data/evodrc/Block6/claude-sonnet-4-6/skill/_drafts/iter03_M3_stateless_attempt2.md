## Via Cell Geometry: V2.M3.EN.2 and V2.M3.AUX.2

Resizing and repositioning V2 shapes along the x-axis inside a via cell definition directly reduces M3-layer DRC violations governed by V2.M3.EN.2 and V2.M3.AUX.2. In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, five x-axis ops on three V2 shapes (two `move_via_shape` and three `resize_via_shape`) in cell VIA_VIA23_1_3_36_36 produced a net reduction of 78 DRC markers (42 in window leaf_0019, 36 in leaf_0020) with full connectivity preserved; the trial was accepted as `applied`. Apply x-axis resize before x-axis move when correcting V2 enclosure by M3: the op sequence in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 interleaved a move followed by resizes on the same shape index, then closed with a move on a second shape, and the combined set resolved both the projection-gap and the opposite-side enclosure checks simultaneously.

V2.M3.AUX.2 requires V2 width to exactly match M3 width in the direction perpendicular to M3 length. When an x-axis resize is applied to V2, verify the perpendicular M3 edge does not move; trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 touched M2 and M3 in addition to V2, confirming that via cell edits propagate geometry changes to both enclosing metal layers and must be checked for M3.W.1 (minimum width 18 nm) and M3.S.1 (minimum side-to-side spacing 18 nm for edges longer than 36 nm) after every resize.

## Instance Moves on M3: Y-Axis Displacement Strategy

Unit-gate instance moves along the y-axis are the dominant operation class across the M3-touching trials accepted in iterations 2 and 3. In trial:i02.ug.leaf_0010.06, 24 instances received y-axis displacements of ±24 dbu or ±72 dbu, and 12 M3/M4/M5 polygon ends were resized by 24 or 72 dbu on the same axis; 26 new violations were introduced inside the crop window and zero outside it, and the trial was gated in with connectivity preserved. In trial:i03.ug.leaf_0002.01, 20 instances received y-axis displacements of ±48 dbu or ±96 dbu, introducing 35 new in-crop violations, also gated in with connectivity preserved.

Use y-axis displacement magnitudes that are multiples of 24 dbu (24, 48, 72, 96) when repositioning M3-touching instances; every accepted unit-gate trial in this history (trial:i02.ug.leaf_0003.03, trial:i02.ug.leaf_0010.06, trial:i03.ug.leaf_0002.01) used displacements that are integer multiples of 24 dbu, consistent with the M3 grid implied by the 18 nm minimum width and spacing rules (M3.W.1, M3.S.1).

Do not use y-axis displacements that would place M3 edge-to-edge gaps below 18 nm (M3.S.1) or tip-to-side gaps below 25 nm (M3.S.2). The unit-gate trials accepted here introduce new in-crop violations precisely because the repositioned instances create new proximity relationships; the gating criterion is connectivity preservation, not zero new violations. Accordingly, accept a unit-gate move only when `conn_preserved` is confirmed, as demonstrated in all three unit-gate trials (trial:i02.ug.leaf_0003.03, trial:i02.ug.leaf_0010.06, trial:i03.ug.leaf_0002.01).

## Small X-Axis Instance Moves

A single small x-axis displacement of −16 dbu on one instance (trial:i02.ug.leaf_0003.03) touching M3, M4, and V3 introduced only 2 new in-crop violations and zero out-of-crop violations and was gated in. This is the smallest move magnitude observed in this history and produced the lowest new-violation count among the unit-gate trials. Prefer smaller x-axis moves when only a narrow M3 spacing gap (M3.S.1 or M3.S.2) needs correction and the instance has V3 connections, because the V3.M3.EN.1 enclosure constraint (5 nm minimum on two opposite sides) limits how far an M3 polygon can shift before losing via coverage.

## V3.M3.EN.1 Interaction with Instance Moves

V3.M3.EN.1 requires V3 to be enclosed by M3 by at least 5 nm on at least two opposite sides. All three unit-gate trials (trial:i02.ug.leaf_0003.03, trial:i02.ug.leaf_0010.06, trial:i03.ug.leaf_0002.01) touch V3 alongside M3; connectivity was preserved in each case, confirming that the applied move magnitudes (16, 24, 48, 72, 96 dbu) kept V3 within M3 coverage. Do not apply y-axis instance moves larger than 96 dbu without re-verifying V3.M3.EN.1, as no accepted trial in this history uses a y-displacement exceeding 96 dbu on M3-V3 instances.

## Tip Spacing Rules: M3.S.3, M3.S.4, M3.S.5

M3.S.3 (27 nm tip-to-tip when both tips are 24–36 nm), M3.S.4 (31 nm tip-to-tip when both tips are < 24 nm), and M3.S.5 (31 nm tip-to-tip when one tip is 24–36 nm and the other is < 24 nm) apply at M3 wire ends. The via cell edit in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 resized V2 shapes whose enclosing M3 tips interact with these rules; when sizing a V2 shape outward in x, the M3 tip edge length increases and may cross the 24 nm or 36 nm thresholds that activate M3.S.3 vs. M3.S.5 vs. M3.S.4. After any V2 resize that changes M3 tip width, re-check which tip-spacing rule governs and confirm the resulting tip gap meets the applicable minimum.

## M3.S.6 Corner-to-Corner Spacing

M3.S.6 requires 20 nm minimum corner-to-corner (Euclidean) spacing between M3 polygons. Instance moves that close y-axis gaps between M3 wires on adjacent instances may satisfy projection-based spacing rules while violating M3.S.6 at polygon corners. The unit-gate trials (trial:i02.ug.leaf_0010.06, trial:i03.ug.leaf_0002.01) each introduced new in-crop violations after y-axis moves; M3.S.6 is a candidate contributor when moved instances bring M3 polygon corners into proximity without their long edges being parallel. Verify corner-to-corner clearance after every multi-instance y-axis repositioning operation.

## M3.A.1 Minimum Area

M3.A.1 requires each M3 polygon to have area of at least 504 nm². Resize operations on M3 polygon ends (as seen in trial:i02.ug.leaf_0010.06, where 12 polygon-end resizes of 24 or 72 dbu were applied) can shrink a polygon if a low-end is moved inward; confirm that the resulting polygon area remains above 504 nm² after any end-resize that reduces polygon length. No M3.A.1 failure is recorded in the history, but the polygon-end resize operations in trial:i02.ug.leaf_0010.06 are the operations most likely to reduce M3 area and must be checked.