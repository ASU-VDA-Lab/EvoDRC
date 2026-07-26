**Via-cell enclosure repair (V4.M4.EN.1)**

Resizing the M5 shape within via-cell definitions that list M4 and V4 in `touched_layers` is a confirmed repair path for enclosure violations affecting M4. Trial i01.cu.def:VIA_VIA45_1_2_58_58.00 targeted cell VIA_VIA45_1_2_58_58 through the cu_pool channel and applied a single op: y-axis resize of −88 dbu on the M5 shape (shape_index 0). This reduced the whole-design violation count by 56 with no connectivity loss. Do not edit M4 geometry directly when the defect originates in the via-cell definition; the M5-shape resize alone was sufficient in trial i01.cu.def:VIA_VIA45_1_2_58_58.00.

**Y-end resize increments must respect the M4.AUX.1 grid**

In trial i02.ug.whole_design.00, y-axis resize_end operations applied to polygons co-edited alongside M4 used deltas of +24 dbu (polygons p1831 low-end, p1806 high-end) and +72 dbu (polygon p1786 high-end). Both 24 dbu and 72 dbu are exact multiples of 24 dbu, the horizontal-edge grid required by M4.AUX.1. Apply y-end resize deltas only in multiples of 24 dbu when M4 geometry is among the touched layers; non-multiples produce off-grid horizontal edges that violate M4.AUX.1.

The +72 dbu delta (trial i02.ug.whole_design.00) also equals three minimum-width units (3 × 24 nm). Three is an odd multiple, which is consistent with M4.W.3 (even-integer multiples of 24 nm are forbidden as vertical widths). When choosing a y-end resize increment, avoid deltas that would bring any M4 polygon's vertical extent to an even-integer multiple of 24 nm (48, 96, 144, 192, 240, 288, 336, 384, 432, 480 nm) or to any of the M4.W.4-prohibited values (72, 168, 264, 360, 456 nm).

**Global instance-placement pass: dominant op type and displacement values**

A whole-design global repair that touches M4, M3, M5, M6, V3, V4, and V5 operates primarily through move_instance operations, not direct polygon edits. Trial i02.ug.whole_design.00 issued 69 ops, the large majority of which were move_instance calls. The x-displacements used were drawn from {−16, 0, +32} dbu; y-displacements spanned {−72, −64, −48, −24, −16, 0, +16, +24, +32, +48, +72, +96} dbu. Direct polygon-level ops (polygon moves and resize_end calls) were a small minority of the total op count in that same trial.

**Unit-gate acceptance criterion: conn_preserved takes priority over per-rule delta**

Trial i02.ug.whole_design.00 was accepted (decision: gated_in) through the unit_gate channel even though the repair introduced 10 new V2.M3.EN.2 violations. Acceptance was granted because conn_preserved was true. The unit_gate channel does not require a zero or negative net violation delta across all rules when connectivity is intact; the binding gate criterion observed is conn_preserved, not per-rule neutrality. A repair touching M4 that produces new violations in neighboring-layer enclosure rules (e.g., V2.M3.EN.2) is still committable through unit_gate provided no connections are broken.

**Assemble-stage drops do not block M4 repairs in cu_pool**

Trial i02.ug.whole_design.00 recorded several assemble_drops for V2 via ops that were skipped because they had already been applied through cu_pool (reason: "cu_pool:applied"). This indicates that cu_pool repairs—including those touching M4 such as trial i01.cu.def:VIA_VIA45_1_2_58_58.00—are committed before the unit_gate global pass assembles, and the global pass must skip re-applying those same ops. Verify that any M4-touching via-cell fix dispatched through cu_pool has already been applied before issuing the same op again through a subsequent global pass, to avoid assemble_drops.