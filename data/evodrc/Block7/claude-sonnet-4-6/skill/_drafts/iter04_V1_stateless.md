## Repair operation repertoire

Every trial in the history was accepted with `conn_preserved: true` and `decision: gated_in`. The repair toolkit that achieves this outcome is: `move_instance` (dominant), `resize_end` on M2 polygons (frequent companion), `resize` and `move` on polygons (occasional), and `add_polygon` on M2 (used when an instance move alone cannot supply the needed M2 area). No trial in the history was rejected, so the knowledge below is grounded exclusively in patterns shared by accepted repairs.

## Instance-move granularity and axis preference

X-axis instance moves dominate the repair history (trial:i01.ug.Block7_union_row10.00 through trial:i04.ug.leaf_0007.06). The most frequent X delta is 36 dbu, appearing across virtually every row unit in iteration 1 and continuing into iterations 2 and 3 (trial:i01.ug.Block7_union_row11.01, trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row6.18, trial:i02.ug.Block7_union_row12.01, trial:i02.ug.Block7_union_row13.02, trial:i03.ug.Block7_union_row13.01, and many others). Larger X steps of 72, 108, and 136 dbu also recur (trial:i01.ug.Block7_union_row14.04 uses 72 and 108 dbu; trial:i01.ug.Block7_union_row13.03 and trial:i01.ug.Block7_union_row15.05 use 136 dbu). Sub-36 moves down to 3–4 dbu appear in tightly constrained contexts (trial:i02.ug.leaf_0022.10 delta_dbu=[3,0]; trial:i01.ug.Block7_union_row6.18 delta_dbu=[28,0]).

Y-axis instance moves are less frequent and smaller in magnitude: −12 dbu moves appear in trial:i01.ug.Block7_union_row16.06 and trial:i02.ug.leaf_0014.08; ±48 dbu in trial:i01.ug.leaf_0095.26, trial:i02.ug.leaf_0017.09, trial:i03.ug.leaf_0008.06, trial:i04.ug.leaf_0007.06; −44 dbu in trial:i04.ug.leaf_0005.04; −84 dbu in trial:i02.ug.Block7_union_row15.03.

## M2 resize_end as enclosure companion

`resize_end` operations on M2 polygons routinely accompany instance moves on V1-touching units. This pairing satisfies V1.M2.EN.2 (minimum M2 enclosure of V1 on two opposite sides is 5 & 5 nm or 5 & 0 nm) and V1.M2.AUX.2 (V1 width along the direction perpendicular to M2 length must match M2 width). Representative pairings: trial:i01.ug.Block7_union_row10.00 pairs a 52 dbu instance move with a 308 dbu high-end resize on p3286; trial:i01.ug.Block7_union_row5.17 pairs moves with 92 dbu high-end resizes on p3737 and p3746; trial:i02.ug.Block7_union_row20.04 pairs a 72 dbu move with a 56 dbu high-end resize on p3048; trial:i02.ug.Block7_union_row9.06 pairs a 56 dbu move with a 112 dbu high-end resize on p3683. The resize delta is generally larger than the accompanying instance move delta, reflecting the need to maintain enclosure margin beyond the moved V1 boundary.

Low-end (end="low") resizes appear when an instance moves in the positive X direction and the trailing M2 edge must follow: trial:i01.ug.Block7_union_row3.15 uses a 56 dbu low-end resize alongside a −36 dbu move; trial:i01.ug.Block7_union_row17.07 uses a 56 dbu low-end resize for a 36 dbu move group; trial:i01.ug.Block7_union_row8.20 pairs a −36 dbu instance move with a 56 dbu low-end resize on p3430; trial:i01.ug.Block7_union_row18.08 uses a 92 dbu low-end resize.

## add_polygon on M2 for enclosure repair

When an instance move would leave a gap in M2 coverage needed to satisfy V1.AUX.1 (V1 must be inside M1 ∩ M2) or V1.M2.EN.2, a new M2 rectangle is inserted directly. trial:i01.ug.Block7_union_row20.10 demonstrates this: after a −36 dbu instance move, an M2 rectangle of 56 dbu × 72 dbu (points [5992,22824]→[6048,22896]) was added to restore enclosure. Use `add_polygon` on M2 when the nearest existing M2 edge is too far from V1 for a resize alone to close the enclosure gap.

