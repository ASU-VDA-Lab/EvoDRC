**Enclosure repair: paired resize of V4 and enclosing metal**

When V4.M4.EN.1 or V4.M5.EN.2 fires, resize the V4 shape outward along the deficient axis and resize the enclosing metal layer in the same direction to preserve the 11 nm overlap on both opposite sides. In trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, two V4 shapes each received a +384 dbu x-resize while the co-located M4 shape received a +152 dbu x-resize; the combined fix reduced violations by 52 across windows leaf_0019 and leaf_0020.

**Spacing repair: symmetric spread moves on sibling V4 shapes**

To increase projection spacing between two V4 shapes in the same via cell without displacing the cell centroid, apply equal and opposite moves along the spacing axis. Trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 used −116 dbu and +116 dbu x-moves on two sibling shapes, spreading them symmetrically. This pattern directly addresses V4.S.1 (same-net, projection) and V4.S.2 (different-net, projection) without shifting either via relative to its nets.

**V4.S.3 corner-to-corner spacing**

V4.S.3 uses Euclidean measurement and fires only on via pairs that pass the 33 nm projection check but fail corner-to-corner distance. Because the projection and Euclidean thresholds are identical (33 nm), increasing projection spacing also satisfies V4.S.3 for shapes that interact at corners. The ±116 dbu symmetric spread in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 addressed all three spacing rules in a single set of moves.

**V4.AUX.1 and V4.M5.AUX.2 containment after resize**

V4.AUX.1 requires every V4 shape to reside inside both M4 and M5. V4.M5.AUX.2 requires V4 to share coincident edges with M5 on at least two sides perpendicular to M5 length. Resize the enclosing metals together with V4 to maintain these containment rules after any V4 shape growth. Trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 demonstrates this directly: M4 was resized +152 dbu in x concurrently with the +384 dbu V4 x-resizes, keeping both V4 shapes inside M4 and preserving the coincident M5 edge condition required by V4.M5.AUX.2.

**Instance-move quanta in the unit-gate channel**

Unit-gate y-displacements observed in trials touching V4 are strict multiples of 24 dbu: values of ±24, ±48, ±72, and ±96 dbu all appear in trial:i02.ug.leaf_0010.06 and trial:i03.ug.leaf_0002.01. X-displacements use smaller values: +32 and −16 dbu appear in trial:i03.ug.leaf_0003.02. Snap V4-touching instance moves to these quanta to stay on the manufacturing grid, as confirmed by the gated-in decisions in trial:i02.ug.leaf_0010.06, trial:i03.ug.leaf_0002.01, and trial:i03.ug.leaf_0003.02.

**Unit-gate gating: accepting new in-crop violations**

All three unit-gate trials introduced new violations inside the crop window (n_new_in_crop: 26, 35, and 26 for trial:i02.ug.leaf_0010.06, trial:i03.ug.leaf_0002.01, and trial:i03.ug.leaf_0003.02 respectively) while exporting zero violations outside the crop (n_new_out_of_crop=0 in all three). Accept unit-gate moves when conn_preserved=true and n_new_out_of_crop=0, as the gating logic confirmed in trial:i02.ug.leaf_0010.06, trial:i03.ug.leaf_0002.01, and trial:i03.ug.leaf_0003.02.

**Multi-layer coupling on V4 operations**

V4 repair in the cu_pool channel always co-modifies M4 and M5 alongside V4 (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01). Unit-gate moves that touch V4 also consistently involve M3, M4, and M5 (trial:i02.ug.leaf_0010.06, trial:i03.ug.leaf_0002.01). When x-adjustments propagate across the metal stack, V4 co-moves with V5 (trial:i03.ug.leaf_0003.02, touched M4, M5, M6, V4, V5). After any V4 move or resize, verify M4 and M5 enclosure rules V4.M4.EN.1 and V4.M5.EN.2, as co-modification of those layers is present in every recorded trial: trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, trial:i02.ug.leaf_0010.06, trial:i03.ug.leaf_0002.01, and trial:i03.ug.leaf_0003.02.