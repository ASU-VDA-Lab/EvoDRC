**V5 Layer — Measured Knowledge (iteration 4)**

**Enclosure repair via Y-axis resize and repositioning of V5 shapes**

Both applied trials in this iteration target via cell definitions in the `VIA_VIA56_2_x_66_58` family (2-column, 66×58 dbu nominal footprint) and address enclosure violations on V5 (rules V5.M5.EN.1 and V5.M6.EN.2). The consistent repair pattern across all shapes in both trials is: move the V5 shape ±132 dbu in Y (outward from the column center) and resize the same shape +512 dbu in Y. M5 is co-resized +248 dbu in Y on the same axis to extend its enclosure margin. All operations are axis-aligned (Y only); no X-axis moves or X-axis resizes of V5 were recorded (trial:i04.cu.def:VIA_VIA56_2_1_66_58.00, trial:i04.cu.def:VIA_VIA56_2_2_66_58.01).

**Sign convention for the move: bottom shapes move −Y, top shapes move +Y**

In the 2×1 cell (2 V5 shapes), shape_index 0 moves −132 dbu and shape_index 1 moves +132 dbu in Y, spreading them away from the via column midpoint. In the 2×2 cell (4 V5 shapes), shapes 0 and 1 both move −132 dbu while shapes 2 and 3 both move +132 dbu, preserving the same outward-displacement logic per row (trial:i04.cu.def:VIA_VIA56_2_2_66_58.01). Apply this sign convention uniformly: the move direction is always away from the geometric center of the via column in Y.

**Resize magnitude is uniform per shape regardless of column height**

Every V5 shape in both trials receives the identical +512 dbu Y-axis resize regardless of whether the cell is a 2×1 or 2×2 configuration. The per-shape resize is not scaled by the number of vias in the column (trial:i04.cu.def:VIA_VIA56_2_1_66_58.00, trial:i04.cu.def:VIA_VIA56_2_2_66_58.01). Do not halve or otherwise scale the 512 dbu delta when applying to denser arrays.

**M5 co-resize is mandatory and uses a smaller delta than V5**

Both trials include a single M5 resize_via_shape operation of +248 dbu in Y (shape_index 0) applied before any V5 operations. V5 resizes by +512 dbu per shape; M5 resizes by only +248 dbu for the enclosing metal. Omitting the M5 co-resize would risk violating M5 width or enclosure rules even as V5 enclosure is corrected. Always pair the V5 Y-axis expansion with the corresponding M5 Y-axis expansion in the same operation sequence (trial:i04.cu.def:VIA_VIA56_2_1_66_58.00, trial:i04.cu.def:VIA_VIA56_2_2_66_58.01).

**M6 is listed as a touched layer but receives no explicit ops in either trial**

Both records show `touched_layers: ["M5","M6","V5"]` yet the ops arrays contain no move or resize entries for M6. M6 is implicated by rule V5.M6.AUX.2 (V5 must exactly match M6 width along the perpendicular direction) and V5.M6.EN.2, but the measured repair achieves compliance without modifying M6 geometry directly — the V5 Y-axis expansion alone satisfies V5.M6.EN.2 when M6 already provides sufficient perpendicular coverage. Do not add M6 ops speculatively; the recorded fix achieves full violation reduction without them (trial:i04.cu.def:VIA_VIA56_2_1_66_58.00, trial:i04.cu.def:VIA_VIA56_2_2_66_58.01).

**Net violation reduction scales with via count**

The 2×1 cell repair reduced violations by 2 (delta_total −2, window unit:leaf_0002 51→49). The 2×2 cell repair reduced violations by 4 (delta_total −4, window unit:leaf_0002 51→47). This 1:1 correspondence between V5 shape count and violation delta indicates each V5 shape in a non-compliant via column generates one countable DRC hit under the active rules, and each corrected shape eliminates one hit. Expect a 2-column N-row cell to yield a delta_total of −2N upon successful application of this repair (trial:i04.cu.def:VIA_VIA56_2_1_66_58.00, trial:i04.cu.def:VIA_VIA56_2_2_66_58.01).

**Connectivity is preserved by the Y-only expansion strategy**

Both trials report `conn_preserved: true`. Expanding V5 outward in Y while keeping M5 and M6 coverage intact does not sever net connectivity, confirming that the ±132/+512 dbu Y-move/resize combination stays within the available M5 and M6 overlap regions. The locus [1728, 2068, 13168, 13052] is shared across both trials, placing them in the same congestion window (unit:leaf_0002 in Block4, cu_pool channel), yet both repairs commit without routing conflicts (trial:i04.cu.def:VIA_VIA56_2_1_66_58.00, trial:i04.cu.def:VIA_VIA56_2_2_66_58.01).

**Op ordering within a repair sequence: M5 resize → V5 moves and resizes interleaved per shape**

Within each trial the M5 resize is the first op, followed by alternating move/resize pairs for each V5 shape index in ascending order. For shape_index k: move (delta_dbu = ∓132) then resize (delta_dbu = +512). This ordering is consistent across the 2×1 and 2×2 cases. Do not reorder to resize before move within a shape pair, as the recorded trials applied them move-first (trial:i04.cu.def:VIA_VIA56_2_1_66_58.00, trial:i04.cu.def:VIA_VIA56_2_2_66_58.01).