## M4 Vertical Moves and Routing Track Alignment

The M4.AUX.2 rule constrains minimum-width M4 tracks to a 192-dbu pitch grid with a 48-dbu offset from the origin. All vertical movements of M4 geometry must land on this grid.

Vertical instance moves of −48 and +96 dbu produced zero new in-crop violations when M4 was among the touched layers (trial:i01.ug.leaf_0012.07). A vertical instance move of +48 dbu likewise produced zero new violations (trial:i03.ug.leaf_0001.00). Both 48 and 96 are integer multiples of 48 and therefore preserve alignment on the 192-dbu routing track grid.

Vertical instance moves of ±72 dbu introduced one new in-crop violation when M4, M3, M5, V3, and V4 were all touched (trial:i03.ug.leaf_0002.01). The value 72 is not a multiple of 48 and does not land on the 192-dbu routing track grid. Move instances vertically only in multiples of 48 dbu when M4 is among the touched layers; do not use 72-dbu or other non-multiples-of-48 increments (trial:i03.ug.leaf_0002.01).

Vertical moves of +36 dbu applied to an M4 polygon (p1036) and to an instance (i0063) introduced one new in-crop violation when M4, M1, M2, M5, V1, and V4 were all touched (trial:i04.ug.leaf_0002.01). The value 36 is not a multiple of 48. Do not use 36-dbu vertical steps for M4 geometry (trial:i04.ug.leaf_0002.01).

## M4 Horizontal End Resizing

The unit_gate channel applied simultaneous resize_end operations to two M4 polygons: p1065 high end +184 dbu in x and p957 low end +176 dbu in x. Both produced zero new in-crop violations (trial:i01.ug.leaf_0001.03). A subsequent smaller adjustment of −4 dbu to the low end of p957 in x also produced zero new violations (trial:i02.ug.leaf_0001.00). Horizontal end resizing in the range of −4 to +184 dbu has been observed safe for M4 when connectivity is preserved.

When resizing M4 polygon ends in x, coordinate both the high and low ends of adjacent polygons together to avoid creating M4.S.2 violations (min horizontal spacing 40 nm between vertical edges); the paired resize of p1065 and p957 achieved this and produced no new violations (trial:i01.ug.leaf_0001.03).

## M4 Horizontal Polygon Moves

Moving M4 polygon p938 in x by +32 dbu produced zero new in-crop violations when M4, M5, and V4 were touched (trial:i02.ug.leaf_0002.01).

Moving M4 polygon p937 in x by −64 dbu, combined with moving several instances in x by −64 dbu and instance i0063 and polygon p1036 in y by +36 dbu, introduced one new in-crop violation when M4, M1, M2, M5, V1, and V4 were touched (trial:i04.ug.leaf_0002.01). The new violation in this trial cannot be isolated to the M4 polygon move alone because the y-move of +36 dbu (which independently violates the 48-dbu grid constraint) was applied in the same trial. Do not combine horizontal M4 polygon moves with off-grid vertical moves in the same operation set (trial:i04.ug.leaf_0002.01).

## Via Cell M4 Shape Resizing (VIA_VIA45_1_2_58_58)

The cu_pool channel applied a resize_via_shape operation on the M4 shape (shape_index 0) in cell VIA_VIA45_1_2_58_58, increasing its x-dimension by +152 dbu. This was the sole M4-touching operation in that trial and reduced the aggregate violation count by 16 (delta_total = −16), making it the single highest-yield M4 repair observed in this history (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01).

The same resize_via_shape operation on this M4 shape subsequently appeared in the assemble_drops list of a unit_gate trial with the reason cu_pool:applied (trial:i01.ug.leaf_0012.07). This confirms the cu_pool channel applies via shape resizes independently and prior to unit_gate assembly. Do not re-issue the same resize_via_shape on M4 shape_index 0 of VIA_VIA45_1_2_58_58 in unit_gate trials once cu_pool has already applied it; the harness will drop it (trial:i01.ug.leaf_0012.07).

## Multi-Instance Moves Touching M4

Instance moves that touch M4 indirectly—by moving instances whose cells contain M4 geometry—behave identically to direct M4 operations from the perspective of DRC outcome. Moving four instances vertically by −48 and +96 dbu while touching M3, M4, M5, V3, and V4 produced two new V1.M1.EN.1 violations but zero new M4-rule violations (trial:i01.ug.leaf_0012.07), indicating vertical instance moves aligned to multiples of 48 are safe for M4 even when other layers are also displaced.

Moving instances i0095, i0099 by +72 dbu and i0069, i0066 by −72 dbu (touching M3, M4, M5, V3, V4) introduced one new in-crop violation (trial:i03.ug.leaf_0002.01), consistent with the 72-dbu off-grid constraint described above. Moving instances i0099, i0111, i0061, i0066 by −64 dbu in x alongside the off-grid +36 dbu y-move also introduced one new in-crop violation (trial:i04.ug.leaf_0002.01). Avoid combining off-grid y-moves with x-displacement of M4-touching instances in the same operation group (trial:i04.ug.leaf_0002.01).