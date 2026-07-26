Now I have everything needed. Let me write the updated knowledge body.

**Analysis of iteration 2 record against current knowledge:**

- `trial:i02.ug.leaf_0001.00` uses `delete_instance` (i0086) + `add_via` (VIA_VIA12 at [5472,2340]) — this is a direct V1 replacement, contradicting the iter-1 claim that "no trial issued a direct V1 add_polygon, resize, or move_via_shape operation." The `add_via` is a distinct op type that directly places V1.
- i0086 was moved in iter 1 (`trial:i01.ug.leaf_0001.03`, +12 dbu); it is now deleted. The per-instance move detail is stale and must be dropped.
- Zero violations still hold across all iter-1 and iter-2 trials.
- M4 appears in `touched_layers` with no corresponding explicit op and no M4 violation — likely a traversal artifact.

**Operation patterns across iterations 1 and 2**

Iteration 1 (trials trial:i01.ug.Block2_union_row1.00 through trial:i01.ug.leaf_0013.08) modified V1 exclusively through `move_instance` operations that displaced entire cell instances along the x-axis, with displacements ranging from 12 dbu to 37 dbu. The most common displacement was 36 dbu (trial:i01.ug.Block2_union_row1.00, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0011.06, trial:i01.ug.leaf_0013.08). In every iter-1 case V1 traveled with M1 and M2 as a passenger in the same instance, keeping relative V1–M1 and V1–M2 geometry fixed.

Iteration 2 introduced a qualitatively different pattern. Trial:i02.ug.leaf_0001.00 issued four ops: `delete` of polygon p1101, `delete_instance` of i0086, `add_via` of cell VIA_VIA12 at origin [5472,2340], and `resize_end` of polygon p957 by +172 dbu on axis x at end "low." The `add_via` op directly places a V1 instance (VIA_VIA12 is the V1 via cell connecting M1 to M2) at an explicitly specified coordinate. This is the first observed case of a direct V1 instance placement op (`add_via`) rather than indirect V1 displacement via `move_instance`.

**Direct V1 replacement: delete_instance + add_via**

Trial:i02.ug.leaf_0001.00 demonstrates a delete-and-reinsert strategy for V1: the existing via instance (i0086) is removed with `delete_instance`, and a new VIA_VIA12 instance is added at [5472,2340] with `add_via`. The result was `n_new_in_crop: 0` and `n_new_out_of_crop: 0` with `conn_preserved: true` and `decision: "gated_in"`. The new V1 at [5472,2340] resides within the locus [4656,2112,5760,3132], satisfying V1.AUX.1 (V1 inside M1 ∩ M2) and V1.M2.AUX.2 (V1 width matches M2 width perpendicular to M2 length). All V1 spacing rules (V1.S.1–V1.S.4) and enclosure rules (V1.M1.EN.1, V1.M2.EN.2) were satisfied at the new placement, as no violations were recorded.

The accompanying M1/M2 ops — deleting polygon p1101 and resizing the low-x end of polygon p957 by +172 dbu — adjusted metal coverage to support the repositioned V1. This confirms that coordinated polygon deletions and end-resizes on M1/M2, when paired with a correctly placed `add_via`, satisfy V1.AUX.1, V1.M1.EN.1, and V1.M2.EN.2 simultaneously (trial:i02.ug.leaf_0001.00).

**DRC outcome: no new V1 violations across all accepted trials**

Every accepted trial in iterations 1 and 2 reported zero new in-crop or out-of-crop violations attributable to V1 rules (trial:i01.ug.Block2_union_row1.00 through trial:i01.ug.leaf_0013.08; trial:i02.ug.leaf_0001.00). Trial:i01.ug.leaf_0013.08 introduced one new in-crop hit charged to M1.A.1, not any V1 rule. All other trials recorded `n_new_in_crop: 0` and `n_new_out_of_crop: 0` for V1.

**Connectivity and gating**

All nine accepted trials across iterations 1 and 2 were accepted with `decision: "gated_in"` and `conn_preserved: true` (trial:i01.ug.Block2_union_row1.00 through trial:i01.ug.leaf_0013.08; trial:i02.ug.leaf_0001.00). Moving V1-bearing instances by 12–37 dbu on the x-axis did not break connectivity in any iter-1 case. Deleting a V1 instance (i0086) and inserting a replacement VIA_VIA12 at [5472,2340] also preserved connectivity in trial:i02.ug.leaf_0001.00, demonstrating that the delete-and-reinsert pattern is connectivity-safe when the new via is placed at a location with valid M1/M2 overlap.

**M1 polygon edits and V1 enclosure**

Trial:i01.ug.leaf_0001.03 issued two M1-layer ops alongside a `move_instance` for i0086: a resize of polygon p1053 by +184 dbu on the x-axis, and an `add_polygon` for a new M1 rectangle at coordinates [5332,2340]–[5532,2448]. No V1 violations were introduced, confirming that extending or adding M1 coverage while moving a V1-bearing instance preserves V1.M1.EN.1 (two-sided enclosure: 5 nm on one axis, 2 nm on the other). The added M1 rectangle spans 200 dbu × 108 dbu, sufficient to fully enclose a minimum-width V1 (18 nm = 180 dbu) with enclosure margin on both axes.

Instance i0086, which was moved by that iter-1 trial, was subsequently deleted in trial:i02.ug.leaf_0001.00. In that iter-2 trial, polygon p1101 was deleted and polygon p957 was extended at its low-x end by +172 dbu, again adjusting M1/M2 coverage alongside the V1 change, with zero V1 violations resulting. The pattern across both trials is consistent: M1/M2 polygon ops that extend or adjust coverage in coordination with V1 placement changes satisfy V1.M1.EN.1, V1.M2.EN.2, V1.AUX.1, and V1.M2.AUX.2.

**touched_layers: M4 artifact**

Trial:i02.ug.leaf_0001.00 lists M4 in `touched_layers` despite no explicit M4 op in the ops array and no M4 violation in the DRC outcome. No V1 rule involves M4, and V1 results were clean. M4 appearing in `touched_layers` with no corresponding op and no violation is treated as a traversal or bookkeeping artifact with no bearing on V1 DRC (trial:i02.ug.leaf_0001.00).

**assemble_drops: cu_pool V2 ops do not affect V1**

Trial:i01.ug.leaf_0013.08 dropped five V2-layer shape operations from the cu_pool during assembly (three `resize_via_shape` and two `move_via_shape` ops on cell VIA_VIA23_1_3_36_36, all on axis x). None of those dropped ops involved V1, and V1 DRC results were clean, confirming that cu_pool-dropped V2 modifications carry no V1 side-effects in this context.

**Multi-instance moves in the same crop**

Trials involving two or three simultaneous `move_instance` ops within one locus (trial:i01.ug.Block2_union_row1.00 moved i0159 and i0152 together; trial:i01.ug.Block2_union_row3.01 moved i0103 and i0115 together; trial:i01.ug.Block2_union_row5.02 moved i0083, i0018, and i0034 together) all reported zero new V1 violations. Uniform x-axis displacement of all instances within a crop by the same delta (36 dbu in each case) preserved inter-instance V1 spacing, satisfying V1.S.1 through V1.S.4.