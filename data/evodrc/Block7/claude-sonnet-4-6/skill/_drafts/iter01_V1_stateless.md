## Repair Strategy: Operate on M1 and M2, Not on V1 Directly

All 27 accepted trials in this iteration resolve V1 DRC violations exclusively by modifying M1 and M2 geometry (via `move_instance`, `resize_end`, `resize`, `add_polygon`, and `move` on polygon objects), never by moving V1 instances themselves. V1 is a via whose shape and position are determined by M1 and M2 overlap; correcting violations means adjusting the enclosing metal layers. This pattern holds across every row unit and leaf cell in Block7, from trial:i01.ug.Block7_union_row10.00 through trial:i01.ug.leaf_0095.26.

## Dominant Repair Direction: X-Axis

The overwhelmingly dominant repair axis is x. Of all 27 trials, all but three (trial:i01.ug.Block7_union_row16.06, trial:i01.ug.Block7_union_row19.09, trial:i01.ug.leaf_0095.26) contain exclusively x-axis move or resize operations. Y-axis corrections appear only in combination with x-axis corrections in those three cases, and in each the y-delta is small (12 dbu or 48 dbu) relative to the corresponding x-deltas. Apply x-axis corrections first and reserve y-axis moves for cases where x-only adjustment is insufficient.

## Move Magnitudes Follow a Discrete Ladder

Observed `delta_dbu` values for `move_instance` cluster around a small set: 4, 12, 24, 28, 36, 40, 52, 64, 68, 72, 108, 136, 160, 192, 216, 288 dbu. The most frequent are 36 dbu and 72 dbu, appearing in the majority of trials (trial:i01.ug.Block7_union_row6.18, trial:i01.ug.Block7_union_row9.21, trial:i01.ug.Block7_union_row11.01, trial:i01.ug.Block7_union_row14.04, trial:i01.ug.Block7_union_row17.07, and many others). Prefer candidate moves snapped to 36 dbu or 72 dbu increments. Larger moves of 108 dbu and 136 dbu are used when spacing violations require moving an instance a full M2-pitch distance away (trial:i01.ug.leaf_0001.22, trial:i01.ug.Block7_union_row7.19, trial:i01.ug.Block7_union_row24.14, trial:i01.ug.Block7_union_row13.03). The 4 dbu case (trial:i01.ug.Block7_union_row22.12) shows that fine-grained sub-grid moves are accepted when they satisfy the enclosure check.

## Instance Movement Must Be Paired with M2 Resize to Maintain V1.M2.AUX.2 and V1.M2.EN.2

When an instance carrying a V1 is moved in x, the M2 polygon spanning that V1 frequently needs a `resize_end` on one end to maintain flush coincidence of V1 edges with M2 edges (required by V1.M2.AUX.2) and enclosure (V1.M2.EN.2). Specifically:

- Moving an instance to higher x while keeping the M2 end fixed reduces enclosure at the high end and leaves the via partially outside M2, violating V1.AUX.1. Apply `resize_end` axis=x end=high to extend M2 to follow.
- Moving an instance to lower x (negative delta) while extending the M2 low end (resize_end axis=x end=low) was the pattern in trial:i01.ug.Block7_union_row3.15 and trial:i01.ug.Block7_union_row8.20, where a negative-direction instance move was paired with a positive delta on the low M2 edge to close the gap.
- trial:i01.ug.Block7_union_row10.00 combined a 52 dbu positive x-move with a 308 dbu M2 resize_end high and a separate 180 + 56 dbu two-step resize on a second M2 polygon.
- trial:i01.ug.Block7_union_row24.14 shows three simultaneous M2 resize_end high operations (136 dbu, 120 dbu, 128 dbu) accompanying three instance moves of 136 dbu, 64 dbu, and 72 dbu, confirming that each affected M2 segment must be extended independently.

Always audit adjacent M2 segments when moving an instance, and extend any M2 end that would undercut V1.M2.EN.2's 5 nm projection requirement.

## resize (whole-polygon) vs resize_end (one end)

Two resize forms appear in the history:

- `resize_end` (axis, end, delta_dbu): extends or contracts one end of an M2 segment in a single axis direction. Used when only one tip of M2 needs adjustment to restore enclosure. Appears in trial:i01.ug.Block7_union_row10.00, trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row13.03, trial:i01.ug.Block7_union_row14.04, trial:i01.ug.Block7_union_row15.05, trial:i01.ug.Block7_union_row17.07, trial:i01.ug.Block7_union_row18.08, trial:i01.ug.Block7_union_row24.14, and others.
- `resize` (no end qualifier, axis or no axis, delta_dbu): moves the entire M2 polygon or applies a symmetric size delta. Appears in trial:i01.ug.Block7_union_row15.05 (160 dbu x resize on polygon p3586) and trial:i01.ug.Block7_union_row19.09 (40 dbu resize on p3619, -72 dbu resize on p3654, 72 dbu resize on p3523).

