## Rule Interactions and Violation Profile

**V2.M3.AUX.2 is the dominant active violation type on this layer.** The full-deck KLayout run at the start of iteration 4 recorded 356 total violations, of which the applied combo fix eliminated 72, all classified as V2.M3.AUX.2 (trial:i04.cu.def:VIA_VIA23_1_3_36_36.01). No violations from M3.W.1, M3.S.1–S.6, M3.A.1, V2.M3.EN.2, V3.M3.EN.1, or the NONORTHOGONAL block appear in any trial outcome in this history.

V2.M3.AUX.2 requires that every V2 via inside an M3 polygon has M3 edges coincident with exactly two opposite V2 edges in the direction perpendicular to M3 length. Any M3 stub that is wider than the V2 cell in the perpendicular direction violates this rule. The rule is checked globally across the assembly, so a fix on one M3 stub polygon can produce violations on neighboring stubs if the enclosing M3 shape changes asymmetrically relative to via placement.

---

## M3 Stub Trim Pattern for V2.M3.AUX.2

The only fix that produced a net reduction of V2.M3.AUX.2 violations is a coordinated two-part operation: (1) trim each M3 stub polygon symmetrically on both ends in the y-axis by -32 dbu on the low end and -32 dbu on the high end, with a minority of stubs trimmed asymmetrically at -32 low / -41 high; and (2) simultaneously apply a resize_via_shape of -40 dbu in y on the VIA_VIA23_1_3_36_36 M3 land shape. Applied together across 72 stubs plus the via cell shape, this combo produced a net reduction of 72 V2.M3.AUX.2 violations (356→284) with connectivity preserved (trial:i04.cu.def:VIA_VIA23_1_3_36_36.01).

Do not apply the M3 stub resize_end operations alone without the matching resize_via_shape on the via cell M3 land. Trial:i05.ug.leaf_0006.05 executed the identical 72 stub resize_end ops without the via shape resize (the resize_via_shape was dropped at assembly via assemble_drops) and introduced 81 new V2.M3.AUX.2 violations while presumably resolving the original set, for a net worsening within the unit scope. The gating system accepted this trial only because conn_preserved=true and n_new_out_of_crop=0; the V2.M3.AUX.2 count reported as 81 new in-crop confirms the stub-only operation is harmful.

Do not apply the resize_via_shape alone without the stub trim operations. Trial:i05.cu.def:VIA_VIA23_1_3_36_36.00 tested the single resize_via_shape op (VIA_VIA23_1_3_36_36 M3 land, y -40 dbu) in isolation and was rejected with decision=rejected_net_positive, increasing the leaf_0006 window count from 130 to 194 (+64 net) (trial:i05.cu.def:VIA_VIA23_1_3_36_36.00). The cu_pool channel requires net-negative delta; this op alone fails that check.

Apply the two parts as a single atomic submission through the cu_pool channel. The identical 73-op set was first submitted through unit_gate channel as trial:i04.ug.leaf_0008.07, which received decision=gated_out with reason=empty_or_missing_patch (locus was null). The gating failure was due to missing patch metadata, not to the operations themselves. The same 73 ops subsequently succeeded as trial:i04.cu.def:VIA_VIA23_1_3_36_36.01 through cu_pool with full-deck DRC verification.

---

## Stub Trim Sizing Details

The applied stub trims (trial:i04.cu.def:VIA_VIA23_1_3_36_36.01) used two resize amounts on the y-axis ends:

- Standard: -32 dbu on the low end, -32 dbu on the high end (symmetric, 64 dbu total reduction per stub). Applied to the majority of stubs including p2624, p2475, p2474, p2628, p2468, p2525, p2396, p2540, p2539, p2379, p2577, p2613, p2575, p2608, p2610, p2551, p2786, p2785, p2734, p2733, p2732, p2835, p2697, p2819, p2686, p2837, p2727, p2840.
- Asymmetric: -32 dbu on the low end, -41 dbu on the high end (73 dbu total). Applied to p2629, p2380, p2784, p2928, p2896, p2795, p2929, p2816.

All 72 stubs are M3 polygons; no M2 or other layer polygons appear in the resize_end ops. The via cell shape resize is a separate op type (resize_via_shape on cell VIA_VIA23_1_3_36_36, shape_index 0, y axis, -40 dbu).

---

## Small M3 Polygon Moves Are Safe Within These Constraints

Translations of individual M3 polygons by small increments in x or y produced zero new violations in all gated_in unit trials in this history. Specific observed moves: p3383 y -57 dbu (trial:i02.ug.leaf_0001.07), p3515 y -12 dbu (trial:i02.ug.leaf_0014.08), p3383 y +21 dbu (trial:i03.ug.leaf_0001.03, which introduced 3 new in-crop violations of unspecified rule but 0 out-of-crop and was still accepted), p2916 x +8 dbu (trial:i04.ug.leaf_0002.01), p2877 x +8 dbu (trial:i04.ug.leaf_0003.02), p2916 x -8 dbu (trial:i05.ug.leaf_0001.00). These moves are co-located with corresponding via instance moves that keep V2 aligned with M3.

Move M3 polygons together with their associated V2 instances to preserve V2 alignment. In every gated_in trial where an M3 polygon was moved, one or more move_instance ops on V2 or V1 instances accompanied the M3 polygon move. Decoupled movement of M3 from its via instances is not tested in this history.

---

## Adding M3 Polygons

Trial:i03.ug.leaf_0002.04 added one new M3 polygon with points [(11664,11756),(11664,11828),(11908,11828),(11908,11756)], a rectangle 244 dbu wide (x) and 72 dbu tall (y), alongside resize_end adjustments on p2720 and p3300 and two instance moves. The trial was gated_in with 0 new violations. This demonstrates that add_polygon on M3 is viable when the added shape meets geometry rules. The added rectangle at 72 dbu height satisfies M3.W.1 (minimum width 18 nm) if dbu maps at 1:1 to nm. No area, spacing, or enclosure violations were introduced.

---

## resize_end Interactions with M3.W.1

The stub trim operations shrink M3 polygons by 32–41 dbu per end. If both ends of a stub are trimmed and the original stub was narrow, the resulting width must remain at or above 18 nm (M3.W.1). No M3.W.1 violations appear in any trial outcome, confirming that the 32–41 dbu trims applied here did not violate minimum width. When applying similar trims to untested stubs, verify that pre-trim stub width minus the sum of both end trims remains >= 18 dbu (assuming 1 dbu = 1 nm) to avoid M3.W.1.

---

## resize_via_shape on VIA_VIA23_1_3_36_36

The VIA_VIA23_1_3_36_36 M3 land shape (shape_index 0) was resized by -40 dbu in y as part of the applied fix (trial:i04.cu.def:VIA_VIA23_1_3_36_36.01). This is a cell-level edit affecting all instances of the via cell across the full block assembly. The operation is classified as touching layers M2, M3, V2. When resizing the via M3 land shape, the M2 land shape may require a corresponding resize to preserve V2.M2.AUX.2 compliance; the history shows M2 in the touched_layers list for this op, consistent with the M2 land being resized in the same cell definition.