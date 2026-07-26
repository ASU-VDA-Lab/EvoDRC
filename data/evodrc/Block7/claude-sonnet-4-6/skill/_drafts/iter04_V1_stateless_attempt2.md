## Operation Vocabulary

Every repair accepted in this layer's history applies one or more of three atomic operations — `move_instance`, `resize_end`, and `resize` — on layers M1, M2, and V1 together; a `move` on a polygon alone or an `add_polygon` on M2 also appears in a small number of cases. All 42 trials are `gated_in` with `conn_preserved: true`, so the following guidance derives exclusively from accepted, connectivity-preserving repairs.

Because V1.AUX.1 requires V1 to lie inside both M1 and M2, and V1.M2.AUX.2 requires V1 to match M2 width in the direction perpendicular to M2 length, every trial that touches V1 simultaneously lists M1 and M2 in `touched_layers`. Never move a V1-carrying instance without co-moving or co-resizing the M2 segment that covers it; this constraint is reflected in every trial in this record (trial:i01.ug.Block7_union_row10.00, trial:i01.ug.Block7_union_row13.03, trial:i02.ug.Block7_union_row9.06, and all others).

## Primary Repair Primitive: X-Direction Instance Move

The dominant repair pattern is a positive x-direction `move_instance` of one or more instances, frequently at 36 dbu increments. Trials at 36 dbu x-delta: trial:i01.ug.Block7_union_row11.01, trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row6.18, trial:i01.ug.Block7_union_row9.21, trial:i02.ug.Block7_union_row12.01, trial:i02.ug.Block7_union_row13.02, trial:i03.ug.Block7_union_row13.01, trial:i03.ug.Block7_union_row20.02. Larger moves (40, 52, 56, 68, 72, 108, 136 dbu) are used when a single 36 dbu step is insufficient to clear a spacing rule (trial:i01.ug.Block7_union_row10.00 at 52 dbu, trial:i01.ug.Block7_union_row13.03 at 136 dbu, trial:i01.ug.leaf_0001.22 at 108 dbu, trial:i02.ug.Block7_union_row9.06 at 56 dbu). Negative x-direction moves are used when the violating V1 is too close on the high-x side and must be pushed toward lower x (trial:i01.ug.Block7_union_row14.04 at -36 dbu on i0519, trial:i01.ug.Block7_union_row18.08 at -72 dbu on i0428, trial:i01.ug.leaf_0024.25 at -24 and -108 dbu, trial:i04.ug.leaf_0004.03 at -56 dbu).

## M2 Resize Must Accompany Instance Moves

When an instance carrying V1 is moved in x, the M2 polygon connecting that via to its net must be resized to keep the V1 enclosed. Apply `resize_end` on the high or low x-end of the M2 polygon by an amount proportional to or slightly larger than the instance delta, so that the via remains fully enclosed and V1.M2.EN.2 (5 nm enclosure on two opposite sides, or 5 & 0 nm flush) continues to hold. This is established by trial:i01.ug.Block7_union_row10.00 (instance moved +52 dbu; p3286 high end resized +308 dbu), trial:i01.ug.Block7_union_row3.15 (instance moved -36 dbu; p3384 low end resized +56 dbu), trial:i01.ug.Block7_union_row5.17 (instances moved +36 dbu; p3737 and p3746 high ends each resized +92 dbu), trial:i02.ug.Block7_union_row9.06 (instance moved +56 dbu; p3683 high end resized +112 dbu), and trial:i01.ug.Block7_union_row24.14 (p3058 high end +136 dbu, p3635 high end +120 dbu, p3564 high end +128 dbu, each matched to their respective instance deltas).

When M2 must extend in the low-x direction, resize the low end; trial:i01.ug.Block7_union_row17.07 applies `resize_end` at the low end of p3187 (+56 dbu) while moving four instances by +36 dbu.

## M2 Polygon Addition to Restore Coverage

When no existing M2 polygon covers a displaced V1, add a new M2 polygon sized to enclose the via on at least two opposite sides per V1.M2.EN.2 and match the via width per V1.M2.AUX.2. Trial:i01.ug.Block7_union_row20.10 added polygon [[5992,22824],[5992,22896],[6048,22896],[6048,22824]] on M2 (56 x 72 dbu) alongside a -36 dbu instance move to restore enclosure after the via was left without coverage.

## Y-Direction Moves and Multi-Layer Coordination

Y-direction instance moves and polygon moves occur in a subset of trials and always co-touch V2 and M3 alongside V1 (trial:i01.ug.Block7_union_row16.06, trial:i02.ug.leaf_0014.08, trial:i01.ug.leaf_0095.26, trial:i03.ug.leaf_0011.07). When applying a y-direction fix on V1, apply the same y-delta to any co-located M2 polygon (trial:i01.ug.Block7_union_row16.06: two instances and p3516 each moved -12 dbu in y; trial:i02.ug.leaf_0014.08: two instances and p3515 each moved -12 dbu in y). The enclosure rules V1.M1.EN.1 and V1.M2.EN.2 apply along both axes; a y-shift that moves V1 relative to M1 or M2 requires verifying that the 5 nm projection enclosure is preserved on the new y-edges.

## Multi-Iteration Convergence: Revisited Units

A single repair pass does not always clear all violations in a unit. Units appearing in more than one iteration require additional ops per pass:

