**V2 is jointly constrained by M2 and M3 geometry**

V2.AUX.1 requires every V2 instance to lie entirely inside both M2 and M3. V2.M3.AUX.2 further requires that V2 width in the direction perpendicular to the M3 length exactly equals the M3 width in that direction. A Y-axis resize of M3 therefore couples directly to V2 geometry: both layers appeared in the touched-layer set of trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 (touched_layers: ["M2","M3","V2"]), confirming that modifying M3 width in Y propagates a V2 change in the same operation.

**Resizing M3 in Y without a net DRC gain is rejected**

trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 applied a -40 dbu Y-axis resize to the M3 shape inside cell VIA_VIA23_1_3_36_36, yielding delta_total=0 across both affected windows (leaf_0025: 88→88, leaf_0026: 35→35). The operation was rejected under decision "rejected_net_positive." Do not apply single-axis M3 shrinks when no active violation exists in the target windows: the zero-delta outcome confirms the resize addressed no outstanding DRC error in those windows.

**End-cap classification determines the applicable spacing rule**

V2.S.1 through V2.S.4 all branch on whether a V2 instance is classified as "with end-cap" (v2_wec: at least one edge not coincident with an M3 edge) or "no end-cap" (v2_nec: all edges fully flush with M3 edges). The applicable minimum changes significantly across cases: same-track spacing ranges from 18 nm (V2.S.1, aligned) to 27 nm (V2.S.1, not aligned); corner-to-corner euclidean spacing ranges from 23 nm (V2.S.2, both wec) to 30 nm (V2.S.3, both nec), with the mixed case at 27 nm (V2.S.4). Any repair that moves or resizes V2 relative to M3 must re-evaluate end-cap class before selecting a spacing target. trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 involved a Y-axis M3 resize that altered the M3-edge coincidence relationship for the touched V2 instances, confirming that axis-aligned M3 shape changes directly affect end-cap classification.

**V2 minimum width is 18 nm along the M3 length direction**

V2.W.1 sets a hard floor of 18 nm for V2 width along the M3 length direction. Never shrink a V2 shape such that its width in that direction falls below 18 nm. trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 touched V2 as part of a coordinated M3/V2 resize, confirming V2 dimensions are modified when the containing M3 is resized.

**M2 enclosure must be preserved on two opposite sides during any resize**

V2.M2.EN.1 requires M2 to enclose V2 by at least 5 nm on at least two opposite sides. trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 lists M2 in touched_layers alongside M3 and V2, confirming that via-shape resize operations affect M2 geometry in addition to V2 and M3. After any coordinated M3/V2 move or resize, verify M2 enclosure is ≥ 5 nm on the required pair of opposing sides before accepting the operation.

**M3 enclosure of V2 requires 5 nm on two opposite sides; flush (0 nm) is permitted on one side only**

V2.M3.EN.2 requires M3 to enclose V2 by 5 nm on two opposite sides and accepts either a 5&5 nm or a 5&0 nm pattern. Apply flush (0 nm) enclosure only when the corresponding V2 edge is fully coincident with the M3 edge, as V2.M3.AUX.2 also requires exact width matching in the perpendicular direction. Do not position V2 such that M3 enclosure is below 5 nm on both sides in either axis. trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 operated on a "resize_via_shape" op type, touching M3 and V2 together, which is the minimum coordinated scope required to maintain V2.M3.EN.2 and V2.M3.AUX.2 simultaneously.

**Non-orthogonal V2 edges are unconditionally forbidden**

The NONORTHOGONAL block applies to V2 as a member of all_drawing. No repair must introduce any V2 edge with angle in the ranges 1–89°, 91–179°, −179° to −91°, or −89° to −1°. All V2 shapes must use only axis-aligned (0° and 90°) edges. trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 used op type "resize_via_shape" on a rectangular geometry, which is the required orthogonal form.

**Connectivity preservation is achievable through coordinated M3/V2 resize**

trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 recorded conn_preserved=true despite simultaneously resizing M3 and touching V2 and M2. A coordinated resize of all three layers (M2, M3, V2) within the same via cell does not sever net connectivity when the via remains inside both metals.