**Via-cell M5 enclosure repair: compound M5+V5 resize is the confirmed fix pattern**

Both applied trials in the measured history address V5.M5.EN.1 enclosure violations on via cells VIA_VIA56_2_1_66_58 and VIA_VIA56_2_2_66_58. In each case the repair consists of a `resize_via_shape` on the M5 shape inside the via cell by +248 dbu in the y-axis, paired with coordinated V5 shape moves (±132 dbu) and V5 resizes (+512 dbu each) on all V5 shapes in the same cell. This compound sequence produced net violation reductions of −2 (trial:i04.cu.def:VIA_VIA56_2_1_66_58.00) and −4 (trial:i04.cu.def:VIA_VIA56_2_2_66_58.01) in window unit:leaf_0002 without breaking connectivity. Do not attempt to fix V5.M5.EN.1 by resizing the M5 shape alone without the accompanying V5 move/resize operations; the applied trials show the two-layer compound operation is the effective unit.

For a cell containing a single V5 cut (VIA_VIA56_2_1_66_58), two V5 shape actions suffice: move shape_index=0 by −132 dbu and resize by +512 dbu, then move shape_index=1 by +132 dbu and resize by +512 dbu (trial:i04.cu.def:VIA_VIA56_2_1_66_58.00). For a cell with four V5 cuts (VIA_VIA56_2_2_66_58), apply the same pair of (move ±132, resize +512) for all four shapes (trial:i04.cu.def:VIA_VIA56_2_2_66_58.01). The V5 move sign pattern is symmetric: inner shapes move inward (−132) and outer shapes move outward (+132), centering the cuts within the enlarged M5 envelope.

**Avoid resizing flat M5 polygon geometry grouped under g_v0056_m6aux1 alongside M6 adjustments**

The only rejected trial in the history (trial:i05.cu.def:VIA_VIA56_2_1_66_58.00) attempted to resize a flat M5 polygon (polygon p1402, group g_v0056_m6aux1) by +128 dbu in the y-axis while simultaneously resizing M6 shapes in both VIA_VIA56_2_1_66_58 and VIA_VIA56_2_2_66_58. This produced a net positive delta of +5 violations across two windows (unit:leaf_0002 rose from 45→47; synth:1688,1960,13196,3440 rose from 45→48) and was rejected. Do not apply M5 polygon resizes from the g_v0056_m6aux1 group paired with M6 shape changes at this locus; the measured outcome is net harmful (trial:i05.cu.def:VIA_VIA56_2_1_66_58.00).

**M5 y-axis resize magnitude: 248 dbu confirmed; 128 dbu in a different operation mode shown harmful**

The +248 dbu y-axis M5 resize on via shapes is the only M5 change confirmed beneficial (trial:i04.cu.def:VIA_VIA56_2_1_66_58.00, trial:i04.cu.def:VIA_VIA56_2_2_66_58.01). A +128 dbu y-axis resize applied to a flat polygon rather than a via shape, in a different grouping context, produced net positive violations (trial:i05.cu.def:VIA_VIA56_2_1_66_58.00). Use +248 dbu on `resize_via_shape` operations targeting M5 within VIA56 cells; do not substitute 128 dbu or apply flat-polygon resizes expecting the same effect.

**Connectivity is preserved by the compound via repair**

Both applied trials report `conn_preserved: true`, confirming that the M5 resize_via_shape (+248 dbu y) combined with V5 move/resize operations does not break net connectivity (trial:i04.cu.def:VIA_VIA56_2_1_66_58.00, trial:i04.cu.def:VIA_VIA56_2_2_66_58.01). The rejected trial also reports `conn_preserved: true` but was rejected on violation count grounds, not connectivity grounds (trial:i05.cu.def:VIA_VIA56_2_1_66_58.00).

**Locus and scope context**

All three trials operate near locus x≈1688–1728, y≈1960–2068 in the upper-right region (x≈13168–13196). The two applied trials share locus [1728,2068,13168,13052] and affect unit:leaf_0002. The rejected trial operates from a slightly shifted locus [1688,1960,13196,13052] and additionally triggers violations in window synth:1688,1960,13196,3440. When the repair target is a via cell at locus [1728,2068,13168,13052], apply the compound via-shape resize pattern; at the adjacent locus [1688,1960,13196,13052], the M5+M6 flat-polygon approach is measured to increase violations (trial:i05.cu.def:VIA_VIA56_2_1_66_58.00).