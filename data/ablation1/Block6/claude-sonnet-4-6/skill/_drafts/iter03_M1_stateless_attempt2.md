## Rule M1.W.1 — Minimum width 18 nm

No M1.W.1 violations appear in any trial's in-crop delta across all three iterations. The resize_end operations in trial:i01.ug.Block6_union_row7.03 (x-axis low end +60 dbu), trial:i01.ug.Block6_union_row8.04 (x-axis high end +36 dbu), trial:i01.ug.leaf_0015.07 (x-axis high end +48 dbu), trial:i02.ug.Block6_union_row7.00 (x-axis high end +56 dbu), trial:i02.ug.leaf_0003.02 (x-axis high end +128 dbu), trial:i02.ug.leaf_0008.05 (x-axis high end +28 dbu), and trial:i03.ug.leaf_0002.00 (x-axis high end +56 dbu) all extended M1 polygon ends without triggering M1.W.1 errors.

## Rules M1.S.1 through M1.S.6 — Spacing rules

No M1.S.1, M1.S.2, M1.S.3, M1.S.4, M1.S.5, or M1.S.6 violations appear in any trial's in-crop delta. This holds across all move_instance operations ranging from ±4 to ±128 dbu in x and ±48 dbu in y, and across all resize_end operations up to +128 dbu, across all 18 trials in the history. Rules M1.S.4 and M1.S.5 use empty result sets in the deck (`RBA::EdgePairs::new`) and produced no findings in any measured trial.

## Rule M1.A.1 — Minimum M1 area 504 nm²

M1.A.1 is one of the two dominant M1 violations produced by large-scope multi-instance displacement operations. trial:i02.ug.leaf_0010.07 reported 28 new M1.A.1 violations in crop after applying five move_instance operations (i0361 [+4,0], i0239 [+4,0], i0112 [-28,0], i0015 [0,-40], i0471 [0,-40]) across a locus spanning 1728–15336 dbu in x and 3148–14608 dbu in y. trial:i03.ug.leaf_0004.02, evaluating the same large locus in the subsequent design state, reported 27 new M1.A.1 violations within crop; its submitted op (move i0015 [+36,-48]) was dropped as an external_duplicate already claimed by trial:i03.ug.leaf_0002.00.

Across the trials that paired resize_end with move_instance — trial:i02.ug.leaf_0008.05 (x-axis high end +28 dbu on p1923, alongside grouped move of i0213) and trial:i03.ug.leaf_0002.00 (x-axis high end +56 dbu on p1991, alongside move of i0015 [+36,-48]) — in-crop M1.A.1 counts were zero and zero respectively. The large-locus trials that used only move_instance without resize_end (trial:i02.ug.leaf_0010.07, trial:i03.ug.leaf_0004.02) accumulated the bulk of M1.A.1 findings.

## Rule V0.M1.EN.1 — Minimum enclosure of V0 by M1 (5 & 5 nm or 5 & 0 nm)

No V0.M1.EN.1 violations appear in any trial's in-crop delta across all three iterations. All trials touch M1 (every record lists M1 in touched_layers), but no measured operation produced a V0-by-M1 enclosure failure.

## Rule V0.M1.AUX.3 — V0 width must exactly match M1 width perpendicular to M1 length

No V0.M1.AUX.3 violations appear in any trial's in-crop delta across all three iterations.

## Rule V1.M1.EN.1 — Minimum enclosure of V1 by M1 (5 & 2 nm on opposite sides)

V1.M1.EN.1 is the highest-count M1 violation in the history. trial:i02.ug.leaf_0010.07 introduced 38 new V1.M1.EN.1 violations after applying five move_instance operations (i0361 [+4,0], i0239 [+4,0], i0112 [-28,0], i0015 [0,-40], i0471 [0,-40]) across the full-design locus. trial:i03.ug.leaf_0004.02 introduced 39 new V1.M1.EN.1 violations in the same large locus in the subsequent design state; its only submitted op was dropped as an external_duplicate of trial:i03.ug.leaf_0002.00's claimed move.

