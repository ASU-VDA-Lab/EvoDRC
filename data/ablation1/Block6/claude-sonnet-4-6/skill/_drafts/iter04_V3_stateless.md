## Rule Geometry Reference

**V3.W.1** sets the minimum V3 width along the M4 length direction at 18 nm. This is unconditional: any V3 shape narrower than 18 nm along that axis fails regardless of enclosure or spacing context.

**V3.S.1** enforces projection-based spacing between V3 instances using a masking construction that classifies each V3 as either NEC (no-end-cap: all edges coincide with M4 edges) or WEC (with-end-cap: at least one edge does not coincide with M4). The WEC mask extends 5 nm beyond the coincident M4 edge, so the effective keep-out zone is larger than the V3 shape itself. Three thresholds apply: 18 nm between instances on the same M4 track; 18 nm between aligned instances on parallel M4 tracks; 27 nm between non-aligned instances on parallel M4 tracks. All thresholds are projection-based, so diagonal relationships between instances that do not project onto each other are not checked by this rule.

**V3.S.2** checks euclidean (corner-to-corner) spacing between two WEC instances, with a threshold of 23 nm, but only for violations that are not already collinear in projection. A pair of WEC instances whose masks project onto each other will be caught by V3.S.1; V3.S.2 catches only the diagonal remainder.

**V3.S.3** applies the analogous euclidean check between two NEC instances, with a threshold of 30 nm, again excluding projection-collinear violations. The NEC mask is the V3 shape grown by 5 nm on all sides, so the geometric footprint used for the check is larger than the drawn shape.

**V3.S.4** checks euclidean spacing between one WEC instance and one NEC instance, threshold 27 nm, excluding projection-collinear violations. This rule is asymmetric in mask construction: the WEC mask (shape plus 5 nm extension beyond the coincident M4 edge) is compared against the NEC mask (shape sized 5 nm uniformly).

**V3.M3.EN.1** requires M3 to enclose V3 by at least 5 nm on at least one pair of opposite sides. The deck checks this by testing whether V3 survives `m3.sized(-5.nm, 0)` (left+right pair) or `m3.sized(0, -5.nm)` (top+bottom pair). A V3 that fails both tests, or that lies outside M3 entirely, triggers this rule. The rule fires jointly with V3.AUX.1 for any V3 outside M3.

**V3.M4.EN.2** requires M4 to enclose V3 by at least 11 nm on at least two opposite sides, tested via `m4.sized(-11.nm, 0)` and `m4.sized(0, -11.nm)`. The 11 nm requirement is more than twice the 5 nm M3 requirement, making M4 enclosure the tighter constraint in both axes.

**V3.AUX.1** requires every V3 instance to reside entirely within the intersection of M3 and M4. Any V3 geometry outside either metal triggers this rule directly.

**V3.M4.AUX.2** requires V3 to exactly match M4's width in the direction perpendicular to the M4 length. The deck identifies V3 shapes that are not inside M4 at all, then among those inside M4 checks for instances whose edges coincide with M4 edges on at least two sides. Any V3 that is partially outside M4 or whose transverse width does not exactly equal the enclosing M4 width fails this rule.

**NONORTHOGONAL** applies to V3 as to all drawing layers: no edge may carry an angle in the ranges 1–89, 91–179, -179–-91, or -89–-1 degrees. All V3 geometry must be strictly rectilinear.

## Measured Repair Behavior

The single measured trial for this layer is trial:i04.ug.leaf_0003.01, a unit_gate channel operation on Block6 at iteration 4. The repair applied 24 `move_instance` operations across 12 instance pairs, distributing them to two x-columns (x=2896 dbu and x=13696 dbu) at six y-track positions (3216, 5424, 7536, 9744, 11856, 14064 dbu). Touched layers were M3, M4, M5, V3, and V4. The decision recorded was `gated_in` with `conn_preserved=true` (trial:i04.ug.leaf_0003.01).

Despite the accepted decision, 68 new violations appeared inside the crop boundary after the move, with zero new violations outside the crop (trial:i04.ug.leaf_0003.01). The `gated_in` path therefore does not guarantee DRC cleanliness on V3 or its neighboring layers: connectivity preservation was the acceptance criterion, not DRC pass status. Do not treat a `gated_in` outcome as evidence that V3 violations were resolved; verify the in-crop violation count independently (trial:i04.ug.leaf_0003.01).

Instance moves in the unit_gate channel that touch V3 also touch M4 and M3 simultaneously (trial:i04.ug.leaf_0003.01). Because V3.M4.AUX.2 requires exact width match between V3 and M4 in the perpendicular direction, and V3.AUX.1 requires V3 to remain within the M3-and-M4 intersection, any instance displacement that shifts V3 relative to M4 or M3 enclosure boundaries risks triggering V3.AUX.1, V3.M4.AUX.2, V3.M4.EN.2, or V3.M3.EN.1 depending on the resulting overlap geometry. The 68 new in-crop violations from trial:i04.ug.leaf_0003.01 are consistent with this multi-rule exposure, but the history record does not itemize which rules were triggered.

The y-track spacing between consecutive positions in trial:i04.ug.leaf_0003.01 is 2208 dbu (e.g., 5424 - 3216). The V3.S.1 maximum inter-instance projection spacing threshold is 27 nm, and V3.S.3 euclidean NEC-to-NEC threshold is 30 nm. If the design database unit is 1 dbu = 1 nm, the 2208 dbu inter-track pitch far exceeds all V3 spacing rule thresholds; track-to-track V3 spacing violations between instances at different y-tracks are not an expected source of the 68 new violations from this particular move pattern (trial:i04.ug.leaf_0003.01). The new violations are more likely attributable to intra-track or enclosure effects introduced by the repositioning.