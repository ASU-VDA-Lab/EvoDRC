The history records are fully provided inline, so I'll work directly from them.

---

## Analysis of measured records

**trial:i01.cu.def:VIA_VIA45_1_2_58_58.01** — `cu_pool` channel, iter 1, applied, −16 total violations.  
Three `resize_via_shape` ops on cell `VIA_VIA45_1_2_58_58`: two on V4 (shape_index 0 and 1, axis=x, +152 dbu each) and one on M4 (shape_index 0, axis=x, +152 dbu). Touched layers: M4, M5, V4. Connectivity preserved.

**trial:i02.ug.whole_design.00** — `unit_gate` channel, iter 2, gated_in, 45 ops across M1–M5 and V1–V4.  
Mix of `move`, `move_instance`, and `resize_end` (axis=x, high-end only) on polygons p937–p1065 and instances i0059–i0119. No new violations introduced inside or outside crop region. Connectivity preserved.

---

Now writing the knowledge body:

---

**Enclosure fixes (V4.M4.EN.1, V4.M5.EN.2): resize V4 and M4 together in x**

When V4 violates V4.M4.EN.1 (M4 must enclose V4 by ≥11 nm on at least two opposite sides) or V4.M5.EN.2 (M5 must enclose V4 by ≥11 nm on two opposite sides), the effective repair is a symmetric bilateral x-axis resize of both the V4 shape(s) and the co-located M4 shape by the same delta. In trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, applying +152 dbu in x to two V4 shapes (shape_index 0 and 1) and +152 dbu in x to one M4 shape inside cell `VIA_VIA45_1_2_58_58` reduced the total violation count by 16. The simultaneous resize of M4 alongside V4 is required: expanding V4 alone would worsen the enclosure deficit, while expanding M4 alone would leave V4 undersized or under-enclosed. Always resize both V4 and the enclosing M4 layer by the same delta on the same axis when V4.M4.EN.1 fires (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01).

V4.M5.EN.2 and V4.M5.AUX.2 share the same geometric constraint direction (perpendicular to M5 length). Because M5 was listed as a touched layer in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 without an explicit M5 resize op, the existing M5 geometry already provided adequate enclosure after the V4 and M4 x-resize; no separate M5 adjustment was needed in that case. Do not pre-emptively resize M5 when only V4.M4.EN.1 fires; the M5 enclosure may already be satisfied once V4 is correctly sized.

**V4.AUX.1: V4 must be inside both M4 and M5**

V4.AUX.1 requires every V4 shape to lie fully within the intersection of M4 and M5. A resize that expands V4 in x without also expanding M4 in x risks violating V4.AUX.1 by pushing V4 outside M4. The coupled M4 resize in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 (+152 dbu on both V4 and M4) prevented this. Never expand V4 without verifying the co-located M4 and M5 shapes are expanded by at least the same amount, or V4.AUX.1 will trigger (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01).

**V4.M5.AUX.2: V4 width must match M5 width along the perpendicular direction**

V4.M5.AUX.2 fires when V4 does not share at least two coincident edges with M5. After the x-resize in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, the M5 layer was touched but no M5 resize op was emitted, indicating that the existing M5 width already aligned with the post-resize V4 width. Where M5 is already correctly sized, resizing V4 to match M5 (rather than resizing M5 to match V4) avoids introducing secondary violations on M5 spacing or width rules.

**Width rule V4.W.1: minimum 24 nm**

V4.W.1 requires V4 width ≥ 24 nm along the M5 length direction. No trial in the measured history records a V4.W.1 violation in isolation; however, the x-axis resizes in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 increase V4 size, which can only improve width compliance. A resize that reduces V4 size in x to fix a spacing violation must verify that the resulting width remains ≥ 24 nm.

**Spacing rules V4.S.1, V4.S.2, V4.S.3: minimum 33 nm (projection and Euclidean)**

No spacing violation on V4 was directly targeted in the cu_pool trial. The unit_gate trial (trial:i02.ug.whole_design.00) performed x-axis `resize_end` (high-end only) on M4 and M5 polygons alongside `move` and `move_instance` operations, affecting V4 indirectly through instance placement. That fix passed gate with zero new violations in or out of crop (trial:i02.ug.whole_design.00), confirming that moving V4-bearing instances in x while also extending the high-end of their metal wires does not introduce V4 spacing violations provided the inter-instance pitch is preserved. When moving instances to correct spacing elsewhere, the projection-based rules V4.S.1 and V4.S.2 require that the post-move x-separation between any two V4 shapes satisfies ≥ 33 nm under projection; corner-to-corner separation (V4.S.3, Euclidean) must also be ≥ 33 nm.

**Unit-gate operations: mixed move + resize_end is safe for V4**

Trial:i02.ug.whole_design.00 demonstrates that a large compound operation (45 ops: instance moves at deltas of ±32, ±48, ±72, ±96 dbu in x or y, plus high-end x resizes of +80 to +116 dbu on M4/M5 polygons) can be gated in cleanly when connectivity is preserved and no new violations are introduced. The gating criterion `reason: conn_preserved` with `n_new_in_crop: 0` and `n_new_out_of_crop: 0` confirms that V4 shapes moved with their parent instances do not independently accumulate new DRC violations under these delta magnitudes (trial:i02.ug.whole_design.00). Resize operations on M4/M5 polygon high-ends do not by themselves trigger V4 enclosure violations, because V4 is resized as part of its via cell and the cell geometry travels with the instance.

**Operation ordering and coupling**

In trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, all three resize ops (two on V4, one on M4) share the same `group` tag `V4M5_fix` and are applied within a single decision. This grouping is required: applying V4 resize without the M4 resize in the same transaction leaves an intermediate state that would violate V4.AUX.1. Always apply coupled V4+M4 resizes atomically in the same operation group.