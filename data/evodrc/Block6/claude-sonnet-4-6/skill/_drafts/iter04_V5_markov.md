## Repair Strategy: Move and Resize on V5 Shapes

The measured repair in trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 demonstrates that symmetric bidirectional x-axis moves paired with uniform x-axis resize across all via shapes is effective: shapes at indices 0 and 2 received `move_via_shape` x=−116 dbu and shapes at indices 1 and 3 received `move_via_shape` x=+116 dbu; all four shapes received `resize_via_shape` x=+320 dbu, reducing violations by 16 (decision=applied).

Trial:i04.cu.def:VIA_VIA56_2_2_66_58.00 establishes that y-axis move-plus-resize on V5 shapes is also an effective and accepted repair pattern. Shapes at indices 0 and 1 received `move_via_shape` y=−132 dbu and shapes at indices 2 and 3 received `move_via_shape` y=+132 dbu (antisymmetric); all four shapes received `resize_via_shape` y=+512 dbu. This repair was decision=applied with delta_total=−14 (trial:i04.cu.def:VIA_VIA56_2_2_66_58.00). Use antisymmetric y-axis moves (opposite-sign pairs) together with positive y-axis resize when projection-based spacing or enclosure violations are oriented along the y axis.

A move-only repair (no resize) with asymmetric x-displacements (p1683: +32 dbu, p1682: −16 dbu) across 18 operations resulted in decision=gated_in with 26 new in-crop violations introduced, despite conn_preserved=true (trial:i03.ug.leaf_0003.02). Prefer move-plus-resize repairs over move-only repairs when V5.W.1 violations are present; omitting resize when via width shortfalls are active risks displacing edges into new spacing conflicts without correcting the width deficiency.

Do not apply move or resize operations to V5 in isolation when enclosure rules V5.M5.EN.1 or V5.M6.EN.2 are involved: all applied trials list touched_layers that include M5 and M6 alongside V5 (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02, trial:i04.cu.def:VIA_VIA56_2_2_66_58.00).

## Connectivity Preservation

All three measured repairs completed with conn_preserved=true (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02, trial:i03.ug.leaf_0003.02, trial:i04.cu.def:VIA_VIA56_2_2_66_58.00). Connectivity is preserved by symmetric equal-and-opposite moves, asymmetric moves, and antisymmetric y-axis moves alike; move symmetry and move axis do not determine connectivity outcome. The quality of the outcome (applied vs. gated_in, net violation delta) depends on whether resize operations accompany the moves, not on move symmetry.

## Decision Outcomes: applied vs. gated_in

A decision=applied outcome indicates the repair was unconditionally committed and produced a net reduction in violations (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02: −16; trial:i04.cu.def:VIA_VIA56_2_2_66_58.00: −14). A decision=gated_in outcome indicates the repair passed only the connectivity gate (reason=conn_preserved) while introducing new violations (trial:i03.ug.leaf_0003.02: n_new_in_crop=26). Do not treat gated_in as equivalent to applied; gated_in repairs require downstream resolution of newly introduced violations. The distinguishing factor across measured trials is that applied decisions pair V5 moves with resize operations, while the gated_in repair omitted resize entirely.

## Multi-Window Impact

A single via cell repair can reduce violations across more than one layout window. In trial:i01.cu.def:VIA_VIA56_2_2_66_58.02, the repair to cell VIA_VIA56_2_2_66_58 produced an 8-violation reduction in both unit:leaf_0019 and unit:leaf_0020 (total −16). In trial:i04.cu.def:VIA_VIA56_2_2_66_58.00, a repair to the same cell produced a 14-violation reduction in unit:leaf_0002 only, with zero impact on unit:leaf_0003. Multi-window propagation is not guaranteed for all instances of a cell; the benefit propagates only to windows whose resident instances lie within the repair locus (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02, trial:i04.cu.def:VIA_VIA56_2_2_66_58.00).

## Channel Differences: cu_pool vs. unit_gate

The cu_pool channel repair in trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 touched only ["M5","M6","V5"]. The cu_pool repair in trial:i04.cu.def:VIA_VIA56_2_2_66_58.00 touched ["M4","M5","M6","V4","V5"], demonstrating that cu_pool repairs are not restricted to M5/M6/V5 — when the repair locus includes V4 connectivity (y-axis instance moves coupled with via cell y-moves), M4 and V4 enter the coordination set. The unit_gate channel repair in trial:i03.ug.leaf_0003.02 also touched ["M4","M5","M6","V4","V5"]. Include M4 and V4 in the coordination set whenever the repair displaces instances in the y direction or involves V4-connected geometry, regardless of channel.

## Enclosure Rule Geometry (V5.M5.EN.1, V5.M6.EN.2)

Both V5.M5.EN.1 and V5.M6.EN.2 require 11 nm enclosure on at least two opposite sides. V5.M6.AUX.2 additionally requires that V5 width exactly matches M6 width perpendicular to M6 length. When resizing V5 shapes, the M6 geometry must be updated to maintain the exact-width constraint; all applied repairs touch M6 alongside V5 (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02, trial:i04.cu.def:VIA_VIA56_2_2_66_58.00). This constraint applies to both x-axis and y-axis resize operations: trial:i04 resizes V5 in y (+512 dbu) and touches M6, consistent with V5.M6.AUX.2 applying to the perpendicular-to-M6-length direction.

## Spacing Rules (V5.S.1, V5.S.2, V5.S.3)

All spacing rules share the 33 nm threshold. V5.S.1 and V5.S.2 use projection-based measurement; V5.S.3 uses Euclidean corner-to-corner measurement. Opposite-sign x-moves applied to paired via shapes increase projected x-separation (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02). Antisymmetric y-moves (shapes 0,1 at −132 dbu; shapes 2,3 at +132 dbu) increase projected y-separation between the two subgroups (trial:i04.cu.def:VIA_VIA56_2_2_66_58.00). Apply same-sign axis moves only when projection-based violations are absent on that axis; use opposite-sign (x) or antisymmetric (y) paired moves to open projected gaps. After any move, verify that corner-to-corner distances clear 33 nm to avoid introducing V5.S.3 violations.

## Width Rule (V5.W.1)

V5.W.1 requires minimum via width of 24 nm along the M6 length direction. Positive resize values increase via extent and correct width shortfalls. The x-axis +320 dbu resize in trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 and the y-axis +512 dbu resize in trial:i04.cu.def:VIA_VIA56_2_2_66_58.00 both apply positive resize deltas and both achieve decision=applied. The move-only repair in trial:i03.ug.leaf_0003.02 omitted resize and introduced 26 new violations. Always apply positive resize when correcting V5.W.1 violations; never reduce V5 extent below 24 nm when performing moves that shift edges inward.

## Orthogonality

All V5 edges must be axis-aligned (0° or 90°). All move and resize operations in the measured trials operate exclusively on a single Cartesian axis per operation — x in trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 and trial:i03.ug.leaf_0003.02, y in trial:i04.cu.def:VIA_VIA56_2_2_66_58.00 (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02, trial:i03.ug.leaf_0003.02, trial:i04.cu.def:VIA_VIA56_2_2_66_58.00). Never apply diagonal or compound-axis transforms to V5 shapes; restrict all V5 move and resize operations to a single axis per operation to avoid triggering the GEOMETRY.NONORTHOGONAL check.