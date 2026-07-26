## Via Enclosure (V2.M3.EN.2, V2.M3.AUX.2)

When V2 enclosure violations involve M3, the effective repair targets the V2 shapes rather than the M3 boundary. In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 (cu_pool channel, iter 1), V2 shapes inside cell VIA_VIA23_1_3_36_36 were shifted -144 dbu on x then resized +288 dbu, centering and widening each shape relative to the existing M3 enclosure. This combination of co-directional move-and-resize reduced the total violation count by 27 across two windows (leaf_0018: -15, leaf_0019: -12) while preserving connectivity. Do not attempt to resize M3 outward to satisfy V2.M3.EN.2 when the V2 shape itself can be repositioned and widened to achieve two-opposite-side enclosure; the cu_pool channel demonstrated that adjusting the via shape is sufficient and avoids perturbing the M3 geometry (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

V2.M3.AUX.2 requires V2 to match M3 width exactly in the perpendicular direction. The resize operations in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 applied symmetric or near-symmetric +288 dbu expansions on multiple shape indices, which simultaneously satisfies the two-opposite-side enclosure required by V2.M3.EN.2 and maintains perpendicular width matching for V2.M3.AUX.2.

## M3 Polygon End-Extension for V3 Enclosure (V3.M3.EN.1)

When M3 must be extended to provide two-opposite-side enclosure of V3, asymmetric end extension is a valid applied pattern. In trial:i02.ug.leaf_0003.02 (unit_gate channel, iter 2), M3 polygon p1059 had its low x-end extended +64 dbu and its high x-end extended +320 dbu—a 5:1 asymmetry. Both resize_end operations were committed and the trial was accepted (decision: gated_in, conn_preserved: true). Do not require symmetric extension amounts on both ends of an M3 polygon; V3.M3.EN.1 checks enclosure on at least two opposite sides and can be satisfied with unequal amounts as long as each satisfies the 5 nm minimum (trial:i02.ug.leaf_0003.02).

## Instance-Move Repairs That Touch M3

The unit_gate channel resolves M3-related violations at instance granularity rather than by editing individual polygons. All four unit_gate trials (trial:i02.ug.leaf_0002.01, trial:i02.ug.leaf_0003.02, trial:i03.ug.leaf_0003.02, trial:i04.ug.leaf_0001.00) were accepted with decision: gated_in and conn_preserved: true, even though each introduced 8–12 new in-crop violations. The gate accepts a repair that preserves connectivity regardless of secondary violations introduced, which means M3 spacing or width violations that arise from instance repositioning do not block acceptance in the unit_gate channel.

Y-axis instance displacements used to relieve M3 violations ranged from -96 dbu to +72 dbu across trials i02.ug.leaf_0002.01 and i02.ug.leaf_0003.02, and a follow-on x-axis shift of +36 dbu was applied to one instance in trial:i03.ug.leaf_0003.02 after the prior y-moves on the same leaf had already been committed. This sequential refinement on the same leaf unit (leaf_0003 across iter 2 and iter 3) shows that a single unit may require multiple trial rounds before the M3 geometry converges.

In trial:i04.ug.leaf_0001.00 (iter 4), a single instance was moved -4 dbu on x, touching M3, M4, and V3. This is the smallest displacement observed across all trials in this history, yet it was accepted (gated_in, conn_preserved). Apply sub-grid or near-minimum nudges when only a small positional correction is needed to satisfy M3.S.1/M3.S.6 or V3.M3.EN.1 margin, rather than forcing a coarser snap (trial:i04.ug.leaf_0001.00).

## Dropped Operations Within Accepted Trials

In trial:i02.ug.leaf_0002.01, two operations targeting M5 (a polygon move and a via shape move in x) were dropped at assembly with reason cu_pool:rejected_net_positive before the trial was committed. The remaining six instance moves on y—which touch M3 indirectly through instance placement—were retained and the trial was accepted. This confirms that the unit_gate channel evaluates the assembled operation set after per-op filtering: a trial touching M3 can succeed even when some operations in the same trial are discarded, provided the surviving ops preserve connectivity (trial:i02.ug.leaf_0002.01).

## Spacing Rule Activation Thresholds (M3.S.1–M3.S.6)

M3.S.1 activates only for edges longer than 36 nm (side-to-side). M3.S.2 applies tip-to-side when the tip edge is ≤ 36 nm and the side edge is > 36 nm; the minimum is 25 nm under projection. M3.S.3 applies tip-to-tip when both tips are ≥ 24 nm and ≤ 36 nm; the minimum is 27 nm. M3.S.4 applies tip-to-tip when both tips are < 24 nm; the minimum is 31 nm. M3.S.5 applies tip-to-tip when one tip is ≥ 24 nm and ≤ 36 nm and the other is < 24 nm; the minimum is 31 nm. M3.S.6 uses euclidean measurement for corner-to-corner and requires 20 nm.

The asymmetric end-extension applied in trial:i02.ug.leaf_0003.02 (+64 dbu on one end, +320 dbu on the other) alters the effective tip-edge lengths of p1059 and, depending on resulting dimensions, shifts which of M3.S.3/M3.S.4/M3.S.5 governs the adjacent tip-to-tip check. Resize operations on M3 ends must account for the post-resize tip-edge length to predict which spacing rule applies; a small extension that pushes a tip from < 24 nm to ≥ 24 nm moves the governing rule from M3.S.4 (31 nm) to M3.S.3 (27 nm), reducing the required separation by 4 nm (trial:i02.ug.leaf_0003.02).

## M3 Width and Area (M3.W.1, M3.A.1)

M3.W.1 requires a minimum width of 18 nm on all M3 shapes. M3.A.1 requires minimum area of 504 nm-sq. No trial in this history records a direct M3.W.1 or M3.A.1 violation repair, but instance moves that shift M3 shapes can bring two formerly-compliant M3 shapes into proximity or alter their effective enclosed area when combined with resize operations. The 10–12 new in-crop violations introduced by trials i02.ug.leaf_0002.01, i02.ug.leaf_0003.02, i03.ug.leaf_0003.02, and i04.ug.leaf_0001.00 were not individually broken out by rule in the records for those trials, so no specific M3.W.1 or M3.A.1 counts can be attributed, but M3 was a touched layer in all four, and the new violations were accepted under conn_preserved gating.

## NONORTHOGONAL Constraint

All M3 edges must be strictly orthogonal; the GEOMETRY.NONORTHOGONAL check flags any edge with angle outside {0, 90, 180, 270}. None of the operations in the measured history introduced non-orthogonal M3 edges: all move_instance, move_via_shape, resize_via_shape, and resize_end operations preserve axis alignment by construction. Do not apply diagonal or angled displacements to M3 polygons or instances containing M3 shapes (no non-orthogonal operation appears in any accepted trial; this rule is universal across all drawing layers per the deck).