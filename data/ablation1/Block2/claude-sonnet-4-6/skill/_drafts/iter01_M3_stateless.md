## Via-Array Geometry Adjustments Targeting M3 Enclosure Violations

### Repair Pattern: Spreading and Resizing V2 Shapes in a 1×3 Via Array

In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, a five-operation repair applied to cell `VIA_VIA23_1_3_36_36` reduced 24 total M3-window violations (12 in `unit:leaf_0012`, 12 in `unit:leaf_0013`) and was accepted (`decision: applied`). The repair targeted three V2 shapes on the x-axis: outer shape 0 was translated −144 dbu, outer shape 2 was translated +144 dbu (spreading the outermost vias apart), and all three shapes (indices 0, 1, 2) were each resized +288 dbu along x. The touched-layers set was `[M2, M3, V2]`, confirming that the V2 geometry changes propagated into M3 (and M2) coverage. Connectivity was preserved (`conn_preserved: true`).

This is the only measured repair for M3 at iteration 1. All prescriptive claims below are grounded exclusively in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00.

### V2.M3.EN.2 and V2.M3.AUX.2 — Via Spread Corrects Enclosure Failures

Rules V2.M3.EN.2 (minimum M3 enclosure of V2 on two opposite sides ≥ 5 nm / 0 nm) and V2.M3.AUX.2 (V2 must match M3 width perpendicular to M3 length) both depend on the positional relationship between V2 edges and M3 edges. In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 the symmetric outward translation of the two outer V2 shapes (−144 dbu for shape 0, +144 dbu for shape 2) increased the span of the via footprint along x, while the uniform +288 dbu x-resize of all three V2 shapes widened each via individually. Together these moves brought V2 edges into a position that satisfies the enclosure and width-matching requirements imposed by M3 on both sides, eliminating violations in both affected leaf windows.

Do not move only the inner via (shape 1 in a 1×3 array) without also adjusting the outer vias; the repair in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 translated only the outer shapes and resized all three, suggesting that symmetric outer spread is the operative correction for enclosure failures across a multi-via row.

### Resize Direction and Axis Selection

In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 all resize operations used `axis: x`. The 1×3 via string `VIA_VIA23_1_3_36_36` is oriented along x (three vias in a row), and the violations appeared in two side-by-side leaf windows, consistent with a shortage of M3 metal extending along x beyond the via endpoints. Apply resize corrections along the axis of the via row, not transverse to it, when targeting enclosure shortfalls on the long sides of a multi-via array.

### M3 Width and Spacing Rules Implicated by Via Cell Edits

Because M3 shapes inside `VIA_VIA23_1_3_36_36` were listed in `touched_layers` and the repair was accepted without residual violations, the resulting M3 geometry after the five operations satisfied M3.W.1 (minimum width 18 nm), M3.S.1 (side-to-side spacing ≥ 18 nm when both edges > 36 nm), and M3.A.1 (area ≥ 504 nm²). The +288 dbu per-shape x-resize is sufficiently large that it did not create a new M3 width violation below 18 nm, and the spread of outer vias did not open an internal spacing gap below 18 nm between the M3 bars covering adjacent vias. Verify that any analogous repair keeps all intermediate M3 segments above the 18 nm width threshold and above the 18 nm side-to-side spacing threshold; trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 confirms this is achievable with the ±144 dbu translation plus +288 dbu resize combination.

### Multi-Window Yield from a Single Cell Repair

The single cell edit in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 simultaneously cleared violations in two distinct leaf windows (`unit:leaf_0012` and `unit:leaf_0013`), each contributing exactly 12 violations. When a via cell is instantiated or referenced across multiple layout windows, a repair applied at the cell definition level propagates to all instances; prioritize cell-level repairs over instance-level shape moves when the same violation pattern appears in multiple windows with equal counts, as seen in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00.

### Connectivity Preservation Constraint

Outward spreading of V2 shapes combined with resizing did not break connectivity in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 (`conn_preserved: true`). The operations kept each V2 shape inside its corresponding M3 landing pad (required by V2.M3.EN.2 and V2.M3.AUX.2) while enlarging the overlap region. Confirm connectivity after any via-spread repair: a translation that moves a via outside its enclosing M3 metal would satisfy neither enclosure rule nor connectivity.