**Analyzing the 6 measured records from iteration 1 and synthesizing the knowledge body.**

All six trials were `gated_in` with `conn_preserved: true` and zero new DRC violations (`n_new_in_crop: 0`, `n_new_out_of_crop: 0`). Here is the synthesized knowledge body:

---

**Repair move granularity and direction.** All accepted M2 repairs in this iteration applied instance moves exclusively along the x-axis (horizontal). The dominant step size is 36 dbu, used in five of six trials (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05). A finer 4 dbu move also resolved a violation without introducing new errors (trial:i01.ug.Block5_union_row6.01). Do not apply y-axis (vertical) moves when x-axis moves alone close the violation; no accepted trial required a vertical component.

**Counter-move pairing for spacing corrections.** Moving two instances in opposite x-directions simultaneously (one +36 dbu, one −36 dbu) preserves connectivity and produces no new violations (trial:i01.ug.leaf_0002.03). Use counter-moves when the spacing violation lies between two instances and shifting either alone would re-create a violation on the opposite side.

**resize_end combined with instance move.** When a M2 polygon endpoint must extend to match a shifted instance, apply `resize_end` on the `high` end of the x-axis together with the instance move. A 36 dbu extension accompanying a 36 dbu instance move (trial:i01.ug.Block5_union_row3.00) and a 72 dbu extension accompanying a 36 dbu instance move (trial:i01.ug.leaf_0001.02) both cleared violations with zero new DRC errors. Never leave a polygon endpoint unextended after moving the instance it must reach; both successful resize_end cases confirm the endpoint must track the instance displacement.

**Single-instance moves are sufficient for isolated violations.** A single `move_instance` op with delta_dbu [36, 0] resolved violations in two separate units without any polygon resize (trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05). Prefer the minimum number of ops; add resize_end or a counter-move only when the single move is geometrically insufficient.

**Multi-layer coordination is standard.** Every accepted fix touched layers M1, M2, and V1 together (all six trials). M2-targeted repairs must account for V1 enclosure rules (V1.M2.EN.2, V1.M2.AUX.2) and M1 geometry simultaneously; moving an instance without checking the effect on V1 enclosure and M1 spacing is not safe.

**Op count scales with locus complexity.** Accepted repairs used 1–3 ops. The 3-op repair (trial:i01.ug.Block5_union_row3.00) involved two instance moves plus one resize_end across a larger locus (3440×864 dbu). The 1-op repairs (trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05) addressed smaller, more isolated loci. Do not add extra ops beyond what the geometry requires; all six accepted trials reached zero new violations with their stated op counts.