## M5 Vertical-Edge Grid (M5.AUX.1 / M5.AUX.2)

M5.AUX.1 requires all M5 vertical edges to land on a 24 nm (24 dbu) grid. M5.AUX.2 further constrains minimum-width M5 tracks: their centerlines must fall on a 192 dbu pitch with a 48 dbu offset from the origin. Corrections to these rules require x-axis moves that are exact multiples of 24 dbu applied in the direction that brings the edge to the nearest legal grid position.

In trial:i03.ug.leaf_0002.01 the fix group "fix_m5aux1" moved polygon p1060 by -64 dbu in x together with all instances sharing that track; the trial was gated_in (n_new_in_crop=8). Moving p1060 in the opposite direction (+32 dbu in x) was rejected twice: it was dropped at assembly as "cu_pool:rejected_net_positive" in trial:i02.ug.leaf_0002.01 and independently rejected as rejected_net_positive (delta_total=+28) in trial:i02.cu.def:VIA_VIA45_1_2_58_58.00, where it caused leaf_0003 to jump from 17 to 46 violations (delta=+29). The -64 dbu direction was the only corrective direction; the +32 dbu direction was strictly harmful.

When correcting M5.AUX.1 or M5.AUX.2, the polygon move must be paired with moves of all instances co-located on that track. Moving the M5 polygon alone without the companion via and instance moves introduces V4.M5.AUX.2 and enclosure violations, as demonstrated by the dropped operations in trial:i02.ug.leaf_0002.01.

## M5 Vertical Dimension (M5.W.5 / M5.S.2)

M5.W.5 sets the minimum vertical width at 44 nm (44 dbu); M5.S.2 sets the minimum vertical spacing at 40 nm (40 dbu). Shrinking an over-tall M5 shape in y is effective when sufficient vertical clearance already exists to neighboring shapes. In trial:i01.cu.def:VIA_VIA45_1_2_58_58.02 a y-axis resize of -88 dbu on M5 shape_index 0 inside cell VIA_VIA45_1_2_58_58 was applied and reduced violations by 20 total (leaf_0018: 32→21, leaf_0019: 35→26). A competing five-operation trial that instead resized V4 and M4 shapes in x lost the tournament at delta_total=-18 (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01), confirming the single y-axis M5 resize is the more efficient repair.

Before applying a y-axis resize, verify the resulting vertical height remains ≥ 44 dbu to avoid triggering M5.W.5, and that the gap to any adjacent M5 shape in y meets M5.S.2 (≥ 40 dbu).

## M5 Horizontal Width Constraints (M5.W.1 / M5.W.2 / M5.W.3 / M5.W.4)

M5.W.1 requires horizontal width ≥ 24 nm. M5.W.2 limits horizontal width to 480 nm. M5.W.3 prohibits widths that are even integer multiples of 24 nm: 48, 96, 144, 192, 240, 288, 336, 384, 432, and 480 nm are all forbidden. M5.W.4 additionally prohibits widths of 72, 168, 264, 360, or 456 nm (spans that equal an even number of minimum-width routing tracks).

In trial:i02.ug.leaf_0003.02 polygon p1059 was resized by +64 dbu at its low x-end and +320 dbu at its high x-end; the trial was gated_in with zero new out-of-crop violations, confirming the resulting width was legal. When sizing M5 horizontal width, target odd-multiple values not appearing in either the M5.W.3 or M5.W.4 forbidden lists. Legal odd-multiple candidates include 24, 120, 216, 312, and 408 nm.

## M5 Horizontal Spacing (M5.S.1 / M5.S.3 / M5.S.4 / M5.S.5)

M5.S.1 requires horizontal spacing between M5 edges ≥ 24 nm and also a general 1 dbu minimum. M5.S.3 requires tip-to-tip spacing ≥ 40 nm for polygons on adjacent tracks that do not share parallel run length. M5.S.4 requires tip-to-tip spacing ≥ 40 nm for polygons that do share parallel run length. M5.S.5 requires minimum parallel run length ≥ 44 nm for polygons on adjacent tracks.

The horizontal resize of p1059 in trial:i02.ug.leaf_0003.02 (gated_in, zero new out-of-crop violations) modified run-length geometry without introducing new spacing violations, demonstrating that end-extension resizes are viable when the resulting edge positions satisfy the 24 nm grid (M5.AUX.1) and the spacing checks above. No trial introduced or corrected M5.S.3–S.5 violations in isolation; monitor these rules whenever horizontal extents change.

## Via Enclosure Interactions with M5 (V4.M5.EN.2 / V4.M5.AUX.2 / V5.M5.EN.1)

V4.M5.EN.2 requires M5 to enclose V4 by ≥ 11 nm on two opposite sides. V4.M5.AUX.2 requires V4 to be exactly the same width as M5 in the direction perpendicular to M5 length (i.e., V4 x-width must equal M5 x-width for a horizontal M5 run). V5.M5.EN.1 requires M5 to enclose V5 by ≥ 11 nm on at least two opposite sides.

The y-axis resize in trial:i01.cu.def:VIA_VIA45_1_2_58_58.02 shrinks the M5 shape in the dimension parallel to the routing direction, preserving the x-width equality that V4.M5.AUX.2 checks; that trial was applied cleanly. The grouped x-moves in trial:i03.ug.leaf_0002.01 co-moved all instances on the track to keep V4 vias aligned with their enclosing M5 shapes. Any x-move on an M5 polygon that is not matched by the same delta on co-located V4/V5 instances will violate V4.M5.AUX.2 or the enclosure rules.

## M5 Bending Prohibition (M5.AUX.3)

M5.AUX.3 prohibits any bend in an M5 polygon (no interior corner in the 0–90° angle range). All accepted operations across trials i01.cu.def:VIA_VIA45_1_2_58_58.02, i02.ug.leaf_0003.02, and i03.ug.leaf_0002.01 were pure end-resizes or rigid translations that preserved rectilinear, unbent M5 geometry. Any resize sequence that would leave a polygon with both horizontal and vertical interior corners is illegal under M5.AUX.3 and must not be issued.

## Tournament Outcome: Single M5 Resize Preferred Over Multi-Layer Via Reshape

When both a multi-operation V4/M4 x-resize approach and a single M5 y-resize approach target the same violation cluster, the single M5 y-resize is the better candidate. In the tournament between trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 (five operations on V4 and M4, delta_total=-18, lost_tournament) and trial:i01.cu.def:VIA_VIA45_1_2_58_58.02 (one operation on M5, delta_total=-20, applied), the M5-only approach won on both violation count and operation count. Prefer single-layer M5 adjustments over coordinated multi-layer via reshapes when the violation source is on M5.

## Grouped Operation Atomicity

trial:i03.ug.leaf_0002.01 demonstrates that M5.AUX.1/AUX.2 fixes must be submitted as an atomic group that includes the M5 polygon move and every instance on the affected vertical routing track. Partial submissions — moving only the polygon or only some instances by the same delta — are either dropped by the assembler (as in trial:i02.ug.leaf_0002.01) or increase the net violation count (as in trial:i02.cu.def:VIA_VIA45_1_2_58_58.00). The group label "fix_m5aux1" on the accepted set in trial:i03.ug.leaf_0002.01 confirms the repair engine treats these as a single atomic commit.