## Operation Types Observed

Every trial in the measured history carries `conn_preserved=true` and `decision=gated_in`. Three M1-touching operation types appear: `move_instance`, `resize_end` (polygon end extension along the x axis), and the paired `delete_instance`/`add_via` sequence. All accepted repairs simultaneously touch layers M1, M2, and V1 in every trial from trial:i01.ug.Block1_union_row1.00 through trial:i04.ug.leaf_0004.03, confirming that M1 geometry changes are consistently co-applied with V1 repositioning and M2 adjustment to maintain stack connectivity.

## Move Quantum: 36 dbu Is the Reliable Horizontal Step

The most common horizontal move delta is 36 dbu. It appears in the majority of accepted repairs with zero new in-crop violations: trial:i01.ug.Block1_union_row10.01, trial:i01.ug.Block1_union_row9.08, trial:i01.ug.Block1_union_row3.03, trial:i01.ug.leaf_0004.09, trial:i04.ug.leaf_0001.00, and others. Multiples of 36 dbu (72 dbu in trial:i03.ug.Block1_union_row3.00 and trial:i03.ug.leaf_0004.01; 108 dbu in trial:i01.ug.Block1_union_row1.00 and trial:i01.ug.Block1_union_row8.07) are also accepted without generating new violations. Do not use sub-36 non-zero move deltas: the 4 dbu move applied to instance i0060 across the large locus (1728,2068)–(14256,13680) in trial:i04.ug.leaf_0004.03 produced 80 new in-crop violations, the highest single-trial violation count in the history.

A move of -32 dbu appeared in trial:i01.ug.Block1_union_row6.06 (single operation, 1 new violation) and in trial:i01.ug.Block1_union_row8.07 (among a five-operation mix, 0 new violations). The -32 dbu step is not a multiple of 36 dbu; its safety depends on surrounding operations. The measured record does not contain a single-operation -32 dbu move that produces zero violations.

The only y-direction move in the history is the [36,-36] delta for instance i0300 in trial:i01.ug.Block1_union_row4.04, which produced zero new violations in a four-operation repair.

## Resize-End Operations

`resize_end` extends one end (high or low) of an M1 polygon along the x axis. Observed deltas and outcomes:

- +36 dbu (trial:i01.ug.Block1_union_row5.05, trial:i01.ug.leaf_0020.10): 0 new violations.
- +52 dbu (trial:i01.ug.Block1_union_row4.04): 0 new violations.
- +72 dbu (trial:i03.ug.leaf_0004.01): 0 new violations.
- +92 dbu (trial:i01.ug.Block1_union_row3.03): 0 new violations.
- +128 dbu and +92 dbu applied simultaneously to two polygons (trial:i01.ug.Block1_union_row1.00): 4 new violations.

Apply resize_end in the 36–92 dbu range when a single polygon is extended; combining two large resize_end operations on different polygons in a single trial introduces new violations (trial:i01.ug.Block1_union_row1.00).

A symmetric (non-directional) `resize` of +36 dbu on polygon p1390 combined with a move_instance in trial:i01.ug.leaf_0031.11 produced 4 new violations. This contrasts with the directional `resize_end` operations at equivalent deltas that produced zero violations when applied without concurrent large moves to the same area.

## Via Replacement (delete_instance / add_via)

Trial:i02.ug.leaf_0004.02 used `delete_instance` on i0300 followed by `add_via` of cell `VIA_VIA12` at origin (5904,6300). This produced zero new violations and was accepted. The locus (5344,5508)–(6192,6372) overlaps the row4 area where trial:i01.ug.Block1_union_row4.04 had previously moved the same unit, establishing that via relocation within a previously repaired area is a valid correction path. Via replacement is the only operation type in the history that modifies M1-connected via placement without a corresponding polygon resize.

## Out-of-Crop Violations

`n_new_out_of_crop` is 0 in every trial across all four iterations. Accepted repairs are localized: no trial propagated new violations outside its declared locus.

## New In-Crop Violations by Trial

Trials with nonzero `n_new_in_crop`:

- trial:i01.ug.Block1_union_row1.00: +4 (two resize_end operations: +128 dbu and +92 dbu on separate polygons)
- trial:i01.ug.Block1_union_row6.06: +1 (single -32 dbu move)
- trial:i01.ug.leaf_0031.11: +4 (move_instance +36 dbu combined with symmetric resize +36 dbu)
- trial:i02.ug.Block1_union_row6.01: +1 (five move_instance operations on the row6 locus revisit)
- trial:i04.ug.leaf_0004.03: +80 (4 dbu move of instance i0060 across the near-full-design locus)

