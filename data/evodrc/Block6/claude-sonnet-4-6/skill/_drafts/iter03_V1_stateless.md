## Repair Operation Classes

All 13 accepted trials across iterations 1–3 use exclusively x-axis operations: `move_instance` applied to one or more cell instances, optionally combined with `resize_end` on an M2 polygon along the x-axis. No y-axis moves and no y-axis resizes appear in any trial. This reflects the orientation of V1 spacing and enclosure rules, which are evaluated along and perpendicular to M2 wire length (x-direction in this design).

## move_instance Is the Primary Repair Primitive

`move_instance` is the sole operation in six trials (trial:i01.ug.Block6_union_row3.00, trial:i01.ug.Block6_union_row8.03, trial:i01.ug.leaf_0011.05, trial:i01.ug.leaf_0018.07, trial:i02.ug.Block6_union_row7.01, trial:i03.ug.leaf_0001.00) and is always present alongside `resize_end` in the mixed trials. Applying `move_instance` alone is sufficient when the M2 polygon attached to the moved instance travels with the instance and the resulting V1 position satisfies all enclosure and spacing rules without requiring the M2 wire endpoint to be separately repositioned.

Move deltas in accepted trials range from +4 dbu (trial:i02.ug.Block6_union_row7.01) to +112 dbu (trial:i01.ug.leaf_0001.04) in the positive x direction. One negative x move of −36 dbu was applied to instance i0074 within a multi-instance operation (trial:i01.ug.Block6_union_row7.02), demonstrating that bidirectional moves within the same repair step are accepted when the net effect clears spacing violations without creating new ones.

## resize_end as a Complement to Instance Moves

Five trials combine `move_instance` with one or more `resize_end` operations on an M2 polygon (trial:i01.ug.Block6_union_row5.01, trial:i01.ug.Block6_union_row7.02, trial:i01.ug.leaf_0001.04, trial:i01.ug.leaf_0015.06, trial:i02.ug.Block6_union_row4.00). In every case the resize is on the x-axis. Both `end:"high"` and `end:"low"` are used: the high end is extended in trial:i01.ug.Block6_union_row5.01 (+92 dbu), trial:i01.ug.leaf_0001.04 (+132 dbu), trial:i01.ug.leaf_0015.06 (+48 dbu), and trial:i02.ug.Block6_union_row4.00 (+132 dbu); the low end is extended in trial:i01.ug.Block6_union_row7.02 (+56 dbu, alongside a high-end +124 dbu resize). These resizes maintain the M2 enclosure of V1 (rules V1.M2.EN.2 and V1.M2.AUX.2) after the associated instances move, preventing the M2 wire from leaving V1 exposed or violating the exact-width constraint.

## Connectivity Is Always Preserved

Every accepted trial records `conn_preserved: true` and `n_new_in_crop: 0 / n_new_out_of_crop: 0`. This holds for both single-instance single-operation repairs (trial:i03.ug.leaf_0001.00) and multi-instance multi-operation repairs touching up to five instances and two polygon resizes (trial:i01.ug.Block6_union_row5.01). The `gated_in` decision is therefore driven by the connectivity gate in all 13 cases, not by a violation-count gate. Any repair that breaks a net connection is rejected before this stage; no such rejection appears in the history.

## All Touched Layers Are M1, M2, V1 Together

Every trial lists `touched_layers: ["M1","M2","V1"]`. V1 does not move independently of its bounding metal layers. Moving a cell instance or resizing an M2 polygon always co-modifies V1 geometry, and the repair system treats M1/M2/V1 as a single co-modified group. Do not attempt to repair V1 DRC by editing V1 geometry in isolation from M1 and M2.

## Multi-Iteration Units Require Progressive Refinement

Two units recurred across multiple iterations with distinct accepted fixes each time:

- **Block6_union_row7** was repaired in iteration 1 with a four-operation fix (two moves, two resizes, trial:i01.ug.Block6_union_row7.02) and again in iteration 2 with a single small move (+4 dbu, trial:i02.ug.Block6_union_row7.01). The large first-pass move (+104 dbu for i0093) left a residual violation that required a fine correction in the next iteration.

- **Block6_union_row8** was repaired in iteration 1 with a single +36 dbu move (trial:i01.ug.Block6_union_row8.03) and again in iteration 2 with two moves (+8 dbu and +36 dbu, trial:i02.ug.Block6_union_row8.02). The second-iteration fix addressed violations introduced or exposed by the first-iteration move.

- **leaf_0001** was repaired in iteration 1 with a +112 dbu move plus a +132 dbu high-end resize (trial:i01.ug.leaf_0001.04) and again in iteration 3 with a single +36 dbu move (trial:i03.ug.leaf_0001.00), indicating the large initial correction was followed by a late fine-tuning step after intermediate design state changes.

Apply the smallest delta that clears the violation rather than over-correcting; large initial moves in these recurring units consistently required follow-up corrections in later iterations.

## Enclosure Rules Constrain the Minimum Viable Move Magnitude

Rules V1.M1.EN.1 and V1.M2.EN.2 require M1 to enclose V1 by at least 5 nm on one side and 2 nm on the opposite side, and M2 to enclose V1 by at least 5 nm on both sides (or 5 nm on one side with flush on the other). Rule V1.M2.AUX.2 requires V1 width to exactly match M2 width perpendicular to M2 length. When moving an instance, the enclosing M2 wire must either travel with the instance or be extended via `resize_end` to maintain enclosure. In trial:i01.ug.leaf_0001.04, the instance was moved +112 dbu and the M2 polygon was extended +132 dbu at the high end, a difference of 20 dbu that represents additional enclosure margin beyond the bare minimum. In trial:i01.ug.Block6_union_row5.01, four instances moved +36 dbu while the M2 polygon was extended +92 dbu, a larger extension relative to the instance shift, reflecting a wider spacing violation requiring more M2 material to maintain enclosure at both V1 ends.

## Spacing Rule Implications for Move Direction

Rules V1.S.1 through V1.S.4 enforce minimum projection-based spacings of 17–18 nm and euclidean corner-to-corner spacings of 23–30 nm depending on end-cap configuration. All accepted instance moves in this history are in the positive x direction (except the single −36 dbu move in trial:i01.ug.Block6_union_row7.02 that separated a pair of vias). This indicates the dominant violation class in Block6 involves V1 instances that are too close in the positive-x direction and are repaired by moving one or more instances away from their neighbors. The −36 dbu move on i0074 in trial:i01.ug.Block6_union_row7.02 was applied concurrently with a +104 dbu move on i0093, a bidirectional split that increases the separation between two V1 groups; both moves together cleared the spacing rules without creating new violations.

## Non-Orthogonal Geometry Is Never Introduced

The NONORTHOGONAL rule applies to all layers including V1. Every operation in the history is a rectilinear x-axis move or x-axis polygon end resize, producing only axis-aligned geometry. Maintain this constraint: do not introduce diagonal edges on any layer during V1 repair.