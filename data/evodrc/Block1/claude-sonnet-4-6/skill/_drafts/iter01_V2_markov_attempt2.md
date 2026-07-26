## Final-pair measured facts (reference-design tail evidence)

Provenance: these facts come from the final-pair comparison of the reference
design's initial layout against its repaired final layout, plus the BEFORE and
AFTER DRC reports. Every coordinate and delta cited in this document is quoted
inline from that pair; the layout files themselves are not needed and are not
shipped with this skill.

The final 33 via instance moves show three stacked-via patterns: coupled,
anchor, and partial. Co-movement is not unconditionally safe; reproduce the
final-pair pattern by checking each shared M2/M3 landing before moving VIA23.
(seed, reference-design-verified)


## Case notes (reference-design tail evidence)

Stacked via movement is a PER-LEVEL decision, not a co-movement law. Verified
modes from the final diff: COUPLED (the (5652,5220) pair moved together, +64 x),
ANCHOR (VIA23 at (3204,1980) stayed while its VIA12 moved +136 x -- the VIA23
remains the M2-M3 anchor at the old position), PARTIAL (the (6228,2340) pair
shared +8 y but split in x, +36 vs 0). Blindly moving every co-located VIA23
with its VIA12 contradicts the clean final pair (seed, reference-design-verified);
the anchor check must be performed before co-moving any stacked via. (seed, reference-design-verified)


## Iteration 1 measured facts

**VIA_VIA23_1_3_36_36 M3 y-shrink produces no DRC improvement.**
A standalone resize of cell VIA_VIA23_1_3_36_36 by -40 dbu on the M3 shape
(axis y) achieved a delta_total of 0 across all measured windows (trial i01.cu.def:VIA_VIA23_1_3_36_36.00).
Do not apply this M3 y-shrink in isolation; it consumes an operation slot without
reducing violation count (trial i01.cu.def:VIA_VIA23_1_3_36_36.00).

**Multi-op sequences mixing instance moves and polygon end-resizes on V2-adjacent
layers break connectivity.**
A 10-op sequence on layers M1, M2, M3, M4, V1, V2 -- combining instance moves
(+72 dbu x for five instances, +136 dbu x for one) with three polygon end-resizes
and one via shape resize -- introduced 89 new violations inside the crop and broke
net connectivity (trial i01.ug.leaf_0034.12, decision gated_out, conn_preserved=false).
Avoid combining V2-touching instance moves with polygon end-resizes in the same
operation sequence without verifying connectivity preservation at each step
(trial i01.ug.leaf_0034.12).