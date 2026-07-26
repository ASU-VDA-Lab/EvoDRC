## Rule Geometry and Constraint Summary

**V1.W.1 — Minimum width 18 nm (parallel to M2 run direction)**
V1 must be at least 18 nm wide along the direction of the M2 track it sits on. Width is measured along the M2 run axis, consistent with V1.M2.AUX.2's requirement that V1 exactly match M2 width perpendicular to that axis.

**V1.S.1 — Minimum projection spacing via mask construction**
The deck constructs per-instance masks that extend M2 end-cap regions by 5 nm. Three spacing sub-cases apply based on track geometry: 18 nm same-track, 27 nm parallel-not-aligned, 18 nm parallel-aligned. The mask-building logic classifies each V1 instance as either full-end-cap (v1_nec: all edges coincident with M2 edges) or partial-end-cap (v1_wec: at least one edge not on an M2 edge). V1_nec masks receive a 5 nm extension on all four sides of the M2 coincident region; v1_wec masks receive the extension only on the free end plus a 5 nm sizing. The three check sub-expressions operate on v1_mask_nm2_nte (non-M2 orthogonal edges of the mask minus M2), v1_maskav_nciem (V1-intersected mask edges not on M2), and v1_mask globally.

**V1.S.2 — Euclidean corner-to-corner spacing, both instances with 5 nm end-cap: 23 nm (deck operand 16.4 nm)**
Applies only between two v1_wec instances. The deck tolerance of 16.4 nm on the mask accounts for the 5 nm sizing on each wec_mask, giving a physical corner distance of ≈23 nm.

**V1.S.3 — Euclidean corner-to-corner spacing, both instances without end-cap: 30 nm (deck operand 16.12 nm)**
Applies only between two v1_nec instances. Violations that also appear in the projection-space check are excluded (projection violations are already covered by V1.S.1). The 16.12 nm deck threshold maps to ≈30 nm physical corner distance given mask expansion.

**V1.S.4 — Euclidean corner-to-corner spacing, mixed end-cap: 27 nm (deck operand 17.11 nm)**
Applies between a v1_wec_mask and a v1_nec_mask. As with V1.S.3, projection-coincident violations are excluded to avoid double-counting with V1.S.1. The 17.11 nm deck value maps to ≈27 nm physical corner distance.

**V1.M1.EN.1 — M1 enclosure of V1: 5 nm on one opposite pair, 2 nm on the other**
The deck tests separately for horizontal (angle=0) and vertical (angle=90) edges. A V1 instance passes if it has 5 nm M1 enclosure on one axis and 2 nm on the other, in either orientation. A V1 not inside M1 at all fires unconditionally.

**V1.M2.EN.2 — M2 enclosure of V1: 5&5 nm or 5&0 nm on opposite sides**
M2 must enclose each V1 edge by 5 nm on one side of a pair and by 5 nm or 0 nm (flush/coincident) on the opposing side. A V1 not inside M2 fires unconditionally. Any non-zero enclosure edge that is less than 5 nm also fires via the second sub-check (`v1_en2_ep_zero`).

**V1.AUX.1 — V1 must be inside M1 ∩ M2**
V1 must reside entirely within the geometric intersection of M1 and M2. Any part of V1 outside either layer fires independently.

**V1.M2.AUX.2 — V1 width must exactly match M2 width perpendicular to M2 length**
V1 inside M2 must have exactly two edges coincident with M2 side edges (the edges perpendicular to the M2 run direction). V1 that is inside M2 but lacks two such coincident opposite edges fires this rule.

**GEOMETRY.NONORTHOGONAL — All V1 edges must be 0° or 90°**
Any V1 edge with an angle outside the set {0°, 90°, 180°, 270°} fires the nonorthogonal check. All V1 geometry must be strictly rectilinear.

---

## Measured Repair Operations

All three recorded trials for Block6 whole-design were accepted (decision: gated_in, n_new_in_crop: 0, n_new_out_of_crop: 0) with connectivity preserved. The patterns below are drawn from those accepted operation sets.

