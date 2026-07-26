## Accepted Repair Patterns

**x-axis end-resize via unit_gate** — Both unit_gate trials accepted `resize_end` operations on M4 polygons along the x-axis when connectivity was preserved and no new DRC markers appeared inside the crop. Extending the high end of p1216 by 132 dbu was accepted (trial:i02.ug.Block1_union_row12.00). Shrinking the low end of p1187 by 44 dbu, in combination with deleting p1211, was also accepted (trial:i05.ug.leaf_0003.02). Apply `resize_end` on M4 when connectivity is intact and the crop introduces no new violations.

**delete + resize_end combination** — Removing an M4 polygon (p1211) and resizing the end of an adjacent M4 polygon (p1187 low end, −44 dbu) in a single two-operation set resolved the violation within a 168 dbu × 308 dbu crop without introducing new errors (trial:i05.ug.leaf_0003.02). Use this combination when a short M4 segment occupies space needed by a neighboring polygon's correct end position.

## Rejected Repair Patterns

**Multi-polygon M4 moves via cu_pool with positive net delta** — Moving p1143 (+32 dbu x) and p1142 (−16 dbu x) through the cu_pool channel was rejected because the net DRC count across units increased by 16: unit leaf_0007 improved by 2 but unit leaf_0008 worsened by 18, yielding delta_total = +16 (trial:i03.cu.def:VIA_VIA45_1_2_58_58.00). Do not issue M4 moves through cu_pool when the summed per-unit delta is positive. The same operation set also resized M5 via shapes; the cross-layer entanglement in the op set did not prevent the rejection from applying.

## Locus and Channel Observations

The two accepted unit_gate trials share the same y-range (14400–14708 dbu) but differ in x-span: trial:i02.ug.Block1_union_row12.00 covers 5332 dbu in x while trial:i05.ug.leaf_0003.02 covers only 168 dbu. The narrower locus in i05 required combining a deletion with a resize to clear the crop cleanly. The rejected cu_pool trial (trial:i03.cu.def:VIA_VIA45_1_2_58_58.00) covers a substantially larger locus (12528 dbu × 12064 dbu) and touches five layers (M4, M5, M6, V4, V5); large multi-layer loci increase exposure to cross-unit error propagation that the per-unit delta check penalizes.

## Geometric Constraints

**Width** — M4.W.1 sets the minimum vertical width at 24 nm. M4.W.2 caps vertical width at 480 nm. M4.W.3 prohibits vertical widths equal to even integer multiples of 24 nm: 48, 96, 144, 192, 240, 288, 336, 384, 432, and 480 nm are all forbidden. M4.W.4 additionally prohibits vertical widths of 72, 168, 264, 360, and 456 nm. M4.W.5 sets the minimum horizontal width at 44 nm; the 44 dbu x-axis resize delta used in trial:i05.ug.leaf_0003.02 matches this floor exactly — resize steps smaller than 44 dbu along x risk a M4.W.5 violation on the resulting shape.

**Spacing** — M4.S.1 requires at least 24 nm vertical spacing between M4 polygon edges. M4.S.2 requires at least 40 nm horizontal edge-to-edge separation. M4.S.3 and M4.S.4 both require at least 40 nm tip-to-tip spacing between M4 polygons on adjacent tracks, regardless of whether the polygons share a parallel run length. M4.S.5 requires at least 44 nm of parallel run length when two M4 polygons occupy adjacent tracks.

**Grid and track alignment** — M4.AUX.1 requires all M4 horizontal edges to lie on a 24 nm grid. M4.AUX.2 requires minimum-width M4 tracks to center on horizontal routing tracks at a pitch of 192 dbu with offset 48 dbu (base 96 dbu). M4.AUX.3 prohibits any bend in M4; all M4 shapes must be strictly rectilinear with no 0°–90° interior corners. M4.AUX.4 prohibits wide M4 polygon outside edges from coinciding with routing track edges.

**Via enclosure** — V3.M4.EN.2 requires V3 to be enclosed by M4 by at least 11 nm on two opposite sides. V3.M4.AUX.2 requires V3 width to exactly match M4 width in the direction perpendicular to M4 length. V4.M4.EN.1 requires V4 inside M4 to be enclosed by at least 11 nm on two opposite sides.

**Orthogonality** — GEOMETRY.NONORTHOGONAL prohibits non-orthogonal edges on M4; all edges must be at 0° or 90°.