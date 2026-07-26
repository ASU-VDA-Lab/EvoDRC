## Geometry and Spacing Constraints

M3.W.1 requires a minimum wire width of 18 nm. M3.S.1 sets a minimum side-to-side spacing of 18 nm between edges longer than 36 nm. Tip-to-side spacing (M3.S.2) is 25 nm when the tip edge is ≤ 36 nm and the opposing edge is > 36 nm. Tip-to-tip spacing rules depend on edge length: M3.S.3 requires 27 nm when both tips are between 24 nm and 36 nm; M3.S.5 requires 31 nm when one tip is in the 24–36 nm range and the other is < 24 nm; M3.S.4 requires 31 nm when both tips are < 24 nm. M3.S.6 adds a 20 nm euclidean corner-to-corner constraint that catches diagonal proximity not covered by projection-based spacing checks. M3.A.1 sets the minimum polygon area at 504 nm². All M3 edges must be orthogonal (GEOMETRY.NONORTHOGONAL applies).

## Via Enclosure Requirements

V2.M3.EN.2 requires that M3 enclose V2 by at least 5 nm on two opposite sides (both sides 5 nm, or one side 5 nm and the opposing side flush). V2.M3.AUX.2 requires that V2 width exactly match the M3 width in the direction perpendicular to the M3 run; any mismatch in that axis triggers a violation. V3.M3.EN.1 requires that M3 enclose V3 by at least 5 nm on at least one pair of opposite sides (horizontal or vertical).

## Observed Repair Pattern: V2 Shape Repositioning and Resizing Within Via Cells

The single measured repair on this layer targeted cell `VIA_VIA23_1_3_36_36` and touched layers M2, M3, and V2 (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). The 5-operation sequence moved two V2 shapes symmetrically outward along the x-axis (shape 0 by −144 dbu, shape 2 by +144 dbu) and then expanded all three V2 shapes in x by +288 dbu each. This produced a net reduction of 27 violations (89 → 62 across the whole design) and preserved connectivity (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

Resizing V2 shapes laterally within a via cell that touches M3 is a viable strategy for reducing the combined violation count on M3-adjacent via rules without breaking connectivity, as demonstrated in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00.

The symmetric outward movement (equal-and-opposite deltas on x for shapes 0 and 2) paired with uniform x-expansion of all shapes in the cell maintained geometric balance while adjusting enclosure margins on both sides of the M3 conductor, consistent with satisfying V2.M3.EN.2 and V2.M3.AUX.2 on both opposing sides simultaneously (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

## Repair Scope and Generalization Limits

Only one trial exists for M3 at iteration 1. All prescriptive guidance above is grounded exclusively in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00. No repair patterns have been measured for M3-only violations (M3.W.1, M3.S.1–M3.S.6, M3.A.1) in isolation, nor for V3.M3.EN.1 violations. Do not apply the via-resizing pattern to M3 spacing or width violations without additional measured evidence.