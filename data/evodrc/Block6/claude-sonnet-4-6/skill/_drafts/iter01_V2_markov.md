## Final-pair measured facts (reference-design tail evidence)

Provenance: these facts come from the final-pair comparison of the reference
design's initial layout against its repaired final layout, plus the BEFORE and
AFTER DRC reports. Every coordinate and delta cited in this document is quoted
inline from that pair; the layout files themselves are not needed and are not
shipped with this skill.

- The final 33 via instance moves show three stacked-via patterns: coupled,
  anchor, and partial. Co-movement is NOT unconditionally safe; reproduce the
  final-pair pattern by checking each shared M2/M3 landing before moving VIA23.


## Case notes (reference-design tail evidence)

Stacked via movement is a PER-LEVEL decision, not a co-movement law. Verified
modes from the final diff: COUPLED (the (5652,5220) pair moved together, +64 x),
ANCHOR (VIA23 at (3204,1980) stayed while its VIA12 moved +136 x -- the VIA23
remains the M2-M3 anchor at the old position), PARTIAL (the (6228,2340) pair
shared +8 y but split in x, +36 vs 0). Anti-pattern AP-1: blindly moving every
co-located VIA23 with its VIA12 contradicts the clean final pair. Always run the
anchor check before co-moving.


## Cell-definition repair: mixed move+resize on V2 shapes

Cell-level repairs (target prefix `def:`) propagate to every instance of the
cell simultaneously, unlike instance-level moves. trial:i01.cu.def:VIA_VIA23_1_3_36_36.00
applied 5 ops across 3 V2 shapes in cell VIA_VIA23_1_3_36_36, touching M2, M3,
and V2, and yielded -42 DRC violations in unit:leaf_0019 and -36 in
unit:leaf_0020 (-78 total) with conn_preserved=true.

The three shapes received asymmetric treatment on axis=x:
- shape_index 0: move -144 dbu, then resize +264 dbu.
- shape_index 1: resize only, +288 dbu (no move).
- shape_index 2: move +144 dbu, then resize +264 dbu.

Move direction is opposite for shape 0 vs shape 2 (-144 vs +144), while resize
magnitudes are consistent (+264 for shapes 0 and 2, +288 for shape 1). This
asymmetric move-then-resize pattern satisfies V2 enclosure and spacing rules
simultaneously across the multi-shape cell without violating connectivity
(trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 conn_preserved=true).

Do not apply a uniform delta to all shapes in a multi-shape V2 cell definition.
The correct strategy is to compute per-shape move and resize deltas
independently, as trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 demonstrates; a
single shared delta would shift the relative positions between shapes and can
introduce new V2.S.1 or V2.M3.EN.2 violations within the same cell.