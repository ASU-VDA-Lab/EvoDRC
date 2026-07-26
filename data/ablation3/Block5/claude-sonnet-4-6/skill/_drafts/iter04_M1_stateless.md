**Observed correction strategies**

All three recorded trials applied instance-level move operations to instances whose flattened geometry includes M1 wiring. In every case the outcome was `gated_in` with `conn_preserved:true` and zero new M1-rule violations in the delta (trial:i01.ug.whole_design.00, trial:i02.ug.whole_design.00, trial:i04.ug.whole_design.00). Instance repositioning is a proven primary lever for M1 at the move magnitudes observed, and it does not break connectivity.

**Move magnitude and axis patterns**

X-axis moves on M1-touching instances span 8 dbu to 136 dbu in absolute value (trial:i01.ug.whole_design.00), with multiples of 36 dbu (±36, ±72 dbu) dominating in later iterations (trial:i02.ug.whole_design.00, trial:i04.ug.whole_design.00). Y-axis moves of 24, 48, 72, and 96 dbu were applied in trial:i01.ug.whole_design.00 without creating new M1 violations. No move in the recorded history introduced new M1.W.1, M1.S.1–S.6, M1.A.1, V0.M1.EN.1, V0.M1.AUX.3, or V1.M1.EN.1 violations across any trial.

**Polygon-level resize operations**

In trial:i01.ug.whole_design.00, polygons p879 and p910 received `resize_end` operations on the y-high end (+48 dbu and +20 dbu respectively), and p910 was also translated +8 dbu in x. The touched-layers set for that trial includes M1; no new M1 violations appeared in the delta. End-extension resizes that grow the polygon (positive delta on the high end) increase area and maintain or widen the wire, keeping M1.W.1 and M1.A.1 clean (trial:i01.ug.whole_design.00).

**V0.M1.EN.1 and V0.M1.AUX.3 enclosure**

V0.M1.EN.1 requires M1 to enclose V0 by at least 5 nm on two opposite sides (complementary side may be 0 nm). V0.M1.AUX.3 requires V0 width to match M1 width perpendicular to the M1 run direction. When M1 and its enclosed V0 travel together inside the same instance, both enclosure rules self-preserve. The measured record confirms no V0.M1.EN.1 or V0.M1.AUX.3 violations were introduced in any trial (trial:i01.ug.whole_design.00, trial:i02.ug.whole_design.00, trial:i04.ug.whole_design.00); move M1 and V0 together at the instance level to maintain this outcome.

**V1.M1.EN.1 enclosure**

V1.M1.EN.1 requires M1 to enclose V1 by 5 nm on one opposing axis and 2 nm on the other. The rule uses a two-threshold check per axis: a V1 is clean only when at least one axis satisfies ≥5 nm enclosure and the opposite side satisfies ≥2 nm. V1 was in the touched-layers set of all three trials; no new V1.M1.EN.1 violations were introduced in any of them (trial:i01.ug.whole_design.00, trial:i02.ug.whole_design.00, trial:i04.ug.whole_design.00). Move M1-and-V1 geometry together within instances to preserve this enclosure.

**Spacing rules M1.S.1 through M1.S.6**

M1.S.1 enforces 18 nm minimum side-to-side spacing when both edges exceed 36 nm. M1.S.2 enforces 25 nm minimum tip-to-side spacing when one edge is ≤36 nm and the other is >36 nm. M1.S.3 enforces 27 nm minimum tip-to-tip spacing when both edges are in the 24–36 nm range. M1.S.4 enforces 31 nm minimum tip-to-tip when both edges are <24 nm. M1.S.5 enforces 31 nm when one edge is 24–36 nm and the other is <24 nm. M1.S.6 enforces 20 nm minimum corner-to-corner between any two M1 polygons. None of these rules generated new violations in any recorded trial (trial:i01.ug.whole_design.00, trial:i02.ug.whole_design.00, trial:i04.ug.whole_design.00). Instance moves at multiples of 36 dbu in x and multiples of 24 dbu in y are sufficient to avoid introducing new M1 spacing violations in the observed design context.

**Width and area minimums: M1.W.1 and M1.A.1**

M1.W.1 requires minimum M1 wire width of 18 nm. M1.A.1 requires minimum M1 polygon area of 504 nm². Neither rule generated new violations in any recorded trial (trial:i01.ug.whole_design.00, trial:i02.ug.whole_design.00, trial:i04.ug.whole_design.00). The end-extension resize operations in trial:i01.ug.whole_design.00 extended polygons in the positive direction, which increases area and does not narrow wires, maintaining compliance with both rules.

**M1.R.0 redundant island rule**

M1.R.0 flags M1 islands that enclose exactly one small V0 via when they appear near a large empty M1 region (≥500 nm wide, area >2.5 µm², expanded by 400 nm). No M1.R.0 violation appeared in any trial delta (trial:i01.ug.whole_design.00, trial:i02.ug.whole_design.00, trial:i04.ug.whole_design.00). The rule is sensitive to the surrounding M1 fill context; moving an M1 island closer to other M1 geometry reduces the empty-region exposure and avoids the trigger condition.

**Cross-layer independence: M1 moves proceed without upper-metal ops**

In trial:i04.ug.whole_design.00, several V2/M3 resize operations were dropped from the assembly pool (`cu_pool:applied`). The M1-touching instance moves in that trial were executed independently of those M3/V2 ops and still achieved `gated_in` with zero new M1 violations. M1 corrections do not require concurrent upper-metal adjustments to remain clean.

**Non-orthogonal geometry**

The GEOMETRY.NONORTHOGONAL rule applies to M1 and flags any edge at an angle other than 0° or 90°. All polygon resize and instance move operations in the recorded history produce only axis-aligned geometry. No non-orthogonal M1 edges were introduced in any trial (trial:i01.ug.whole_design.00, trial:i02.ug.whole_design.00, trial:i04.ug.whole_design.00). Restrict all M1 shape modifications to horizontal and vertical edge movements to avoid triggering this rule.