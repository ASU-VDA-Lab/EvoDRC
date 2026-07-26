**M5.AUX.1 — Vertical Edge Grid (24 nm)**

M5.AUX.1 requires every M5 polygon vertex to lie on a 24 nm horizontal grid. Trial i02.ug.leaf_0004.03 introduced 12 new M5.AUX.1 violations; the direct polygon moves in that trial shifted p1143 by +32 dbu and p1142 by -16 dbu on the x-axis. Neither 32 nor 16 is an integer multiple of 24, so those moves placed M5 vertical edges at off-grid coordinates. Do not apply direct x-axis polygon moves with deltas that are not multiples of 24 dbu (trial i02.ug.leaf_0004.03).

**M5.AUX.3 — No Bends**

M5.AUX.3 forbids any M5 polygon from containing a corner with an included angle in the 0°–90° range. Trial i02.ug.leaf_0004.03 introduced 38 new M5.AUX.3 violations; that trial applied a y-axis direct polygon move of +32 dbu on p1561 together with x-axis direct polygon moves on p1143 and p1142, plus instance moves with non-zero y-components (e.g., [+32,+32], [-16,+32], [+32,+72], [+32,-72], [+32,-24], [-16,-72] dbu). Trial i02.ug.leaf_0002.01, which applied a pure y-axis resize_end (+44 dbu on p1154) and a pure x-axis instance move (-76 dbu on i0181) and introduced zero M5.AUX.3 violations, shows that operations confined to a single axis on each polygon do not generate M5.AUX.3 violations in that context. Avoid applying simultaneous x-axis and y-axis displacements across M5 polygons that form a shared routing segment, as trial i02.ug.leaf_0004.03 demonstrates this combination produces large numbers of M5.AUX.3 violations.

**M5.W.5 — Minimum Vertical Width (44 nm)**

M5.W.5 requires every M5 polygon to be at least 44 nm tall. Trial i02.ug.leaf_0004.03 introduced 12 new M5.W.5 violations; that trial's ops included instance moves with y-components of -64, -112, -96, -72, and -24 dbu, reducing vertical clearances in the M5 shapes below the 44 nm threshold. Trial i02.ug.leaf_0002.01 applied a y-axis resize_end of +44 dbu on the low end of M5 polygon p1154 and introduced zero M5.W.5 violations; a +44 dbu extension equals the rule minimum exactly and resolves a short-M5-endpoint deficit without introducing a new violation (trial i02.ug.leaf_0002.01). Avoid y-axis instance moves with negative components that compress M5 vertical span, as shown in trial i02.ug.leaf_0004.03.

**M5.S.4 — Tip-to-Tip Spacing on Adjacent Tracks (40 nm)**

M5.S.4 requires a 40 nm minimum tip-to-tip spacing between M5 polygons that share parallel run length on adjacent tracks. Trial i02.ug.leaf_0004.03 introduced 4 new M5.S.4 violations alongside the same set of polygon and instance moves that also produced M5.AUX.3 and M5.W.5 violations. Avoid instance moves that shift M5 polygon tips toward facing M5 tips on neighboring tracks without verifying the resulting gap exceeds 40 nm (trial i02.ug.leaf_0004.03).

**V4.M5.AUX.2 — V4 Width Must Match M5 Width**

V4.M5.AUX.2 requires V4 cuts to be exactly co-wide with the enclosing M5 in the direction perpendicular to M5 routing length. Trial i02.ug.leaf_0003.02 introduced 4 new V4.M5.AUX.2 violations; that trial moved M5 polygons p1143 (+32 dbu, x-axis) and p1142 (-16 dbu, x-axis) without applying matching x-axis adjustments to the coincident V4 shapes. When x-axis moves are applied directly to M5 polygons, any V4 shape that straddles the moved M5 edge must receive a matching x-axis delta to preserve the exact-width condition required by V4.M5.AUX.2 (trial i02.ug.leaf_0003.02). The 4 V4.M5.AUX.2 violations introduced in trial i02.ug.leaf_0003.02 did not block the gated_in decision because no new out-of-crop violations were created and connectivity was preserved.

**Repair Operations with Net Violation Reduction**

Trial i01.cu.def:VIA_VIA45_1_2_58_58.01 applied a single y-axis resize_via_shape of -88 dbu to the M5 shape (shape_index 0) in cell VIA_VIA45_1_2_58_58, reducing the violation count by 26 in window unit:leaf_0034 (182 to 156) and by 26 in window unit:leaf_0035 (113 to 87), for a net reduction of 52 violations. Connectivity was preserved and the decision was applied. A y-axis shrink of an M5 via shape by 88 dbu is a confirmed effective repair in that cell context (trial i01.cu.def:VIA_VIA45_1_2_58_58.01).

Trial i02.ug.leaf_0002.01 combined a pure x-axis instance move on i0181 (-76 dbu) with a pure y-axis resize_end (+44 dbu, low end) on M5 polygon p1154, producing zero new in-crop violations and a gated_in decision with connectivity preserved. The +44 dbu y-axis endpoint extension—equal to the M5.W.5 minimum—resolved an endpoint deficiency without introducing secondary M5.AUX.1, M5.AUX.3, M5.S.4, or V4.M5.AUX.2 violations in that unit's crop window (trial i02.ug.leaf_0002.01).