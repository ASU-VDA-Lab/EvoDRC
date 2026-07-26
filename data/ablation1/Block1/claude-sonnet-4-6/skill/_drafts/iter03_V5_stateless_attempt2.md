## V5 Layer Repair Knowledge — Iteration 3

### Summary of measured history

Two trials exist for V5 in iteration 3. Both were rejected with net-positive violation deltas: trial:i03.cu.def:VIA_VIA45_1_2_58_58.00 produced a net delta of +16 (leaf_0007 improved by −2, leaf_0008 worsened by +18), and trial:i03.cu.def:VIA_VIA56_2_2_66_58.01 produced a net delta of +19 (leaf_0007 worsened by +20, leaf_0008 improved by −1). No trial in this layer's history was accepted.

---

### x-axis resize-and-move combinations on the V5/M5 stack

Trial:i03.cu.def:VIA_VIA45_1_2_58_58.00 applied four coordinated x-axis operations: polygon p1143 was moved +32 dbu along x, polygon p1142 was moved −16 dbu along x, and M5 via shapes were resized by −32 dbu along x in both VIA_VIA45_1_2_58_58 and VIA_VIA56_2_2_66_58. This combination touched M4, M5, M6, V4, and V5, and resulted in a net increase of 16 violations. The M5 resize operations (resize_via_shape, −32 dbu x) did not compensate for the asymmetric polygon moves, and the worsening was concentrated in leaf_0008 (+18). Do not rely on M5 x-axis shrinks to absorb asymmetric V5 x-axis displacements; trial:i03.cu.def:VIA_VIA45_1_2_58_58.00 shows that this class of operation drives leaf_0008 violations sharply upward while providing only marginal improvement elsewhere.

V5.M5.EN.1 requires at least 11 nm enclosure of V5 by M5 on two opposite sides in x. Shrinking the M5 via shape by −32 dbu along x while simultaneously moving V5 polygons in the same direction risks reducing enclosure below 11 nm on one or both sides. Trial:i03.cu.def:VIA_VIA45_1_2_58_58.00 shows that a −32 dbu M5 resize paired with asymmetric V5 moves (one polygon at +32 dbu, another at −16 dbu) worsened the overall count by 16, consistent with one or more V5.M5.EN.1 violations being introduced in leaf_0008.

V5.M6.AUX.2 requires V5 width along the direction perpendicular to M6 length to exactly match the M6 width in that direction. The x-axis resize of M5 via shapes in trial:i03.cu.def:VIA_VIA45_1_2_58_58.00 also touched M6 (via the touched_layers list including M6), so any x-axis change to the V5 or M6 shape must preserve this exact-width constraint. The rejection with +16 violations in trial:i03.cu.def:VIA_VIA45_1_2_58_58.00 is consistent with V5.M6.AUX.2 being violated when M5 is resized without a matching M6 adjustment.

---

### y-axis co-moves of V5 and M6 without M5 adjustment

Trial:i03.cu.def:VIA_VIA56_2_2_66_58.01 moved polygon p1561 +32 dbu along y and moved the M6 via shape of VIA_VIA56_2_2_66_58 +32 dbu along y. The touched layers were M5, M6, and V5, but no M5 shape was moved or resized. This trial produced a net delta of +19, with leaf_0007 worsening by +20. Avoid y-axis V5-and-M6 co-moves that omit a matching M5 adjustment; trial:i03.cu.def:VIA_VIA56_2_2_66_58.01 shows this pattern increases violations by +19, driven almost entirely by leaf_0007 (+20).

V5.AUX.1 requires every V5 instance to lie inside both M5 and M6. When p1561 and the M6 shape were displaced +32 dbu along y without moving the M5 boundary, V5 may no longer be fully enclosed by M5, directly triggering V5.AUX.1. The +20 worsening in leaf_0007 in trial:i03.cu.def:VIA_VIA56_2_2_66_58.01 is consistent with V5.AUX.1 firing for vias in that window after the y-displacement left V5 outside M5.

V5.M5.EN.1 (11 nm enclosure on two opposite sides) and V5.M6.EN.2 (11 nm enclosure by M6 on two opposite sides) both depend on maintaining enclosure margins after any translation. A +32 dbu y-move of V5 and M6 without a matching M5 y-move erodes M5 enclosure on the leading edge. Trial:i03.cu.def:VIA_VIA56_2_2_66_58.01 confirms that this class of partial y-move is net-harmful.

---

### Window-locality of violations

Both rejections show that violations are unevenly distributed across windows. In trial:i03.cu.def:VIA_VIA45_1_2_58_58.00 the net was +16 despite leaf_0007 improving by −2, because leaf_0008 worsened by +18. In trial:i03.cu.def:VIA_VIA56_2_2_66_58.01 the net was +19 despite leaf_0008 improving by −1, because leaf_0007 worsened by +20. Operations that appear locally beneficial in one window consistently produced larger damage in the adjacent window for this V5 locus. Do not accept a repair candidate based on single-window improvement; trial:i03.cu.def:VIA_VIA45_1_2_58_58.00 and trial:i03.cu.def:VIA_VIA56_2_2_66_58.01 both show cross-window degradation that dominates the net count.

---

### V5.W.1 minimum width

No trial in this history modified V5 width directly. The minimum width of 24 nm must be maintained in any resize operation. Trial:i03.cu.def:VIA_VIA45_1_2_58_58.00 resized M5 via shapes (not V5 directly) along x by −32 dbu; a −32 dbu change on M5 that implicitly narrows V5 below 24 nm would trigger V5.W.1.

---

### V5.S.1 / V5.S.2 / V5.S.3 spacing rules

The 33 nm minimum spacing rules (same-net V5.S.1, different-net V5.S.2, corner-to-corner V5.S.3) were not exercised by either trial in this history. No citation is available for these rules.