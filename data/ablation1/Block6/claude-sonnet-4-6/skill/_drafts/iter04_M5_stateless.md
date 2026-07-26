## V4.M5.AUX.2: Resize M5 in Y to Match V4 Perpendicular Width

Rule V4.M5.AUX.2 requires V4 to be exactly the same width as M5 along the direction perpendicular to M5's length. When a violation occurs, the repair group `v4_m5_aux2_fix` targets M5 directly with a `resize_via_shape` operation on the y-axis rather than adjusting V4. In trial:i01.cu.def:VIA_VIA45_1_2_58_58.00 a single y-axis resize of the M5 shape by −88 dbu eliminated 56 violations (−30 in leaf_0019, −26 in leaf_0020) and was applied. The fix is applied on the M5 layer within the via cell (`VIA_VIA45_1_2_58_58`), not on the V4 layer, and connectivity was preserved. This is the most productive single-operation fix observed for this rule class at iteration 1.

## V5/M5 Interaction: Y-Axis Resize of V5 Outperforms X-Axis Resize

Two competing repairs were tested for `VIA_VIA56_2_2_66_58`, both touching M5 indirectly through V5 edits. Trial:i01.cu.def:VIA_VIA56_2_2_66_58.01 attempted x-axis move-then-resize on all four V5 shapes (move ±116 dbu, resize +320 dbu each) and achieved only −16 total violations; it lost the tournament and was not applied. Trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 resized the same four V5 shapes in y by +248 dbu each under the group `v5_m6_aux2_fix`, achieving −32 total violations, and was applied. The x-axis approach delivered half the DRC reduction of the y-axis approach for this via type. When M5-related violations arise from V5/M6 via interactions, prefer y-axis resizing of V5 over x-axis move-plus-resize sequences.

## Unit-Gate Instance Moves Affect M5 Without Targeted M5 Ops

Trial:i04.ug.leaf_0003.01 moved 24 instances through the `unit_gate` channel and was gated in because connectivity was preserved (`conn_preserved: true`, `n_new_out_of_crop: 0`). M5 appears in `touched_layers` alongside M3, M4, V3, and V4, but none of the 24 operations directly target M5 geometry — all ops are `move_instance`. The gate accepted 68 new in-crop violations as a net result. Instance moves at this scale routinely affect M5 indirectly by shifting the relative positions of metal shapes and vias within the affected cells; M5 DRC violations introduced by such moves must be resolved by subsequent targeted repairs rather than by blocking the move itself.

## Repair Channel and Decision Patterns

All three cu_pool trials at iteration 1 preserved connectivity. The applied trials (trial:i01.cu.def:VIA_VIA45_1_2_58_58.00 at −56, trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 at −32) each used group-tagged resize operations; the losing trial (trial:i01.cu.def:VIA_VIA56_2_2_66_58.01 at −16) used untagged move-plus-resize pairs. Group-tagged operations (`v4_m5_aux2_fix`, `v5_m6_aux2_fix`) correlate with applied decisions in every M5-touching record so far.