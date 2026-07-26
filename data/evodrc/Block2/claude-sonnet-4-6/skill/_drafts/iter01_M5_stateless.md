## Repair Actions That Touch M5: Measured Outcomes

### VIA45 X-Axis Resize Reduces M5-Region Violations

Resizing both V4 shapes of cell `VIA_VIA45_1_2_58_58` by +152 dbu on the x-axis (two V4 shape_index entries plus the companion M4 shape) was applied and achieved a net violation reduction of 16 across the locus (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, `decision:"applied"`, `delta_total:-16`). This operation touches M5 as a consequence of the via cell geometry change. The rules most likely implicated in this locus are V4.M5.EN.2 (minimum enclosure of V4 by M5 on two opposite sides, 11 nm) and V4.M5.AUX.2 (V4 must be exactly the same width as M5 perpendicular to M5 length), since expanding V4 shapes in x affects the overlap relationship with underlying M5 metal. Do not apply this resize to via cells other than `VIA_VIA45_1_2_58_58` without independent measurement; the grounded record covers only this cell definition.

### Instance Moves Touching M5 Were Gated, Not Committed

Instance moves of i0097 and i0092 by [0, -48] dbu and i0064/i0072 by [0, +96] dbu (touching M3, M4, M5, V3, V4) were evaluated under the unit_gate channel and received `decision:"gated_in"` rather than full application (trial:i01.ug.leaf_0012.07). The move preserved connectivity (`conn_preserved:true`) and produced two new in-crop violations for V1.M1.EN.1 (a different layer), but the record does not confirm net improvement specifically to M5 rules. Do not treat gated_in as equivalent to applied; this move set has not been demonstrated to reduce M5 DRC violations.

### V4.M5 Enclosure and Alignment Rules Are Sensitive to Via Cell X-Dimension

The successful cu_pool operation (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01) resized via shapes on x only — no y-axis change. This is consistent with V4.M5.EN.2 and V4.M5.AUX.2 both operating primarily along x for a horizontally routed M5 segment: EN.2 checks 11 nm enclosure on two opposite sides, and AUX.2 requires V4 width to exactly match M5 width perpendicular to M5 length. An x-axis expansion of +152 dbu per shape edge addresses undersized enclosure margin without disturbing the vertical (y) alignment that M5.AUX.1 (24 nm x-grid) and M5.AUX.2 (routing track centerline snap) enforce.

### No M5-Specific Width, Spacing, or Grid Violations Have Been Repaired Yet

The two trials in this layer's history do not include any repair targeting M5.W.1 through M5.W.5, M5.S.1 through M5.S.5, M5.AUX.1, M5.AUX.2, M5.AUX.3, or M5.AUX.4 directly. No citation exists for x-grid snapping, width correction, spacing enlargement, bend removal, or routing-track centering on M5. Do not assert repair strategies for those rules until measured trials establish them.