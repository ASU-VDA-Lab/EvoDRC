Now I have everything needed. The new record introduces two key changes:

1. **Contradicts** the "end=high exclusively / low edge never modified" claim — trial:i04.ug.leaf_0001.00 uses `end="low"`.
2. **Extends** the violation-producing trial set — trial:i04 also delivers 10 new violations despite adding a resize_end, so the "only trial to introduce violations" framing is now false.
3. **Strengthens** the negative-x-move danger finding — now 4 attempts, 2 failures.

**Operation Patterns**

All 14 recorded trials touch V1 together with M1 and M2 simultaneously. This is consistent with V1.AUX.1 (V1 must be inside M1 and M2) and V1.M2.AUX.2 (V1 width must match M2 width perpendicular to M2 length): moving a V1 instance without co-moving the enclosing M1 and M2 geometry risks violating both rules. Every trial in this layer's history co-moves M1, M2, and V1 in the same repair pass (trial:i01.ug.Block3_union_row1.00 through trial:i04.ug.leaf_0001.00).

All move_instance ops displace V1 in the x-direction only (y-component = 0 in every record). V1 instances travel along the M2 track direction; no y-axis displacements appear in any recorded op.

**Coordinated Move + Resize Pattern**

Nine of the fourteen trials pair each move_instance with a resize_end (axis: x, end: high) on the associated M2 polygon. In every such case the crop introduced 0 new violations and the decision was gated_in (trial:i01.ug.Block3_union_row1.00, trial:i01.ug.Block3_union_row5.02, trial:i01.ug.Block3_union_row8.03, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0008.06, trial:i01.ug.leaf_0012.08, trial:i02.ug.leaf_0002.01). The resize_end delta is not always equal to the move delta for the same polygon pair: in trial:i01.ug.Block3_union_row1.00 the move delta is 136 dbu and the resize delta on p1254 is 192 dbu; in trial:i01.ug.leaf_0012.08 the move is 72 dbu and the resize on p1256 is 108 dbu; in trial:i01.ug.leaf_0008.06 the move is 136 dbu and the resize on p1261 is 92 dbu. The asymmetric pairing adjusts M2 enclosure at the trailing edge to satisfy V1.M2.EN.2 after the shift.

trial:i04.ug.leaf_0001.00 introduces the first recorded resize_end with end="low": a -76 dbu move_instance paired with a +132 dbu resize_end (axis: x, end: low) on p1207. This trial produced 10 new violations (n_new_in_crop=10). Extending the low-x edge of M2 leftward by 132 dbu while shifting V1 leftward by 76 dbu does not mitigate the spacing violations toward the low-x V1 neighbor; the expanded v1_mask on the low-x side may worsen V1.S.1 projection distances and V1.S.2/V1.S.4 euclidean distances to that neighbor's mask. Do not treat a resize_end(end=low) as a spacing-safe companion to a negative-x move_instance.

**Pure Move_Instance Trials**

Five trials move one or more instances without any resize_end: trial:i01.ug.Block3_union_row2.01, trial:i01.ug.leaf_0006.04, trial:i01.ug.leaf_0009.07, trial:i01.ug.leaf_0013.09, trial:i02.ug.leaf_0001.00. All five produced 0 new violations and were gated_in.

**Violation-Producing Trials: Iterations 3 and 4**

Two trials in the full history introduce new violations. trial:i03.ug.leaf_0003.02 is a pure move_instance with a -36 dbu x-delta — the same delta magnitude as the successful trial:i01.ug.leaf_0013.09 (-36 dbu, 0 violations) and trial:i02.ug.leaf_0001.00 (-36 dbu, 0 violations). Despite identical delta magnitude and op type, trial:i03.ug.leaf_0003.02 introduced 10 new violations within the crop (n_new_in_crop=10). trial:i04.ug.leaf_0001.00 pairs a larger -76 dbu negative x-move with a resize_end(end=low, +132 dbu) on the same wide locus [1728,3148,11016,9812] and also produces exactly 10 new violations. The identical violation count across two distinct op sequences in the same locus and a late-iteration design state indicates that the spacing deficit in this crop is structural, not correctable by adjusting the resize_end endpoint alone.

The distinguishing factor for both failures is the locus and design state. trial:i03.ug.leaf_0003.02 and trial:i04.ug.leaf_0001.00 both operate on locus [1728,3148,11016,9812], spanning approximately 9288 dbu wide by 6664 dbu tall — substantially wider than any prior successful negative-x-move trial. trial:i01.ug.leaf_0013.09 used a locus 1352 dbu wide; trial:i02.ug.leaf_0001.00 used a locus 428 dbu wide. A larger crop encloses more V1 neighbors that a negative x-shift can approach. Design states for iterations 3 (382d59...) and 4 (f0e0dfb1...) differ from the states for iterations 1 and 2 and from each other, but both reflect accumulated geometry changes that have reduced residual spacing margins to the point where any leftward V1 displacement on this locus triggers violations under V1.S.1 (minimum projection spacing 17 nm between v1_mask edges, 18 nm on non-M2-coincident segments) or V1.S.2 (16.4 nm euclidean corner-to-corner between wec-masked pairs).

**Negative X-Moves Are High-Risk Late in Repair**

