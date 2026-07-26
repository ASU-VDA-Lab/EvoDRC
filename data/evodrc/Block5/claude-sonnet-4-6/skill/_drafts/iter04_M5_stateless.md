## M5.AUX.1 — Vertical edge grid (24 nm pitch)

The trial:i02.ug.leaf_0002.01 pre-drop evaluation recorded M5.AUX.1:7 in `new_in_crop_by_rule`; the triggering op set included an x+32 dbu move of polygon p879, a step that is not a multiple of 24 dbu and therefore displaces vertical edges off the required 24 nm grid. After assembly drops (the p879 x-move was dropped due to a cu_pool reservation conflict), the net n_new_in_crop resolved to 0. The same x+32 dbu move of p879 was re-applied in trial:i04.ug.leaf_0001.00 and produced 8 new in-crop violations in the assembled result. Do not move M5 polygons by x-offsets that are not integer multiples of 24 dbu; 32 dbu is a confirmed source of M5.AUX.1 when starting from an on-grid position (trial:i02.ug.leaf_0002.01, trial:i04.ug.leaf_0001.00).

## M5.AUX.3 — No bends

The trial:i02.ug.leaf_0002.01 pre-drop evaluation recorded M5.AUX.3:13 in `new_in_crop_by_rule`. The op set for that trial included instance moves with simultaneous x and y displacements on the same set of instances (i0112 x+32/y-48, i0073 x+32/y+96, i0062 x+32/y+48). After the cu_pool-conflicted p879 x-move was dropped and both cu_pool-already-applied ops were removed, the net n_new_in_crop resolved to 0. Avoid combining non-zero x and non-zero y deltas on instances that share M5 segments in the same trial, as this pattern produced 13 M5.AUX.3 violations before drops in trial:i02.ug.leaf_0002.01.

## M5.S.4 — Tip-to-tip spacing, shared parallel run length (≥40 nm)

The trial:i02.ug.leaf_0002.01 pre-drop evaluation recorded M5.S.4:2 in `new_in_crop_by_rule`. The op set included the x+32 dbu lateral shift of p879 combined with mixed-axis instance moves; the net n_new_in_crop was 0 after drops. M5.S.4 is sensitive to lateral shifts of M5 wire ends toward adjacent wire tips on tracks sharing a parallel run length; the 32 dbu x-shift of p879 was the only non-instance lateral op in that trial (trial:i02.ug.leaf_0002.01).

## M5.W.5 — Minimum vertical width (44 nm)

The trial:i02.ug.leaf_0002.01 pre-drop evaluation recorded M5.W.5:5 in `new_in_crop_by_rule`; after drops the net was 0. In trial:i03.ug.leaf_0003.02, polygon p892 was shortened symmetrically at both ends (low end +32 dbu, high end -32 dbu, a 64 dbu net reduction in y-extent) as part of group "m5_fix". That trial was gated in with 15 new in-crop violations; the shrink of p892 did not eliminate all violations but was used as the explicit M5 fix operation. Vertical resizing of M5 shapes is the primary geometric lever for M5.W.5; however, symmetric end-shrink by 32 dbu at each end does not guarantee a clean result on its own (trial:i03.ug.leaf_0003.02).

## M5.AUX.2 — Minimum-width track centerline grid (pitch 192 dbu, offset 48 dbu)

No M5.AUX.2 violations appear in any per_rule breakdown across the full history. All gated-in instance moves that shifted M5 polygons in x used deltas of 8, 28, 32, or 64 dbu. The 32 dbu moves on p878 and p879 (trial:i03.ug.leaf_0003.02, trial:i04.ug.leaf_0001.00) produced in-crop violations attributable to M5.AUX.1 rather than M5.AUX.2, suggesting the track centerlines remained on the required 192 dbu / 48 dbu grid after those moves while edge alignment failed.

## Effective cu_pool repair operations on M5

**y-elongation of polygon p879 (+96 dbu):** Resizing p879 y+96 dbu in trial:i02.cu.poly:p879.00 reduced the violation count in unit leaf_0002 from 17 to 15, a net of -2. This is a moderate-yield single-polygon y-extension with no out-of-crop debt.

