## Effective M2 Repair Operations

**Instance moves on X-axis are the primary successful repair strategy for M2.** Across trials trial:i03.ug.whole_design.00 and trial:i05.ug.whole_design.00, collective X-axis instance moves in the range of ±36 to ±72 dbu resolved M2 (and co-located M1/V1) violations without introducing new violations and with full connectivity preservation. Both trials gated in with zero new violations in crop. Moves at ±64 dbu (trial:i03.ug.whole_design.00) and mixed ±36/44/48/72 dbu (trial:i05.ug.whole_design.00) were both accepted.

**M2 polygon end extension (resize_end, axis=x, end=high) reliably resolves enclosure and spacing violations.** trial:i04.ug.whole_design.00 extended multiple M2 polygon high-X ends by 128–192 dbu (polygons p1214, p1178, p1211, p1216 at +172, +192, +172, +128 dbu respectively) and gated in with zero new violations. A low-X-end retraction of +48 dbu (p1301, axis x, end low) was included in the same accepted batch. This extension pattern directly addresses V1.M2.EN.2 (5 nm minimum enclosure of V1 by M2 on two opposite sides) and V2.M2.EN.1 (5 nm minimum enclosure of V2 by M2 on two opposite sides), since extending the M2 wire end in the via's axial direction increases the enclosure margin without affecting perpendicular edges.

**Small Y-axis end extensions of M2-adjacent shapes are safe.** trial:i04.ug.whole_design.00 included +9 dbu Y-axis high-end extensions on polygons p1543 and p1458 (touching M2/M3/M4 layers) with no new violations introduced.

## Via Shrink Operations Do Not Repair M2 Violations

Shrinking a via shape in the Y dimension does not reduce M2 DRC violations. trial:i04.cu.def:VIA_VIA23_1_3_36_36.00 attempted a −40 dbu Y-axis resize on VIA_VIA23_1_3_36_36 (touching M2 and V2 enclosure geometry); the cu_pool gate rejected it as `rejected_net_positive` with the violation count unchanged at 122 before and after. The correct repair for V2.M2.EN.1 (M2 must enclose V2 by ≥5 nm on two opposite sides) and V1.M2.EN.2 (M2 must enclose V1 by ≥5 nm on two opposite sides) is to extend the M2 polygon end toward the via, not to shrink the via, as confirmed by the accepted X-axis end extensions in trial:i04.ug.whole_design.00.

## Spacing Rule Hierarchy and Thresholds

The M2 spacing rules form a cascade by edge-length category. The thresholds that separate rule domains are 24 nm and 36 nm:

- Edges longer than 36 nm: side-to-side minimum is 18 nm (M2.S.1).
- Tip edge (≤36 nm) opposite a side edge (>36 nm): minimum tip-to-side is 25 nm (M2.S.2). The 7 nm gap over M2.S.1 is significant; moving a polygon by 64 dbu (≈64 nm) in X—as done in trial:i03.ug.whole_design.00—is more than sufficient to clear either threshold in a single step.
- Both tips in the 24–36 nm range: minimum tip-to-tip is 27 nm (M2.S.3).
- One tip 24–36 nm, one tip <24 nm: minimum tip-to-tip is 31 nm (M2.S.5).
- Both tips <24 nm: minimum tip-to-tip is 31 nm (M2.S.4).

M2.S.6 adds an independent Euclidian corner-to-corner floor of 20 nm for any pair of M2 polygons not already covered by the projection-mode spacing rules.

## Compound Rule M2.S.7: Forbidden 18 nm Tip-to-Tip + Narrow Side Context

M2.S.7 prohibits any configuration where a tip-to-tip gap of 18 nm in the vertical direction co-exists with a side-to-side spacing of ≤32 nm in the horizontal direction, and additionally requires that horizontal parallel run length be ≥35 nm whenever the side spacing is ≤32 nm. This rule interacts with instance placement density. The batched X-axis moves in trial:i03.ug.whole_design.00 and trial:i05.ug.whole_design.00 that shifted groups of instances by +44 to +72 dbu or −64 to −72 dbu simultaneously adjust both the tip gap and the side spacing context, making coordinated multi-instance moves the correct repair tool for M2.S.7 rather than single-polygon edits that could resolve one dimension while worsening the other.

## Compound Rule M2.S.8: Diagonal Gap Spacing

M2.S.8 requires that Euclidian center-to-center distance between tip-to-tip gaps on different M2 tracks be ≥80 nm. Gap centers are computed by shrinking each 18 nm tip-to-tip gap region by 8.5 nm per side. No trial in the measured history targeted M2.S.8 directly, but the multi-instance X-axis moves in trial:i03.ug.whole_design.00 and trial:i05.ug.whole_design.00—which simultaneously repositioned 22–32 instances—are the correct mechanism for adjusting diagonal gap offsets across tracks, since M2.S.8 is a cross-track spatial constraint that requires changing relative positions of multiple wires together.

## V1 and V2 Enclosure: Extension Over Shrink

For V1.M2.EN.2 (two-opposite-side enclosure of V1 by M2, ≥5 nm each), the rule requires that for every V1 edge in each orthogonal direction, at least one pair of opposite M2 edges encloses by ≥5 nm (or one side may be 0 nm if the other is ≥5 nm). Repair must extend the M2 polygon along the wire axis. trial:i04.ug.whole_design.00 extended M2 high-X ends by 128–192 dbu and was accepted; the rejected trial:i04.cu.def:VIA_VIA23_1_3_36_36.00 shrank the via in Y and was not. Never shrink the via shape to resolve enclosure violations; always extend the enclosing M2 shape.

For V1.M2.AUX.2 (V1 must match M2 width in the direction perpendicular to M2 length), the constraint is geometric identity: the V1 width perpendicular to the M2 run direction must equal the M2 width. This is satisfied automatically when V1 is generated aligned to the M2 track width and move_instance ops shift both M2 and V1 together, as in trial:i03.ug.whole_design.00 and trial:i05.ug.whole_design.00 (both listed V1 and M2 in touched_layers and preserved connectivity).

## Minimum Width and Area

M2.W.1 sets the minimum M2 width at 18 nm. M2.A.1 sets the minimum area at 504 nm². A minimum-width wire of 18 nm meets the area floor only if its length is at least 28 nm (504/18 = 28). Any resize_end retraction must not reduce polygon length below 28 nm when the wire is at minimum width. The low-end retraction in trial:i04.ug.whole_design.00 (p1301, axis x, end low, +48 dbu—a retraction of the low coordinate) was accepted, confirming that end retractions are viable provided the resulting shape clears both M2.W.1 and M2.A.1.

## Orthogonality Constraint

All M2 edges must be axis-aligned (0° or 90°). The NONORTHOGONAL block applies to every drawing layer including M2. All successful operations in the measured history (move_instance and resize_end on axis-aligned ends) preserve orthogonality by construction. Never introduce diagonal edges through partial polygon reshape operations.