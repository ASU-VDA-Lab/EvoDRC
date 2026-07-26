**Effective repair: x-axis move and resize of V2 shapes in the VIA_VIA23_1_3_36_36 cell**

The single largest measured DRC reduction on layer V2 came from simultaneously moving and resizing multiple V2 shapes along the x-axis within cell VIA_VIA23_1_3_36_36 (trial:i05.cu.def:VIA_VIA23_1_3_36_36.00, delta_total -51, leaf_0001: 74→38, leaf_0002: 29→14). The applied operation set consisted of three move_via_shape steps (delta_dbu -144, +144) bracketing three resize_via_shape steps (each delta_dbu +288) on shape indices 0, 1, and 2. All operations acted on the V2 layer along the x-axis within the same def target. Do not attempt single-shape edits in isolation on this cell; the coordinated multi-shape pattern across all three shape indices is what produced the net reduction (trial:i05.cu.def:VIA_VIA23_1_3_36_36.00).

**Ineffective repair: y-axis M3 resize does not resolve V2 violations**

Shrinking the M3 shape inside VIA_VIA23_1_3_36_36 along the y-axis by 40 dbu (resize_via_shape, layer M3, delta_dbu -40) produced zero net change in V2 DRC count and was rejected as net_positive (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, delta_total 0, both windows unchanged). Do not use y-axis M3 resizing as a primary repair action for V2 violations in this cell.

**Rule V2.M3.AUX.2 and V2.M3.EN.2: x-axis sizing governs M3 width match**

Rule V2.M3.AUX.2 requires V2 to exactly match M3 width in the direction perpendicular to the M3 length. Rule V2.M3.EN.2 requires M3 to enclose V2 by 5 nm on two opposite sides (5&5 nm or 5&0 nm). The successful repair (trial:i05.cu.def:VIA_VIA23_1_3_36_36.00) achieved its DRC reduction through x-axis moves and resizes on V2 shapes, consistent with correcting alignment and sizing relationships between V2 and the underlying M3 track. y-axis adjustments on M3 (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00) did not address these constraints.

**Rule V2.AUX.1: V2 must remain inside both M2 and M3**

All three recorded trials preserved connectivity (conn_preserved: true). The applied x-axis moves and resizes in trial:i05.cu.def:VIA_VIA23_1_3_36_36.00 touched M2, M3, and V2 together; always include the enclosing metal layers in the operation scope when repositioning V2 shapes to avoid introducing V2.AUX.1 violations.

**Rule V2.M2.EN.1: M2 enclosure constraint**

V2.M2.EN.1 requires M2 to enclose V2 by at least 5 nm on at least two opposite sides. The repair in trial:i05.cu.def:VIA_VIA23_1_3_36_36.00 applied symmetric x-axis moves (-144 dbu on one side, +144 dbu on the opposite side) and uniform positive resizes (+288 dbu per shape), keeping the V2 shapes centered relative to M2. Use symmetric move-and-expand patterns on V2 along x to avoid creating asymmetric enclosure deficits under V2.M2.EN.1.

**Rule V2.W.1: minimum width 18 nm**

V2.W.1 requires a minimum V2 width of 18 nm along the M3 length direction. The resize operations in trial:i05.cu.def:VIA_VIA23_1_3_36_36.00 expanded V2 shapes by +288 dbu each along x, which increases rather than decreases width. Avoid shrinking V2 shapes below 18 nm; when a repair requires lateral repositioning, apply a compensating resize to maintain or increase width.

**Rule V2.S.1 and spacing context**

V2.S.1 enforces minimum spacing of 18 nm (same M3 track or aligned parallel tracks) or 27 nm (non-aligned parallel tracks). The gated trial (trial:i02.ug.leaf_0003.02) introduced two new V2-touching violations within crop without eliminating any outside crop and was gated for further evaluation rather than immediately applied; instance moves on adjacent cells can shift V2 spacing relationships and generate new spacing violations. When instance moves touch V2 indirectly, verify spacing after each step before committing.