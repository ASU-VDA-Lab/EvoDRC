## Repair Strategy Overview

The sole measured repair for V4 at iteration 5 (trial:i05.cu.def:VIA_VIA45_1_2_58_58.00) targeted cell `VIA_VIA45_1_2_58_58` and produced a net reduction of 158 violations across the affected windows (leaf_0002: −2, leaf_0013: −81, leaf_0014: −75). The repair was accepted (`decision: applied`) with connectivity preserved (`conn_preserved: true`). All prescriptive guidance below is grounded in that single record.

---

## Effective Operation Bundle for V4 Spacing and Width Violations

The 5-operation bundle applied in trial:i05.cu.def:VIA_VIA45_1_2_58_58.00 demonstrates the canonical repair sequence for V4 vias in array cells when spacing or width violations cluster across multiple via instances:

1. **Move V4 shape (shape_index 0) inward on X** by −116 dbu, then **resize V4 shape (shape_index 0) on X** by +232 dbu.
2. **Move V4 shape (shape_index 1) outward on X** by +116 dbu, then **resize V4 shape (shape_index 1) on X** by +232 dbu.
3. **Resize M5 shape (shape_index 0) on X** by −152 dbu to restore AUX.2 width matching.

The move-then-resize pairing for each V4 shape (trial:i05.cu.def:VIA_VIA45_1_2_58_58.00, ops 0–1 and ops 2–3) achieves a net symmetric expansion: for shape_index 0, the −116 dbu move shifts the shape's reference point inward while the +232 dbu resize extends the opposite edge outward by +116 dbu, yielding a net +116 dbu expansion on the outer side without displacing the inner edge further toward the adjacent via. This pattern avoids worsening V4.S.1 / V4.S.2 / V4.S.3 spacing between the two via instances while simultaneously satisfying V4.W.1 (24 nm minimum width along M5 length) and V4.M4.EN.1 / V4.M5.EN.2 (11 nm enclosure on opposite sides).

Do not apply the resize alone without the paired move: trial:i05.cu.def:VIA_VIA45_1_2_58_58.00 shows that both ops are issued together for each shape, indicating that a symmetric resize from the original center would violate inter-via spacing constraints on one side.

---

## M5 Must Be Co-Adjusted When V4 is Resized (V4.M5.AUX.2)

Rule V4.M5.AUX.2 requires V4 to be exactly the same width as M5 along the direction perpendicular to M5 length. Whenever V4 shapes are resized on the X axis, the overlying M5 shape must be simultaneously adjusted to preserve this exact-width match. In trial:i05.cu.def:VIA_VIA45_1_2_58_58.00, op 4 resizes M5 (shape_index 0) by −152 dbu on X immediately after the two V4 expansions (+232 dbu each). Always include a compensating M5 resize in the same operation bundle as any V4 resize; omitting it will produce or preserve V4.M5.AUX.2 violations.

The M5 resize delta (−152 dbu) is not identical to the V4 resize delta (+232 dbu per shape), confirming that the relationship is determined by the actual geometry of the enclosing M5 shape and the two V4 shapes together, not by a simple 1:1 ratio. Compute the required M5 adjustment from the post-move V4 extents rather than copying the V4 resize delta.

---

## Touched-Layer Scope for v45-fix Group

All five operations in trial:i05.cu.def:VIA_VIA45_1_2_58_58.00 belong to the `v45-fix` group, and the `touched_layers` record lists `["M4", "M5", "V4"]`. M4 appears in `touched_layers` even though no explicit M4 operation is listed among the five ops. This indicates that M4 geometry is evaluated for enclosure compliance (V4.M4.EN.1) as a side-effect of V4 movement, and the solver reads M4 state to confirm the 11 nm two-opposite-sides enclosure is maintained after the V4 moves. Do not exclude M4 from DRC re-evaluation after any V4 move or resize, even when no M4 op is issued.

---

## Via Array Cells: Both Instances Must Be Repaired Together

Cell `VIA_VIA45_1_2_58_58` contains at least two V4 via instances (shape_index 0 and shape_index 1 are both operated on in trial:i05.cu.def:VIA_VIA45_1_2_58_58.00). Repairing only one instance of a multi-via array cell leaves V4.S.1 / V4.S.2 / V4.S.3 inter-via spacing violations unresolved; the bundle must address all instances in the cell in a single atomic application. The −158 total violation reduction achieved by trial:i05.cu.def:VIA_VIA45_1_2_58_58.00 was produced by operating on both shape_index 0 and shape_index 1 together.

---

## Violation Concentration in Large Leaf Windows

In trial:i05.cu.def:VIA_VIA45_1_2_58_58.00, 98.7% of the total violation delta (156 of 158) came from two windows: leaf_0013 (−81) and leaf_0014 (−75). Windows leaf_0002, leaf_0005, leaf_0009, leaf_0010, and leaf_0011 were either unchanged or reduced by only 2. Prioritize repair of V4 violations that appear in large-count leaf windows; a single cell repair targeting the right via definition can eliminate violations across many instances instantiated throughout the design.

---

## Locus and Cell Targeting

The repair locus `[1728, 2068, 28728, 28172]` in trial:i05.cu.def:VIA_VIA45_1_2_58_58.00 corresponds to a bounding box covering the violation cluster in the `cu_pool` channel of Block7. The repair was issued against the via cell definition (`target: def:VIA_VIA45_1_2_58_58`) rather than an instance, so the fix propagated to all instantiations of that cell across the design. When the same via definition drives violations in multiple leaf windows simultaneously, target the cell definition (`def:`) rather than individual instances to achieve global violation reduction in a single bundle.