trial:i03.ug.leaf_0002.00 — operating on the smaller locus [4244,6588,12316,7596] and combining move of i0015 [+36,-48] with resize_end on p1991 (x-axis high end, +56 dbu) — produced only 1 new in-crop violation total across all rules, with no V1.M1.EN.1 reported. The earlier trials that also paired resize_end with move_instance — trial:i01.ug.Block6_union_row7.03 (x-axis low +60 dbu on p1920), trial:i01.ug.Block6_union_row8.04 (x-axis high +36 dbu on p1907), trial:i01.ug.leaf_0015.07 (x-axis high +48 dbu on p1923), trial:i02.ug.Block6_union_row7.00 (x-axis high +56 dbu on p1903), trial:i02.ug.leaf_0003.02 (x-axis high +128 dbu on p2020), trial:i02.ug.leaf_0008.05 (x-axis high +28 dbu on p1923) — each reported zero new in-crop violations of any rule. resize_end on M1 polygon x-axis ends is present in every trial that combined such an operation with a move_instance, and all of these trials were accepted (decision="gated_in") with n_new_in_crop at 0 in trial:i01.ug.Block6_union_row7.03, trial:i01.ug.Block6_union_row8.04, trial:i01.ug.leaf_0015.07, trial:i02.ug.Block6_union_row7.00, trial:i02.ug.leaf_0003.02, and trial:i02.ug.leaf_0008.05.

No y-axis resize_end on M1 appears in any trial in the history. All observed resize_end operations target the x-axis (axis="x"), with end values of "low" (trial:i01.ug.Block6_union_row7.03) or "high" (all remaining resize trials).

## Rule M1.R.0 — Redundant M1 island

No M1.R.0 violations appear in any trial's in-crop delta across all three iterations.

## Conflict resolution and op drops

Two inter-unit conflict patterns appear in the history, both involving instance i0015. trial:i02.ug.leaf_0004.03 had a move of i0015 [+36,-48] dropped due to external_conflict with leaf_0010 (claimants: leaf_0004, leaf_0010); that trial still reported zero new in-crop violations using its remaining two ops (moves of i0459 [+36,0] and i0437 [+36,0]). trial:i02.ug.leaf_0010.07 had a move of i0015 [0,-40] dropped due to external_conflict with leaf_0004, yet still introduced 77 new in-crop violations from its other four move_instance ops. In iter3, trial:i03.ug.leaf_0004.02 dropped its single submitted op (move i0015 [+36,-48]) as an external_duplicate already claimed by trial:i03.ug.leaf_0002.00, resulting in no applied correction for leaf_0004's locus; the 74 new in-crop violations measured for that trial (M1.A.1: 27, M4.W.5: 2, V1.M1.EN.1: 39) are attributable to pre-existing state accumulated from iter2's large-scope moves.

When a unit's only submitted op is dropped, the unit applies no correction in that iteration, and its crop count reflects violations introduced by prior iterations rather than by the current trial's ops.

## Operation magnitude reference

move_instance x-axis deltas observed across M1-touching trials: +4 dbu (trial:i01.ug.leaf_0001.05, trial:i01.ug.leaf_0003.02), +12 dbu (trial:i01.ug.Block6_union_row7.03 on i0093), +28 dbu (trial:i01.ug.leaf_0015.07, trial:i02.ug.leaf_0008.05), +36 dbu (trial:i01.ug.Block6_union_row4.01, trial:i01.ug.Block6_union_row8.04, trial:i01.ug.leaf_0011.06, trial:i01.ug.leaf_0018.08, trial:i02.ug.leaf_0004.03, trial:i03.ug.leaf_0002.00, trial:i03.ug.leaf_0004.02), -40 dbu (trial:i01.ug.Block6_union_row7.03 on i0074), +96 dbu (trial:i02.ug.Block6_union_row7.00 on i0093), +104 dbu (trial:i02.ug.leaf_0001.01, trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0005.04). move_instance y-axis deltas: +48 dbu (trial:i01.ug.Block6_union_row3.00, trial:i01.ug.Block6_union_row5.02), -40 dbu (trial:i02.ug.leaf_0010.07), -48 dbu (trial:i03.ug.leaf_0002.00, trial:i03.ug.leaf_0004.02). resize_end x-axis deltas: +28 dbu (trial:i02.ug.leaf_0008.05), +36 dbu (trial:i01.ug.Block6_union_row8.04), +48 dbu (trial:i01.ug.leaf_0015.07), +56 dbu (trial:i02.ug.Block6_union_row7.00, trial:i03.ug.leaf_0002.00), +60 dbu (trial:i01.ug.Block6_union_row7.03), +128 dbu (trial:i02.ug.leaf_0003.02).