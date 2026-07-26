## Effective Repair Pattern: M3 Y-Axis Shrink on VIA_VIA23_1_3_36_36

The single proven repair pattern for V2 violations in this design targets cell `VIA_VIA23_1_3_36_36` via a coordinated M3 y-axis shrink. In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 and trial:i02.cu.def:VIA_VIA23_1_3_36_36.00, the identical op structure — `resize_via_shape` on M3 shape_index=0 by -40 dbu along y, followed by four polygon resizes of -64 dbu along y (p965/p964/p963/p962 in iteration 1; p961/p960/p959/p958 in iteration 2) — was applied and in both cases `decision=applied` with `delta_total=-8`. These are the only two trials in the record with a net-negative V2-touching outcome.

The -8 reduction per application came from different windows across the two iterations: trial:i01 reduced `unit:leaf_0012` from 27 to 19 with no change in `unit:leaf_0013`; trial:i02 reduced `unit:leaf_0003` from 20 to 12 with no change in `unit:leaf_0002`. The pattern therefore resolves violations in distinct spatial windows on successive applications without cross-contaminating adjacent windows.

## M3 Y-Axis Growth on the Same Cell Is Unproductive

The inverse operation — `resize_via_shape` on M3 shape_index=0 by +40 dbu along y — was attempted at iteration 5 (trial:i05.cu.def:VIA_VIA23_1_3_36_36.00) and returned `decision=rejected_net_positive` with `delta_total=0`. The same +40 dbu y-expand on M3 was also dropped from the unit-gate candidate at iteration 5 (trial:i05.ug.leaf_0002.01, `assemble_drops`, reason `cu_pool:rejected_net_positive`). Do not apply positive y-axis M3 growth to VIA_VIA23_1_3_36_36; the measured record shows it produces no violation reduction.

## Unit-Gate Move-Instance Operations Touch V2 Without Dedicated V2 Ops

Trial:i05.ug.leaf_0002.01 touched V2 (among M1, M2, M3, V1) through two `move_instance` operations (`i0071` by [0, 36 dbu] and `i0063` by [36, 0 dbu]) plus an x-axis `resize_end` on p1036 (+56 dbu, end=high). The trial was accepted (`decision=gated_in`) with `conn_preserved=true` despite introducing one new `M1.A.1` violation in crop. No explicit V2-only resize was included in this trial's op list, yet V2 remained in `touched_layers`, indicating that instance moves propagate geometric changes to V2 shapes implicitly through their parent cells.

## Consistency of the Resize Polygon Count

Both applied cu_pool trials (trial:i01 and trial:i02) used exactly four polygon resizes at -64 dbu/y in addition to the via-shape resize. This count and magnitude were consistent across the two successful iterations. The trial that attempted only the single +40 dbu via-shape resize without accompanying polygon resizes (trial:i05.cu.def:VIA_VIA23_1_3_36_36.00) was rejected. The full five-op bundle (one `resize_via_shape` + four `resize` on associated polygons) is the unit of repair; partial application of only the via-shape op at a positive delta was not effective per trial:i05.cu.def:VIA_VIA23_1_3_36_36.00.

## V2.AUX.1 and V2.M3.AUX.2 Sensitivity to M3 Y-Dimension

V2.AUX.1 requires V2 to remain inside both M2 and M3. V2.M3.AUX.2 requires V2 width perpendicular to the M3 length direction to match M3 exactly at that perpendicular cross-section. The measured repair ops shrink M3 along y while also resizing the four associated polygons along y by a larger amount (-64 dbu vs. -40 dbu on the via shape). This differential suggests the polygon resizes adjust M2 or V2 shapes to maintain the M3/V2 width-match required by V2.M3.AUX.2 and the containment required by V2.AUX.1 after the M3 shrink. Applying the via-shape shrink alone would likely violate V2.AUX.1 or V2.M3.AUX.2 by leaving V2 or M2 shapes extending beyond the new M3 boundary; the coordinated four-polygon resize prevents this. This is grounded in trial:i01 and trial:i02 both using the five-op bundle and achieving clean `conn_preserved=true` outcomes.

## Spacing Rule Context: V2.S.1 Track-Direction Spacing Is 18 nm on Same M3 Track

V2.S.1 enforces a minimum 18 nm same-track spacing (projection metric) between V2 instances on the same M3 track, 27 nm between V2 instances on parallel non-aligned M3 tracks, and 18 nm between V2 instances on parallel aligned M3 tracks. The y-axis shrink applied in trial:i01 and trial:i02 reduces M3 end-cap extent along y, which compresses the `v2_mask` regions used in the V2.S.1 check. Shrinking M3 along y on both ends of the via shape reduces the effective projected spacing-check footprint between adjacent V2 masks, resolving violations where two V2 masks on the same track were closer than 18 nm before the shrink but compliant afterward.

## No V2.W.1 Violations Were Introduced by Applied Repairs

V2.W.1 requires a minimum V2 width of 18 nm along the M3 length direction. Neither trial:i01 nor trial:i02 produced a net-positive delta or were flagged as introducing new violations; both ended with `decision=applied` and negative delta totals. The -40 dbu y-shrink on the via shape and -64 dbu y-shrink on associated polygons did not trigger V2.W.1 errors in the measured outcomes, establishing that VIA_VIA23_1_3_36_36 has sufficient y-dimension headroom to absorb at least two sequential -40/-64 dbu y-shrink passes without falling below the 18 nm width floor.