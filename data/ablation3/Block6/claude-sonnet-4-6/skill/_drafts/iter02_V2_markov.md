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


## Within-cell multi-shape V2 repair (iteration 2 evidence)

**Move + resize on individual cuts is a valid repair primitive.** Trial
i02.cu.def:VIA_VIA23_1_3_36_36.00 repaired cell `VIA_VIA23_1_3_36_36` by
applying five operations across three V2 shapes on the x-axis: shape\_0 moved
−144 dbu then resized +288 dbu x; shape\_1 resized +288 dbu x (no move);
shape\_2 moved +144 dbu then resized +288 dbu x. The repair reduced violations
from 159 to 81 (−78) and preserved connectivity (trial
i02.cu.def:VIA_VIA23_1_3_36_36.00).

**Asymmetric displacement within one cell is intentional.** The −144 dbu move on
shape\_0 and the +144 dbu move on shape\_2 are opposite-direction; this is not
an error. The pattern spreads cuts outward symmetrically while expanding each
cut's width, consistent with simultaneously satisfying V2.W.1 (minimum width
18 nm) and V2.S.1 spacing constraints for cuts sharing the same M3 track (trial
i02.cu.def:VIA_VIA23_1_3_36_36.00).

**All three touched layers (M2, M3, V2) must remain consistent.** The repair
touches M2, M3, and V2 and still preserves connectivity, confirming that
within-cell cut reshaping on V2 does not by itself break M2/M3 enclosure
(V2.M2.EN.1, V2.M3.EN.2) when the resize keeps cuts inside the existing metal
overlap region (trial i02.cu.def:VIA_VIA23_1_3_36_36.00).

**Do not apply a uniform delta to all shapes in a multi-cut cell.** Shapes
received different move deltas (−144, 0, +144) and all received the same resize
delta (+288). Applying one move value to every cut would shift the centroid of
the cut array and risk introducing new V2.AUX.1 or V2.M3.AUX.2 violations.
Derive per-shape deltas independently (trial i02.cu.def:VIA_VIA23_1_3_36_36.00).