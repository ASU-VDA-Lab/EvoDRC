**Repair Effectiveness: Resize vs. Move**

A `resize_via_shape` operation contracting M5 by −96 dbu along the x-axis for via cell `VIA_VIA56_2_2_66_58`, which touched V5, produced zero net reduction in total violation count and was rejected as non-improving (trial:i01.cu.def:VIA_VIA56_2_2_66_58.01). Do not apply shrink resizes to via shapes as a strategy for resolving V5 violations; the measured outcome from that operation confirms no violation improvement results from this approach (trial:i01.cu.def:VIA_VIA56_2_2_66_58.01).

**Instance and Polygon Moves**

A batch of 57 move operations on instances and polygons touching layers M3, M4, M5, M6, V3, V4, and V5 was accepted with connectivity preserved and with no new V5-rule violations recorded in the crop window (trial:i02.ug.whole_design.00). The accepted deltas in that trial included both x- and y-axis displacements across a range of values (−96 to +96 dbu) applied to instances and individual polygons. No V5-specific rule appeared in the new-in-crop violation breakdown, confirming that these moves did not introduce fresh V5 width, spacing, enclosure, containment, or width-match violations (trial:i02.ug.whole_design.00).