## Repair Outcomes: Iteration 3 Summary

Both recorded trials for layer V5 in iteration 3 were rejected as net-positive — each increased the total DRC violation count across their respective windows, leaving the design state unchanged at `f1b04dbd5a83f26f0f545ff5f9314c5c4ce3c88c4c844762b5ce90dcceddf86f`.

---

## Trial-by-Trial Analysis

### VIA_VIA45_1_2_58_58 — x-axis resize and move (trial:i03.cu.def:VIA_VIA45_1_2_58_58.00)

This trial targeted `VIA_VIA45_1_2_58_58` and touched layers M4, M5, M6, V4, and V5. Four operations were applied under group D:

- Move polygon `p1143` along x by +32 dbu.
- Move polygon `p1142` along x by -16 dbu.
- Resize M5 shape (index 0) inside `VIA_VIA45_1_2_58_58` along x by -32 dbu.
- Resize M5 shape (index 0) inside `VIA_VIA56_2_2_66_58` along x by -32 dbu.

Window `unit:leaf_0007` improved slightly (175 → 173, delta −2), but window `unit:leaf_0008` worsened substantially (113 → 131, delta +18), producing a net delta of +16. The trial was rejected (trial:i03.cu.def:VIA_VIA45_1_2_58_58.00).

Do not apply simultaneous x-axis shrinkage of M5 via shapes on adjacent vias VIA_VIA45_1_2_58_58 and VIA_VIA56_2_2_66_58 together with asymmetric polygon moves in the same group: trial:i03.cu.def:VIA_VIA45_1_2_58_58.00 shows this combination displaces violations into `unit:leaf_0008` far more than it relieves violations in `unit:leaf_0007`.

The large asymmetry (+18 in one window versus −2 in the other) indicates that M5 enclosure rules (V5.M5.EN.1: minimum 11 nm enclosure on two opposite sides) and the V5.M6.AUX.2 width-matching constraint are sensitive to x-axis M5 resizes when two adjacent vias share the same M5 run. Shrinking M5 shapes in x on both vias simultaneously risks violating V5.M5.EN.1 on the side where M5 overlap is already marginal, as seen in trial:i03.cu.def:VIA_VIA45_1_2_58_58.00.

### VIA_VIA56_2_2_66_58 — y-axis M6 move (trial:i03.cu.def:VIA_VIA56_2_2_66_58.01)

This trial targeted `VIA_VIA56_2_2_66_58` and touched layers M5, M6, and V5. Two operations were applied under group EF:

- Move polygon `p1561` along y by +32 dbu.
- Move M6 shape (index 0) inside `VIA_VIA56_2_2_66_58` along y by +32 dbu.

Window `unit:leaf_0007` worsened severely (175 → 195, delta +20), while `unit:leaf_0008` improved by only 1 (113 → 112), producing a net delta of +19. The trial was rejected (trial:i03.cu.def:VIA_VIA56_2_2_66_58.01).

Do not move M6 via shapes and their associated V5 polygon in the +y direction by 32 dbu on `VIA_VIA56_2_2_66_58`: trial:i03.cu.def:VIA_VIA56_2_2_66_58.01 shows this move increases violations in `unit:leaf_0007` by 20 while recovering only 1 in `unit:leaf_0008`.

Moving V5 and its enclosing M6 shape together in y without adjusting the corresponding M5 enclosure risks violating V5.AUX.1 (V5 must be inside both M5 and M6) or V5.M6.EN.2 (11 nm enclosure on two opposite sides in M6) at the leading or trailing edge of the via, as corroborated by the severe `unit:leaf_0007` increase in trial:i03.cu.def:VIA_VIA56_2_2_66_58.01. The +32 dbu y-displacement is large relative to a 24 nm minimum V5 width (V5.W.1) and the 11 nm minimum enclosure margins, making enclosure violations at the shifted edge a direct consequence of this move magnitude.

---

## Cross-Trial Patterns

### Both repairs failed; no successful repair exists in this history

All two trials recorded for V5 in iteration 3 were rejected as net-positive. No repair attempt reduced the total violation count. Every prescriptive statement below is grounded in rejections rather than confirmations.

