## V4 width and M4/M5 enclosure

Rule V4.W.1 sets a 24 nm minimum width for V4 along the M5 length direction. Rules V4.M4.EN.1 and V4.M5.EN.2 each require 11 nm enclosure of V4 on two opposite sides by M4 and M5, respectively. In trial:i03.cu.def:VIA_VIA45_1_2_58_58.00, a +152 dbu x-axis resize applied to both V4 shape indices and the M4 shape in cell VIA_VIA45_1_2_58_58 reduced the total violation count by 28 with connectivity preserved (conn_preserved: true). In trial:i04.ug.whole_design.00, x-axis resize_end operations on polygons p1374 (+140 dbu high end), p1395 (+172 dbu high end), and p1382 (+176 dbu low end) across touched layers M3, M4, M5, V3, V4 preserved connectivity and produced zero new violations in or out of crop.

## Resizing both V4 shape indices in a multi-via cell definition

When repairing width or enclosure violations in a via cell definition that contains more than one V4 shape, resize all V4 shape indices by the same delta in the same operation set; in trial:i03.cu.def:VIA_VIA45_1_2_58_58.00, applying identical +152 dbu x-axis deltas to shape_index 0 and shape_index 1 of V4 in cell VIA_VIA45_1_2_58_58 eliminated 28 violations while preserving connectivity. Always include the enclosing M4 shape in the same resize operation to maintain the 11 nm enclosure margin required by V4.M4.EN.1, as demonstrated in trial:i03.cu.def:VIA_VIA45_1_2_58_58.00 where the M4 shape_index 0 was resized by the same +152 dbu x-axis delta alongside both V4 shapes.

## DRC window scope for cell-definition and whole-design repairs

Use the full design locus when repairing V4 violations at both the cell-definition level and the whole-design level. Trial:i03.cu.def:VIA_VIA45_1_2_58_58.00 applied fixes with locus [0, 0, 14672, 14672] and achieved a 28-violation net reduction. Trial:i04.ug.whole_design.00 used the same locus [0, 0, 14672, 14672] with 25 mixed operations (polygon resize_end plus move_instance) and produced conn_preserved: true with zero new violations. Do not restrict the DRC evaluation window to a sub-region when targeting V4 repairs.

## Instance movement as a V4 violation repair mechanism

Move_instance operations quantized to multiples of 24 dbu are a valid repair strategy for V4 violations when used in combination with polygon resize_end operations. Trial:i04.ug.whole_design.00 applied 22 move_instance operations with deltas drawn from {±24, ±48, ±72} dbu on both x and y axes across instances i0319, i0307, i0237, i0239, i0212, i0205, i0313, i0306, i0214, i0223, i0103, i0141, i0136, i0128, i0032, i0021, i0104, i0150, i0099, i0113, i0079, i0019, achieving conn_preserved: true with zero new violations. Instance moves address positional spacing between placed via instances and are applied alongside polygon resizes that correct enclosure and width.

## Multi-layer coordinated repairs spanning M3/V3/M4/V4/M5

Effective V4 repairs extend the touched-layer set beyond V4, M4, and M5 when the violation context involves adjacent metal and via layers. Trial:i04.ug.whole_design.00 touched layers M3, M4, M5, V3, and V4 in a single 25-operation repair set; trial:i03.cu.def:VIA_VIA45_1_2_58_58.00 touched M4, M5, and V4. Both preserved connectivity. When V4 spacing or enclosure violations are coupled to M3/V3 geometry, include M3 and V3 in the repair operation set rather than limiting changes to V4 and its immediate enclosing metals.

## Spacing rules V4.S.1, V4.S.2, and V4.S.3

Rules V4.S.1 and V4.S.2 impose a 33 nm minimum projection-based spacing between V4 instances on the same net and on different nets, respectively. Rule V4.S.3 imposes a 33 nm Euclidean corner-to-corner minimum spacing between any two V4 instances. Trial:i04.ug.whole_design.00 demonstrates that instance moves quantized to multiples of 24 dbu in x and y, combined with polygon end resizes, form an effective repair pattern that preserves connectivity; the move deltas used (±24, ±48, ±72 dbu) represent the observed granularity for repositioning instances to satisfy spacing constraints.

## Containment rules V4.AUX.1 and V4.M5.AUX.2

V4.AUX.1 requires every V4 instance to lie inside both M4 and M5. V4.M5.AUX.2 requires each V4 instance to share coincident edges with M5 on at least two sides, enforcing exact V4 width match in the direction perpendicular to M5 length. In trial:i03.cu.def:VIA_VIA45_1_2_58_58.00, the touched-layer set included M4, M5, and V4, and conn_preserved was true; no separate fix for V4.AUX.1 or V4.M5.AUX.2 was recorded beyond the co-resize of all three layers in that operation set. In trial:i04.ug.whole_design.00, M5 was included in the touched-layer set alongside x-axis polygon end resizes, maintaining M5 containment and width-match constraints while instance positions were adjusted.