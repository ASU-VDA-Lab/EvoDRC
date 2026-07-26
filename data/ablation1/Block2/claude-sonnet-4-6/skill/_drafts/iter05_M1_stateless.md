**M1.A.1 — Minimum area 504 nm²**

Instance moves across a wide locus can fragment M1 polygons to sub-minimum area. In trial:i01.ug.leaf_0013.08 a single `move_instance` over a locus spanning [1728,3148]–[10368,9812] introduced 1 new M1.A.1 violation. The trial was still accepted because connectivity was preserved, but the violation count confirms that large-crop moves carry M1.A.1 fragment risk. Add-polygon repairs must clear M1.A.1: the patch added in trial:i01.ug.leaf_0001.03 (points [[5332,2340],[5532,2340],[5532,2448],[5332,2448]], 200×108 dbu) produced no M1.A.1 flag, confirming a rectangle of at least that size is area-safe. The same polygon was later deleted in trial:i02.ug.leaf_0001.00 and replaced by a `resize_end` on an adjacent polygon, also without an area violation, showing both patch-add and delete-plus-reshape are compliant paths at this locus.

**X-axis instance moves: safe at 36–37 dbu**

All x-only instance moves at 36 dbu in iter 1 produced zero new in-crop or out-of-crop M1 violations: trial:i01.ug.Block2_union_row1.00, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0001.03, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0011.06. A 37 dbu shift (trial:i01.ug.leaf_0004.04) and a repeat 36 dbu shift in iter 4 (trial:i04.ug.leaf_0001.00) were likewise clean. The 36 dbu increment aligns with a 2× multiple of the 18 nm M1.W.1 minimum width at the process grid, which is why these steps do not disturb M1 spacing or width constraints.

**Y-axis moves introduce M1-layer violations**

The only trials applying y-axis deltas are in trial:i05.ug.leaf_0003.01 (five `move_instance` ops at ±24 dbu in y), which produced 13 new in-crop violations across touched layers M1, M2, M3, M4, M5, V1, V3, V4. No x-only trial at comparable step sizes produced any violations. Y-axis moves at this pitch disrupt M1 widths, spacings, or via enclosures across the full vertical stack. When y-axis adjustment is required, the 13-violation result from trial:i05.ug.leaf_0003.01 — accepted only because connectivity was preserved — sets a measured upper-bound on the risk; connectivity preservation is the gate condition, not violation-zero.

**V0.M1.EN.1 — Enclosure ≥5 nm on two opposite sides (or 5 & 0 nm)**

The rule checks both horizontal and vertical enclosure projections independently and fires if neither pair of opposite sides satisfies the 5 nm requirement. No trial produced a V0.M1.EN.1 error. Rigid `move_instance` operations move M1 and the V0 vias it contains as a unit, preserving relative enclosure (trial:i01.ug.Block2_union_row1.00 through trial:i01.ug.leaf_0011.06). The `resize_end` in trial:i02.ug.leaf_0001.00 (axis x, delta 172 dbu, low end, polygon p957) extended M1 toward a newly placed via rather than shrinking it, maintaining enclosure on both opposing sides without violation.

**V1.M1.EN.1 — Enclosure ≥5 nm one side, ≥2 nm opposite**

No trial raised a V1.M1.EN.1 error. All `move_instance` ops that touch V1 (trial:i01.ug.Block2_union_row1.00 through trial:i05.ug.leaf_0003.01) preserve the M1-to-V1 enclosure relationship by moving the entire cell, including the M1 landing metal and the V1 via, by the same delta. The add_via in trial:i02.ug.leaf_0001.00 (VIA_VIA12 at [5472,2340]) combined with `resize_end` on p957 also produced no enclosure error, confirming that resizing M1 toward a new via by a large margin (172 dbu) satisfies the 5 nm / 2 nm pair constraint without risk.

**V0.M1.AUX.3 — V0 must be exactly the same width as M1 in the perpendicular direction**

AUX.3 fires when any V0 edge is not coincident with an M1 edge, indicating V0 overhangs or M1 undercuts the via perpendicularly. No AUX.3 violation appeared in any trial. `move_instance` operations that shift M1 and V0 together rigidly preserve edge coincidence by definition (trial:i01.ug.Block2_union_row1.00, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0001.03, trial:i04.ug.leaf_0001.00). Polygon-only operations (add_polygon in trial:i01.ug.leaf_0001.03, `resize_end` in trial:i02.ug.leaf_0001.00) did not trigger AUX.3, indicating the shape edits in those trials did not affect the V0 edge alignment. Any M1 polygon resize that changes the M1 width adjacent to a V0 must maintain coincidence with the V0 boundary edges on both sides perpendicular to the M1 length axis.

