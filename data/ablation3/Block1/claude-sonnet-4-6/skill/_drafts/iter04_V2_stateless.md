## Rule Geometry Summary

**V2.W.1** requires every V2 instance to be at least 18 nm wide along the M3 length direction.

**V2.S.1** enforces projection-based spacing between V2 mask shapes. The effective minimum depends on track alignment: 18 nm between instances on the same M3 track or on aligned parallel M3 tracks, and 27 nm between instances on non-aligned parallel M3 tracks. The spacing check operates on a derived mask (`v2_mask`) that incorporates M3 end-cap extensions of 5 nm, so the spacing seen in layout coordinates between bare V2 rectangles will differ from the rule threshold.

**V2.S.2** sets a 23 nm Euclidean corner-to-corner floor between any two `v2_wec` (with-end-cap) instances. **V2.S.3** sets 30 nm Euclidean corner-to-corner between two `v2_nec` (no-end-cap) instances. **V2.S.4** sets 27 nm Euclidean corner-to-corner between a `v2_wec` and a `v2_nec` instance. These three rules fire only on diagonal (non-projection) violations; a spacing edge-pair that also fires under projection measurement is excluded.

**V2.M2.EN.1** requires M2 to enclose V2 by at least 5 nm on at least two opposite sides. The check uses independent x and y size erosions, so both axis pairs must be evaluated when assessing enclosure coverage.

**V2.M3.EN.2** requires M3 to enclose V2 by 5 nm on two opposite sides (the allowed patterns are 5 & 5 nm or 5 & 0 nm). A V2 entirely outside M3 always violates this rule; a V2 inside M3 that lacks the required two-sided enclosure also fires.

**V2.AUX.1** requires every V2 polygon to lie fully inside both M2 and M3. Any V2 that is outside either metal layer is an unconditional violation.

**V2.M3.AUX.2** requires V2 to have exactly the same width as the enclosing M3 wire in the direction perpendicular to the M3 length. A V2 narrower or wider than the M3 track in that cross-cut direction will fire this rule, even if it satisfies V2.W.1 and V2.M3.EN.2.

**NONORTHOGONAL** applies globally: every edge on V2 must be at exactly 0° or 90°. Any non-rectilinear geometry on V2 is an unconditional violation.

## Measured Repair Observations

### M3 y-axis shrink on VIA_VIA23_1_3_36_36 produced zero net DRC change

In trial:i04.cu.def:VIA_VIA23_1_3_36_36.00, the operation `resize_via_shape` on the M3 layer of cell `VIA_VIA23_1_3_36_36` applied a delta of −40 dbu along the y-axis. The trial was rejected with decision `rejected_net_positive` and `delta_total` of 0: no violation count improved and none worsened. Do not apply a y-axis shrink to the M3 shape of this cell as a V2 DRC repair; the outcome is a null move (trial:i04.cu.def:VIA_VIA23_1_3_36_36.00).

The touched-layer set for that operation was {M2, M3, V2} and connectivity was confirmed preserved, so the rejection was not a connectivity failure. The zero delta indicates the M3 y-shrink did not shift any V2-related violation boundary (trial:i04.cu.def:VIA_VIA23_1_3_36_36.00).

### Interaction between M3 resize and V2.M3.AUX.2

Because V2.M3.AUX.2 requires V2 to match the M3 track width in the perpendicular direction, any resize of M3 in the axis perpendicular to its length without a corresponding resize of the V2 shape risks introducing or sustaining a V2.M3.AUX.2 violation. The trial:i04.cu.def:VIA_VIA23_1_3_36_36.00 result — zero net change despite a −40 dbu M3 y-shrink — is consistent with V2 and M3 remaining mismatched in width after the operation, neither creating nor closing any violation.

Do not resize only M3 in the perpendicular direction while leaving V2 untouched; the coupled nature of V2.M3.AUX.2 means the repair must move both shapes together to have any chance of a net improvement (trial:i04.cu.def:VIA_VIA23_1_3_36_36.00).