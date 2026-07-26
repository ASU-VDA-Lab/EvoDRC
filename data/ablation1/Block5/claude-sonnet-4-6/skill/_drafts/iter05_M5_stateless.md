## Horizontal End-Resize on M5 Polygons

The only direct M5 repair operation in the measured history is an asymmetric horizontal end-resize: in trial:i05.ug.leaf_0001.00 polygon p879 had its low x-end moved by 352 dbu and its high x-end moved by 32 dbu. The unit gate accepted this change (decision: gated_in) because conn_preserved=true and both n_new_in_crop and n_new_out_of_crop remained zero. This confirms that repositioning M5 polygon endpoints along the x-axis can resolve violations without introducing new ones, provided connectivity is maintained. No further M5-direct operations exist in the history to extend this conclusion.

## M5 as a Downstream Touched Layer in Via-Chain Repairs

In trial:i01.cu.def:VIA_VIA34_1_2_58_52.00, M5 appears in touched_layers despite no op targeting M5 geometry directly; all six ops in that record acted on M3, V3, M4, and V4 shapes (y-axis resize_via_shape). The fix was applied and reduced the violation count by 13 across two windows. This establishes that via-chain repairs operating below M5 (V3/M3/V4/M4) will list M5 as a touched layer — likely because the DRC engine re-checks rules such as V4.M5.EN.2 and V4.M5.AUX.2 whenever V4 is resized — without requiring any change to M5 shapes themselves. No M5-side action was needed for the repair to succeed in that case.

## Coverage Limitation

Only two trial records exist for this layer (trial:i01.cu.def:VIA_VIA34_1_2_58_52.00 and trial:i05.ug.leaf_0001.00). The measured history does not cover repairs for M5.W.1, M5.W.2, M5.W.3, M5.W.4, M5.W.5, M5.S.1, M5.S.2, M5.S.3, M5.S.4, M5.S.5, M5.AUX.1, M5.AUX.2, M5.AUX.3, M5.AUX.4, or V5.M5.EN.1 as primary targets. No prescriptive repair guidance for those rules can be grounded in current evidence.