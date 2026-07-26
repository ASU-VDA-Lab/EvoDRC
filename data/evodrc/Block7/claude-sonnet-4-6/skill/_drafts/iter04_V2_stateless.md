## Dominant Violation and Its Root Cause

The only rule with a confirmed measured net reduction in this Block7 assembly is V2.M3.AUX.2. A full-deck KLayout DRC run documented in trial:i04.cu.def:VIA_VIA23_1_3_36_36.01 moved the violation count from 356 to 284, a reduction of 72, with every eliminated error attributed to V2.M3.AUX.2. No measured trial in this history records a net reduction in V2.W.1, V2.S.1, V2.S.2, V2.S.3, V2.S.4, V2.M2.EN.1, V2.M3.EN.2, or V2.AUX.1.

V2.M3.AUX.2 requires that each V2 instance is exactly as wide as the M3 wire it lands on, measured perpendicular to the M3 length direction. The violations arise when M3 stub polygons extend laterally beyond the V2 footprint (or fall short), causing the "same width" check to fail. The repair therefore addresses M3 geometry, not V2 geometry directly.

## Proven Repair: Combo Trim of M3 Stubs Plus VIA Cell Definition Shrink

The single repair action that produced the confirmed -72 count is a coordinated combo edit comprising 72 M3-stub `resize_end` operations (trimming both the low and high y-ends of each stub polygon) combined with one `resize_via_shape` on the VIA_VIA23_1_3_36_36 cell definition, shrinking its M3 landing shape by -40 dbu in y (trial:i04.cu.def:VIA_VIA23_1_3_36_36.01). The trim deltas on the stubs are -32 dbu on both ends for most polygons, with -32 low / -41 high for a subset (e.g., p2629, p2380, p2784, p2928, p2896, p2795, p2929, p2816).

Do not apply the VIA cell definition shrink alone. Trial:i05.cu.def:VIA_VIA23_1_3_36_36.00 applied only the `resize_via_shape` (-40 dbu y on VIA_VIA23_1_3_36_36) without the stub trims and was rejected because it increased the total violation count by 64 (unit:leaf_0006 rose from 130 to 194 errors). The full combo is required; partial application is net harmful.

The identical 73-op set was initially attempted through the unit_gate channel in trial:i04.ug.leaf_0008.07 and was gated out with reason `empty_or_missing_patch`, meaning it did not pass the unit-level locus check. It was subsequently submitted and accepted through the cu_pool channel as a user-accepted combo applied at block scope (trial:i04.cu.def:VIA_VIA23_1_3_36_36.01). When the unit_gate channel rejects a large coordinated M3-stub batch due to locus mismatch, re-submit through cu_pool at block scope with an explicit target on the VIA cell definition.

## Coordinated Instance + Polygon Moves for V2-Bearing Nets

All gated_in unit_gate trials in this history move V2-touching instances and their associated M3/M2 polygons by exactly the same delta vector. Connectivity is preserved in every such case (conn_preserved=true across trial:i01.ug.Block7_union_row16.06, trial:i01.ug.leaf_0095.26, trial:i02.ug.leaf_0001.07, trial:i02.ug.leaf_0014.08, trial:i03.ug.leaf_0001.03, trial:i03.ug.leaf_0002.04, trial:i03.ug.leaf_0011.07, trial:i04.ug.leaf_0002.01, trial:i04.ug.leaf_0003.02, trial:i05.ug.leaf_0001.00). Mismatched deltas between instance moves and polygon moves break connectivity; every gated_in trial avoids this by using a single shared delta applied to all objects on the same net segment.

Small lateral x-axis nudges of 8 dbu applied to an M3 polygon plus its co-located via instances (trial:i04.ug.leaf_0002.01: polygon p2916 and instances i2005, i1790 each +8 dbu x; trial:i04.ug.leaf_0003.02: polygon p2877 and instances i1706, i1738 each +8 dbu x) were gated in with zero new violations introduced. A subsequent correction of -8 dbu x on the same polygon p2916 and instances (trial:i05.ug.leaf_0001.00) was also gated in cleanly. This confirms that sub-grid lateral shifts of this magnitude on M2/M3/V2 stacks are safe when the full instance group moves together.

