## Grid and Track Alignment

M6.AUX.1 requires horizontal edges to fall on the 32 nm grid; M6.AUX.2 requires minimum-width M6 tracks (those not surviving `m6.sized(0,-17.nm).sized(0,17.nm)`) to have their centerlines satisfy `(cl − 64) % 256 == 0` in dbu, restricted to polygons whose bottom and top are both multiples of 128 dbu. In trial:i01.ug.whole_design.00 (iter 1), all six M6 polygon violations were resolved with pure y-axis translations: p3806 and p3801 moved −64 dbu, p3804 moved −32 dbu, p3802 moved −16 dbu, p3805 moved +16 dbu, and p3803 moved +32 dbu. Every cell instance touching those polygons (V5 and M5 hierarchy) received the identical y-delta in the same operation group ("m6_snap"), preserving enclosure relationships with no new in-crop or out-of-crop violations.

Move increments observed for y-axis snapping are 16, 32, and 64 dbu (trial:i01.ug.whole_design.00). These are sub-multiples of the 256 dbu routing pitch specified by M6.AUX.2, confirming that corrections need not be full-pitch jumps; the smallest step resolving the offgrid condition is sufficient.

## Horizontal Spacing and Width Correction

M6.S.2 requires ≥ 40 nm horizontal spacing; M6.W.5 requires ≥ 44 nm horizontal width; M6.S.3 and M6.S.4 each require ≥ 40 nm tip-to-tip spacing on adjacent tracks; M6.S.5 requires ≥ 44 nm parallel run length on adjacent tracks. In trial:i04.ug.whole_design.00 (iter 4), M6 polygons received x-axis translations: p2213 and p2216 moved +32 dbu, p2212 and p2215 moved −16 dbu, p2211 and p2214 moved −64 dbu. Paired polygons within each group moved by the same delta, preserving intra-pair spacing while shifting relative to neighboring shapes.

The iter 4 operation also repositioned 156 cell instances with x and y components, spanning M3–M6 and V3–V5. The trial was gated in with conn_preserved=true and zero new DRC violations (trial:i04.ug.whole_design.00). This establishes that cross-layer instance repositioning combined with direct M6 polygon x-moves is a valid and connectivity-safe strategy for resolving horizontal M6 rule violations.

Move increments for x-axis correction also used 16, 32, and 64 dbu steps (trial:i04.ug.whole_design.00), consistent with those used in y-axis corrections.

## Coupled Polygon-and-Instance Move Strategy

In both accepted trials, every M6 polygon move was accompanied by moves of all cell instances whose geometry depends on that polygon (via or higher-metal instances), using the same displacement vector. This pattern produced conn_preserved=true in trial:i01.ug.whole_design.00 and trial:i04.ug.whole_design.00. Applying a polygon translation without moving dependent instances risks introducing new enclosure violations under V5.M6.EN.2 (≥ 11 nm enclosure of V5 by M6 on two opposite sides) and V6.M6.EN.1 (≥ 11 nm enclosure of V6 by M6 on two opposite sides).

## Via Enclosure Under Translation

V5.M6.EN.2 is satisfied when M6 encloses V5 by ≥ 11 nm on two opposite sides; V5.M6.AUX.2 additionally requires V5 to be exactly as wide as M6 perpendicular to the M6 length direction, verified by two coincident edges. In trial:i01.ug.whole_design.00, the group move of M6 polygons and their V5/M5 instances by equal y-deltas preserved both rules without any separate resize or enclosure-grow step. No trial records a standalone enclosure-increase operation on M6; all enclosure compliance was maintained through the coupled translation approach.

## Forbidden Vertical Width Values

M6.W.3 forbids vertical widths that are even integer multiples of 32 nm: 64, 128, 192, 256, 320, 384, 448, 512, 576, 640 nm. M6.W.4 forbids vertical widths of 96, 224, 352, 480, and 608 nm. Neither trial records any vertical-resize operation on M6 polygons; all M6 ops in both trials are pure translations. No width violation was triggered or repaired by translation alone in the recorded history. Vertical resizes for W.3 or W.4 violations have no measured precedent in this history and must avoid landing on any of the values above.

## No-Bend and Orthogonality Constraints

M6.AUX.3 forbids bends (corners with included angle 0–90°). The NONORTHOGONAL block forbids any non-axis-aligned edge. No reshape or corner-removal operation appears in either trial. Both trials operated exclusively with whole-polygon translations. Any repair of a bend or nonorthogonal edge would require polygon reshaping, for which no measured approach exists in this history.

## Connectivity-Safe Operation Scope

Both trials used the "m6_snap" operation group label (trial:i01.ug.whole_design.00) or equivalent grouped x-axis moves (trial:i04.ug.whole_design.00) and produced conn_preserved=true with n_new_in_crop=0 and n_new_out_of_crop=0 in a design locus covering the full 30440 × 30440 dbu block. The only operation types observed are "move" (single polygon, single axis) and "move_instance". No merges, splits, insertions, or deletions of M6 polygons appear in any accepted trial.