Negative x-delta move_instance ops have been attempted four times: trial:i01.ug.leaf_0013.09 (-36 dbu, 0 violations), trial:i02.ug.leaf_0001.00 (-36 dbu, 0 violations), trial:i03.ug.leaf_0003.02 (-36 dbu, 10 violations), trial:i04.ug.leaf_0001.00 (-76 dbu, 10 violations). The first two succeed because the local design state carries margin at the moved instance's x-neighbor positions. In iterations 3 and 4, accumulated geometry changes have reduced residual spacings such that any leftward shift on the wide locus [1728,3148,11016,9812] introduces violations regardless of delta magnitude or whether a resize_end is added. Do not apply negative-x-delta move_instance ops to V1-bearing units in iteration-3 or later crops without first confirming that the distance to the nearest low-x V1 neighbor exceeds all applicable V1.S.1 through V1.S.4 thresholds by more than the intended delta, and do not assume that a resize_end(end=low) corrects the resulting spacing deficit.

**Width Rule V1.W.1**

V1.W.1 requires a minimum width of 18 nm (180 dbu). No trial records any op that directly modifies V1 width. All resize_end ops modify the x-axis edge of M2, not the V1 shape itself. V1 width is implicitly preserved because V1.M2.AUX.2 constrains V1 to match M2 width perpendicular to the M2 length direction, and no trial shrinks M2 in that transverse direction. This implicit coupling has held without failure in all 14 trials (trial:i01.ug.Block3_union_row1.00 through trial:i04.ug.leaf_0001.00).

**Enclosure Rules V1.M1.EN.1 and V1.M2.EN.2**

V1.M1.EN.1 requires M1 to enclose V1 with 5 nm on one pair of opposite sides and 2 nm on the other. V1.M2.EN.2 requires M2 to enclose V1 with 5 nm and 5 nm, or 5 nm and 0 nm (flush), on opposite sides. For end=high resize_end ops, extending the high-x edge of M2 increases or preserves M2 enclosure at that edge. In trials where the end=high resize delta exceeds the move delta — for example trial:i01.ug.Block3_union_row1.00 (resize 192 vs. move 136 dbu) and trial:i01.ug.leaf_0012.08 (resize 108 vs. move 72 dbu) — the extra extension builds additional end-cap margin on the trailing (high) edge to satisfy V1.M2.EN.2's 5 nm minimum enclosure. For trial:i04.ug.leaf_0001.00, the end=low resize of +132 dbu exceeds the -76 dbu move magnitude, extending M2's low-x edge further left than V1 travels; this preserves or increases M2 enclosure at the low edge post-shift but does not prevent the 10 new spacing violations that result. In pure move_instance trials, all geometry shifts together so relative M1/M2 enclosure is unchanged, and enclosure rules remain satisfied without additional resizing (trial:i01.ug.Block3_union_row2.01, trial:i01.ug.leaf_0006.04, trial:i01.ug.leaf_0009.07).

**Spacing Rules V1.S.1 Through V1.S.4**

V1.S.1 imposes a minimum of 18 nm along the same M2 track and between aligned parallel tracks, and 27 nm between non-aligned parallel tracks, measured by projection on the v1_mask geometry. V1.S.2 requires 16.4 nm euclidean corner-to-corner spacing between instances both carrying a 5 nm M2 end-cap (wec classification). V1.S.3 requires 16.12 nm euclidean corner-to-corner between non-end-cap instances (nec classification), excluding purely projecting violations. V1.S.4 requires 17.11 nm euclidean corner-to-corner between one wec and one nec instance. All positive-x-delta move trials displace V1 away from the low-x neighbor toward the high-x neighbor; these produced 0 new violations in all 10 positive-delta cases across iterations 1 and 2 (trial:i01.ug.Block3_union_row1.00, trial:i01.ug.Block3_union_row5.02, trial:i01.ug.Block3_union_row8.03, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0008.06, trial:i01.ug.leaf_0012.08, trial:i02.ug.leaf_0002.01, and the positive-delta instances within multi-instance trials). Negative-x moves contract spacing toward the low-x neighbor; trial:i03.ug.leaf_0003.02 and trial:i04.ug.leaf_0001.00 both confirm that this contraction crosses a spacing threshold in a late-iteration design state, with 10 new violations in each case. Adding a resize_end(end=low) to the negative-x move (as in trial:i04.ug.leaf_0001.00) does not resolve these spacing violations.

**Non-Orthogonal Geometry**

The GEOMETRY.NONORTHOGONAL rule applies to V1. No recorded trial introduces any angled or diagonal V1 geometry: all move_instance ops are axis-aligned and all resize_end ops extend along a single Cartesian axis. Maintain strictly orthogonal V1 shapes in all repair ops.

**Multi-Instance Repair in a Single Crop**

trial:i01.ug.Block3_union_row8.03 applies four move+resize pairs within one crop using non-uniform per-instance deltas (move deltas of 72, 72, 72, and 108 dbu; resize deltas of 92, 128, 128, and 164 dbu across polygons p1257, p1266, p1269, and p1267) and produces 0 new violations. Non-uniform per-instance deltas within a single crop are compatible with a clean V1 outcome provided each instance satisfies spacing and enclosure constraints in its local context.

**Connectivity Preservation**

All 14 trials record conn_preserved=true and decision=gated_in. The repair channel does not commit trials that break connectivity. In trial:i03.ug.leaf_0003.02 and trial:i04.ug.leaf_0001.00, connectivity is preserved despite 10 new DRC violations in each, confirming that gated_in reflects connectivity acceptance, not DRC cleanliness. The presence of new violations in a gated_in trial means the repair loop must continue; gated_in alone does not signal a DRC-clean state.