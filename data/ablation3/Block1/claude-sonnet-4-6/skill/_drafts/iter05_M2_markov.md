## Measured Operation Summary

Three trials in this layer's history touched M2 and were accepted; one was rejected at the cu_pool gate with zero net improvement.

**Accepted trials:**

- trial:i03.ug.whole_design.00 (iter 3): 32 instance moves at ±64 dbu in X across the whole design locus, touching M1, M2, V1. Decision: gated_in; conn_preserved=true; n_new_in_crop=0; n_new_out_of_crop=0.
- trial:i04.ug.whole_design.00 (iter 4): 7 resize_end operations on polygons in M2, M3, M4. Decision: gated_in; conn_preserved=true; n_new_in_crop=0; n_new_out_of_crop=0. One candidate op (resize_via_shape on M3 layer, -40 dbu in Y for cell VIA_VIA23_1_3_36_36) was dropped at assembly because cu_pool had already rejected it as net_positive.
- trial:i05.ug.whole_design.00 (iter 5): 16 instance moves (positive X: +36, +44, +48 dbu; negative X: −64, −72 dbu) plus 5 resize_end operations on M2 polygons (all +44 dbu at X high end), touching M1, M2, V1. Decision: gated_in; conn_preserved=true; n_new_in_crop=0; n_new_out_of_crop=0.

**Rejected trials:**

- trial:i04.cu.def:VIA_VIA23_1_3_36_36.00 (iter 4): Single op — resize_via_shape on M3 layer (VIA_VIA23_1_3_36_36), axis=y, delta=-40 dbu. Touched layers M2, M3, V2. Decision: rejected_net_positive; delta_total=0 (no change in violation count, window whole_design stayed at 122 before and after).

---

## Instance-Move Safety on M2

Whole-design instance moves at a range of X displacements introduced zero new M2 violations across all accepted trials (full 16032×16032 dbu locus):

- ±64 dbu X: 30 instances +64 dbu, 2 instances −64 dbu (trial:i03.ug.whole_design.00).
- +36, +44, +48 dbu X (positive): 2 instances at +36, 5 at +44, 7 at +48 (trial:i05.ug.whole_design.00).
- −64, −72 dbu X (negative): 1 instance at −64, 2 at −72 (trial:i05.ug.whole_design.00).

Across both accepted move trials, the confirmed safe positive X range is +36–+64 dbu and the confirmed safe negative X range is −64–−72 dbu for M2 DRC. Do not treat any of these X-axis instance displacements as inherently risky for M2 at this design density.

M2.S.1 (side-to-side 18 nm), M2.S.2 (tip-to-side 25 nm), M2.S.3/S.4/S.5 (tip-to-tip 27–31 nm), M2.S.6 (corner-to-corner 20 nm), M2.S.7, and M2.S.8 all survived both move batches without new violations (trial:i03.ug.whole_design.00, trial:i05.ug.whole_design.00).

V1.M2.EN.2 and V1.M2.AUX.2 also survived across both instance-move trials; connectivity was preserved, confirming that these X-axis moves maintained M2 polygon alignment relative to V1 vias (trial:i03.ug.whole_design.00, trial:i05.ug.whole_design.00).

---

## M2 Polygon End Extensions

Across iter 4 and iter 5, multiple M2 polygons received X-axis and Y-axis end extensions; all were accepted with zero new M2 violations.

**Iter 4 extensions** (trial:i04.ug.whole_design.00):
- p1214, p1211: +172 dbu at X high end.
- p1178: +192 dbu at X high end.
- p1216: +128 dbu at X high end.
- p1301: +48 dbu at X low end.
- p1543, p1458: +9 dbu at Y high end.

**Iter 5 extensions** (trial:i05.ug.whole_design.00):
- p1255, p1270, p1295, p1309, p1320: +44 dbu at X high end.

The confirmed clean X high-end extension range therefore spans +44 dbu through +192 dbu (trial:i04.ug.whole_design.00, trial:i05.ug.whole_design.00). A +48 dbu X low-end extension and small +9 dbu Y high-end extensions are also confirmed clean (trial:i04.ug.whole_design.00). None of these operations triggered M2.S.1, M2.S.2, M2.S.3, M2.S.4, M2.S.5, M2.S.6, M2.S.7, M2.W.1, or M2.A.1 in this design context.

Do not avoid X high-end extensions in the 44–192 dbu range for M2 polygons; the measured record confirms they are clean (trial:i04.ug.whole_design.00, trial:i05.ug.whole_design.00).

---

## V2.M2.EN.1 Interaction with Via Shrinks

Shrinking VIA_VIA23_1_3_36_36 by −40 dbu in Y on its M3 layer shape produced zero net change in total M2-touching violations (trial:i04.cu.def:VIA_VIA23_1_3_36_36.00; delta_total=0, window whole_design before=122 after=122). V2.M2.EN.1 requires M2 to enclose V2 by at least 5 nm on two opposite sides. Do not apply negative-Y via-shape resizes to VIA_VIA23_1_3_36_36 expecting M2 DRC improvement; the measured record shows no benefit (trial:i04.cu.def:VIA_VIA23_1_3_36_36.00).

This op was also dropped by the assembler in trial:i04.ug.whole_design.00, confirming that the cu_pool rejection (trial:i04.cu.def:VIA_VIA23_1_3_36_36.00) preceded assembly and the drop was consistent across both records.

---

## Rule-Coverage Gaps in Measured History

M2.S.3 (tip-to-tip 27 nm, both tips 24–36 nm), M2.S.4 (tip-to-tip 31 nm, both tips < 24 nm), M2.S.5 (tip-to-tip 31 nm, mixed), M2.S.6 (corner-to-corner 20 nm), M2.S.7 (combined tip-to-tip + side-to-side constraint), M2.S.8 (diagonal gap 80 nm), and M2.A.1 (area 504 nm²) have not been violated or individually stress-tested in any recorded trial. The only evidence for these rules is that the accepted trials (trial:i03.ug.whole_design.00, trial:i04.ug.whole_design.00, trial:i05.ug.whole_design.00) did not trigger them — which establishes that the operations performed were safe, not that the rules have slack to spare.

V1.M2.AUX.2 (V1 width must match M2 width in the direction perpendicular to M2 length) was not violated in trial:i03.ug.whole_design.00 or trial:i05.ug.whole_design.00, confirming that X-axis instance moves in the +36 to +64 dbu and −64 to −72 dbu range kept M2/V1 width relationships intact.