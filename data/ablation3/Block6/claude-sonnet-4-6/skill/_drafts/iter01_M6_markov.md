**Via enclosure and width repair on M6: resize V5 in Y**

Resizing V5 shapes in the Y axis within via cell definitions is an effective repair strategy for M6-touching enclosure and perpendicular-width violations. In trial:i01.cu.def:VIA_VIA56_2_2_66_58.01, applying axis:y delta_dbu:+248 to all four V5 shapes in cell VIA_VIA56_2_2_66_58 eliminated 32 violations (delta_total: -32) while preserving connectivity (conn_preserved: true). The touched layers were M5, M6, and V5; no M6 geometry itself was modified — the correction acted exclusively through V5 resizing.

**Cell-level repair scope**

Via cell definitions (def: targets) are the correct repair locus for V5.M6.EN.2 and V5.M6.AUX.2 class violations. In trial:i01.cu.def:VIA_VIA56_2_2_66_58.01, a single cell edit (n_ops:4, all targeting the same cell VIA_VIA56_2_2_66_58) resolved violations across the whole design (window unit:whole_design, before:247, after:215), confirming that cell-level fixes propagate to all instances and are more efficient than per-instance polygon edits when the root cause is in a shared via cell.

**Y-axis resize delta magnitude**

A Y-axis delta of +248 dbu was sufficient to clear 32 violations in trial:i01.cu.def:VIA_VIA56_2_2_66_58.01 without introducing new violations. No smaller delta for this cell has been measured; 248 dbu is the only confirmed effective value for this cell and iteration.

**Connectivity safety**

The Y-axis V5 resize at +248 dbu preserved all connections in trial:i01.cu.def:VIA_VIA56_2_2_66_58.01 (conn_preserved: true). Resizing V5 shapes in Y within a via cell does not break M5–M6 connectivity at this delta magnitude for this cell geometry.