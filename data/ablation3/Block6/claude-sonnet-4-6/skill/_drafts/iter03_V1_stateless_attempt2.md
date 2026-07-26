The history is already provided inline. Writing the knowledge section now based solely on the single measured trial `i03.ug.whole_design.00` and the DRC rules.

---

**Repair Pattern: Paired M2 High-End Extension With V1 Instance Move**

In trial:i03.ug.whole_design.00, the accepted repair (decision: gated_in, conn_preserved=true) consists of `resize_end` operations on M2 polygons (axis x, end high) followed immediately by `move_instance` operations on cell instances. Seven of the nine moved instances — i0536, i0410, i0446, i0361, i0239, i0093, i0015 — each received a paired M2 high-x extension before the instance was displaced. The remaining two instances, i0404 and i0471, were moved without any paired M2 resize and the repair still passed. Apply a paired M2 high-end extension for every V1 instance move that would otherwise leave V1 closer to the M2 boundary than the 5 nm enclosure required by V1.M2.EN.2; do not add an M2 extension when the existing M2 margin already absorbs the displacement with enclosure to spare, as demonstrated by i0404 and i0471 in trial:i03.ug.whole_design.00.

**M2 Extension Must Exceed V1 Displacement**

All nine instance moves in trial:i03.ug.whole_design.00 applied delta [96, 0] dbu in x. The seven paired M2 resize_end deltas were 116 dbu (polygons p2020, p1946, p1903, p1991) or 152 dbu (polygons p2071, p2072, p2086) — both values strictly greater than the 96 dbu instance displacement. The minimum observed excess is 20 dbu (116 − 96 = 20 dbu ≈ 2 nm); the maximum is 56 dbu (152 − 96 = 56 dbu ≈ 5.6 nm). V1.M2.EN.2 requires M2 to enclose V1 by at least 5 nm on both M2-length-parallel sides (5 & 5 or 5 & 0 nm). Set the M2 high-end extension to at least V1_displacement_dbu + 50 dbu (5 nm) to guarantee V1.M2.EN.2 compliance; trial:i03.ug.whole_design.00 shows both 116 dbu and 152 dbu extensions accepted with a 96 dbu V1 move.

**V1 Must Remain Co-Located With M2 Width (V1.M2.AUX.2 and V1.AUX.1)**

V1.M2.AUX.2 requires V1 to match M2's width exactly along the axis perpendicular to the M2 run direction; V1.AUX.1 requires V1 to lie fully inside M1 ∩ M2. In trial:i03.ug.whole_design.00, M2 high-x extensions appear in the operation list immediately before the matching `move_instance` for each paired case (e.g., p2071 extended then i0536 moved, p2020 extended then i0410 moved). Extend M2 before or simultaneously with the instance displacement to keep V1 inside M2 at every stage and satisfy V1.AUX.1 and V1.M2.AUX.2.

**M1 Enclosure Must Be Checked After V1 Moves**

The touched_layers field of trial:i03.ug.whole_design.00 lists M1 alongside M2 and V1. Because `move_instance` relocates all geometry within the cell instance, M1 shapes inside the instance co-move with V1 by the same delta [96, 0] dbu. V1.M1.EN.1 requires M1 to enclose V1 by 5 nm and 2 nm on two opposite sides. The repair in trial:i03.ug.whole_design.00 was accepted with conn_preserved=true, confirming that co-moving M1 with V1 via `move_instance` kept V1.M1.EN.1 satisfied for all nine instances. Do not apply a standalone V1 shape move that separates V1 from its co-located M1; use `move_instance` so that M1 and V1 shift together and V1.M1.EN.1 is preserved by construction.

**Uniform Same-Direction Instance Moves Preserve V1 Spacing**

All nine instance moves in trial:i03.ug.whole_design.00 applied the identical delta [96, 0] dbu, and the repair was accepted without introducing V1.S.1, V1.S.2, V1.S.3, or V1.S.4 violations. Because every inter-instance distance is unchanged when all instances shift by the same vector, the spacing checks based on v1_mask, v1_nec_mask, and v1_wec_mask — which are derived from V1 shape positions — return the same values before and after the move. Use a uniform displacement for all V1 instances in a region to avoid introducing spacing violations; trial:i03.ug.whole_design.00 confirms this for nine instances moved 96 dbu in x simultaneously.

**V1.W.1 Is Not Affected by Instance Move**

`move_instance` does not alter V1 polygon geometry; it only translates position. V1.W.1 (minimum width 18 nm along M2 length) depends on V1 polygon dimensions, not position. No resize of V1 polygons occurred in trial:i03.ug.whole_design.00, and no V1.W.1 violation arose, confirming that width compliance is unaffected by pure instance displacement operations.

**GEOMETRY.NONORTHOGONAL Is Not Affected by Axis-Aligned Ops**

All operations in trial:i03.ug.whole_design.00 are axis-aligned: `resize_end` on axis x and `move_instance` with delta [96, 0] — both orthogonal. The repair passed without triggering V1.GEOMETRY.NONORTHOGONAL. Apply only axis-aligned resize and move operations on V1 and M2 to avoid introducing non-orthogonal edges, which the NONORTHOGONAL block flags for every layer.