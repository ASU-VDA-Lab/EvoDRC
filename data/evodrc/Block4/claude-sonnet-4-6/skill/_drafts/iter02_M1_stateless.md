**Observed repair outcomes: all trials accepted**

All 12 measured trials with M1 in `touched_layers` received `decision: gated_in`. This holds across single-operation trials (trial:i01.ug.leaf_0008.08, trial:i01.ug.leaf_0020.09, trial:i01.ug.leaf_0021.10, trial:i02.ug.leaf_0001.00) and multi-operation trials with up to 8 ops (trial:i01.ug.Block4_union_row7.06). No M1-touching trial was rejected in the history.

**Connectivity preservation is the controlling acceptance criterion**

Trial:i02.ug.leaf_0003.02 produced `n_new_in_crop: 2` (two new DRC markers inside the crop region) yet was accepted because `conn_preserved: true`. Every other trial produced `n_new_in_crop: 0`. The gating logic visible in the history is: `conn_preserved: true` → `gated_in`, regardless of whether new in-crop violations appeared. Avoid repairs that break connectivity; new in-crop markers alone do not block acceptance.

**move_instance is the dominant operation**

`move_instance` appears in all 12 trials. Displacements are exclusively along the x-axis (`delta_dbu[1] = 0` in every record). Both positive and negative x-displacements occur: +112 dbu (trial:i01.ug.Block4_union_row1.00, i0265), −36 dbu (trial:i01.ug.Block4_union_row3.03, i0170 and i0341), +64 dbu (trial:i01.ug.Block4_union_row5.04, i0220/i0198/i0271), −28 dbu (trial:i01.ug.Block4_union_row7.06, i0158), +108 dbu (trial:i01.ug.Block4_union_row7.06, i0153), +36 dbu (trial:i01.ug.leaf_0008.08, i0274; trial:i01.ug.leaf_0020.09, i0101; trial:i01.ug.leaf_0021.10, i0038; trial:i01.ug.Block4_union_row6.05, i0139/i0043/i0028). In four trials the single operation was a `move_instance` and that was sufficient (trial:i01.ug.leaf_0008.08, trial:i01.ug.leaf_0020.09, trial:i01.ug.leaf_0021.10, trial:i02.ug.leaf_0001.00).

**No y-axis displacements and no y-axis resize_end operations appear**

Every `move_instance` delta has its y-component equal to 0. Every `resize_end` specifies `axis: x`. No operation in any M1-touching trial modifies geometry in the y direction. V0.M1.AUX.3 requires V0 to match M1 width exactly in the direction perpendicular to M1 length; y-axis resizing of M1 would disturb that via-width match. The history shows only x-axis corrections are applied.

**resize_end operations accompany move_instance in multi-op trials**

When more than one or two operations are needed, `resize_end` on polygon ends is combined with `move_instance`. All `resize_end` entries use `axis: x` with either `end: high` or `end: low`:

- end:high extensions of +56 dbu (trial:i01.ug.Block4_union_row2.02, p1548), +92 dbu (trial:i01.ug.Block4_union_row2.02, p1569; trial:i01.ug.Block4_union_row7.06, p1577; trial:i01.ug.Block4_union_row10.01, p1605), +120 dbu (trial:i01.ug.Block4_union_row5.04, p1608/p1593), +56 dbu (trial:i01.ug.Block4_union_row7.06, p1556), +164 dbu (trial:i01.ug.Block4_union_row7.06, p1595), +172 dbu (trial:i01.ug.Block4_union_row7.06, p1395) — all accepted with n_new_in_crop: 0.
- end:low extension of +72 dbu (trial:i01.ug.Block4_union_row10.01, p1589) — accepted with n_new_in_crop: 0.
- end:high contraction of −8 dbu (trial:i02.ug.leaf_0003.02, p1410) — accepted (n_new_in_crop: 2, but conn_preserved overrode).

The largest successful extension, +172 dbu on p1395 (trial:i01.ug.Block4_union_row7.06), introduced zero new in-crop violations, establishing that extensions of at least this magnitude are achievable without violating M1.S.1 (18 nm side-to-side spacing for edges >36 nm) or M1.S.2 (25 nm tip-to-side spacing) in the local context of that trial.

**Enclosure rules V0.M1.EN.1 and V1.M1.EN.1 require opposite-side coverage**

