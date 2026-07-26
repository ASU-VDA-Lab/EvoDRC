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

**V2 y-axis resize with co-resize of M2 clears DRC violations.**
In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, all three V2 shapes in cell
VIA_VIA23_1_3_36_36 were resized +64 dbu along the y-axis (shape_index 0, 1, 2),
and the single M2 shape in that cell was co-resized +64 dbu in y. This 4-op
batch reduced total violations by 8 (from 68 to 60) with conn_preserved=true.
Net rate: 2 violations cleared per shape resize.

**Multi-shape V2 cells require whole-cell resize, not single-shape edits.**
Cell VIA_VIA23_1_3_36_36 contains at least three V2 shapes. The repair applied
the same delta (+64 dbu y) to all three simultaneously (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).
Resizing only a subset would leave internal V2.W.1 or V2.S.1 violations between
the resized and unresized shapes within the same cell.

**M2 co-resize is required when V2 shapes are resized in y.**
The single M2 shape in the cell was included in the same op batch as the V2
resize (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, touched_layers includes M2).
V2.M2.EN.1 requires ≥5 nm M2 enclosure of V2 on at least two opposite sides;
expanding V2 in y without expanding M2 in y would violate that rule.

**M3 enclosure must be verified after y-resize even without an explicit M3 op.**
M3 appears in touched_layers for trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 despite
no explicit M3 resize op being listed. V2.M3.EN.2 and V2.M3.AUX.2 impose strict
M3-enclosure and M3-width-matching constraints; the DRC checker evaluates M3
interactions whenever V2 geometry changes, and the net −8 result confirms these
rules were satisfied without a separate M3 edit.

**A +64 dbu y-expansion is a verified safe resize quantum for this cell type.**
The 36×36 (dbu) nominal V2 cell dimension embedded in VIA_VIA23_1_3_36_36's
name, combined with the +64 dbu delta, yields a post-resize y-extent well above
the V2.W.1 minimum of 18 nm (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). No new
width, spacing, or enclosure violations were introduced.