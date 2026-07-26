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


## Resize-via-shape measured results (iteration 4)

Shrinking cell VIA_VIA23_1_3_36_36 on M3 in the y-axis by -40 dbu produced zero
net DRC improvement (before=122, after=122 violations, delta_total=0) and was
rejected (trial:i04.cu.def:VIA_VIA23_1_3_36_36.00). Do not apply a y-axis M3
resize of -40 dbu to this cell; the enclosure budget in that axis is already at
or below the V2.M3.EN.2 floor and the operation achieves nothing while consuming
a repair slot.