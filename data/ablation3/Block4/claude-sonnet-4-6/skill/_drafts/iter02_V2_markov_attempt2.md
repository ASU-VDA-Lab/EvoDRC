## Final-pair measured facts (reference-design tail evidence)

Provenance: these facts come from the final-pair comparison of the reference design's initial layout against its repaired final layout, plus the BEFORE and AFTER DRC reports. Every coordinate and delta cited in this document is quoted inline from that pair; the layout files themselves are not needed and are not shipped with this skill.

The final 33 via instance moves show three stacked-via patterns: coupled, anchor, and partial. Co-movement is NOT unconditionally safe; check each shared M2/M3 landing before moving VIA23 (seed).


## Case notes (reference-design tail evidence)

Stacked via movement is a PER-LEVEL decision, not a co-movement law. Verified modes from the final diff: COUPLED (the (5652,5220) pair moved together, +64 x), ANCHOR (VIA23 at (3204,1980) stayed while its VIA12 moved +136 x -- the VIA23 remains the M2-M3 anchor at the old position), PARTIAL (the (6228,2340) pair shared +8 y but split in x, +36 vs 0). Anti-pattern AP-1: never move every co-located VIA23 with its VIA12 without an anchor check -- the clean final pair contradicts blind co-movement (reference-design-verified). Always run the anchor check before co-moving (reference-design-verified).


## Resize operations (iteration 2 measured evidence)

Resizing a V2 shape along x by +144 dbu (cell VIA_VIA23_1_3_36_36, shape_index 1) reduced DRC violations from 140 to 89 (delta -51) while preserving connectivity (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00). Apply resize_via_shape on V2 when projection-space violations exist on M2/M3-touching instances; this operation touches M2, M3, and V2 simultaneously and must be applied as a unit (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00).