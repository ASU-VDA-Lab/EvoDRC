## Via Cell Identity and Repair Scope

The only V5 via cell directly manipulated across all recorded trials is `VIA_VIA56_2_2_66_58`. All direct `move_via_shape` and `resize_via_shape` operations targeting V5 polygons occur inside this cell (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02, trial:i04.cu.def:VIA_VIA56_2_2_66_58.00). Unit-gate trials that touch V5 (trial:i03.ug.leaf_0003.02, trial:i05.ug.leaf_0002.01) do so indirectly through instance moves that shift the enclosing M5 and M6 polygons rather than the V5 shapes themselves.

## X-Axis Repair Pattern: Symmetric Spread Plus Uniform Resize

In trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 the engine moved four V5 shapes symmetrically in X—shapes 0 and 2 by −116 dbu, shapes 1 and 3 by +116 dbu—and simultaneously resized all four by +320 dbu along X. This combined operation produced a net DRC reduction of −16 violations across two windows (leaf_0019 −8, leaf_0020 −8) while preserving connectivity. The symmetric spread addresses V5.S.1/V5.S.2/V5.S.3 spacing violations between adjacent array members by pushing via shapes apart, while the resize ensures each shape continues to satisfy the V5.W.1 minimum width of 24 nm and maintains the enclosure margins required by V5.M5.EN.1 and V5.M6.EN.2 on the X axis. Never apply the spread move without the compensating resize: the resize is what keeps V5.W.1 and V5.M6.AUX.2 satisfied (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02).

## Y-Axis Repair Pattern: Outer-Pair Spread Plus Resize

In trial:i04.cu.def:VIA_VIA56_2_2_66_58.00 an analogous pattern was applied along Y. Shapes 2 and 3 moved +132 dbu in Y; shapes 0 and 1 moved −132 dbu in Y; all four were resized +512 dbu in Y. This was coupled with instance moves that repositioned the enclosing M5/M6 wires (polygons p2109 and p2108 moved −64 and −112 dbu in Y respectively, with their associated via instances moved in the same direction). The trial was applied and reduced violations by −14 (leaf_0002 −14). The larger Y resize (+512 dbu) versus X resize (+320 dbu, trial:i01.cu.def:VIA_VIA56_2_2_66_58.02) reflects that the Y-axis enclosure margin budget under V5.M5.EN.1 and V5.M6.EN.2 required more material to close after the spread. Always co-move the enclosing M-layer wires when spreading V5 shapes along Y so V5.AUX.1 and V5.M6.AUX.2 are not introduced (trial:i04.cu.def:VIA_VIA56_2_2_66_58.00).

## Rule V5.M6.AUX.2: Width-Match Constraint Drives Coupled Moves

V5.M6.AUX.2 requires V5 to exactly match M6's width in the direction perpendicular to M6's length. Both applied trials (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02, trial:i04.cu.def:VIA_VIA56_2_2_66_58.00) include resize operations on every moved V5 shape, not just the shapes that were displaced. A move without a matching resize would shift the V5 edge relative to M6's edge, violating V5.M6.AUX.2. Use resize to absorb any positional delta that would otherwise misalign V5 edges with M6 edges.

## Rule V5.AUX.1: V5 Must Remain Inside Both M5 and M6

All four trials preserved connectivity (conn_preserved: true) and none introduced V5.AUX.1 violations. In trial:i04.cu.def:VIA_VIA56_2_2_66_58.00, M5/M6 instance placements were adjusted in the same group as the V5 spread, keeping V5 inside both metal layers. When the V5 bounding box is enlarged by resize, confirm M5 and M6 are enlarged or repositioned commensurately to maintain the inside relationship required by V5.AUX.1 (trial:i04.cu.def:VIA_VIA56_2_2_66_58.00).

## Enclosure Rules V5.M5.EN.1 and V5.M6.EN.2: 11 nm on Opposite Sides

