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


## resize_via_shape: M3 y-axis shrink (iteration 1 evidence)

A `resize_via_shape` trial on cell VIA_VIA23_1_3_36_36 that contracted the M3
shape by 40 dbu (4 nm) along the y axis produced zero change in DRC violation
count across both sampled windows (before 88, after 88; before 35, after 35;
delta_total 0) and was rejected as not net-negative (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).
Connectivity was preserved throughout that trial. Do not apply a y-axis M3 shrink
of 40 dbu to VIA_VIA23_1_3_36_36 as a first-pass repair; the DRC violations
present in locus [1728,2068,13168,13052] are insensitive to that operation.