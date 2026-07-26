## Repair Mechanics Grounded in Measured History

**Coordinate units.** All delta values in the history are in dbu. The single accepted trial (trial:i02.ug.whole_design.00) applied x-axis moves of 32 dbu and resize_end operations ranging from 32 to 116 dbu on the high x-end of polygons, co-moving M1, M2, M3, M4, M5, V1, V2, V3, and V4 together as a coherent bundle. Zero new violations were introduced in-crop or out-of-crop after these moves (trial:i02.ug.whole_design.00, n_new_in_crop=0, n_new_out_of_crop=0).

**Connectivity must be preserved across co-moved layers.** The trial was gated_in specifically because conn_preserved was true (trial:i02.ug.whole_design.00). When adjusting V1 positions to satisfy spacing or enclosure rules, any M1 and M2 polygons that enclose or are coincident with the affected V1 shapes must move with the via, not be left behind. Moving V1 alone without its enclosing metal will violate V1.AUX.1, V1.M1.EN.1, and V1.M2.EN.2 simultaneously.

**Simultaneous multi-layer bundled moves can be DRC-clean.** The 45-operation bundle in trial:i02.ug.whole_design.00 moved instances and resized polygon ends across nine layers without producing new violations. This confirms that coordinated moves—where V1 polygons, their enclosing M1 shapes, and their enclosing M2 tracks all shift by the same x delta—are a viable repair strategy for spacing violations that require lateral relocation of an entire via stack.

**resize_end on the high x-end of M2 (or M1) polygons accompanies lateral via moves.** In trial:i02.ug.whole_design.00, after moving via stacks rightward, the high-x ends of associated metal polygons were extended (32–116 dbu). This is consistent with maintaining V1.M2.AUX.2 (V1 width must equal M2 width perpendicular to M2 length) and V1.M2.EN.2 (M2 must enclose V1 by 5 nm on two opposite sides) when the via shifts but the metal track does not fully follow.

## Rule-Specific Operational Notes

**V1.W.1 (minimum width 18 nm along M2 length).** No measured trial directly tested a width-below-18nm violation repair on V1. Do not resize a V1 polygon below 18 nm in the M2 length direction; the rule fires on the via shape itself.

**V1.S.1 (spacing 18/27/18 nm by track configuration).** The rule discriminates three cases by mask geometry derived from M2 edge coincidence. Vias fully flush with M2 edges (no non-coincident M2 edges, i.e., "nec" class) use a 5 nm end-cap extended mask; vias with non-coincident M2 edges ("wec" class) use a differently computed mask. Spacing checks are projection-based for the 17 nm projection check and supplemented by mask-level checks. When moving a V1 to resolve a V1.S.1 violation, the minimum required lateral displacement depends on which mask class both vias belong to; the bundled x-move of 32 dbu applied in trial:i02.ug.whole_design.00 was sufficient to achieve a clean result across all spacing rules active in that crop.

**V1.S.2 / V1.S.3 / V1.S.4 (euclidean corner-to-corner spacings).** These rules use euclidean distance checks (16.4 nm, 16.12 nm, 17.11 nm check thresholds corresponding to 23 nm, 30 nm, 27 nm nominal spacings) on the wec-mask, nec-mask, or their separation, respectively. Euclidean violations only fire when projection-based checks do not already capture the edge pair (V1.S.3 uses `not_interacting(v1_s3_proj.polygons)` to isolate true diagonal cases). No trial directly measured a repair for a diagonal corner-to-corner violation in isolation; the general lateral bundle move in trial:i02.ug.whole_design.00 did not introduce new violations of these rules.

**V1.M1.EN.1 (M1 enclosure 5 & 2 nm on opposite sides).** The rule requires that for each V1, at least one axis has ≥5 nm M1 enclosure on both horizontal edges, or ≥5 nm on both vertical edges, with ≥2 nm on the perpendicular axis. Moving V1 relative to M1 without co-moving M1 will break this rule. The accepted bundle in trial:i02.ug.whole_design.00 co-moved M1 instances and resized M1 polygon ends alongside V1 to preserve enclosure.

**V1.M2.EN.2 (M2 enclosure 5 & 5 nm or 5 & 0 nm).** The rule allows two valid enclosure patterns: 5 nm on both sides of one axis, or 5 nm on one side and 0 nm (flush) on the other. The second sub-check (`v1_en2_ep_zero`) fires when any enclosing M2 edge that has 5 nm clearance does not also have a paired flush (0 nm) edge on the opposite side—enforcing the 5&5 or 5&0 constraint strictly. Resize_end operations on M2 polygon high ends (as performed in trial:i02.ug.whole_design.00) are consistent with restoring the 5 nm enclosure on the trailing side of a rightward-shifted via.

**V1.M2.AUX.2 (V1 width equals M2 width perpendicular to M2 length).** This rule requires exact width match; V1 must not be narrower or wider than M2 in the cross-track direction. Any resize of V1 in the perpendicular direction must be matched by an identical resize of the enclosing M2 polygon, or the rule fires. No direct repair of this violation was measured; the accepted trial avoided introducing this violation by bundling all layer moves together (trial:i02.ug.whole_design.00).

**V1.AUX.1 (V1 must be inside both M1 and M2).** This is a containment check against the intersection of M1 and M2. Any move of V1 that takes it outside the overlap region of its enclosing M1 and M2 will fire this rule. The accepted trial preserved containment by moving all layers together (trial:i02.ug.whole_design.00).

**NONORTHOGONAL.** All V1 edges must be at 0° or 90°. No nonorthogonal repair was measured. Do not introduce diagonal edges when resizing or moving V1 polygons.

## Summary of What Is Measured

Only one trial exists for this layer and iteration: trial:i02.ug.whole_design.00, a 45-operation bundle across nine layers that was gated_in with conn_preserved and zero new violations. All prescriptive repair guidance above beyond this single data point derives from the DRC rule logic itself, not from additional measured repair experiments.