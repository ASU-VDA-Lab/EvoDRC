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


## Iteration 1 measured facts (trial:i01.ug.whole_design.00)

Provenance: Block5, channel unit_gate, whole-design crop, 19 ops, connectivity
preserved (conn_preserved: true), design state ef66d47d. Touched layers include
V2 among M1–M5, V1–V4.

**Paired co-movement on V2-adjacent instances is the dominant repair pattern.**
In trial:i01.ug.whole_design.00, every instance move that affects a V2-touching
net was issued as a same-delta pair: i0112/i0105 both [0,-48], i0001/i0002 both
[0,+24], i0073/i0075 both [0,+96], i0067/i0070 both [0,-24], i0062/i0076 both
[0,+48], i0061/i0104 both [+8,0]. Issuing a move to only one member of such a
pair while leaving the other stationary breaks the shared landing geometry and
introduces new V2.AUX.1 or V2.M3.AUX.2 violations. Always identify the full
co-move group before committing any instance delta (trial:i01.ug.whole_design.00).

**Polygon resize on M3 or M2 is required when instance moves shift a V2 landing
edge.** In trial:i01.ug.whole_design.00, polygon p879 received a resize_end on
the high-y edge (+48 dbu) and polygon p910 received both a translate (+8 x) and
a resize_end on the high-y edge (+20 dbu). These polygon edits accompany the
[+8,0] move of i0061/i0104, confirming that metal-end extension must track via
displacement to satisfy V2.M3.EN.2 (5 nm enclosure on two opposite sides) and
V2.M3.AUX.2 (via width matches M3 width perpendicular to length). Do not move a
V2-touching instance without also adjusting the coincident metal polygon end to
maintain the required enclosure (trial:i01.ug.whole_design.00).

**Axis-split moves (x-only vs y-only in the same repair) are both valid and
connectivity-safe.** trial:i01.ug.whole_design.00 shows moves with delta_dbu
vectors that are purely y ([0,±N]) or purely x ([+8,0]) within a single
19-op repair that passed conn_preserved. Do not assume all V2-adjacent moves must
share the same axis or the same sign within one repair pass.

**i0012 moves +136 x while no paired partner appears in the op list.** This
matches the ANCHOR pattern from the reference-design tail evidence: one instance
advances while the corresponding via on the adjacent level remains stationary as
the M2–M3 anchor. Before issuing such a solo move, confirm that the stationary
partner's M2 and M3 landings still satisfy V2.M2.EN.1 (5 nm enclosure on two
opposite sides) and V2.AUX.1 (V2 inside both M2 and M3) at the post-move
geometry (trial:i01.ug.whole_design.00; seed, reference-design-verified).

**i0103 moves −28 x (negative, non-standard grid step).** The repair grid is not
restricted to multiples of 24 dbu or 36 dbu; −28 dbu is a legal delta in this
process. Do not reject or round a computed delta solely because it is not a
"round" grid multiple; apply it if it resolves the violation and preserves
connectivity (trial:i01.ug.whole_design.00).