## V4-M5 Via Cell Repair: Coordinated M5 Resize with V4 Adjustment

When a VIA_VIA45-type cell violates V4.M5.EN.2 or V4.M5.AUX.2, repair requires simultaneous adjustment of both V4 and M5 shapes within the same operation group. In trial:i05.cu.def:VIA_VIA45_1_2_58_58.00, an M5 x-axis resize of −152 dbu was applied together with ±116 dbu V4 moves and +232 dbu V4 resizes (group "v45-fix"), yielding a net reduction of −158 violations while preserving connectivity. Applying the M5 resize without the paired V4 moves, or vice versa, is not represented as a successful pattern in the measured history; treat the grouped operation as the atomic repair unit.

The −152 dbu M5 horizontal resize in trial:i05.cu.def:VIA_VIA45_1_2_58_58.00 must not push M5 width below the 24 nm minimum (M5.W.1) or violate M5.AUX.1 (vertical edges on 24 nm grid) or M5.AUX.2 (minimum-width tracks on routing tracks at 192 dbu pitch, 48 dbu offset). Verify post-resize that the resulting M5 edge positions remain on the 24 nm vertical grid and that the M5 centerline, if the shape is minimum-width, lands on a permitted AUX.2 track.

## M5 as Touched-But-Unmodified Layer in V5-M6 Via Repairs

In trial:i02.cu.def:VIA_VIA56_2_2_66_58.01, M5 appears in `touched_layers` but no M5 operation appears in the ops list; all explicit operations targeted V5 (y-axis moves of ±132 dbu and resizes of +128 dbu on four shapes) and M6 (y-axis resize of −384 dbu). The −39 total violation reduction and preserved connectivity confirm the repair was effective without direct M5 modification. This establishes that V5 enclosure compliance (V5.M5.EN.1: 11 nm on two opposite sides) can be restored by adjusting V5 shape positions and sizes relative to a fixed M5 boundary, provided M5 already supplies adequate vertical extent.

## V4.M5.AUX.2 Constraint: M5 Width Must Match V4 Width Perpendicularly

V4.M5.AUX.2 requires V4 to be exactly as wide as the M5 it sits on, measured perpendicular to M5's length (i.e., in x for a horizontal M5 track). In trial:i05.cu.def:VIA_VIA45_1_2_58_58.00, the coordinated +232 dbu V4 x-resize alongside the −152 dbu M5 x-resize preserves the coincident-edge condition that AUX.2 checks (v4_aux2_coinc / v4_aux2_ok path in the rule deck). Do not resize M5 in x without simultaneously adjusting V4 x-extent by a compensating amount to maintain edge coincidence on both sides.

## Violation Budget and Locality

trial:i05.cu.def:VIA_VIA45_1_2_58_58.00 concentrated its −158 total reduction in two windows (leaf_0013: −81, leaf_0014: −75), with zero impact on three other tracked windows (leaf_0005, leaf_0009, leaf_0010, leaf_0011 each showed delta 0). This confirms that M5 via-cell edits are spatially local: a single via cell definition repair propagates only to layout windows that instantiate that specific cell, leaving unrelated windows unaffected. Target via cell definitions (def: targets) to achieve large, focused violation reductions without collateral impact.