## Geometry Rules

V3.W.1 requires a minimum width of 18 nm along the M4 length direction. All V3 polygon edges must be strictly orthogonal; any edge with an angle in [1°, 89°] ∪ [91°, 179°] ∪ [−179°, −91°] ∪ [−89°, −1°] triggers the NONORTHOGONAL violation for layer V3.

## Enclosure Rules

V3.AUX.1 requires every V3 instance to lie entirely within the intersection of M3 and M4. V3.M3.EN.1 requires M3 to enclose V3 by at least 5 nm on at least one pair of opposite sides (left/right pair via `m3.sized(-5nm, 0)`, or top/bottom pair via `m3.sized(0, -5nm)`); failing both tests simultaneously constitutes a violation. V3.M4.EN.2 requires M4 to enclose V3 by at least 11 nm on at least one pair of opposite sides. V3.M4.AUX.2 requires V3 to match the M4 width exactly in the direction perpendicular to M4 length: the instance must have at least two opposite edges coincident with M4 edges, and any V3 geometry not satisfying this constraint on two sides is flagged.

## Spacing Rules and WEC/NEC Classification

The V3 spacing deck separates instances into two classes based on their relationship to M4 edges. A "no-end-cap" (NEC) instance has all its edges coincident with M4 edges (`v3_full_flush_m4`). A "with-end-cap" (WEC) instance has at least one edge not coincident with M4 (`v3_wec`), and the deck extends its mask by 5 nm outward along the M4 direction (`v3_wec_coinc_m4.extended(0, 0, 5nm, 0)`). Spacing requirements:

- **V3.S.1** (projection): 18 nm on the same M4 track or between aligned parallel tracks; 27 nm between non-aligned parallel tracks. The rule applies both to NEC mask edges not interacting with M4 and to the merged WEC+extension mask edges not on M4.
- **V3.S.2** (Euclidean, WEC–WEC): 23 nm corner-to-corner between two WEC instances. Violations appear only as Euclidean hits that lack a corresponding projected hit.
- **V3.S.3** (Euclidean, NEC–NEC): 30 nm corner-to-corner between two NEC instances. Same Euclidean-without-projection logic as V3.S.2.
- **V3.S.4** (Euclidean, WEC–NEC): 27 nm corner-to-corner between one WEC and one NEC instance.

The 5 nm end-cap extension used in WEC mask construction is the same threshold that defines M4 enclosure for spacing purposes; a V3 instance that perfectly matches M4 extent (NEC) carries the larger corner spacing requirement (30 nm NEC–NEC vs. 23 nm WEC–WEC) because its mask is not extended before the check.

## Accepted Repair Operations (Measured)

### Single-Instance X-Axis Move

trial:i02.ug.leaf_0003.03 applied one move_instance of −16 dbu in x to instance i0358 within a compact locus. The operation touched M3, M4, and V3 and was accepted with connectivity preserved and no new violations propagated outside the crop area (n_new_out_of_crop=0). A small x-axis shift that moves a V3-touching instance is a viable repair primitive when connectivity is maintained.

### Large Coordinated Y-Axis Moves with Polygon Resizes

trial:i02.ug.leaf_0010.06 applied 24 move_instance operations (deltas of ±24 dbu and ±72 dbu in y across instances i0379, i0366, i0360, i0198, i0136, i0168, i0527, i0435, i0411, i0109, i0022, i0026, i0375, i0367, i0362, i0225, i0137, i0177, i0531, i0426, i0424, i0114, i0023, i0030) and 12 resize_end operations on polygons (p1826, p1833, p1831, p1792, p1786, p1806, p1845, p1844, p1857, p1734, p1757, p1749), with high-end and low-end y deltas of ±24 dbu and ±72 dbu, across a large locus. The 36-operation batch touched M3, M4, M5, V3, and V4, and was accepted with connectivity preserved and n_new_out_of_crop=0. Mixed positive and negative y deltas within the same accepted batch are valid: some instances moved +72 dbu while others moved −72 dbu in the same trial (trial:i02.ug.leaf_0010.06).

### Multi-Layer Scope

Both accepted trials modified V3 alongside its bounding metal layers. trial:i02.ug.leaf_0003.03 touched M3 and M4 alongside V3. trial:i02.ug.leaf_0010.06 extended to M5 and V4 as well. Because V3.AUX.1 mandates that V3 lie inside M3 ∩ M4 and V3.M4.AUX.2 mandates exact width matching with M4 perpendicular to its length, moving a V3 instance without coordinating the enclosing M3 and M4 geometry risks introducing enclosure or containment violations; both trials adjusted M3 and M4 in the same operation batch as V3 (trial:i02.ug.leaf_0003.03, trial:i02.ug.leaf_0010.06).