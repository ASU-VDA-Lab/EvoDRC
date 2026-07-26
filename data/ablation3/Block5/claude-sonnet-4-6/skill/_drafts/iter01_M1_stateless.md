## Rule Reference

**M1.W.1** — Minimum M1 wire width is 18 nm. All M1 shapes must satisfy this on every internal cross-section.

**M1.S.1** — Minimum side-to-side spacing between M1 polygons is 18 nm when both opposing edges are longer than 36 nm.

**M1.S.2** — Minimum tip-to-side spacing is 25 nm when the tip edge is ≤ 36 nm and the opposing side edge is > 36 nm. The tip classification is based on the edge length of a single polygon edge, not the polygon width overall.

**M1.S.3** — Minimum tip-to-tip spacing is 27 nm when both facing edges are in the range 24–36 nm.

**M1.S.4** — Minimum tip-to-tip spacing rises to 31 nm when both facing edges are < 24 nm.

**M1.S.5** — Minimum tip-to-tip spacing is also 31 nm when one edge falls in the 24–36 nm band and the other is < 24 nm. Rules M1.S.3, M1.S.4, and M1.S.5 together cover all tip-to-tip combinations; the controlling rule depends on the pair of edge lengths actually present.

**M1.S.6** — Minimum corner-to-corner spacing between any two M1 polygons is 20 nm.

**M1.A.1** — Minimum M1 polygon area is 504 nm². Small M1 slivers created during repair operations must be checked against this threshold.

**M1.R.0** — An M1 polygon that encloses exactly one small V0 via and sits near a large empty M1 region (≥ 500 nm wide, area > 2.5 µm², expanded by 400 nm) is flagged as a redundant island. Repair operations that produce isolated single-via M1 stubs in sparsely populated areas can trigger this rule even when all geometric spacing rules pass.

**V0.M1.EN.1** — M1 must enclose every V0 via by ≥ 5 nm on at least two opposite sides. The rule accepts a 5 nm / 0 nm asymmetric enclosure (one side 5 nm, opposite side 0 nm) as well as symmetric 5 nm / 5 nm enclosure. The DRC deck implements this via a projection-based enclosure check; edges that fail the 5 nm projection on a given axis generate violations. Any M1 resize or polygon move that changes the overlap between an M1 shape and an underlying V0 must preserve the required enclosure on both the horizontal and vertical axis pairs.

**V0.M1.AUX.3** — V0 vias must be exactly the same width as the enclosing M1 shape in the direction perpendicular to M1 length. This rule flags V0 corners that are not coincident with M1 edges; it is evaluated by comparing V0 non-coincident edges on both axes. Widening or narrowing an M1 polygon in the perpendicular direction without simultaneously adjusting the V0 footprint (or vice versa) will trip this rule.

**V1.M1.EN.1** — M1 must enclose every V1 via by ≥ 5 nm on one pair of opposite sides and ≥ 2 nm on the other pair. The rule uses an asymmetric two-threshold scheme: a via qualifies as good on a given axis if it has at least one 5 nm enclosure edge on that axis and no edge below 2 nm. Repair operations that extend or contract M1 near V1 must preserve both the 5 nm and the 2 nm thresholds simultaneously.

**GEOMETRY.NONORTHOGONAL** — All M1 edges must be strictly horizontal (0°) or strictly vertical (90°). Any polygon resize or move that produces a non-rectilinear edge on M1 will generate a GEOMETRY.NONORTHOGONAL marker. This constraint applies globally to all drawing layers including M1.

---

## Observed Repair Behavior

The sole measured trial for this layer is trial:i01.ug.whole_design.00 (Block5, channel unit_gate, iteration 1). The trial applied 19 operations to the whole-design locus (0, 0, 10784, 10784 dbu) across layers M1, M2, M3, M4, M5, V1, V2, V3, V4. The decision was `gated_in` with `conn_preserved=true` and zero new violations introduced inside or outside the crop boundary (`n_new_in_crop=0`, `n_new_out_of_crop=0`).

**Operation mix:** Of the 19 operations, 17 were `move_instance` calls on instances i0001, i0002, i0012, i0061, i0062, i0067, i0070, i0073, i0075, i0076, i0099, i0103, i0104, i0105, i0112, i0113. The remaining two targeted M1 polygons directly: polygon p879 received a `resize_end` on the y-axis at the high end (+48 dbu), and polygon p910 received a `move` on the x-axis (+8 dbu) followed by a `resize_end` on the y-axis at the high end (+20 dbu). All displacements in trial:i01.ug.whole_design.00 are therefore small — under 140 dbu in x and under 100 dbu in y for instance moves, and under 50 dbu for the direct polygon edits.

**Mixed instance-plus-polygon repair is viable.** The trial demonstrates that combining instance moves with direct polygon endpoint adjustments on M1 (resize_end, move operations on individual polygons) can be executed in a single operation batch without introducing new M1 violations, provided connectivity is preserved — trial:i01.ug.whole_design.00 achieved gated_in status with conn_preserved=true and zero new violations under this mixed strategy.

**Small incremental adjustments preserved rule compliance.** The polygon-level edits in trial:i01.ug.whole_design.00 were limited to extending the high-y endpoint of p879 by 48 dbu and shifting p910 by 8 dbu in x while also extending its high-y endpoint by 20 dbu. These moves did not create new M1.W.1, M1.S.*, M1.A.1, V0.M1.EN.1, V0.M1.AUX.3, V1.M1.EN.1, or GEOMETRY.NONORTHOGONAL violations, establishing that single-axis endpoint extensions and lateral shifts of this magnitude are safe starting points for enclosure correction on M1.