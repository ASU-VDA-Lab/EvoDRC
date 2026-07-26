## Repair Patterns Grounded in Measured History

### Uniform-delta co-move of instance and M3 polygon is the established V2 repair pattern

All accepted trials that touch only M2, M3, and V2 — with no other layers — apply a single (dx, dy) displacement identically to the V2-containing instance and the associated M3 polygon. Trial `i02.ug.leaf_0001.07` moved instance i1643 and polygon p3383 each by (0, −57) dbu; trial `i03.ug.leaf_0001.03` moved the same pair by (0, +21) dbu. Both were accepted (gated_in, conn_preserved). Apply the identical delta to every instance and M3 polygon that share the V2 connection being repositioned; diverging the deltas would disturb the relative offset between V2 and its enclosing metals, risking violations of V2.M2.EN.1, V2.M3.EN.2, and V2.AUX.1.

### M3 resize_end extends end-cap enclosure for V2.M3.EN.2

When a V2 sits near an M3 terminus and the 5 nm enclosure on the terminus side is insufficient, extend the M3 end by issuing a `resize_end` operation on the relevant end. Trial `i01.ug.leaf_0095.26` extended polygon p2432 end=high by y=+68 dbu and polygon p3537 end=high by y=+48 dbu while V2 was among the touched layers, and the trial was accepted. Trial `i03.ug.leaf_0011.07` applied resize_end on p3537 end=high by y=−48 dbu and was also accepted. Direct the resize_end to the M3 end nearest the V2 face lacking adequate enclosure.

### Inserting a new M3 stub polygon resolves enclosure shortfall when no existing M3 segment can be extended

Trial `i03.ug.leaf_0002.04` added an M3 polygon with corners at [[11664,11756],[11664,11828],[11908,11828],[11908,11756]] (244 × 72 dbu) while V2 was among the touched layers, and the trial was accepted. The stub must cover the V2 footprint with sufficient overlap on two opposite sides to satisfy V2.M3.EN.2 (5 nm on each of the two sides, or 5 nm on one and 0 nm flush on the other). The M3 stub width in the direction perpendicular to M3 length must exactly match the V2 width in that direction to satisfy V2.M3.AUX.2; the stub added in trial `i03.ug.leaf_0002.04` has 72 dbu in the shorter dimension, constraining the co-located V2 to that same perpendicular width.

### Moving multiple V2-containing instances by an identical delta preserves V2.S.1 inter-instance spacing

Trial `i02.ug.leaf_0014.08` moved instances i0519 and i0524 and polygon p3515 each by (0, −12) dbu while V2 was among the touched layers, and the trial was accepted. Translating co-routed V2 instances by the same vector keeps all pairwise spacings constant, satisfying V2.S.1 (minimum spacing 18 nm on the same track, 27 nm across non-aligned parallel tracks).

### Iterative re-repair on the same unit across iterations is valid

A unit repaired in one iteration can be revisited in a later iteration without structural conflict. Leaf_0001 received a move of (0, −57) dbu in iter 2 via `i02.ug.leaf_0001.07` and a corrective move of (0, +21) dbu in iter 3 via `i03.ug.leaf_0001.03`, yielding a net displacement of (0, −36) dbu; both trials were accepted. Re-repair is appropriate when an earlier repair left residual violations or introduced new ones.

### New violations introduced within the crop window do not block acceptance when connectivity is preserved

Trial `i03.ug.leaf_0001.03` reported n_new_in_crop=3 yet was accepted (gated_in) because conn_preserved=true. The acceptance gate is connectivity preservation; a non-zero n_new_in_crop count is tolerated.