**M5 landing-pad shrink inside VIA_VIA45_1_2_58_58 (y-88 dbu):** Resizing the M5 shape (shape_index 0) inside cell VIA_VIA45_1_2_58_58 by y-88 dbu in trial:i02.cu.def:VIA_VIA45_1_2_58_58.02 reduced violations by 9 in leaf_0002 and 6 in leaf_0003, a combined reduction of 15—the largest single repair step in the entire history. Shrinking an oversized M5 via landing pad vertically is the highest-yield M5 repair operation observed; prefer this target when VIA_VIA45 cells are present with wide M5 shapes (trial:i02.cu.def:VIA_VIA45_1_2_58_58.02).

## x-translation of M5 polygon with co-moved instances (unit_gate channel)

Moving p879 x+32 dbu together with four instances (i0114, i0112, i0073, i0062) appears in both trial:i02.ug.leaf_0002.01 (op dropped at assembly due to cu_pool reservation) and trial:i04.ug.leaf_0001.00 (applied, gated_in, 8 new in-crop violations). The +32 dbu step is a confirmed source of in-crop violations; when the op was dropped in trial:i02.ug.leaf_0002.01 the violations resolved to 0, and when it was applied in trial:i04.ug.leaf_0001.00 the violations materialized. Use x-moves of M5 polygons only in multiples of 24 dbu to preserve M5.AUX.1 compliance (trial:i02.ug.leaf_0002.01, trial:i04.ug.leaf_0001.00).

## Assembly conflict patterns affecting M5

**cu_pool reservation blocks unit_gate x-moves on the same polygon within the same iteration:** In trial:i02.ug.leaf_0002.01, the x+32 dbu move of p879 was dropped at assembly because cu_pool had reserved p879 for a y-resize (applied in trial:i02.cu.poly:p879.00 at the same iteration). Schedule unit_gate x-moves of cu_pool-targeted M5 polygons in a subsequent iteration, after the cu_pool repair has been applied (trial:i02.ug.leaf_0002.01, trial:i02.cu.poly:p879.00).

**external_duplicate drops on shared instance moves between concurrent unit_gate trials:** In trial:i03.ug.leaf_0002.01, the x-32 dbu move of instance i0073 was dropped because leaf_0001 had already claimed the identical move in trial:i03.ug.leaf_0001.00 at the same iteration. Only the first claimant's move is applied; subsequent claims for the same instance in the same iteration are silently dropped (trial:i03.ug.leaf_0002.01, trial:i03.ug.leaf_0001.00).

## Via enclosure compliance during M5 repairs

No V4.M5.EN.2, V4.M5.AUX.2, or V5.M5.EN.1 violations appear in the `new_in_crop_by_rule` breakdowns of any trial in this history. Every trial that jointly touched M5 and V4 maintained conn_preserved=true and n_new_out_of_crop=0 (trial:i01.ug.leaf_0010.07, trial:i02.ug.leaf_0002.01, trial:i02.cu.def:VIA_VIA45_1_2_58_58.02, trial:i03.ug.leaf_0001.00, trial:i03.ug.leaf_0002.01, trial:i03.ug.leaf_0003.02, trial:i04.ug.leaf_0001.00). The y-88 dbu shrink of the M5 landing pad in VIA_VIA45_1_2_58_58 did not introduce V4 enclosure violations, establishing that moderate vertical shrinkage of that cell's M5 shape is enclosure-safe (trial:i02.cu.def:VIA_VIA45_1_2_58_58.02).

## Iteration-level repair sequencing

cu_pool repairs in iteration 2 (trial:i02.cu.poly:p879.00: -2, trial:i02.cu.def:VIA_VIA45_1_2_58_58.02: -15) achieved the largest violation reductions in the history before any iteration-3 or iteration-4 unit_gate trials were applied. Unit_gate trials in iterations 1 through 4 are consistently gated in with n_new_out_of_crop=0 and conn_preserved=true across all records; no trial has been rejected. Cu_pool via-shape resizing precedes and enables unit_gate polygon placement adjustments; the order observed is cu_pool first within an iteration, unit_gate second (trial:i02.cu.poly:p879.00, trial:i02.cu.def:VIA_VIA45_1_2_58_58.02, then trial:i03 and trial:i04 unit_gate trials).