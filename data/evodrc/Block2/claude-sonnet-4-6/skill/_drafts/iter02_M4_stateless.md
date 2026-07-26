## Repair Operations Observed on M4

### X-axis resize_end is the primary single-polygon repair primitive

X-axis `resize_end` operations on M4 polygons introduced no new violations and preserved connectivity in every trial that used them. trial:i01.ug.leaf_0001.03 applied `resize_end` to p1065 (high end, +184 dbu) and p957 (low end, +176 dbu) simultaneously; both gated in with `n_new_in_crop=0`. trial:i02.ug.leaf_0001.00 subsequently applied a small corrective `resize_end` to the same polygon p957 (low end, −4 dbu) and again gated in cleanly. The recurrence of p957 across two iterations demonstrates that coarse endpoint moves made in iteration 1 require fine trimming in iteration 2; do not treat an iter-1 gated_in outcome as final for that polygon.

### X-axis polygon move and instance move preserve connectivity and introduce no M4 violations

trial:i02.ug.leaf_0002.01 moved M4 polygon p938 by +32 dbu in x and simultaneously moved four instances (i0098, i0097, i0064, i0068) by [32, 0]. The trial gated in with `n_new_in_crop=0` and `n_new_out_of_crop=0`. When an M4 segment and every instance that lands on its routing track must shift together, co-moving the polygon and all co-located instances in a single trial prevents internal spacing violations between the shifted M4 geometry and its neighbors.

### Y-axis instance moves touching M4 are viable but introduce cross-layer debt

trial:i01.ug.leaf_0012.07 moved four instances in y (two by −48 dbu, two by +96 dbu). The touched layers included M4, M5, V3, V4. The trial gated in (`conn_preserved=true`) but introduced 2 new in-crop violations of rule V1.M1.EN.1. No new M4-specific violations were reported in this trial. However, several cu_pool M4 and V4 via shape resize ops were listed under `assemble_drops` as already applied, meaning cu_pool had previously committed VIA_VIA45_1_2_58_58 shape changes before this trial assembled. Y-axis instance moves that span M4 must account for already-applied cu_pool via shape changes; the assembler silently drops duplicate ops, so the effective M4 geometry at assembly time may differ from the pre-op snapshot.

### Cu_pool via shape resize on M4 is effective and must not be re-applied by unit_gate

trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 resized the M4 via shape (shape_index 0) of cell `VIA_VIA45_1_2_58_58` by +152 dbu in x (axis x), reducing total violation count by 16 across leaf_0012 and leaf_0013. When trial:i01.ug.leaf_0012.07 subsequently attempted to apply the same op, the assembler dropped it with reason `cu_pool:applied`. Never include a cu_pool-applied M4 via shape resize in a unit_gate trial op list; the drop is silent and the expected geometric outcome will not materialize.

---

## M4 Geometric Constraints and Their Repair Implications

### Vertical width must be in [24 nm, 480 nm] and must not equal even multiples of 24 nm or the forbidden odd-track values

Rules M4.W.1 and M4.W.2 bound vertical width to [24, 480] nm. Rule M4.W.3 forbids vertical widths that are exact even multiples of 24 nm (48, 96, 144, 192, 240, 288, 336, 384, 432, 480 nm). Rule M4.W.4 additionally forbids widths 72, 168, 264, 360, and 456 nm. When a `resize_end` on a y-endpoint is being planned to fix another violation, verify the resulting vertical extent does not land on any of these forbidden values. The safe single-track width is 24 nm; the next allowable wider values are those not in M4.W.3 or M4.W.4 lists (e.g., 25 nm through 47 nm, 49 nm through 71 nm, etc., subject to other rules).

### Horizontal width minimum is 44 nm (M4.W.5)

M4.W.5 requires a minimum horizontal (x-direction) width of 44 nm. X-axis resize operations observed in trial:i01.ug.leaf_0001.03 and trial:i02.ug.leaf_0001.00 operated on the x-endpoints of M4 polygons; both gated in without triggering M4.W.5, confirming that the pre-op horizontal extents were safely above 44 nm. When shrinking an M4 polygon in x, confirm the resulting width does not fall below 44 nm before committing.

### Horizontal edges must lie on a 24 nm grid (M4.AUX.1)

M4.AUX.1 requires all M4 horizontal edges to be on a 24 nm grid. Y-axis instance moves by −48 dbu and +96 dbu (trial:i01.ug.leaf_0012.07) are multiples of 24 nm and therefore grid-safe. X-axis moves of +32 dbu (trial:i02.ug.leaf_0002.01) and resize_end deltas of −4 dbu (trial:i02.ug.leaf_0001.00) do not affect horizontal edges, so they do not implicate M4.AUX.1. Any repair that does shift y-positions of M4 horizontal edges must use deltas that are multiples of 24 nm.

