## Via Cell M2 Landing Shape Resize

A y-axis extension of the M2 landing shape inside a via cell, combined with matching V2 shape resizes, reduced violations. In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, a +64 dbu y-axis `resize_via_shape` on M2 shape_index 0 in cell VIA_VIA23_1_3_36_36 was applied together with three +64 dbu y-axis resizes on V2 shapes in the same cell, reducing total violations by 8 (68 → 60) with connectivity preserved. The repair touched layers M2, M3, and V2.

The single observed repair in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 resized both the M2 landing shape and the enclosed V2 shapes together; no trial exists in which M2 was resized without simultaneously adjusting the V2 shapes.

## Rule Thresholds

The entries below state rule thresholds only. No additional repair trial data exists for these rules in this iteration.

- **M2.W.1**: minimum M2 width is 18 nm.
- **M2.S.1**: side-to-side spacing ≥ 18 nm when both interacting edges are > 36 nm long.
- **M2.S.2**: tip-to-side spacing ≥ 25 nm (projection) when one edge is ≤ 36 nm and the other is > 36 nm.
- **M2.S.3**: tip-to-tip spacing ≥ 27 nm when both tip edges are between 24 nm and 36 nm.
- **M2.S.4**: tip-to-tip spacing ≥ 31 nm when both tip edges are < 24 nm.
- **M2.S.5**: tip-to-tip spacing ≥ 31 nm when one tip edge is 24–36 nm and the other is < 24 nm.
- **M2.S.6**: corner-to-corner euclidean spacing ≥ 20 nm between any two M2 polygons (Euclidean, not projection).
- **M2.A.1**: minimum M2 polygon area is 504 nm².
- **M2.S.7**: a tip-to-tip gap of 18 nm co-located with a side-to-side spacing of ≤ 32 nm is forbidden; parallel run length must be ≥ 35 nm when side spacing is ≤ 32 nm.
- **M2.S.8**: euclidean distance between centers of tip-to-tip gaps on different M2 tracks must be ≥ 80 nm; gap centers are computed by shrinking each 18 nm tip-to-tip gap region by 8.5 nm per side.
- **V1.M2.EN.2**: M2 must enclose V1 by ≥ 5 nm on at least two opposite sides; the opposite pair may be 0 nm enclosure.
- **V1.M2.AUX.2**: V1 must match M2 width exactly in the direction perpendicular to the M2 run direction.
- **V2.M2.EN.1**: M2 must enclose V2 by ≥ 5 nm on at least two opposite sides.
- **GEOMETRY.NONORTHOGONAL**: all M2 edges must be strictly orthogonal (0° or 90°); edges at any other angle are forbidden.