Use `resize_end` when one via is displaced relative to a fixed-anchor end of M2. Use full `resize` when the M2 segment itself must shift while following an instance that is also being moved by the same delta, as in trial:i01.ug.Block7_union_row19.09 where instance i0026 and polygon p3654 both received -72 dbu.

## add_polygon to Extend M2 Coverage

When no existing M2 polygon can be stretched to cover a V1 location, add a new M2 polygon. trial:i01.ug.Block7_union_row20.10 inserted a rectangle on M2 at points [5992,22824],[5992,22896],[6048,22896],[6048,22824] (56 x 72 dbu, x-width 56 dbu = 14 nm at 4 dbu/nm scale). This trial accompanied a -36 dbu move of instance i0753, suggesting the add fills a gap created after the instance shift displaced a V1 away from its original M2 coverage. Apply `add_polygon` on M2 when a `move_instance` leaves a V1 with no M2 parent rectangle satisfying V1.AUX.1.

## Multi-Instance Coordinated Moves Are Normal

The number of operations per trial spans 1 (trial:i01.ug.Block7_union_row22.12, trial:i01.ug.leaf_0001.22, trial:i01.ug.leaf_0002.23) to 11 (trial:i01.ug.Block7_union_row14.04). Rows with more V1 instances per locus need more simultaneous adjustments. In trial:i01.ug.Block7_union_row14.04, 9 instance moves plus 2 M2 resize_ends were applied together in a single accepted repair. Do not attempt to fix V1 spacing violations one instance at a time if the row contains multiple violating V1 pairs; co-move all affected instances in the same operation set to avoid introducing new V1.S.1 violations between the just-moved and as-yet-unmoved neighbors.

## V1.M1.EN.1: M1 Enclosure Follows Instance Moves Automatically in Most Cases

All repairs that touched M1 did so through `move_instance`, not through direct M1 polygon resizing. This implies M1 geometry is coupled to instance placement and moves with the instance. No standalone M1 polygon resize operation appears in the history. Do not plan standalone M1 resize ops to fix V1.M1.EN.1; instead, move the instance so that the M1 polygon it carries satisfies the 5 nm / 2 nm opposite-side enclosure rule, then verify that the resulting M1 position also satisfies its own spacing rules.

## Y-Axis Polygon Move (op type "move") for V1 on Horizontal M2

trial:i01.ug.Block7_union_row16.06 used a `move` operation on polygon p3516 with axis=y and delta=-12 dbu alongside y-axis instance moves of -12 dbu. This is the only `move` polygon operation in the history. It co-occurred with the only trial that touches M3 and V2 in addition to M1, M2, V1 (trial:i01.ug.leaf_0095.26 also touches M3/V2). When V1 violations are entangled with upper metal layers, a vertical polygon translate may be required in addition to instance moves.

## New In-Crop Violations Are Acceptable if Connectivity Is Preserved

Several accepted trials introduce new DRC violations within the crop window (n_new_in_crop > 0): trial:i01.ug.Block7_union_row13.03 introduces 1, trial:i01.ug.Block7_union_row19.09 introduces 1, trial:i01.ug.Block7_union_row21.11 introduces 9, trial:i01.ug.Block7_union_row22.12 introduces 2, trial:i01.ug.Block7_union_row24.14 introduces 2, trial:i01.ug.Block7_union_row4.16 introduces 1, trial:i01.ug.Block7_union_row5.17 introduces 1, trial:i01.ug.leaf_0002.23 introduces 2, trial:i01.ug.leaf_0024.25 introduces 1. All were accepted (decision="gated_in") because conn_preserved=true. Do not reject a repair solely because it introduces new in-crop violations; the gating criterion is connectivity preservation, not zero new violations.

## All Iter-1 Trials Accepted: The Unit-Gate Channel Accepts Conn-Preserving Repairs Unconditionally

Every trial in this iteration was accepted via the "unit_gate" channel with conn_preserved=true and decision="gated_in". No trial was rejected. This confirms that the unit_gate channel's acceptance criterion at iteration 1 is: connectivity preserved and no new out-of-crop violations (n_new_out_of_crop=0 in all 27 trials). Design choices that preserve nets while possibly introducing new in-crop violations are viable for passage through this gate.