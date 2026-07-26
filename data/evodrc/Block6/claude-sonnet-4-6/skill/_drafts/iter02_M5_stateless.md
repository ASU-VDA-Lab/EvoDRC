## Via Enclosure Repairs (V4.M5.EN.2 / V4.M5.AUX.2 / V5.M5.EN.1)

Fixing via-to-M5 enclosure violations requires a paired **move + resize** on the via shapes, not a resize alone. In trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, each V4 shape pair was first spread outward by ±116 dbu in x (shape_index 0 moved −116 dbu, shape_index 1 moved +116 dbu), then both were widened by +384 dbu in x. In trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 the same pattern applied to four V5 shapes: ±116 dbu moves followed by +320 dbu resizes. Applying a resize without the accompanying spread move leaves the via centroid misaligned with the M5 track centerline and fails V4.M5.AUX.2 / V5.M5.EN.1 co-requirements.

The spread step (±116 dbu) positions the outer edges of each sub-via shape to coincide exactly with the outer edges of the M5 wire, satisfying V4.M5.AUX.2 (V4 width must equal M5 width perpendicular to M5 run direction). The subsequent resize step (384 dbu for V4; 320 dbu for V5) extends each sub-shape along the M5 run axis to provide the ≥11 nm two-sided enclosure required by V4.M5.EN.2 and V5.M5.EN.1. Always apply both steps together: trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 and trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 each yielded negative delta totals (−52 and −16 respectively) only when both move and resize ops were committed as a unit.

When a via cell contains multiple sub-shapes (e.g., the four V5 shapes in trial:i01.cu.def:VIA_VIA56_2_2_66_58.02), apply the ±116 dbu spread and the resize to every sub-shape; partial application leaves residual V4.M5.AUX.2 or V5.M5.EN.1 violations on the untouched shapes.

M4 may also require a coordinated resize when V4 is modified. In trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, M4 shape_index 0 was resized +152 dbu in x alongside the V4 operations. This co-modification maintains the enclosure on the M4 side of the via cell and prevents secondary violations from propagating upward to M5.

## M5 Polygon End Resizing (M5.W.5 / M5.S.2 / M5.AUX.1)

M5 wire endpoints must be adjusted in integer multiples of 24 dbu to remain on the 24 nm vertical-edge grid enforced by M5.AUX.1. In trial:i02.ug.leaf_0010.06, all resize_end operations on M5 polygons used delta values of exactly ±24 dbu or ±72 dbu (3×24 dbu): polygons p1826, p1786, p1845, p1757 were extended by +72 dbu at the high end; p1733, p1792 were retracted by −72 dbu at the low end; p1833, p1806, p1844, p1749 were extended by +24 dbu; p1831, p1857 were retracted by −24 dbu at the low end. No odd or non-grid delta appeared among the M5 ops in that trial. Always snap resize_end deltas to multiples of 24 dbu when modifying M5 wire tips.

The minimum vertical width of M5 is 44 nm (M5.W.5). When retracting a wire tip, verify that the resulting vertical span does not drop below 44 nm; the retractions of −24 dbu seen in trial:i02.ug.leaf_0010.06 were safe because the affected polygons had sufficient pre-existing vertical extent.

## Coordinated Instance + Polygon Moves (M5.AUX.2 / M5.S.1 / M5.S.2)

Unit-level repairs that touch M5 require coordinating instance moves with polygon end resizes in the same commit. In trial:i02.ug.leaf_0010.06, 24 instance moves (delta_dbu in y: ±24 or ±72) were bundled with 12 polygon resize_end ops (also ±24 or ±72 in y), all in a single n_ops=36 operation. Splitting these into separate commits risks intermediate states where M5 wires violate M5.S.2 (minimum 40 nm vertical spacing) or M5.AUX.2 (minimum-width track centerline alignment) before the paired polygon adjustment closes the gap.

All instance move deltas in trial:i02.ug.leaf_0010.06 were multiples of 24 dbu (24 or 72 dbu), consistent with the M5.AUX.2 routing-track pitch of 192 dbu with 48 dbu offset. Do not move instances by amounts that are not multiples of 24 dbu; doing so displaces M5 track centerlines off the required grid.

The gate channel (unit_gate) accepted the trial:i02.ug.leaf_0010.06 set as gated_in with conn_preserved=true and 26 new violations entering the crop window and 0 exiting outside crop. A large n_ops count does not preclude acceptance; connectivity preservation is the binding constraint, not operation count.

## Width-Rule Compliance During Resize (M5.W.1 / M5.W.2 / M5.W.3 / M5.W.4)

No trial in this history violated M5.W.1–W.4 after repair. The via resize deltas used (384 dbu for V4, 320 dbu for V5 in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 and trial:i01.cu.def:VIA_VIA56_2_2_66_58.02) operate on via sub-shapes, not directly on M5 wires; the M5 wire widths are governed by the M5 polygon geometry, which was not directly resized in those trials. When M5 polygons are resized in x (horizontal), verify post-repair that the resulting width is not an even integer multiple of 24 nm (M5.W.3) and does not equal 72, 168, 264, 360, or 456 nm (M5.W.4). The M5 end resizes in trial:i02.ug.leaf_0010.06 were in y only and therefore cannot trigger M5.W.3 or M5.W.4.

## No-Bend Constraint (M5.AUX.3)

M5 may not bend (M5.AUX.3). All M5 operations in this history operate on rectilinear wire ends (resize_end in y) or leave M5 topology unchanged while adjusting vias. Do not introduce corner points into M5 polygons when performing tip extensions or retractions; restrict resize_end ops to the single axis of the wire's run direction.

## AUX.4 Wide-M5 Track Constraint

Wide M5 shapes must not have vertical edges that align with the centerline of an adjacent minimum-width (1x) M5 routing track (M5.AUX.4). The instance and polygon adjustments in trial:i02.ug.leaf_0010.06 moved M5 endpoints in y, not x, so track-edge alignment in x was not disturbed. When any repair shifts M5 geometry in x — including indirect shifts via enclosing cell moves — confirm that the resulting vertical edges of wide M5 polygons do not land on a 1x routing-track edge position (pitch 192 dbu, offset 48 dbu).