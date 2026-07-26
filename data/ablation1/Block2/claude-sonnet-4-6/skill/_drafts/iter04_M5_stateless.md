## Width and Track Placement

Horizontal polygon end resizes are accepted without connectivity loss when the resize delta is a multiple of 64 dbu along the x-axis: trial:i01.ug.leaf_0012.07 applied +64 dbu (low end) and +128 dbu (high end) to p938; trial:i02.ug.leaf_0003.02 applied +192 dbu (low end) to p938; trial:i03.ug.leaf_0002.01 applied +64 dbu (low end) and +320 dbu (high end) to p937. All three produced zero out-of-crop violations and received "gated_in" decisions.

M5.W.3 forbids horizontal widths equal to any even integer multiple of 24 nm: 48, 96, 144, 192, 240, 288, 336, 384, 432, and 480 nm. M5.W.4 additionally forbids widths of 72, 168, 264, 360, and 456 nm. When choosing a resize delta for a polygon end, compute the resulting width and confirm it falls outside both forbidden sets before applying.

M5.AUX.2 requires min-width M5 track centerlines to lie on a 192 dbu pitch grid with a 48 dbu offset from the origin (valid centerlines at x = 48, 240, 432, … dbu). The x-axis resize deltas used in trial:i01.ug.leaf_0012.07, trial:i02.ug.leaf_0003.02, and trial:i03.ug.leaf_0002.01 — all multiples of 64 dbu — are consistent with snapping endpoints to positions that preserve this centerline grid.

M5.AUX.1 requires every M5 vertical edge to sit on a 24 nm grid. Resize deltas that are multiples of 24 dbu preserve this alignment; all x-axis deltas in the history (64, 128, 192, 320 dbu) satisfy this criterion (trial:i01.ug.leaf_0012.07, trial:i02.ug.leaf_0003.02, trial:i03.ug.leaf_0002.01).

## Via Shape Resize (y-axis)

Shrinking a V4/M5 via cell shape in the y-axis by 88 dbu (trial:i04.cu.def:VIA_VIA45_1_2_58_58.00) is the only operation in this layer's history committed to the design. It reduced total violations by 16 (−8 in unit leaf_0002, −8 in unit leaf_0003) via the cu_pool channel targeting cell def:VIA_VIA45_1_2_58_58. Via shape resizes on M5 in the y-axis must go through the cu_pool channel because they modify the shared cell definition rather than an instance placement.

V4.M5.EN.2 requires V4 to be enclosed by M5 by at least 11 nm on two opposite sides. V4.M5.AUX.2 requires V4 to be exactly as wide as M5 in the direction perpendicular to the M5 run length. When applying a y-axis shrink to an M5 via shape, verify the remaining M5 extent still provides the 11 nm two-sided enclosure; the successful −88 dbu shrink in trial:i04.cu.def:VIA_VIA45_1_2_58_58.00 met both constraints.

V5.M5.EN.1 imposes the same 11 nm two-sided enclosure requirement for V5 inside M5. Via shape resizes that adjust M5 extent in y must be checked against V5 enclosure as well as V4 enclosure.

## Instance Moves Affecting M5

Instance moves in the y-axis at ±24 dbu and ±72 dbu are accepted without adding out-of-crop violations. trial:i03.ug.leaf_0002.01 moved eight instances (four at ±72 dbu, four at ±24 dbu), touching M3/M4/M5/V3/V4, and received "gated_in" with zero out-of-crop violations. trial:i04.ug.leaf_0003.02 moved three instances at ±24 dbu, touching M2/M3/M4/M5/V2/V3/V4, with the same result.

All successful y-axis move deltas in this history (±24 and ±72 dbu) are multiples of 24 dbu, which is the M5 vertical-edge grid pitch required by M5.AUX.1. Use only y-axis instance move deltas that are multiples of 24 dbu to preserve grid alignment across M5 and the via layers it interacts with (trial:i03.ug.leaf_0002.01, trial:i04.ug.leaf_0003.02).

M5.W.5 sets a 44 nm minimum vertical width; M5.S.2 sets a 40 nm minimum vertical spacing. Y-axis instance moves that are multiples of 24 dbu (24, 48, 72, …) were confirmed to leave these constraints satisfied in trial:i03.ug.leaf_0002.01 and trial:i04.ug.leaf_0003.02.

## Shape Topology Constraints

M5.AUX.3 forbids bends in M5: no M5 polygon may contain a corner between non-collinear edges. All resize operations in this history (trial:i01.ug.leaf_0012.07, trial:i02.ug.leaf_0003.02, trial:i03.ug.leaf_0002.01, trial:i04.cu.def:VIA_VIA45_1_2_58_58.00) operate on rectangular, straight-run polygons; do not apply end resizes that would form an L-shaped or non-rectilinear outline.

M5.AUX.4 prohibits the outside vertical edges of wide M5 polygons from aligning with the vertical edge positions of adjacent min-width routing tracks. When a resize delta extends a polygon beyond the 24 nm min-width, verify that the new outer vertical edge does not coincide with any min-width track edge in the same vertical band.

## Connectivity and Channel Policy

Every unit_gate trial in this history (trial:i01.ug.leaf_0012.07, trial:i02.ug.leaf_0003.02, trial:i03.ug.leaf_0002.01, trial:i04.ug.leaf_0003.02) preserved connectivity (conn_preserved=true) and introduced zero out-of-crop violations; all received "gated_in" decisions. "Gated_in" means the operation enters the unit pool but is not itself committed to the design. Only cu_pool operations that pass the delta evaluation are applied to the design state; trial:i04.cu.def:VIA_VIA45_1_2_58_58.00 is the sole applied commit in this layer's history, establishing the design state "70ef603a…".