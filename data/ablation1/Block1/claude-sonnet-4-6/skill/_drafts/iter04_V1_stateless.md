## Repair Operation Catalogue

Every trial in this layer's history was accepted (decision: gated_in) via the unit_gate channel with conn_preserved=true and n_new_out_of_crop=0. No trial was rejected. All patterns below describe accepted operations.

### move_instance

Moving V1-bearing instances along the x-axis is the most frequent single repair primitive. Accepted x-deltas include ±32 dbu, ±36 dbu, ±72 dbu, and ±108 dbu (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row8.07, trial:i01.ug.Block1_union_row5.05, trial:i01.ug.Block1_union_row6.06, trial:i01.ug.Block1_union_row9.08, trial:i01.ug.leaf_0004.09, trial:i01.ug.leaf_0020.10, trial:i02.ug.Block1_union_row6.01, trial:i03.ug.Block1_union_row3.00, trial:i03.ug.leaf_0004.01, trial:i03.ug.leaf_0005.02, trial:i04.ug.leaf_0001.00). One accepted trial also included a simultaneous y-delta of −36 dbu on the same instance (trial:i01.ug.Block1_union_row4.04).

Moving multiple instances within the same crop window in a single trial is accepted; up to five move_instance ops appear together (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row5.05, trial:i01.ug.Block1_union_row8.07, trial:i02.ug.Block1_union_row6.01). A single-instance x-move of 4 dbu on a widely-shared instance spanning a large locus is also accepted (trial:i04.ug.leaf_0004.03).

### resize_end on M2

Extending an M2 polygon end (resize_end) is accepted alongside move_instance to satisfy enclosure rules. Accepted x-deltas for resize_end: 36 dbu (trial:i01.ug.Block1_union_row5.05, trial:i01.ug.leaf_0020.10, trial:i03.ug.leaf_0004.01), 52 dbu (trial:i01.ug.Block1_union_row4.04), 72 dbu (trial:i03.ug.leaf_0004.01 on p1295), 92 dbu (trial:i01.ug.Block1_union_row3.03 on p1370, trial:i01.ug.Block1_union_row1.00 on p1321), and 128 dbu (trial:i01.ug.Block1_union_row1.00 on p1320). Both "high" and "low" ends are used within the same trial (trial:i01.ug.Block1_union_row5.05 on p1297 and p1301, trial:i01.ug.leaf_0020.10 on p1253).

V1.M2.EN.2 requires M2 to enclose V1 by 5 nm on two opposite sides. Extending the M2 end via resize_end directly addresses enclosure shortfalls on the end-cap axis. The repeated use of resize_end alongside move_instance in the same trial confirms these two primitives together address coupled V1.M2.EN.2 and V1.S.1 violations (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row3.03, trial:i01.ug.Block1_union_row4.04).

When a trial combines move_instance and resize_end, move_instance ops appear first in the recorded operation sequence, followed by resize_end ops (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row3.03, trial:i01.ug.Block1_union_row4.04, trial:i01.ug.Block1_union_row5.05).

### resize (symmetric) on M2

A symmetric resize of 36 dbu on M2 polygon p1390 was accepted together with a move_instance (trial:i01.ug.leaf_0031.11). Use symmetric resize when both ends of the M2 polygon require adjustment; use resize_end when only one end is deficient.

### delete_instance + add_via (VIA_VIA12)

Replacing a misaligned via instance by deleting it and inserting a VIA_VIA12 cell at a corrected origin is accepted (trial:i02.ug.leaf_0004.02). The deletion precedes the insertion in the recorded operation sequence. This strategy resolves violations that arise when a via position cannot be corrected by translation alone within the existing M2 boundary, such as V1.AUX.1 or V1.M2.AUX.2 violations caused by positional conflict with M2 geometry.

## New-Violation Tolerance Under gated_in

The gating criterion accepts new DRC violations introduced within the crop locus provided connectivity is preserved (conn_preserved=true) and no new violations appear outside the crop (n_new_out_of_crop=0). Do not abort a repair sequence solely because in-crop violation counts increase. Trials with n_new_in_crop of 1, 4, and 80 were all accepted on this basis (trial:i01.ug.Block1_union_row6.06 n_new_in_crop=1; trial:i01.ug.Block1_union_row1.00 and trial:i01.ug.leaf_0031.11 n_new_in_crop=4; trial:i04.ug.leaf_0004.03 n_new_in_crop=80). A fine-grain positional adjustment on a widely-shared instance can generate many in-crop DRC interactions and still be accepted under this criterion (trial:i04.ug.leaf_0004.03).

## Iterative Re-visitation of Loci

