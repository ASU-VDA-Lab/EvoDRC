## Repair Effectiveness by Operation Type

**M5 x-axis resize on via cell shapes does not reduce V5 violations.** Shrinking the M5 shape of cell `VIA_VIA56_2_2_66_58` by -96 dbu along the x-axis produced `delta_total = 0` (244 violations before and after) and was rejected as `rejected_net_positive` (trial:i01.cu.def:VIA_VIA56_2_2_66_58.01). Do not apply unidirectional M5 x-resize to this cell when targeting V5 violations; the operation changes M5 geometry but leaves the V5 violation count unchanged.

**Whole-design instance and polygon moves touching V5 can achieve acceptance.** A 57-operation set of `move_instance` and `move` (polygon) ops spanning M3–M6, V3–V5 was accepted (`gated_in`, `conn_preserved`) in trial:i02.ug.whole_design.00. The trial added 48 new in-crop `V1.M2.AUX.2` violations but zero new out-of-crop violations; acceptance was granted because connectivity was preserved. This establishes that bulk repositioning operations on V5-touching layers can pass the gate even when they incidentally introduce in-crop violations on other layers, provided connectivity is maintained.

## Via Cell Association

Cell `VIA_VIA56_2_2_66_58` has V5 among its `touched_layers` (trial:i01.cu.def:VIA_VIA56_2_2_66_58.01). Repairs targeting V5 violations must consider this cell as a locus. The cell name pattern `VIA56` indicates it bridges M5 and M6, consistent with V5.AUX.1 (V5 must be inside both M5 and M6) and V5.M6.AUX.2 (V5 width must match M6 width perpendicular to M6 length).

## Move Grid Observed in Accepted Ops

All move deltas in the accepted trial (trial:i02.ug.whole_design.00) are multiples of 8 dbu: observed values include ±16, ±24, ±32, ±48, ±64, ±72, ±96 dbu. Use move deltas aligned to the 8-dbu grid when repositioning V5-touching instances or polygons.

## Rule-Specific Repair Constraints (from DRC rules, grounded by history)

**V5.AUX.1 and V5.M6.AUX.2 impose coupled M5+M6 containment.** Any move or resize that shifts V5 relative to its enclosing M5 or M6 risks violating V5.AUX.1 (V5 not inside both M5 and M6) or V5.M6.AUX.2 (V5 width must match M6 width perpendicular to M6 length). The M5 x-resize in trial:i01.cu.def:VIA_VIA56_2_2_66_58.01 touched M5, M6, and V5 together; the zero-delta outcome confirms that resizing M5 alone without corresponding V5 or M6 adjustment does not resolve the coupled containment constraint.

**V5.M5.EN.1 and V5.M6.EN.2 require 11 nm enclosure on two opposite sides.** These rules evaluate both x and y enclosure independently (`m5.sized(-11.nm, 0)` and `m5.sized(0, -11.nm)`). Resizing M5 in a single axis by -96 dbu (as in trial:i01.cu.def:VIA_VIA56_2_2_66_58.01) did not fix violations, which is consistent with a scenario where the enclosure deficiency exists on the perpendicular axis that was not resized; always verify enclosure on both opposing side pairs before committing a single-axis resize.

**V5.W.1 minimum width is 24 nm.** No trial in this history records a V5 width change, so width repair has not been measured. Do not resize V5 below 24 nm.

**V5.S.1, V5.S.2, V5.S.3 all require 33 nm spacing** (same-net, different-net, and corner-to-corner respectively). The bulk move trial (trial:i02.ug.whole_design.00) repositioned many V5-touching instances without adding new out-of-crop V5 spacing violations, confirming that coordinated multi-instance moves can respect these spacing rules simultaneously. Moving a single instance in isolation without verifying neighboring V5 spacing remains unvalidated by the current history.