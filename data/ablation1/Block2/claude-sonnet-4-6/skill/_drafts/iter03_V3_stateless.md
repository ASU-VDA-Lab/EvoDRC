**Rule Summary**

V3.W.1 requires a minimum V3 width of 18 nm along the M4 length direction.

V3.S.1 enforces projection-based spacing between V3 instances, with the threshold depending on M4 end-cap configuration: 18 nm between vias on the same M4 track or on aligned parallel tracks, and 27 nm between vias on non-aligned parallel tracks. The rule constructs masks (`v3_nec_mask` for end-cap-absent vias sized by 5 nm, `v3_wec_mask` for end-cap-present vias extended 5 nm along M4) and checks spacing on their exposed non-M4-coincident edges.

V3.S.2 enforces a minimum Euclidean corner-to-corner spacing of 23 nm between two V3 instances that both carry a 5 nm M4 end-cap (wec class). V3.S.3 enforces 30 nm between two instances both lacking an M4 end-cap (nec class). V3.S.4 enforces 27 nm between one wec and one nec instance. The Euclidean checks are filtered to exclude violations that also appear under the corresponding projection check, isolating true diagonal corner cases.

**M4 End-Cap Classification**

V3 end-cap class (wec vs. nec) is determined by whether the V3 instance has at least one edge not coincident with an M4 edge. A V3 instance is wec when at least one edge is non-coincident (M4 overhangs V3); it is nec when all edges are fully flush with M4 edges. The deck derives this from `v3_non_coinc_m4` and `v3_full_flush_m4` edge sets, and the resulting class directly selects which S.2/S.3/S.4 Euclidean threshold applies. Changing the extent of M4 relative to V3 can therefore shift a via between nec and wec classes and change which corner spacing rule governs it.

V3.M3.EN.1 requires M3 to enclose V3 by at least 5 nm on at least two opposite sides (left+right OR top+bottom). The rule uses `m3.sized(-5.nm, 0)` and `m3.sized(0, -5.nm)` independently, and a V3 instance passes if it is fully inside either shrunk polygon. Failures occur when M3 is undersized on both axis pairs simultaneously.

V3.M4.EN.2 requires M4 to enclose V3 by at least 11 nm on at least two opposite sides, checked analogously via `m4.sized(-11.nm, 0)` and `m4.sized(0, -11.nm)`. The 11 nm threshold is substantially larger than the M3 enclosure threshold (5 nm), making M4 enclosure the tighter constraint in the direction perpendicular to M4 length.

V3.AUX.1 requires V3 to be fully inside the intersection of M3 and M4. Any V3 polygon extending outside either metal layer triggers this rule, independent of the enclosure rules.

V3.M4.AUX.2 requires V3 to match M4's width exactly in the direction perpendicular to M4's length. A V3 inside M4 must have at least two coincident edges with M4 edges (checked via `v3_aux2_coinc` and `interacting(..., 2)`). A V3 that is narrower than M4 across its full span, leaving no flush edges, fails this rule.

The NONORTHOGONAL block applies to every drawing layer including V3. Edges at any angle other than 0° or 90° (i.e., angles in 1–89°, 91–179°, −179° to −91°, or −89° to −1°) constitute a violation. All move and resize operations on V3 must preserve rectilinear geometry.

**Measured Repair: trial:i03.ug.leaf_0002.01**

The single measured repair for this layer addressed V3-related DRC violations in Block2, unit leaf_0002 by combining symmetric opposing Y-axis instance moves with asymmetric X-axis M4 polygon resizing across five layers: M3, M4, M5, V3, and V4 (trial:i03.ug.leaf_0002.01). The instance moves were applied as four opposing pairs: i0098 and i0094 at +72 dbu, i0110 and i0090 at +24 dbu, i0061 and i0070 at −24 dbu, and i0066 and i0069 at −72 dbu. This symmetric Y-axis spread increased inter-via separation without displacing the centroid of the via cluster. Polygon p937 was simultaneously resized on the X axis with the low end extended by 64 dbu and the high end extended by 320 dbu, an asymmetric extension favoring the high end by a factor of five (trial:i03.ug.leaf_0002.01).

Apply symmetric Y-axis instance spreading in opposing pairs when inter-via spacing violations are present along the Y axis; the accepted repair at trial:i03.ug.leaf_0002.01 demonstrates that graded offsets (±72 dbu outer pair, ±24 dbu inner pair) distributes spacing increases across multiple via pairs in a single operation. Apply asymmetric X-axis M4 polygon extension when enclosure or width violations exist on both ends but at different magnitudes; trial:i03.ug.leaf_0002.01 shows that unequal end extensions (64 dbu low, 320 dbu high) are compatible with a clean gated_in outcome.

The repair introduced 2 new violations within the crop region and zero outside it (trial:i03.ug.leaf_0002.01, n_new_in_crop=2, n_new_out_of_crop=0). The decision was gated_in because connectivity was preserved (trial:i03.ug.leaf_0002.01, conn_preserved=true). Preserve connectivity when applying move or resize operations to V3-adjacent layers (trial:i03.ug.leaf_0002.01); conn_preserved=true was the required condition for gated_in acceptance in this repair, and the presence of 2 residual in-crop violations did not block acceptance when that condition held.