## Y-axis moves correlate with M3/V2 layer involvement

Trials that touch M3 and V2 in addition to M1/M2/V1 exclusively contain Y-axis adjustments: trial:i01.ug.Block7_union_row16.06 (touched M3,V2; Y moves −12 dbu), trial:i01.ug.leaf_0095.26 (touched M3,V2; Y move +48 dbu and resize_end +68 dbu), trial:i02.ug.leaf_0014.08 (touched M3,V2; Y moves −12 dbu), trial:i03.ug.leaf_0002.04 (touched M3,V2; Y resize +20 dbu plus M3 add_polygon), trial:i03.ug.leaf_0011.07 (touched M3,V2; Y moves −48 dbu). Pure M1/M2/V1 trials use only X-axis moves. When a repair involves Y displacement, budget for updating M3/V2 connectivity simultaneously.

## Multi-iteration convergence on persistent units

Several unit IDs recur across multiple iterations, indicating that a first-pass fix introduces or exposes residual violations requiring additional rounds:

- Block7_union_row10: iterations 1 and 3 (trial:i01.ug.Block7_union_row10.00, trial:i03.ug.Block7_union_row10.00)
- Block7_union_row12: iterations 1 and 2 (trial:i01.ug.Block7_union_row12.02, trial:i02.ug.Block7_union_row12.01)
- Block7_union_row13: iterations 1, 2, and 3 (trial:i01.ug.Block7_union_row13.03, trial:i02.ug.Block7_union_row13.02, trial:i03.ug.Block7_union_row13.01)
- Block7_union_row15: iterations 1 and 2 (trial:i01.ug.Block7_union_row15.05, trial:i02.ug.Block7_union_row15.03)
- Block7_union_row20: iterations 1, 2, and 3 (trial:i01.ug.Block7_union_row20.10, trial:i02.ug.Block7_union_row20.04, trial:i03.ug.Block7_union_row20.02)
- Block7_union_row22: iterations 1 and 2 (trial:i01.ug.Block7_union_row22.12, trial:i02.ug.Block7_union_row22.05)
- Block7_union_row9: iterations 1 and 2 (trial:i01.ug.Block7_union_row9.21, trial:i02.ug.Block7_union_row9.06)
- leaf_0004: iterations 3, 4, and 5 (trial:i03.ug.Block7_union_row20.02 note: leaf_0004 first appears in trial:i04.ug.leaf_0004.03, then again trial:i05.ug.leaf_0004.03)
- leaf_0007: iterations 3 and 4 (trial:i03.ug.leaf_0007.05, trial:i04.ug.leaf_0007.06)

Units that appear three or more times across iterations have tight local spacing constraints that each incremental fix only partially resolves. The repair loop must continue until a unit no longer appears in the violation set.

## n_new_in_crop behavior and wide-locus moves

A non-zero `n_new_in_crop` does not block acceptance: trials with n_new_in_crop values of 1, 2, 3, 9, 48, and 173 were all gated_in because conn_preserved remained true (trial:i01.ug.Block7_union_row13.03 n=1; trial:i01.ug.Block7_union_row22.12 n=2; trial:i02.ug.leaf_0017.09 n=3; trial:i01.ug.Block7_union_row21.11 n=9; trial:i04.ug.leaf_0007.06 n=48; trial:i04.ug.leaf_0006.05 n=173).

The two largest n_new_in_crop values correspond to the two widest loci in the history. trial:i04.ug.leaf_0006.05 spans locus [1728,2068,28728,28172] (≈27000×26104 dbu, covering nearly the full design extent) for a single −108 dbu X move of instance i0235, producing 173 new in-crop violations. trial:i04.ug.leaf_0007.06 spans locus [1728,3148,28728,27092] for a single +48 dbu Y move of instance i0177, producing 48 new in-crop violations. Instances with globally-spanning loci are hierarchical cells placed at a high level of the design; their moves propagate displacement to all child V1 shapes across the entire block, exposing latent spacing violations throughout. Subsequent iterations must process those newly exposed violations.

