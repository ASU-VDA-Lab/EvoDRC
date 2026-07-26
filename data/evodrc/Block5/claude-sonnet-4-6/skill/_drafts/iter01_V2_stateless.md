## Repair Operation Coupling: V2 and M3 Must Move Together

When shrinking a V2 instance along a given axis, the enclosing M3 wire must be co-resized in the same axis and in the same direction to preserve V2.AUX.1 ("V2 must be inside M2 and M3") and V2.M3.AUX.2 ("V2 must exactly be the same width as M3 along the direction perpendicular to the M3 length"). In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, a y-axis V2 shrink of −40 dbu was paired with y-axis shrinks of −64 dbu on four associated M3 polygons (p894–p897); the repair was applied with `conn_preserved: true` and reduced the violation count by 8.

Do not resize V2 in isolation without simultaneously adjusting the M3 geometry: the −64 dbu M3 delta used in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 was larger in magnitude than the −40 dbu V2 delta, indicating the M3 wire required additional pullback beyond the V2 shrink to clear spacing violations on the M3 mask constructs that feed V2.S.1.

## Axis Selection for Width and Spacing Violations

V2.W.1 constrains width along the M3 length direction (18 nm minimum). V2.S.1 uses projection-based spacing checks on horizontal edges (angle 0) of the v2_mask geometry, meaning horizontal spacing violations require y-axis adjustments to V2 and M3. In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, all resize operations were on `axis: "y"`, and the operation reduced violations from 25 to 17 in the affected window; use y-axis resizes to address spacing violations that appear on horizontal mask edges.

## End-Cap Category Determines Applicable Spacing Rule

V2.S.1 through V2.S.4 each apply to a distinct combination of end-cap presence (whether M3 extends ≥5 nm beyond the V2 edge). The deck constructs `v2_nec` (no end-cap: all V2 edges are flush with M3 edges) and `v2_wec` (with end-cap: at least one V2 edge is not coincident with an M3 edge), and builds separate mask geometries for each. Before selecting a repair magnitude, determine which category applies to the V2 instance being repaired:

- **v2_wec** (with end-cap): governed by V2.S.2 (23 nm Euclidean corner-to-corner) and V2.S.1 (17 nm projection on horizontal mask edges).
- **v2_nec** (no end-cap): governed by V2.S.3 (30 nm Euclidean corner-to-corner).
- **Mixed pairs**: governed by V2.S.4 (27 nm Euclidean corner-to-corner).

The repair in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 targeted `VIA_VIA23_1_3_36_36` with associated M3 resizes; the 5 nm end-cap classification of that instance determines which spacing budget applied and therefore how large the delta needed to be.

## M2 Enclosure Constraint Limits Shrink Magnitude

V2.M2.EN.1 requires M2 to enclose V2 by at least 5 nm on two opposite sides. Any y-axis shrink of V2 that moves an edge closer to the M2 boundary must not reduce M2 enclosure below 5 nm on the opposite-side pair. In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, the repair was applied with `conn_preserved: true`, confirming the −40 dbu V2 delta did not violate V2.M2.EN.1 in that instance; verify M2 enclosure margin before applying a larger delta.

## Connectivity Preservation Is Achievable with Coordinated Shrink

A coordinated y-axis shrink (V2 at −40 dbu, M3 at −64 dbu) preserved electrical connectivity in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 (`conn_preserved: true`). Shrinks applied as a grouped operation (`group: "g1"`) on the via shape and all four surrounding M3 polygons simultaneously achieved an 8-violation reduction in the affected leaf window without opening nets.

## Partial Violation Reduction Is Normal Within a Window

In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, the repair reduced violations in `unit:leaf_0009` from 25 to 17 (delta −8) while `unit:leaf_0010` remained at 25 (delta 0). A single grouped resize targeting one via instance does not clear all violations in its window when multiple independent violation sources are present. Subsequent repair iterations must target the remaining violations separately.

## NONORTHOGONAL Constraint

All V2 shapes must have strictly orthogonal edges (angles limited to 0° and 90°). The NONORTHOGONAL block checks every drawing layer including V2. Do not use diagonal or off-axis moves; all resize operations must be pure x-axis or pure y-axis. Trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 used only y-axis operations and was applied without triggering nonorthogonal violations.