## V5 Co-movement With M6 During Grid Snapping

When M6 polygons are snapped to grid (group `m6_snap`), every V5 instance landing on that M6 stripe must be co-moved by the identical y-axis delta. In trial:i01.ug.whole_design.00, six M6 polygons (p3801–p3806) were each moved in y by one of {-64, -32, -16, +16, +32, +64} DBU; three V5 instances were bundled with each respective M6 polygon and received the same [0, delta_y] displacement. Applying mismatched or absent deltas to V5 would violate V5.M6.AUX.2 (V5 width must exactly equal M6 width perpendicular to M6 length) and V5.AUX.1 (V5 must lie inside both M5 and M6 simultaneously).

## Move Granularity: 16 DBU Base Step

All y-axis corrections observed in trial:i01.ug.whole_design.00 are integer multiples of 16 DBU (16, 32, 64). Do not apply sub-16-DBU V5 or M6 adjustments; such moves would not land on the manufacturing grid and would leave the snapping violation unresolved.

## Connectivity Preservation Requires Grouping V5 With M6

In trial:i01.ug.whole_design.00, `conn_preserved` is true and `n_new_in_crop` = 0, `n_new_out_of_crop` = 0. The operation was admitted (`decision: gated_in`). The six M6 stripes carried eighteen V5 instances in total (three per stripe); bundling all eighteen into the same `m6_snap` group as their parent M6 polygon was sufficient to preserve connectivity across the whole-design locus [0, 0, 30440, 30440]. Splitting V5 moves into a separate repair group from the M6 move risks introducing V5.M6.EN.2 or V5.M6.AUX.2 violations on the trailing edge of the shifted M6 stripe.

## Enclosure Rules Constrain Allowable Move Magnitude

V5.M5.EN.1 requires M5 to enclose V5 by at least 11 nm on two opposite sides; V5.M6.EN.2 requires the same from M6. After a y-axis M6 snap, the co-moved V5 inherits the same vertical offset, so the M6-side enclosure is automatically preserved. However, the M5 stripes are not part of the `m6_snap` group in trial:i01.ug.whole_design.00 (touched_layers includes M5 but none of the 24 ops modify M5 polygons directly). This means the M5 enclosure margin must already be sufficient to absorb the largest applied delta (64 DBU) before the snap is applied; a snap magnitude exceeding the available M5 enclosure slack would introduce a V5.M5.EN.1 violation. Always verify remaining M5 enclosure slack before choosing a snap delta.

## Spacing Rules Are Not Perturbed by Pure Translation

V5.S.1, V5.S.2, and V5.S.3 all enforce a 33 nm minimum spacing. A pure rigid translation of a V5 group (all instances on one M6 stripe moved together) does not change intra-stripe V5 spacing. Inter-stripe spacing changes only if two adjacent stripes move by different deltas. In trial:i01.ug.whole_design.00 the six stripes received six distinct deltas, yet `n_new_in_crop` = 0, confirming that the chosen delta set did not compress any inter-stripe V5 gap below 33 nm. Before assigning independent deltas to neighboring M6 stripes, compute the post-move projected and euclidean separations of their V5 instances against the 33 nm threshold.

## Width Rule Is Invariant to Translation

V5.W.1 (minimum width 24 nm along M6 length direction) is a property of each V5 polygon's own geometry. Translation does not alter polygon dimensions. No width violations were introduced in trial:i01.ug.whole_design.00. Width violations on V5 must be resolved by resizing V5, not by moving M6 or V5.

## Non-Orthogonal Edge Rule

The GEOMETRY.NONORTHOGONAL rule applies to V5. All moves in trial:i01.ug.whole_design.00 are axis-aligned (x=0, y=delta_y), preserving the orthogonality of all V5 edges. Never apply diagonal or rotational transforms to V5 polygons or instances.