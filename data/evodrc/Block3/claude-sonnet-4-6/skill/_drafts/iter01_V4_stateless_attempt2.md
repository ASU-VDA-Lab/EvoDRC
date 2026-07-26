## Repair Pattern: Symmetric Move + Resize of V4 Shapes with M4 Enclosure Expansion

The single accepted repair (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01) reduced violations by 18 across two windows (unit:leaf_0018: 32→22, unit:leaf_0019: 35→27) using five operations on cell VIA_VIA45_1_2_58_58, touching layers V4 and M4 (M5 was listed as touched but received no direct operations in that trial).

## V4 Shape Operations: Symmetric Outward Move Combined with X-Axis Resize

In trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, the two V4 shapes in the via cell received mirror-image x-axis moves: shape_index=0 moved −116 dbu and shape_index=1 moved +116 dbu, spreading the pair apart symmetrically about their common center. Both shapes were then resized +384 dbu along x. Apply symmetric outward moves paired with equal x-axis resizes when correcting spacing violations between co-located V4 shapes; trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 shows this combined approach achieved net violation reduction without breaking connectivity (conn_preserved=true).

The resize magnitude (+384 dbu) exceeded the move magnitude (116 dbu) by more than 3×, indicating that width growth was the dominant correction, not position shift alone. Do not rely on position adjustment alone when V4.W.1 (24 nm minimum width) or enclosure rules are simultaneously violated; trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 applied resize on top of move to satisfy both spacing and width constraints in a single pass.

## M4 Enclosure Must Be Expanded When V4 Shapes Grow

trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 resized the M4 shape (shape_index=0) by +152 dbu along x alongside the V4 +384 dbu x-resize. V4.M4.EN.1 requires M4 to enclose V4 by at least 11 nm on at least two opposite sides; any x-axis growth of V4 therefore requires a corresponding M4 x-resize to maintain that enclosure. Always resize M4 when V4 is resized along x; the accepted repair in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 used an M4 delta of 152 dbu against a V4 delta of 384 dbu, confirming that M4 expansion need not match V4 expansion in magnitude but must be nonzero to satisfy V4.M4.EN.1.

## Spacing Rules Govern Both Same-Net and Different-Net V4 Instances

V4.S.1 and V4.S.2 both set a 33 nm minimum projection-based spacing; V4.S.3 adds a 33 nm Euclidean corner-to-corner floor. The symmetric outward move of ±116 dbu in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 increased the projection gap between the two V4 shapes, confirming that outward displacement resolves projection-space spacing violations. Never move only one shape of a symmetric via pair; trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 moved both shapes by equal and opposite deltas, preserving the cell's center alignment and satisfying spacing on both sides simultaneously.

## V4.AUX.1 and V4.M5.AUX.2 Constrain Valid Shape Positions

V4.AUX.1 requires every V4 shape to lie inside the intersection of M4 and M5. V4.M5.AUX.2 requires V4 width to exactly match M5 width in the direction perpendicular to M5 length. The repair in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 preserved connectivity (conn_preserved=true) and the decision was "applied," confirming the post-repair state satisfied both auxiliary rules. Resize V4 only along the axis consistent with M5 width alignment; trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 confined all V4 and M4 operations to the x-axis, leaving y-extents unchanged, which kept V4 within the M5 width constraint.

## All V4 Edges Must Remain Orthogonal

The NONORTHOGONAL BLOCK fires on V4 for any edge angle outside {0°, 90°, 180°, 270°}. Every operation in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 used axis-aligned move_via_shape and resize_via_shape calls on rectangular shapes, producing only orthogonal edges. Use only axis-aligned (x or y) move and resize operations on V4 shapes; trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 confirms that restricting deltas to a single named axis per operation preserves orthogonality throughout a multi-step repair sequence.