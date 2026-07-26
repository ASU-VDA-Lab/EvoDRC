## Iteration 1 Outcome Summary

All 8 trials in iteration 1 were accepted (decision: gated_in) with zero new DRC violations introduced in-crop and zero out-of-crop. Connectivity was preserved in every case: trial:i01.ug.Block6_union_row3.00, trial:i01.ug.Block6_union_row5.01, trial:i01.ug.Block6_union_row7.02, trial:i01.ug.Block6_union_row8.03, trial:i01.ug.leaf_0001.04, trial:i01.ug.leaf_0011.05, trial:i01.ug.leaf_0015.06, trial:i01.ug.leaf_0018.07.

## Operation Types Observed on M1

All repairs operated exclusively along the x-axis. Two operation types touched M1 polygons.

**move_instance (x-axis).** Translations ranged from −36 dbu (trial:i01.ug.Block6_union_row7.02, instance i0074) to +112 dbu (trial:i01.ug.leaf_0001.04, instance i0404). Single-instance moves at +36 dbu were accepted in trial:i01.ug.Block6_union_row8.03, trial:i01.ug.leaf_0011.05, and trial:i01.ug.leaf_0018.07. Multi-instance moves at +72 dbu across three instances were accepted in trial:i01.ug.Block6_union_row3.00. Moves at +28 dbu (trial:i01.ug.leaf_0015.06) and +36 dbu combined with a resize (trial:i01.ug.Block6_union_row5.01) were also accepted.

**resize_end (x-axis).** High-end extensions of +92 dbu (trial:i01.ug.Block6_union_row5.01, polygon p2072), +124 dbu (trial:i01.ug.Block6_union_row7.02, polygon p1903), +132 dbu (trial:i01.ug.leaf_0001.04, polygon p2016), and +48 dbu (trial:i01.ug.leaf_0015.06, polygon p1923) were all accepted. A low-end extension of +56 dbu (trial:i01.ug.Block6_union_row7.02, polygon p1920) was also accepted. Every resize_end in this iteration extended a polygon endpoint; no shrink operations were applied to M1.

## Multi-Operation Combinations

Combining multiple move_instance and resize_end operations in a single trial produced zero new violations in every case. Trial:i01.ug.Block6_union_row5.01 applied four move_instances and one resize_end simultaneously. Trial:i01.ug.Block6_union_row7.02 applied two move_instances and two resize_ends (one high-end on p1903, one low-end on p1920) simultaneously. Trial:i01.ug.leaf_0001.04 applied one move_instance and one resize_end together. All were gated_in.

## Layers Co-Touched with M1

Every trial simultaneously touched M1, M2, and V1; no trial modified M1 in isolation. All trials were routed through the unit_gate channel.

## DRC Rule Applicability

### V0.M1.EN.1

V0.M1.EN.1 requires M1 to enclose V0 by ≥ 5 nm on two opposite sides (or 5 & 0 nm with projection). The x-axis resize_end extensions applied in trial:i01.ug.Block6_union_row5.01, trial:i01.ug.Block6_union_row7.02, trial:i01.ug.leaf_0001.04, and trial:i01.ug.leaf_0015.06 did not introduce new V0.M1.EN.1 violations, showing that extending M1 polygon endpoints along x is compatible with maintaining V0 enclosure margins.

### V1.M1.EN.1

V1.M1.EN.1 requires M1 to enclose V1 by ≥ 5 nm on one side and ≥ 2 nm on the opposite side. No new V1.M1.EN.1 violations were introduced in any trial. Resize_end operations extending M1 along x in trial:i01.ug.Block6_union_row7.02 and trial:i01.ug.leaf_0001.04, which co-touched V1, remained compliant.

### V0.M1.AUX.3

V0.M1.AUX.3 requires V0 to exactly match M1 width in the direction perpendicular to M1 length (i.e., all V0 edges must coincide with M1 edges). No new AUX.3 violations were introduced in any trial, including those applying resize_end to M1 (trial:i01.ug.Block6_union_row5.01, trial:i01.ug.Block6_union_row7.02, trial:i01.ug.leaf_0001.04, trial:i01.ug.leaf_0015.06).

### M1.W.1 and M1.S.1 through M1.S.6

M1.W.1 (minimum M1 width 18 nm), M1.S.1 (minimum side-to-side spacing 18 nm for edges > 36 nm), M1.S.2 (minimum tip-to-side spacing 25 nm), M1.S.3 (minimum tip-to-tip spacing 27 nm for edges 24–36 nm), M1.S.4 (minimum tip-to-tip spacing 31 nm for edges < 24 nm), M1.S.5 (mixed-width tip-to-tip 31 nm), and M1.S.6 (corner-to-corner 20 nm) all remained satisfied after every trial in this iteration. The largest resize_end extension (+132 dbu in trial:i01.ug.leaf_0001.04) and the largest combined move (+112 dbu in trial:i01.ug.leaf_0001.04) did not introduce new spacing or width violations. The only negative x-direction move (−36 dbu in trial:i01.ug.Block6_union_row7.02) also introduced no new spacing violations.

### M1.A.1

M1.A.1 requires a minimum M1 polygon area of 504 nm². All resize_end operations in this iteration extended M1 polygon endpoints, maintaining or increasing M1 polygon area. No M1.A.1 violations were introduced in trial:i01.ug.Block6_union_row5.01, trial:i01.ug.Block6_union_row7.02, trial:i01.ug.leaf_0001.04, or trial:i01.ug.leaf_0015.06.

### M1.R.0

M1.R.0 flags M1 islands enclosing exactly one small V0 via near large empty M1 regions (≥ 500 nm wide, area > 2.5 µm², expanded by 400 nm). No new M1.R.0 violations were introduced in any trial.

## Move and Resize Magnitude Summary

Accepted x-axis move_instance deltas in this iteration: −36 dbu (trial:i01.ug.Block6_union_row7.02), +28 dbu (trial:i01.ug.leaf_0015.06), +36 dbu (trial:i01.ug.Block6_union_row3.00, trial:i01.ug.Block6_union_row5.01, trial:i01.ug.Block6_union_row8.03, trial:i01.ug.leaf_0011.05, trial:i01.ug.leaf_0018.07), +72 dbu (trial:i01.ug.Block6_union_row3.00), +104 dbu (trial:i01.ug.Block6_union_row7.02), +112 dbu (trial:i01.ug.leaf_0001.04).

Accepted x-axis resize_end deltas in this iteration: +48 dbu high (trial:i01.ug.leaf_0015.06), +56 dbu low (trial:i01.ug.Block6_union_row7.02), +92 dbu high (trial:i01.ug.Block6_union_row5.01), +124 dbu high (trial:i01.ug.Block6_union_row7.02), +132 dbu high (trial:i01.ug.leaf_0001.04).