- **Block7_union_row13** was repaired in iterations 1, 2, and 3 (trial:i01.ug.Block7_union_row13.03, trial:i02.ug.Block7_union_row13.02, trial:i03.ug.Block7_union_row13.01). The op count decreased from 6 to 3 to 2 across passes, indicating that each pass addressed a progressively smaller residual violation set.
- **Block7_union_row20** was repaired in iterations 1, 2, and 3 (trial:i01.ug.Block7_union_row20.10, trial:i02.ug.Block7_union_row20.04, trial:i03.ug.Block7_union_row20.02), with op counts of 2, 3, 1.
- **Block7_union_row12** recurred in iterations 1 and 2 (trial:i01.ug.Block7_union_row12.02, trial:i02.ug.Block7_union_row12.01); **Block7_union_row15** recurred in iterations 1 and 2 (trial:i01.ug.Block7_union_row15.05, trial:i02.ug.Block7_union_row15.03); **leaf_0004** recurred in iterations 4 and 5 (trial:i04.ug.leaf_0004.03, trial:i05.ug.leaf_0004.03).

Apply repairs for a unit and continue to the next iteration for that unit if it remains in the violation set; do not treat one accepted pass as sufficient for convergence. The history shows Block7_union_row13 required three accepted `gated_in` passes before it stopped recurring (trial:i01.ug.Block7_union_row13.03, trial:i02.ug.Block7_union_row13.02, trial:i03.ug.Block7_union_row13.01).

## n_new_in_crop and Accepted Trade-offs

Several gated_in decisions accepted repairs that introduced new violations into the crop window (n_new_in_crop > 0). These were accepted because `conn_preserved: true` takes priority. The extreme case is trial:i04.ug.leaf_0006.05 (n_new_in_crop = 173, single -108 dbu x-move on i0235) and trial:i04.ug.leaf_0007.06 (n_new_in_crop = 48, single +48 dbu y-move on i0177). Smaller n_new_in_crop values of 1-9 are also common (trial:i01.ug.Block7_union_row13.03, trial:i01.ug.Block7_union_row19.09, trial:i01.ug.leaf_0002.23, trial:i02.ug.leaf_0017.09, trial:i02.ug.leaf_0022.10, trial:i03.ug.leaf_0008.06). These new violations become the target of subsequent iteration passes; the multi-iteration recurrence pattern above reflects this.

## Spacing Rules and the V1 Mask Geometry

V1.S.1 through V1.S.4 operate on derived mask shapes, not raw V1 polygons. The key distinction is the M2 end-cap status:

- A via with a **5 nm M2 end-cap** (wec: V1 edges that do NOT fully flush with M2 edges) contributes to `v1_wec_mask`, which is the V1 footprint extended by 5 nm in the endcap direction. The corner-to-corner Euclidean spacing for two such vias is 23 nm (V1.S.2), driven by `v1_wec_mask.space(16.4.nm, euclidian)`.
- A via **without a 5 nm M2 end-cap** (nec: fully flush with M2 on both ends) contributes to `v1_nec_mask`, extended 5 nm in each flush direction. The corner-to-corner Euclidean spacing for two such vias is 30 nm (V1.S.3), with the diagonal-only violations flagged by `v1_s3_all.not_interacting(v1_s3_proj)`.
- Mixed-cap pairs (one wec, one nec) carry a 27 nm Euclidean minimum (V1.S.4).

Because the mask geometry absorbs the end-cap, moving a V1 instance changes its wec/nec classification only if that move alters whether its edges are flush with the M2 boundary. Resize operations on M2 that change whether a V1 edge becomes flush (or not) with M2 change the applicable spacing rule for that via. All resize_end operations in this record keep V1 enclosed within the resized M2, preserving the via's wec or nec status depending on the local geometry.

## V1.M2.AUX.2: Width Match Constraint

V1.M2.AUX.2 requires the V1 width in the direction perpendicular to M2 length to exactly equal the M2 width. When M2 is routed horizontally (x-direction), the y-extent of V1 must match the y-extent of M2. Resize operations that change M2 width in the perpendicular direction are absent from the accepted repairs in this record; all accepted M2 resizes in this history extend M2 along its length (x or y, matching the via's M2 routing direction), not across its width. Do not resize the M2 width in the direction perpendicular to routing without simultaneously resizing the V1 to match; trial:i02.ug.Block7_union_row15.03 resizes p3592 in the y-direction (axis:y, op:resize, delta -96 dbu in both ends simultaneously) while the via moves, which adjusts M2 length without violating the width-match constraint.

## V1.M1.EN.1: Two-Opposite-Sides Enclosure

V1.M1.EN.1 requires M1 to enclose V1 with at least 5 nm on one pair of opposite sides and at least 2 nm on the other pair. Instance moves that shift V1 relative to M1 must not violate this. All accepted repairs in this record that include large x-moves (trial:i01.ug.Block7_union_row13.03 at 136 dbu, trial:i01.ug.Block7_union_row24.14 at 136 and 64 dbu) remain within a single M1 cell's M1 extent. When a move shifts a V1 close to an M1 boundary, verify that the projected enclosure along both axes still satisfies the 5 & 2 nm requirement; the history does not include any repair that added M1 geometry, implying the accepted moves stayed within existing M1 enclosure margins.

## Orthogonality

V1 geometry must remain orthogonal. All accepted ops in this record produce only axis-aligned moves and axis-aligned polygon endpoints. The NONORTHOGONAL check fires on any V1 edge not at 0 or 90 degrees. No repair in this record introduces diagonal edges; `resize_end` on a single axis and `move_instance` with orthogonal delta vectors are the exclusive shape-modification primitives observed (trial:i01.ug.Block7_union_row10.00 through trial:i05.ug.leaf_0004.03).