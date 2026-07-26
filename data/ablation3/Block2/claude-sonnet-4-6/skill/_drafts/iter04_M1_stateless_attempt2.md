**M1 repair operation types in this block**

Every M1 operation across all three accepted trials used one of two primitives: translating a polygon in x or y (`move`), or extending the high-x end of a polygon (`resize_end` on axis x, end high). No y-axis end resizes and no low-x-end resizes appear in the M1 record (trial:i02.ug.whole_design.00, trial:i03.ug.whole_design.00, trial:i04.ug.whole_design.00).

**Instance displacement and M1 polygon resize must be coordinated**

When an instance moves in x, the M1 polygon connecting it must have its high-x end extended to maintain via enclosure required by V0.M1.EN.1 and V1.M1.EN.1 — confirmed by all three accepted trials (trial:i02.ug.whole_design.00, trial:i03.ug.whole_design.00, trial:i04.ug.whole_design.00). In trial:i04, the minimum-resize pattern is visible: all 11 instance moves were +72 dbu in x and all 11 corresponding M1 polygon resizes were also exactly +72 dbu on the high-x end, producing zero new in-crop violations (trial:i04.ug.whole_design.00). Matching the resize delta to the instance displacement is sufficient when the prior enclosure margin was already at or above the rule minimum before the move.

**Resize delta can exceed instance move delta when additional enclosure margin is required**

In trial:i02, instance i0086 moved +72 dbu in x while polygon p1065 was resized +116 dbu on the high-x end, and instance i0063 moved +72 dbu while polygon p1036 was resized +80 dbu (trial:i02.ug.whole_design.00). In trial:i03, instance i0063 moved +36 dbu while polygon p1036 was resized +84 dbu on the high-x end (trial:i03.ug.whole_design.00). Both trials were accepted with no new violations. The resize delta must therefore cover not only the instance displacement but also any pre-existing enclosure shortfall, so that the resulting geometry satisfies V0.M1.EN.1 (5 nm two-sided enclosure of V0) and V1.M1.EN.1 (5 nm and 2 nm on opposite sides of V1).

**Y-axis polygon moves track instance y-displacements**

In trial:i02, M1 polygons were displaced in y simultaneously with their x-end extensions: p964 moved -48 dbu, p963 moved -96 dbu, p962 moved +48 dbu, p961 moved +72 dbu, p960 moved -72 dbu, p959 moved +72 dbu, p958 moved -72 dbu (trial:i02.ug.whole_design.00). These y-displacements match the y-components of the paired instance moves, keeping the via positions aligned with the M1 polygon body as required by V0.M1.AUX.3 (V0 must share the same width as M1 perpendicular to M1 length) and preserving the two-sided enclosure demanded by V0.M1.EN.1.

**Width, spacing, and area effects of high-x end extension**

Extending the high-x end of an M1 polygon increases the polygon's x-extent and total area. M1.A.1 (minimum 504 nm² area) is not at risk from extension operations, as confirmed by zero new violations across all three accepted trials (trial:i02.ug.whole_design.00, trial:i03.ug.whole_design.00, trial:i04.ug.whole_design.00). Extension lengthens what was the polygon's rightmost tip edge, converting it into a side edge; this changes which spacing rule governs the right end: M1.S.1 (18 nm side-to-side for edges longer than 36 nm), M1.S.2 (25 nm tip-to-side), M1.S.3 (27 nm tip-to-tip for edges 24–36 nm), M1.S.4 (31 nm tip-to-tip for edges below 24 nm), and M1.S.5 (31 nm for mixed 24–36 nm and sub-24 nm tip pairs) all distinguish tip from side geometry. The three trials collectively confirm that coordinated extension and instance moves can satisfy the full M1 spacing and enclosure rule set with no new in-crop violations.

**Whole-design locus**

All three trials operated on the full design extent with locus [0, 0, 11992, 11992] and no sub-region cropping (trial:i02.ug.whole_design.00, trial:i03.ug.whole_design.00, trial:i04.ug.whole_design.00). M1 repair moves therefore spanned the entire layout simultaneously.