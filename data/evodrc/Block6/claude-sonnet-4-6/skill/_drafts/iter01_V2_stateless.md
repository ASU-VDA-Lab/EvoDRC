## Repair Strategy: X-Axis Move-and-Resize on V2 Via Shapes

The single measured repair on this layer demonstrates that combined move-then-resize operations confined to the x-axis can resolve violations in a multi-shape via cell while preserving connectivity. In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, five x-axis operations were applied across three V2 shape indices inside cell `VIA_VIA23_1_3_36_36`: shape 0 was first moved −144 dbu then resized +264 dbu; shape 1 was resized +288 dbu (no move); shape 2 was moved +144 dbu then resized +264 dbu. The result was a net DRC reduction of 78 violations across two windows (unit:leaf_0019: −42, unit:leaf_0020: −36), with `conn_preserved: true` and `decision: applied`.

## Move-Before-Resize Ordering

In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, the move operation on shapes 0 and 2 preceded their resize operations within the same op sequence. This ordering is the form that was measured and accepted by the repair engine; both shapes required both a positional shift and an extent change along x to reach a valid state.

## Symmetric vs. Asymmetric Shape Adjustment

The three shapes in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 received different magnitudes: shapes 0 and 2 each got +264 dbu resize (with moves in opposite x-directions, −144 and +144 dbu respectively), while shape 1 received the largest resize (+288 dbu) with no move. This asymmetry across shape indices within the same cell is consistent with the repair satisfying width or enclosure constraints that differ per shape position relative to M2/M3 edges.

## Layer Co-Touch Requirement

Every operation in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 modified V2 shapes, and the touched-layers record includes M2, M3, and V2 together. Rules V2.M2.EN.1, V2.M3.EN.2, V2.AUX.1, and V2.M3.AUX.2 all constrain V2 geometry relative to M2 or M3 boundaries. A repair that adjusts V2 shapes must be evaluated against both enclosing metal layers simultaneously; the measured outcome confirms that modifying V2 alone (with the co-touched M2/M3 implicitly participating in enclosure checks) was sufficient to pass.

## Connectivity Preservation Under X-Only Ops

trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 confirms that x-axis move and resize operations on V2 via shapes, even when applied to multiple shape indices with differing magnitudes and directions, preserve inter-layer connectivity (`conn_preserved: true`). No y-axis operations were used in the successful repair, indicating that the violation set resolved here did not require adjustments along the y-axis.

## Via Cell with Multiple V2 Shapes

The target `def:VIA_VIA23_1_3_36_36` contains at least three V2 shape indices (0, 1, 2) that were individually adjusted in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00. Repairs in such multi-shape via cells must account for inter-shape spacing rules (V2.S.1 through V2.S.4) in addition to individual shape width (V2.W.1) and enclosure (V2.M2.EN.1, V2.M3.EN.2) rules. The 78-violation reduction achieved by adjusting all three shapes together, rather than any subset, is the only measured outcome for this cell type.

## DRC Violation Count as Repair Signal

In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, the before-counts were 139 (leaf_0019) and 154 (leaf_0020), reducing to 97 and 118 respectively. The repair did not fully eliminate violations in either window but was still `decision: applied`, indicating that partial violation reduction across a window is an accepted outcome in the cu_pool channel at iteration 1.