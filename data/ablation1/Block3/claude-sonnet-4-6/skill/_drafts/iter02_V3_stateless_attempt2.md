## Rule Parameters

**V3.W.1** enforces a minimum V3 width of 18 nm along the direction parallel to M4 length.

**V3.S.1** covers three spacing sub-cases, all using projected distances on the `v3_mask` derived geometry. The mask adds a virtual 5 nm extension to "with-end-cap" (wec) shapes (V3 shapes whose edges do not fully coincide with M4 edges) and applies `sized(5.nm)` to "no-end-cap" (nec) shapes (V3 shapes that are fully flush with M4). The three thresholds are: 18 nm between shapes on the same M4 track; 27 nm between shapes on parallel non-aligned tracks; 18 nm between shapes on parallel aligned tracks.

**V3.S.2** enforces 23 nm Euclidean corner-to-corner separation between two wec-class V3 shapes (both carrying a 5 nm M4 end-cap).

**V3.S.3** enforces 30 nm Euclidean corner-to-corner separation between two nec-class V3 shapes (neither carries an end-cap).

**V3.S.4** enforces 27 nm Euclidean separation between a wec-class shape and an nec-class shape (mixed end-cap pair), checked as `v3_wec_mask.separation(v3_nec_mask)`.

## Enclosure Rules

**V3.M3.EN.1** requires M3 to enclose V3 by at least 5 nm on at least one pair of opposite sides. The check passes when V3 is either fully contained in `m3.sized(-5.nm, 0)` (left+right enclosure) or in `m3.sized(0, -5.nm)` (top+bottom enclosure); shapes failing both checks, or lying outside M3 entirely, are flagged.

**V3.M4.EN.2** requires M4 to enclose V3 by at least 11 nm on at least one pair of opposite sides. Shapes failing both the x-inset and y-inset tests simultaneously are flagged.

## Containment and Width-Match Rules

**V3.AUX.1** fires on any V3 shape that falls outside the boolean intersection of M3 and M4. The rule checks `v3.not_inside(m3 & m4)`, so a V3 shape partially outside either metal layer is flagged.

**V3.M4.AUX.2** fires when a V3 shape inside M4 does not have at least two edges coincident with M4 boundary edges. The check requires `v3_aux2_in.interacting(v3_aux2_coinc, 2)`: each qualifying V3 must touch the M4 boundary on two or more edges, enforcing that V3 exactly spans the M4 width in the axis perpendicular to M4 length.

## Repair Observations from Measured Trials

Both completed trials for this layer were accepted with connectivity preserved (trial:i02.ug.leaf_0002.01, trial:i02.ug.leaf_0003.02).

**Y-axis instance moves** were the primary repair operation in both accepted trials. In trial:i02.ug.leaf_0002.01, six instances were translated along y at magnitudes of ±48 dbu and ±96 dbu across a locus touching M3, M4, M5, V3, and V4. The moves were applied in opposing balanced pairs: instances i0177 and i0152 at −48 dbu, i0079 and i0102 at −96 dbu, and i0078 and i0101 at +48 dbu. Applying y-axis instance moves in balanced, opposing pairs across the V3 locus resolved the spacing condition while preserving connectivity (trial:i02.ug.leaf_0002.01).

**X-axis polygon resize combined with y-axis instance moves** was used in trial:i02.ug.leaf_0003.02, where polygon p1059 was resized with +64 dbu on the low x-end and +320 dbu on the high x-end, and eight instances were moved along y at displacements of +72, +24, −24, and +24 dbu. The combined resize-and-move approach on M-layer geometry, applied over a locus touching M3, M4, M5, V3, and V4, was accepted with connectivity preserved (trial:i02.ug.leaf_0003.02).

All grid-aligned y-axis move increments recorded across the two accepted trials are multiples of 24 dbu (24, 48, 72, 96 dbu in trial:i02.ug.leaf_0002.01 and trial:i02.ug.leaf_0003.02). Moves at these increments produced clean results on V3 without violating the containment or enclosure relationships to M3 and M4.

Trial:i02.ug.leaf_0002.01 introduced four new violations each of M1.A.1 and V1.M1.EN.1 within the crop window, yet the trial was still gated in because connectivity was preserved. V3-targeted move operations are therefore not required to eliminate all in-crop violations in unrelated layers in order to be accepted.