## Via Enclosure Fixes: Prefer cu_pool Before unit_gate

VIA_VIA45_1_2_58_58 M4 land expansion (x-axis, +152 dbu per shape) successfully cleared enclosure violations when applied through the cu_pool channel: trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 reduced the total violation count by 16 across leaf_0012 and leaf_0013 (from 27+28 down to 19+20). Apply via-land resizes through cu_pool first; unit_gate trials operating on the same locus will encounter the op already in the pool and drop it at assembly (trial:i01.ug.leaf_0012.07 assemble_drops record shows all three VIA_VIA45/M4 resize ops dropped with reason `cu_pool:applied`). Do not re-issue cu_pool-applied M4 via resizes within the same design_state in a unit_gate trial.

## Horizontal (x-axis) M4 Polygon Resizes

Extending M4 polygon ends in the x-direction in steps on the order of 152–184 dbu was consistently gated_in without introducing new M4 violations. trial:i01.ug.leaf_0001.03 extended p1065 x-high by +184 dbu and p957 x-low by +176 dbu simultaneously without any new violations. A follow-on small x-low trim of p957 by −4 dbu (trial:i02.ug.leaf_0001.00) was likewise gated_in clean. These results confirm that x-direction end resizes on M4 at these magnitudes do not disturb M4.S.2 (40 nm horizontal spacing between vertical edges) or M4.W.5 (44 nm minimum horizontal width) provided the surrounding design state accommodates the extension.

Horizontal move of M4-containing polygon p938 by +32 dbu, together with four associated instance moves of [32,0] on M4/M5/V4 geometry (trial:i02.ug.leaf_0002.01), was gated_in with zero new violations. Lateral translation at 32 dbu increments is safe when applied uniformly to all M4 shapes sharing a connectivity group, as connectivity is preserved and the relative x-spacings remain unchanged.

## Instance Moves in Y Affecting M4 Stacks

Instance moves that shift M4/M3/M5/V3/V4 stacks vertically must be in multiples of 24 nm (M4.AUX.1 grid constraint on horizontal edges) and must not push minimum-width M4 centerlines off the 192 dbu pitch with 48 dbu offset defined by M4.AUX.2.

Moves of ±48 dbu in y on the M3/M4/M5/V3/V4 stack (trial:i01.ug.leaf_0012.07: instances i0097 [0,−48], i0092 [0,−48], i0064 [0,+96], i0072 [0,+96]; trial:i03.ug.leaf_0001.00: instances i0068 [0,+48], i0073 [0,+48]) were gated_in with zero new M4 violations. These deltas (48 and 96 dbu) are multiples of 48 (2× the 24 nm M4 y-grid), consistent with M4.AUX.1 compliance.

Moves of ±72 dbu in y (trial:i03.ug.leaf_0002.01: i0095 [0,+72], i0099 [0,+72], i0069 [0,−72], i0066 [0,−72]) were gated_in due to conn_preserved but introduced 1 new in-crop violation. The 72 dbu step is a multiple of 24 nm and therefore M4.AUX.1-legal, but 72 is not a multiple of 96 and therefore can shift M4 centerlines relative to the M4.AUX.2 routing track grid. Avoid ±72 dbu y-moves on M4 stacks when the region contains minimum-width M4 tracks subject to M4.AUX.2; prefer ±48 or ±96 dbu steps instead, as confirmed safe by trial:i01.ug.leaf_0012.07 and trial:i03.ug.leaf_0001.00.

## Forbidden Vertical Width Values

M4.W.3 forbids vertical widths that are even multiples of 24 nm: 48, 96, 144, 192, 240, 288, 336, 384, 432, 480 nm. M4.W.4 additionally forbids widths that span an even number of routing tracks: 72, 168, 264, 360, 456 nm. Taken together, the legal width sequence from 24 nm upward begins at 24 nm (1×), then jumps to non-even-track-count odd-multiple values. When resizing M4 vertically—whether through polygon resize or instance move—verify that the resulting width does not land on any value in the union {48, 72, 96, 144, 168, 192, 240, 264, 288, 336, 360, 384, 432, 456, 480} nm. The measured history contains no trials that violated these width rules in the current iteration, consistent with all vertical moves being executed in ±48 or ±72 dbu steps that preserved pre-existing widths rather than altering them (trial:i01.ug.leaf_0012.07, trial:i02.ug.leaf_0002.01, trial:i03.ug.leaf_0001.00, trial:i03.ug.leaf_0002.01).

## M4 Track Placement (M4.AUX.2)

Minimum-width M4 tracks (vertical width = 24 nm) must have their y-centerlines satisfying (cl − 48) mod 192 = 0 dbu, subject to the base filter that both the bottom and top edges of the shape are multiples of 96 dbu. When performing instance moves in y, confirm that all 24 nm M4 tracks within the moved instances land on an allowed centerline. The safe move increments observed (48 dbu, 96 dbu) are both exact multiples of the 192 dbu pitch, meaning any centerline that was legal before the move remains legal after (trial:i01.ug.leaf_0012.07, trial:i03.ug.leaf_0001.00). The 72 dbu increment is not a multiple of 192 and introduced a new in-crop violation (trial:i03.ug.leaf_0002.01).

## M4.AUX.3: No Bends

M4 polygons must not contain corners with angles in the 0°–90° range (i.e., M4 must be strictly rectangular, no L-bends). No trial in the current history introduced any bend geometry in M4; all M4 shape operations were end-resize or uniform lateral translation, neither of which introduces a non-rectangular corner. When composing repair ops for M4, limit polygon modifications to axis-aligned edge translations and avoid any operation that would produce a non-rectangular polygon.

## M4.AUX.4: Wide M4 Alignment

Wide M4 shapes (vertical width > 24 nm, specifically those not classified as 1x minimum-width) must not have their horizontal (y-constant) edges touching a routing track edge position. The M4.AUX.4 rule projects horizontal bands from minimum-width tracks outward and flags any wide M4 edge coinciding with those bands. No measured trial directly tested or triggered M4.AUX.4; however, instance moves that shift wide M4 geometry in y must account for this constraint to avoid aligning a wide M4 edge with a neighboring minimum-track band.

## V3.M4.AUX.2: V3 Width Must Match M4

V3 shapes that reside inside M4 must have their perpendicular-to-length width exactly equal to the M4 width at that location; V3 must not protrude or be narrower than M4 in that direction. No V3/M4 width mismatch violation was introduced by any measured trial. Instance moves that translate entire M3/M4/V3 stacks uniformly (trial:i01.ug.leaf_0012.07, trial:i03.ug.leaf_0001.00) preserve the relative V3–M4 width relationship and are safe with respect to V3.M4.AUX.2.