### Net-positive rejections involve strong cross-window violation transfer

In trial:i03.cu.def:VIA_VIA45_1_2_58_58.00, the net delta was +16 despite a −2 improvement in one window. In trial:i03.cu.def:VIA_VIA56_2_2_66_58.01, the net delta was +19 despite a −1 improvement in one window. Both rejections follow the same pattern: the repair displaces violations into the neighboring window at a ratio far exceeding any local relief. Avoid any repair strategy that moves or resizes V5-adjacent shapes when the operation's geometric reach spans both `unit:leaf_0007` and `unit:leaf_0008`, unless the per-window deltas in both windows are individually verified to be non-positive.

### x-axis M5 resize on co-planar vias amplifies inter-window coupling

The four-operation group in trial:i03.cu.def:VIA_VIA45_1_2_58_58.00 resized M5 shapes on two distinct via cells (VIA_VIA45_1_2_58_58 and VIA_VIA56_2_2_66_58) in the same operation group. The resulting +18 delta in `unit:leaf_0008` substantially exceeds the −2 relief in `unit:leaf_0007`. When M5 shapes from multiple vias share or neighbor the same M5 metal segment, resizing both simultaneously in the same direction couples their enclosure margins; do not resize M5 via shapes on more than one via cell in a single operation group targeting V5 repairs (trial:i03.cu.def:VIA_VIA45_1_2_58_58.00).

### y-axis via-and-metal co-moves must include M5 adjustment to preserve V5.AUX.1

In trial:i03.cu.def:VIA_VIA56_2_2_66_58.01, moving both the V5 polygon and the M6 via shape together in y by +32 dbu without a corresponding M5 adjustment produced a net +19 delta. V5.AUX.1 requires V5 to be inside both M5 and M6. Moving V5 with M6 but not M5 breaks the M5 enclosure side that is not co-moved. Do not co-move V5 and M6 shapes in y without an equivalent M5 shape adjustment; trial:i03.cu.def:VIA_VIA56_2_2_66_58.01 confirms this produces a large net-positive outcome.

### 32 dbu move/resize magnitude exceeds safe margin for V5 rules at this geometry

Both trials used 32 dbu as the primary displacement or resize quantum. Given V5.W.1 (24 nm minimum width) and V5.M5.EN.1 / V5.M6.EN.2 (11 nm minimum two-sided enclosure), a 32 dbu move on any V5-touching shape directly threatens one or both enclosure constraints on the trailing edge. Both 32 dbu operations were rejected (trial:i03.cu.def:VIA_VIA45_1_2_58_58.00, trial:i03.cu.def:VIA_VIA56_2_2_66_58.01). Do not use 32 dbu as the repair step size for V5-adjacent move or resize operations without first verifying remaining enclosure margin on all four sides.

### V5.S.1 / V5.S.2 / V5.S.3 spacing rules are untested in this history

No trial in this iteration produced a repair that passed, and neither rejection record identifies spacing (V5.S.1, V5.S.2, V5.S.3, all 33 nm minimum) as the primary triggered rule. The rejection rationale recorded is net-positive delta count across windows, not a rule-specific annotation. No spacing-targeted repair has been attempted or confirmed in this layer's history.

### V5.M6.AUX.2 width-matching is at risk whenever M6 is resized or moved independently of V5

V5.M6.AUX.2 requires V5 to match M6 width exactly in the direction perpendicular to M6 length. In trial:i03.cu.def:VIA_VIA56_2_2_66_58.01, M6 was moved in y without any width change, and the result was rejected with a +20 violation increase in `unit:leaf_0007`. While the rejection is attributable to missing M5 co-move, any operation that changes the relative position of M6 relative to V5 without preserving the exact width match perpendicular to M6 length will trigger V5.M6.AUX.2. Always treat V5 and its enclosing M6 shape as a width-locked pair in the perpendicular direction; trial:i03.cu.def:VIA_VIA56_2_2_66_58.01 confirms that decoupled y-axis movement produces large net-positive outcomes.