## V1.S.1 spacing repair via coordinated lateral displacement

V1.S.1 enforces minimum projection-measured spacing between V1 instances on the same M2 track (18 nm), parallel non-aligned tracks (27 nm), and parallel aligned tracks (18 nm). The repair pattern across all iterations is lateral (X) displacement of the instance carrying one of the violating V1 shapes, always accompanied by a matching resize of the connecting M2 wire to preserve connectivity. The displacement magnitude required to clear a V1.S.1 violation depends on the current gap: moves as small as 36 dbu suffice for near-miss cases (trial:i01.ug.Block7_union_row11.01); moves of 136 dbu are used when the violation is larger (trial:i01.ug.Block7_union_row13.03, trial:i01.ug.Block7_union_row15.05).

## V1.M1.EN.1 and V1.M2.EN.2: enclosure maintained by paired resize

V1.M1.EN.1 requires M1 to enclose V1 by 5 nm on one pair of opposite sides and 2 nm on the other pair. V1.M2.EN.2 requires M2 to enclose V1 by 5 & 5 nm or 5 & 0 nm. Since V1 rides with the instance, moving an instance moves V1 relative to both M1 and M2 wires. The consistent repair pattern is to resize the M2 polygon end that trails the direction of motion (low-end resize when moving positive X; high-end resize when extending M2 in the same direction as the move). M1 enclosure is maintained by the instance geometry itself since M1 is part of the standard cell. The resize_end deltas observed (56–308 dbu) are always larger than or equal to the corresponding instance move delta, ensuring the M2 end does not fall short of the V1 boundary after relocation (trial:i01.ug.Block7_union_row10.00, trial:i01.ug.Block7_union_row5.17, trial:i02.ug.Block7_union_row9.06, trial:i01.ug.Block7_union_row7.19).

## V1.AUX.1 and V1.M2.AUX.2: containment invariants

V1.AUX.1 (V1 must be inside M1 ∩ M2) is the hardest constraint to violate inadvertently: every gated-in repair preserves it by construction because conn_preserved is the gate criterion and a V1 outside M1 or M2 would sever the connection. V1.M2.AUX.2 (V1 width perpendicular to M2 length must equal M2 width) is maintained by keeping V1 centered on the M2 track; the resize_end operations that accompany instance moves ensure M2 does not narrower than V1 at the via location. The add_polygon case in trial:i01.ug.Block7_union_row20.10 restores M2 coverage when an instance move would otherwise leave V1 partially outside M2.

## Negative X moves for spacing relief

Several trials use negative X displacements to relieve spacing violations between a moved V1 and a neighboring fixed V1. trial:i01.ug.Block7_union_row14.04 moves i0519 by −36 dbu while moving other instances positive; trial:i01.ug.Block7_union_row18.08 moves i0428 by −72 dbu; trial:i01.ug.Block7_union_row19.09 moves i0026 by −72 dbu alongside a −72 dbu polygon resize. trial:i02.ug.Block7_union_row13.02 moves i1059 by −72 dbu. Negative moves are used when the violating pair straddles an instance boundary and the enclosure-limited instance must retreat rather than the other advance.

## Iteration 4 repair profile

Iteration 4 contains four trials on a new design state (c2a236476b62c824de655a4b65282a99612453b68edba1609ae633b5a09c08b0). All four are single-operation trials: trial:i04.ug.leaf_0004.03 (−56 dbu X move), trial:i04.ug.leaf_0005.04 (−44 dbu Y move), trial:i04.ug.leaf_0006.05 (−108 dbu X move, wide locus, 173 new in-crop), trial:i04.ug.leaf_0007.06 (+48 dbu Y move, wide locus, 48 new in-crop). The large n_new_in_crop values from the last two trials indicate that iteration 5 must process the newly exposed violations, as confirmed by trial:i05.ug.leaf_0004.03 (−96 dbu X, −48 dbu Y diagonal move on unit leaf_0004 again).