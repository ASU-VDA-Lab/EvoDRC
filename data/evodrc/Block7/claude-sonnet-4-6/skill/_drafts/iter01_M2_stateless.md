## Repair Operation Vocabulary

All 27 trials in this iteration used the `unit_gate` channel and were accepted (decision=gated_in) with connectivity preserved (trial:i01.ug.Block7_union_row10.00 through trial:i01.ug.leaf_0095.26). The full repair vocabulary for M2 violations on Block7 consists of five operation types: `move_instance`, `resize_end`, `resize`, `add_polygon`, and polygon-level `move` (y-axis).

**move_instance** is the most frequent primitive: every trial applies at least one move_instance, and trials with simpler spacing violations resolve with move_instance alone (trial:i01.ug.Block7_union_row11.01, trial:i01.ug.Block7_union_row22.12, trial:i01.ug.leaf_0001.22). Do not reach for polygon operations before exhausting instance moves.

**resize_end** is applied after move_instance when the instance displacement creates or leaves a width or enclosure shortfall on an M2 polygon endpoint (trial:i01.ug.Block7_union_row10.00, trial:i01.ug.Block7_union_row13.03, trial:i01.ug.Block7_union_row14.04, trial:i01.ug.Block7_union_row17.07, trial:i01.ug.Block7_union_row18.08, trial:i01.ug.Block7_union_row24.14). Always pair a resize_end with the instance move that displaces the connected polygon end; leaving the endpoint unadjusted produces secondary width or enclosure violations.

**resize** (symmetric, both ends) applies to M2 polygons that require uniform extension without a neighboring instance move dictating one specific end (trial:i01.ug.Block7_union_row15.05, trial:i01.ug.Block7_union_row19.09). Use resize when side-spacing or enclosure rules require growth or shrinkage across the full x-extent of an M2 wire simultaneously.

**add_polygon** is used only when an M2 segment is absent and cannot be recovered by moving existing geometry (trial:i01.ug.Block7_union_row20.10). The inserted polygon in trial:i01.ug.Block7_union_row20.10 occupied [5992,22824]-[6048,22896] dbu, giving width 56 dbu and height 72 dbu. Both dimensions exceed the 18 dbu M2.W.1 minimum, and the area (56×72 = 4032 nm²) is well above the 504 nm² M2.A.1 floor. Do not insert an M2 patch whose width in either axis falls below 18 dbu (M2.W.1) or whose area falls below 504 nm² (M2.A.1).

**Polygon-level y-axis move** appears only in trials that also touch M3 and V2 (trial:i01.ug.Block7_union_row16.06, trial:i01.ug.leaf_0095.26). Apply polygon-level y moves on M2 only when the repair requires realignment of a via stack spanning M2, V2, and M3; pure M2 spacing violations resolve with x-axis operations alone.

---

## Instance Move Magnitudes

Small moves (4–40 dbu) resolve spacing violations with minimal disruption (trial:i01.ug.Block7_union_row22.12 used 4 dbu; trial:i01.ug.Block7_union_row9.21 and trial:i01.ug.Block7_union_row6.18 used 36–40 dbu). Large moves (72–288 dbu) are required when the violation margin is large or when multiple polygons must shift together (trial:i01.ug.Block7_union_row10.00 used 52, 288, and 216 dbu across three instances; trial:i01.ug.Block7_union_row14.04 used 136, 108, and 72 dbu; trial:i01.ug.Block7_union_row24.14 used 136, 64, and 72 dbu).

Never pair a large instance move with a resize_end in the opposing direction without verifying that the net displacement satisfies the target spacing rule. Trial:i01.ug.Block7_union_row13.03 applied a +56 dbu resize_end on the low end and a +100 dbu resize_end on the high end of the same polygon alongside 136 dbu instance moves, demonstrating that asymmetric endpoint correction is required when an instance move overpowers one end.

resize_end deltas as small as 16 dbu (trial:i01.ug.Block7_union_row14.04, polygon p3539) and as large as 308 dbu (trial:i01.ug.Block7_union_row10.00, polygon p3286) are accepted. A 16 dbu resize_end on a polygon end indicates the width or enclosure deficit at that endpoint was 2 dbu; precision at the dbu level is necessary.

---

## Connectivity as the Acceptance Gate

All 27 accepted trials set conn_preserved=true. The gating criterion is connectivity preservation, not zero new in-crop violations. Trial:i01.ug.Block7_union_row21.11 introduced 9 new in-crop violations and was still accepted because conn_preserved was true. Do not discard a repair candidate solely because n_new_in_crop > 0; verify conn_preserved=true first.