The same crop locus is re-visited across iterations with different operation sets, each accepted independently. Locus [8152,7668,13752,8532] was repaired in iter 1 with a single move_instance and again in iter 2 with five move_instance ops on different instances (trial:i01.ug.Block1_union_row6.06, trial:i02.ug.Block1_union_row6.01). Locus [5128,4428,11376,5292] was repaired in iter 1 with a move_instance + resize_end pair and re-visited in iter 3 with three move_instance ops on different instances (trial:i01.ug.Block1_union_row3.03, trial:i03.ug.Block1_union_row3.00). Locus [5344,5508,...] used move_instance + resize_end in iter 1 and then delete_instance + add_via in iter 2 (trial:i01.ug.Block1_union_row4.04, trial:i02.ug.leaf_0004.02). Re-visiting a locus does not indicate a failed prior repair; it reflects residual or newly exposed violations after upstream design-state changes.

## Rule-Specific Guidance

### V1.W.1 — Minimum width 18 nm

V1.M2.AUX.2 constrains V1 width to equal the M2 width perpendicular to the M2 length direction, so widening M2 via resize or resize_end satisfies both rules simultaneously. The symmetric resize on p1390 (trial:i01.ug.leaf_0031.11) and the resize_end extensions across multiple polygons confirm that adjusting M2 geometry is the effective path for width violations. Apply symmetric resize when V1.M2.AUX.2 is the primary target, not resize_end, because resize_end changes only one end and would shift the V1 width boundary rather than expanding it uniformly (trial:i01.ug.leaf_0031.11).

### V1.S.1 — Spacing between V1 instances (same-track, parallel-track, aligned)

V1.S.1 operates on v1_mask geometry derived from M2 edge coincidence. V1 instances with full M2 flush (nec, no end-cap) require 18 nm same-track projection spacing; those with 5 nm end-cap (wec) require 18 nm projection spacing; cross-track non-aligned pairs require 27 nm. Moving instances in x to increase their separation is the primary resolution primitive (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row5.05, trial:i01.ug.Block1_union_row8.07, trial:i01.ug.Block1_union_row9.08). When spacing and enclosure violations co-occur, pair move_instance with resize_end so that M2 end-cap geometry changes do not reintroduce enclosure shortfalls on the repositioned via (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row3.03, trial:i01.ug.Block1_union_row4.04).

### V1.S.2 / V1.S.3 / V1.S.4 — Corner-to-corner spacing

These rules use euclidian checks on v1_wec_mask (S.2, 23 nm), v1_nec_mask (S.3, 30 nm), and their cross-separation (S.4, 27 nm). The effective correction is to increase euclidian distance between via mask geometries by moving instances away from each other in x — and, where necessary, in y as well (trial:i01.ug.Block1_union_row4.04). When extending the M2 end-cap via resize_end changes a via from nec to wec classification, also verify the S.3 and S.4 euclidian clearances at the previously flush edge, as the mask geometry changes under that reclassification (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row3.03).

### V1.M1.EN.1 — M1 enclosure (5 & 2 nm on opposite sides)

V1 must have M1 enclosure of at least 5 nm on one projection axis and 2 nm on the other. Moving a V1 instance in x within its M1 enclosing rectangle corrects enclosure shortfalls on the horizontal axis without requiring M1 geometry changes, as confirmed by the prevalence of x-only move_instance repairs across multiple rows (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row9.08, trial:i01.ug.leaf_0004.09, trial:i04.ug.leaf_0001.00). After any move, confirm V1.AUX.1 compliance — V1 must remain inside both M1 and M2.

### V1.M2.EN.2 — M2 enclosure (5 & 5 nm or 5 & 0 nm on opposite sides)

M2 enclosure violations on the end axis are resolved by extending M2 ends using resize_end. Accepted end extensions range from 36 dbu to 128 dbu in x (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row3.03, trial:i01.ug.Block1_union_row4.04, trial:i01.ug.Block1_union_row5.05, trial:i01.ug.leaf_0020.10, trial:i03.ug.leaf_0004.01). V1.M2.EN.2 also prohibits non-zero enclosure on an edge that is coincident with an M2 boundary (the 5 & 0 nm alternative); do not inadvertently create a non-flush edge by over-extending M2 on a side that must remain flush.

### V1.AUX.1 — V1 inside M1 and M2

After any move_instance, the V1 geometry must remain within the intersection of M1 and M2. All accepted moves in this history satisfy this requirement. When a via position after translation would place V1 outside M1 or M2, delete the instance and place a VIA_VIA12 at a compliant origin rather than extending the via beyond either enclosing layer (trial:i02.ug.leaf_0004.02).

### V1.M2.AUX.2 — V1 width matches M2 width perpendicular to M2 length

Resizing an M2 polygon in the direction perpendicular to M2 length changes the M2 width and the V1 width in tandem. Apply symmetric resize (trial:i01.ug.leaf_0031.11) when the V1.M2.AUX.2 violation is the primary target. Resize_end adjusts M2 along its length direction and does not correct a perpendicular width mismatch.

### GEOMETRY.NONORTHOGONAL — All V1 edges must be axis-aligned

All resize_end, resize, move_instance, and add_via operations in this history produce orthogonal geometries. Do not apply diagonal move vectors or non-axis-aligned end extensions to V1 or its enclosing M2 (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row4.04, trial:i02.ug.leaf_0004.02, trial:i01.ug.leaf_0031.11).