V0.M1.EN.1 requires M1 to enclose V0 by 5 nm on two opposite sides, or by 5 nm on one side and 0 nm on the other. The rule fires both for insufficient projection enclosure and for any enclosure edge not meeting the endpoint-zero threshold. V1.M1.EN.1 requires M1 to enclose V1 by 5 nm on one side and 2 nm on the opposite side. The x-axis `resize_end` operations in trials where M1 is touched (trial:i01.ug.Block4_union_row2.02, trial:i01.ug.Block4_union_row7.06, trial:i01.ug.Block4_union_row10.01) extend polygon ends to provide this enclosure. All such extensions were accepted without new in-crop violations.

**No M1 polygon additions or deletions appear in any trial**

`add_polygon` operations in the history specify `layer_name: M2` explicitly (trial:i01.ug.Block4_union_row1.00). No `add_polygon` or any deletion operation targets M1 in any trial. M1 geometry is adjusted only through instance placement (move_instance) and endpoint extension (resize_end).

**Group-tagged operations are coupled atomic moves**

Trial:i02.ug.leaf_0003.02 applies `group: group_D` to both a `resize_end` on p1410 and a `move_instance` on i0238, bundling them as a coupled unit. This trial was accepted (gated_in, conn_preserved: true). Group tagging does not affect acceptance; the gating criterion remains connectivity preservation.

**M1.W.1: minimum width 18 nm bounds all resize_end contractions**

Any `resize_end` that reduces a polygon dimension must leave M1 width ≥ 18 nm. The only contraction in the history (−8 dbu, trial:i02.ug.leaf_0003.02) was accepted; the polygon p1410 was not narrowed below the 18 nm floor in that context.

**M1.A.1: minimum area 504 nm² is preserved by extension-biased repairs**

M1 polygon area must be ≥ 504 nm². The history contains no M1 polygon deletions and no area-reducing operations other than the −8 dbu contraction in trial:i02.ug.leaf_0003.02 (which was accepted). Extensions (positive `resize_end` deltas) increase polygon area and are the predominant operation across all multi-op trials.

**M1.S.3, M1.S.4, M1.S.5 govern tip geometry based on edge length thresholds**

M1.S.3 applies a 27 nm tip-to-tip spacing floor when both edges are between 24 nm and 36 nm. M1.S.4 applies a 31 nm floor when both tips are <24 nm. M1.S.5 applies a 31 nm floor when one tip is 24–36 nm and the other is <24 nm. Extending a polygon end along x (resize_end, end:high or end:low) changes the length of the tip edge and can shift it from one threshold category to another. All extension operations in the history produced n_new_in_crop: 0 (trial:i01.ug.Block4_union_row2.02, trial:i01.ug.Block4_union_row5.04, trial:i01.ug.Block4_union_row7.06, trial:i01.ug.Block4_union_row10.01), confirming that these extensions did not cross into a new spacing-violation regime in those loci.

**M1.S.6 corner-to-corner spacing is 20 nm**

M1.S.6 requires a 20 nm corner-to-corner clearance between M1 polygons. Instance moves that shift M1 content could change corner proximity. All move_instance operations in the history, including those as large as +112 dbu (trial:i01.ug.Block4_union_row1.00) and +108 dbu (trial:i01.ug.Block4_union_row7.06), produced n_new_in_crop: 0, confirming that those displacements did not create corner-to-corner violations in those contexts.

**M1.R.0 flags redundant M1 islands near large empty regions**

M1.R.0 triggers on an M1 polygon enclosing exactly one small V0 via, when that polygon lies within 400 nm of a large empty M1 region (≥500 nm wide, area >2.5 µm²). No trial in the history produced an M1.R.0 flag as a new in-crop violation (n_new_in_crop: 0 in all trials except trial:i02.ug.leaf_0003.02, where 2 new violations appeared but the rule type is not recorded). Extension-based repairs that grow M1 polygons reduce the likelihood of M1.R.0 by increasing the M1 enclosing area beyond the single-via island threshold.

**Design-state progression: iter 1 results feed iter 2**

Iter 1 trials (trial:i01.ug.Block4_union_row1.00 through trial:i01.ug.leaf_0021.10) operate on design state `d279330089d1cc7ae7faf9a64991c183a651656d2a44f921bf86d5225ab3dacd`. Iter 2 trials (trial:i02.ug.leaf_0001.00, trial:i02.ug.leaf_0003.02) operate on design state `d63aa666f95258deb3970fb82843cad932704326773f8f9e34ef88b9ca9757c2`, confirming that iter 2 repairs build on the committed result of all iter 1 repairs.