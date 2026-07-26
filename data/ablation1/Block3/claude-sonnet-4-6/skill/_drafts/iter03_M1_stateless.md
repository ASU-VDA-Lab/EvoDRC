## Effective Repair Operations on M1

### move_instance in +X is the dominant correction action

Every iter-1 trial applied `move_instance` with a positive X displacement as the core or sole operation. Displacements of 36 dbu are the most common step: trial:i01.ug.Block3_union_row2.01, trial:i01.ug.Block3_union_row5.02, trial:i01.ug.leaf_0006.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0009.07, and trial:i01.ug.leaf_0012.08 all used 36 dbu per instance. Larger displacements of 108 dbu were applied selectively within the same batch: trial:i01.ug.Block3_union_row1.00 moved i0246 and i0205 by 108 dbu while moving i0233 by only 36 dbu; trial:i01.ug.Block3_union_row8.03 moved i0017 by 108 dbu alongside three 36-dbu moves. One trial used a negative X displacement: trial:i01.ug.leaf_0013.09 moved i0023 by [-36,0]. All ten iter-1 trials were accepted with n_new_in_crop=0, n_new_out_of_crop=0, and conn_preserved=true.

When multiple instances are displaced simultaneously, all ten iter-1 trials show that moves in the same X direction applied to two to four instances at once did not produce new violations (n_new_in_crop=0). Trial:i01.ug.Block3_union_row1.00 (3 instances), trial:i01.ug.Block3_union_row5.02 (3 instances), and trial:i01.ug.Block3_union_row8.03 (4 instances) confirm that coordinated group moves avoid introducing secondary M1 spacing violations between members of the moved set while opening the needed gap to neighboring polygons. When instances within a group need different displacement magnitudes (e.g., 36 vs. 108 dbu as in trial:i01.ug.Block3_union_row1.00 and trial:i01.ug.Block3_union_row8.03), the larger step is applied only to instances whose post-move position would otherwise still violate the spacing requirement; the smaller step is used for instances that already clear the rule at 36 dbu.

### resize_end on the M1 high-X edge repairs via-enclosure deficits

A `resize_end` operation extending the high-X end of an M1 polygon was paired with instance moves in trial:i01.ug.leaf_0008.06 (polygon p1261, axis=x, delta=36 dbu, end=high), trial:i02.ug.leaf_0001.00 (polygon p1261, axis=x, delta=72 dbu, end=high), and trial:i03.ug.leaf_0001.00 (polygon p1226, axis=x, delta=130 dbu, end=high). All three targeted the leaf_0001/leaf_0008 region. V0.M1.EN.1 requires M1 to enclose V0 by at least 5 nm on two opposite sides; V1.M1.EN.1 requires M1 to enclose V1 by 5 nm and 2 nm on opposite sides. Extending the M1 high-X edge directly adds enclosure on the horizontal projection side for whichever via type is under-enclosed in that area. Apply resize_end to the M1 end nearest the enclosure shortfall, not to the opposite end, as confirmed by all three trials targeting end=high in the +X direction.

### Residual enclosure violations grow across iterations and require increasing deltas

Polygon p1261 was resized by 36 dbu in trial:i01.ug.leaf_0008.06 and by 72 dbu in trial:i02.ug.leaf_0001.00. In trial:i03.ug.leaf_0001.00, the repair shifted to polygon p1226 with a 130 dbu resize alongside a 73 dbu instance move for i0239. The enclosure check must be re-run after every instance displacement that shifts a via relative to its covering M1 polygon; a resize applied in one iteration does not guarantee enclosure clearance in the next iteration if a subsequent move shifts the via or the M1 boundary again.

The iter-3 trial at this locus also shows that the instance displacement can be non-grid-aligned (73 dbu rather than a multiple of 36) when the residual enclosure gap requires it: trial:i03.ug.leaf_0001.00 used 73 dbu for i0239 and was still accepted (n_new_in_crop=0, conn_preserved=true, decision=gated_in).

### Y-direction moves occur only in broader multi-layer operations and may introduce new in-crop violations

The only Y-direction displacements appear in trial:i03.ug.leaf_0003.02, which moved i0085 and i0088 each by [0,-96] dbu (negative Y) while moving i0099 by [36,0]. This trial touched M1, M2, M3, M4, M5, V1, V3, V4 — the widest layer set in the history — and introduced n_new_in_crop=10, the only non-zero value across all 12 trials. The trial was still accepted (decision=gated_in) because conn_preserved=true and n_new_out_of_crop=0. New in-crop violations resulting from a Y move do not block acceptance in the unit_gate channel, provided no violations escape the crop boundary and connectivity is intact.

### Gating criterion: connectivity preservation and crop containment are binding; zero new in-crop violations is not required

All 12 trials were accepted with conn_preserved=true and n_new_out_of_crop=0. Trial:i03.ug.leaf_0003.02 with n_new_in_crop=10 confirms that the unit_gate channel will accept an operation that introduces new in-crop violations as long as the two binding constraints (connectivity preserved, violations not exported outside crop) are satisfied. Do not discard a repair candidate solely because it generates new in-crop M1 violations; verify instead that it passes the conn_preserved and n_new_out_of_crop checks, as demonstrated by trial:i03.ug.leaf_0003.02.

### All operations are strictly orthogonal

Every operation in the history uses axis-aligned displacements ([36,0], [108,0], [-36,0], [0,-96]) or an axis-aligned resize_end (axis=x). The NONORTHOGONAL rule outputs a violation for any M1 edge whose angle is not 0 or 90 degrees. No diagonal moves or non-rectilinear polygon reshaping appear in any of the 12 trials, confirming that all repair deltas must stay on the Manhattan grid.