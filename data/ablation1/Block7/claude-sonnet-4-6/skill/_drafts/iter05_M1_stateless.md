## Connectivity Preservation and Gate Policy

Every trial in the recorded history was accepted with `conn_preserved: true` and `decision: gated_in` (trial:i01.ug.Block7_union_row10.00 through trial:i05.ug.leaf_0004.04, 55 consecutive accepted trials). Do not apply any repair that breaks connectivity; the gate rejects such moves regardless of DRC improvement.

## Move-Instance as Primary Repair Primitive

The dominant repair operation across all 55 trials is `move_instance`. Apply instance moves to reposition M1-bearing cells rather than editing M1 polygons directly when connectivity and grid alignment allow (trial:i01.ug.Block7_union_row15.05, trial:i01.ug.Block7_union_row11.01, trial:i02.ug.Block7_union_row6.08, trial:i02.ug.Block7_union_row21.05). After moving an instance, always update the M1 routing polygons that connect to it: use `resize_end` to stretch or retract the affected polygon endpoint, or use `move` on the entire interstitial polygon when neither endpoint is anchored to a fixed instance (trial:i01.ug.Block7_union_row9.21, trial:i02.ug.Block7_union_row17.02, trial:i03.ug.Block7_union_row17.02, trial:i04.ug.leaf_0007.05).

## X-Axis Instance Move Magnitudes

Use 36 dbu as the default x-axis move step for M1 spacing repairs. This magnitude appears in the overwhelming majority of trials and resolves M1.S.1 and M1.S.2 violations in a single step (trial:i01.ug.Block7_union_row10.00, trial:i01.ug.Block7_union_row15.05, trial:i01.ug.Block7_union_row18.08, trial:i01.ug.Block7_union_row11.01, trial:i02.ug.Block7_union_row14.01, trial:i02.ug.Block7_union_row21.05, trial:i03.ug.Block7_union_row24.05, trial:i05.ug.leaf_0003.03).

When 36 dbu undershoots, use 40 dbu (trial:i01.ug.Block7_union_row13.03 instance i0263, trial:i01.ug.Block7_union_row7.19 instance i1442) or 28 dbu for finer correction (trial:i01.ug.Block7_union_row4.16 instance i1573, trial:i01.ug.Block7_union_row6.18 instance i1473, trial:i01.ug.Block7_union_row14.04 instances i0874, i0915). Use 64 dbu when the violation spans roughly two grid pitches (trial:i01.ug.Block7_union_row8.20 instances i1405, i1921). Use 72 dbu for larger clearance requirements (trial:i01.ug.leaf_0002.23 instance i1646, trial:i01.ug.leaf_0095.26 instance i0175, trial:i01.ug.Block7_union_row23.13 instance i0678). Use 108 dbu for the largest observed displacements (trial:i01.ug.Block7_union_row7.19 instance i1446, trial:i01.ug.Block7_union_row9.21 instance i1117, trial:i01.ug.leaf_0008.24 instance i1968, trial:i04.ug.leaf_0001.01 instance i1140).

Apply 4 dbu only for fine-grain residual adjustments after a larger move has already closed most of the gap (trial:i01.ug.Block7_union_row10.00 instance i1140 +4 dbu, trial:i01.ug.Block7_union_row21.11 instance i0100 +4 dbu).

Negative x moves (-36 dbu) are correct when the adjacent M1 edge must retreat rather than the primary violator advance (trial:i01.ug.Block7_union_row10.00 instances i1811, i1180 at -36; trial:i01.ug.Block7_union_row16.06 instances i0407, i0928 at -36; trial:i02.ug.Block7_union_row18.03 instance i0428 at -36). Use -44 dbu for larger retreats (trial:i01.ug.Block7_union_row20.10 instance i0753).

## Y-Axis Instance Move Magnitudes

Y-axis moves address M1 enclosure violations in the vertical direction and vertical spacing between M1 segments. Effective upward magnitudes: 44 dbu (trial:i01.ug.Block7_union_row22.12 instance i0132, trial:i01.ug.Block7_union_row23.13 instance i0041, trial:i01.ug.leaf_0024.25 instance i0347), 52 dbu (trial:i02.ug.leaf_0032.17 instances i0949, i0950; trial:i04.ug.leaf_0008.06 instances i0949, i0950), 57 dbu (trial:i02.ug.Block7_union_row17.02 instances i0794, i0810; trial:i04.ug.leaf_0007.05 instances i0794, i0810), 64 dbu (trial:i01.ug.Block7_union_row14.04 instances i0894, i0920; trial:i05.ug.leaf_0004.04 instance i0920), 68 dbu (trial:i04.ug.leaf_0007.05 instances i0794, i0810), 72 dbu (trial:i03.ug.Block7_union_row23.04 instance i0041).

