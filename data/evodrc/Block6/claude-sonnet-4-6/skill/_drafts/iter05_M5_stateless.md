## M5 Layer Geometry

M5 is a horizontal routing layer. All polygons must be rectilinear and axis-aligned; the GEOMETRY.NONORTHOGONAL check fires on any edge with an angle not in {0°, 90°, 180°, 270°}. M5.AUX.3 additionally prohibits any corner that introduces a 0-to-90 degree turn within the metal itself, so M5 shapes are straight bars only — no L-shapes, T-shapes, or bends.

### Horizontal Width (x-axis)

The minimum horizontal width is 24 nm (M5.W.1) and the maximum is 480 nm (M5.W.2).

M5.W.3 forbids widths that are exact even-integer multiples of 24 nm. The illegal set is {48, 96, 144, 192, 240, 288, 336, 384, 432, 480} nm.

M5.W.4 additionally forbids widths of {72, 168, 264, 360, 456} nm (the 3×, 7×, 11×, 15×, 19× multiples of 24 nm). Combined with M5.W.3, the smallest allowable widths above the minimum are 24 nm, 120 nm, 216 nm, 312 nm, and 408 nm.

When extending a polygon end in x to increase wire width, verify the resulting width is not in either forbidden set before committing the operation. Trial i05.ug.leaf_0002.01 resized polygon ends in x by +168 nm, +132 nm, and +100 nm and was accepted (n_new_in_crop=22); those deltas each reached a target width outside both forbidden sets.

### Vertical Width (y-axis)

The minimum vertical width is 44 nm (M5.W.5). Resize operations on polygon ends in y must result in a height of at least 44 nm. Trial i02.ug.leaf_0010.06 applied resize_end operations of +24 nm and +72 nm in y across multiple polygons (polygon_ids p1826, p1833, p1831, p1792, p1786, p1806, p1845, p1844, p1857, p1734, p1757, p1749) and was accepted; all resulting heights satisfied the 44 nm floor.

### Vertical Edge Grid (M5.AUX.1)

All vertical edges of M5 polygons must land on a 24 nm x-grid. Move and resize operations in x must be chosen so that every resulting vertical edge position is a multiple of 24 nm. The instance moves in trial i03.ug.leaf_0003.02 and trial i04.cu.def:VIA_VIA56_2_2_66_58.00 used +32 nm and -16 nm x-shifts; those deltas are not themselves multiples of 24 nm, confirming that the repair engine chooses deltas based on the offset needed to bring a specific edge from its current (already potentially off-grid) position to a legal grid position — the delta is not required to be grid-aligned, only the endpoint.

### Minimum-Width Track Placement (M5.AUX.2)

The M5.AUX.2 rule checks that minimum-width M5 tracks (those with horizontal width ≈ 24 nm, selected by the erosion/dilation filter `m5 - m5.sized(-13.nm, 0).sized(13.nm, 0)`) whose bounding-box edges are both divisible by 96 nm have their x-centerlines at positions satisfying x_center ≡ 48 (mod 192 nm). The base divisibility pre-filter means not all minimum-width tracks are checked; the rule targets only those already positioned at 96 nm-aligned boundaries. No trial in this history records a repair specifically addressing an M5.AUX.2 violation in isolation.

### Wide Polygon Outside Edges (M5.AUX.4)

Wide M5 polygons (those that survive the `m5.sized(-13.nm, 0).sized(13.nm, 0)` erosion) must not have their outside vertical edges coincide with the edges of any minimum-width routing track. When extending a wide polygon in x, confirm that the new outside edge does not land on a vertical edge position used by a nearby thin M5 wire. Trial i05.ug.leaf_0002.01 extended three wide polygon ends in x by +168 nm, +132 nm, and +100 nm and was accepted, indicating those target positions were clear of thin-track edges.

## Horizontal Spacing

The minimum horizontal spacing between M5 polygons is 24 nm (M5.S.1). This is checked both projection-filtered (parallel edges only) and as a bare Euclidean 1 nm floor, so both parallel-edge and tip-to-corner approaches are caught.

## Vertical Spacing and Parallel Run Rules

Minimum vertical spacing between M5 polygon edges is 40 nm (M5.S.2). Minimum tip-to-tip spacing — both for polygon pairs that do not share a parallel run (M5.S.3) and for those that do (M5.S.4) — is 40 nm. The minimum parallel run length between adjacent same-track polygons is 44 nm (M5.S.5).

