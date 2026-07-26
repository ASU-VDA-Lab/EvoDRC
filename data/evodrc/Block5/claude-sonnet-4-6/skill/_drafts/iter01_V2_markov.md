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

**Coordinated y-axis shrink of V2 instance with M2/M3 landing geometry resolves V2.W.1 / V2.S.1 / V2.M3.EN.2 violations.** In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, the repair engine applied a 5-op group to VIA_VIA23_1_3_36_36 at locus (1728,2068,9072,8732): the V2 shape on M3 was resized -40 dbu along the y-axis, and the four connected M2/M3 polygons (p894–p897) were each resized -64 dbu along the y-axis. This reduced the DRC error count in unit:leaf_0009 from 25 to 17 (-8 violations) while leaving unit:leaf_0010 unchanged at 25. Connectivity was preserved (conn_preserved: true). The touched layer set was {M2, M3, V2}.

**The via-shape resize delta (-40 dbu) and the landing-metal resize delta (-64 dbu) are not equal.** In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, the V2 shape shrank 4 nm while the four surrounding M2/M3 polygons each shrank 6.4 nm along the same axis. Do not assume a single uniform delta applies to all layers in a coordinated group; the shape-resize and metal-resize operations in the same group can carry different magnitudes.

**A multi-layer group (V2 + M2 + M3 simultaneously) is a valid and connectivity-safe repair strategy.** trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 confirms that resizing V2, M2, and M3 shapes in a single committed group preserves connectivity and resolves violations. This contradicts any assumption that V2 repairs must be isolated to the V2 layer alone before touching enclosing metals.

**Partial window improvement (not full clearance) is an accepted intermediate outcome.** In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, the repair was applied (decision: "applied") with delta_total -8 despite leaf_0010 remaining at 25 errors. A repair group need not clear all windows to be committed; net negative delta across the locus is sufficient for application.