All trials that modified M2 geometry completed without introducing new M2 DRC violations: trial:i01.ug.whole_design.00, trial:i02.ug.whole_design.00, trial:i04.ug.whole_design.00, trial:i04.cu.def:VIA_VIA23_1_3_36_36.00, and trial:i05.ug.whole_design.00. The observations below are drawn directly from those records.

---

**M2.W.1 — Minimum width 18 nm**

No M2.W.1 violation was created across all trials. Polygon endpoint extensions applied in trial:i01.ug.whole_design.00 (p879 +48 dbu in y, p910 +8 dbu in x and +20 dbu in y) and trial:i05.ug.whole_design.00 (p951 +128 dbu in x, p955 +128 dbu in x) all added material to existing shapes. Operations that strictly increase a polygon dimension along one axis do not narrow any edge and therefore cannot trigger M2.W.1.

---

**M2.S.1 — Side-to-side spacing 18 nm (both edges > 36 nm)**

Instance moves of 36 dbu and 72 dbu in x executed in trial:i02.ug.whole_design.00 and trial:i04.ug.whole_design.00, and moves up to 136 dbu in x in trial:i01.ug.whole_design.00, produced no M2.S.1 errors. When an instance move co-displaces M2 and its neighboring layers together, the relative spacing within the instance is preserved; only cross-instance gaps change. The gap increments used in these trials left all side-to-side spacings above 18 nm.

---

**M2.S.2 — Tip-to-side spacing 25 nm (one edge <= 36 nm, other > 36 nm)**

No M2.S.2 violation was generated in any trial. The x-axis end extensions of p951 and p955 by 128 dbu in trial:i05.ug.whole_design.00 did not produce tip-to-side errors, confirming that the space into which those ends were extended exceeded 25 nm in the projection direction.

---

**M2.S.3 — Tip-to-tip spacing 27 nm (both edges 24–36 nm)**

No M2.S.3 violation appeared in any trial. End extensions in trial:i01.ug.whole_design.00 and trial:i05.ug.whole_design.00 did not bring any pair of edges in the 24–36 nm range closer than 27 nm.

---

**M2.S.4 and M2.S.5 — Tip-to-tip spacing 31 nm (narrow tips < 24 nm)**

No M2.S.4 or M2.S.5 violation was introduced. The end resize and instance-move operations in trial:i01.ug.whole_design.00, trial:i02.ug.whole_design.00, trial:i04.ug.whole_design.00, and trial:i05.ug.whole_design.00 all maintained tip-to-tip clearances above the 31 nm floor for edges below 24 nm.

---

**M2.S.6 — Corner-to-corner spacing 20 nm (Euclidean)**

No M2.S.6 violation was triggered in any trial. This rule fires only when two polygons are close enough diagonally (< 20 nm Euclidean) while their projection separation stays >= 20 nm. All instance moves in trial:i01.ug.whole_design.00, trial:i02.ug.whole_design.00, trial:i04.ug.whole_design.00, and trial:i05.ug.whole_design.00 kept corner separations above the Euclidean threshold.

---

**M2.S.7 — Forbidden tip-to-tip 18 nm gap co-located with side spacing <= 32 nm**

No M2.S.7 violation was generated. The rule requires that wherever a tip-to-tip gap of 18 nm exists between vertical M2 edges, the parallel run length of neighboring horizontal edges must be >= 35 nm if the side-to-side spacing is <= 32 nm. The horizontal end extensions of p951 and p955 by 128 dbu in trial:i05.ug.whole_design.00 increased run length beyond the 35 nm threshold and were accepted without error.

---

**M2.S.8 — Diagonal gap center-to-center spacing 80 nm**

No M2.S.8 violation was produced. This rule flags Euclidean distances below 80 nm between centers of tip-to-tip gaps on different tracks (gaps are identified by shrinking each 18 nm gap by 8.5 nm per side). None of the polygon or instance operations in trial:i01.ug.whole_design.00, trial:i02.ug.whole_design.00, trial:i04.ug.whole_design.00, trial:i04.cu.def:VIA_VIA23_1_3_36_36.00, or trial:i05.ug.whole_design.00 created a new gap pair violating this threshold.

