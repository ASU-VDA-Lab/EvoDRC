## M1.A.1 — Minimum Area (504 nm-sq)

Instance moves can produce new M1.A.1 area violations within the crop region. trial:i01.ug.leaf_0013.08 introduced one new in-crop M1.A.1 violation when a single `move_instance` (+36 dbu x) displaced connectivity geometry; the trial was accepted under `conn_preserved=true` gating despite the new violation.

When adding an M1 patch polygon, dimensions of 200 × 108 dbu cleared M1.A.1 with zero new errors (trial:i01.ug.leaf_0001.03). The area of that patch (21 600 dbu²) far exceeds the 504 nm-sq floor.

## M1 Polygon Lifecycle — Add and Delete

The patch polygon added in trial:i01.ug.leaf_0001.03 was deleted in trial:i02.ug.leaf_0001.00 as part of a restructured repair that replaced the patch-plus-instance-move approach with a `resize_end` + `add_via` approach. Both the addition and the deletion were accepted with zero new M1 violations.

## V0.M1.EN.1 and V1.M1.EN.1 — Via Enclosure by M1

V0.M1.EN.1 requires M1 to enclose V0 on two opposite sides by at least 5 nm, with the complementary side at ≥0 nm. V1.M1.EN.1 requires 5 nm and ≥2 nm on opposite sides for V1.

All instance-move and resize operations across iter 1–4 that touched M1 and V1 were accepted with zero new enclosure violations: trial:i01.ug.Block2_union_row1.00, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0004.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0011.06, trial:i01.ug.leaf_0013.08, and trial:i04.ug.leaf_0001.00.

When a via cell (`VIA_VIA12`) was inserted via `add_via` and the adjacent M1 polygon end was extended by `resize_end` (+172 dbu, x-axis, low end), all enclosure constraints were met with no new violations (trial:i02.ug.leaf_0001.00). Pairing `resize_end` toward the via with the `add_via` call satisfies enclosure on the approached side.

## Resize Operations on M1

An x-axis `resize` of polygon p1053 by +184 dbu produced zero new M1.W.1, M1.S.1–S.6, or M1.A.1 violations (trial:i01.ug.Block2_union_row1.00). An x-axis `resize_end` of polygon p957 by +172 dbu at the low end also produced no new M1 rule violations (trial:i02.ug.leaf_0001.00). Both operations extended M1 rather than shrinking it, which is consistent with the absence of width or area failures.

## Instance Move Step Size

The predominant M1-touching instance-move step across iter 1 and iter 4 is +36 dbu in the x-direction: trial:i01.ug.Block2_union_row1.00, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0001.03, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0011.06, trial:i01.ug.leaf_0013.08, and trial:i04.ug.leaf_0001.00 all used this step and were gated_in. A step of +37 dbu was used in trial:i01.ug.leaf_0004.04 and also accepted. No y-axis instance moves appear in the M1-touching history.

## Gating Policy

All 10 recorded trials were decided `gated_in`. `conn_preserved=true` is the operative gating criterion: trial:i01.ug.leaf_0013.08 was accepted despite one new in-crop M1.A.1 violation because connectivity was preserved. New out-of-crop violations were zero in every trial.