The gate criterion is `conn_preserved`, not zero new violations. All five trials above were accepted. The 80-violation outcome in trial:i04.ug.leaf_0004.03 is an order of magnitude larger than any other trial and is attributable to the combination of a sub-grid move delta (4 dbu) and a locus that spans most of the design.

## Units Requiring Multi-Iteration Repair

Several units appear in more than one iteration's repair records, indicating that a single repair pass does not fully resolve violations:

- **Block1_union_row3**: trial:i01.ug.Block1_union_row3.03 (iter 1), trial:i03.ug.Block1_union_row3.00 (iter 3). Both produced zero new violations.
- **Block1_union_row6**: trial:i01.ug.Block1_union_row6.06 (iter 1, +1 new violation), trial:i02.ug.Block1_union_row6.01 (iter 2, +1 new violation). Row6 introduced one new violation in each of two consecutive repair attempts.
- **leaf_0004**: trial:i01.ug.leaf_0004.09 (iter 1, 0 new), trial:i02.ug.leaf_0004.02 (iter 2, 0 new via replacement), trial:i03.ug.leaf_0004.01 (iter 3, 0 new), trial:i04.ug.leaf_0004.03 (iter 4, +80 new). The first three iterations of leaf_0004 repair each produced zero new violations using move_instance or move+resize_end in small, bounded loci. The iteration 4 repair moved instance i0060 by 4 dbu across a locus covering virtually the entire design and produced 80 new violations. Repair of leaf_0004 in iterations 1–3 used loci of at most (9936,4048)–(10620,4212) (56 nm × 164 nm range), (5344,5508)–(6192,6372), and (4480,6588)–(5544,7452). The iteration 4 locus (1728,2068)–(14256,13680) is an order of magnitude larger than any prior leaf_0004 locus.

Avoid expanding the repair locus to near-full-design scale for a unit that has been successfully repaired with bounded loci in prior iterations (trial:i04.ug.leaf_0004.03 versus trial:i01.ug.leaf_0004.09, trial:i02.ug.leaf_0004.02, trial:i03.ug.leaf_0004.01).

## Enclosure Repair via resize_end

Rules V0.M1.EN.1 (minimum M1 enclosure of V0: 5 nm on two opposite sides) and V1.M1.EN.1 (minimum M1 enclosure of V1: 5 nm and 2 nm on opposite sides) are addressed by extending M1 polygon length. The resize_end operations in trial:i01.ug.Block1_union_row3.03 (+92 dbu high-end extension on p1370) and trial:i03.ug.leaf_0004.01 (+72 dbu high-end extension on p1295) both produced zero new violations while the locus previously contained enclosure-related errors. Extending M1 length increases the projection distance between M1 and via edges, directly satisfying the EN.1 projection-based checks without altering via position.

## V0.M1.AUX.3 and Symmetric Resize

V0.M1.AUX.3 requires V0 width to exactly equal M1 width in the direction perpendicular to M1 length. The only symmetric `resize` operation in the history (polygon p1390, delta +36 dbu, trial:i01.ug.leaf_0031.11) was accompanied by a move_instance and produced 4 new violations. No trial demonstrates a symmetric resize producing zero violations in isolation. The resize in trial:i01.ug.leaf_0031.11 changed p1390 width on both ends simultaneously; the resulting geometry violated spacing rules in the surrounding area.

## M1.A.1 Area Constraint

M1.A.1 requires minimum M1 polygon area of 504 nm². All resize_end operations in the history add area (positive deltas only in the measured records). No operation reduces M1 polygon area below the pre-repair value. No trial reports a violation attributed to M1.A.1.

## M1.R.0 Redundant Island Avoidance

M1.R.0 flags M1 polygons enclosing exactly one small V0 via that are located near large empty M1 regions. No trial in the history records an M1.R.0 violation or attributes any new violation to this rule. The via replacement in trial:i02.ug.leaf_0004.02 (add_via VIA_VIA12 at a specific origin) would be subject to M1.R.0 if the resulting M1 island is isolated near a large empty zone, but that trial produced zero new violations.