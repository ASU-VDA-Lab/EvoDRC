**V5 via-array y-axis paired move-then-resize repair**

For a 2×2 V5 via array (cell VIA_VIA56_2_2_66_58), applying paired y-axis `move_via_shape` / `resize_via_shape` operations to all four V5 shape indices — with shapes 0 and 1 shifted −132 dbu and grown +128 dbu, and shapes 2 and 3 shifted +132 dbu and grown +128 dbu — together with a −384 dbu y-axis `resize_via_shape` on M6, reduced total DRC violations by 39 across four affected windows and preserved connectivity (trial:i02.cu.def:VIA_VIA56_2_2_66_58.01).

**Move-then-resize sequencing on the same axis**

The effective repair sequence for each V5 shape is: move first on the target axis, then resize on the same axis in the same operation batch. Applying move and resize on the same axis and same shape in the same committed op set is connectivity-safe for V5 within the cu_pool channel (trial:i02.cu.def:VIA_VIA56_2_2_66_58.01).

**Outward spread of inner and outer via rows**

In a 2×2 V5 array, moving the lower pair (shapes 0, 1) in the −y direction and the upper pair (shapes 2, 3) in the +y direction — both with a positive resize on y — spreads the array along the y-axis. This pattern simultaneously addresses V5.M5.EN.1 and V5.M6.EN.2 enclosure margins on opposite sides, and satisfies V5.S.1/V5.S.2/V5.S.3 spacing between via instances (trial:i02.cu.def:VIA_VIA56_2_2_66_58.01).

**M6 y-shrink accompanies V5 y-spread**

When V5 shapes are spread in y, M6 must be shrunk in y (−384 dbu in trial:i02.cu.def:VIA_VIA56_2_2_66_58.01) to maintain V5.M6.AUX.2 compliance: V5 width perpendicular to M6 length must exactly match M6 width on that axis. Do not spread V5 shapes in y without a corresponding reduction of M6 on the same axis.

**Window-level violation counts after repair**

After applying the y-spread repair to VIA_VIA56_2_2_66_58, per-window violation counts fell: unit:Block7_union_row21 from 6 to 5 (−1), unit:leaf_0038 from 13 to 11 (−2), unit:leaf_0045 from 426 to 408 (−18), unit:leaf_0046 from 395 to 377 (−18), for a combined reduction of 39 (trial:i02.cu.def:VIA_VIA56_2_2_66_58.01). The dominant savings come from the leaf-level windows, not the union/block-level window.

**Repair scope: 9 ops across three layers**

A complete V5 enclosure repair for a 2×2 array requires exactly 9 ops: 4 move ops (one per V5 shape on the target axis) + 4 resize ops (one per V5 shape on the same axis) + 1 M6 resize op. Fewer ops leave at least one of V5.M5.EN.1, V5.M6.EN.2, or V5.M6.AUX.2 unresolved in this configuration (trial:i02.cu.def:VIA_VIA56_2_2_66_58.01).