### Minimum-width M4 tracks must align to 192 nm pitch with 48 nm offset (M4.AUX.2)

M4.AUX.2 requires that single-track (minimum-width) M4 polygons have their centerline on the horizontal routing grid at pitch 192 nm with a 48 nm offset. Y-axis instance moves must land the resulting M4 track centerlines on this grid. The observed moves in trial:i01.ug.leaf_0012.07 (−48 and +96 dbu) are multiples of 48, which is a divisor of 192, ensuring they remain on grid.

### M4 may not bend (M4.AUX.3)

M4.AUX.3 prohibits any corner angles between 0° and 90°. All observed M4 repairs used axis-aligned resize or move operations; none introduced non-Manhattan geometry. Do not use diagonal or multi-axis simultaneous endpoint moves that would create an angled edge.

### Wide M4 polygon outside edges may not touch a routing track edge (M4.AUX.4)

M4.AUX.4 prohibits the horizontal outside edges of wide M4 polygons from coinciding with the horizontal routing track edges defined by minimum-width M4 neighbors. When widening an M4 polygon in y, its outer horizontal edges must not align with any minimum-width track edge in the same horizontal band.

### Vertical spacing minimum is 24 nm (M4.S.1), horizontal spacing minimum is 40 nm (M4.S.2)

When performing x-axis resize_end or move operations, the new polygon endpoints must maintain at least 40 nm horizontal separation from any neighboring M4 vertical edge (M4.S.2). The resize deltas in trial:i01.ug.leaf_0001.03 (+184 and +176 dbu) were large enough that M4.S.2 was not violated, and the gated_in outcome confirms clearance. A corrective trim of −4 dbu in trial:i02.ug.leaf_0001.00 was sufficient to achieve the final clean state, suggesting the iter-1 endpoint overshot by a small amount without crossing a spacing threshold.

### Tip-to-tip spacing on adjacent tracks is 40 nm (M4.S.3, M4.S.4)

M4.S.3 and M4.S.4 enforce 40 nm tip-to-tip spacing between M4 polygons on adjacent tracks. Endpoint extension (30 nm beyond the tip) is used by the DRC to catch tip proximity even without a shared run length. When adjusting x-endpoints, ensure the resulting tip is at least 40 nm from any opposing tip on the adjacent track.

### Parallel run length minimum is 44 nm (M4.S.5)

M4.S.5 requires that whenever two M4 polygons on adjacent tracks run parallel with a vertical gap ≤ 24 nm, the overlap (parallel run length) is at least 44 nm. This is relevant when x-axis resize operations change the length of an M4 segment: do not create a configuration where two adjacent-track M4 segments have a parallel run length greater than zero but less than 44 nm.

---

## Via Enclosure Rules and Via Shape Resizing

### V3.M4.EN.2 and V4.M4.EN.1 require ≥11 nm enclosure on at least two opposite sides

Both V3.M4.EN.2 and V4.M4.EN.1 require that the respective via is enclosed by M4 by at least 11 nm on at least two opposite sides. The cu_pool resize of VIA_VIA45_1_2_58_58's M4 via shape by +152 dbu in x (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01) produced a net reduction of 16 violations, which is consistent with the resize bringing M4 enclosure of V4 into compliance on the x-axis at multiple sites simultaneously. When planning x-axis M4 endpoint moves near V4 locations, the minimum x-enclosure margin of 11 nm must be preserved or restored.

### V3.M4.AUX.2 requires V3 width to match M4 width along the perpendicular direction

V3.M4.AUX.2 requires that V3 vias inside M4 have the same width as the M4 polygon along the direction perpendicular to M4's length, and must share at least two coincident edges with M4. Resize operations that change M4's vertical extent near V3 locations must also adjust V3 dimensions correspondingly, or ensure V3 remains exactly covered.

---

## Cross-Iteration Refinement Pattern

The history for p957 shows a two-step pattern: a large coarse adjustment in iteration 1 (trial:i01.ug.leaf_0001.03, +176 dbu on the low end) followed by a small corrective adjustment in iteration 2 (trial:i02.ug.leaf_0001.00, −4 dbu on the low end). Both gated in cleanly. This confirms that M4 endpoint repairs may require a sub-grid refinement pass in iteration 2 to reach the precise DRC-clean position after an initial coarse move.