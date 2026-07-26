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


## Multi-layer repair scope (iteration 1)

Both iteration-1 trials touch layers M1, M2, M3, V1, and V2 together in a
single gated-in repair unit (trial:i01.ug.Block7_union_row16.06,
trial:i01.ug.leaf_0095.26). V2 violations are resolved as part of a coordinated
multi-layer adjustment rather than by moving V2 instances in isolation. Treating
V2 as a single-layer target while ignoring co-located M1/M2/M3/V1 geometry
leaves the repair incomplete.


## Multi-directional instance moves within a single repair

A single V2 repair unit can require instances to move in opposing directions on
the same axis. In trial:i01.ug.Block7_union_row16.06, instances i0928 and i0407
move [−36, 0] while instance i0320 moves [+36, 0], and instances i0336 and i0308
move [0, −12], all within the same 6-op repair that preserves connectivity and
introduces zero new violations. Do not assume all instances in a repair unit
share a common delta; compute the required displacement per instance.


## M3 polygon resize as a V2 repair primitive

Resize-end operations on M3 polygons are a confirmed V2 repair primitive.
Trial:i01.ug.leaf_0095.26 resizes polygon p2432 by +68 dbu on the high-y end and
polygon p3537 by +48 dbu on the high-y end within the same repair unit, alongside
two instance moves of [0, +48]. The resize deltas are not uniform across polygons
in the same repair; each polygon receives an independently computed delta. A
resize_end on M3 can differ from the companion instance move delta (+68 vs +48
vs +48 in trial:i01.ug.leaf_0095.26) and still yield a clean DRC result.


## Connectivity preservation as a gate condition

Both iteration-1 trials are accepted on the basis of conn_preserved=true with
n_new_in_crop=0 and n_new_out_of_crop=0 (trial:i01.ug.Block7_union_row16.06,
trial:i01.ug.leaf_0095.26). A repair that introduces new violations outside the
crop region or breaks connectivity is rejected regardless of whether it resolves
the in-crop V2 error. Check both the in-crop violation count and the
out-of-crop delta before committing any move or resize.