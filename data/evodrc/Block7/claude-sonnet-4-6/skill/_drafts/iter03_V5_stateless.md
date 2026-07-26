## V5 Repair Knowledge — Layer V5, Iteration 3

### Y-Axis Resize of V5 Shapes Is the Primary Effective Repair Action

The only applied repair in this layer's history resized all four V5 shape instances along the Y axis by +512 dbu each, paired with small compensating Y-axis moves of ±132 dbu to maintain centering, within cell VIA_VIA56_2_2_66_58. This produced a net violation reduction of 80 across four affected windows (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02). Apply Y-axis resize to V5 shapes when enclosure or width violations are present on the Y dimension; the paired move-then-resize pattern (move shape to offset center, then resize) preserved the via's structural alignment and connectivity.

### Do Not Resize Only the Enclosing Metal Without Resizing V5

Resizing M6 in the Y axis (+128 dbu) and M5 in the X axis (-96 dbu) without a corresponding change to the V5 shape geometry increased total violations by 234 and was rejected (trial:i02.cu.def:VIA_VIA56_2_2_66_58.01). Rules V5.M5.EN.1 and V5.M6.EN.2 require 11 nm enclosure on at least two opposite sides; shrinking or independently resizing the enclosing metal shifts that enclosure balance and triggers new violations. Never treat metal resizes as a substitute for adjusting the V5 shape itself when the V5 geometry is the root cause.

### Instance and Polygon Moves in the Unit-Gate Channel Preserve Connectivity

The unit-gate channel move of 15 polygon and instance objects (mix of X- and Y-axis displacements of 32, -16, and 64 dbu across nine instance IDs and three polygon IDs) was gated in with conn_preserved=true and zero violations introduced outside the crop window (trial:i03.ug.leaf_0013.09). Use instance-level moves in the unit_gate channel when V5-related spacing violations (V5.S.1, V5.S.2, V5.S.3) arise from cluster proximity; coordinated multi-object moves within the unit boundary reliably preserve net connectivity under these rules.

### V5.AUX.1 and V5.M6.AUX.2 Are Implicitly Sensitive to Metal Resize Directions

V5.AUX.1 requires V5 to be inside the intersection of M5 and M6. V5.M6.AUX.2 requires V5 to exactly match M6's width in the direction perpendicular to M6 length. The rejection of the M6 Y-resize plus M5 X-resize trial (trial:i02.cu.def:VIA_VIA56_2_2_66_58.01) demonstrates that independently resizing one enclosing metal without the other breaks the exact-width constraint of V5.M6.AUX.2 or causes V5 to protrude outside the resized metal, triggering V5.AUX.1. Always resize V5 shapes in concert with both M5 and M6 when any of these rules are active.

### Spacing Rules Require 33 nm in All Measurement Modes

V5.S.1, V5.S.2, and V5.S.3 each enforce a 33 nm minimum: projection-based spacing for same-net and different-net pairs, and Euclidean corner-to-corner spacing for cases not caught by projection. The successful unit-gate repair (trial:i03.ug.leaf_0013.09) involved coordinated moves at 32, -16, and 64 dbu offsets across a grid of nine instances, resolving spacing violations by distributing via positions rather than enlarging or shrinking individual shapes. When spacing violations are the root cause, prefer multi-instance positional adjustment over shape resizing.

### All V5 Geometry Must Remain Orthogonal

The NONORTHOGONAL block applies to the V5 layer. No non-orthogonal edges were introduced in any of the three recorded trials; all ops were axis-aligned moves and resizes (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02, trial:i02.cu.def:VIA_VIA56_2_2_66_58.01, trial:i03.ug.leaf_0013.09). All V5 resize and move operations must be constrained to X or Y axes only. Never apply diagonal or angled transforms to V5 shapes or the cells containing them.