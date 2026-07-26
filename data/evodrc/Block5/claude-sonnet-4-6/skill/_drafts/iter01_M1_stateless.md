All six trials in iteration 1 share the same design state and all received decision "gated_in" with conn_preserved=true, n_new_in_crop=0, and n_new_out_of_crop=0. The operations touch layers M1, M2, and V1 together in every case. No trial in this history introduced new M1 violations or resolved existing ones within the crop region; the gating criterion was connectivity preservation alone.

**X-axis instance moves are safe when connectivity is preserved and no new violations appear in crop.**

All accepted move_instance operations are strictly x-direction (y component of delta_dbu is 0 in every record). Single-instance x moves of 36 dbu (trial:i01.ug.leaf_0001.02, trial:i01.ug.Block5_union_row3.00), 4 dbu (trial:i01.ug.leaf_0006.05), 112 dbu (trial:i01.ug.leaf_0005.04), and 108 dbu (trial:i01.ug.Block5_union_row6.01) were all accepted without introducing M1 DRC errors. Apply x-axis instance moves over this range (4–112 dbu) when connectivity is confirmed preserved; do not use y-axis moves unless independently validated, since no y-direction move appears in this history.

**Multi-instance bundles moving in the same x-direction are accepted.**

Two-instance bundles with identical delta_dbu=[36,0] applied to separate instances in the same locus were gated in without new violations (trial:i01.ug.Block5_union_row3.00, which moved i0117 and i0131 each by +36 dbu in x). Use co-directional multi-instance moves when the full bundle preserves connectivity and n_new_in_crop remains 0.

**Opposing x-direction instance moves in the same locus are accepted.**

trial:i01.ug.leaf_0002.03 moved instance i0056 by delta_dbu=[36,0] and instance i0103 by delta_dbu=[-36,0] simultaneously within locus [3520,4428,4464,6372]. Both directions were combined in a single two-op bundle and gated in with conn_preserved=true and zero new M1 violations. Apply opposing-direction moves as a bundle (not sequentially in isolation) when each move independently preserves connectivity.

**X-axis polygon resizes combined with instance moves in the same bundle are accepted.**

trial:i01.ug.Block5_union_row6.01 combined two move_instance operations (each +108 dbu in x, instances i0025 and i0019) with two resize operations on polygons p955 (axis=x, delta_dbu=256) and p971 (axis=x, delta_dbu=328). The four-op bundle was gated in with conn_preserved=true and n_new_in_crop=0. Apply x-axis polygon resize deltas in the range 256–328 dbu together with x-direction instance moves when connectivity and crop-violation counts are verified. Do not apply resize operations on the y-axis without independent validation, since no y-axis resize appears in this history.

**Every accepted M1 operation in this iteration also modifies M2 and V1.**

All six trials list touched_layers=["M1","M2","V1"]. Never modify M1 geometry in isolation from the associated V0/V1 landing context when adjusting instance placement or polygon extents along x; the repair bundle must account for V1 and M2 co-movement, as all gated-in trials confirm this co-touch pattern (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.Block5_union_row6.01, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05).

**Gating criterion: conn_preserved=true and n_new_in_crop=0 are both required.**

Every accepted trial satisfies both conditions. Do not gate in any M1 repair op that breaks connectivity or introduces new DRC violations within the crop boundary, regardless of op type or magnitude.