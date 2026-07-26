## Repair Strategy Overview

Both completed trials on this layer were accepted with `decision: "gated_in"` and `conn_preserved: true` (trial:i01.ug.whole_design.00, trial:i04.ug.whole_design.00). All repairs combined direct M6 polygon moves with co-movement of V5 instances, and neither trial introduced new DRC markers in or out of the crop window.

## V5 Must Track M6 Polygon Moves (V5.AUX.1 and V5.M6.AUX.2)

V5.AUX.1 requires V5 to lie inside both M5 and M6. V5.M6.AUX.2 requires V5 width to exactly match M6 width perpendicular to M6's length direction. Both constraints make V5 a rigid dependent of the M6 geometry it connects: any positional change to an M6 polygon must be propagated to every V5 instance that lands on that polygon.

In trial:i01.ug.whole_design.00, M6 polygon p3806 moved -64 dbu in Y and the three V5 instances bound to it (i1469, i1666, i2012) each received `delta_dbu:[0,-64]`. Polygon p3803 moved +32 dbu in Y and its bound instances (i1524, i1693, i2026) moved `[0,32]`. Every M6 polygon in that repair had an exactly matching set of instance moves under the same `"group":"m6_snap"` label. No residual enclosure violations were reported.

In trial:i04.ug.whole_design.00, M6 polygons moved in X: p2213 and p2216 at +32 dbu, p2212 and p2215 at -16 dbu, p2211 and p2214 at -64 dbu. The paired V5 instances reflected identical X components: groups moving at `[32,*]`, `[-16,*]`, and `[-64,*]`. The same trial is also the only record where V5 instances received non-zero Y components alongside the mandatory X tracking; those Y offsets varied per instance (e.g., `[32,48]`, `[32,-72]`, `[-64,72]`). The trial was accepted, confirming that independent Y adjustment is compatible with the width-match requirement as long as the X component faithfully tracks the M6 polygon displacement.

**Rule**: when an M6 polygon is moved, apply the same displacement vector component along the polygon's translation axis to every V5 instance whose enclosing M6 boundary is that polygon. Failure to do so violates V5.AUX.1 and V5.M6.AUX.2 simultaneously.

## Enclosure Constraints Determine Minimum Move Granularity (V5.M5.EN.1 and V5.M6.EN.2)

V5.M5.EN.1 requires M5 to enclose V5 by at least 11 nm on two opposite sides; V5.M6.EN.2 imposes the same 11 nm two-sided enclosure requirement from M6. The DRC deck implements both as sized-erosion checks: a V5 instance fails if it falls outside `m5.sized(-11nm, 0)` and `m5.sized(0, -11nm)` (or the M6 equivalents) simultaneously.

The move magnitudes observed across both trials — 16, 24, 32, 48, 64, 72, 96 dbu — are all multiples of 8 dbu (the apparent grid step). Displacements as small as 16 dbu (-2 nm at 8 dbu/nm) were accepted in trial:i01.ug.whole_design.00 and trial:i04.ug.whole_design.00 without creating new enclosure violations, meaning the existing M5/M6 envelopes had at least 2 nm of slack beyond the 11 nm minimum when those moves were applied. Do not assume slack is always available; verify enclosure margin before choosing a move magnitude for an enclosure-tight V5.

## Spacing Rules Require Awareness of Whole-Crop V5 Populations (V5.S.1, V5.S.2, V5.S.3)

V5.S.1, V5.S.2, and V5.S.3 all enforce a 33 nm minimum clearance between V5 instances, using projection (S.1, S.2) or euclidean corner-to-corner (S.3) metrics. Net membership determines which rule applies, but the 33 nm floor is the same in all three cases.

Both trials operated on `locus:[0,0,30440,30440]` (whole design), and the `"n_new_in_crop":0, "n_new_out_of_crop":0` deltas confirm no new spacing violations were introduced despite moving large numbers of instances simultaneously (24 ops in trial:i01.ug.whole_design.00, 162 ops in trial:i04.ug.whole_design.00). This is consistent with the co-movement strategy: when a V5 instance moves by the same delta as its M6 host, its position relative to neighboring V5 instances on the same M6 run is unchanged, preserving inter-via spacings. However, at M6 run boundaries — where adjacent M6 polygons are on different nets or receive different displacement magnitudes — the relative spacing between V5 instances changes. Trial:i04.ug.whole_design.00 moved three distinct M6 groups (at +32, -16, and -64 dbu) simultaneously without creating spacing violations, establishing that mixed-magnitude co-movement across net boundaries is safe when the absolute post-move coordinates respect the 33 nm floor.

## Width Rule Rarely Acts as Primary Constraint (V5.W.1)

V5.W.1 requires a minimum V5 instance width of 24 nm along the M6 length direction. No width resize operations appear in either trial record; all ops are moves or instance moves. This is consistent with V5.M6.AUX.2 fixing the V5 width to the M6 width: if M6 is wide enough to be DRC-clean under its own rules, V5 inherits that width and V5.W.1 is satisfied automatically. Neither trial:i01.ug.whole_design.00 nor trial:i04.ug.whole_design.00 contains any polygon resize op, confirming that the repair loop for this layer does not require width adjustment.

## Nonorthogonal Geometry

The GEOMETRY.NONORTHOGONAL rule applies to all drawing layers including V5. Neither trial record contains any op on V5 that would introduce a non-axis-aligned edge (all moves are pure X or pure Y translations, or combined orthogonal [X,Y] instance moves). No nonorthogonal violations were reported as new markers in either trial:i01.ug.whole_design.00 or trial:i04.ug.whole_design.00. Apply only orthogonal moves to V5 instances and M6 polygons.

## Connectivity Preservation

Both trials carry `conn_preserved: true`, meaning the repair harness validated that no net was broken. The co-movement pattern — moving V5 instances by the same displacement as their M6 polygon — preserves the M5-V5-M6 stack alignment and avoids dropping a via off its metal landing. In trial:i04.ug.whole_design.00 the additional Y component on some instances did not break connectivity, confirming that small Y offsets within the M5/M6 enclosure envelope are tolerated. Do not move V5 instances independently of their M6 host along the M6 translation axis; the co-movement protocol in both trials is the only pattern on record that achieves conn_preserved.