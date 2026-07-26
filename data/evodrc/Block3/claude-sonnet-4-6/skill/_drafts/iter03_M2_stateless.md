## Repair Operation Inventory

### Instance moves — x-direction

Positive x-direction instance moves from 36 dbu to 136 dbu produced zero new in-crop M2 violations across every unit_gate trial in iterations 1 and 2 (trial:i01.ug.Block3_union_row1.00, trial:i01.ug.Block3_union_row2.01, trial:i01.ug.Block3_union_row5.02, trial:i01.ug.Block3_union_row8.03, trial:i01.ug.leaf_0006.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0009.07, trial:i01.ug.leaf_0012.08, trial:i02.ug.leaf_0002.01). These moves shift M2 wires and their attached V1 vias in the +x direction; no M2.W.1, M2.S.1, M2.S.2, M2.S.3, M2.S.4, M2.S.5, M2.S.6, M2.A.1, M2.S.7, or M2.S.8 violations were introduced within the crop window for any of these moves.

Negative x-direction instance moves of 36 dbu have a mixed record: two instances introduced zero new violations (trial:i01.ug.leaf_0013.09, trial:i02.ug.leaf_0001.00), but one introduced 10 new in-crop violations (trial:i03.ug.leaf_0003.02). Do not treat a -36 dbu instance move as unconditionally safe for M2; the context of surrounding M2 polygons determines whether spacing rules (M2.S.1 at 18 nm side-to-side, M2.S.2 at 25 nm tip-to-side, M2.S.6 at 20 nm corner-to-corner) are stressed by the shift.

### Polygon resize operations — resize_end, high end, x-axis

Extending the high-x end of M2 polygons (resize_end, axis x, end high) by amounts ranging from 36 dbu to 192 dbu introduced zero new M2 violations across all trials where such operations appeared (trial:i01.ug.Block3_union_row1.00 at +192 dbu on p1254, p1270, p1255; trial:i01.ug.Block3_union_row5.02 at +36 dbu on p1265; trial:i01.ug.Block3_union_row8.03 at +164/+128/+128/+92 dbu on p1267/p1266/p1269/p1257; trial:i01.ug.leaf_0007.05 at +56 dbu on p1223, p1189; trial:i01.ug.leaf_0012.08 at +108 dbu on p1256; trial:i02.ug.leaf_0002.01 at +128 dbu on p1226). Elongating a segment toward +x increases the side-edge length, moving short tip edges (≤36 nm) into the longer-edge category (>36 nm) as the segment grows, which relaxes M2.S.2 tip-to-side requirements (25 nm) and replaces them with the more permissive M2.S.1 side-to-side requirement (18 nm). None of these trials produced M2.S.7 or M2.S.8 composite violations, indicating that the corresponding horizontal spacing and run-length conditions remained satisfied after extension.

### Polygon resize operations — resize_end, high end, y-axis

A single +20 dbu resize of the high-y end of a polygon (trial:i01.ug.leaf_0008.06, polygon p1159) produced zero new in-crop violations. This is the only measured y-direction resize on M2; the result confirms that a small extension in the y direction does not necessarily introduce M2.S.1 or M2.S.3 violations in this design context.

### V2 via resizing and repositioning (cu_pool channel)

Applying resize_via_shape (+288 dbu in x on three V2 shapes) combined with move_via_shape repositioning on cell VIA_VIA23_1_3_36_36 reduced the total DRC count by 27 across units leaf_0018 (32→17, −15) and leaf_0019 (35→23, −12) and was accepted with decision "applied" (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). The touched layers were M2, M3, and V2. V2.M2.EN.1 requires at least 5 nm enclosure of V2 by M2 on two opposite sides; widening or repositioning V2 shapes in x can correct enclosure failures when the M2 bar is already wide enough in x to absorb the enlarged V2 footprint. The cu_pool channel applied this change globally to the via cell definition, propagating the fix to all placements of that cell in the design.

## Channel Behavior

### unit_gate: connectivity-driven acceptance

