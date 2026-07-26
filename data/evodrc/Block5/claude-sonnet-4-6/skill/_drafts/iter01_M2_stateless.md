## Operation Types Observed on Layer M2

Two distinct operation channels appear in the iteration-1 history: `unit_gate` (trials i01.ug.*) and `cu_pool` (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). All unit_gate trials carried `decision: gated_in` with `n_new_in_crop: 0` and `n_new_out_of_crop: 0`, meaning they were accepted by the gate but produced no net change to M2 violation count inside the crop window. The single cu_pool trial carried `decision: applied` and reduced the total violation count by 8 (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

---

## move_instance Operations on M2-Touching Instances

All six unit_gate trials used `move_instance` ops on instances whose touched layers included M2 (alongside M1 and V1). All six completed with `conn_preserved: true` and introduced zero new violations within the crop window.

Move deltas observed (x-axis only across all unit_gate trials):

| Trial | Instance(s) | delta_dbu (x) |
|---|---|---|
| trial:i01.ug.Block5_union_row3.00 | i0117, i0131 | +36 each |
| trial:i01.ug.Block5_union_row6.01 | i0025, i0019 | +108 each |
| trial:i01.ug.leaf_0001.02 | i0011 | +36 |
| trial:i01.ug.leaf_0002.03 | i0056, i0103 | +36, -36 |
| trial:i01.ug.leaf_0005.04 | i0017 | +112 |
| trial:i01.ug.leaf_0006.05 | i0012 | +4 |

No y-axis move_instance deltas appear in any unit_gate trial. All instance moves are strictly horizontal (x-axis). Moves as small as 4 dbu (trial:i01.ug.leaf_0006.05) and as large as 112 dbu (trial:i01.ug.leaf_0005.04) were accepted without introducing new M2 violations. Counter-direction moves on distinct instances within the same trial are permissible: trial:i01.ug.leaf_0002.03 moved i0056 by +36 and i0103 by -36, still producing zero new violations.

Do not expect unit_gate move_instance trials to reduce M2 violations directly; their recorded delta is zero in every instance. Their role is repositioning geometry to satisfy violations detected elsewhere, accepted only when connectivity is preserved.

---

## polygon resize Operations on M2

Trial:i01.ug.Block5_union_row6.01 combined two move_instance ops (+108 dbu x) with two `resize` ops on M2 polygons p955 and p971, both along the x-axis, with deltas of +256 dbu and +328 dbu respectively. This trial was gated_in with zero new violations, confirming that x-axis expansion of M2 polygons by these amounts (alongside corresponding instance moves) does not introduce M2 spacing, width, or area violations inside that crop window.

Trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 applied y-axis `resize` ops with delta_dbu of -64 on four consecutive M2 polygons (p894, p895, p896, p897), touching layers M2, M3, and V2. This trial achieved a net violation reduction of 8 (from 25 to 17 in the leaf_0009 window). The accompanying op was a `resize_via_shape` on the VIA_VIA23_1_3_36_36 cell (M3 layer, y-axis, -40 dbu). The targeted cell name (def:VIA_VIA23_1_3_36_36) and the involvement of V2 point directly to rule V2.M2.EN.1, which requires M2 to enclose V2 by at least 5 nm on two opposite sides. Shrinking M2 polygons in y by -64 dbu resolved enclosure violations in this context.

---

## V2.M2.EN.1 Repair Pattern

Rule V2.M2.EN.1 fires when V2 is not enclosed by M2 by at least 5 nm on two opposite sides (checked via `m2.sized(-5.nm, 0)` and `m2.sized(0, -5.nm)`). The only trial that demonstrably reduced M2-related violations (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00) resized four M2 polygons by -64 dbu in y, coordinated with a -40 dbu y-axis shrink of the via shape itself. This produced an 8-violation reduction. The repair targeted a named via cell (VIA_VIA23_1_3_36_36), and the touched layers (M2, M3, V2) match the V2.M2.EN.1 rule's operands exactly.

When M2 polygon edges fail to provide 5 nm enclosure around a V2 instance, shrinking the via shape in the deficient axis alongside shrinking the M2 polygon in the same direction resolves the geometric conflict (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). Connectivity was preserved across all five ops in that trial.

---

## V1.M2.EN.2 and V1.M2.AUX.2 Observations

All unit_gate trials touched V1 alongside M2 and M1. Rule V1.M2.EN.2 requires M2 to enclose V1 by 5 nm on at least two opposite sides. Rule V1.M2.AUX.2 requires V1 to match M2 width exactly in the direction perpendicular to M2 length. All six unit_gate move_instance trials with V1 in touched_layers completed with zero new violations (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.Block5_union_row6.01, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05), confirming that horizontal instance moves of 4-112 dbu do not disturb V1/M2 enclosure relationships when instances are moved as a group (instance and its via content move together).

---

## Connectivity Preservation Requirement

Every trial in the history carries `conn_preserved: true`. No trial was accepted or applied with connectivity broken. Treat connectivity preservation as a hard gate: all M2 resize and move_instance operations must pass connectivity checks before being considered viable repair candidates.

---

## Spacing and Width Rule Context (no direct repair trials observed)

Rules M2.W.1 (minimum width 18 nm), M2.S.1 through M2.S.8, M2.A.1 (minimum area 504 nm²), and M2.S.6 through M2.S.8 (corner-to-corner and diagonal gap constraints) have no direct single-rule repair trials in iteration-1 history. The unit_gate trials that touched M2 produced zero violations in and out, so they neither expose nor resolve those rule-specific patterns. No quantitative repair prescriptions for M2.W.1, M2.S.1–M2.S.8, or M2.A.1 can be grounded in the current measured record.