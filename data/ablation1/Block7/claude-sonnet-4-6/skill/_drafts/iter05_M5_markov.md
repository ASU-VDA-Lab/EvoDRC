## Repair Approach for M5-Related Violations

M5 violations are resolved from the via side rather than by directly modifying M5 routing-track geometry. In both measured repairs, the engine touched via shapes (V4 or V5) and the overlapping metal shape (M5 or M6) inside the via cell definition, leaving M5 routing tracks unchanged (trial:i02.cu.def:VIA_VIA56_2_2_66_58.01, trial:i05.cu.def:VIA_VIA45_1_2_58_58.00). Via cell repairs affecting M5 enclosure rules are localized; each via cell definition must be repaired independently, and a fix to one cell type does not extend to other variants (trial:i02.cu.def:VIA_VIA56_2_2_66_58.01, trial:i05.cu.def:VIA_VIA45_1_2_58_58.00).

## Symmetric Via Shape Expansion With Coordinated Metal Resize

Two distinct via cell types have been repaired using the same structural pattern: move each via shape outward symmetrically along a single axis, apply an equal positive resize to both shapes along that axis, and then apply a negative resize to the coincident metal shape along the same axis.

For VIA_VIA56_2_2_66_58 (y-axis), V5 shapes 0 and 1 were moved −132 dbu and +132 dbu respectively, both resized +128 dbu in y, and the M6 shape was resized −384 dbu in y (trial:i02.cu.def:VIA_VIA56_2_2_66_58.01).

For VIA_VIA45_1_2_58_58 (x-axis), V4 shapes 0 and 1 were moved −116 dbu and +116 dbu respectively, both resized +232 dbu in x, and the M5 shape (index 0) was resized −152 dbu in x (trial:i05.cu.def:VIA_VIA45_1_2_58_58.00).

In both cases the move magnitude equals half the resize magnitude for each via shape, preserving the outer edge position while extending the inner edge toward center. Never move only one end of a symmetric via array without applying the matching resize; the unmoved end will produce a new enclosure violation on the opposite side (trial:i02.cu.def:VIA_VIA56_2_2_66_58.01).

## M5 X-Axis Resize Coordinated With V4 Moves

In VIA_VIA45_1_2_58_58, the M5 shape (index 0) was resized −152 dbu in x in the same operation batch as the V4 x-axis moves. This coordinated contraction is required: if M5 retains its pre-repair x-extent after the V4 shapes are repositioned, V4.M5.AUX.2 or V4.M5.EN.2 violations can be introduced on the side that the via shapes moved toward. Apply the M5 x-axis resize in the same batch as the V4 moves (trial:i05.cu.def:VIA_VIA45_1_2_58_58.00).

## V5 Shape Adjustments That Resolved M5 Enclosure Errors

In VIA_VIA56_2_2_66_58, four V5 shapes were adjusted in two symmetric pairs along the y-axis. The opposing-direction moves with same-sign resize produced a net spread of the two outer V5 shapes away from center while the inner shapes contracted toward it, bringing all four shapes into compliance with the 11 nm two-opposite-sides enclosure requirement of V5.M5.EN.1. The M6 shape was resized −384 dbu in y concurrently (trial:i02.cu.def:VIA_VIA56_2_2_66_58.01).

## Violation Count and Window Distribution

The iteration-5 repair of VIA_VIA45_1_2_58_58 reduced violations by 158 in 5 operations, distributed across leaf_0013 (−81), leaf_0014 (−75), and leaf_0002 (−2). Residual counts after repair were 324 in leaf_0013 and 311 in leaf_0014; these windows remain dominant sources of M5-affecting violations and require further iteration (trial:i05.cu.def:VIA_VIA45_1_2_58_58.00).

The iteration-2 repair of VIA_VIA56_2_2_66_58 reduced violations by 39, with the bulk in leaf_0045 (−18) and leaf_0046 (−18), which retained 408 and 377 residual violations respectively after that pass (trial:i02.cu.def:VIA_VIA56_2_2_66_58.01). Both sets of high-count windows require continued iteration.

## Connectivity Preservation

Both measured repairs preserved all connections (conn_preserved: true). Symmetric axis-aligned repositioning of via shapes without altering the orthogonal extent or the M5 routing-track geometry does not break net connectivity for M5 routes in the repaired via cell types (trial:i02.cu.def:VIA_VIA56_2_2_66_58.01, trial:i05.cu.def:VIA_VIA45_1_2_58_58.00).

## Locus and Scope

Both repairs operated within the same bounding box [1728, 2068, 28728, 28172] (x_lo, y_lo, x_hi, y_hi in dbu), confirming that this locus encompasses the active repair region for M5-affecting via cell work across iterations (trial:i02.cu.def:VIA_VIA56_2_2_66_58.01, trial:i05.cu.def:VIA_VIA45_1_2_58_58.00).