## via23-m3 Group: Y-Axis Shrink Repairs Enclosure Violations on {M2, M3, V2}

The via23-m3 group has produced two successful M3 repairs across two iterations, both targeting cell `VIA_VIA23_1_3_36_36` with identical operation structure but at different loci.

Iteration 1: five y-axis shrinks on the M3 via shape (shape_index 0, -40 dbu) and M3 polygons p962–p965 (-64 dbu each); violation count for unit:leaf_0012 dropped from 27 to 19 (delta -8); unit:leaf_0013 unaffected (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

Iteration 2: same operation structure applied to a different locus — via shape (shape_index 0, -40 dbu) and polygons p958–p961 (-64 dbu each); violation count for unit:leaf_0003 dropped from 20 to 12 (delta -8); unit:leaf_0002 unaffected at 7 (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00).

Both trials: decision `applied`, connectivity preserved, touched layers M2, M3, V2 exclusively.

The repeated delta -8 outcome across two independent loci confirms that the -40 dbu / -64 dbu repair pattern is reproducible and not specific to a single instance. When violations are concentrated on the {M2, M3, V2} layer combination in the via23-m3 group, apply y-axis shrinks using -40 dbu on the M3 via cell shape and -64 dbu on enclosing M3 polygons as the primary starting point (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, trial:i02.cu.def:VIA_VIA23_1_3_36_36.00).

The touched layers for both repairs are M2, M3, and V2 exclusively. The rules coupling these layers are V2.M3.EN.2 (M3 must enclose V2 on two opposite sides by at least 5 nm, projection) and V2.M3.AUX.2 (V2 must be exactly the same width as the enclosing M3 in the direction perpendicular to M3 length). Both rules were repaired without introducing new violations by the shrink approach confirmed here.

Do not apply a uniform delta across via cell shapes and surrounding M3 polygons; the cell shape requires -40 dbu while enclosing polygons require -64 dbu (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, trial:i02.cu.def:VIA_VIA23_1_3_36_36.00).

## Unit-Gate Instance Moves That Touch M3

A unit_gate move of four instances within unit leaf_0012 — i0097 and i0092 shifted [0, -48] dbu, i0064 and i0072 shifted [0, +96] dbu — was accepted (`decision: gated_in`) with connectivity preserved and no new M3-layer violations introduced (trial:i01.ug.leaf_0012.07). The touched layers were M3, M4, M5, V3, and V4. The only new in-crop violations produced were 2 V1.M1.EN.1 violations on a separate layer stack; the M3 geometry was not adversely perturbed by this placement adjustment (trial:i01.ug.leaf_0012.07).

The cu_pool M3 shrinks (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00) were assembled into the unit_gate trial as `assemble_drops` with `reason: cu_pool:applied`, confirming that previously accepted cu_pool ops on M3 are eligible for inclusion in unit_gate decisions without re-triggering violations (trial:i01.ug.leaf_0012.07).

## M3 Width and Spacing Rules: No Violations Triggered by Recorded Operations

None of the recorded operations across either iteration triggered M3.W.1 (18 nm minimum width), M3.S.1 (18 nm side-to-side spacing for edges > 36 nm), M3.S.2 (25 nm tip-to-side spacing), M3.S.3 (27 nm wide-tip-to-wide-tip spacing), M3.S.4 (31 nm narrow-tip-to-narrow-tip spacing), M3.S.5 (31 nm wide-tip-to-narrow-tip spacing), M3.S.6 (20 nm corner-to-corner Euclidean spacing), or M3.A.1 (504 nm² minimum area). Y-axis shrinks of -40 dbu and -64 dbu on M3 shapes in cell `VIA_VIA23_1_3_36_36` were net-beneficial without introducing any of these violations across both recorded loci (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, trial:i02.cu.def:VIA_VIA23_1_3_36_36.00). This establishes that these shrink magnitudes are within the safe operating range for shapes of this type at the loci tested; no general lower bound on safe shrink magnitude can be asserted from the current records alone.

## V3.M3.EN.1: No Measured Activity

No operations targeting V3.M3.EN.1 (minimum 5 nm enclosure of V3 by M3 on at least two opposite sides) appear in the recorded history. The unit_gate trial touched V3 and M3 simultaneously (trial:i01.ug.leaf_0012.07), but introduced no new V3.M3.EN.1 violations, confirming that the instance moves in that trial did not degrade V3-M3 enclosure margins.