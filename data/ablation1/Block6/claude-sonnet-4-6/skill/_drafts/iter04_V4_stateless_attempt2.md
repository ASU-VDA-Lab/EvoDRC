## V4.M5.AUX.2 — Resize M5 perpendicular dimension to fix width-match violations

The single confirmed repair for V4.M5.AUX.2 violations is a `resize_via_shape` operation that adjusts M5 size along the axis perpendicular to M5's routing direction. In trial:i01.cu.def:VIA_VIA45_1_2_58_58.00, a y-axis resize of M5 by −88 dbu on cell VIA_VIA45_1_2_58_58 (group `v4_m5_aux2_fix`) reduced total V4 violations by 56, across two affected windows (unit:leaf_0019: 139→109; unit:leaf_0020: 154→128). This repair was applied in the `cu_pool` channel and touched layers M4, M5, and V4. The rule V4.M5.AUX.2 requires that V4 width exactly matches M5 width in the direction perpendicular to M5 length; the only confirmed fix is a shrink of M5 along the mismatched axis to achieve this coincidence.

## Move-instance operations introduce net-new V4 violations in crop

Instance moves at the unit level generate new V4 violations within the crop window without removing any. In trial:i04.ug.leaf_0003.01, 24 `move_instance` operations on leaf_0003 (channel `unit_gate`, iter 4, touching M3, M4, M5, V3, V4) produced 68 new violations inside the crop and 0 outside. The trial was accepted (decision: `gated_in`) solely because `conn_preserved` was true. Avoid relying on move-instance repairs to reduce V4 DRC counts: trial:i04.ug.leaf_0003.01 confirms that even conn-safe moves can introduce a large number of new in-crop V4 violations while contributing zero reductions.

## Connectivity preservation does not imply DRC improvement for V4

The `unit_gate` channel accepts a trial when `conn_preserved` is true, regardless of new V4 violation counts introduced within the crop. Trial:i04.ug.leaf_0003.01 demonstrates this: 68 new in-crop violations were introduced and the trial was still gated in. Do not treat a `gated_in` decision as evidence that the V4 violation count improved; inspect `n_new_in_crop` directly to assess DRC impact of any move-instance sequence.