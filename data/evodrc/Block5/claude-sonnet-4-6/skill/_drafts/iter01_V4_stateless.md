## Geometry Constraints

**Minimum width** of V4 is 24 nm (V4.W.1). No trial in this history targeted a width fix directly, so no width-repair sequence has been measured yet.

**Non-orthogonal edges** are prohibited by the global GEOMETRY.NONORTHOGONAL rule. All move_instance operations observed in trial:i01.ug.leaf_0010.07 produced only axis-aligned displacements ([0,+72], [0,+24], [0,−24] DBU), confirming that instance moves along a single axis do not introduce diagonal edges.

## Spacing Rules (V4.S.1 / V4.S.2 / V4.S.3)

All three spacing rules share the 33 nm threshold. V4.S.1 and V4.S.2 apply a **projection** metric; V4.S.3 applies a **euclidean** (corner-to-corner) metric and fires only on pairs not already caught by projection. Because the projection rules are evaluated first, euclidean violations tend to appear at corners where projection clearance is satisfied but the diagonal gap is still below 33 nm.

Trial:i01.ug.leaf_0010.07 introduced 3 new in-crop violations (n_new_in_crop=3) while moving instances in opposing Y directions (+72/+24 vs −24 DBU). The move set included instances on both sides of the locus [1728,3148,9072,7652], consistent with spacing violations arising from instances moving toward each other. The trial was accepted because connectivity was preserved (conn_preserved=true, decision=gated_in), not because the spacing violations were resolved. Do not interpret a gated_in decision as spacing-clean; verify the specific rule counts independently.

## Enclosure by M4 (V4.M4.EN.1)

V4 must be enclosed by M4 by at least 11 nm on at least two opposite sides. The rule uses a sizing check: any V4 that protrudes outside m4.sized(−11 nm, 0) in X **and** outside m4.sized(0, −11 nm) in Y simultaneously is a violation. Practically this means M4 must extend 11 nm beyond the V4 boundary on at least one pair of opposing edges.

Trial:i01.ug.leaf_0010.07 moved instances that touched M4 (touched_layers includes M4), with Y-only displacements. Moving an instance that carries both M4 and V4 geometry together preserves the relative enclosure on the moved instance. However, moving neighboring instances in the opposite direction can change whether a shared M4 run still covers a V4 at the 11 nm minimum. This is consistent with the 3 new in-crop violations observed in that trial.

## Enclosure by M5 (V4.M5.EN.2)

V4 must be enclosed by M5 by at least 11 nm on two opposite sides, using the same bilateral sizing check as V4.M4.EN.1. M5 was touched in trial:i01.ug.leaf_0010.07 alongside M4, confirming that unit_gate channel repairs routinely move geometry on both enclosing layers simultaneously. Repairs that move an M5-carrying instance without also adjusting adjacent M4 (or vice versa) risk creating a one-sided fix that satisfies one enclosure rule while violating the other.

## Containment (V4.AUX.1)

V4 must lie entirely inside the intersection of M4 and M5 (v4.not_inside(m4 & m5)). Because V4 is sandwiched between M4 below and M5 above, any move that shifts either metal layer without moving the via will produce an AUX.1 violation. In trial:i01.ug.leaf_0010.07 the move_instance operations displaced instances carrying M4, M5, and V4 together (all appear in touched_layers), so containment was maintained on the moved instances. Partial moves — shifting M4 without M5, or moving an M5 instance while a V4 on a neighboring instance overlaps the old M5 boundary — are the primary containment risk.

## Width-matching (V4.M5.AUX.2)

V4 must exactly match the width of M5 in the direction perpendicular to the M5 run. The rule detects V4 instances that do not share two coincident edges with M5. This is a stricter constraint than enclosure: enclosure allows M5 to be wider than V4, but AUX.2 requires exact width match. No trial in this history directly exercised a V4.M5.AUX.2 repair; however, because move_instance operations in trial:i01.ug.leaf_0010.07 displaced M5-carrying instances and V4 appears in touched_layers, any future operation that changes M5 width or misaligns the V4 footprint relative to M5 will trigger this rule.

## Move-instance Repair Patterns

The only repair operation class observed is **move_instance**. Trial:i01.ug.leaf_0010.07 used 6 move operations across 6 instances (i0113, i0099, i0001, i0002, i0067, i0070), all with purely Y-axis deltas. The moves were not uniform: two instances moved +72 DBU, two moved +24 DBU, and two moved −24 DBU. This spread-and-compress pattern on the Y axis is consistent with closing a spacing violation on one pair of instances while opening headroom on another pair.

Connectivity was preserved across all 6 moves (conn_preserved=true), which was the stated reason for gating the repair in despite 3 new violations (n_new_in_crop=3, n_new_out_of_crop=0). All new violations remained inside the crop window, confirming the repair did not push problems outside the repair locus.

No resize_instance, reshape, or net-topology operations appear in this history. No same-net vs. different-net spacing distinction has been exercised in a measurable way across the current record set.