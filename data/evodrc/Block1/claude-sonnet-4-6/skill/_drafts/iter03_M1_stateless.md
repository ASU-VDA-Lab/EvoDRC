## M1.S.2: Tip-to-Side Spacing Fixed by Small VIA12 Instance Moves

Rule M1.S.2 requires 25 nm separation between an M1 tip edge (length ≤ 36 nm) and a longer M1 side edge (length > 36 nm), measured under a projection check. In trial:i03.ug.leaf_0003.02, two M1.S.2 violations (v0011 and v0012) were cleared by moving VIA12 instances by +4 dbu (1 nm) in the x-direction. Each 4 dbu shift displaced the M1 land's tip edge by exactly the same amount, bringing both tip-to-side gaps to 100 dbu (25 nm):

- VIA12 i0485 moved from x=12276 to x=12280: M1 left tip edge advanced from x=12240 to x=12244, achieving a 100 dbu gap to the M1 side edge at x=12144 (trial:i03.ug.leaf_0003.02).
- VIA12 i0188 moved from x=2772 to x=2776: M1 left tip edge advanced from x=2736 to x=2740, achieving a 100 dbu gap to the M1 side edge at x=2640 (trial:i03.ug.leaf_0003.02).

No separate polygon resize was required for either M1.S.2 correction; the instance move alone propagated to the M1 land edge (trial:i03.ug.leaf_0003.02).

## M2 Overlap Must Be Confirmed After Any VIA12 Move That Fixes M1.S.2

Moving a VIA12 instance to resolve M1.S.2 simultaneously displaces the via's M2 land. In trial:i03.ug.leaf_0003.02, each VIA12 move was verified to leave the M2 land within the bounds of the connected M2 routing polygon: i0485's new M2 left edge at x=12208 fell inside p1309 (11808..12312), and i0188's new M2 left edge at x=2704 fell inside p1270 (2448..2808). Do not move a VIA12 to fix an M1.S.2 violation without confirming the resulting M2 land still overlaps the connected M2 polygon (trial:i03.ug.leaf_0003.02).

## Connectivity Preservation Is the Acceptance Gate for M1 Repairs

Every trial accepted (decision: gated_in) in the full history carried conn_preserved: true. The sole gated_out trial, trial:i01.ug.leaf_0034.12, broke connectivity (conn_preserved: false) and introduced 89 new violations in crop from 10 operations spanning M1, M2, M3, M4, V1, and V2 over a locus covering nearly the full design extents (1728,2068 to 14256,13680). No M1 repair that breaks connectivity is admitted, regardless of the DRC violation count resolved (trial:i01.ug.leaf_0034.12).

## New In-Crop Violations Do Not Block Acceptance When Connectivity Is Preserved

Several gated_in trials introduced new violations within the crop yet were still accepted: trial:i01.ug.Block1_union_row1.00 (4 new), trial:i01.ug.Block1_union_row6.06 (1 new), trial:i01.ug.leaf_0031.11 (4 new), trial:i02.ug.leaf_0001.00 (8 new), trial:i03.ug.leaf_0003.02 (8 new). The presence of new in-crop violations does not in itself cause gating-out; broken connectivity does (trial:i01.ug.leaf_0034.12).

## Large-Locus, Multi-Layer Operations Produce Connectivity Failures

The only gated_out result (trial:i01.ug.leaf_0034.12) involved the largest locus in the history (~12,500 × 11,600 dbu) and the largest layer set (M1, M2, M3, M4, V1, V2). All accepted trials operated on smaller, unit-level loci and touched at most M1, M2, and V1. Prefer localized, single-unit repairs for M1; the full-block, multi-layer sweep failed with 89 new violations and broken connectivity (trial:i01.ug.leaf_0034.12).

## V1.M1.EN.1 Enclosure: Satisfied by Standard VIA12 Placement After Small Moves

V1.M1.EN.1 requires M1 to enclose V1 by 5 nm on one pair of opposite sides and at least 2 nm on the other pair. In trial:i03.ug.leaf_0003.02, VIA12 instances i0485 and i0188 were each shifted by +4 dbu in x, and the resulting state was accepted (gated_in, conn_preserved), with no enclosure violation reported as cause for rejection. A 4 dbu shift of a VIA12 toward a nearer M1 side does not violate V1.M1.EN.1 when standard VIA12 cell geometry provides the required 5 nm and 2 nm enclosure margins (trial:i03.ug.leaf_0003.02).

## Instance Move Deltas Observed in M1-Touching Trials

All observed move_instance delta magnitudes across the M1-touching gated_in trials are multiples of 4 dbu. Values seen include 4, 8, 36, 37, 56, 64, 72, 100, 108, 128, 136 dbu in x (trials i01.ug.Block1_union_row1.00, i01.ug.Block1_union_row3.03, i01.ug.Block1_union_row4.04, i01.ug.Block1_union_row5.05, i01.ug.Block1_union_row6.06, i01.ug.Block1_union_row8.07, i01.ug.Block1_union_row9.08, i01.ug.leaf_0004.09, i01.ug.leaf_0020.10, i01.ug.leaf_0031.11, i02.ug.leaf_0001.00, i03.ug.leaf_0003.02). The smallest delta that directly fixed an M1 rule (M1.S.2) is 4 dbu (trial:i03.ug.leaf_0003.02).

## resize_end on M1 Polygons Is Used Together With Instance Moves

Multiple gated_in trials used resize_end operations on M1 polygon edges coordinated with instance moves: high-end extensions of 36, 48, 92, 128, 156, 192 dbu appear in trials i01.ug.Block1_union_row5.05, i01.ug.Block1_union_row6.06, i01.ug.Block1_union_row8.07, i02.ug.leaf_0001.00. Low-end moves of 36 and 56 dbu appear in trials i01.ug.Block1_union_row5.05 and i01.ug.Block1_union_row6.06. All trials combining resize_end on M1 with instance moves were accepted (conn_preserved: true), confirming that endpoint resizing of M1 polygons in tandem with via or cell repositioning does not inherently break connectivity (trials i01.ug.Block1_union_row5.05, i01.ug.Block1_union_row6.06, i01.ug.Block1_union_row8.07, i02.ug.leaf_0001.00).