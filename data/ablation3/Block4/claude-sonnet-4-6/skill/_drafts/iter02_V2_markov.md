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


## Resize operations (iteration 2 measured evidence)

`resize_via_shape` on the x-axis is a valid and effective repair operation for V2
DRC violations. Expanding VIA_VIA23_1_3_36_36 in x by +144 dbu eliminated 51
violations (140 → 89) with connectivity preserved (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00).

Resizing V2 touches M2, M3, and V2 simultaneously (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00).
Apply enclosure checks on both M2 (V2.M2.EN.1: ≥5 nm on two opposite sides) and
M3 (V2.M3.EN.2: two-opposite-sides 5&5 or 5&0 nm) after any x-axis resize, since
both layers are affected by a single resize operation.

A resize that extends V2 in x widens the via footprint relative to the M3 track
direction. Verify V2.M3.AUX.2 (V2 width must match M3 width perpendicular to M3
length) after applying an x-axis resize; the resize must not create a width
mismatch on the perpendicular axis (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00).

Resize operations on V2 are distinct from translation moves: they alter the shape
index of the via cell rather than the cell origin. Resize and move are not
interchangeable repair strategies; the choice depends on which rule class is
violated (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00).