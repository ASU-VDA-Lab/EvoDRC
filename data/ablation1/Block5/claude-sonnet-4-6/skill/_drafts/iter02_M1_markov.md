The staged files aren't accessible, but the full input was provided inline. I have everything needed to produce the updated knowledge body.

**Accepted repair operations and their scope**

All eight accepted trials across iterations 1 and 2 touch layers M1, M2, and V1 together (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.Block5_union_row6.01, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05, trial:i02.ug.Block5_union_row6.00, trial:i02.ug.leaf_0002.02). When adjusting M1, include the co-moving V1 and M2 geometry in every operation set; partial moves that shift M1 without its co-located V1 break the enclosure margin required by V0.M1.EN.1 and V1.M1.EN.1.

**X-axis instance moves: accepted quanta are 4, 36, 72, and 104 dbu**

The set of confirmed safe x-axis move deltas now spans four distinct magnitudes. A move of +4 dbu was accepted in trial:i01.ug.Block5_union_row6.01 (two instances, same direction). Moves of +36 dbu were accepted in trial:i01.ug.Block5_union_row3.00, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, and trial:i01.ug.leaf_0006.05. A move of +72 dbu on a single instance was accepted in trial:i02.ug.leaf_0002.02. Paired moves of +104 dbu on two instances simultaneously were accepted in trial:i02.ug.Block5_union_row6.00. All produced zero new in-crop and zero new out-of-crop violations.

Do not treat 36 dbu as a universal cap; use the minimum delta that closes the enclosure or spacing deficit, confirmed against adjacent M1 geometry for M1.S.1 and M1.S.2 compliance. Select the quantum based on the size of the violation gap: larger gaps measured by the enclosure shortfall on V0.M1.EN.1 or V1.M1.EN.1 have been cleared with 72 dbu and 104 dbu steps without inducing new violations.

**resize_end on the M1 high-x edge clears enclosure deficits without introducing spacing violations**

Three accepted trials extended the high-x edge of an M1 polygon via resize_end: trial:i01.ug.Block5_union_row3.00 extended polygon p967 by 36 dbu; trial:i01.ug.leaf_0001.02 extended polygon p974 by 72 dbu; trial:i02.ug.Block5_union_row6.00 extended polygon p955 by 20 dbu. All three produced zero new violations. Accepted resize_end deltas span 20, 36, and 72 dbu on the high-x axis; there is no measured lower bound below 20 dbu and no upper bound above 72 dbu in the accepted set. When a V0 or V1 enclosure margin is short on the high-x side (V0.M1.EN.1, V1.M1.EN.1), apply resize_end on the M1 high-x edge concurrently with the associated instance move rather than as a separate pass. Use the minimum extension that satisfies the 5 nm enclosure requirement and confirm the resulting edge does not push into a spacing violation with adjacent M1 geometry.

**Connectivity preservation is a hard prerequisite**

All eight accepted trials report conn_preserved: true, and all eight produced zero new violations inside and outside the crop region (trial:i01.ug.Block5_union_row3.00 through trial:i02.ug.leaf_0002.02). The gating logic rejects operations that break connectivity before DRC scoring is reached, so never apply an operation set that disconnects a net; such moves cannot produce a gated_in outcome regardless of their geometric effect on M1.

**Multi-instance coordinated moves and single-instance moves**

Four accepted trials moved two instances simultaneously within the same locus: trial:i01.ug.Block5_union_row3.00 moved i0117 and i0131 both +36 dbu in x; trial:i01.ug.Block5_union_row6.01 moved i0025 and i0019 both +4 dbu in x; trial:i01.ug.leaf_0002.03 moved i0056 +36 dbu and i0103 -36 dbu; trial:i02.ug.Block5_union_row6.00 moved i0025 and i0019 both +104 dbu in x. Single-instance moves were also accepted in trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05, and trial:i02.ug.leaf_0002.02 (i0017, +72 dbu). Use paired moves—same direction to shift a sub-block, opposite directions to widen an internal gap—when the M1 spacing or enclosure violation involves two adjacent metal runs; a single-instance move is sufficient when only one side of the constraint is active.

**Combined move-plus-resize_end is accepted for the Block5_union_row6 locus**

trial:i02.ug.Block5_union_row6.00 combined two instance moves of +104 dbu with a resize_end of +20 dbu on p955 in a single three-operation set, producing zero new violations. This confirms that mixing instance moves and polygon edge extensions in a single operation set is safe when all three ops share the same directional axis (x, high-end) and the resize target is co-located with the moved instances in the same locus.

**No y-axis moves appear in the accepted set**

All accepted operation deltas are of the form [±n, 0] with zero y-component, and no y-axis resize_end operations are present across all eight accepted trials (trial:i01.ug.Block5_union_row3.00 through trial:i02.ug.leaf_0002.02). Confine repair moves to the x-axis; x-axis repositioning adjusts tip-to-side and tip-to-tip geometry governed by M1.S.2 and M1.S.3 while preserving the vertical track alignment that M1.W.1 minimum-width compliance depends on.