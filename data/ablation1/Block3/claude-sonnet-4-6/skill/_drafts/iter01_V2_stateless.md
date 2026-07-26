## Repair Patterns and Outcomes

**Single applied trial available.** All claims in this file are grounded in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00. No superseded or conflicting records exist at iteration 1.

---

### Applied Operation Pattern: Symmetric x-axis Expand-and-Shift on Multi-Shape V2 Cells

The one applied repair in this layer's history operates exclusively on the x-axis, combining `move_via_shape` and `resize_via_shape` on all three V2 shapes within cell `VIA_VIA23_1_3_36_36` (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). The five-operation sequence is:

- shape_index 0: move x by -144 dbu, then resize x by +288 dbu
- shape_index 1: resize x by +288 dbu (no move)
- shape_index 2: move x by +144 dbu, then resize x by +288 dbu

This pattern is symmetric: shapes at the outer indices (0 and 2) are displaced outward from center (+/-144 dbu) while all three shapes are widened by the same amount (+288 dbu). The repair was accepted (`decision: applied`), preserved connectivity (`conn_preserved: true`), and reduced the total violation count by 27 across two leaf windows (leaf_0018: -15, leaf_0019: -12) (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

The repair touched M2, M3, and V2 simultaneously. Because V2.M3.AUX.2 requires V2 width to exactly match M3 width in the direction perpendicular to M3 length, and V2.AUX.1 requires V2 to remain inside both M2 and M3, any resize of V2 in x will only remain valid if M3 (and M2) are also adjusted to match—consistent with the multi-layer touch observed (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

### Rule-Specific Repair Guidance

**V2.W.1 (minimum width 18 nm along M3 length):** The resize operations expanding all V2 shapes by +288 dbu in x are the direction consistent with correcting a V2.W.1 violation, since x-axis width along the M3 length direction is what the rule checks. The repair produced a net violation reduction, confirming that widening undersized V2 shapes is an effective response (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

**V2.M3.AUX.2 (V2 width must exactly match M3 width perpendicular to M3 length):** Because M3 was among the touched layers and all V2 resize operations are x-axis, the repair maintains the exact-match constraint by co-adjusting M3 alongside V2. Do not resize V2 in x without also adjusting M3 (and verifying M2 enclosure per V2.M2.EN.1), as the single applied trial shows a coordinated three-layer touch is the successful strategy (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

**V2.AUX.1 (V2 must be inside M2 and M3):** The applied repair kept connectivity intact and touched M2 and M3, demonstrating that when V2 shapes are widened, M2 and M3 must be expanded concurrently to avoid V2.AUX.1 failures. A V2 resize that does not co-move M2 and M3 boundaries risks pushing V2 outside its enclosing metals (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

**V2.M2.EN.1 (M2 enclosure of V2 ≥ 5 nm on two opposite sides) and V2.M3.EN.2 (M3 enclosure of V2 ≥ 5 nm on two opposite sides):** The repair's simultaneous expansion of M2 and M3 alongside V2 is consistent with maintaining the required 5 nm enclosure margins. When widening V2, the enclosing metal must be widened by at least as much on each relevant side to avoid enclosure violations (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

**V2.S.1 / V2.S.2 / V2.S.3 / V2.S.4 (spacing rules):** The move operations on shapes 0 and 2 (outward displacement by ±144 dbu) increase spacing between adjacent V2 instances within the cell. The applied repair confirms that moving outer V2 shapes outward while expanding them is compatible with a net violation reduction; however, whether the moves resolved spacing violations specifically or were required to reposition the shapes relative to their M3 context cannot be isolated from this single trial (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

### Structural Observations on Cell VIA_VIA23_1_3_36_36

This cell contains at least three V2 shapes (indices 0, 1, 2). All are arranged along the x-axis and all were modified together in the single applied repair (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). Repairs that modify only a subset of shapes in this cell without adjusting the others may leave residual violations, since the symmetric pattern applied to all three shapes was what produced the net -27 outcome.

The `cu_pool` channel was used, and the locus `[1728, 2068, 11016, 10892]` localizes the defect region in Block3. Future repairs touching this cell or nearby instances in the same region should expect the same three-layer (M2, M3, V2) coordination requirement (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

### GEOMETRY.NONORTHOGONAL

All operations in the single applied trial are axis-aligned moves and resizes (x-axis only, on rectangular via shapes). No non-orthogonal geometry was introduced. All V2 shapes must remain orthogonal; the NONORTHOGONAL rule applies to every drawing layer including V2. The applied repair is consistent with this constraint (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).