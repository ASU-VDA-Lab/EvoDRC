## V1 Rule Structure

V1 sits at the M1-to-M2 via stack. Its geometry is constrained in three independent ways: width along the M2 run direction (V1.W.1), inter-via spacing that varies by end-cap configuration (V1.S.1 through V1.S.4), and enclosure by M1 and M2 on opposite-side pairs (V1.M1.EN.1, V1.M2.EN.2). Two auxiliary rules bind V1 placement to its parent metals (V1.AUX.1, V1.M2.AUX.2). The global NONORTHOGONAL block forbids any V1 edge at a non-rectilinear angle.

## Measured Repair Outcome

One trial has been measured for this layer: trial:i03.ug.whole_design.00 (iteration 3, channel `unit_gate`, scope `whole_design`, Block1). That trial applied 32 `move_instance` operations to instances touching M1, M2, and V1 simultaneously. Move deltas were entirely in the X direction: 30 instances moved +64 dbu and 2 instances (i0455, i0079) moved −64 dbu. The result was `decision: gated_in`, `conn_preserved: true`, and `n_new_in_crop: 0` / `n_new_out_of_crop: 0`. No new V1 DRC violations were introduced by that operation.

## Repair Strategy Grounded in Trial:i03.ug.whole_design.00

Bulk X-direction instance displacement that moves M1, M2, and V1 together in a single coordinated operation — without changing the relative geometry between the via and its enclosing metals — does not introduce new V1 violations, as confirmed by trial:i03.ug.whole_design.00.

Preserve connectivity when moving instances that carry V1 geometry: the zero-violation outcome of trial:i03.ug.whole_design.00 was recorded under `conn_preserved: true`; the repair channel gated the operation in on that basis. Do not move V1-containing instances in a way that severs M1 or M2 connections, because the gating criterion observed in trial:i03.ug.whole_design.00 treats connectivity preservation as a precondition for acceptance.

Move V1 as part of its parent instance rather than editing V1 shape geometry directly when the violation is a relative-placement issue: trial:i03.ug.whole_design.00 achieved clean V1 DRC results exclusively through `move_instance` operations, with no resize or shape-edit ops on the V1 layer itself.

## Spacing Rules: Configuration Determines Threshold

V1.S.1 through V1.S.4 each apply to a different pairing of end-cap configurations (presence or absence of a 5 nm M2 end-cap on each via). Before choosing a repair move magnitude, identify whether each via in a violating pair falls into the wec (with-end-cap) or nec (no-end-cap) class:

- Both wec: euclidean 16.4 nm / projected 23 nm threshold (V1.S.2).
- Both nec: euclidean 16.12 nm / projected 30 nm threshold (V1.S.3).
- Mixed wec + nec: euclidean 17.11 nm / projected 27 nm threshold (V1.S.4).
- Same-track or aligned-track: 18 nm projected; not-aligned parallel: 27 nm projected (V1.S.1).

No trial has yet measured a direct repair targeting any of these spacing variants in isolation. The ±64 dbu move magnitudes used in trial:i03.ug.whole_design.00 did not produce new spacing violations, indicating that coordinated bulk moves at that magnitude are compatible with at least the spacing constraints active in the Block1 whole-design context.

## Enclosure Rules: Opposite-Side Pairs Required

V1.M1.EN.1 requires M1 to enclose V1 by 5 nm on one axis and 2 nm on the other (both opposite-side pairs must be satisfied independently). V1.M2.EN.2 requires M2 to enclose V1 on two opposite sides at 5 & 5 nm or 5 & 0 nm; the 0 nm case corresponds to flush M2 edges (edge-coincident with V1). V1.M2.AUX.2 further constrains V1 width perpendicular to the M2 run to match M2 width exactly.

These enclosure and width constraints are geometry-coupling constraints between V1 and its parent metals. Moving a full instance (so that M1, M2, and V1 translate together) leaves all enclosure margins unchanged, which is consistent with the zero-violation result seen in trial:i03.ug.whole_design.00. Any repair that instead moves M1 or M2 independently of V1, or resizes V1 without adjusting the parent metals, risks violating V1.M1.EN.1, V1.M2.EN.2, or V1.M2.AUX.2. No such decoupled repair has been measured for this layer.

## Width Rule

V1.W.1 sets a minimum V1 width of 18 nm along the M2 run direction. The single measured trial did not involve any V1 shape resizing, so no direct resize-to-width-floor repair has been measured. Do not shrink V1 width below 18 nm in any repair: the rule is an absolute floor per the DRC deck, and the successful zero-violation trial (trial:i03.ug.whole_design.00) operated without altering V1 shape dimensions.

## Orthogonality

The NONORTHOGONAL block flags any V1 edge not at 0° or 90°. No diagonal or angled V1 shapes have appeared in the measured history. Move operations in trial:i03.ug.whole_design.00 were axis-aligned (X-only deltas), producing no orthogonality violations. Use only axis-aligned deltas when moving V1-containing instances: trial:i03.ug.whole_design.00 confirms that X-only moves at ±64 dbu do not introduce NONORTHOGONAL violations.

## V1.AUX.1 Placement Constraint

V1 must reside inside the intersection of M1 and M2 (V1.AUX.1). Moving instances as a coordinated group — so that V1, M1, and M2 translate by the same vector — maintains this containment relationship. Trial:i03.ug.whole_design.00 used exactly this approach across 32 instances and recorded zero new AUX.1 violations. Any repair that shifts V1 relative to its enclosing metals, or that places V1 outside the M1 ∩ M2 region, will trigger V1.AUX.1 regardless of whether spacing and enclosure margins are otherwise satisfied.