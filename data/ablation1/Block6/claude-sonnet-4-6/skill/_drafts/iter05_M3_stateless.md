## Via Shape Resizing on M3: Ineffective for V2 Enclosure

Shrinking a V2 via shape along the y-axis by resizing the M3 layer geometry produced a delta_total of zero — no net DRC improvement — and was rejected (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00). The operation touched M2, M3, and V2, preserving connectivity, yet neither the leaf_0009 window (110 violations before and after) nor the leaf_0010 window (138 violations before and after) changed. Do not apply a single-axis y-direction resize_via_shape on M3 for a V2 via shape when the anticipated benefit targets V2.M3.EN.2 or V2.M3.AUX.2 enclosure: the measured outcome is zero delta, and the operation is rejected on that basis (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00).

## Unit-Gate Instance Moves Touching M3: Accepted Pattern

Mass move_instance operations that include M3 in their touched-layer set are accepted by the unit_gate channel when connectivity is preserved and no violations move out of crop. trial:i04.ug.leaf_0003.01 applied 24 move_instance ops (instances i0375, i0379, i0531, i0527, i0366, i0367, i0426, i0435, i0362, i0360, i0424, i0411, i0225, i0198, i0114, i0109, i0137, i0136, i0023, i0022, i0177, i0168, i0030, i0026) across M3, M4, M5, V3, and V4, fixing 68 violations in crop with zero new out-of-crop violations, and was gated_in. The subsequent iteration trial:i05.ug.leaf_0003.01 applied 18 further ops over M3, M4, M5, M6, V3, V4, and V5 — also gated_in with 68 in-crop violations resolved and zero out-of-crop — despite introducing new in-crop violations in unrelated rules (M1.A.1: 27, M4.W.5: 2, V1.M1.EN.1: 39). No M3-specific rule violations were listed in the per_rule breakdown of new violations for either accepted move (trial:i04.ug.leaf_0003.01, trial:i05.ug.leaf_0003.01).

## Assemble-Drop Interaction With M3-Touching Moves

When a unit_gate move touching M3 follows a cu_pool operation that was already applied to an overlapping layer set, the assembler drops the redundant cu_pool ops rather than re-applying them. trial:i05.ug.leaf_0003.01 records four assemble_drops, all on M5 geometry (polygon moves and via shape resizes on VIA_VIA45_1_2_58_58 and VIA_VIA56_2_2_66_58), each marked "cu_pool:applied". The M3-touching ops in that same trial proceeded without conflict. This confirms that previously applied cu_pool shape edits to layers adjacent to M3 do not block acceptance of a subsequent unit_gate move that re-touches M3 (trial:i05.ug.leaf_0003.01).

## V2.M3.EN.2 and V2.M3.AUX.2: Resize Approach Not Validated

The only cu_pool operation recorded against a V2/M3 via cell (VIA_VIA23_1_3_36_36) was rejected with zero delta. No successful resize_via_shape, polygon move, or width adjustment for M3 geometry near V2 appears in the measured history. Avoid concluding that any specific M3 geometric edit resolves V2.M3.EN.2 or V2.M3.AUX.2 enclosure violations; the only measured attempt yielded no improvement (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00).

## V3.M3.EN.1: No Direct Fix Recorded

No operation targeting V3.M3.EN.1 appears in isolation in the measured history. The unit_gate moves in trial:i04.ug.leaf_0003.01 and trial:i05.ug.leaf_0003.01 both touched V3 alongside M3, but neither trial's per_rule breakdown attributes resolved or newly introduced violations to V3.M3.EN.1. No prescriptive repair recipe for V3.M3.EN.1 is grounded in the available records.

## M3 Width, Spacing, and Area Rules: No Direct Violations Observed

The per_rule fields in the accepted trials list no new M3.W.1, M3.S.1, M3.S.2, M3.S.3, M3.S.4, M3.S.5, M3.S.6, or M3.A.1 violations resulting from any of the measured operations (trial:i04.ug.leaf_0003.01, trial:i05.ug.leaf_0003.01). The move deltas applied to instances in those trials (±24 dbu, ±32 dbu, ±16 dbu in x or y) did not trigger M3 intrinsic spacing or width violations within the reported crop windows.