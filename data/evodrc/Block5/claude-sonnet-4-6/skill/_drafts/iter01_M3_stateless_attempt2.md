Working from the inline history records provided in the prompt directly.

## Spacing Rule Summary

M3 has six spacing rules that depend on which edge class is involved. Side edges are those longer than 36 nm; wide-tip edges are 24–36 nm; narrow-tip edges are shorter than 24 nm. The resulting minimum-spacing matrix is:

- Side-to-side (M3.S.1): 18 nm
- Tip-to-side (M3.S.2): 25 nm, measured by projection
- Wide-tip-to-wide-tip (M3.S.3): 27 nm, measured by projection
- Wide-tip-to-narrow-tip (M3.S.5): 31 nm, measured by projection
- Narrow-tip-to-narrow-tip (M3.S.4): 31 nm, measured by projection
- Corner-to-corner (M3.S.6): 20 nm, measured by Euclidean distance

The tip-to-tip rules (M3.S.3, M3.S.4, M3.S.5) use projection, so a diagonal corner encounter that is not collinear along either axis does not trigger them; it is caught instead by M3.S.6 at 20 nm. A repair that widens a narrow-tip edge beyond 36 nm promotes it to a side edge, dropping its required spacing to 18 nm on the side axis and to 25 nm on the tip axis — a net relaxation of the tip-to-tip budget without lengthening the polygon.

## Width and Area Rules

M3.W.1 sets a 18 nm minimum width. M3.A.1 sets a 504 nm² minimum area. A rectangle at minimum width requires at least 28 nm of length to satisfy area (18 × 28 = 504). Any resize that narrows M3 geometry must therefore check both rules together.

## Via Enclosure Rules (V2)

V2.M3.EN.2 requires M3 to enclose V2 by at least 5 nm on two opposite sides (either both horizontal or one horizontal and one vertical at 0 nm, i.e., flush). V2.M3.AUX.2 requires that V2's width in the direction perpendicular to the M3 run exactly matches M3's width in that direction — V2 must not protrude and must share edges with M3 along that axis. These two rules together constrain how M3 can be resized around a V2: shrinking M3 in the direction of the V2 run risks violating EN.2 on the enclosing ends, and shrinking M3 perpendicular to the run risks violating AUX.2 if V2 now protrudes or if the coincident-edge condition on two sides is lost.

The only measured operation that directly repaired M3 violations involving V2 is trial:i01.cu.def:VIA_VIA23_1_3_36_36.00. That trial resized the VIA_VIA23_1_3_36_36 M3 via shape by −40 dbu on the y-axis and also resized four adjacent M3 polygons (p894–p897) by −64 dbu on the y-axis. The result was a net reduction of 8 DRC violations in unit leaf_0009 (from 25 to 17), and the trial was accepted (decision: applied) — trial:i01.cu.def:VIA_VIA23_1_3_36_36.00. The operation touched M2, M3, and V2 simultaneously, consistent with AUX.2's requirement that M3 and V2 dimensions stay coordinated.

Resizing the M3 via shape and the surrounding M3 polygons together on the same axis in the same trial is the pattern that succeeded: trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 performed both a `resize_via_shape` on M3 and four `resize` operations on adjacent M3 polygons, all along y, in one atomic group (group g1). Splitting those two resize types across separate trials was not observed and the single-group approach produced a valid result.

## Via Enclosure Rule (V3)

V3.M3.EN.1 requires that M3 encloses V3 by at least 5 nm on at least two opposite sides (either the left/right pair or the top/bottom pair). The rule is satisfied if V3 fits inside M3 shrunk by 5 nm horizontally or inside M3 shrunk by 5 nm vertically — one pair is sufficient. A repair that extends M3 in either axis by 5 nm beyond the V3 boundary on both sides of that axis clears this rule for that axis. No trial in the current history directly targets a V3.M3.EN.1 violation in isolation; trial:i01.ug.leaf_0010.07 touched V3 and M3 as part of an instance-move but was gated before application (decision: gated_in) and introduced 3 new in-crop violations — trial:i01.ug.leaf_0010.07. That gated result provides no confirmation that instance moves reliably repair V3.M3.EN.1.

## Instance-Move Operations on M3

trial:i01.ug.leaf_0010.07 executed six instance moves (four y-axis moves of ±24 dbu and two y-axis moves of +72 dbu) affecting M3, M4, M5, V3, and V4 in the unit_gate channel. Although connections were preserved (conn_preserved: true), the operation introduced 3 new in-crop violations (n_new_in_crop: 3) with no new out-of-crop violations. The trial was gated (decision: gated_in), meaning the repair harness blocked it because the net new-violation count was positive. Instance moves that span multiple layers including M3 therefore carry a risk of introducing new M3-region violations even when connectivity is maintained — trial:i01.ug.leaf_0010.07. The cu_pool channel, by contrast, produced a net negative delta (−8 violations) and was applied — trial:i01.cu.def:VIA_VIA23_1_3_36_36.00.

## Geometry Constraints

All M3 edges must be orthogonal (0° or 90°). The NONORTHOGONAL block fires on any edge at any other angle on any drawing layer including M3. No measured trial introduced nonorthogonal geometry, consistent with the resize operations in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 all being axis-aligned (axis: "y").