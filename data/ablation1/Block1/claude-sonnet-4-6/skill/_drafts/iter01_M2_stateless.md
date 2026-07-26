## Observed Repair Operations and Outcomes

All 11 trials in this iteration were accepted (`decision: gated_in`, `conn_preserved: true`). No trial was rejected. All trials touched layers M1, M2, and V1 together. Operations on M2 are exclusively `move_instance` and `resize_end` / `resize` on M2 polygons. No out-of-crop violations were introduced in any trial.

---

## Move-Instance Patterns

**Use x-axis displacements that are multiples of 36 dbu.** The dominant move delta is +36 dbu, appearing across trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row10.01, trial:i01.ug.Block1_union_row3.03, trial:i01.ug.Block1_union_row4.04, trial:i01.ug.Block1_union_row5.05, trial:i01.ug.Block1_union_row8.07, trial:i01.ug.Block1_union_row9.08, trial:i01.ug.leaf_0004.09, trial:i01.ug.leaf_0020.10, and trial:i01.ug.leaf_0031.11. Multiples of 108 dbu (+3× grid) were also used in trial:i01.ug.Block1_union_row1.00 and trial:i01.ug.Block1_union_row8.07 without producing out-of-crop errors. Negative moves of -36 dbu appear in trial:i01.ug.Block1_union_row5.05, trial:i01.ug.Block1_union_row8.07, and trial:i01.ug.leaf_0020.10, all accepted.

**Avoid -32 dbu moves when M2 side spacing is already tight.** The single -32 dbu move (trial:i01.ug.Block1_union_row6.06, instance i0455) introduced 1 new in-crop DRC error while all other single-move trials introduced zero new errors. This trial was still accepted because conn_preserved was satisfied, but the error introduction is consistent with a -32 dbu displacement landing off the 36 dbu grid into a marginal M2.S.7 or M2.S.1 region. Prefer -36 dbu (grid-aligned) over -32 dbu for x-axis moves.

**Y-axis moves are valid when needed.** A combined delta of [+36, -36] dbu was applied to instance i0300 in trial:i01.ug.Block1_union_row4.04 and accepted with zero new in-crop errors.

---

## Resize-End Patterns

**Apply resize_end on the x-axis high end to extend M2 polygon lengths.** All resize_end operations in this iteration target the x-axis exclusively. Accepted high-end deltas are:
- +128 dbu: trial:i01.ug.Block1_union_row1.00 (p1320)
- +92 dbu: trial:i01.ug.Block1_union_row1.00 (p1321), trial:i01.ug.Block1_union_row3.03 (p1370)
- +52 dbu: trial:i01.ug.Block1_union_row4.04 (p1238)
- +36 dbu: trial:i01.ug.Block1_union_row5.05 (p1297)

**Resize the low end by +36 dbu** when the low-end tip also requires repositioning: accepted in trial:i01.ug.Block1_union_row5.05 (p1301) and trial:i01.ug.leaf_0020.10 (p1253). A symmetric `resize` of +36 dbu (both ends simultaneously, x-axis) was accepted in trial:i01.ug.leaf_0031.11 (p1390).

**Never shrink M2 polygon width or length via resize_end in a repair.** All observed resize_end deltas are positive (extensions), and all were accepted. No negative resize_end deltas appear in the measured history; reducing M2 geometry risks M2.W.1 (18 nm minimum width) and M2.A.1 (504 nm² minimum area) violations with no measured support for recovery.

---

## DRC Error Introduction vs. Acceptance

Three trials introduced new in-crop violations but were still accepted because `conn_preserved: true`:

