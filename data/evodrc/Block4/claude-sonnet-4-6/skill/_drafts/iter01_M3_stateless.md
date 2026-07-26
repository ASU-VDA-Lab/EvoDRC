## Via-Shape Shrinks on M3 in the Y-Axis Do Not Clear Violations and May Increase Them

Shrinking M3 metal shapes that belong to via cell definitions via `resize_via_shape` along the y-axis was tested in two cu_pool trials and rejected as `rejected_net_positive` in both cases.

- trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 applied a single y-axis delta of -40 dbu to the M3 shape in cell `VIA_VIA23_1_3_36_36`. The cu_pool delta_total was 0 across both affected windows (leaf_0025 and leaf_0026), meaning the operation neither introduced nor removed any in-crop violations. The operation was nonetheless rejected because it failed to produce a net improvement.

- trial:i01.cu.def:VIA_VIA34_1_2_58_52.01 applied a y-axis delta of -64 dbu to the M3 shape in `VIA_VIA34_1_2_58_52`, alongside concurrent -24 dbu shrinks on two V3 shapes in the same cell. This combination increased the total in-crop violation count by 34 (leaf_0025: +24, leaf_0026: +10) and was rejected. Touching M3 and V3 together in the same via-cell resize moved the design farther from clean.

Do not apply `resize_via_shape` on M3 in the y-axis for cells `VIA_VIA23_1_3_36_36` or `VIA_VIA34_1_2_58_52` in Block4 at iteration 1; the cu_pool evidence shows these moves are at best neutral and at worst substantially harmful.

## Bulk Y-Axis Resize of M3 Polygons Can Be Accepted by the Unit-Gate Channel

trial:i01.ug.leaf_0026.12 applied a y-axis delta of -64 dbu to five M3 polygons (p1406, p1407, p1408, p1409, p1410) as a coordinated unit-gate operation. The decision was `gated_in`. Key conditions that held:

- `conn_preserved` was true.
- No new out-of-crop violations were introduced (`new_out_of_crop`: 0).
- Two new in-crop violations appeared (`M1.A.1`: 1, `V1.M1.EN.1`: 1); the unit-gate channel accepted these because the connectivity and out-of-crop constraints were satisfied.

The assembled trial excluded the two cu_pool-rejected via-cell shrinks (listed in `assemble_drops`): the VIA_VIA23_1_3_36_36 M3 -40 dbu op and the VIA_VIA34_1_2_58_52 M3 -64 dbu op were both dropped before assembly. The accepted bulk resize therefore operated on standalone M3 polygons, not via-cell-owned shapes.

A y-axis shrink of -64 dbu on M3 polygons in unit leaf_0026 is viable under the unit-gate channel when connectivity is preserved and no out-of-crop violations are produced, even if it induces minor in-crop violations on adjacent layers (M1, V1).

## Cross-Layer Coupling: M3 Y-Shrink Affects M1 and V1 In-Crop Counts

The two new in-crop violations introduced by trial:i01.ug.leaf_0026.12 were on rules M1.A.1 and V1.M1.EN.1, not on any M3 rule. This indicates that reducing M3 metal extent in the y-direction can shrink connected M1 shapes or alter enclosure geometry for V1, causing area or enclosure violations on those layers. When evaluating whether a proposed M3 y-axis resize is safe, check downstream M1 area (M1.A.1) and V1-to-M1 enclosure (V1.M1.EN.1) in addition to M3-local rules.

## M3 Via-Enclosure Rules Constrain Minimum Metal Extent Around V2 and V3

Rules V2.M3.EN.2 and V2.M3.AUX.2 require that V2 is enclosed by M3 by at least 5 nm on two opposite sides and that V2 width matches M3 width along the perpendicular direction. Rule V3.M3.EN.1 requires V3 to be enclosed by M3 by at least 5 nm on at least two opposite sides. The cu_pool rejections in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 and trial:i01.cu.def:VIA_VIA34_1_2_58_52.01 confirm that naive y-axis shrinks of M3 via shapes do not satisfy these enclosure constraints in a way that reduces total violations; the enclosure geometry for V2 or V3 is disrupted and violations are traded rather than resolved.

## Spacing and Width Margins: No Direct Measurements Yet

No trials in the current history directly tested corrections for M3.W.1 (18 nm minimum width), M3.S.1 (18 nm side-to-side spacing), M3.S.2 (25 nm tip-to-side), M3.S.3 (27 nm wide-tip-to-wide-tip), M3.S.4 (31 nm narrow-tip-to-narrow-tip), M3.S.5 (31 nm wide-tip-to-narrow-tip), M3.S.6 (20 nm corner-to-corner euclidean), or M3.A.1 (504 nm² minimum area). No prescriptive guidance on these rules can be issued from the measured history.