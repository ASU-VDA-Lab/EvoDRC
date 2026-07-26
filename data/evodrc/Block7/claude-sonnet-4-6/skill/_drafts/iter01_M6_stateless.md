## Via Enclosure Violations (V5.M6.EN.2, V5.M6.AUX.2): Repair via V5 Shape Adjustment

The only repair recorded for M6 at iteration 1 targeted cell `VIA_VIA56_2_2_66_58` and operated exclusively on V5 shapes, not on M6 geometry directly. All eight operations were y-axis moves and y-axis resizes on V5 shapes (shape indices 0–3); M6 was listed in `touched_layers` because the enclosure checks couple V5 placement to M6 boundaries (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02).

The repair pattern was: move each V5 shape by ±132 dbu on the y-axis (outer two shapes moved +132 dbu, inner two moved −132 dbu, achieving symmetric repositioning), then resize every shape by +512 dbu on y. This two-step sequence—translate then expand—resolved V5.M6.EN.2 (minimum 11 nm enclosure of V5 by M6 on two opposite sides) and V5.M6.AUX.2 (V5 width must exactly match M6 width perpendicular to M6 length) without touching M6 polygons. Total violation count dropped by 80 across four measurement windows (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02).

The four affected windows split into two categories: `unit:Block7_union_row21` and `unit:Block7_union_row22` each improved by 6 and 2 violations respectively, while `unit:leaf_0103` and `unit:leaf_0104` each improved by 36 violations, indicating that the via cell instance was placed repeatedly in the leaf cells and that fixing the cell definition propagated improvement to all instantiation sites (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02).

Connectivity was preserved across all eight operations (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02). Do not modify M6 polygons to fix V5.M6.EN.2 or V5.M6.AUX.2 when adjusting V5 shape placement and extent is sufficient; the measured repair confirms that V5-only edits clear both rules while keeping the net intact.

## Rule Interaction: V5.M6.AUX.2 Width-Match Constraint

V5.M6.AUX.2 requires that each V5 via be exactly as wide as its enclosing M6 polygon in the direction perpendicular to M6's length. Because M6 routes horizontally (minimum horizontal width 44 nm per M6.W.5, minimum vertical width 32 nm per M6.W.1), the perpendicular direction is vertical (y-axis). The measured repair resized V5 shapes by +512 dbu in y, implying the pre-repair V5 shapes were narrower in y than the enclosing M6 polygon. When V5.M6.AUX.2 fires alongside V5.M6.EN.2, apply the y-axis resize to V5 first; if the enclosure margin (V5.M6.EN.2 requires ≥11 nm on two opposite sides) is also violated, the y-axis translation of ±132 dbu per shape corrects the offset (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02).

## M6 Grid and Track Constraints: No Violations Observed, Context for Future Repairs

No repairs to M6 polygon geometry (M6.W.1–M6.W.5, M6.S.1–M6.S.5, M6.AUX.1–M6.AUX.4) were recorded at iteration 1. However, the DRC rules impose constraints that must be respected when any future repair does move or resize M6:

- M6 horizontal edges must land on a 32 nm grid (M6.AUX.1). Any y-coordinate adjustment to an M6 edge must be a multiple of 32 nm (32 dbu if 1 dbu = 1 nm).
- Minimum-width M6 tracks (vertical width ≤ ~34 nm after the M6.AUX.2 sizing test of ±17 nm) must have their centerlines on the horizontal routing grid: pitch 256 dbu, offset 64 dbu, with the additional constraint that the base polygon edges are at 128 dbu multiples (M6.AUX.2 offgrid_cl definition). Repairs that shift a min-width M6 track in y must snap the track centerline to this grid.
- M6 must not bend (M6.AUX.3): all M6 polygons must be rectilinear with no interior corners in the 0–90 degree range. Do not introduce L-shapes or jogs when merging or extending M6 to fix enclosure.
- Outside edges of wide M6 polygons (vertical extent > ~34 nm after ±17 nm erosion/dilation) must not coincide with any routing track edge occupied by a separate min-width M6 track (M6.AUX.4).
- Forbidden vertical widths include any even integer multiple of 32 nm (64, 128, 192, 256, 320, 384, 448, 512, 576, 640 nm — M6.W.3) and the subset 96, 224, 352, 480, 608 nm that span an even number of routing tracks (M6.W.4). When resizing M6 vertically, check the resulting height against both forbidden sets before committing.
- Minimum vertical spacing between M6 edges is 32 nm (M6.S.1); minimum horizontal spacing is 40 nm (M6.S.2). Tip-to-tip spacing on adjacent tracks is 40 nm regardless of parallel run length sharing (M6.S.3, M6.S.4). Minimum parallel run length on adjacent tracks is 44 nm (M6.S.5).