No trial produced n_new_out_of_crop > 0. Confine all M2 geometry changes to within the designated locus; no accepted trial spread repair effects outside its crop boundary.

---

## Multi-Instance Repairs

When multiple instances along the same row contribute to a single DRC violation, move all contributing instances in consistent directions and magnitudes. Trial:i01.ug.Block7_union_row9.21 moved five instances each +40 dbu x. Trial:i01.ug.Block7_union_row6.18 moved five of six instances at +36 dbu x (the sixth at +28 dbu). Inconsistent instance moves within the same crop window introduce secondary tip-to-side or tip-to-tip violations, which explains the mixed resize_end adjustments in trial:i01.ug.Block7_union_row10.00 (52, 288, -216, 180, 56 dbu across different objects).

Bidirectional instance moves are valid when the violation is a pinch between two converging polygons. Trial:i01.ug.Block7_union_row14.04 moved i0519 by -36 dbu while moving i0874, i0915, i0920 in the positive x direction, resolving a bilateral spacing conflict. Use bidirectional moves whenever two neighboring M2 edges are both inside their respective minimum spacing margins.

---

## Via Enclosure Rules and resize_end Coupling

V1.M2.EN.2 requires M2 to enclose V1 by at least 5 nm on two opposite sides. V1.M2.AUX.2 requires V1 to match M2 width along the direction perpendicular to the M2 length. When resize_end is applied to an M2 polygon endpoint, verify that the resized end still encloses all V1 contacts at that end by at least 5 nm. Every trial that applied resize_end also listed V1 in touched_layers (trial:i01.ug.Block7_union_row10.00, trial:i01.ug.Block7_union_row13.03, trial:i01.ug.Block7_union_row24.14), confirming that V1 geometry is co-adjusted whenever M2 endpoints change.

V2.M2.EN.1 requires M2 to enclose V2 by at least 5 nm on two opposite sides. In trials touching both M2 and V2 (trial:i01.ug.Block7_union_row16.06, trial:i01.ug.leaf_0095.26), y-direction moves on M2 instances (-12 dbu in trial:i01.ug.Block7_union_row16.06, +48 dbu in trial:i01.ug.leaf_0095.26) adjust M2 polygon position to re-satisfy V2 enclosure after the primary x-direction spacing repair. Apply y-direction moves on M2 only when V2 is listed in touched_layers.

---

## M2.A.1 Floor When Adding or Shrinking Polygons

The minimum M2 area is 504 nm². The only add_polygon in the measured history (trial:i01.ug.Block7_union_row20.10) produced a 56×72 dbu rectangle (4032 nm²), 8× above the minimum. Do not insert M2 patches sized below 23×22 dbu (smallest integer-dbu rectangle above 504 nm²). When shrinking an M2 polygon to resolve a spacing violation, compute the post-shrink area before committing. A resize of -72 dbu on polygon p3654 (trial:i01.ug.Block7_union_row19.09) was accepted; verify that the pre-shrink polygon dimensions provide sufficient margin above 504 nm² before applying any shrink operation.

---

## M2.S.7 and M2.S.8 Compound Rules

M2.S.7 forbids a tip-to-tip gap of 18 nm co-located with side-to-side spacing at or below 32 nm; parallel run length must reach 35 nm when side spacing is at or below 32 nm. M2.S.8 requires diagonal gap center-to-center spacing of at least 80 nm between M2 tip-to-tip gaps on different tracks. Neither rule is satisfied by a uniform single-direction instance move because both depend on relative positions of gap centers across M2 tracks. Apply asymmetric multi-instance moves to stagger gap positions when neighboring M2 tracks have gaps near the 80 nm diagonal threshold. Trial:i01.ug.Block7_union_row19.09 applied -72 dbu on i0026 (plus -72 dbu resize on p3654), +36 dbu on i0294, and +72 dbu on i0418 (plus +72 dbu resize on p3523) within the same crop window, dispersing gap centers to satisfy M2.S.8 spacing.

---

## Non-Orthogonal Geometry

All M2 polygons in accepted trials remain rectilinear; every operation is axis-aligned to x or y. No accepted trial introduced a non-orthogonal M2 edge (trial:i01.ug.Block7_union_row10.00 through trial:i01.ug.leaf_0095.26). Never apply diagonal or angled resize operations to M2 polygons; the GEOMETRY.NONORTHOGONAL rule flags any edge with angle outside {0°, 90°, 180°, 270°} on all drawing layers including M2.