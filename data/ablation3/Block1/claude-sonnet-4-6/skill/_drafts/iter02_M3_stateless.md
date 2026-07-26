---

## Observed repair behavior — iteration 2

**Single accepted trial on record:** trial:i02.ug.whole_design.00, decision `gated_in`, reason `conn_preserved`. Touched layers included M3. No M3-specific rule (M3.W.1, M3.S.1, M3.S.2, M3.S.3, M3.S.4, M3.S.5, M3.S.6, M3.A.1, V2.M3.EN.2, V2.M3.AUX.2, V3.M3.EN.1) appeared in `new_in_crop_by_rule` or `new_out_of_crop_by_rule` (trial:i02.ug.whole_design.00). The only new in-crop violations introduced belonged to V1.M2.AUX.2 (48 new), which is an M2-layer via rule and does not reflect M3 rule stress.

---

## M3 polygon move magnitudes applied without incurring M3 violations

In trial:i02.ug.whole_design.00, four M3 polygons received x-axis moves: p1142 at -16 dbu, p1143 at +32 dbu, p1144 at -16 dbu, p1145 at +32 dbu. Three additional M3 polygons received y-axis moves: p1561 at +32 dbu, p1562 at +16 dbu, p1563 at -64 dbu. None of these moves introduced any new in-crop or out-of-crop M3 violations (trial:i02.ug.whole_design.00). Move magnitudes of 16 dbu, 32 dbu, and 64 dbu are therefore confirmed safe for M3 in the context of this design state, subject to the caveat that the full design state at that moment already satisfied M3 rules before the move.

---

## Instance moves coexisting with M3 layer

Trial:i02.ug.whole_design.00 applied 50 instance moves ranging from -16 to +32 dbu in x and from -72 to +96 dbu in y (instances i0025 through i0505). With M3 among the touched layers and no new M3 violations introduced (trial:i02.ug.whole_design.00), instance translations up to ±96 dbu in y and ±32 dbu in x did not cause M3 rule failures in this design context.

---

## Rule threshold reference for repair decisions

The following thresholds are enforced by the checker and must be respected when moving or resizing M3 shapes.

**Width (M3.W.1):** Do not create M3 edges that leave any M3 polygon narrower than 18 nm. Moves that compress a polygon from both sides simultaneously are the primary risk.

**Side-to-side spacing (M3.S.1):** Edges longer than 36 nm must maintain at least 18 nm clearance to any other qualifying edge. In trial:i02.ug.whole_design.00, moves of up to +32 dbu and -64 dbu did not violate this rule, confirming that the pre-existing layout already had sufficient margin.

**Tip-to-side spacing (M3.S.2):** An edge of length ≤ 36 nm must maintain at least 25 nm projected separation from any edge > 36 nm on a neighboring polygon. This threshold is higher than M3.S.1 (25 nm vs. 18 nm); repair moves that close tip-to-side gaps are riskier than moves that close side-to-side gaps.

**Tip-to-tip spacings (M3.S.3, M3.S.4, M3.S.5):** Wide-tip (24–36 nm) to wide-tip requires 27 nm; narrow-tip (< 24 nm) to narrow-tip requires 31 nm; wide-tip to narrow-tip requires 31 nm. The narrow-tip threshold of 31 nm is the most restrictive among all spacing rules. Moves that bring narrow polygon ends closer together must ensure the resulting projected gap is ≥ 31 nm.

**Corner spacing (M3.S.6):** Euclidean corner-to-corner separation must be ≥ 20 nm. This rule catches diagonal proximity not covered by the projection-based rules above.

**Area (M3.A.1):** Any M3 polygon must have area ≥ 504 nm². Moves that shorten a polygon along one axis while leaving the other axis unchanged must be checked; a polygon that was exactly at the area limit will fall below it if shortened.

**Via enclosure — V2 in M3 (V2.M3.EN.2):** M3 must enclose each V2 by at least 5 nm on two opposite sides (either both directions of a horizontal pair or both of a vertical pair). Moving M3 polygons away from a V2 they currently enclose can violate this rule. In trial:i02.ug.whole_design.00, no V2.M3.EN.2 violations were introduced despite M3 polygon moves, confirming that the moves stayed within the enclosure margin present in that design state.

**Via alignment — V2 in M3 (V2.M3.AUX.2):** V2 must span the full M3 width in the direction perpendicular to M3 length; edges of V2 must be coincident with edges of M3 on at least two sides. Resizing M3 in the narrow dimension without adjusting V2, or moving M3 laterally past a V2, can trigger this rule.

**Via enclosure — V3 in M3 (V3.M3.EN.1):** M3 must enclose each V3 by at least 5 nm on at least two opposite sides (horizontal pair or vertical pair). In trial:i02.ug.whole_design.00, no V3.M3.EN.1 violations were introduced despite M3 polygon and instance moves on a design state that includes V3 in the touched-layer set.

**Nonorthogonal geometry:** All M3 edges must be strictly horizontal or vertical (0°, 90°, 180°, 270°). No diagonal or angled edges are permitted. All moves observed in trial:i02.ug.whole_design.00 were axis-aligned (x-only or y-only), consistent with this requirement.

---

## Interaction between M3 moves and via rules

Trial:i02.ug.whole_design.00 moved M3 polygons and instances touching V3 and V2 layers (both V3 and V2 appear indirectly via the touched layer set M3, V3, V4, V5) without introducing any via-related M3 enclosure violations. This confirms that the polygon-level and instance-level moves applied in that trial preserved the V2.M3.EN.2, V2.M3.AUX.2, and V3.M3.EN.1 enclosure conditions. When planning future moves, keep via enclosure margins in view: V2 and V3 require a minimum 5 nm M3 enclosure on opposite sides, and any move that shifts M3 away from an enclosed via must not drop the enclosure below that threshold on both members of the required pair simultaneously.

---

## Connectivity and gate-in criterion

The trial was accepted under the `conn_preserved` gate criterion (trial:i02.ug.whole_design.00). This confirms that connectivity preservation is a sufficient condition for gate-in even when other layers (here, M2 via rule V1.M2.AUX.2) incur new in-crop violations, as long as no new out-of-crop violations are created and no new M3 violations appear. Do not move M3 shapes in ways that sever net connectivity; the gate will reject such moves regardless of DRC improvement.