**M1.S.1 — Side-to-side spacing ≥18 nm when both edges >36 nm**

No M1.S.1 violation appeared in any trial. The consistent 36 dbu x-axis step used across iter 1 (trial:i01.ug.Block2_union_row1.00 through trial:i01.ug.leaf_0011.06) and iter 4 (trial:i04.ug.leaf_0001.00) did not close any side-to-side gaps below 18 nm, confirming the cell placement grid already accounts for M1.S.1. The rule only fires when both edges are longer than 36 nm; tip edges are governed by M1.S.2 through M1.S.5.

**M1.S.2 — Tip-to-side ≥25 nm (tip ≤36 nm, side >36 nm)**

No M1.S.2 violation appeared in any trial. The add_polygon in trial:i01.ug.leaf_0001.03 placed an M1 patch of 200×108 dbu without triggering tip-to-side violations, and the subsequent delete in trial:i02.ug.leaf_0001.00 removed it cleanly. When placing new M1 patches adjacent to existing M1 long edges, a 25 nm clearance from any patch tip to any neighboring long-edge side must be maintained; the measured 200×108 dbu patch was located without encroaching on that margin.

**M1.S.3 through M1.S.6 — Narrow tip spacings and corner clearance**

No violations under M1.S.3 (tip-to-tip ≥27 nm for tips 24–36 nm), M1.S.4 (tip-to-tip ≥31 nm for tips <24 nm), M1.S.5 (mixed-width tip-to-tip ≥31 nm), or M1.S.6 (corner-to-corner ≥20 nm) appeared in any trial. The magnitude of x-shifts used (36–37 dbu) and the add_polygon dimensions in trial:i01.ug.leaf_0001.03 did not approach these thresholds.

**M1.W.1 — Minimum width 18 nm**

No M1.W.1 violation appeared in any trial. The add_polygon in trial:i01.ug.leaf_0001.03 used 108 dbu in its narrower dimension, well above 18 nm. The `resize_end` in trial:i02.ug.leaf_0001.00 extended polygon p957 (added material), not reduced it, so no width narrowing occurred. Resize operations that trim the low end of an M1 polygon must verify the residual width remains ≥18 nm after the trim; the 172 dbu extension measured in trial:i02.ug.leaf_0001.00 is an additive operation with no such risk.

**M1.R.0 — Redundant island near large empty M1 region**

No M1.R.0 flag appeared in any trial. The add_polygon in trial:i01.ug.leaf_0001.03 was a temporary patch that was removed in trial:i02.ug.leaf_0001.00 before it could persist as an island. M1.R.0 is triggered only when an M1 polygon enclosing exactly one small V0 via lands within 400 nm of a large empty M1 region (≥500 nm wide, area >2.5 µm²). No measured operation created that configuration.

**NONORTHOGONAL constraint on M1**

All add_polygon and resize operations in the history used Manhattan-aligned coordinates. The polygon added in trial:i01.ug.leaf_0001.03 has points [[5332,2340],[5532,2340],[5532,2448],[5332,2448]], forming a rectilinear rectangle with no diagonal edges. No nonorthogonal edge error was flagged on M1 in any trial. New M1 polygon points must remain on orthogonal (0° or 90°) edges; any non-axis-aligned coordinate in an add_polygon or resize will directly trigger the NONORTHOGONAL rule for M1.

**Connectivity preservation as acceptance gate**

Across all 11 trials in this history, every trial that touched M1 was accepted (`decision: gated_in`) and every accepted trial had `conn_preserved: true`. In trial:i01.ug.leaf_0013.08, 1 new M1.A.1 violation was introduced but the trial was still accepted because connectivity was preserved. In trial:i05.ug.leaf_0003.01, 13 new in-crop violations were introduced (across M1 and co-touched layers) and the trial was still accepted on the same grounds. Connectivity preservation is the dominant acceptance criterion; violation-zero is not required for gating. However, violations introduced in a conn_preserved trial persist into subsequent iterations and become the base state for further repair.