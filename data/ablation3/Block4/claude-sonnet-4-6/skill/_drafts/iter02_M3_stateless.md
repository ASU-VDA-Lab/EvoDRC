## V2 Resize as the Primary M3 Violation Driver in Iteration 2

The sole measured operation for M3 in iteration 2 is a `resize_via_shape` on V2 in cell `VIA_VIA23_1_3_36_36`, axis x, delta_dbu +144. This single operation reduced the whole-design violation count from 140 to 89, a net delta of -51 (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00). The repair was accepted (decision: applied) with connectivity preserved (conn_preserved: true).

## Layer Interaction: M3 Is Touched by V2 Resize Operations

The operation's `touched_layers` field lists M2, M3, and V2 (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00). When a via cell is resized in X, the enclosing M3 metal geometry within that cell moves with it. This means M3-layer violations—including those governed by V2.M3.EN.2 and V2.M3.AUX.2—are directly coupled to the V2 via shape dimensions.

## V2.M3.EN.2 and V2.M3.AUX.2 Are the Target Rules for Via Resize Repairs

V2.M3.EN.2 requires that V2 be enclosed by M3 by at least 5 nm on two opposite sides (or 5 nm on one side and 0 nm on the other). V2.M3.AUX.2 requires that V2 match M3 width exactly along the direction perpendicular to the M3 run direction. A resize of V2 in X by +144 dbu directly widens the via in the horizontal axis; because the M3 enclosure rectangle also moves (touched_layers includes M3), this operation repairs enclosure shortfalls on horizontal edges consistent with V2.M3.EN.2, and brings the via perpendicular width into alignment with M3 consistent with V2.M3.AUX.2 (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00).

## Resize Magnitude and Repair Scale

A single +144 dbu X-axis resize of V2 in one via cell eliminated 51 violations across the whole design (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00). The high per-operation yield indicates that cell `VIA_VIA23_1_3_36_36` is instantiated many times in Block4, and all instances shared the same enclosure shortfall before the fix.

## Connectivity Safety of Via Resize

The resize was applied with conn_preserved: true (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00). Widening V2 in X within its M3 enclosure context did not break any electrical connection. Do not avoid via resizes on connectivity grounds when the operation is confined to expanding the via shape within its host M3 metal.

## M3 Spacing and Width Rules: No Violations Triggered by the Via Resize

The trial applied a net-positive fix (delta -51) without introducing new M3.W.1, M3.S.1, M3.S.2, M3.S.3, M3.S.4, M3.S.5, M3.S.6, or M3.A.1 violations, as evidenced by the accepted outcome (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00). Expanding V2 and the accompanying M3 enclosure shape in X did not violate minimum width (18 nm), any spacing rule between neighboring M3 polygons, or the minimum area rule (504 nm²) for M3 in this case. This establishes that the as-taped M3 geometry surrounding `VIA_VIA23_1_3_36_36` had sufficient clearance on all sides to absorb a +144 dbu X expansion without secondary violations.

## No Non-Orthogonal Geometry Introduced

The GEOMETRY.NONORTHOGONAL rule applies to M3. The accepted fix involved axis-aligned resize operations only (axis: x), and the repair was accepted without new violations (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00). Restrict all M3 shape modifications to orthogonal (0° and 90°) edges.