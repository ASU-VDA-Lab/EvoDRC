## V2 Rule Geometry

**V2.W.1** enforces a minimum V2 width of 18 nm along the M3 length direction.

**V2.S.1** builds per-instance masks before checking projected spacing. The mask construction splits V2 instances into two classes based on edge coincidence with M3:

- **nec** (no end-cap): all V2 edges coincide with M3 edges. The mask extends each coincident M3-side edge by 5 nm outward on each end.
- **wec** (with end-cap): at least one V2 edge does not coincide with any M3 edge. The mask extends coincident edges by 5 nm laterally, then sizes +5 nm and -5 nm to round corners.

Projected spacing thresholds on the merged mask: 18 nm (same M3 track, horizontal edges), 1 nm (cross-check on non-horizontal edges), 18 nm (non-M3 mask edges). The mask-versus-actual V2 intersection is also checked at 18 nm projection.

**V2.S.2** checks euclidean corner-to-corner spacing ≥ 23 nm between any two wec-classified V2 instances (using the wec mask with 16.4 nm euclidean threshold, which accounts for the 5 nm mask extension on each side).

**V2.S.3** checks euclidean corner-to-corner spacing ≥ 30 nm between any two nec-classified V2 instances, but only for violations that are not also caught by projection — isolating true diagonal near-misses.

**V2.S.4** checks euclidean corner-to-corner spacing ≥ 27 nm between one wec and one nec V2 instance, again filtering projection-visible violations.

**V2.M2.EN.1** requires M2 to enclose V2 by at least 5 nm on at least two opposite sides, verified by checking that V2 does not protrude past an x-shrunk and a y-shrunk version of M2 simultaneously.

**V2.M3.EN.2** requires M3 to enclose V2 by at least 5 nm on two opposite sides. Valid enclosure patterns are (5 nm, 5 nm) or (5 nm, 0 nm) on the perpendicular pair. V2 that lacks any qualifying opposite-side pair, or that is not inside M3, triggers the rule.

**V2.AUX.1** requires every V2 polygon to lie entirely inside the intersection of M2 and M3.

**V2.M3.AUX.2** requires V2 to share at least two coincident edges with M3. In practice this means V2 must span M3 exactly in the direction perpendicular to M3 length with zero overhang and zero gap on both perpendicular sides.

**GEOMETRY.NONORTHOGONAL** fires on any V2 edge whose angle is not a multiple of 90°; all V2 geometry must be rectilinear.

## Repair Observations

**Multi-layer co-moves across M1/M2/M3/V1/V2 simultaneously** produced zero new in-crop violations and zero new out-of-crop violations in both accepted trials (trial:i01.ug.Block7_union_row16.06, trial:i01.ug.leaf_0095.26). Both trials also confirmed conn_preserved=true, meaning the stack-wide co-move strategy preserved electrical connectivity while introducing no secondary DRC hits.

**Move deltas used in trial:i01.ug.Block7_union_row16.06**: instances moved by [-36, 0] dbu (two instances), [0, -12] dbu (two instances), and [+36, 0] dbu (one instance); one polygon moved by [0, -12] dbu on the y-axis. This mix of opposing-direction instance moves with a single polygon nudge resolved the targeted violation without introducing new ones (n_new_in_crop=0, n_new_out_of_crop=0).

**Resize-end on M3** at delta +68 dbu (high end, y-axis) on one polygon and +48 dbu (high end, y-axis) on another, combined with instance moves of [0, +48] dbu and [+36, 0] dbu, was accepted in trial:i01.ug.leaf_0095.26 with conn_preserved=true and n_new_in_crop=0, n_new_out_of_crop=0. Extending M3 length alters which V2 edges are coincident with M3 edges, directly shifting the nec/wec classification that drives V2.S.1 through V2.S.4 mask construction and V2.M3.AUX.2 compliance.

**Both accepted trials operated on the full metal/via stack** (touched_layers included M1, M2, M3, V1, and V2 in both trial:i01.ug.Block7_union_row16.06 and trial:i01.ug.leaf_0095.26). No trial in this history operated on V2 in isolation.