Downward y moves: -12 dbu (trial:i01.ug.Block7_union_row14.04 instances i0519, i0524), -16 dbu (trial:i02.ug.leaf_0023.16 instances i0336, i0308), -44 dbu (trial:i02.ug.leaf_0022.15 instance i1062; trial:i02.ug.leaf_0041.19 instance i0041; trial:i04.ug.leaf_0006.04 instance i1062), -48 dbu (trial:i02.ug.leaf_0035.18 instance i0235; trial:i04.ug.leaf_0009.07 instance i0235), -52 dbu (trial:i01.ug.Block7_union_row19.09 instances i0949, i0950; trial:i03.ug.Block7_union_row19.03 instances i0949, i0950), -57 dbu (trial:i03.ug.Block7_union_row17.02 instances i0794, i0810), -64 dbu (trial:i02.ug.leaf_0021.14 instance i0920; trial:i04.ug.leaf_0005.03 instance i0920), -88 dbu (trial:i03.ug.Block7_union_row13.00 instance i0347).

When moving an instance in y, also translate the connecting M1 routing polygon with `move axis:y delta:same` (trial:i02.ug.Block7_union_row17.02 polygon p3631 +57; trial:i03.ug.Block7_union_row17.02 polygon p3631 -57; trial:i04.ug.leaf_0007.05 polygon p3631 +68) or apply `resize_end axis:y` to the appropriate endpoint of the routing segment (trial:i01.ug.Block7_union_row14.04 polygon p3576 end-high +64; trial:i03.ug.Block7_union_row14.01 polygon p3515 end-high +8).

## V0.M1.EN.1: Repairing V0 Enclosure by M1

V0.M1.EN.1 requires M1 to enclose V0 by at least 5 nm on two opposite sides. To repair an enclosure deficiency, pair a `move_instance` that repositions the V0-bearing cell with a `resize_end` that extends the M1 polygon end toward the via:

- trial:i01.ug.Block7_union_row3.15: move instance i1623 by -36 dbu x, then resize polygon p3379 axis:x end:high by +49 dbu.
- trial:i01.ug.leaf_0002.23: move instance i1646 by +72 dbu x, then resize polygon p3695 axis:x end:high by +128 dbu.
- trial:i01.ug.leaf_0008.24: move instance i1968 by +108 dbu x, then resize polygon p3771 axis:x end:high by +164 dbu; also move instance i1964 by +40 dbu x.

The resize_end delta must be large enough to close the enclosure gap on both opposite sides simultaneously, not just the deficient side — the large magnitudes (49–164 dbu) observed in these trials reflect that requirement. Do not resize the M1 polygon without also moving the via instance; the cell's internal geometry determines where the via edge falls, so the polygon extension alone cannot guarantee correct two-sided enclosure (trial:i01.ug.Block7_union_row3.15, trial:i01.ug.leaf_0008.24).

## V1.M1.EN.1: Repairing V1 Enclosure by M1

V1.M1.EN.1 requires M1 to enclose V1 by 5 nm on one side and at least 2 nm on the opposite side. Apply the same combined move-instance plus resize_end strategy. When the V1 is under-enclosed in both x and y simultaneously, apply both axis corrections in the same trial (trial:i01.ug.leaf_0024.25: resize p3538 axis:x end:high +36 and axis:y end:high +44; resize p2333 axis:y end:high +20; resize p3706 axis:x end:low +52; move instance i1292 by -16 dbu x; move instance i0347 by +72 x and +44 y).

## M1.W.1: Minimum M1 Width (18 nm)

To fix an M1 width violation, expand the narrow polygon by applying `resize_end axis:x end:low` with a negative delta (expanding outward in -x) or the symmetric operation on the high end. trial:i01.ug.Block7_union_row9.21 applies resize p3300 axis:x end:low delta:-36 to widen a narrow M1 segment. After expansion, verify that no new M1.S.1 or M1.S.2 violation is introduced with adjacent M1 shapes.

