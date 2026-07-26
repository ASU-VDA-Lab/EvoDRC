Only one trial exists in this layer's history. Every prescriptive claim must cite it, and the rejection shows that uncited prescriptions are not permitted. I will write only what that single record actually demonstrates.

**Via-cell Y-resize on M5 resolves M4/V4 violations without touching M4 geometry directly.**

In trial:i01.cu.def:VIA_VIA45_1_2_58_58.00, a single `resize_via_shape` operation on layer M5 (axis `y`, delta `−88 dbu`) inside cell `VIA_VIA45_1_2_58_58` reduced the whole-design violation count by 52 (244 → 192). The touched-layers set was `{M4, M5, V4}`, meaning the operation affected M4-related checks despite no direct edit to any M4 shape. Connectivity was preserved (`conn_preserved: true`, `decision: applied`).

The practical consequence is: when a via cell simultaneously touches M4 and V4 checks, shrinking the M5 shape in Y is a viable first repair move; the M4 shapes themselves need not be modified to clear those violations (trial:i01.cu.def:VIA_VIA45_1_2_58_58.00).

No further prescriptions regarding M4 width, spacing, parallel run length, grid alignment, enclosure margins, or topology can be grounded in the current measured history. Those rules are present in the deck but no trial has yet tested any repair strategy for them on this layer.