Every trial processed through the unit_gate channel in this history was accepted with decision "gated_in" and conn_preserved: true. The acceptance criterion in this channel is connectivity preservation, not DRC cleanliness: trial:i03.ug.leaf_0003.02 was gated_in despite introducing 10 new in-crop violations (n_new_in_crop: 10) because connectivity was preserved (trial:i03.ug.leaf_0003.02). Do not interpret a unit_gate "gated_in" decision as confirmation that the operation is DRC-neutral on M2; subsequent iterations must absorb any new violations that unit_gate repairs introduce.

### cu_pool: net-reduction enforcement

The single cu_pool trial in this history required delta_total to be negative (−27) before the decision "applied" was recorded (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). Operations on via cell definitions in the cu_pool channel propagate to all instances of that cell, making per-unit violation counts drop simultaneously across multiple placement sites.

## Rule-Specific Repair Guidance

### M2.W.1 (minimum width 18 nm)

No M2.W.1 violations were explicitly triggered or repaired in any recorded trial. All resize_end operations extended polygons outward (increasing length or width), which cannot narrow an existing segment. Avoid resize operations that shrink the low end of a polygon below 18 nm.

### M2.S.1 and M2.S.2 (side and tip-to-side spacing)

The consistent pattern across successful trials is moving or extending M2 segments in the +x direction, which increases side-edge lengths and shifts segments away from neighbors. Positive x moves of 36–136 dbu and +x end extensions of 36–192 dbu all cleared the crop window of new M2.S.1 and M2.S.2 violations (trial:i01.ug.Block3_union_row1.00, trial:i01.ug.Block3_union_row2.01, trial:i01.ug.Block3_union_row5.02, trial:i01.ug.Block3_union_row8.03, trial:i01.ug.leaf_0006.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0012.08, trial:i02.ug.leaf_0002.01). Negative x moves at -36 dbu are not uniformly safe (trial:i03.ug.leaf_0003.02).

### M2.S.7 and M2.S.8 (composite tip-to-tip + parallel run length, and diagonal gap spacing)

No M2.S.7 or M2.S.8 violations were reported as introduced in any trial. The resize_end operations that elongated M2 segments by 36–192 dbu in x (trial:i01.ug.Block3_union_row1.00, trial:i01.ug.Block3_union_row8.03, trial:i02.ug.leaf_0002.01) increased segment run length, which works toward satisfying M2.S.7's requirement that parallel run length be ≥ 35 nm when side spacing is ≤ 32 nm. Extending M2 endpoints in the direction of the wire run is the measured repair direction for M2.S.7 compliance.

### V1.M2.EN.2 and V1.M2.AUX.2 (V1 enclosure by M2)

All unit_gate trials touched M1, M2, and V1 simultaneously via instance moves. The uniform absence of new V1.M2.EN.2 violations across all clean trials (trial:i01.ug.Block3_union_row1.00 through trial:i02.ug.leaf_0002.01 excluding trial:i03.ug.leaf_0003.02) demonstrates that moving an instance in the +x direction preserves V1 enclosure by M2, because M2 and the V1 vias it encloses move together as a rigid unit. When resize_end extends only the M2 polygon without a corresponding V1 move, the enclosure on the extended end increases, which satisfies V1.M2.EN.2 more easily. V1.M2.AUX.2 requires V1 width to match M2 width perpendicular to the M2 length direction; instance moves preserve this by moving both layers together.

### V2.M2.EN.1 (V2 enclosure by M2)

V2.M2.EN.1 violations were reduced via V2 shape resizing in the cu_pool channel (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). Because the enclosure check requires M2 to surround V2 by ≥ 5 nm on at least two opposite sides, repositioning V2 within M2 (move_via_shape) and adjusting V2 extent (resize_via_shape) are the effective repair operations when M2 geometry is not easily widened. This repair acted on a via cell definition, fixing 27 violations in two units simultaneously.

## Iteration-by-Iteration State Transitions

The design state changed at each iteration boundary: iteration 1 operated on state fa7319ee…, iteration 2 on cd809b6a…, iteration 3 on 382d59e7…. The 10 new in-crop violations introduced in the first trial of iteration 3 (trial:i03.ug.leaf_0003.02) represent unresolved M2 DRC debt entering the iteration-3 repair pool. Repairs in iteration 3 and beyond must account for these additional violations in unit leaf_0003.