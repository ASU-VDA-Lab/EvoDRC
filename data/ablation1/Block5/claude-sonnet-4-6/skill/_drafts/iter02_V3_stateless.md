**Coordinated Y-axis expansion of V3 via shapes reduces violations; isolated shrinkage increases them.**

In trial:i01.cu.def:VIA_VIA34_1_2_58_52.00, both V3 shapes (shape_index 0 and 1) in cell VIA_VIA34_1_2_58_52 were expanded along the Y axis by +88 dbu as part of a `chain_fix` group that simultaneously resized the enclosing M4 (+88 dbu Y), the stacked V4 shapes (+88 dbu Y), and the underlying M3 (+48 dbu Y). That coordinated operation reduced total DRC violations from 50 (25+25 across two windows) to 37 (18+19), a net improvement of -13, and the trial was applied. In trial:i02.cu.def:VIA_VIA23_1_3_36_36.01, V3 shapes in the same cell were shrunk by -112 dbu along Y (group `V2M3_corrected`), with a matching -112 dbu shrink of M3 and additional -32 dbu end-retractions on three M3 polygons (p891, p892, p893). That operation increased total violations from 36 (20+16) to 41 (28+13), a net deterioration of +5, and was rejected.

**Never shrink V3 shapes in Y without verifying that V3.M3.EN.1 and V3.M4.EN.2 enclosure minima are preserved.**

V3.M3.EN.1 requires M3 to enclose V3 by at least 5 nm on two opposite sides; V3.M4.EN.2 requires M4 to enclose V3 by at least 11 nm on two opposite sides. The -112 dbu Y shrink of V3 in trial:i02.cu.def:VIA_VIA23_1_3_36_36.01 was accompanied by an equal -112 dbu shrink of M3, meaning the M3-to-V3 enclosure relationship may have been maintained in magnitude but the absolute M3 length also shrank, which drove a net increase in violations (+8 in one window). Simultaneous shrinkage of both V3 and its enclosing M3 at the same rate does not guarantee enclosure compliance when other shapes on the same net interact within the spacing masks.

**V3.M4.AUX.2 mandates width-matching with M4 perpendicular to M4 length; resize V3 and M4 together along that axis.**

The rule requires V3 to be exactly the same width as M4 in the direction perpendicular to M4's length. In trial:i01.cu.def:VIA_VIA34_1_2_58_52.00 the successful chain_fix expanded both V3 and M4 by the same +88 dbu in Y, preserving this co-width constraint and yielding a net violation reduction of -13. Any operation that resizes V3 in Y without a matching M4 resize in Y will violate V3.M4.AUX.2.

**V3.AUX.1 is a strict containment rule; V3 must remain inside both M3 and M4 after every operation.**

Both trials touched M3 alongside V3. In trial:i01.cu.def:VIA_VIA34_1_2_58_52.00, M3 received a +48 dbu Y expansion (smaller than V3's +88 dbu), yet the trial was applied successfully, indicating the pre-existing M3 geometry already provided sufficient margin. In trial:i02.cu.def:VIA_VIA23_1_3_36_36.01, M3 was shrunk by -112 dbu in Y together with V3, and violations increased. Do not shrink M3 and V3 together by large symmetric amounts when the resulting geometry pushes V3 toward or past the M3 boundary.

**The `chain_fix` group pattern—expanding V3 together with its neighboring M4 and V4 in the same direction and by the same delta—is the only applied, violation-reducing pattern in the measured history.**

Trial:i01.cu.def:VIA_VIA34_1_2_58_52.00 is the sole accepted operation. It expanded V3 (two shapes, +88 dbu Y), M4 (+88 dbu Y), V4 (two shapes, +88 dbu Y), and M3 (+48 dbu Y) in a single coordinated group. The `V2M3_corrected` group pattern from trial:i02.cu.def:VIA_VIA23_1_3_36_36.01 (shrinking V3, M3, and polygon ends simultaneously) produced a net-positive outcome and was rejected. Prefer the chain_fix expansion pattern over correction-by-shrinkage patterns for V3.

**V3.S.1 spacing violations are sensitive to the M4 end-cap classification of each via instance.**

V3.S.1 enforces three distinct minimums depending on track alignment and end-cap presence (18 nm same-track, 27 nm parallel non-aligned, 18 nm parallel aligned). The DRC deck computes separate masks for vias with full M4 edge coincidence (`v3_nec`) versus those with partial coincidence (`v3_wec`), and checks spacing on mask edges not coincident with M4. Expanding V3 shapes along Y—as done in trial:i01.cu.def:VIA_VIA34_1_2_58_52.00—changes which mask category a via falls into and how the 5 nm end-cap extension is computed. Always verify the post-resize end-cap classification of every modified V3 instance against V3.S.2 (23 nm corner-to-corner, both with end-cap), V3.S.3 (30 nm corner-to-corner, neither with end-cap), and V3.S.4 (27 nm corner-to-corner, mixed) after any Y-axis change.

**V3.W.1 sets an 18 nm floor on V3 width along the M4 length direction; the +88 dbu (~8.8 nm at 0.1 nm/dbu) expansion in trial:i01 implies shapes were already above this floor and had headroom to grow.**

In trial:i01.cu.def:VIA_VIA34_1_2_58_52.00, a +88 dbu expansion was applied and the trial cleared, confirming no V3.W.1 violation was introduced by that resize. No trial has recorded a V3.W.1 violation as the cause of rejection; the only rejection in the history (trial:i02.cu.def:VIA_VIA23_1_3_36_36.01) was due to net-positive violation count, not a specific rule flag. Do not shrink V3 width along the M4 direction below 18 nm (180 dbu at 0.1 nm/dbu scale).