The 11 nm minimum enclosure on at least two opposite sides (V5.M5.EN.1 for M5, V5.M6.EN.2 for M6) constrains how far any V5 shape edge may be from the enclosing metal edge. In trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 the +320 dbu X resize on shapes that were also moved ±116 dbu was sufficient to maintain this margin in X. In trial:i04.cu.def:VIA_VIA56_2_2_66_58.00 the +512 dbu Y resize was paired with M-layer wire repositioning to preserve the same margin in Y. Do not resize V5 in isolation without verifying that the resulting extent still falls within M5 and M6 by at least 11 nm on opposite sides.

## Spacing Rules V5.S.1, V5.S.2, V5.S.3: 33 nm Minimum

All three spacing rules share the same 33 nm threshold (projection-based for S.1/S.2, Euclidean corner-to-corner for S.3). The symmetric X-spread in trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 (±116 dbu per shape) directly targets these rules: moving via shapes apart by 232 dbu total per pair is more than sufficient to clear the 33 nm projection gap when shapes were previously too close. The Y-spread of ±132 dbu per pair in trial:i04.cu.def:VIA_VIA56_2_2_66_58.00 similarly addresses projection-axis spacing along Y. V5.S.3 corner-to-corner violations are relieved as a side effect of the same spread operations because displacing shapes along a primary axis also increases diagonal distances (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02, trial:i04.cu.def:VIA_VIA56_2_2_66_58.00).

## Unit-Gate Trials: Indirect V5 Impact via Instance and Wire Moves

Trial:i03.ug.leaf_0003.02 (iter 3, gated_in, 26 new violations absorbed in crop) and trial:i05.ug.leaf_0002.01 (iter 5, gated_in, 22 new violations absorbed in crop) both touch V5 through their `touched_layers` field but contain no direct `move_via_shape` or `resize_via_shape` operations on V5. Instead, they move instances that carry V5-containing sub-cells and resize M5/M6 polygon endpoints (trial:i05.ug.leaf_0002.01 resizes the high end of p2086, p1946, p2046 in X). These instance-level moves propagate to V5 positions indirectly. A unit-gate trial touching V5 does not guarantee that V5 shapes were individually edited; inspect the ops list for `move_via_shape`/`resize_via_shape` to determine direct versus indirect V5 impact (trial:i03.ug.leaf_0003.02, trial:i05.ug.leaf_0002.01).

## Connectivity Preservation Is a Hard Requirement

Every trial in the history records conn_preserved: true. Connectivity is explicitly the gate criterion for unit-gate trials (trial:i03.ug.leaf_0003.02 reason: "conn_preserved", trial:i05.ug.leaf_0002.01 reason: "conn_preserved"). For cu_pool trials the field is also true (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02, trial:i04.cu.def:VIA_VIA56_2_2_66_58.00). No trial has been applied or gated in with conn_preserved: false. Do not apply any V5 operation that severs connectivity between M5 and M6 through the via.

## Minimum Width Rule V5.W.1: 24 nm

The +320 dbu X resize in trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 and the +512 dbu Y resize in trial:i04.cu.def:VIA_VIA56_2_2_66_58.00 both increase via shape extent. No trial records a shrink operation on any V5 shape; all measured resizes are strictly positive (expansion). Avoid negative (shrink) resizes on V5 shapes because they risk violating the 24 nm minimum width required by V5.W.1 when shapes are already near the minimum. Both applied expansions successfully passed DRC (decision: "applied"), confirming that expansion is the safe direction for V5 resize (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02, trial:i04.cu.def:VIA_VIA56_2_2_66_58.00).

## Multi-Layer Grouping: V5 Ops Are Bundled with M5/M6

In trial:i04.cu.def:VIA_VIA56_2_2_66_58.00 all 30 operations share group "g1", including M4/M5/M6 wire moves and V5 shape moves and resizes. This grouping is essential: the V5 shape move alone would violate V5.AUX.1 (V5 outside M5 or M6) unless the enclosing wires move with it. The same principle applies in trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 where M5 and M6 are listed in touched_layers alongside V5. Always treat V5 shape edits as belonging to a multi-layer transaction that includes the immediately enclosing M5 and M6 geometry.