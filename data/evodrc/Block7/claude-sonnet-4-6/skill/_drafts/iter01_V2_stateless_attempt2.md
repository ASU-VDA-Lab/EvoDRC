The two available measured records for this layer both resulted in accepted outcomes (`gated_in`, `conn_preserved`, zero new DRC errors in crop). Both touched V2 among M1, M2, M3, V1, and V2. The operations span instance moves and polygon end resizes. Because no violation records exist yet, the prescriptive repair knowledge derived from trials is narrow; the rule summaries below are descriptive characterizations of the checker logic, not independent assertions.

## Rule summary (checker structure)

**V2.W.1** enforces a minimum via width of 18 nm along the M3 length direction.

**V2.S.1** governs minimum projection-based spacing between V2 instances depending on M3 track relationship and end-cap type. The checker constructs a mask that extends beyond each via depending on whether the via is fully coincident with M3 edges (no-end-cap, NEC) or has exposed non-coincident edges (with-end-cap, WEC). Spacing values enforced are 18 nm (same-track or aligned parallel tracks) and 27 nm (non-aligned parallel tracks).

**V2.S.2** enforces a minimum Euclidean corner-to-corner spacing of 23 nm between two WEC (5 nm M3 end-cap) vias, computed on the extended WEC mask.

**V2.S.3** enforces a minimum Euclidean corner-to-corner spacing of 30 nm between two NEC (no end-cap) vias, flagging only violations that are not also projection-based violations.

**V2.S.4** enforces a minimum Euclidean corner-to-corner spacing of 27 nm between one WEC and one NEC via.

**V2.M2.EN.1** requires that M2 encloses V2 by at least 5 nm on at least two opposite sides.

**V2.M3.EN.2** requires that M3 encloses V2 by at least 5 nm on two opposite sides; the pair of enclosures may be (5 nm, 5 nm) or (5 nm, 0 nm, i.e., flush on one end).

**V2.AUX.1** requires V2 to reside inside the overlap of M2 and M3.

**V2.M3.AUX.2** requires V2 width in the direction perpendicular to M3 length to equal the M3 width exactly (no overhang, no gap).

**NONORTHOGONAL** flags any non-rectilinear edge on V2 (angles 1–89, 91–179, −179–−91, −89–−1 degrees).

## Observed repair patterns

In trial:i01.ug.Block7_union_row16.06, six operations were applied across M1, M2, M3, V1, and V2: four instance moves (two in −x by 36 dbu, one in +x by 36 dbu, two in −y by 12 dbu) and one direct polygon move (p3516, −12 dbu in y). The trial was accepted with no new V2 violations introduced or removed inside the crop. This confirms that translating instances and polygons in small integer-grid steps while preserving net connectivity is a safe strategy that does not generate secondary V2 DRC failures when the moved geometry already satisfies the enclosure and spacing rules relative to its neighbors (trial:i01.ug.Block7_union_row16.06).

In trial:i01.ug.leaf_0095.26, five operations were applied: two instance moves in +y by 48 dbu, one direct polygon end resize (p2432, y-axis, high end, +68 dbu), one instance move in +x by 36 dbu, and one direct polygon end resize (p3537, y-axis, high end, +48 dbu). The trial was accepted with connectivity preserved and no new in-crop V2 violations (trial:i01.ug.leaf_0095.26). Resizing the high end of an M3 (or M2) polygon upward while simultaneously moving the connected V2-touching instances upward by a matching or compatible delta avoids creating M3.EN.2 or AUX.1 failures at the extended boundary (trial:i01.ug.leaf_0095.26).

## Repair guidance grounded in measured records

When moving a V2-touching instance along x or y, move all co-connected M2/M3 polygon endpoints by a consistent delta so that the enclosure relationships defined by V2.M2.EN.1 and V2.M3.EN.2 are preserved; both trials demonstrate that consistent delta application across all touched layers produces zero new V2 errors (trial:i01.ug.Block7_union_row16.06, trial:i01.ug.leaf_0095.26).

When an M3 polygon end must be extended to resolve a V2.M3.EN.2 violation, resize only the high end of the polygon (the end that is deficient in enclosure); do not extend the opposite end unless that end also violates enclosure, because excess extension risks creating new V2.S.1 or V2.S.3 spacing failures with adjacent vias. Trial:i01.ug.leaf_0095.26 shows the high-end-only resize pattern (p2432 +68 dbu, p3537 +48 dbu on the high end) producing a clean accepted result.

Instance moves of 36 dbu in x and 12–48 dbu in y have been validated as safe step sizes that preserve V2 alignment on the M3 track grid in both recorded trials (trial:i01.ug.Block7_union_row16.06, trial:i01.ug.leaf_0095.26).