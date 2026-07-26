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


## Iteration 1 measured facts

**Y-axis shrink of V2 cell shape plus coordinated M3 resize clears spacing violations.**
In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, target VIA_VIA23_1_3_36_36 at locus
[1728,2068,10368,9812] was repaired by shrinking the V2 cell shape by -40 dbu
on the y-axis (op: resize_via_shape) and shrinking four M3 polygons (p962–p965)
by -64 dbu on the y-axis. This five-op sequence reduced violations in
unit:leaf_0012 from 27 to 19 (delta -8) while unit:leaf_0013 held flat at 28,
yielding a net delta_total of -8 with conn_preserved=true. Do not apply the V2
shape resize without the coordinated M3 resize; the full five-op group is what
produced the clean result (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

**M3 and V2 resize magnitudes differ in the y-axis shrink pattern.**
The V2 cell shape shrank -40 dbu while the four M3 polygons each shrank -64 dbu
in the same repair (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). Do not assume a
1:1 dbu ratio between V2 and M3 delta magnitudes when applying this pattern.

**The cu_pool channel produces applied decisions that preserve connectivity.**
The repair at trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 was routed through the
cu_pool channel, decision=applied, conn_preserved=true. Repairs delivered through
cu_pool with applied status are safe to commit without a separate connectivity
re-check, provided conn_preserved=true is confirmed in the record.