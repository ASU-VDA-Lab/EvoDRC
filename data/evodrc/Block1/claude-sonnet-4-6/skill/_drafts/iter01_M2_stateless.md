## Repair operations on M2 are exclusively horizontal

Every accepted unit-gate repair in this iteration displaces M2 geometry along the x-axis only. Instance moves carry `delta_dbu = [x, 0]` and polygon resize operations use `axis:x` or `edge_spec:right`. No y-direction displacement of any M2 polygon appears in any gated-in trial (trial:i01.ug.Block1_union_row1.00 through trial:i01.ug.leaf_0031.11). M2 spacing violations in this design arise between wires on the same track or adjacent tracks in the x-direction.

## Common move quanta

The most frequently observed instance-move increment is 36 dbu. Multiples of 36 — 72, 108, and 136 dbu — dominate across all row-level repairs. Smaller deltas of 8 dbu and 37 dbu appear without introducing new violations (trial:i01.ug.Block1_union_row4.04 uses 8 dbu, trial:i01.ug.Block1_union_row1.00 uses 37 dbu). Fractional moves are acceptable as long as the resulting geometry satisfies M2.W.1 (18 nm minimum width) and the applicable spacing rules; the records provide no basis for requiring grid-aligned moves.

## resize_end accompanies move_instance to maintain polygon span

When an instance is moved, the M2 polygon spanning to adjacent geometry requires a matching end resize to follow the instance. The pattern: move_instance by delta X in +x then resize_end `end:high` (right edge) by the same or larger delta (trial:i01.ug.Block1_union_row5.05, trial:i01.ug.Block1_union_row6.06, trial:i01.ug.Block1_union_row8.07). For a move in the −x direction, `end:low` extends the low-x edge to maintain span (trial:i01.ug.Block1_union_row5.05 p1305 delta:56 end:low; trial:i01.ug.Block1_union_row6.06 p1346 delta:36 end:low). The resize_end delta is not required to equal the move delta — larger values appear when the polygon must also clear a spacing constraint at its extended tip (trial:i01.ug.Block1_union_row8.07 resize_end p1388 and p1345 each delta:192 with accompanying instance moves of 136 dbu).

## All resize_end operations in accepted trials are extensions, never contractions

Every accepted trial applies non-negative resize_end deltas on M2, extending polygon ends. Extension increases area, which moves geometry away from the M2.A.1 minimum area threshold (504 nm²). The only negative-delta polygon resize in the history (p1214 delta:−4 edge_spec:right) appears exclusively in the gated-out trial:i01.ug.leaf_0034.12, which also broke connectivity. Contracting M2 polygon ends is not a validated repair strategy.

## Multi-instance coordination: move all affected row instances together

Row-level repairs move 2–5 instances simultaneously within a single trial. Trial:i01.ug.Block1_union_row5.05 moves three instances (i0294, i0433, i0313) and resizes four polygon ends in one operation; trial:i01.ug.Block1_union_row6.06 moves five instances and resizes five polygon ends. Moving all affected instances together avoids secondary spacing violations (M2.S.1, M2.S.2) that arise when only one endpoint of an M2 wire is displaced while the other remains fixed. Trials that move only one or two instances (trial:i01.ug.leaf_0004.09, trial:i01.ug.leaf_0020.10) belong to compact leaf units where a single instance encompasses the entire wire in the locus.

## Positive and negative direction moves coexist within one trial

Repairs validly combine positive and negative x-moves in the same trial. Trial:i01.ug.Block1_union_row5.05 moves i0433 by −36 dbu while moving i0294 by +136 dbu. Trial:i01.ug.Block1_union_row6.06 moves i0455 by −72 dbu alongside four positive moves. Trial:i01.ug.Block1_union_row8.07 moves i0258 by −64 dbu alongside three positive moves. All three achieved zero or one new in-crop violation. A negative move pulls an instance away from a neighbor to resolve a close spacing; the associated polygon end resize (end:low) then re-extends the wire to maintain connectivity.

## Trials introducing 1–4 new in-crop violations are accepted when connectivity is preserved

Trial:i01.ug.Block1_union_row1.00 (n_new_in_crop=4), trial:i01.ug.Block1_union_row6.06 (n_new_in_crop=1), and trial:i01.ug.leaf_0031.11 (n_new_in_crop=4) were all gated_in. The acceptance criterion is `conn_preserved:true`, not zero new violations. Small numbers of new in-crop violations are acceptable and become candidates for subsequent repair iterations. The violated limit is connectivity: once `conn_preserved:false`, the trial is unconditionally gated out regardless of DRC counts (trial:i01.ug.leaf_0034.12, gated_out, 89 new violations).

## Wide multi-layer perturbation is the critical failure mode

Trial:i01.ug.leaf_0034.12 was gated out because it broke connectivity and introduced 89 new in-crop violations. Its ops spanned M1, M2, M3, M4, V1, V2 — a six-layer perturbation involving a via shape shrink on M3 and multiple large polygon expansions. Every accepted trial in this iteration touched exactly M1, M2, and V1. Restricting the touched-layer set to {M1, M2, V1} correlates with connectivity preservation across all eleven accepted trials.

## Via shrinks on M3 do not improve M2 DRC

Trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 attempted to resolve a violation by shrinking VIA_VIA23_1_3_36_36 in the y-direction on M3 by 40 dbu. This operation also touches M2 and V2. The result was delta_total=0 — no net DRC improvement — and the trial was rejected as not net positive. Shrinking a via shape in the M3 y-dimension does not relieve M2 spacing or enclosure violations. The same via shrink operation appeared in the failed trial:i01.ug.leaf_0034.12 as the first operation and is associated with the worst outcome in this iteration.

## V1 enclosure and width matching are maintained by accepted move sizes

All accepted unit-gate trials also touch V1, consistent with M2 polygon displacements requiring maintained V1 enclosure. V1.M2.EN.2 requires 5 nm enclosure on two opposite sides; V1.M2.AUX.2 requires V1 width to match M2 width in the perpendicular direction. No V1 enclosure violation was introduced by any accepted trial. The smallest move in the accepted set is 8 dbu (trial:i01.ug.Block1_union_row4.04), which did not cause enclosure loss, indicating that M2 polygons in these units carry sufficient enclosure margin to absorb sub-36-dbu displacements.

## M2.S.7 context: polygon end extensions of ≥ 36 dbu do not create forbidden short parallel runs

M2.S.7 forbids a tip-to-tip gap of 18 nm co-located with a side-to-side spacing ≤ 32 nm when the parallel run length is < 35 nm. All accepted resize_end operations deliver end extensions of 36–192 dbu, extending polygon ends well beyond the tip-classification boundary (36 nm). Trial:i01.ug.Block1_union_row6.06 uses the minimum observed end:high resize (36 dbu on p1323) and was accepted with one new violation, but that violation is not identified as M2.S.7 in the available records. No accepted trial is documented as producing an M2.S.7 violation.

## M2.S.8 diagonal gap spacing: no violations introduced by accepted trials

M2.S.8 penalizes diagonal proximity between tip-to-tip gaps on different tracks (center-to-center < 80 nm). All accepted trials shift wires horizontally by 8–192 dbu without introducing new out-of-crop violations, and n_new_out_of_crop=0 across every trial in the history. No M2.S.8 violation appears as an outcome of any trial.