**Cu-pool via-cell repairs: move-then-resize on y-axis**

Both via cell definitions repaired this iteration used the same two-step per-shape sequence on V5: translate the shape along y by ±132 dbu, then grow it along y by +512 dbu (trial:i01.cu.def:VIA_VIA56_2_1_66_58.00, trial:i01.cu.def:VIA_VIA56_2_2_66_58.01). Shapes below center receive a −132 dbu translation; shapes above center receive a +132 dbu translation before the +512 dbu resize (trial:i01.cu.def:VIA_VIA56_2_1_66_58.00, trial:i01.cu.def:VIA_VIA56_2_2_66_58.01). Apply this symmetric split — move outward then grow — rather than a pure resize from the original centroid when repairing V5 shapes in VIA_VIA56_* cells (trial:i01.cu.def:VIA_VIA56_2_1_66_58.00, trial:i01.cu.def:VIA_VIA56_2_2_66_58.01).

**Violation reduction per cell**

VIA_VIA56_2_1_66_58 carried 2 shapes and the repair reduced the whole-design violation count by 2 (trial:i01.cu.def:VIA_VIA56_2_1_66_58.00). VIA_VIA56_2_2_66_58 carried 4 shapes and the repair reduced the count by 4 (trial:i01.cu.def:VIA_VIA56_2_2_66_58.01). Scale the expected delta by the number of V5 shapes in the cell when estimating repair benefit for VIA_VIA56_* variants (trial:i01.cu.def:VIA_VIA56_2_1_66_58.00, trial:i01.cu.def:VIA_VIA56_2_2_66_58.01).

**Connectivity preservation**

All three applied trials — unit-gate move of polygon p1402 and instances i0234/i0305 on y by +64 dbu, plus both cu-pool cell repairs — preserved connectivity (trial:i01.ug.whole_design.00, trial:i01.cu.def:VIA_VIA56_2_1_66_58.00, trial:i01.cu.def:VIA_VIA56_2_2_66_58.01). Accept cu-pool V5 shape edits only when conn_preserved is confirmed; both cell repairs here met that condition and were admitted (trial:i01.cu.def:VIA_VIA56_2_1_66_58.00, trial:i01.cu.def:VIA_VIA56_2_2_66_58.01).

**Multi-layer co-modification**

Every repair in this iteration touched M5, M6, and V5 together (trial:i01.ug.whole_design.00, trial:i01.cu.def:VIA_VIA56_2_1_66_58.00, trial:i01.cu.def:VIA_VIA56_2_2_66_58.01). Do not edit V5 shapes in isolation from their enclosing M5/M6 geometry; the cu-pool always co-modifies all three layers to keep enclosure rules V5.M5.EN.1 and V5.M6.EN.2 satisfied (trial:i01.cu.def:VIA_VIA56_2_1_66_58.00, trial:i01.cu.def:VIA_VIA56_2_2_66_58.01).

**Unit-gate gating**

The unit-gate trial moved polygon p1402 and two instances by +64 dbu on y and was accepted (decision: gated_in) with zero new in-crop or out-of-crop violations introduced (trial:i01.ug.whole_design.00). A small y-translation of active V5-touching geometry does not introduce new violations when the move is uniform across the net and connectivity is preserved (trial:i01.ug.whole_design.00).