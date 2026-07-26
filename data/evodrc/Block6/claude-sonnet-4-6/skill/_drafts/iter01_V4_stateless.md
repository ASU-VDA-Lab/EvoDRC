## Effective Repair Pattern: Symmetric X-Axis Spread with Co-Resize

The only measured repair for V4 in this iteration targeted cell `VIA_VIA45_1_2_58_58` in Block6 (channel `cu_pool`). The repair was applied and reduced total DRC violations by 52 across two windows (unit:leaf_0019: −28, unit:leaf_0020: −24), with connectivity preserved (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01).

The repair comprised five operations all on the x-axis:

1. Move V4 shape 0 by −116 dbu in x
2. Move V4 shape 1 by +116 dbu in x
3. Resize V4 shape 0 by +384 dbu in x
4. Resize V4 shape 1 by +384 dbu in x
5. Resize M4 shape 0 by +152 dbu in x

This pattern — moving a pair of V4 shapes symmetrically outward while also widening each in x, then widening the enclosing M4 shape — achieved net violation reduction without breaking connectivity (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01). The co-resize of M4 is necessary when V4 shapes are repositioned or enlarged in x: widening V4 without correspondingly widening M4 risks triggering V4.M4.EN.1, which requires at least 11 nm enclosure on two opposite sides (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01).

## Rule-Grounded Repair Guidance

**V4.W.1 (minimum width 24 nm):** Resize operations on V4 shapes must not reduce x-dimension below 24 nm. The measured resize of +384 dbu per V4 shape moved both shapes further from this lower bound (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01); shrinking V4 in x is not a viable repair direction for any rule that does not specifically require width reduction.

**V4.S.1 / V4.S.2 / V4.S.3 (minimum spacing 33 nm, projection and euclidean):** Moving two V4 shapes apart symmetrically (−116 dbu and +116 dbu on x) directly increases their projected separation. The applied symmetric spread on x in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 produced a net violation reduction of 52; use symmetric outward x-moves on a via pair when spacing rules fire on adjacent V4 shapes.

**V4.M4.EN.1 (enclosure by M4 ≥ 11 nm on two opposite sides):** After any V4 move or resize in x, the enclosing M4 shape must be co-resized to maintain enclosure. In trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, M4 shape 0 was widened by +152 dbu in x to accompany the V4 repositioning and enlargement. Do not move or resize V4 in x without auditing M4 enclosure margins on both the near and far x-edges.

**V4.M5.EN.2 (enclosure by M5 ≥ 11 nm on two opposite sides):** V4 must sit 11 nm inside M5 on at least two opposite sides. The repair in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 touched M5 (listed under `touched_layers`) but applied no explicit M5 resize operation; the V4 resize of +384 dbu per shape in x must have remained within M5 bounds. Before widening V4 in x, verify that M5 provides sufficient enclosure; if not, M5 must also be co-resized.

**V4.AUX.1 (V4 must be inside both M4 and M5):** All five operations in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 preserved the inside-both-layers condition (conn_preserved: true, decision: applied). Any x-axis move or resize of a V4 shape must be checked against both M4 and M5 extents before committing; violating V4.AUX.1 is a hard failure.

**V4.M5.AUX.2 (V4 width must exactly match M5 width perpendicular to M5 length):** This rule constrains V4 width in the cross-M5 direction to be identical to the M5 width in that direction. When resizing V4 in x, if x is the cross-M5 direction, V4 and M5 must be resized together to remain coincident on both lateral edges. The trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 repair touched M5 (in `touched_layers`) even though no explicit M5 resize op appears; this indicates the existing M5 width already accommodated the V4 resize, or that M5 edge coincidence was maintained implicitly. Do not resize V4 in the cross-M5 direction without verifying V4.M5.AUX.2 compliance.

**GEOMETRY.NONORTHOGONAL:** All V4 operations in the measured history were strictly x-axis moves and resizes (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01). Never introduce diagonal or angled edges on V4; all repair deltas must be axis-aligned.

## Op-Level Observations

The locus [1728, 2068, 15336, 15216] and the two affected windows (unit:leaf_0019, unit:leaf_0020) span a region where a single via cell instance influenced violations in two distinct layout windows simultaneously. A single 5-op repair addressing both windows in one pass produced the total −52 reduction (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01). When a V4 cell instance straddles multiple violation windows, a combined move-and-resize strategy that addresses enclosure and spacing simultaneously is more efficient than sequential single-rule fixes.

The repair moved the two V4 shapes outward by 116 dbu each (total separation increase: 232 dbu) and widened each by 384 dbu in x, for a gross x-extension of 384 dbu per shape. The M4 co-resize of 152 dbu in x is smaller than the V4 resize, consistent with M4 already providing partial enclosure margin before the repair. When M4 already partially encloses V4 in x, the required M4 co-resize delta is less than the V4 resize delta (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01).