## M1.S.1: Minimum Side-to-Side Spacing (18 nm, Edges > 36 nm)

M1.S.1 fires when two M1 side edges both longer than 36 nm are spaced less than 18 nm apart. Move all instances contributing to the same spacing conflict in the same direction by the same delta; do not move only one side. trial:i01.ug.Block7_union_row15.05 moves 7 instances each by +36 dbu x. trial:i02.ug.Block7_union_row6.08 moves 5 instances each by +36 dbu x. trial:i01.ug.Block7_union_row11.01 moves 2 instances each by +36 dbu x. After the instance moves, extend the M1 routing polygon that bridges the now-wider gap using `resize_end` on the endpoint that was not carried by the moved instances (trial:i01.ug.Block7_union_row12.02: resize p3273 axis:x end:high +56 after moving i1208 +36 dbu).

## M1.S.2: Minimum Tip-to-Side Spacing (25 nm)

M1.S.2 fires when an M1 tip edge (length <= 36 nm) is within 25 nm of a side edge (length > 36 nm). Move the instance containing the tip away from the side edge. Apply 36–40 dbu x-shifts as the first-attempt delta (trial:i01.ug.Block7_union_row13.03, trial:i01.ug.Block7_union_row7.19). Update the M1 routing polygon endpoint with a matching `resize_end` to maintain continuity after the move.

## M1.S.3, M1.S.4, M1.S.5, M1.S.6, M1.A.1, M1.R.0: No Direct Violation Records

The history contains no trial where these rules are identified as the specific target violation. The repair strategies documented above for M1.S.1 and M1.S.2 address the most frequent spacing classes. For M1.A.1 (minimum area 504 nm-sq), a resize_end operation that increases both width and length of a sub-threshold polygon is the appropriate repair form, consistent with the general resize_end usage seen throughout the history.

## M1 Routing Polygon Updates: Observed Patterns

After any instance move, apply the following polygon corrections to maintain M1 routing continuity:

- Instance moved +x: apply `resize_end axis:x end:high delta:+delta` to the polygon whose high-x end connects to the moved instance's low-x port (trial:i01.ug.Block7_union_row12.02 p3273 +56; trial:i01.ug.Block7_union_row3.15 p3379 +49; trial:i02.ug.Block7_union_row19.04 p3523 +92). Alternatively, use `move axis:x delta:+delta` if the polygon is a free-floating interstitial segment (trial:i01.ug.Block7_union_row9.21 polygon p2720 +56).
- Instance moved -x: apply `resize_end axis:x end:low delta:negative` to the polygon whose low-x end must retreat (trial:i01.ug.Block7_union_row9.21 p3300 end:low -36; trial:i04.ug.leaf_0001.01 p3297 end:low -40).
- Instance moved +y: apply `resize_end axis:y end:high delta:+delta` (trial:i01.ug.Block7_union_row14.04 p3576 end:high +64; trial:i03.ug.Block7_union_row14.01 p3515 end:high +8; trial:i04.ug.leaf_0007.05 p2596 end:high +68) or `move axis:y delta:+delta` for floating segments (trial:i02.ug.Block7_union_row17.02 p3631 +57; trial:i04.ug.leaf_0007.05 p3631 +68).
- Instance moved -y: apply `move axis:y delta:negative` (trial:i03.ug.Block7_union_row17.02 p3631 -57) or `resize_end axis:y end:low delta:negative` as needed.
- For 2D moves (x and y simultaneously): apply both axis corrections independently (trial:i01.ug.leaf_0024.25: p3538 resized in both x and y; trial:i03.ug.Block7_union_row13.00: p3538 axis:y end:high -44 after instance i0347 moved -88 y).

Also apply `resize_end` corrections to polygons on adjacent layers (M2, M3) when those layers are listed in `touched_layers` and connect through the moved via stack (trial:i01.ug.Block7_union_row12.02, trial:i03.ug.Block7_union_row17.02, trial:i04.ug.Block7_union_row13.00).

## Multi-Layer Stack Coupling