---

**M2.A.1 — Minimum area 504 nm²**

No M2.A.1 violation was introduced. All polygon resize operations in the recorded trials (trial:i01.ug.whole_design.00: p879, p910; trial:i04.cu.def:VIA_VIA23_1_3_36_36.00: p891–p897 shrunk in y by 64 dbu; trial:i05.ug.whole_design.00: p951, p955) either added material or applied a shrink that left the surviving polygon area above 504 nm². The shrink of p891–p897 by 64 dbu in y in trial:i04.cu.def:VIA_VIA23_1_3_36_36.00 did not produce an M2.A.1 error, indicating those shapes remained above the area floor after the reduction.

---

**V1.M2.EN.2 — Enclosure of V1 by M2 on two opposite sides (5 nm each, or 5 nm and 0 nm)**

No V1.M2.EN.2 violation was generated in any trial. Instance moves in trial:i02.ug.whole_design.00 (i0011, i0017, i0019, i0025, i0056, i0111, i0131) and trial:i04.ug.whole_design.00 (i0012, i0117, i0131, i0017, i0019, i0011) displaced M2 and V1 shapes that belong to the same cell as a unit, preserving the enclosure geometry. M2 polygon end extensions in trial:i01.ug.whole_design.00 (p879, p910) and trial:i05.ug.whole_design.00 (p951, p955) that added material to M2 did not reduce any V1 enclosure.

---

**V2.M2.EN.1 — Enclosure of V2 by M2 on at least two opposite sides (5 nm each)**

The cu_pool fix in trial:i04.cu.def:VIA_VIA23_1_3_36_36.00 shrunk seven polygons (p891–p897) by 64 dbu in y and simultaneously reduced the M3 shape inside cell VIA_VIA23_1_3_36_36 by 40 dbu in y. The global violation count dropped from 30 to 22 (delta -8) and no V2.M2.EN.1 error appeared in the outcome, showing that the y-shrink on those M2-touching shapes preserved at least 5 nm of V2 enclosure on both opposing sides. Avoid shrinking an M2 shape in the y direction beneath an existing V2 without confirming that both the top and bottom enclosure margins remain >= 5 nm (trial:i04.cu.def:VIA_VIA23_1_3_36_36.00).

---

**V1.M2.AUX.2 — V1 must exactly match M2 width in the direction perpendicular to M2 length**

No V1.M2.AUX.2 violation appeared in any trial. Instance moves in trial:i02.ug.whole_design.00 and trial:i04.ug.whole_design.00 co-displaced M2 and V1 within each cell without altering the relative perpendicular width relationship. No record shows a modification that changed M2 width in isolation from its associated V1.

---

**GEOMETRY.NONORTHOGONAL**

All recorded M2 polygon operations are axis-aligned: x- and y-axis resize_end and move operations in trial:i01.ug.whole_design.00, trial:i04.cu.def:VIA_VIA23_1_3_36_36.00, and trial:i05.ug.whole_design.00, and rectilinear instance moves throughout. No non-orthogonal edge was introduced on M2 in any trial.

---

**Grid and move-size observations**

Instance moves affecting M2 used x-deltas of 36, 72, 128, and 136 dbu and y-deltas of 24, 48, 72, and 96 dbu across trial:i01.ug.whole_design.00, trial:i02.ug.whole_design.00, trial:i04.ug.whole_design.00, and trial:i05.ug.whole_design.00, all accepted without new M2 violations. Polygon end extensions used increments of 8, 20, 48, and 128 dbu (trial:i01.ug.whole_design.00, trial:i05.ug.whole_design.00), all accepted. The cu_pool channel's coordinated via-cell shrink of 64 dbu in y across p891–p897, coupled with a 40 dbu M3 shape reduction, reduced total violations by 8 while leaving all M2 rules clean (trial:i04.cu.def:VIA_VIA23_1_3_36_36.00).