## Repair Operation Patterns

**Instance moves in the x-direction resolve M2 spacing violations without introducing new M2 violations.** All iter-1 trials touching M2 that used move_instance with delta_dbu of [36,0] — trial:i01.ug.Block2_union_row1.00, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0011.06, trial:i01.ug.leaf_0013.08 — and the iter-4 trial trial:i04.ug.leaf_0001.00 all achieved conn_preserved=true with n_new_out_of_crop=0. A single-instance move of [37,0] in trial:i01.ug.leaf_0004.04 produced equivalent success. The 36 dbu x-step is the dominant unit-gate repair primitive for M2 on this design.

**M2 polygon resize in x corrects tip position without connectivity loss.** In trial:i01.ug.Block2_union_row1.00, polygon p1053 was resized along x by +184 dbu alongside two instance moves with no new violations. In trial:i02.ug.leaf_0001.00, a resize_end on polygon p957 (low end, +172 dbu in x) resolved the violation as part of a multi-op sequence on M1, M2, and V1, also producing no new violations.

**Moving an M2 polygon directly — without any instance move — resolves M2-only violations.** In trial:i02.ug.leaf_0002.01 only M2 appeared in touched_layers: polygon p1053 was translated in x by +76 dbu, producing conn_preserved=true and zero new violations. This confirms that direct M2 polygon translation suffices when the violation is confined to M2 geometry and no via enclosure constraint is at risk.

**Y-direction instance moves at 24 dbu increments also resolve M2-involved violations.** In trial:i04.ug.leaf_0003.02, three instances were moved in y (i0090 and i0110 by +24 dbu, i0089 by -24 dbu), touching M2 through M5 and V2 through V4. The result was gated_in with conn_preserved=true; two new violations appeared in-crop (n_new_in_crop=2) but none out-of-crop, and all were on layers above M2.

## Via Enclosure (V1.M2.EN.2, V1.M2.AUX.2, V2.M2.EN.1)

**V1 enclosure violations involving M2 are resolved inside unit_gate instance operations, not as standalone polygon edits.** Every trial that moves instances and touches M1, M2, and V1 together — trial:i01.ug.Block2_union_row1.00 through trial:i01.ug.leaf_0013.08 — resolves V1.M2.EN.2 and V1.M2.AUX.2 implicitly by repositioning the entire instance, which carries the V1 shape with its enclosing M2 in fixed relative position.

**V2 enclosure violations (V2.M2.EN.1) are resolved by the cu_pool channel, not by unit_gate.** trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 applied move_via_shape and resize_via_shape operations on V2 shapes inside cell VIA_VIA23_1_3_36_36, reducing total violations by 24 across two windows (leaf_0012 and leaf_0013). The unit_gate channel does not independently repair V2.M2.EN.1.

**When cu_pool has already committed V2 fixes for a via cell, duplicate V2 ops from unit_gate are dropped at assembly and must not be re-issued.** In trial:i01.ug.leaf_0013.08, five V2 ops targeting VIA_VIA23_1_3_36_36 appeared in assemble_drops with reason "cu_pool:applied", because trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 had already applied those changes. Re-issuing those ops would create assembly conflicts; the harness silently drops them rather than applying them twice.

**Replacing an added M2/M1 polygon with a proper via structure resolves enclosure violations introduced in prior iterations.** In trial:i02.ug.leaf_0001.00, polygon p1101 (an M1 shape added in trial:i01.ug.leaf_0001.03) and instance i0086 were deleted, a VIA_VIA12 was inserted at origin [5472,2340], and polygon p957 was extended at its low end by +172 dbu. This produced gated_in with no new violations. Polygon additions made in early iterations can be temporary scaffolding; a subsequent iteration must replace them with via-compliant structures to satisfy V1.M2.EN.2 and V1.M2.AUX.2.

## Geometric Constraints

**All M2 operations must produce strictly orthogonal geometry.** The NONORTHOGONAL rule flags any M2 edge at angles 1–89°, 91–179°, -179– -91°, or -89– -1°. Every move, resize, resize_end, and add_via in the measured history produces only 0° or 90° edges. Do not apply diagonal translations or shear transformations to M2 polygons.

**Moving an M2 polygon that does not enclose a via requires no adjustment to V1 or V2 shapes.** trial:i02.ug.leaf_0002.01 moved only an M2 polygon and listed only M2 in touched_layers, with no V1 or V2 changes, and produced no new enclosure violations. When the M2 polygon being translated does not serve as an enclosing shape for any via within the affected locus, via enclosure rules are unaffected.

**Resize and resize_end operations must keep M2 polygon area at or above 504 nm² (M2.A.1).** No M2.A.1 violation appears in any trial's new_in_crop set, indicating that the applied resize deltas (+76 dbu to +184 dbu in x) preserve sufficient area. When applying resize_end to shorten an M2 tip, verify that the post-operation polygon area remains ≥ 504 nm².

**M2.S.7 forbids pairing an 18 nm tip-to-tip gap with side-to-side spacing ≤ 32 nm; parallel run length must be ≥ 35 nm at side spacings ≤ 32 nm.** No trial in the history violated M2.S.7 after repair, confirming that instance moves at 36 dbu in x provide sufficient displacement to clear both the tip-to-tip gap constraint and the co-location restriction together.

**M2.S.8 enforces ≥ 80 nm euclidean center-to-center spacing between tip-to-tip gaps on different tracks.** No M2.S.8 violation was introduced in any trial, indicating that the 36 dbu x-step and 24 dbu y-step repair increments do not place gap centers within the 80 nm exclusion zone relative to other tracks in this design's pitch context.

## Channel Interaction and Gating

**conn_preserved=true is achievable for every class of M2 repair applied in this design.** All twelve trials in the measured history achieved conn_preserved=true, spanning instance moves, standalone polygon moves, polygon resizes, and via replacements. Connectivity preservation is not a binding constraint for M2 repairs when moved shapes remain on their original nets.

**New in-crop violations on non-M2 layers introduced by conn_preserved repairs are tolerated by the gating criterion.** trial:i01.ug.leaf_0013.08 introduced one new M1.A.1 violation (n_new_in_crop=1) while resolving M2-related violations and was still gated_in. trial:i04.ug.leaf_0003.02 introduced two new violations (n_new_in_crop=2) on layers above M2 and was still gated_in. In contrast, no trial in the history produced any n_new_out_of_crop > 0; out-of-crop new violations are avoided in all successful repairs.

**Multi-instance coordinated moves resolve M2 violations in densely packed rows.** trial:i01.ug.Block2_union_row1.00 moved two instances together by [36,0] plus resized an M2 polygon; trial:i01.ug.Block2_union_row5.02 moved three instances together by [36,0]. Coordinated multi-instance displacement in the same direction within a row eliminates relative spacing violations while preserving the row's internal topology.