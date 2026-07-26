## V2.M3.AUX.2 Is the Dominant Violation Class

V2.M3.AUX.2 requires that each V2 instance be exactly the same width as M3 in the direction perpendicular to the M3 length. At iter 4 the full-deck count stood at 356 V2.M3.AUX.2 markers. The combo edit accepted in trial:i04.cu.def:VIA_VIA23_1_3_36_36.01 cleared 72 of them in a single pass (356 → 284), with `per_rule` confirming all 72 deletions belonged to V2.M3.AUX.2 and zero to any other rule.

## Repairing V2.M3.AUX.2: Required Combo Operation

The repair that succeeded (trial:i04.cu.def:VIA_VIA23_1_3_36_36.01) combined two distinct edits applied together:

1. **M3 stub resize on both ends (y-axis):** 36 distinct M3 stub polygons each received a `resize_end` on both the `low` end (delta_dbu = -32) and the `high` end (delta_dbu = -32 or -41). This narrows the M3 stub in y to match the V2 footprint width.

2. **VIA23 cell M3 landing shrink:** A `resize_via_shape` on cell `VIA_VIA23_1_3_36_36`, layer M3, shape index 0, with delta_dbu = -40 (y-axis) was applied alongside the stub shrinks.

Both parts must be applied together. The identical set of ops had already appeared in trial:i04.ug.leaf_0008.07, but that trial was `gated_out` with reason `empty_or_missing_patch` (locus=null, 73 ops); the ops themselves were correct but the trial lacked a valid crop locus and was rejected at the gating stage, not for DRC reasons.

## Standalone VIA M3 Land Shrink Worsens V2.M3.AUX.2

Applying only the `resize_via_shape` on `VIA_VIA23_1_3_36_36` (M3, delta_dbu = -40) without the accompanying M3 stub `resize_end` operations produced a net increase of +64 violations (leaf_0006 window: 130 → 194). Trial:i05.cu.def:VIA_VIA23_1_3_36_36.00 was `rejected_net_positive` on this basis. Never issue the via M3 land shrink alone; it must be paired with the stub resize operations.

## M3 Stub Resize Asymmetry

Among the 36 stub polygons in the accepted combo (trial:i04.cu.def:VIA_VIA23_1_3_36_36.01), most received symmetric -32 dbu on both ends. A subset (polygons p2629, p2380, p2784, p2928, p2896, p2795, p2929, p2816) received -32 on the `low` end and -41 on the `high` end. The asymmetric cases require the larger -41 delta on the high end to achieve the exact-width match mandated by V2.M3.AUX.2; do not flatten all deltas to -32.

## Move Operations Preserve V2 Stack Connectivity

All accepted unit-gate trials that moved M2/M3/V2 stacks reported conn_preserved=true and introduced zero new violations inside crop (n_new_in_crop=0). Successful move patterns include:

- Moving an M3 polygon and its associated via instance together along y by -57 dbu: trial:i02.ug.leaf_0001.07 (p3383 + i1643).
- Moving an M3 polygon and via instance along y by -12 dbu: trial:i02.ug.leaf_0014.08 (p3515 + i0519 + i0524).
- Moving an M3 polygon and via instances along x by +8 dbu: trial:i04.ug.leaf_0002.01 (p2916 + i2005 + i1790) and trial:i04.ug.leaf_0003.02 (p2877 + i1706 + i1738).
- Moving an M3 polygon and via instances along x by -8 dbu: trial:i05.ug.leaf_0001.00 (p2916 + i2005 + i1790).

The pattern across all these trials: move the M3 stub polygon and every via instance that sits on it by the same delta vector. Mismatching the delta between polygon and instances breaks the V2.AUX.1 / V2.M3.AUX.2 coincidence relationship.

## n_new_in_crop Can Be Non-Zero and Still Gate In

Trial:i03.ug.leaf_0001.03 moved polygon p3383 and instance i1643 by y=+21 (partially reversing the y=-57 from trial:i02.ug.leaf_0001.07) and produced n_new_in_crop=3 while still being `gated_in`. The unit_gate channel gates on conn_preserved, not on n_new_in_crop=0; a trial with a small number of new in-crop violations is accepted provided connectivity is intact.

## V2.AUX.1 and V2.M3.EN.2 Were Not Triggered by Accepted Edits

No accepted trial recorded new violations attributed to V2.AUX.1 (V2 must be inside M2 and M3) or V2.M3.EN.2 (M3 must enclose V2 by 5 nm on at least two opposite sides). The move distances used across accepted trials (8 dbu, 12 dbu, 21 dbu, 48 dbu, 57 dbu) stayed within the enclosure budget without requiring separate enclosure fixups, as confirmed by conn_preserved=true and n_new_in_crop=0 in trial:i02.ug.leaf_0001.07, trial:i02.ug.leaf_0014.08, trial:i04.ug.leaf_0002.01, trial:i04.ug.leaf_0003.02, and trial:i05.ug.leaf_0001.00.

## Gated-Out Trials: Empty-or-Missing-Patch Failure Mode

Trial:i04.ug.leaf_0008.07 had locus=null and was `gated_out` with reason `empty_or_missing_patch` despite carrying 73 syntactically valid ops. A null locus prevents patch construction and blocks gating regardless of op correctness. The same 73 ops, submitted through the cu_pool channel with a valid target (`def:VIA_VIA23_1_3_36_36`), succeeded in trial:i04.cu.def:VIA_VIA23_1_3_36_36.01. When a large batch of M3 stub shrinks is needed, submit via the cu_pool channel targeting the via cell definition, not as a unit-gate crop with no locus.