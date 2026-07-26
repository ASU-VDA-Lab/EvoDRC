## Repair Strategy: X-Axis Move-and-Resize Pairs

The only recorded repair for V2 at iteration 1 applied a five-operation sequence to cell `VIA_VIA23_1_3_36_36`, all confined to the x-axis and all on layer V2, while also touching M2 and M3 (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). The pattern couples a `move_via_shape` with a subsequent `resize_via_shape` on the same shape index, which shifts one edge of the shape while extending the opposite edge, yielding a net width expansion without displacing the shape's center unilaterally. This produced a 27-violation reduction (delta_total = -27) across two windows and was accepted (decision: applied) with connectivity preserved.

The specific deltas were -144 dbu move followed by +288 dbu resize on shape_index 0, +288 dbu resize on shape_index 1 (no accompanying move), and +144 dbu move followed by +288 dbu resize on shape_index 2 (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). At the process grid where 1 dbu = 0.125 nm, 144 dbu = 18 nm and 288 dbu = 36 nm, directly matching the V2.W.1 minimum width of 18 nm and twice that value — consistent with repairs that bring undersized shapes into compliance.

When a move and resize appear together on the same shape, the effective edge displacement equals `delta_move + delta_resize` on the far side and `delta_move` on the near side. In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, shape_index 0 received a -144 dbu move (left) and +288 dbu resize (right expansion), producing a net rightward extension of +144 dbu at the right edge while the left edge moved -144 dbu — a symmetric widening of 18 nm on each side. Shape_index 2 received the mirror: +144 dbu move (right) and +288 dbu resize, consistent with a symmetric outward expansion.

## Enclosure Coupling: V2 Resizes Must Co-Move M2 and M3

V2.M2.EN.1 requires M2 to enclose V2 by at least 5 nm on two opposite sides. V2.M3.EN.2 requires M3 to enclose V2 by 5 & 5 nm or 5 & 0 nm on two opposite sides. V2.AUX.1 further requires V2 to remain fully inside both M2 and M3. Because trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 listed both M2 and M3 in `touched_layers` alongside V2, any x-axis resize of a V2 shape requires corresponding adjustment to the enclosing M2 and M3 geometry to maintain these enclosure constraints. Resizing V2 alone without co-adjusting the enclosing metals will create or worsen V2.M2.EN.1, V2.M3.EN.2, and V2.AUX.1 violations.

## Width Rule (V2.W.1) Is the Likely Primary Driver

V2.W.1 mandates a minimum V2 width of 18 nm along the M3 length direction (the x-axis in the context of trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). The repair deltas of ±144 dbu (= 18 nm) and 288 dbu (= 36 nm) on the x-axis directly correspond to this constraint. A shape that was undersized in x by 18 nm requires a 144 dbu bilateral expansion (72 dbu per side) or an asymmetric expansion of 144 dbu on one side — both of which match the observed delta pattern in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00.

## Width Rule Perpendicular to M3 (V2.M3.AUX.2) Constrains Y-Axis

V2.M3.AUX.2 requires that V2 exactly match M3's width in the direction perpendicular to M3's length. No y-axis operations appeared in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00; all five ops were x-axis only. This is consistent with V2.M3.AUX.2 being a hard constraint that prevents free resizing in the y-axis: the V2 y-extent is locked to M3's y-extent, so y-axis adjustments to V2 require equal adjustments to M3 and cannot be made independently.

## Spacing Rules Govern Inter-Via Clearances After Resizing

V2.S.1 through V2.S.4 establish projection- and euclidean-based spacing requirements that interact through the v2_mask construction, which extends V2 shapes by 5 nm along M3 edges (the end-cap region). After an x-axis resize, the effective mask footprint grows, which can create or resolve V2.S.1 (17 nm or 18 nm projection spacing), V2.S.2 (16.4 nm euclidean for both-with-end-cap pairs), V2.S.3 (16.12 nm euclidean for both-without-end-cap pairs), and V2.S.4 (17.11 nm euclidean for mixed pairs). The 27-violation reduction in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 across windows leaf_0018 and leaf_0019 is consistent with simultaneous resolution of width and spacing violations in a local cluster, since widening underfilled vias can simultaneously satisfy V2.W.1 while repositioning mask edges that were too close to neighbors.

## Non-Orthogonal Geometry Prohibition

The NONORTHOGONAL block applies to V2. All five operations in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 are axis-aligned (x-only moves and resizes), producing only 0° and 90° edges. Any repair must restrict V2 shape deltas to axis-aligned operations; diagonal or off-grid moves will trigger GEOMETRY.NONORTHOGONAL violations.

## Observed Operation Sequencing

In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, the five operations were ordered: move(shape_0), resize(shape_0), resize(shape_1), move(shape_2), resize(shape_2). Each shape received its own move-resize sub-sequence before the next shape was touched. This per-shape sequencing (move then resize on the same index before advancing to the next index) is the only ordering directly observed in the history.