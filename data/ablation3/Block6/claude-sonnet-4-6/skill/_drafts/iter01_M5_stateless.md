**Via-cell M5 repair on Block6, iteration 1**

Only two trials exist for M5 in this iteration; all prescriptive claims below are grounded in those records.

**Shrinking M5 vertically inside VIA_VIA45 cells eliminates violations efficiently.**
In trial:i01.cu.def:VIA_VIA45_1_2_58_58.00, a single resize_via_shape operation on M5 along the y-axis (delta = -88 dbu, one shape) inside cell VIA_VIA45_1_2_58_58 reduced the whole-design violation count from 247 to 191, a net improvement of 56. Connectivity was preserved. The touched layer set was M4, M5, and V4, meaning the repair simultaneously resolved violations that span V4.M5.EN.2 and V4.M5.AUX.2 alongside any M5 vertical-dimension rules (M5.W.5, M5.S.2). Apply a negative y-axis resize on M5 inside VIA_VIA45 variants as a first-choice repair when V4/M5 enclosure or width-matching violations are reported; a delta of -88 dbu is the only measured value and should be the starting point.

**Growing V5 shapes vertically inside VIA_VIA56 cells also reduces M5-touching violations.**
In trial:i01.cu.def:VIA_VIA56_2_2_66_58.01, four resize_via_shape operations on V5 along the y-axis (each delta = +248 dbu, shapes 0–3) inside cell VIA_VIA56_2_2_66_58 reduced the whole-design count from 247 to 215, a net improvement of 32. Connectivity was preserved. M5 was among the touched layers (M5, M6, V5), so this V5 growth resolves violations whose root cause involves the M5/V5 interface, most directly V5.M5.EN.1 (minimum enclosure of V5 by M5 on two opposite sides, 11 nm). Do not attempt to fix V5.M5.EN.1 by moving or resizing M5 directly in VIA_VIA56 cells before first trying to expand V5 in y; the measured result confirms the V5-grow path works and preserves connectivity.

**Repair sequencing: M5 shape changes and V-layer shape changes are independent within these via cells.**
The two applied trials target distinct cell types (VIA_VIA45 vs. VIA_VIA56) and distinct layers as primary operands (M5 vs. V5). No trial shows that repairing one cell type degrades the other; both were applied from the same pre-repair design state (design_state 685706506817f4f5a58d885e68808402b61fcf189fed22cc344fa6dec38c0f99). Treat repairs to VIA_VIA45/M5 and VIA_VIA56/V5 as non-conflicting operations that can be staged without ordering constraints.

**No M5 horizontal-dimension repairs are recorded in this iteration.**
Rules M5.W.1, M5.W.2, M5.W.3, M5.W.4, M5.S.1, M5.S.3, M5.S.4, M5.S.5, M5.AUX.1, M5.AUX.2, M5.AUX.3, and M5.AUX.4 have zero measured repair trials. Do not apply prescriptive guidance for those rules from this knowledge file; no measured data supports any repair action for them.

**Connectivity is preserved by both via-cell resize strategies.**
Both trial:i01.cu.def:VIA_VIA45_1_2_58_58.00 and trial:i01.cu.def:VIA_VIA56_2_2_66_58.01 report conn_preserved = true. Resize operations on M5 (y shrink) or on V5 (y grow) inside via cells, at the magnitudes used, do not break net connectivity.