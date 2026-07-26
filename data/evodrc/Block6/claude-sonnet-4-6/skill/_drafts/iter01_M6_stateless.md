## Via Enclosure Repairs via V5 x-Axis Adjustment

Repositioning and enlarging V5 shapes in the x-axis inside a shared via cell resolved M6-related violations across multiple units simultaneously. In trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 (channel: cu_pool, decision: applied), four V5 shapes inside cell `VIA_VIA56_2_2_66_58` were first spread apart by ±116 dbu in x and then each resized by +320 dbu in x. The touched layers were M5, M6, and V5. The outcome was a net reduction of 16 violations: −8 in `unit:leaf_0019` and −8 in `unit:leaf_0020`, with connectivity fully preserved. Because the same via cell is instantiated in at least two units, a single repair to the cell definition propagated clean enclosure geometry to both sites.

Rules V5.M6.EN.2 and V5.M6.AUX.2 govern the relationship between V5 and M6 in this layer. V5.M6.EN.2 requires at least 11 nm of M6 enclosure on two opposite sides of each V5; V5.M6.AUX.2 requires that V5 width in the direction perpendicular to the M6 run exactly matches the M6 width (via coincident edges on two sides). The x-axis spread-and-enlarge pattern in trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 is consistent with simultaneously satisfying both rules: spreading shapes along the wire axis addresses the enclosure margin, while the resize extends shapes to the M6 edge to satisfy the coincident-edge requirement.

When a via cell is shared across units and exhibits symmetric enclosure shortfalls on opposite x-faces, applying paired move + resize on the V5 shapes in x (with equal and opposite moves and equal resizes) is the repair pattern confirmed to apply cleanly without introducing new violations (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02).

## M6 Vertical End Resizing Produces New Violations

Resizing M6 polygon endpoints in the y-axis introduced 55 new violations within the crop window while preserving connectivity. In trial:i01.ug.leaf_0020.09 (channel: unit_gate, decision: gated_in, reason: conn_preserved), two M6 polygons were modified:

- `p2107`: low end moved −96 dbu (bottom contracted), high end moved +32 dbu (top extended).
- `p2106`: low end moved −16 dbu (bottom contracted), high end moved +112 dbu (top extended).

The trial was gated in (not rejected for connectivity failure) but produced `n_new_in_crop: 55` new violations and zero new violations outside the crop. The large count of new in-crop violations after vertical end adjustments is consistent with M6's strict vertical-dimension rule set. M6.W.1 mandates a minimum vertical width of 32 nm; M6.W.2 caps vertical width at 640 nm; M6.W.3 forbids vertical widths that are exact even integer multiples of 32 nm (64, 128, 192, 256, 320, 384, 448, 512, 576, 640 nm); M6.W.4 forbids widths that span an even number of minimum-width routing tracks vertically (96, 224, 352, 480, 608 nm). M6.AUX.2 further constrains that minimum-width (1x) M6 tracks must have their centerlines on the horizontal routing grid at pitch 256 dbu, offset 64 dbu (with base alignment 128 dbu). M6.AUX.1 requires all M6 horizontal edges to fall on a 32 nm grid.

Vertical end moves that are not multiples of 32 dbu risk violating M6.AUX.1 (the −16 dbu move on p2106's low end is not a multiple of 32 nm and may directly trigger grid violations on that edge). Moves that shift the centerline of a 1x M6 segment off the 256 dbu routing pitch grid violate M6.AUX.2. Any resulting width that lands on a forbidden value from M6.W.3 or M6.W.4 adds further violations. The 55 new violations from trial:i01.ug.leaf_0020.09 confirm that M6 vertical end moves must be quantized to 32 nm and must be checked against M6.AUX.2 centerline alignment after each adjustment.

Do not apply vertical end delta values that are not multiples of 32 dbu to M6 polygons; trial:i01.ug.leaf_0020.09 demonstrates that even a −16 dbu move on one end produces a large burst of new violations.

## M6 No-Bend and Orthogonality Constraints Are Absolute

M6.AUX.3 prohibits any 0°–90° or 90°–0° corner (bend) in an M6 polygon; all M6 shapes must be rectilinear wire segments without L-turns or T-junctions that would appear as corners in the hull. The GEOMETRY.NONORTHOGONAL rule independently prohibits any edge with angle outside the set {0°, 90°, 180°, 270°}. No trial in this iteration created or repaired a bend or non-orthogonal edge on M6; these rules appear as hard structural constraints that repair operations must respect. All ops in trial:i01.ug.leaf_0020.09 used `resize_end` on y-axis endpoints of existing straight M6 segments, consistent with maintaining rectilinear shapes.

## Track Alignment for 1x M6 Segments

M6.AUX.2 enforces that minimum-width M6 segments (those that cannot survive a vertical erosion of 17 nm and re-dilation, i.e., segments with vertical extent < 34 nm after merging) must have centerlines on the grid defined by pitch = 256 dbu, offset = 64 dbu, with base = 128 dbu. M6.AUX.4 prohibits the outer horizontal edges of wide M6 polygons from coinciding with the routing track edges occupied by adjacent 1x M6 segments.

The y-axis end resizes in trial:i01.ug.leaf_0020.09 altered polygon extents without an explicit centerline check, which is consistent with the observed 55 new violations. When resizing 1x M6 segment endpoints, verify post-move that (centerline_y − 64) mod 256 == 0 to satisfy M6.AUX.2.

## Horizontal Spacing and Width Are Distinct from Vertical

M6.W.5 sets a minimum horizontal width of 44 nm. M6.S.2 sets a minimum horizontal spacing of 40 nm. M6.S.3 covers tip-to-tip spacing on adjacent tracks without shared run (40 nm), M6.S.4 covers tip-to-tip spacing on adjacent tracks with shared parallel run (40 nm), and M6.S.5 sets a minimum parallel run length of 44 nm. No repair in this iteration directly targeted horizontal width or spacing; the cu_pool trial (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02) operated on V5 x-positions and sizes within a via cell and did not change M6 polygon geometry directly, yet it was the only trial that reduced the violation count. This outcome isolates horizontal M6 spacing/width violations as not the primary issue at this locus — the enclosure-related V5/M6 rules (V5.M6.EN.2, V5.M6.AUX.2) were the target of the successful fix.