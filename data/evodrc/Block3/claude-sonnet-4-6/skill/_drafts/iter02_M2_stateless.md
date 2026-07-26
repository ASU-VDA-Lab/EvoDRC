**Repair Operation Primitives on M2**

Two primitive operations appear in every unit_gate repair that touches M2: `move_instance` (translating an entire cell instance) and `resize_end` (extending one endpoint of an M2 polygon along a given axis). All `resize_end` operations in both iter-1 and iter-2 records target the `high` end, extending polygons in the positive-X or positive-Y direction (trial:i01.ug.Block3_union_row1.00, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0012.08, trial:i02.ug.leaf_0002.01, and others). No `low`-end resizes appear in any M2-touching trial in this history.

The dominant repair axis is X. Every unit_gate trial moves instances exclusively in the X direction (delta_dbu with y=0). The sole Y-axis resize in the dataset—polygon p1159, +20 dbu in trial:i01.ug.leaf_0008.06—appeared alongside a large X-axis correction for a different polygon in the same locus.

**Paired Move-and-Resize Pattern**

When an M2 polygon endpoint must be repositioned by an amount that exceeds the instance grid step, the repair combines a `move_instance` with a `resize_end` on a polygon within that instance. The net displacement of the polygon's high end equals the sum of the move delta and the resize delta. Observed net displacements on the X high end: +328 dbu (move +136, resize +192, trial:i01.ug.Block3_union_row1.00); +92 dbu (move +36, resize +56, trial:i01.ug.leaf_0007.05); +180 dbu (move +72, resize +108, trial:i01.ug.leaf_0012.08); +232 dbu (move +104, resize +128, trial:i02.ug.leaf_0002.01). Not every move operation is paired with a resize: trial:i01.ug.Block3_union_row2.01, trial:i01.ug.leaf_0006.04, trial:i01.ug.leaf_0009.07, trial:i01.ug.leaf_0013.09, and trial:i02.ug.leaf_0001.00 apply only `move_instance` with no accompanying `resize_end`.

**Multi-Instance Coordination Within a Locus**

Several repair loci require moving multiple instances in a single trial. In trial:i01.ug.Block3_union_row1.00 three instances (i0233, i0246, i0205) each received identical +136 dbu X moves, each paired with a +192 dbu `resize_end` on their respective M2 polygons (p1254, p1270, p1255). In trial:i01.ug.Block3_union_row2.01 two instances (i0221, i0203) received identical +36 dbu X moves with no resize. In trial:i01.ug.Block3_union_row8.03 four instances received two distinct move deltas (+108 dbu for i0017 and +72 dbu for i0016, i0019, i0021) paired with four `resize_end` operations (+164, +128, +128, +92 dbu respectively). Applying different deltas to instances in the same locus, as in trial:i01.ug.Block3_union_row8.03, corrects individual M2 endpoint positions differentially within a shared repair window.

**Gating and Connectivity Preservation**

Every trial in this history carries `conn_preserved: true`. All unit_gate trials have `decision: gated_in` with `n_new_in_crop: 0` and `n_new_out_of_crop: 0`, confirming that no repair in iter 1 or iter 2 introduced new violations either inside or outside the crop window (trial:i01.ug.Block3_union_row1.00 through trial:i02.ug.leaf_0002.01). The single cu_pool trial (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00) carried `decision: applied` rather than `gated_in` and reduced violations by 27 across two windows (leaf_0018: 32→17, leaf_0019: 35→23) without breaking connectivity.

**Via Cell Parameter Repair and Indirect M2 Modification**

Trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 operated on the via cell definition `VIA_VIA23_1_3_36_36` by moving and resizing V2 shapes in X. Shape index 0 was moved −144 dbu and resized +288 dbu; shape index 1 was resized +288 dbu; shape index 2 was moved +144 dbu and resized +288 dbu. The touched layers are M2, M3, and V2, meaning M2 geometry was affected through the enclosure relationship between M2 and V2 rather than through any direct polygon edit on M2. This is the only operation in the history that modifies M2 indirectly through a cell definition.

**Inter-Iteration Corrections on the Same Instance**

Instance i0233 receives opposite-sign X moves across two iterations: +136 dbu in trial:i01.ug.Block3_union_row1.00 (iter 1, locus [6856,2268,10512,3132], group of three instances) and −36 dbu in trial:i02.ug.leaf_0001.00 (iter 2, locus [7276,2268,7704,3132], i0233 alone). The iter-2 locus is a strict sub-range of the iter-1 locus, isolating the single instance that required partial rollback. The net X displacement of i0233 after both accepted repairs is +100 dbu.

Instance i0239 required incremental correction in the same spatial region: +4 dbu in trial:i01.ug.leaf_0008.06 (iter 1, locus [9232,5508,10080,8532]) and +104 dbu in trial:i02.ug.leaf_0002.01 (iter 2, locus [9232,5508,10080,6372]), for a cumulative +108 dbu. The iter-1 move of +4 dbu is the smallest X displacement in the entire dataset; it was applied in the same locus as a large correction for instance i0047 (+136 dbu) on a different polygon. The iter-2 trial targeted i0239 independently in the vertical sub-range that retained residual violations.

**Move Step Sizes and Resize Magnitudes Observed**

X-axis instance move deltas across all unit_gate trials: −36, +4, +36, +72, +72, +104, +108, +136 dbu (distinct per-operation values, from trial:i01.ug.leaf_0013.09, trial:i01.ug.leaf_0008.06, trial:i01.ug.Block3_union_row2.01 and others, through trial:i01.ug.Block3_union_row1.00 and trial:i02.ug.leaf_0002.01). The most frequent step is 36 dbu, appearing in trial:i01.ug.Block3_union_row2.01, trial:i01.ug.Block3_union_row5.02, trial:i01.ug.leaf_0006.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0009.07, trial:i01.ug.leaf_0013.09, and trial:i02.ug.leaf_0001.00. X-axis `resize_end` deltas range from +36 dbu (trial:i01.ug.Block3_union_row5.02) to +192 dbu (trial:i01.ug.Block3_union_row1.00). All move and resize values are integer dbu with no fractional components.

**Locus Reuse and Subregion Targeting Across Iterations**

The x-range [9232,*,10080,*] appears in both iter-1 trial:i01.ug.leaf_0008.06 (y-range 5508–8532) and iter-2 trial:i02.ug.leaf_0002.01 (y-range 5508–6372). The iter-2 locus is a strict vertical sub-range of the iter-1 locus; both trials touch M1, M2, and V1. The upper sub-range [9232,6372,10080,8532] is not re-targeted in iter 2, indicating those positions were resolved by the iter-1 repair. The repeat of the lower sub-range confirms that trial:i01.ug.leaf_0008.06's +4 dbu correction for i0239 did not achieve the required M2 spacing or enclosure margin in that zone.