To resolve vertical spacing violations, apply y-axis end-resize operations in multiples of the 24 nm pitch. Trial i02.ug.leaf_0010.06 used resize_end deltas of +24 nm and +72 nm in y across 12 polygons and was accepted (n_new_in_crop=26). For instance-level adjustments, trial i03.ug.leaf_0002.01 applied y-axis instance moves of ±48 nm and ±96 nm across 20 instances (n_new_in_crop=35); those multiples of 48 nm satisfy both the 44 nm vertical width floor and the 40 nm spacing rule simultaneously.

## Via Enclosure — V4 on M5

M5 must enclose any V4 via lying inside it by at least 11 nm on two opposite sides (V4.M5.EN.2). The V4 width measured perpendicular to the M5 run direction must equal the M5 width at that point (V4.M5.AUX.2).

When M5 is too narrow to provide 11 nm enclosure in x, apply a symmetric via split: move one V4 shape by -116 nm in x and another by +116 nm in x, then expand both by +384 nm in x. Trial i01.cu.def:VIA_VIA45_1_2_58_58.01 applied exactly this pattern (two move_via_shape ops at ±116 nm, two resize_via_shape ops at +384 nm on V4, plus a +152 nm resize on the M4 landing pad) and achieved delta_total=-52.

## Via Enclosure — V5 on M5

M5 must enclose any V5 via it covers by at least 11 nm on two opposite sides (V5.M5.EN.1).

The equivalent symmetric split for V5 uses ±116 nm moves combined with +320 nm x-expansion per shape. Trial i01.cu.def:VIA_VIA56_2_2_66_58.02 applied this to four V5 shapes (four move_via_shape ops alternating -116/+116 nm, four resize_via_shape ops at +320 nm) and achieved delta_total=-16.

When M5 polygons shift in y and carry their hosted V5 with them, the V5 must be repositioned and resized in y to maintain enclosure. Trial i04.cu.def:VIA_VIA56_2_2_66_58.00 moved four V5 shapes in y by ±132 nm and expanded each by +512 nm in y after M5 polygons shifted vertically, and achieved delta_total=-14. The y-resize absorbs the differential motion between adjacent M5 tracks that move by different amounts.

## X-Axis Paired Shift Pattern

When resolving horizontal spacing or track-alignment violations on M5 polygons that share a region, a paired bidirectional shift is effective: one group moves +32 nm in x while an adjacent group moves -16 nm in x. Trial i03.ug.leaf_0003.02 applied this pattern to two M5 polygons (p1682 at -16 nm, p1683 at +32 nm) along with 16 instance moves carrying associated M5/M6 content, and was accepted (n_new_in_crop=26). Trial i04.cu.def:VIA_VIA56_2_2_66_58.00 repeated the identical +32/-16 nm polygon shift (p1684, p1685) with 14 instance moves and achieved delta_total=-14. Both trials involved layers M4, M5, M6, V4, and V5, confirming that the shift must propagate through the full local via stack.

## Multi-Layer Coherence

Every trial that modifies M5 geometry also modifies at least one adjacent layer. The minimum touched-layer set for an M5 repair is two layers: M5 plus either M4 or M6 (typically via a shared via cell). All five trials that touched M5 also touched the via and adjacent metal on both sides of the via:

- trial i01.cu.def:VIA_VIA45_1_2_58_58.01: M4, M5, V4
- trial i01.cu.def:VIA_VIA56_2_2_66_58.02: M5, M6, V5
- trial i02.ug.leaf_0010.06: M3, M4, M5, V3, V4
- trial i03.ug.leaf_0002.01: M3, M4, M5, V3, V4
- trial i03.ug.leaf_0003.02: M4, M5, M6, V4, V5
- trial i04.cu.def:VIA_VIA56_2_2_66_58.00: M4, M5, M6, V4, V5
- trial i05.ug.leaf_0002.01: M1, M2, M5, M6, V1, V5

Move M5 shapes only as part of a coherent group operation that also repositions the landing pads and via shapes above and below.

## Connectivity Preservation

Every trial in the measured history carried `conn_preserved: true` and was applied or gated_in. The unit_gate channel enforces `n_new_out_of_crop: 0` in all accepted decisions (trial i02.ug.leaf_0010.06, trial i03.ug.leaf_0002.01, trial i03.ug.leaf_0003.02, trial i05.ug.leaf_0002.01). Do not accept an M5 repair that introduces a new out-of-crop connectivity change, regardless of DRC violation count improvement.