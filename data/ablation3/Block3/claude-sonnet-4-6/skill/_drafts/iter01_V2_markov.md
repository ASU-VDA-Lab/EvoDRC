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


## Iteration 1 measured facts (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00)

Within a multi-shape via cell, individual V2 shapes may require independent
move and resize operations along the same axis to resolve DRC violations.
In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, a 1×3 array cell (VIA_VIA23_1_3_36_36)
was repaired with 5 ops on V2: shape_index 0 moved −144 dbu x and resized +288 dbu x;
shape_index 2 moved +144 dbu x and resized +288 dbu x; shape_index 1 resized +288 dbu x
with no positional move. This asymmetric spread (outer shapes move outward, all shapes
widen) eliminated 27 DRC markers (delta_total = −27) while preserving connectivity
(conn_preserved = true). Touched layers were M2, M3, and V2, consistent with
enclosure rules V2.M2.EN.1 and V2.M3.EN.2 being the active constraints.

Within-cell V2 shape operations are PER-SHAPE, not uniform. A resize applied
to all shapes in the cell combined with asymmetric outward moves on the end shapes
is a confirmed repair pattern for array cells with enclosure violations on both ends
(trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). Do not apply a single uniform delta
to all shapes in an array cell; compute per-shape deltas based on each shape's
enclosure margin independently.

The +288 dbu x resize applied uniformly across all three shapes in
trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 confirms that V2.W.1 (18 nm minimum
width) and V2.M3.AUX.2 (V2 must match M3 width perpendicular to M3 length) permit
widening in the direction along M3 length when M3 co-extends with V2 after the
operation. Connectivity was preserved after all five ops, confirming M2 and M3
footprints accommodated the expanded V2 geometry.