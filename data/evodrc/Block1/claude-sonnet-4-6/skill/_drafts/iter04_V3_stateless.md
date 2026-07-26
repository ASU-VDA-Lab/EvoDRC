**Repair operations observed for V3**

All four measured trials that touch V3 (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03, trial:i04.ug.leaf_0002.01, trial:i04.ug.leaf_0003.02) achieve DRC improvement exclusively through `move_instance` and `move` (polygon) operations. No resize, reshape, or delete operations appear for V3 in any record. Every trial was accepted with `decision: gated_in` and `conn_preserved: true`, confirming that V3 connectivity to M3 and M4 is preserved across all repair moves.

**X-axis quantization**

The dominant X-axis correction magnitudes are +32 dbu and -16 dbu, applied as paired groups across many instances in a single trial. trial:i02.ug.leaf_0003.02 moves twelve instances by +32 dbu X and twelve by -16 dbu X in the same commit. trial:i04.ug.leaf_0003.02 repeats the same magnitude pairs (+32 dbu and -16 dbu) across a partially overlapping instance set. The asymmetry between the two directions (+32 vs. -16) indicates two distinct V3/M4-track populations that require different X displacements to achieve legal enclosure or spacing. Do not assume symmetric ±N corrections; the two correction values target geometrically different situations and must be applied to the correct instance subset.

**Y-axis quantization**

trial:i04.ug.leaf_0002.01 shows three Y-axis correction magnitudes: -48 dbu (instances i0267, i0265, i0392, i0393, i0175, i0182, i0043, i0038), -96 dbu (i0341, i0337, i0416, i0401), and +48 dbu (i0189, i0193, i0127, i0130). In trial:i02.ug.leaf_0003.02, Y-components of -64, -96, and -112 dbu appear in compound moves. The 48 dbu / 96 dbu step pattern in the Y direction (trial:i04.ug.leaf_0002.01) is consistent with a grid pitch; moves that deviate from this quantization do not appear in any gated-in record.

**Compound X+Y moves**

trial:i02.ug.leaf_0003.02 applies simultaneous X and Y displacements to six instances: i0356 by [+32,-64], i0176 by [+32,-112], i0493 by [-16,-64], i0042 by [-16,-112], i0345 by [+32,-96], and i0505 by [-16,-96]. These compound moves indicate that certain V3 instances require repositioning in both axes within a single operation. Splitting such moves into separate X-only and Y-only steps is not attested in the measured history and the compound form is the form that was accepted.

**Polygon-level moves alongside instance moves**

trial:i02.ug.leaf_0003.02 also moves polygons directly: p1145 by +32 dbu X, p1144 by -16 dbu X, p1143 by +32 dbu X, p1142 by -16 dbu X, and p1563 by -64 dbu Y, p1562 by -112 dbu Y, p1561 by -96 dbu Y. These polygon moves occur in the same commit as the instance moves and the trial touches M2, M3, M4, M5, M6, V2, V3, V4, V5. The polygon moves adjust the local M-layer boundary geometry that surrounds V3 (governing V3.M3.EN.1 and V3.M4.EN.2 enclosure and V3.AUX.1 containment), while the instance moves shift the V3-containing cells. Both types of operation are needed within the same repair commit when the enclosing metal boundary falls short.

**Multi-iteration convergence**

V3 violations are not fully resolved in a single iteration. trial:i02.ug.leaf_0003.02 and trial:i02.ug.leaf_0004.03 both run at iter=2 and touch V3, yet trial:i04.ug.leaf_0002.01 (iter=4, 20 new violations cleared) and trial:i04.ug.leaf_0003.02 (iter=4, 8 new violations cleared) are required to finish the repair. The iter=2 trials clear the larger violation counts on other layers (M1, V1, V2, M4, M5, M6) while moving V3-containing geometry as a side effect; the iter=4 trials then address the residual V3 spacing and enclosure conditions left by the iter=2 displacements. Expect at least two iterations when V3 violations co-exist with M4/M5/M3 violations in the same locus.

**Cross-leaf conflict resolution**

trial:i02.ug.leaf_0003.02 and trial:i02.ug.leaf_0004.03 propose overlapping moves for the same V3-containing instances (e.g., i0352, i0312, i0317, i0229, i0139, i0170, i0509, i0398, i0421, i0105, i0025, i0045, i0363, i0331, i0344, i0207, i0141, i0171, i0499, i0412, i0417, i0102, i0026, i0037). The assembler resolves these as `external_conflict_dropped` for leaf_0004's ops and as `external_duplicate` when the two leaves proposed identical deltas. The first leaf (leaf_0003) retains its moves; leaf_0004's conflicting moves are dropped entirely. When two leaf regions share V3-containing instances at a crop boundary, only the first-committed leaf's displacement is applied. The second leaf must not assume its move for those shared instances will execute.

**Locus overlap and crop boundary sharing**

trial:i02.ug.leaf_0003.02 locus is [1728,2068,14256,13680] and trial:i02.ug.leaf_0004.03 locus is [1728,3148,14256,14132]. These loci overlap in X and share a Y band, which is why the same instances appear in both leaves' op lists. trial:i04.ug.leaf_0002.01 locus is [1728,2068,14256,13680] (identical to the iter=2 leaf_0003 locus), and trial:i04.ug.leaf_0003.02 locus is [1728,3072,14256,14132]. The iter=4 loci thus correspond closely to the iter=2 loci, operating on the same spatial regions to clean up residual violations.

**Connectivity-safe move strategy**

All four trials confirm conn_preserved=true. The move_instance operations applied to V3-containing cells keep V3 inside M3 and M4 (V3.AUX.1) because the enclosing metal layers are co-moved with the instances or their boundaries are adjusted by the accompanying polygon moves. Do not apply move_instance to a V3-containing cell without verifying that the M3 and M4 geometry either moves with it or is separately adjusted to maintain ≥5 nm M3 enclosure (V3.M3.EN.1) and ≥11 nm M4 enclosure (V3.M4.EN.2) on the required opposite-side pairs.

**No out-of-crop debt**

All four trials report `new_out_of_crop_bboxes: []` and `new_out_of_crop_by_rule: {}`. No V3 repair move in the measured history pushed violations outside the crop boundary. Move magnitudes of ±16 to ±112 dbu remain within the crop locus in every case; larger displacements do not appear in any accepted trial.