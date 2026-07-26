## Repair Effectiveness

**Y-axis via resizing is the sole confirmed effective repair action for V5 violations in this design.** In trial:i01.cu.def:VIA_VIA56_2_2_66_58.01, applying `resize_via_shape` with `axis=y`, `delta_dbu=248` to all four V5 shapes in cell `VIA_VIA56_2_2_66_58` reduced total violations by 32 (whole-design count dropped from 247 to 215) while preserving connectivity.

## Via Cell Repair Pattern

When a V5 via cell contains multiple shapes requiring enclosure repair, resize all shapes uniformly. In trial:i01.cu.def:VIA_VIA56_2_2_66_58.01, shape indices 0 through 3 in `VIA_VIA56_2_2_66_58` each received the same `delta_dbu=248` on the y-axis; the operation was applied in full (channel decision: `applied`) with no partial application. Applying the same delta to all shapes in the cell, rather than selectively resizing a subset, produced the full -32 violation reduction.

## Enclosure Rules Drive Y-Axis Sizing

Rules V5.M5.EN.1 and V5.M6.EN.2 both require 11 nm enclosure on at least two opposite sides, and the DRC deck tests this by shrinking the enclosing metal independently in x and y. A y-axis resize of V5 directly addresses the y-direction enclosure margin checked by those rules. The measured repair in trial:i01.cu.cu.def:VIA_VIA56_2_2_66_58.01 targeted `axis=y` and achieved a net reduction of 32 violations, confirming that y-direction undersizing was the active failure mode for that cell.

## Large Multi-Layer Instance Moves: No New V5 Violations Introduced

Trial:i02.ug.whole_design.00 applied 69 operations (instance moves, polygon moves, and polygon end-resizes) across layers M3, M4, M5, M6, V3, V4, V5 in a whole-design unit-gate pass. The per-rule delta for that trial records no new in-crop V5 violations of any kind. The operation was gated in (`decision: gated_in`) because connectivity was preserved. This establishes that wholesale instance repositioning at the scale of trial:i02.ug.whole_design.00 does not by itself generate V5 spacing (V5.S.1, V5.S.2, V5.S.3), width (V5.W.1), enclosure (V5.M5.EN.1, V5.M6.EN.2), or containment (V5.AUX.1, V5.M6.AUX.2) violations in Block6.

## Connectivity Preservation Is a Gate Condition

Both trials in the measured history carried `conn_preserved: true`. Trial:i02.ug.whole_design.00 was explicitly accepted on that basis (`reason: conn_preserved` in the delta record). Any V5 repair operation — whether a via shape resize or an instance move touching V5 — must preserve connectivity; the harness uses this as a gate for accepting operations that introduce violations on other rules or layers.

## M6 Width-Match Constraint (V5.M6.AUX.2)

Rule V5.M6.AUX.2 requires V5 to be exactly the same width as M6 perpendicular to the M6 length direction. In trial:i01.cu.def:VIA_VIA56_2_2_66_58.01 the repair resized V5 only on the y-axis; M6 is listed in `touched_layers`, indicating M6 was co-adjusted to maintain the width-match relationship. Do not resize V5 in isolation when V5.M6.AUX.2 applies; the enclosing M6 geometry must be updated in concert, consistent with the observed repair in trial:i01.cu.def:VIA_VIA56_2_2_66_58.01.

## No Evidence for X-Axis V5 Resize

The only V5-specific resize operations in the full measured history use `axis=y` (trial:i01.cu.def:VIA_VIA56_2_2_66_58.01). No x-axis V5 resize has been attempted or measured. V5.M6.AUX.2 ties the x-dimension of V5 to M6 width, making independent x-axis V5 resizing structurally risky; avoid it unless a measured trial demonstrates safety.