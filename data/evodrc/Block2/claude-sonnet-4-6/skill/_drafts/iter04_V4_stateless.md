**Via cell resize on the x-axis is an effective V4 repair strategy when paired with a matching M4 resize.**

In trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 the cu_pool channel applied `resize_via_shape` to both V4 shape_index 0 and shape_index 1 (x-axis, +152 dbu each) and simultaneously to M4 shape_index 0 (x-axis, +152 dbu) inside cell `VIA_VIA45_1_2_58_58`. This reduced the total DRC violation count by 16 across windows `unit:leaf_0012` and `unit:leaf_0013` (delta_total = −16) while preserving connectivity. The same three operations appeared as `cu_pool:applied` drops assembled into the unit_gate decision in trial:i01.ug.leaf_0012.07, confirming the cu_pool channel authored and committed them before unit_gate evaluated the broader locus.

**M5 is not co-resized when V4 and M4 are resized in the x-axis inside this via cell.**

In trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 only V4 (two shapes) and M4 (one shape) received the +152 dbu x-axis resize; M5 received no shape-level operation. Because rule V4.M5.AUX.2 constrains V4 width only in the direction perpendicular to M5's length, a resize along M5's length axis does not affect V4.M5.AUX.2 compliance. The trial was accepted without new violations, confirming that for `VIA_VIA45_1_2_58_58` the x-axis is aligned with M5's length direction, not the width direction governed by V4.M5.AUX.2.

**V4 is always touched as part of multi-layer operations; it is never moved or resized in isolation.**

Every trial that lists V4 in `touched_layers` also lists at minimum M4 and M5: trial:i01.ug.leaf_0012.07 (M3, M4, M5, V3, V4), trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 (M4, M5, V4), trial:i02.ug.leaf_0002.01 (M4, M5, V4), trial:i03.ug.leaf_0001.00 (M3, M4, M5, V3, V4), trial:i03.ug.leaf_0002.01 (M3, M4, M5, V3, V4), trial:i04.ug.leaf_0002.01 (M1, M2, M4, M5, V1, V4). This is consistent with rule V4.AUX.1 (V4 must reside inside the intersection of M4 and M5): any move or resize of V4 requires co-movement of its enclosing M4 and M5 to maintain that containment.

**Instance moves in both x and y are accepted repair vehicles for V4 violations.**

Trial:i02.ug.leaf_0002.01 moved polygon p938 and instances i0098, i0097, i0064, i0068 by +32 dbu in x (touching M4, M5, V4) and was accepted with zero new violations in either direction. Trial:i03.ug.leaf_0001.00 moved instances i0068 and i0073 by +48 dbu in y (M3, M4, M5, V3, V4) with zero new violations. Trial:i03.ug.leaf_0002.01 moved instances i0095/i0099 by +72 dbu in y and i0069/i0066 by −72 dbu in y (M3, M4, M5, V3, V4) and introduced one new in-crop violation without introducing out-of-crop violations; the decision was still gated_in with conn_preserved. Trial:i04.ug.leaf_0002.01 moved polygon p937 and instances i0099, i0111, i0061, i0066 by −64 dbu in x plus instance i0063 and polygon p1036 by +36 dbu in y (M1, M2, M4, M5, V1, V4), also gated_in with one new in-crop violation and conn_preserved. Move deltas ranging from ±32 to ±72 dbu in x and from ±36 to ±72 dbu in y have all been accepted without producing new out-of-crop violations.

**All accepted trials preserved connectivity; no trial in this layer's history was rejected.**

Across all six recorded trials (trial:i01.ug.leaf_0012.07, trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, trial:i02.ug.leaf_0002.01, trial:i03.ug.leaf_0001.00, trial:i03.ug.leaf_0002.01, trial:i04.ug.leaf_0002.01) `conn_preserved` is `true` and `decision` is either `gated_in` or `applied`. No trial was rejected. Accordingly, the repair record contains no negative examples from which contra-indications can be drawn.

**New in-crop violations introduced by unit_gate moves do not block acceptance when connectivity is preserved.**

Trial:i03.ug.leaf_0002.01 introduced one new in-crop violation and trial:i04.ug.leaf_0002.01 introduced one new in-crop violation; both were gated_in. Trial:i01.ug.leaf_0012.07 introduced two new in-crop violations (both on V1.M1.EN.1, unrelated to V4) and was also gated_in. In contrast, the cu_pool trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 reduced total violations by 16 with no new violations, representing the highest net improvement of any single operation in the history. New out-of-crop violations were zero in every trial.

**The locus [1728, 3148, 10368, 9812] recurs across iterations for unit leaf_0002.**

Trials trial:i03.ug.leaf_0002.01 and trial:i04.ug.leaf_0002.01 both target `unit_id: leaf_0002` at locus `[1728, 3148, 10368, 9812]`, operating in successive iterations (3 and 4) with different op sets. Both were accepted. This indicates that repeated repair passes on the same unit and locus are viable; the second pass on leaf_0002 (iter 4) shifted to a wider set of layers (adding M1, M2, V1) compared to the iter-3 pass (M3, M4, M5, V3, V4).