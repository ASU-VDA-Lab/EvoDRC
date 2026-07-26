## Decision policy

The gating channel accepts candidates that introduce new in-crop violations provided the connectivity invariant holds. trial:i01.ug.leaf_0010.07 introduced 3 new in-crop violations (n_new_in_crop=3) and was still decided gated_in because conn_preserved=true and n_new_out_of_crop=0. New in-crop violations do not disqualify a candidate when connectivity is preserved.

## M4 grid and track alignment

M4.AUX.1 requires every M4 horizontal edge to land on a 24 nm grid. Consequently, y-axis instance moves must use deltas that are integer multiples of 24 nm. trial:i01.ug.leaf_0010.07 applied y-deltas of 72, 24, and −24 nm (all multiples of 24) and produced no new M4.AUX.1 violations. trial:i02.ug.leaf_0002.01 used y-deltas of −48, 96, 48, and 96 nm (all multiples of 24) across its instance moves and likewise produced no M4.AUX.1 violations.

M4.AUX.2 requires minimum-width M4 tracks to align to horizontal routing tracks with pitch 192 dbu and a 48 dbu offset from the origin (the offgrid_cl check with pitch_dbu=192, offset_dbu=48, base_dbu=96). Moves that respect 24 nm y-grid alignment do not automatically satisfy track centering; the track pitch must also be respected. The y-deltas observed in trial:i01.ug.leaf_0010.07 (72, 24, −24) are all divisors or multiples of the 24 nm pitch and kept instances within their routing tracks without creating M4.AUX.2 violations.

## Forbidden vertical widths

M4.W.1 sets the minimum vertical width at 24 nm. M4.W.3 forbids vertical widths that are exact even integer multiples of 24 nm: 48, 96, 144, 192, 240, 288, 336, 384, 432, and 480 nm. M4.W.4 additionally forbids widths of 72, 168, 264, 360, and 456 nm (widths that span an even number of minimum-width routing tracks). M4.W.2 caps vertical width at 480 nm. When resizing an M4 polygon vertically, verify that the resulting height does not fall on any value in either the M4.W.3 or M4.W.4 forbidden lists. M4.W.5 sets the minimum horizontal width at 44 nm.

## Spacing rules

M4.S.1 requires 24 nm minimum vertical spacing between M4 polygon edges regardless of edge length or mask color. M4.S.2 requires 40 nm minimum horizontal spacing between vertical M4 edges. M4.S.3 and M4.S.4 both require 40 nm tip-to-tip spacing on adjacent tracks whether or not the two polygons share a parallel run length. M4.S.5 requires a minimum parallel run length of 44 nm when two M4 polygons on adjacent tracks have a gap smaller than 25 nm between their horizontal edges.

## No-bend and non-orthogonal constraints

M4.AUX.3 forbids any bend in M4 polygons; the rule flags any M4 edge that participates in a corner between 0° and 90°. The global NONORTHOGONAL block additionally flags any M4 edge with an angle outside 0° or 90°. M4 shapes must remain strictly axis-aligned rectangles or L-free rectilinear polygons with no diagonal edges.

## Via enclosure

V3.M4.EN.2 requires M4 to enclose V3 by at least 11 nm on two opposite sides. V3.M4.AUX.2 requires the V3 width perpendicular to the M4 run direction to exactly match the M4 width at that location; any M4 edge that does not coincide with two V3 edges on the perpendicular axis violates this rule. V4.M4.EN.1 imposes the same 11 nm two-sided enclosure requirement for V4.

trial:i01.ug.leaf_0010.07 moved instances with y-deltas of 72 and −24 nm and touched the V3 and V4 layers alongside M4; the decision recorded n_new_out_of_crop=0, confirming that the moves maintained adequate enclosure on both via levels despite the non-trivial vertical displacements.

## Wide M4 and AUX.4

M4.AUX.4 prohibits a horizontal edge of a wide M4 polygon from coinciding with a minimum-width routing track edge. The rule classifies a polygon as wide if it survives `m4.sized(0, -13.nm).sized(0, 13.nm)` and is not adjacent to a minimum-width segment. The outside horizontal edges of such polygons must not land on the routing track grid lines defined by M4.AUX.2.

## cu_pool interaction and assembly drops

cu_pool operations take priority over unit_gate operations on shared polygon targets. trial:i02.ug.leaf_0002.01 targeted polygon p879 with an x-move of 32 dbu; at assembly this op was dropped with reason reserved_by_cu_pool_winner because the cu_pool had already claimed p879. The applied cu_pool ops on p879 (a y-resize of +96 dbu and an x-move of a V2 shape) were retained instead.

Resizing via cell M5 shapes in y resolves violations on M4 and the vias that land on it. trial:i02.cu.def:VIA_VIA45_1_2_58_58.02 shrank the M5 shape in cell VIA_VIA45_1_2_58_58 by −88 nm in y; this operation touched M4 and V4 and reduced the total violation count by 15 across two windows (leaf_0002: 17→8, leaf_0003: 25→19), decision applied.