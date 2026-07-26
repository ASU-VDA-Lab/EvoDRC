## Operation Repertoire

Every repair trial in the measured history used move_instance and, where needed, resize_end or via-replacement operations. All 13 trials across both iterations were gated_in with conn_preserved=true (trial:i01.ug.Block1_union_row1.00 through trial:i02.ug.leaf_0004.02). No trial produced a net increase in out-of-crop violations, confirming that the move+resize strategy does not propagate damage beyond the repair window.

## Move_Instance Is the Primary Repair Action

Move_instance operations appear in all 13 trials and are the dominant mechanism for correcting V1 spacing (V1.S.1–V1.S.4) and enclosure (V1.M1.EN.1, V1.M2.EN.2) violations. The standard lateral step is 36 dbu; most instances are displaced by exactly [+36, 0] or [−36, 0] (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row8.07, trial:i01.ug.Block1_union_row9.08, trial:i01.ug.Block1_union_row10.01, trial:i02.ug.Block1_union_row6.01). Larger displacements of 108 dbu appear when a wider gap must be opened (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row8.07). The [−32, 0] variant appears in trial:i01.ug.Block1_union_row6.06 and trial:i01.ug.Block1_union_row8.07; use 36 dbu steps first and fall back to 32 dbu only when the target snap is off the 36-dbu grid.

Apply moves in the positive x-direction when the high-x neighbor has headroom; apply moves in the negative x-direction when the upstream neighbor must retract to open spacing. Trial:i01.ug.Block1_union_row5.05 mixed [+36, 0] and [−36, 0] on the same row simultaneously, and trial:i02.ug.Block1_union_row6.01 mixed [+36, 0] with [−36, 0] for instance i0455 in a five-operation sequence.

A single diagonal move ([+36, −36]) is recorded for instance i0300 in trial:i01.ug.Block1_union_row4.04, showing that y-axis adjustments are also applied when the enclosure geometry requires it; this is the only recorded y-delta in the history.

## Coordinate Move_Instance With resize_end on M2

Whenever an instance is moved, the M2 polygon that forms the V1 landing wire must be resized to maintain V1.M2.EN.2 (enclosure on two opposite sides) and V1.M2.AUX.2 (V1 width matches M2 width). resize_end on the x-axis high end extends the M2 wire rightward: observed deltas are +36 dbu (trial:i01.ug.Block1_union_row5.05), +52 dbu (trial:i01.ug.Block1_union_row4.04), +92 dbu (trial:i01.ug.Block1_union_row3.03), and +128 dbu (trial:i01.ug.Block1_union_row1.00). resize_end on the x-axis low end trims the M2 wire from the left: +36 dbu at the low end appears in trial:i01.ug.Block1_union_row5.05 and trial:i01.ug.leaf_0020.10. Always pair a move_instance step with a resize_end on the affected M2 polygon when the move would otherwise leave V1 under-enclosed or outside M2.

A symmetric resize (both ends adjusted together) is recorded in trial:i01.ug.leaf_0031.11, where polygon p1390 received a uniform +36 dbu resize rather than a directional resize_end; apply this form when the M2 wire must grow symmetrically around V1 to satisfy the 5&5 nm enclosure variant of V1.M2.EN.2.

## Multi-Layer Operations Are Required for Every Repair

All 13 trials touched M1, M2, and V1 simultaneously (trial:i01.ug.Block1_union_row1.00 through trial:i02.ug.leaf_0004.02). No trial repaired V1 violations by modifying V1 geometry directly. V1 polygons move only as passengers inside cell instances; the repair lever is the instance origin and the surrounding M2 wire ends. Do not attempt to fix V1.M1.EN.1 or V1.M2.EN.2 by editing V1 shapes in isolation; move the owning instance and resize M2 to match.

## Via Replacement as an Alternative to Instance Move

Trial:i02.ug.leaf_0004.02 deleted instance i0300 and inserted a new VIA_VIA12 cell at origin [5904, 6300]. Instance i0300 had previously been moved by [+36, −36] during trial:i01.ug.Block1_union_row4.04 at the same locus origin [5344, 5508]. The iteration-2 pass replaced the instance entirely rather than applying a further displacement. Use delete_instance + add_via when a second-iteration repair targets a locus where a prior move_instance on the same instance did not eliminate all violations.

## Connectivity Preservation Is the Binding Acceptance Criterion

Every gated_in decision required conn_preserved=true. Trials trial:i01.ug.Block1_union_row1.00 and trial:i01.ug.leaf_0031.11 introduced 4 new in-crop violations each; trial:i01.ug.Block1_union_row6.06 and trial:i02.ug.Block1_union_row6.01 introduced 1 new in-crop violation each. All four were still accepted because connectivity was intact. Do not sacrifice connectivity to eliminate a spacing or enclosure count; a residual in-crop violation increase is acceptable when conn_preserved remains true, but a repair that breaks connectivity must be rejected regardless of DRC improvement.

## Iteration Structure and Residual Violations

Iteration 1 (trial:i01.ug.Block1_union_row1.00 through trial:i01.ug.leaf_0031.11) left residual violations in at least two units. Block1_union_row6 (locus [8152, 7668, 13752, 8532]) and leaf_0004 (locus origin [5344, 5508]) were both revisited in iteration 2 as trial:i02.ug.Block1_union_row6.01 and trial:i02.ug.leaf_0004.02. The iteration-2 design_state (45ca183...) differs from the iteration-1 state (796a626...), confirming that prior repairs accumulate into a new baseline before the next pass. When a locus appears again in iteration 2, increase the operation count or switch to via replacement; the single-instance move applied in iteration 1 is insufficient for the residual violation at that location.

## Repair Window Sizing

Locus widths in the x-direction range from 684 dbu (trial:i01.ug.leaf_0004.09, locus [9936, 4048, 10620, 4212]) to over 11 792 dbu (trial:i01.ug.Block1_union_row5.05, locus [2536, 6588, 14328, 7452]). Multi-instance rows require wide crop windows so all instances that interact under V1.S.1–V1.S.4 projection spacing rules are visible simultaneously. Single-via units with one instance use narrow windows. The number of operations per trial scales with window width: narrow-window trials use 1–2 ops (trial:i01.ug.leaf_0004.09, trial:i01.ug.leaf_0020.10) while wide-window row repairs use 3–5 ops (trial:i01.ug.Block1_union_row5.05, trial:i01.ug.Block1_union_row8.07, trial:i02.ug.Block1_union_row6.01).

## Nonorthogonal Geometry Must Not Be Introduced

All move and resize deltas in every recorded trial are axis-aligned integer values; no fractional or non-right-angle increments appear in the history (trial:i01.ug.Block1_union_row1.00 through trial:i02.ug.leaf_0004.02). The GEOMETRY.NONORTHOGONAL rule fires on any V1 edge deviating from 0 or 90 degrees. Never produce a fractional-angle delta when computing a move_instance displacement or resize_end amount.