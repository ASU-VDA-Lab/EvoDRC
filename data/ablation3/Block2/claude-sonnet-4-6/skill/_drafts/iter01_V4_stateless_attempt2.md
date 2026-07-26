## Observed Repair Pattern

**V4 width / M4 co-resize along x-axis reduces violations.**
Trial `i01.cu.def:VIA_VIA45_1_2_58_58.01` applied three `resize_via_shape` operations to cell `VIA_VIA45_1_2_58_58`: two on layer V4 (shape indices 0 and 1, axis x, +152 dbu each) and one on layer M4 (shape index 0, axis x, +152 dbu). The repair group was `V4M5_fix`. Total V4-layer violations fell from 68 to 52 (delta −16) in a single iteration (trial `i01.cu.def:VIA_VIA45_1_2_58_58.01`).

**Both V4 shapes in the cell were resized together.** The two V4 shape indices (0 and 1) received identical x-axis deltas in the same operation batch (trial `i01.cu.def:VIA_VIA45_1_2_58_58.01`). Resizing only one shape while leaving the other unmodified was not attempted; the co-resize strategy was the one that produced the measured improvement.

**M4 must be co-resized when V4 is widened along x.** The M4 shape in `VIA_VIA45_1_2_58_58` was widened by the same +152 dbu x-axis delta applied to V4 (trial `i01.cu.def:VIA_VIA45_1_2_58_58.01`). Rule V4.M4.EN.1 requires M4 to enclose V4 by at least 11 nm on two opposite sides; widening V4 without a matching M4 resize would erode that enclosure.

**The repair targets enclosure rules, not spacing rules.** The `V4M5_fix` group name and the combination of touched layers (V4, M4, M5) in trial `i01.cu.def:VIA_VIA45_1_2_58_58.01` align with rules V4.M4.EN.1, V4.M5.EN.2, V4.M5.AUX.2, and V4.AUX.1, all of which govern enclosure or containment geometry. No measured record in this history addresses violations of V4.S.1, V4.S.2, or V4.S.3; no prescriptive guidance for spacing-motivated moves or via deletions is drawn here.

**Positive x-axis delta corrected the violation.** The signed delta was +152 dbu (expansion, not shrinkage) along x for both V4 shapes and the M4 shape (trial `i01.cu.def:VIA_VIA45_1_2_58_58.01`). The repair moved the design toward enclosure compliance, consistent with V4.M4.EN.1's 11 nm enclosure requirement on at least two opposite sides.

**Residual violations remain after one iteration.** After applying the three-operation repair, 52 violations remained (trial `i01.cu.def:VIA_VIA45_1_2_58_58.01`). The single repair pass did not fully clear the design, indicating that additional cells or shape indices carry independent violations not addressed by this operation set.