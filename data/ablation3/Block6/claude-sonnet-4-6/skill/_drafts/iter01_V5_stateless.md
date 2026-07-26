## Repair Strategy

### Y-axis resize is the confirmed repair operation for V5 violation reduction

The sole verified repair in this layer's history applies `resize_via_shape` along the y-axis to all V5 shapes within a via cell. In trial:i01.cu.def:VIA_VIA56_2_2_66_58.01, resizing all four V5 shapes in cell `VIA_VIA56_2_2_66_58` by +248 dbu on the y-axis reduced the total violation count by 32 (247 → 215), with connectivity preserved and the decision accepted. Do not attempt x-axis-only resizes as a first move for multi-shape via cells when y-axis enclosure or width deficits are suspected; the confirmed productive direction from measured data is y-axis (trial:i01.cu.def:VIA_VIA56_2_2_66_58.01).

### Apply resize to all shapes in the via cell together

In trial:i01.cu.def:VIA_VIA56_2_2_66_58.01, four separate V5 shape indices (0, 1, 2, 3) within the same cell each received an identical +248 dbu y-axis resize in a single applied operation (n_ops=4). Never resize a subset of shapes within a via cell while leaving others unchanged; apply a uniform delta to every shape index in the cell to avoid introducing intra-cell spacing or enclosure asymmetry (trial:i01.cu.def:VIA_VIA56_2_2_66_58.01).

### Touched-layer scope: M5, M6, and V5 are co-modified

The accepted repair in trial:i01.cu.def:VIA_VIA56_2_2_66_58.01 reported touched layers M5, M6, and V5. This confirms that a y-axis resize of V5 shapes propagates geometry changes across both enclosing metal layers. When evaluating post-repair DRC impact, always check V5.AUX.1 (V5 must remain inside both M5 and M6), V5.M5.EN.1, V5.M6.EN.2, and V5.M6.AUX.2 after any resize, because the enclosing metal boundaries move alongside the via (trial:i01.cu.def:VIA_VIA56_2_2_66_58.01).

### Enclosure rules require symmetric opposite-side coverage

Rule V5.M5.EN.1 requires M5 to enclose V5 by at least 11 nm on at least two opposite sides; V5.M6.EN.2 imposes the same 11 nm minimum on two opposite sides of M6. A y-axis resize that increases V5 extent in both +y and −y directions simultaneously satisfies opposite-side enclosure. The confirmed +248 dbu y-axis resize across all four shapes in trial:i01.cu.def:VIA_VIA56_2_2_66_58.01 addressed enclosure deficits without violating connectivity, establishing 248 dbu as a repair magnitude that cleared violations in this cell geometry.

### Width rule imposes a 24 nm floor along M6 length direction

Rule V5.W.1 sets a minimum via width of 24 nm measured along the M6 length direction. Any resize that shrinks V5 extent in that direction must be rejected if the resulting dimension would fall below 24 nm. The only measured resize (trial:i01.cu.def:VIA_VIA56_2_2_66_58.01) was an expansion (+248 dbu), not a shrink, and was accepted; no shrink operations have been measured on this layer, so do not apply negative-delta resizes without verifying the post-resize width against 24 nm.

### Spacing rules use projection metric at 33 nm

Rules V5.S.1 and V5.S.2 enforce a minimum 33 nm projected spacing between V5 instances, whether on the same or different nets. Rule V5.S.3 enforces a 33 nm Euclidean corner-to-corner spacing for cases not covered by projection. When expanding V5 shapes in y (as in trial:i01.cu.def:VIA_VIA56_2_2_66_58.01), verify that no neighboring V5 instance falls within 33 nm in the projection direction after the resize; a net reduction of 32 violations was achieved without introducing new spacing errors, confirming that the +248 dbu delta did not violate V5.S.1, V5.S.2, or V5.S.3 in this layout context.

### V5.M6.AUX.2 constrains cross-M6 width to exact match

Rule V5.M6.AUX.2 requires that V5 width perpendicular to the M6 length direction exactly equals M6 width at that location — edges must be coincident on both sides. Because the accepted repair in trial:i01.cu.def:VIA_VIA56_2_2_66_58.01 touched M6 alongside V5, the resize preserved this coincidence constraint. Never resize V5 in the dimension perpendicular to M6 length without simultaneously adjusting M6 to match, or V5.M6.AUX.2 will fire; the co-modification of M6 observed in trial:i01.cu.def:VIA_VIA56_2_2_66_58.01 is mandatory, not optional.

### V5.AUX.1 requires full containment inside both M5 and M6

V5 must reside entirely within the intersection of M5 and M6. The repair in trial:i01.cu.def:VIA_VIA56_2_2_66_58.01 preserved connectivity (conn_preserved=true) and was accepted, confirming that the +248 dbu y-axis expansion kept all four V5 shapes inside both enclosing metals. Before applying any resize, confirm that the expanded V5 boundary does not exceed either M5 or M6 extents; if the metal boundary is the limiting factor, expand the metal first (as the co-modification of M5 and M6 in trial:i01.cu.def:VIA_VIA56_2_2_66_58.01 demonstrates is permissible).

### Orthogonality must be preserved on all V5 geometry

The NONORTHOGONAL block flags any edge whose angle deviates from 0°/90°/180°/270°. All `resize_via_shape` operations in trial:i01.cu.def:VIA_VIA56_2_2_66_58.01 operated on rectilinear shapes along an axis-aligned direction (+y), producing no diagonal edges. Never introduce diagonal cuts or non-axis-aligned moves on V5 shapes; axis-aligned resizes are the only confirmed safe operation class (trial:i01.cu.def:VIA_VIA56_2_2_66_58.01).

### Channel and cell-type context

The single confirmed repair targets cell `VIA_VIA56_2_2_66_58` via channel `cu_pool` in Block6 (trial:i01.cu.def:VIA_VIA56_2_2_66_58.01). The cell name encodes a V5–M6 via stack (VIA56) with nominal dimensions 2×2 on a 66×58 pitch. When encountering this cell type, a y-axis resize of all V5 shapes by approximately 248 dbu is a measured-successful starting point. For other cell geometries, the same axis (y) and direction (expansion) apply as the first-attempt strategy, but the magnitude must be derived from the specific enclosure or width deficit present.