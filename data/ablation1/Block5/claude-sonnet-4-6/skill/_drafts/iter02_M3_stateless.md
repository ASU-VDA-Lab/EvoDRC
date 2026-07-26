## Via enclosure fixes on M3: positive y-resize in coordinated chain succeeds; negative resize fails

The only cu_pool operation on M3 that was applied in this history targeted cell VIA_VIA34_1_2_58_52. The fix grew the M3 via shape by +48 dbu on the y-axis, grouped under label "chain_fix" alongside simultaneous y-resizes of V3 (two shapes, +88 dbu each) and M4/V4 shapes (trial:i01.cu.def:VIA_VIA34_1_2_58_52.00). Net violation count across both affected windows dropped by 13. V3.M3.EN.1 requires at least 5 nm enclosure of V3 by M3 on two opposite sides; V2.M3.EN.2 requires 5+5 or 5+0 nm enclosure of V2 by M3. Enlarging the M3 via shape on the enclosing axis increases the enclosure margins for whichever via it wraps, and the cross-layer chain_fix grouping ensured that the via metal shapes on adjacent layers grew in step. Do not resize only M3 while leaving via shapes unchanged: the applied fix moved all layers in the enclosure stack together (trial:i01.cu.def:VIA_VIA34_1_2_58_52.00).

## Negative y-resize of M3 via shapes is ineffective or harmful

Two separate cu_pool attempts shrinking M3 via shapes on the y-axis were both rejected. The first attempt (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00) applied a single resize_via_shape of -40 dbu to VIA_VIA23_1_3_36_36's M3 shape; delta_total was 0 (no net change), triggering rejection as "rejected_net_positive". The second attempt (trial:i02.cu.def:VIA_VIA23_1_3_36_36.01) bundled that same -40 dbu M3 shrink with an additional -112 dbu shrink of the VIA_VIA34_1_2_58_52 M3 shape (group "V2M3_corrected"), and also applied resize_end at both the low and high ends of M3 polygons p891, p892, and p893 by -32 dbu each. That bundle increased total violations by +5 and was likewise rejected. Never apply a negative y-resize to an M3 via shape in isolation or in combination with symmetric resize_end contractions on M3 polygons: the measured outcomes are zero gain (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00) and net degradation (trial:i02.cu.def:VIA_VIA23_1_3_36_36.01).

## Symmetric resize_end contraction on both ends of an M3 polygon degrades violation counts

In trial:i02.cu.def:VIA_VIA23_1_3_36_36.01, resize_end was applied to M3 polygons p891, p892, and p893 at both "low" and "high" ends simultaneously (delta_dbu -32 on each end). This shortens the polygon from both tips. Under M3.W.1 (minimum width 18 nm), M3.S.2 (tip-to-side spacing 25 nm), M3.S.3/S.4/S.5 (tip-to-tip spacings 27–31 nm depending on tip width), and M3.A.1 (minimum area 504 nm²), shortening both ends simultaneously risks violating minimum area and tightening tip-to-tip clearance simultaneously. The net result was +5 violations in that trial. Avoid bilateral resize_end contractions on M3 polygons when the polygons are already near minimum length or area.

## Unit gate accepts M3 moves and resizes that introduce small numbers of in-crop violations when connectivity is preserved

The unit_gate channel applied a +8 dbu x-axis move of M3 polygon p910 (trial:i01.ug.leaf_0010.07) despite n_new_in_crop of 3, because conn_preserved was true and n_new_out_of_crop was 0. Similarly, four M3 polygons (p894–p897) were each shrunk by -64 dbu on y (trial:i02.ug.leaf_0005.03) with conn_preserved true and n_new_in_crop of 2 (all under V1.M1.EN.1, a non-M3 rule) and n_new_out_of_crop of 0; that trial was also gated_in. The unit_gate decision therefore tolerates a small positive n_new_in_crop provided it is accompanied by zero out-of-crop growth and preserved connectivity. Note that the M3 via-shape resize that cu_pool had rejected (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00) was listed in the assemble_drops of trial:i02.ug.leaf_0005.03 under reason "cu_pool:rejected_net_positive", confirming that the unit_gate assembler discards any per-shape op that a prior cu_pool evaluation already found non-improving.

## Instance moves on the x-axis that carry M3 can clear violations without introducing new ones

Moving instances i0104 and i0061 by +8 dbu on x (trial:i02.ug.leaf_0001.01) touched layers M2, M3, and V2 and was gated_in with n_new_in_crop of 0 and n_new_out_of_crop of 0. This shows that small lateral instance translations (8 dbu on x) can resolve M3 spacing or enclosure violations in the affected locus without creating new M3 rule failures. Rules M3.S.1 (side-to-side spacing 18 nm) and M3.S.6 (corner-to-corner spacing 20 nm euclidean) are the most sensitive to lateral polygon displacement; an 8 dbu shift achieving zero new violations demonstrates that the separation budget in this locus was sufficient to absorb the move without crossing either threshold.

## M3 via shape resize direction summary from applied and rejected outcomes

| Op | Cell | Axis | Delta (dbu) | Decision | Net delta |
|---|---|---|---|---|---|
| resize_via_shape +48 (chain_fix with V3/M4/V4) | VIA_VIA34_1_2_58_52 | y | +48 | applied | -13 |
| resize_via_shape -40 (standalone) | VIA_VIA23_1_3_36_36 | y | -40 | rejected_net_positive | 0 |
| resize_via_shape -112 + -40 + resize_end bilateral -32 (V2M3_corrected) | VIA_VIA34_1_2_58_52 + VIA_VIA23_1_3_36_36 + p891–p893 | y | negative | rejected_net_positive | +5 |

Sources: trial:i01.cu.def:VIA_VIA34_1_2_58_52.00, trial:i02.cu.def:VIA_VIA23_1_3_36_36.00, trial:i02.cu.def:VIA_VIA23_1_3_36_36.01.

Apply positive y-growth to M3 via shapes only when the full enclosure chain (V3 or V2 shapes, and the adjacent metal layer) is grown in the same operation group.