- trial:i01.ug.Block1_union_row1.00: 4 new in-crop errors, 5 ops (3 instance moves + resize_end +128 and +92 dbu). Largest single resize delta in the iteration; the in-crop errors are consistent with M2 tip or side spacing being tightened inside the crop window by the large geometry extensions.
- trial:i01.ug.Block1_union_row6.06: 1 new in-crop error, 1 op (move_instance -32 dbu). The off-grid displacement is the only differentiator from other single-move trials that introduced zero errors.
- trial:i01.ug.leaf_0031.11: 4 new in-crop errors, 2 ops (move +36 dbu + symmetric resize +36 dbu). Consistent with the symmetric polygon resize shifting both tip positions simultaneously and creating new near-tip spacing interactions (M2.S.3, M2.S.4, M2.S.5 candidates).

**Always verify that `conn_preserved` remains true when new in-crop errors are introduced**, as the measured gating criterion (`reason: conn_preserved`) was the accepted basis for all three error-introducing trials above.

---

## Multi-Operation Trial Behavior

**Multi-instance, multi-resize trials with up to 5 operations are supported.** Trials with 5 operations were accepted: trial:i01.ug.Block1_union_row1.00 (3 moves + 2 resize_end), trial:i01.ug.Block1_union_row5.05 (3 moves + 2 resize_end), trial:i01.ug.Block1_union_row8.07 (5 moves). Trials with 4 operations also succeeded: trial:i01.ug.Block1_union_row4.04 (3 moves + 1 resize_end). Single-operation trials succeeded in trial:i01.ug.Block1_union_row6.06 and trial:i01.ug.leaf_0004.09.

**Moving multiple instances in the same x-direction within one trial is safe.** In trial:i01.ug.Block1_union_row9.08, three instances (i0195, i0245, i0078) were each moved +36 dbu in x simultaneously and accepted with zero new errors. In trial:i01.ug.Block1_union_row8.07, five instance moves ranging from -36 to +108 dbu were combined with zero out-of-crop errors.

---

## V1 Enclosure Maintenance on M2

**When applying resize_end to extend an M2 polygon end, the V1 enclosure rules (V1.M2.EN.2, V1.M2.AUX.2) remain satisfiable.** All trials that performed resize_end operations also touched V1 and were accepted: trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row3.03, trial:i01.ug.Block1_union_row4.04, trial:i01.ug.Block1_union_row5.05, trial:i01.ug.leaf_0020.10, trial:i01.ug.leaf_0031.11. The measured record shows no out-of-crop V1.M2.EN.2 or V1.M2.AUX.2 violations were introduced by any resize_end operation in this iteration, meaning the polygon extensions preserved or increased M2 overhang past the V1 edges on the resized side.

**Do not resize M2 polygon ends in the direction that exposes a V1 edge** without confirming that the 5 nm minimum enclosure (V1.M2.EN.2) on both opposite sides is maintained. The AUX.2 rule additionally requires V1 to be flush-width with M2 perpendicular to the M2 length axis; all accepted resize_end operations were along x only, preserving y-dimension flush-width alignment (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row3.03, trial:i01.ug.Block1_union_row4.04, trial:i01.ug.Block1_union_row5.05, trial:i01.ug.leaf_0020.10, trial:i01.ug.leaf_0031.11).

---

## M2.S.7 and Corner-Condition Awareness

The M2.S.7 rule forbids a tip-to-tip gap of 18 nm co-located with a side-to-side spacing of ≤32 nm; the parallel run length must be ≥35 nm when side spacing is ≤32 nm. The single off-grid -32 dbu move in trial:i01.ug.Block1_union_row6.06 introduced 1 new in-crop error, which is consistent with the displacement marginally tightening a side spacing toward or past the 32 nm threshold in the M2.S.7 compound condition. Snap moves to the 36 dbu grid to avoid landing in the M2.S.7 forbidden region.

M2.S.6 (20 nm Euclidean corner-to-corner) was not triggered in any out-of-crop position across all 11 trials; instance moves of ±36 dbu maintain sufficient corner clearance in the observed locus geometries (trial:i01.ug.Block1_union_row1.00 through trial:i01.ug.leaf_0031.11).