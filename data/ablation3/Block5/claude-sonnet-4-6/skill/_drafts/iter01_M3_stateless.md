## M3 Layer DRC Repair Knowledge — Iteration 1

### Spacing Rule Hierarchy

M3 spacing is governed by five distinct rules whose applicable edge lengths determine which minimum applies. Edge classification thresholds are 24 nm and 36 nm. For two long edges (both > 36 nm, side-to-side), the minimum spacing is 18 nm (M3.S.1). When exactly one edge is a tip (≤ 36 nm) against a long side (> 36 nm), the minimum rises to 25 nm (M3.S.2). Tip-to-tip spacing depends on the shorter tip: if both tips are wide (≥ 24 nm and ≤ 36 nm), 27 nm applies (M3.S.3); if one tip is narrow (< 24 nm) and the other wide, 31 nm applies (M3.S.5); if both tips are narrow (< 24 nm), 31 nm also applies (M3.S.4). Corner-to-corner (euclidean, off-axis) requires 20 nm (M3.S.6). The practical consequence is that shortening a polygon end—reducing its terminal edge below 36 nm—switches the governing spacing from 18 nm to 25 nm (tip-to-side) or 27–31 nm (tip-to-tip), which is the opposite of the intended relief. In trial:i01.ug.whole_design.00, p879's high-Y end was extended by 48 dbu and p910's high-Y end was extended by 20 dbu; both repairs grew the terminal edges rather than trimming them, consistent with maintaining the less-restrictive M3.S.1 side-to-side regime rather than entering a more-restrictive tip-based regime.

### Width and Area Minimums

Minimum M3 width is 18 nm (M3.W.1). Minimum M3 area is 504 nm² (M3.A.1). A 28 nm × 18 nm rectangle exactly satisfies both. Any resize that narrows a polygon below 18 nm or reduces its enclosed area below 504 nm² is an outright violation; extend the polygon or do not shrink below those bounds. In trial:i01.ug.whole_design.00, the two polygon-level M3 edits were both extension operations (positive delta_dbu on the high end) and the trial was accepted with zero new in-crop violations, confirming that extension rather than shrinkage is the safe direction when resolving M3 spacing problems near minimum-width geometries.

### Orthogonality

All M3 edges must be axis-aligned (0° or 90°). Non-orthogonal edges on M3 produce a GEOMETRY.NONORTHOGONAL marker. The repair operations in trial:i01.ug.whole_design.00 were restricted to axis-aligned moves (delta_dbu on a single axis) and single-axis resize_end edits, and no NONORTHOGONAL violations were introduced, confirming that M3 edits must be constrained to x-only or y-only displacements.

### Via Enclosure Constraints

**V2 enclosure (V2.M3.EN.2):** M3 must enclose each V2 with at least 5 nm on two opposite sides; the legal configurations are 5 & 5 nm or 5 & 0 nm (flush on one side, 5 nm on the other). Any M3 edge that pulls back past the flush-zero limit without maintaining 5 nm on the opposite side triggers V2.M3.EN.2. The rule additionally requires that no V2 edge is left outside M3 entirely.

**V2 width matching (V2.M3.AUX.2):** V2 must span the full width of M3 in the direction perpendicular to M3's length. This means M3 cannot be widened or narrowed independently of its V2 occupants without verifying that V2 still coincides with both M3 edges on its short axis.

**V3 enclosure (V3.M3.EN.1):** M3 must enclose each V3 by at least 5 nm on at least one pair of opposite sides (left+right or top+bottom). A V3 that is inside M3 but does not satisfy either opposite-pair condition fails V3.M3.EN.1.

In trial:i01.ug.whole_design.00, V2 and V3 were both among the touched layers and the trial completed with zero new violations, confirming that the combined M3 polygon extensions and instance moves preserved all enclosure relationships. When extending a M3 polygon end to satisfy M3.S.1 or M3.S.2, verify that the extension does not carry a V2 or V3 into a region where the new enclosure geometry fails V2.M3.EN.2, V2.M3.AUX.2, or V3.M3.EN.1 on the opposite side.

### Repair Operation Strategy

Trial:i01.ug.whole_design.00 applied 19 operations across M1, M2, M3, M4, M5, V1, V2, V3, and V4 in a single coordinated repair: 16 move_instance operations and 3 polygon-level edits (one polygon move, two resize_end calls). The trial was gated in with conn_preserved = true and zero new in-crop or out-of-crop violations. This demonstrates that M3 violations in dense gate-channel contexts are addressed jointly with neighboring metal and via layers rather than in isolation; an M3-only fix without corresponding adjustments to adjacent instance placements carries risk of introducing violations on the coupled layers.

The two M3 polygon edits used resize_end on the high-Y end exclusively, not shrinkage or lateral displacement of long sides. Extending the endpoint of a wire segment is the first-choice M3 polygon edit when the violation involves tip spacing (M3.S.2 through M3.S.5): lengthening the tip converts it to a long side, switching the applicable minimum from ≥ 25 nm back to 18 nm (M3.S.1), provided sufficient space exists in the extension direction. Trial:i01.ug.whole_design.00 confirms this approach resolves the violation without connectivity loss.