**Co-moving instances with M2 polygon-end extension is the primary accepted repair pattern.**
In trial:i03.ug.whole_design.00, eight V1-carrying instances (i0536, i0410, i0446, i0361, i0239, i0093, i0015, i0404) were each shifted +96 dbu in x. Each instance shift was paired with a resize_end on the high-x end of the corresponding M2 polygon (p2071, p2020, p2072, p2086, p1946, p1903, p1991, p1903) extending the M2 end by 116–152 dbu. The M2 extension exceeded the instance shift (116–152 > 96 dbu), maintaining or increasing the enclosure margin required by V1.M2.EN.2 on the direction of travel. Apply co-moves — shift the V1 instance and simultaneously extend the M2 polygon end in the direction of travel by at least the shift amount — when resolving V1.S.1 or V1.S.2/S.3/S.4 spacing violations by lateral repositioning (trial:i03.ug.whole_design.00).

**Fine-grain lateral moves (13–48 dbu) successfully resolve marginal spacing violations.**
In trial:i05.ug.whole_design.00, multiple instance/polygon pairs were moved by +13 dbu (i0446/p2072, i0093/p1903, i0410/p2020, i0239/p1946, i0536/p2071, i0361/p2086, i0404/p2019) and by +37 dbu (i0459/p2050, i0122/p1911, i0481/p2049, i0078/p1914, i0071/p1907, i0159/p2046, i0138/p1927, i0060/p1910, i0324/p2067, i0512/p2030) without introducing new violations. These sub-pitch moves confirm that the repair increment does not need to align to any coarse grid; move only as far as needed to satisfy the spacing check (trial:i05.ug.whole_design.00).

**Small-cluster negative moves (−12 dbu) are accepted when balancing spacing across multiple instances.**
In trial:i05.ug.whole_design.00, thirteen instances (i0137, i0162, i0177, i0187, i0225, i0226, i0244, i0357, i0362, i0367, i0370, i0375, i0377) were shifted −12 dbu while other instances in the same trial moved in the positive direction. The combined result passed with no new violations. Coordinated bidirectional adjustments — pulling one cluster negative while pushing another positive — can resolve spacing violations without exceeding the enclosure limits on either side (trial:i05.ug.whole_design.00).

**Shortening an M2 polygon end (resize_end with negative delta) is accepted when enclosure margin permits.**
In trial:i05.ug.whole_design.00, M2 polygon ends p1831, p1786, and p1806 were trimmed by −20 dbu (resize_end, axis=x, end=high) in the same trial that touched V1. This was accepted without new V1.M2.EN.2 violations, confirming that trimming a polygon end is safe when the resulting enclosure still satisfies the 5 nm minimum (or 0 nm flush). Do not trim an M2 end beyond the existing enclosure margin minus 5 nm unless the V1 end is flush at that edge (trial:i05.ug.whole_design.00).

**Symmetric M2 polygon resizes (op: resize, both sides) by small amounts do not disturb V1.M2.AUX.2.**
In trial:i04.ug.whole_design.00, polygons p1990, p1923, and p1920 received symmetric x-axis resizes of 10 dbu while V1 was in the touched layers, and the trial was accepted with no new violations. Because V1.M2.AUX.2 requires V1 to exactly match M2 width perpendicular to M2 length, a symmetric resize on M2 alone (without a matching resize on V1) is viable only when those polygons are not in the V1 zone, or when V1 is contained within instances that co-resize. Symmetric resize operations in passing trials confirm this pattern is safe in the accepted context (trial:i04.ug.whole_design.00).

**Instance moves accompanied by matching polygon lateral translations are consistently accepted across all trials.**
In all three trials (trial:i03.ug.whole_design.00, trial:i04.ug.whole_design.00, trial:i05.ug.whole_design.00), every move_instance targeting a V1-touching cell was accompanied either by a resize_end on the M2 feeding polygon or by a lateral move (op: move) on the M2/M1 polygon at the same or correlated delta. No isolated instance move without any polygon adjustment appears in the accepted operation sets for V1-touching instances. Always pair a V1 instance move with a corresponding M2 polygon adjustment to maintain V1.M2.EN.2 and V1.AUX.1 compliance.