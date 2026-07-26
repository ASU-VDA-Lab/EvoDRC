## Repair Outcomes: All Recorded Trials Accepted

All twelve unit_gate trials and one cu_pool trial in the recorded history were accepted. Unit_gate decisions for trial:i01.ug.Block3_union_row1.00, trial:i01.ug.Block3_union_row2.01, trial:i01.ug.Block3_union_row5.02, trial:i01.ug.Block3_union_row8.03, trial:i01.ug.leaf_0006.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0008.06, trial:i01.ug.leaf_0009.07, trial:i01.ug.leaf_0012.08, trial:i01.ug.leaf_0013.09, trial:i02.ug.leaf_0001.00, and trial:i02.ug.leaf_0002.01 were all "gated_in" with conn_preserved=true, n_new_in_crop=0, n_new_out_of_crop=0. The cu_pool trial trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 was "applied" with delta_total=-27. No trial was rejected.

## Unit_gate Acceptance Conditions

The gated_in outcome in the unit_gate channel requires conn_preserved=true, n_new_in_crop=0, and n_new_out_of_crop=0 simultaneously. All twelve unit_gate trials satisfy this triple condition (trial:i01.ug.Block3_union_row1.00 through trial:i02.ug.leaf_0002.01). The zero new violations criterion held even for trials with large move and resize magnitudes such as the +192 dbu resizes in trial:i01.ug.Block3_union_row1.00 and the +164 dbu resize in trial:i01.ug.Block3_union_row8.03.

## Operation Types on M2

Two operation types appear in all unit_gate trials touching M2: move_instance and resize_end. Move-only trials (no resize) were accepted in trial:i01.ug.Block3_union_row2.01 (two +36 dbu X moves), trial:i01.ug.leaf_0006.04 (two +36 dbu X moves), trial:i01.ug.leaf_0009.07 (one +36 dbu X move), and trial:i01.ug.leaf_0013.09 (one -36 dbu X move). Trials combining move_instance with resize_end on M2 polygons were accepted in trial:i01.ug.Block3_union_row1.00, trial:i01.ug.Block3_union_row5.02, trial:i01.ug.Block3_union_row8.03, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0008.06, trial:i01.ug.leaf_0012.08, and trial:i02.ug.leaf_0002.01.

Negative-direction moves on M2-touching instances are accepted: trial:i01.ug.leaf_0013.09 moved instance i0023 by -36 dbu and was gated_in, and trial:i02.ug.leaf_0001.00 moved instance i0233 by -36 dbu and was gated_in.

## Y-axis Resize

A Y-axis high-end resize on an M2 polygon was accepted in trial:i01.ug.leaf_0008.06: resize_end on polygon p1159 with axis=y, delta_dbu=20, end=high. This appeared alongside a +4 dbu X move of instance i0239, a +136 dbu X move of instance i0047, and a +92 dbu X resize of polygon p1261. The trial was gated_in.

## Move_instance Magnitudes Observed (All Accepted)

The following X-axis move_instance delta magnitudes were accepted in unit_gate trials touching M2:

- +4 dbu: instance i0239 in trial:i01.ug.leaf_0008.06.
- +36 dbu: instances i0221 and i0203 in trial:i01.ug.Block3_union_row2.01; instances i0124, i0011, and i0033 in trial:i01.ug.Block3_union_row5.02; instances i0179 and i0106 in trial:i01.ug.leaf_0006.04; instances i0263 and i0210 in trial:i01.ug.leaf_0007.05; instance i0041 in trial:i01.ug.leaf_0009.07.
- -36 dbu: instance i0023 in trial:i01.ug.leaf_0013.09; instance i0233 in trial:i02.ug.leaf_0001.00.
- +72 dbu: instances i0016, i0019, and i0021 in trial:i01.ug.Block3_union_row8.03; instance i0103 in trial:i01.ug.leaf_0012.08.
- +104 dbu: instance i0239 in trial:i02.ug.leaf_0002.01.
- +108 dbu: instance i0017 in trial:i01.ug.Block3_union_row8.03.
- +136 dbu: instances i0233, i0246, and i0205 in trial:i01.ug.Block3_union_row1.00; instance i0047 in trial:i01.ug.leaf_0008.06.

## Resize_end Magnitudes Observed on M2 Polygons (All Accepted)

The following resize_end high-end magnitudes on M2 polygon endpoints were accepted in unit_gate trials:

