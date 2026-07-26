## Effective Repair Patterns

Both applied trials in this layer's history operate on the y-axis and target V5 enclosure deficiency inside M5, consistent with rule V5.M5.EN.1 (minimum 11 nm enclosure by M5 on at least two opposite sides). The canonical per-shape repair sequence is: **move V5 shape on y by ±132 dbu, then resize V5 shape on y by +512 dbu**. M5 is simultaneously resized by +248 dbu on y (applied once per cell at shape_index 0) to preserve V5.AUX.1 containment after V5 grows. This compound sequence was applied and accepted in trial:i04.cu.def:VIA_VIA56_2_1_66_58.00 (2-shape via) and trial:i04.cu.def:VIA_VIA56_2_2_66_58.01 (4-shape via).

## Shape-Count Scaling

The repair scales directly with the number of V5 shapes in the via cell:

- **2-shape via (VIA_VIA56_2_1_...):** 5 ops total — one M5 resize and one (move + resize) pair per V5 shape. Yielded −2 violations (trial:i04.cu.def:VIA_VIA56_2_1_66_58.00).
- **4-shape via (VIA_VIA56_2_2_...):** 9 ops total — one M5 resize and one (move + resize) pair per V5 shape. Yielded −4 violations (trial:i04.cu.def:VIA_VIA56_2_2_66_58.01).

The per-pair violation reduction is consistently −2 per corrected V5 shape pair. Apply the full complement of moves to every V5 shape in the cell; partial correction (some shapes treated, others not) is not attested and the scaling law implies it would leave residual violations.

## Move Direction Convention

The y-axis move direction is antisymmetric across shapes within a cell. In all observed repairs:

- Shapes with lower indices (shapes 0 and 1 in the 4-shape cell, shape 0 in the 2-shape cell) receive a **−132 dbu** move before the resize (trial:i04.cu.def:VIA_VIA56_2_1_66_58.00, trial:i04.cu.def:VIA_VIA56_2_2_66_58.01).
- Shapes with higher indices (shapes 2 and 3 in the 4-shape cell, shape 1 in the 2-shape cell) receive a **+132 dbu** move before the resize (trial:i04.cu.def:VIA_VIA56_2_1_66_58.00, trial:i04.cu.def:VIA_VIA56_2_2_66_58.01).

This antisymmetric displacement spreads the shapes away from their original center positions before the resize, preventing the grown shapes from overlapping each other and triggering V5.S.1 / V5.S.2 / V5.S.3 spacing violations. Never apply a uniform move direction to all shapes; trial:i04.cu.def:VIA_VIA56_2_2_66_58.01 confirms the split-direction pattern for the 4-shape case.

## M5 Resize Scope

Apply the M5 +248 dbu y-axis resize exactly once per cell at shape_index 0, regardless of how many V5 shapes exist. Both trials used a single M5 resize op (trial:i04.cu.def:VIA_VIA56_2_1_66_58.00, trial:i04.cu.def:VIA_VIA56_2_2_66_58.01). Resizing additional M5 shape indices is not attested and is unnecessary for maintaining V5.AUX.1. Oversizing M5 risks introducing new M5-layer violations outside the scope of this repair.

## Connectivity and Containment

Both trials report `conn_preserved: true`, confirming that the combined V5 resize (+512 dbu y) plus M5 resize (+248 dbu y) does not break net connectivity (trial:i04.cu.def:VIA_VIA56_2_1_66_58.00, trial:i04.cu.def:VIA_VIA56_2_2_66_58.01). Because the V5 shape grows larger than the M5 delta, the M5 resize must accompany every V5 repair to satisfy V5.AUX.1 (V5 must be inside M5 and M6). Do not apply V5 resize without the corresponding M5 resize.

## Rule Coverage Achieved

The measured repairs address violations that engage V5.M5.EN.1. No operations target the x-axis, so enclosure deficiency along x (also checked by V5.M5.EN.1's two-opposite-sides requirement) is not evidenced as a problem for these cell types. Rules V5.M6.EN.2 and V5.M6.AUX.2 are implicitly satisfied by the M6 geometry already in place — the trials touch M6 as a net participant but perform no direct M6 shape edits, and both were accepted without residual M6-rule flags (trial:i04.cu.def:VIA_VIA56_2_1_66_58.00, trial:i04.cu.def:VIA_VIA56_2_2_66_58.01).

## Locus and Applicability

Both applied trials share identical locus coordinates [1728, 2068, 13168, 13052] and the same design state hash (`ed567ea8...`), confirming they operate on distinct cells within the same region of Block4 at iteration 4. The repair is applicable to any VIA_VIA56_2_N cell exhibiting V5.M5.EN.1 violations where N encodes the shape count; scale op count as 1 M5 resize + 2×N V5 (move + resize) ops.