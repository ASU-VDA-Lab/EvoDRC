**V2.M3.EN.2 — V2 enclosure by M3**

M3 must enclose V2 by at least 5 nm on two opposite sides; a 5 & 5 nm pair or a 5 & 0 nm pair both satisfy the rule. In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, five operations on cell VIA_VIA23_1_3_36_36 moved and resized V2 shapes along the x-axis (shape 0: move −144 dbu, resize +264 dbu; shape 1: resize +288 dbu; shape 2: move +144 dbu, resize +264 dbu) and reduced total M3-touching violations by 78 across two windows while preserving connectivity. Move and resize V2 shapes along the axis with deficient enclosure to recover the required 5 nm margin. The repair in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 held M3 geometry fixed and adjusted V2 to fit within the existing M3 boundary.

**V2.M3.AUX.2 — V2 width matching M3**

V2 must match M3 width in the direction perpendicular to M3 length; V2 edges in that direction must be coincident with M3 edges. The x-axis resize operations in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 corrected this relationship while preserving connectivity. Resize V2 shapes along the perpendicular axis to align V2 edges with the M3 boundary edges.

**M3 intrinsic geometry rules**

M3.W.1 requires minimum M3 width of 18 nm. M3.S.1 requires minimum 18 nm side-to-side spacing between polygons when both interacting edges exceed 36 nm in length. M3.S.2 requires 25 nm minimum tip-to-side spacing when a tip edge (≤ 36 nm) faces a side edge (> 36 nm). M3.S.3 requires 27 nm tip-to-tip spacing when both edges fall in the 24–36 nm range. M3.S.4 requires 31 nm tip-to-tip spacing when both edges are < 24 nm. M3.S.5 requires 31 nm tip-to-tip spacing when one edge is 24–36 nm and the other is < 24 nm. M3.S.6 requires a 20 nm euclidean corner-to-corner minimum between any two M3 polygons. M3.A.1 requires each M3 polygon to have area ≥ 504 nm². No repair operations addressing any of these rules appear in this layer's measured history; the rules are stated here from the DRC deck. No prescriptive repair guidance for M3.W.1, M3.S.1, M3.S.2, M3.S.3, M3.S.4, M3.S.5, M3.S.6, or M3.A.1 is grounded by a measured citation.

**V3.M3.EN.1 — V3 enclosure by M3**

M3 must enclose V3 by at least 5 nm on at least one horizontal opposite pair or one vertical opposite pair of sides. No repair operations addressing this rule appear in this layer's measured history. No prescriptive repair guidance for V3.M3.EN.1 is grounded by a measured citation.

**M3.GEOMETRY.NONORTHOGONAL**

All M3 edges must be strictly orthogonal (0° or 90°); edges at any other angle trigger a violation. No repair operations addressing this rule appear in this layer's measured history. No prescriptive repair guidance for M3.GEOMETRY.NONORTHOGONAL is grounded by a measured citation.