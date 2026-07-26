**V1.W.1 — Minimum Width**

V1.W.1 mandates a minimum width of 18 nm along the M2 length direction. The 32 move_instance operations in trial:i03.ug.whole_design.00 (all in the x-direction, ±64 dbu) were accepted with conn_preserved=true and zero new violations; preserve the 18 nm floor on any resize or placement of V1.

**V1.S.1 — Projected Spacing**

V1.S.1 enforces projected spacing between V1 mask geometries: 18 nm on the same M2 track or on aligned parallel tracks, and 27 nm on parallel tracks that are not aligned. The deck classifies vias into NEC (full-flush M2 edges, no end-cap) and WEC (partial coincidence, 5 nm end-cap) and computes separate masks before applying the spacing check. trial:i03.ug.whole_design.00 moved 30 instances +64 dbu and 2 instances −64 dbu in x and was accepted; trial:i05.ug.whole_design.00 moved instances at +48, +44, +36, −72, and −64 dbu in x and extended five M2 polygons by 44 dbu at their high-x end, and was also accepted. Do not shrink inter-via x-pitch below the V1.S.1 bounds when moving in the direction parallel to M2 runs.

**V1.S.2 — Euclidean Corner Spacing, Both WEC**

When both V1 instances carry a 5 nm M2 end-cap (WEC class), the minimum euclidean corner-to-corner clearance between their masks is 23 nm (deck projection threshold 16.4 nm). The acceptance of trial:i03.ug.whole_design.00 and trial:i05.ug.whole_design.00, both of which touched M2 and V1 across moved and resized cells, confirms this diagonal constraint is active; do not place two WEC vias such that their mask corners are closer than 23 nm euclidean.

**V1.S.3 — Euclidean Corner Spacing, Both NEC**

When both V1 instances lack the 5 nm end-cap (NEC class), the euclidean corner-to-corner minimum between their expanded NEC masks is 30 nm (deck projection threshold 16.12 nm). The rule fires only on violations not already captured by the projection check. trial:i03.ug.whole_design.00 and trial:i05.ug.whole_design.00 both preserved this clearance across all moved instances; do not place two NEC vias with mask corners closer than 30 nm euclidean.

**V1.S.4 — Euclidean Corner Spacing, Mixed WEC/NEC**

For a WEC–NEC pair, the euclidean separation threshold between the respective masks is 27 nm (deck projection threshold 17.11 nm); as with V1.S.3, only violations not already caught by the projection metric are reported. trial:i03.ug.whole_design.00 and trial:i05.ug.whole_design.00, both touching V1 and M2 across multiple cell moves, confirmed no mixed-class corner violations were introduced; do not allow WEC and NEC mask corners to approach within 27 nm euclidean.

**V1.M1.EN.1 — M1 Enclosure of V1**

M1 must enclose each V1 on two opposite sides: one opposite-side pair at ≥5 nm and the orthogonal opposite-side pair at ≥2 nm (both measured by projection). A V1 not meeting both requirements on at least one axis pair, or placed outside M1 entirely, triggers this rule. trial:i03.ug.whole_design.00 and trial:i05.ug.whole_design.00 both moved instances on layers M1, M2, and V1 together and were accepted with conn_preserved=true and no new violations; maintain the 5 nm / 2 nm enclosure relationship when repositioning any V1 or its enclosing M1, moving M1 together with V1 so the enclosure is preserved.

**V1.M2.EN.2 — M2 Enclosure of V1**

M2 must enclose V1 on two opposite sides with either a 5 nm & 5 nm pair or a 5 nm & 0 nm pair (projection). The zero end-cap is valid only when that V1 edge is exactly coincident with an M2 edge (flush); a non-zero enclosure below 1 dbu on any non-flush side also triggers the rule. trial:i03.ug.whole_design.00 preserved M2 enclosure across all 32 moved instances; trial:i05.ug.whole_design.00 preserved it across moves at varied dbu distances and five resize_end operations that extended M2 polygon high-x ends by 44 dbu. When moving V1 or M2, keep at least one axis pair at 5 nm & 5 nm, or keep the zero-enclosure edge exactly flush with the M2 boundary. When a move shifts V1 toward the high end of an M2 segment and risks reducing enclosure, extending the M2 high end via resize_end to restore the required enclosure is valid, as confirmed by trial:i05.ug.whole_design.00.

**V1.AUX.1 — V1 Inside M1 ∩ M2**

Every V1 polygon must lie entirely within the geometric intersection of M1 and M2. trial:i03.ug.whole_design.00 and trial:i05.ug.whole_design.00 both moved cells on M1, M2, and V1 simultaneously and were accepted with conn_preserved=true; when repositioning instances, move the enclosing M1 and M2 geometries together with V1 to preserve containment inside M1 ∩ M2. When an M2 extension is needed after a via move, resize_end on the M2 polygon in the same direction as the move restores the containment requirement, as confirmed by trial:i05.ug.whole_design.00.

**V1.M2.AUX.2 — V1 Width Matches M2 Width**

V1 must be exactly as wide as the M2 track in the direction perpendicular to the M2 run; the deck requires each V1 inside M2 to share at least two coincident M2 edges. trial:i03.ug.whole_design.00 accepted all 32 x-direction moves without V1.M2.AUX.2 errors; trial:i05.ug.whole_design.00 accepted 19 move_instance operations and 5 resize_end operations (all on the x-axis, end=high) without V1.M2.AUX.2 errors, confirming that resize_end on M2 at the end parallel to the M2 run does not alter the perpendicular width match. Avoid any edit that widens or narrows V1 relative to its enclosing M2 stripe.

**GEOMETRY.NONORTHOGONAL**

All V1 edges must be axis-aligned (0° or 90°). Any non-orthogonal edge angle triggers the global NONORTHOGONAL check applied to every drawing layer. trial:i03.ug.whole_design.00 performed only rectilinear move_instance operations (±64 dbu in x) and was accepted; trial:i05.ug.whole_design.00 performed rectilinear move_instance and resize_end operations and was accepted. Do not introduce diagonal or angled edges on V1 geometry.

**Repair Strategy Observed**

trial:i03.ug.whole_design.00 applied 32 move_instance operations (30 at +64 dbu, 2 at −64 dbu in x); all touched M1, M2, and V1 together; decision gated_in with conn_preserved=true, n_new_in_crop=0, n_new_out_of_crop=0.

trial:i05.ug.whole_design.00 applied 22 operations over the same layer set (M1, M2, V1): 19 move_instance steps at varying positive displacements (+48, +44, or +36 dbu) for the forward-moving group and at negative displacements (−72 or −64 dbu) for 3 instances (i0433, i0082, i0258); and 5 resize_end operations on M2 polygons (p1255, p1270, p1295, p1309, p1320), each extending the high-x end by 44 dbu. The trial was gated_in with conn_preserved=true, n_new_in_crop=0, n_new_out_of_crop=0.

Two repair classes are now measured for this layer:

1. **Coordinated instance moves** — translate M1, M2, and V1 together in x (positive or negative) to resolve projected-spacing violations without breaking connectivity. Move magnitudes observed: +36, +44, +48, −64, −72 dbu.

2. **M2 polygon resize_end** — extend the high end of an M2 polygon along the x-axis (axis=x, end=high) after an associated instance move, restoring M2 enclosure of V1 (V1.M2.EN.2, V1.AUX.1) when the move shifts a via toward the trailing M2 boundary. All five observed resize_end deltas were 44 dbu, matching the move delta of the instances they accompany. Apply resize_end only on the same axis and end-direction as the triggering move, and verify that the extension does not violate V1.S.1 spacing to neighboring mask geometries.