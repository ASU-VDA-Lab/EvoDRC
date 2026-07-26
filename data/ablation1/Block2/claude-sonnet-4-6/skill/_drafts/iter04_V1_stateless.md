## Repair Operation Patterns

All ten trials in the measured history were accepted (`decision: gated_in`, `conn_preserved: true`). The `target` field is null in every record, so no trial directly names the V1 DRC rule that triggered the repair. The assertions below describe operational patterns observed across accepted trials.

### Multi-Layer Coupling

Every accepted trial touched M1, M2, and V1 simultaneously — none modified V1 in isolation. One trial also touched M4 (trial:i02.ug.leaf_0001.00). Because V1.AUX.1 requires V1 to lie inside both M1 and M2, and V1.M1.EN.1 and V1.M2.EN.2 impose enclosure requirements on both surrounding metal layers, any operation that repositions or replaces a V1 instance must keep M1 and M2 geometry consistent. Treat V1 repairs as inherently three-layer (M1, M2, V1) operations.

### Move-Instance as the Primary Repair

The dominant operation across trials is `move_instance`. It appeared in all ten trials, often as the sole operation (trial:i01.ug.leaf_0004.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0011.06, trial:i01.ug.leaf_0013.08, trial:i04.ug.leaf_0001.00). The most common displacement is 36 dbu along the x-axis (trial:i01.ug.Block2_union_row1.00, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0001.03, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0011.06, trial:i01.ug.leaf_0013.08, trial:i04.ug.leaf_0001.00); one trial used 37 dbu (trial:i01.ug.leaf_0004.04) and one used 12 dbu (trial:i01.ug.leaf_0001.03). Apply move_instance as the first repair option; a one-grid-step shift in x is the most recurrent successful delta.

### Supplementary M1 Polygon Addition

When moving an instance alone leaves M1 coverage insufficient, adding a new M1 polygon alongside the move resolved the case. In trial:i01.ug.leaf_0001.03 a 200 x 108 dbu M1 rectangle was added while also moving instance i0086 by 12 dbu. This is consistent with V1.M1.EN.1, which requires M1 to enclose V1 by 5 nm on one axis and 2 nm on the other; after an instance shift, the M1 footprint may no longer satisfy the enclosure requirement on both sides, making a supplementary M1 polygon necessary.

### Via Replacement

A more invasive repair — delete the via polygon, delete the via instance, add a fresh VIA_VIA12 at the new location, and resize the endpoint of an adjacent M1 or M2 wire — was accepted in trial:i02.ug.leaf_0001.00. This pattern is appropriate when the existing via cell's shape cannot satisfy V1.M2.AUX.2 (V1 width must equal M2 width perpendicular to M2 length) at its current position, or when V1.M2.EN.2 enclosure cannot be recovered by a simple move alone. The matching resize operation (axis x, delta 172 dbu, end low, polygon p957) reclaimed the correct M2 wire extent after the via was relocated.

### Tolerance for Incidental New Violations

Trial:i01.ug.leaf_0013.08 introduced one new in-crop M1.A.1 violation (`n_new_in_crop: 1`) yet was still gated in because connectivity was preserved. The harness accepts a repair that creates a new non-V1 in-crop violation as long as `conn_preserved` is true and no new out-of-crop violations appear. Do not reject a V1 repair candidate solely because it incidentally worsens an M1 area rule; connectivity preservation is the primary acceptance gate.

### Spacing Rules: Geometry Context Required

V1.S.1 through V1.S.4 distinguish between via instances that have a 5 nm M2 end-cap (wec) and those that do not (nec), with different minimum spacings for wec-wec (23 nm, euclidean), nec-nec (30 nm, euclidean), and mixed wec-nec (27 nm, euclidean) corner-to-corner cases, plus projection-based spacing (18 nm same-track, 27 nm parallel not-aligned, 18 nm parallel aligned). The measured trials resolved spacing issues via move_instance without altering via cell type, so the applicable spacing floor depends on the wec/nec classification of both vias involved. Determine whether each via's edges coincide with M2 edges before selecting the target separation distance.

### Width and Enclosure Minimums

V1.W.1 sets 18 nm minimum width along the M2 direction. V1.M2.EN.2 requires M2 to enclose V1 by 5 nm on both sides, or by 5 nm on one side and flush (0 nm) on the other — but flush (zero enclosure) on one side requires the V1 edge to exactly coincide with the M2 edge. V1.M1.EN.1 requires M1 enclosure of 5 nm on one axis and 2 nm on the other. All measured repairs preserved these constraints; no trial attempted to shrink a via below 18 nm or relax enclosure below the minimum. Do not reduce via size as a spacing repair; use instance displacement or wire-end resize instead (as in trial:i01.ug.Block2_union_row1.00 and trial:i02.ug.leaf_0001.00).