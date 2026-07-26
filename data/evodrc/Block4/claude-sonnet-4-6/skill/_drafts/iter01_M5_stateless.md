## M5 Geometry Rules Summary

M5 is a strictly horizontal routing layer. Every M5 polygon must be an axis-aligned rectangle with no bends (M5.AUX.3 fires on any corner angle between 0° and 90°). Vertical edges must land on a 24 nm grid (M5.AUX.1).

### Horizontal Width (M5.W.1 – M5.W.4)

Horizontal width must be at least 24 nm (M5.W.1) and at most 480 nm (M5.W.2). M5.W.3 prohibits widths that are exact even integer multiples of 24 nm: 48, 96, 144, 192, 240, 288, 336, 384, 432, and 480 nm are all forbidden. M5.W.4 additionally forbids widths of 72, 168, 264, 360, and 456 nm, which cause the polygon to span an even number of minimum-width routing tracks. Together, the compliant widths below 480 nm follow the pattern 24×(4k+1) nm: 24, 120, 216, 312, and 408 nm.

### Vertical Width (M5.W.5)

Minimum vertical extent (height of the M5 rectangle) is 44 nm. Because M5 cannot bend, this constraint applies uniformly to the whole polygon.

### Routing Track Placement (M5.AUX.2, M5.AUX.4)

Minimum-width M5 segments (those that do not survive a −13 nm horizontal erosion/re-expansion) must have their horizontal centerlines on the vertical routing grid: pitch 192 dbu, offset 48 dbu, with edge quantization base 96 dbu (M5.AUX.2). Wide M5 polygons (those that do survive the −13 nm erosion) must not place their vertical side edges at positions that coincide with routing track edges (M5.AUX.4).

### Horizontal Spacing (M5.S.1)

Minimum horizontal spacing between any two M5 edges is 24 nm, regardless of edge length or mask color (M5.S.1). The rule fires on both projection-based checks (with_angle(90)) and general Euclidean checks (space(1.nm)), so even point or near-point proximity triggers a violation.

### Vertical Spacing (M5.S.2 – M5.S.5)

- Minimum vertical spacing between any two M5 edges: 40 nm (M5.S.2, with_angle(0)).
- Tip-to-tip between polygons on adjacent tracks that do not share a parallel run length: 40 nm (M5.S.3). The rule identifies non-overlapping tip edges via a sized(48 nm, 0) expansion then checks 40 nm spacing on those exposed edges.
- Tip-to-tip between polygons on adjacent tracks that do share a parallel run length: 40 nm (M5.S.4). Each horizontal endpoint edge is extended 30 nm outward; the extension must clear any facing horizontal edge by 40 nm.
- Minimum parallel run length between polygons on adjacent tracks: 44 nm (M5.S.5). Any horizontal gap narrower than 25 nm that places two tracks in proximity requires at least 44 nm of vertical overlap between the facing edges.

### Via Enclosure (V4.M5.EN.2, V4.M5.AUX.2, V5.M5.EN.1)

V4 and V5 vias inside M5 must be enclosed on at least two opposite sides by a minimum of 11 nm (V4.M5.EN.2, V5.M5.EN.1). Additionally, V4 must exactly match the M5 width in the direction perpendicular to the M5 run: the via's cross-track edges must be coincident with the enclosing M5 edges (V4.M5.AUX.2). A V4 whose side edges do not touch two opposite M5 edges fails this rule even if it is fully inside M5.

### Observed Repair Behavior

The single measured repair in this iteration moved two instances (i0234 and i0305) by 64 dbu in the vertical direction (trial:i01.ug.leaf_0025.11). That vertical shift simultaneously perturbed geometry on M5, M6, and V5, producing 9 new in-crop DRC violations (trial:i01.ug.leaf_0025.11). The repair was accepted because connectivity was preserved (trial:i01.ug.leaf_0025.11). A vertical instance move touching M5 must therefore be evaluated for cascading impact on both the via layer immediately above (V5) and the next metal layer (M6), not M5 alone.