Every trial with a move_instance on M1 also touches V1 in `touched_layers` (trial:i01.ug.Block7_union_row10.00 through trial:i05.ug.leaf_0004.04 — all 55 trials). Propagate every M1 instance move to the V1 cell sitting on that M1 segment. When the stack extends to V2/M3, propagate the same move through those layers as well: this occurs in trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row13.03, trial:i01.ug.Block7_union_row14.04, trial:i01.ug.Block7_union_row9.21, trial:i02.ug.Block7_union_row17.02, trial:i03.ug.Block7_union_row17.02, trial:i04.ug.Block7_union_row13.00, trial:i04.ug.leaf_0007.05, trial:i04.ug.leaf_0008.06.

## Multi-Instance Simultaneous Moves

When multiple instances in the same locus share the same x or y displacement, move them all in the same trial with the same delta. Splitting the move across two trials risks creating an intermediate state with worse DRC than the starting state. trial:i01.ug.Block7_union_row15.05 moves 7 instances simultaneously by +36 x. trial:i01.ug.Block7_union_row9.21 moves 7 instances with varying x deltas in a single 9-op trial. trial:i01.ug.Block7_union_row14.04 moves 5 instances with a mix of x and y deltas in one 8-op trial.

## Repeated Unit Revisitation

The following units appear across multiple iterations, indicating that a first-pass repair exposed secondary violations requiring follow-up:

- Block7_union_row13: iter 1 (trial:i01.ug.Block7_union_row13.03), iter 2 (trial:i02.ug.Block7_union_row13.00), iter 3 (trial:i03.ug.Block7_union_row13.00), iter 4 (trial:i04.ug.Block7_union_row13.00).
- Block7_union_row14: iter 1 (trial:i01.ug.Block7_union_row14.04), iter 2 (trial:i02.ug.Block7_union_row14.01), iter 3 (trial:i03.ug.Block7_union_row14.01).
- Block7_union_row17: iter 2 (trial:i02.ug.Block7_union_row17.02), iter 3 (trial:i03.ug.Block7_union_row17.02), iter 4 (trial:i04.ug.leaf_0007.05).
- leaf_0001: iter 1 (trial:i01.ug.leaf_0001.22), iter 2 (trial:i02.ug.leaf_0001.09), iter 4 (trial:i04.ug.leaf_0001.01).
- leaf_0021/leaf_0005 (same instance i0920 at the same locus): iter 2 (trial:i02.ug.leaf_0021.14 -64 y), iter 4 (trial:i04.ug.leaf_0005.03 -64 y).
- leaf_0022/leaf_0006 (instance i1062 at locus 14112,17388): iter 2 (trial:i02.ug.leaf_0022.15 -44 y), iter 4 (trial:i04.ug.leaf_0006.04 -44 y).

Each revisit applies different ops on different polygon IDs at the same locus. Apply the complete set of ops needed to close all violations in a unit in a single trial where possible, rather than making minimal one-op moves that guarantee a follow-up iteration.

## New In-Crop Violations from Accepted Repairs

Thirty-eight of the 55 trials produce `n_new_in_crop: 0`. Prefer such repairs. Trials that introduce new in-crop violations (n_new_in_crop >= 1) while still being gated_in include: trial:i01.ug.Block7_union_row13.03 (+1), trial:i01.ug.Block7_union_row22.12 (+2), trial:i01.ug.Block7_union_row24.14 (+2), trial:i01.ug.leaf_0002.23 (+2), trial:i01.ug.leaf_0008.24 (+1), trial:i01.ug.leaf_0024.25 (+1), trial:i01.ug.Block7_union_row16.06 (from adjacent rows being adjusted), trial:i01.ug.Block7_union_row21.11 (+9), trial:i02.ug.leaf_0032.17 (+4), trial:i02.ug.leaf_0041.19 (+5), trial:i03.ug.leaf_0010.08 (+4), trial:i03.ug.leaf_0020.09 (+5), trial:i04.ug.leaf_0008.06 (+4). All were accepted because `conn_preserved: true`. New in-crop violations from a repair require resolution in a subsequent iteration; they contribute to the unit revisitation patterns above.

## GEOMETRY.NONORTHOGONAL

All M1 edges must be axis-aligned. Every delta_dbu in the recorded history is of the form [dx, 0] or [0, dy] — no diagonal instance moves are used on any trial (trial:i01.ug.Block7_union_row10.00 through trial:i05.ug.leaf_0004.04). All `resize_end` operations specify a single axis (x or y). Never produce a non-Manhattan M1 polygon edge; the NONORTHOGONAL check flags any M1 edge at 1–89 or 91–179 degrees, and no repair in the history has ever needed or applied a diagonal move to M1.