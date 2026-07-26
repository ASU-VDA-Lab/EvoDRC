## V2 Co-Movement Constraint with M3

V2 must remain inside M2 ∩ M3 at all times (V2.AUX.1) and must match the M3 width perpendicular to the M3 length direction (V2.M3.AUX.2). Every successful repair that touched V2 achieved this by co-moving the V2-containing instance and its associated M3 polygon by an identical delta in the same operation. In trial:i02.ug.leaf_0001.07, instance i1643 and polygon p3383 were both moved [0, -57] in the same op-set, touching only the {M2, M3, V2} layer set. In trial:i03.ug.leaf_0001.03 the same pair (i1643, p3383) were moved [0, +21] together. Decoupling the V2 instance move from its M3 polygon move would violate V2.AUX.1 or V2.M3.AUX.2; no trial in the history does so.

## Minimal Layer Set for Pure V2 Repairs

When the violation involves only M2/M3/V2 interconnection and no M1 or V1 geometry, the repair can be confined to {M2, M3, V2} with no lateral fan-out to other layers. Both trial:i02.ug.leaf_0001.07 and trial:i03.ug.leaf_0001.03 report `"touched_layers":["M2","M3","V2"]` and each accepted with zero new violations (or with conn_preserved overriding the in-crop count). Repairs that also touch M1/V1 used 5–6 ops across the fuller layer set (trial:i01.ug.Block7_union_row16.06, trial:i02.ug.leaf_0014.08, trial:i03.ug.leaf_0011.07) but still kept V2-associated moves co-planar and co-delta with their M3 partners.

## Y-Axis Translation as the Primary Repair Motion for V2

In every trial where the layer set is {M2, M3, V2}, the repair is a pure y-axis translation applied identically to the instance and its M3 polygon. trial:i02.ug.leaf_0001.07 applies delta_dbu [0, -57] to both i1643 and p3383; trial:i03.ug.leaf_0001.03 applies [0, +21] to the same pair. No x-axis component appears in either. X-axis moves do occur but only in multi-layer repairs where M1/V1 are also involved (trial:i01.ug.Block7_union_row16.06 uses [-36, 0] and [+36, 0] on separate instances; trial:i03.ug.leaf_0002.04 uses [+68, 0] and [+172, 0]).

## M3 End-Cap Extension to Satisfy V2.M3.EN.2 and Spacing Classification

V2.M3.EN.2 requires M3 to enclose V2 by 5 nm on two opposite sides. The spacing rules V2.S.1–V2.S.4 apply different thresholds depending on whether a V2 instance has a 5 nm M3 end-cap (wec, with-end-cap) or is fully flush with M3 (nec, no-end-cap). Extending the M3 high end using `resize_end` is a validated repair move. trial:i01.ug.leaf_0095.26 extends polygon p2432 y-high by +68 dbu and p3537 y-high by +48 dbu alongside V2 instance moves, and is accepted with zero new violations. trial:i03.ug.leaf_0011.07 reverses p3537's high-end extension by -48 dbu and is also accepted with zero new violations, demonstrating that both extending and contracting the M3 end-cap can clear violations depending on the spatial context.

## Adding New M3 Polygons to Provide V2 Coverage

When no existing M3 geometry can be resized to cover a V2 instance while satisfying V2.M3.EN.2, adding a new M3 polygon is a valid repair. trial:i03.ug.leaf_0002.04 adds an M3 rectangle at points [[11664,11756],[11664,11828],[11908,11828],[11908,11756]] alongside instance moves and a polygon resize, and is accepted with zero new violations. This operation co-occurs with an x-direction resize of p3300 (x-low end by -88 dbu) and a y-direction resize of p2720 (y-high end by +20 dbu), confirming that new-polygon addition is used in conjunction with geometry adjustments rather than in isolation.

## Incremental Refinement Across Iterations on the Same Unit

The same unit, polygon, and instance can undergo multiple repair passes across iterations. Polygon p3383 and instance i1643 in unit leaf_0001 were moved [0, -57] in iter 2 (trial:i02.ug.leaf_0001.07) and then partially reversed by [0, +21] in iter 3 (trial:i03.ug.leaf_0001.03), yielding a net displacement of [0, -36] from the pre-iter-2 state. The iter-3 move introduced `n_new_in_crop: 3` but was still accepted because `conn_preserved: true`. This establishes that the gating criterion prioritizes connectivity preservation over zero new in-crop violations: a repair that introduces new in-crop DRC markers is accepted as long as it does not break connectivity.

## V2.M2.EN.1: M2 Opposite-Side Enclosure Must Be Maintained Through Moves

V2.M2.EN.1 requires M2 to enclose V2 by at least 5 nm on at least two opposite sides. Every repair that co-moves a V2 instance also implicitly moves M2 geometry (since M2/M3/V2 are always co-listed in `touched_layers` when V2 is present). No trial applies a delta to a V2 instance without M2 also appearing in `touched_layers`, consistent with the enclosure constraint being jointly maintained. Direct M2 geometry resizes are not visible as explicit polygon ops in the history, but M2 is always part of the touched set, implying M2 moves with the instance hierarchy rather than requiring standalone polygon edits.

## Orthogonality: All V2 Repair Operations Preserve Axis-Aligned Geometry

The GEOMETRY.NONORTHOGONAL rule prohibits any edge with angle outside {0°, 90°, 180°, 270°}. All repair operations in the history use rectilinear moves (`delta_dbu` with one zero component or both non-zero but applied to instance-level moves that preserve orthogonality), rectilinear polygon end-resizes, and a new M3 polygon defined by four axis-aligned corners (trial:i03.ug.leaf_0002.04). No diagonal move or non-orthogonal polygon is introduced in any trial.

## V2.W.1: Width Along M3 Length is Enforced via Instance Sizing, Not Polygon Edit

V2.W.1 requires 18 nm minimum width along the M3 length direction. No trial applies a `resize_end` directly to a V2 polygon; all width-related geometry is controlled through the instance cell dimensions. Resizing ops in the history target M3 polygons (p2432, p2720, p3300, p3537), never a V2 polygon directly. This means V2 width is fixed by the instantiated cell geometry and is not modified by the repair engine; spacing and position fixes are applied by moving or adding M3 and by relocating V2-carrying instances.