Looking at the two measured trials in this layer's history, I'll generate the knowledge section now.

---

**Repair strategy for V4/M5 enclosure violations in VIA_VIA45 cells**

The only applied repair in this layer's history targeted `VIA_VIA45_1_2_58_58` and resolved violations in two windows (unit:leaf_0103 and unit:leaf_0104) with a combined delta of -156 (trial:i01.cu.def:VIA_VIA45_1_2_58_58.00). The winning strategy used five coordinated operations: move V4 shape 0 along x by -116 dbu, resize V4 shape 0 along x by +232 dbu, move V4 shape 1 along x by +116 dbu, resize V4 shape 1 along x by +232 dbu, then resize the shared M5 shape along x by -152 dbu. This move-then-resize pairing on each V4 instance symmetrically expands the via along x while keeping it centered, and the companion M5 x-shrink preserves the V4.M5.AUX.2 constraint (V4 must exactly match M5 width perpendicular to M5 length) and avoids creating new V4.AUX.1 failures (V4 must remain inside both M4 and M5).

**Losing single-op approach: do not use y-axis M5 shrink alone**

A competing trial for the same target resized only M5 along y by -88 dbu (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01). Although it achieved the same raw delta_total of -156, it lost the tournament against trial:i01.cu.def:VIA_VIA45_1_2_58_58.00. Do not rely on a single y-axis M5 resize as the primary repair when the x-axis multi-op sequence is available; the multi-op x-axis approach is tournament-preferred for this cell type.

**Move-resize pairing preserves enclosure rules**

V4.M4.EN.1 requires M4 to enclose V4 by at least 11 nm on two opposite sides; V4.M5.EN.2 imposes the same 11 nm two-sided enclosure by M5. When expanding V4 along x, the paired move-and-resize pattern used in trial:i01.cu.def:VIA_VIA45_1_2_58_58.00 shifts the shape center so that the expansion is symmetric (+116 on each edge), keeping both enclosing metal layers from being undercut. The simultaneous M5 x-resize of -152 dbu re-aligns the M5 boundary to satisfy V4.M5.AUX.2 without violating V4.AUX.1.

**Touched-layer scope**

Both trials in this history touched M4, M5, and V4 together (trial:i01.cu.def:VIA_VIA45_1_2_58_58.00, trial:i01.cu.def:VIA_VIA45_1_2_58_58.01). V4 repairs in VIA_VIA45 cells must account for all three layers simultaneously; adjusting V4 geometry in isolation risks breaking V4.AUX.1 or the enclosure rules without corresponding metal adjustments.

**Spacing rules: no violations recorded**

V4.W.1 (minimum width 24 nm), V4.S.1 (same-net spacing 33 nm projection), V4.S.2 (different-net spacing 33 nm projection), and V4.S.3 (corner-to-corner spacing 33 nm euclidean) did not generate any repair operations in the recorded history. The measured x-expansion of 232 dbu per V4 shape (trial:i01.cu.def:VIA_VIA45_1_2_58_58.00) must not push neighboring V4 instances closer than the 33 nm spacing thresholds; this constraint was satisfied in the applied trial but should be verified when the locus contains closely packed via arrays.