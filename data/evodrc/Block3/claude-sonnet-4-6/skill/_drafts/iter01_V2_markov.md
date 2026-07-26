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


## Cell-definition (def-level) repairs

**Def-level shape editing is a distinct repair modality from instance placement moves.**
trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 demonstrates a successful 5-op cell-definition
repair on cell VIA_VIA23_1_3_36_36 that reduced DRC violations by 27 (leaf_0018: 32→17,
leaf_0019: 35→23) with connectivity preserved.

The repair applied asymmetric per-shape treatment across three shape indices within
the same cell definition (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00):

- shape_index 0: move x −144 dbu, then resize x +288 dbu
- shape_index 1: resize x +288 dbu only (no move)
- shape_index 2: move x +144 dbu, then resize x +288 dbu

This asymmetry — different move deltas (−144, 0, +144) combined with uniform resize
(+288 each) — is the operative pattern. Do not assume all shapes in a cell definition
receive the same move delta; the solver assigns per-shape transforms independently.

The touched layers were M2, M3, and V2 (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00),
confirming that a def-level V2 shape edit propagates enclosure and spacing checks
simultaneously on both bounding metal layers. A repair targeting V2.W.1 or V2.S.1
violations inside a named via cell must therefore validate M2 enclosure (V2.M2.EN.1)
and M3 enclosure (V2.M3.EN.2) after the edit before declaring the repair clean.