## M3 Polygon Resize for Geometry Adjustment

Resizing M3 stub ends is the geometric mechanism that resolves V2.M3.AUX.2. Trial:i01.ug.leaf_0095.26 applied `resize_end` on M3 polygon p2432 (y high, +68 dbu) and p3537 (y high, +48 dbu) while simultaneously moving the associated V2-bearing instances; this was gated in with conn_preserved and zero new violations. Trial:i03.ug.leaf_0011.07 reversed one of these: p3537 was trimmed -48 dbu on the high y end (undoing the iter-1 growth) along with matching instance moves, also gated in cleanly (trial:i03.ug.leaf_0011.07). These paired forward/reverse operations confirm that M3 stub end resizing is reversible without connectivity loss when the associated via instances track the stub endpoint.

Trial:i03.ug.leaf_0002.04 added a new M3 polygon (add_polygon at coordinates [11664,11756]-[11908,11828]) alongside resize_end on p2720 (y high, +20 dbu) and p3300 (x low, -88 dbu), plus instance moves, and was gated in with n_new_in_crop=0. Adding an M3 polygon to close a gap is safe when V2 instances are repositioned consistently with the new geometry.

## Iterative Position Correction Pattern

Polygon p3383 (M3, on unit leaf_0001) was moved -57 dbu in y at iter 2 (trial:i02.ug.leaf_0001.07, with instance i1643 co-moved by the same delta) and then corrected +21 dbu in y at iter 3 (trial:i03.ug.leaf_0001.03, same instance co-moved). The iter-3 correction introduced n_new_in_crop=3 in the local crop window but was still gated in (conn_preserved=true, n_new_out_of_crop=0). Net displacement of p3383 after both operations is -36 dbu y from its iter-1 position. When an over-correction is gated in, the crop-local violation count may transiently rise; the block-level DRC state decides whether to retain the move.

## Channel and Scope Selection

Unit_gate trials (channel prefix `ug`) operate on a single-unit locus and require a non-empty patch within that locus. The 73-op block-scope combo was rejected by unit_gate at iter 4 (trial:i04.ug.leaf_0008.07) solely because of locus/patch mismatch, not because the ops themselves were incorrect. The cu_pool channel (channel prefix `cu`) accepts block-scope targets (e.g., `def:VIA_VIA23_1_3_36_36`) and was the correct submission path for the same ops, as confirmed by the applied outcome in trial:i04.cu.def:VIA_VIA23_1_3_36_36.01. Use cu_pool with a `def:` target when the repair touches a shared cell definition or spans more units than unit_gate's locus can cover.

A cu_pool trial is rejected with decision `rejected_net_positive` when the block-level delta_total is positive even if individual windows show zero change, as seen in trial:i05.cu.def:VIA_VIA23_1_3_36_36.00 (unit:leaf_0003 and unit:leaf_0005 unchanged, unit:leaf_0006 +64, net +64 rejected). The rejection threshold is any positive delta_total; a single worsened unit blocks acceptance regardless of other neutral windows.

## V2 Geometry Constraints Summary (from rules, repair context)

V2.W.1 sets minimum V2 width at 18 nm along the M3 length direction. No measured trial has addressed a V2.W.1 violation; all V2 width adjustments in the history act on M3 stub geometry, not on V2 shapes directly.

V2.AUX.1 requires V2 to reside inside both M2 and M3. Every gated_in move trial preserves this by co-moving via instances with their M2/M3 stack; no trial introduced a V2.AUX.1 violation.

V2.M3.AUX.2 is the repair target for this block. The rule is checked by comparing V2 edges against M3 edges perpendicular to the M3 wire direction; V2 must have at least two edges coincident with M3 edges. Trimming the M3 stub to match the V2 footprint (rather than resizing V2) is the repair pattern confirmed by trial:i04.cu.def:VIA_VIA23_1_3_36_36.01.