- X-axis +20 dbu Y: polygon p1159 in trial:i01.ug.leaf_0008.06 (Y-axis).
- X-axis +36 dbu: polygon p1265 in trial:i01.ug.Block3_union_row5.02.
- X-axis +56 dbu: polygons p1223 and p1189 in trial:i01.ug.leaf_0007.05.
- X-axis +92 dbu: polygon p1261 in trial:i01.ug.leaf_0008.06; polygon p1257 in trial:i01.ug.Block3_union_row8.03.
- X-axis +108 dbu: polygon p1256 in trial:i01.ug.leaf_0012.08.
- X-axis +128 dbu: polygons p1266 and p1269 in trial:i01.ug.Block3_union_row8.03; polygon p1226 in trial:i02.ug.leaf_0002.01.
- X-axis +164 dbu: polygon p1267 in trial:i01.ug.Block3_union_row8.03.
- X-axis +192 dbu: polygons p1254, p1270, and p1255 in trial:i01.ug.Block3_union_row1.00.

## Paired Move and Resize Deltas

When move_instance and resize_end appear together in the same trial, the pairing of instance move delta to polygon resize delta varies:

- trial:i01.ug.Block3_union_row1.00: three instance moves of +136 dbu each paired with three polygon resizes of +192 dbu each (p1254, p1270, p1255). Resize delta exceeds move delta by 56 dbu in each pair.
- trial:i01.ug.Block3_union_row5.02: instance i0124 moved +36 dbu alongside polygon p1265 resized +36 dbu. Deltas equal.
- trial:i01.ug.Block3_union_row8.03: instance i0017 +108 dbu with p1267 +164 dbu (resize exceeds move by 56 dbu); instance i0016 +72 dbu with p1266 +128 dbu (resize exceeds by 56); instance i0019 +72 dbu with p1269 +128 dbu (resize exceeds by 56); instance i0021 +72 dbu with p1257 +92 dbu (resize exceeds by 20).
- trial:i01.ug.leaf_0007.05: instance i0263 +36 dbu with p1223 +56 dbu; instance i0210 +36 dbu with p1189 +56 dbu. Resize exceeds move by 20 dbu in each pair.
- trial:i01.ug.leaf_0008.06: instance i0239 +4 dbu X alongside p1159 +20 dbu Y (different axes); instance i0047 +136 dbu X with p1261 +92 dbu X. In this last pair the move delta exceeds the resize delta by 44 dbu.
- trial:i01.ug.leaf_0012.08: instance i0103 +72 dbu with p1256 +108 dbu. Resize exceeds move by 36 dbu.
- trial:i02.ug.leaf_0002.01: instance i0239 +104 dbu with p1226 +128 dbu. Resize exceeds move by 24 dbu.

## Layers Co-touched with M2

Every unit_gate trial that touches M2 also touches M1 and V1 in touched_layers (trial:i01.ug.Block3_union_row1.00 through trial:i02.ug.leaf_0002.01). Trial:i01.ug.leaf_0008.06 additionally touches M3 alongside M1, M2, and V1. The cu_pool trial trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 touches M2, M3, and V2 without touching M1 or V1.

## Via Cell Modification (cu_pool Channel)

The cu_pool channel modifies via cell shapes directly. Trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 applied five operations to V2 shapes in cell VIA_VIA23_1_3_36_36: move shape_index 0 by -144 dbu in X; resize shape_index 0 by +288 dbu in X; resize shape_index 1 by +288 dbu in X; move shape_index 2 by +144 dbu in X; resize shape_index 2 by +288 dbu in X. The trial touched M2, M3, and V2, and was applied with delta_total=-27, reducing violations by 15 in unit leaf_0018 and by 12 in unit leaf_0019. The V2.M2.EN.1 rule requires M2 to enclose V2 by at least 5 nm on two opposite sides; the V2.M2.EN.1 and V2.M2.EN.1-adjacent enclosure context is the only rule set directly implicating the M2/V2 interface in the touched_layers list for this trial.

## Multi-unit Scope

The cu_pool channel trial trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 operated on a shared via cell definition (target=def:VIA_VIA23_1_3_36_36) and reduced violations across two distinct units simultaneously (leaf_0018 and leaf_0019). The unit_gate trials each targeted a single unit_id. Locus extents in unit_gate trials ranged from sub-micron to multi-row spans: the single-instance trial:i01.ug.leaf_0009.07 covered a 684x164 dbu locus, while trial:i01.ug.leaf_0006.04 spanned a 632x6264 dbu locus across two units.