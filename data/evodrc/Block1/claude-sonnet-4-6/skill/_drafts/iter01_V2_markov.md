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

### VIA_VIA23_1_3_36_36 M3 y-shrink isolation

Shrinking the M3 shape of cell VIA_VIA23_1_3_36_36 in y by -40 dbu in isolation
preserves connectivity but yields zero net DRC improvement across both the
enclosing unit (leaf_0034, 182 violations before and after) and the adjacent unit
(leaf_0035, 113 violations before and after). The cu_pool channel rejected this
op as `rejected_net_positive` (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). Do not
apply this standalone M3 y-shrink to VIA_VIA23_1_3_36_36 as a repair action; it
consumes an op slot with no benefit.

### Compound op sequence on VIA_VIA23_1_3_36_36 breaks connectivity

A 10-op compound sequence applied to leaf_0034 — comprising the same M3 y-shrink
(-40 dbu y on VIA_VIA23_1_3_36_36) combined with polygon end-resizes (p1214
right -4 dbu, p1178 right +192 dbu, p1255 right +100 dbu) and five instance
lateral moves (+72 dbu x for i0373, i0369, i0154, i0061, i0404; +136 dbu x for
i0060) touching layers M1, M2, M3, M4, V1, V2 — broke connectivity and was
gated out with 89 new violations introduced in crop and zero resolved outside
crop (trial:i01.ug.leaf_0034.12, decision gated_out, reason conn_broken). This
sequence must not be reused.

Anti-pattern AP-2: combining a V2-layer M3 y-shrink with lateral instance moves
of +72/+136 dbu x on shared-net instances in the same crop window destroys
net continuity. The unit_gate channel gated this out before any DRC evaluation
(trial:i01.ug.leaf_0034.12). Lateral moves of this magnitude must be validated
for net preservation independently before being paired with via-shape resizes.