## Repair Strategy by Channel

**cu_pool channel (via cell shape edits):** The single cu_pool repair in this layer's history targeted cell `VIA_VIA45_1_2_58_58` and operated directly on V4 shapes within that cell. The applied recipe combined symmetric lateral moves with bilateral resizes: shape_index 0 moved −116 dbu and shape_index 1 moved +116 dbu on the x-axis (spreading the two shapes apart), then both shapes were resized +384 dbu on the x-axis, and M4 shape_index 0 was resized +152 dbu on the same axis. This five-operation sequence reduced the violation count by 52 across the two affected windows (leaf_0019 −28, leaf_0020 −24) and preserved connectivity (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01). When a cu_pool trial targets a multi-shape via cell, apply spread-then-resize: separate the V4 shapes symmetrically before widening them, and accompany the V4 resize with a coordinated M4 resize to maintain enclosure compliance under V4.M4.EN.1.

**unit_gate channel (instance moves):** All three unit_gate trials resolved V4 violations exclusively through instance moves, without directly editing any V4 shape geometry. Instances were displaced in y by multiples of 24 dbu (observed deltas: ±24, ±48, ±72, ±96 dbu) in trial:i02.ug.leaf_0010.06 and trial:i03.ug.leaf_0002.01, and in x by multiples of 16 dbu (observed deltas: +32 and −16 dbu) in trial:i03.ug.leaf_0003.02. All three were accepted as gated_in with connectivity preserved. Use instance displacement — not direct shape edits — as the primary repair mechanism in the unit_gate channel.

## Move Granularity

Y-axis instance displacements observed across all unit_gate trials are strict multiples of 24 dbu: 24, 48, 72, and 96 dbu (trial:i02.ug.leaf_0010.06, trial:i03.ug.leaf_0002.01). X-axis instance displacements are multiples of 16 dbu: 16 and 32 dbu (trial:i03.ug.leaf_0003.02). Polygon moves on M4/M5/M6 in the x direction also used 16 and 32 dbu increments (trial:i03.ug.leaf_0003.02). Do not propose instance or polygon moves that are not multiples of these respective grid values; all accepted moves in this history align to them.

## Enclosure Rules: Coordinated Metal Resizing

V4.M4.EN.1 requires M4 to enclose V4 by ≥ 11 nm on at least two opposite sides; V4.M5.EN.2 requires the same from M5. In trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, the V4 resize (+384 dbu x-axis per shape) was paired with an M4 resize (+152 dbu x-axis). Resizing V4 without also extending the enclosing metal on the same axis risks introducing or worsening V4.M4.EN.1 or V4.M5.EN.2 violations. Always extend the relevant metal (M4 or M5) in the same axis direction when expanding V4 shape dimensions.

## Width and M5 Width-Match Constraint

V4.W.1 sets a 24 nm minimum width along the M5 length direction. V4.M5.AUX.2 additionally requires that V4 exactly match M5's width along the axis perpendicular to M5's length — V4 edges must be coincident with M5 edges on at least two sides for the via to be considered valid. The +384 dbu bilateral resize applied to both V4 shapes in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, combined with a simultaneous M4 extension, is consistent with bringing under-width V4 shapes into compliance with both V4.W.1 and V4.M5.AUX.2. When resizing V4 to fix width violations, the resize magnitude must bring the shape dimension to at least 24 nm, and the resulting V4 edges must align with M5 edges to satisfy V4.M5.AUX.2.

## Spacing Rules and Instance Spreading

V4.S.1, V4.S.2, and V4.S.3 all share a 33 nm threshold; S.1 and S.2 use projection, S.3 uses Euclidean corner-to-corner distance. Instance moves in y by up to ±96 dbu (trial:i02.ug.leaf_0010.06, trial:i03.ug.leaf_0002.01) and in x by ±32 dbu (trial:i03.ug.leaf_0003.02) resolved spacing violations while preserving connectivity. No case in this history required a move larger than 96 dbu to clear spacing violations. Moves of mixed sign within the same trial (some instances pushed positive, others negative) are used to spread groups that violate spacing between themselves rather than shifting the entire group in one direction, as seen in trial:i03.ug.leaf_0002.01 and trial:i03.ug.leaf_0003.02.

## Placement Legality (V4.AUX.1)

V4.AUX.1 requires every V4 shape to lie fully within the intersection of M4 and M5. The cu_pool repair in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 touched all three layers (M4, M5, V4) simultaneously, ensuring that both enclosing metals covered the resized V4 shapes. Avoid any operation that moves or resizes V4 shapes without verifying that the resulting V4 boundary remains inside both the M4 and M5 boundaries at that location.

## Connectivity Preservation Across All Accepted Trials

Every trial in this history — whether applied (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01) or gated_in (trial:i02.ug.leaf_0010.06, trial:i03.ug.leaf_0002.01, trial:i03.ug.leaf_0003.02) — reports conn_preserved: true. No trial was rejected due to connectivity loss. Proposals that cannot preserve connectivity are outside the pattern established by this history and should not be generated for V4 repairs.

## Multi-Layer Scope of Operations

V4 repairs consistently touch more than V4 alone. The cu_pool trial modified M4, M5, and V4 (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01). Unit_gate trials modified M3, M4, M5, V3, and V4 (trial:i02.ug.leaf_0010.06, trial:i03.ug.leaf_0002.01) or M4, M5, M6, V4, and V5 (trial:i03.ug.leaf_0003.02). V4 violations in this design do not occur in isolation from adjacent metal and via layers. Repairs that move instances propagate adjustments across the full stack of layers present in those instances; account for downstream effects on M3/V3 and M5/V5 neighbors when scoping V4 repairs.