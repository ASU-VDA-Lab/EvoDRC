**Repair strategy: expand V5 shapes along the y-axis before resizing enclosing metal layers**

The only accepted repair in this layer's history operated exclusively on V5 shapes using paired y-axis move and y-axis resize operations applied to all shapes in the target cell simultaneously (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02). Shapes on the negative-y side of the array received a move of −132 dbu followed by a resize of +512 dbu; shapes on the positive-y side received a move of +132 dbu and the same +512 dbu resize. This symmetric outward expansion reduced the total violation count by 80 across four measurement windows, preserved connectivity, and was committed (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02).

Attempting to fix the same locus by instead resizing the enclosing metal layers — specifically growing M6 along y by +128 dbu and shrinking M5 along x by −96 dbu — increased the total violation count by +234 and was rejected as net-positive (trial:i02.cu.def:VIA_VIA56_2_2_66_58.01). Do not substitute metal-layer resizes for V5-shape resizes when targeting enclosure violations in this cell type.

**Enclosure rules V5.M5.EN.1 and V5.M6.EN.2**

Both rules require 11 nm enclosure on at least two opposite sides. The successful repair pattern (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02) used equal outward moves (±132 dbu) paired with identical resize magnitudes (+512 dbu) on every V5 shape in the cell, covering all four shapes (indices 0–3) in a single eight-operation group labelled "v56-fix". Apply move and resize as a unit to each shape — splitting them or applying them to a subset of shapes in the cell is untested and the rejected trial (trial:i02.cu.def:VIA_VIA56_2_2_66_58.01) demonstrates that partial adjustments to surrounding metal produce worse outcomes.

**Rule V5.M6.AUX.2 interaction**

V5.M6.AUX.2 requires V5 width perpendicular to M6 length to exactly match M6 width. The rejected trial grew M6 along y by +128 dbu without a corresponding V5 adjustment, and this contributed to the +234 violation increase (trial:i02.cu.def:VIA_VIA56_2_2_66_58.01). When any M6 dimension is changed, V5 shapes that share that M6 boundary must be updated in the same operation set to maintain the width-match constraint; the measured records show the reverse is safer — adjust V5 and leave M6 unchanged (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02).

**Rule V5.AUX.1: containment in both M5 and M6**

The accepted repair touched M5, M6, and V5 simultaneously and preserved containment (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02). No repair that moves or resizes V5 without verifying the resulting shape still lies inside the intersection of M5 and M6 has been observed to succeed; the rejected trial's metal-layer changes altered the M5 boundary without compensating V5 or M6 changes and worsened violations (trial:i02.cu.def:VIA_VIA56_2_2_66_58.01).

**Spacing rules V5.S.1, V5.S.2, V5.S.3**

Minimum spacing is 33 nm under projection (V5.S.1, V5.S.2) and Euclidean (V5.S.3) metrics. The symmetric outward expansion in the accepted repair (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02) increased shape extent along y; verify that the expanded shapes do not violate the 33 nm projection or corner-to-corner spacing toward neighboring V5 instances before committing any y-axis resize. The accepted trial achieved a net −80 reduction across all windows including spacing-sensitive windows (unit:leaf_0103, unit:leaf_0104), confirming that +512 dbu resizes at this locus did not introduce new spacing violations (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02).

**Minimum width rule V5.W.1**

V5.W.1 requires 24 nm minimum width along the M6 length direction. The +512 dbu per-shape resize in the accepted repair increased — not decreased — shape extent along y, so no V5.W.1 violations were introduced by that operation (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02). Avoid any operation that reduces a V5 shape dimension below 24 nm; the only observed resize direction in accepted repairs is positive (expansion).

**Non-orthogonal geometry**

All move and resize operations in the measured history act along axis-aligned directions (x or y only). The GEOMETRY.NONORTHOGONAL rule fires on any edge not at 0°, 90°, 180°, or 270°. No non-orthogonal edges were introduced in either trial; use only axis-aligned delta_dbu values in move_via_shape and resize_via_shape operations.

**Operational summary derived from measured records**

- Apply move_via_shape and resize_via_shape to V5 shapes as symmetric pairs along the y-axis, covering every shape in the affected cell in one grouped operation (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02).
- Do not attempt to repair V5 enclosure violations by resizing M5 or M6 alone; doing so increases total violations (trial:i02.cu.def:VIA_VIA56_2_2_66_58.01).
- The "v56-fix" group tag was used for the accepted enclosure repair; use this group consistently to keep operations identifiable across iterations (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02).
- Connectivity was preserved in the accepted repair, confirming that outward V5 expansion within a single cell does not break nets when M5 and M6 are touched as part of the same operation set (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02).