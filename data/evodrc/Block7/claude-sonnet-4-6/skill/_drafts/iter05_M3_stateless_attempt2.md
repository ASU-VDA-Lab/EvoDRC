## V2.M3.AUX.2: Dominant Active Violation and Combo-Fix Pattern

V2.M3.AUX.2 requires every V2 via to be exactly the same width as M3 in the direction perpendicular to the M3 run. A combined edit of 72 M3 stub `resize_end` operations (y-axis) paired with one `resize_via_shape` shrink of -40 dbu on the VIA_VIA23_1_3_36_36 M3 landing shape cleared all 72 violations, confirmed by full-deck KLayout DRC (356 -> 284, delta -72 on V2.M3.AUX.2) (trial:i04.cu.def:VIA_VIA23_1_3_36_36.01).

Do not apply the M3 stub `resize_end` operations without also applying the VIA_VIA23_1_3_36_36 M3 land `resize_via_shape`. When the same 72 stub resizes were submitted without the via land shrink (the `resize_via_shape` op was dropped by the assembler, reason `cu_pool:rejected_net_positive`), 81 new V2.M3.AUX.2 violations appeared in-crop (trial:i05.ug.leaf_0006.05).

## VIA_VIA23_1_3_36_36 M3 Land: Standalone Shrink Rejected

Applying only the `resize_via_shape` of -40 dbu on y to VIA_VIA23_1_3_36_36 without the M3 stub resizes was rejected_net_positive: it increased the DRC count by +64 (unit:leaf_0006 window delta +64) (trial:i05.cu.def:VIA_VIA23_1_3_36_36.00). The identical operation was accepted when bundled with the full 72 stub resizes in the cu_pool channel (trial:i04.cu.def:VIA_VIA23_1_3_36_36.01). Always submit the via land shrink as part of the combo, not as a standalone op.

## M3 Stub resize_end Pattern for V2.M3.AUX.2

Apply `resize_end` on both the low and high y-ends of each M3 stub polygon. The most common symmetric delta is -32 dbu on both ends; a subset of stubs (p2629, p2380, p2784, p2928, p2896, p2795, p2929, p2816) receive -32 dbu low and -41 dbu high (trial:i04.cu.def:VIA_VIA23_1_3_36_36.01). After these resizes, no M3.W.1 or M3.A.1 violation was introduced in that trial, confirming the shrunk stubs remain above the 18 nm minimum width and 504 nm^2 minimum area thresholds.

## Block-Scope Combo Edits: Use cu_pool, Not unit_gate

The same 73-operation batch (72 stub resizes plus via land shrink) was first submitted via unit_gate and rejected with decision `gated_out`, reason `empty_or_missing_patch`; locus was null (trial:i04.ug.leaf_0008.07). The identical op set succeeded when submitted through cu_pool with explicit target `def:VIA_VIA23_1_3_36_36` (trial:i04.cu.def:VIA_VIA23_1_3_36_36.01). Move edits that span multiple units and target a cell definition must be routed through cu_pool, not unit_gate (trial:i04.ug.leaf_0008.07, trial:i04.cu.def:VIA_VIA23_1_3_36_36.01).

## Instance and Polygon Moves for M3 Spacing Corrections

Small incremental moves on M3-touching polygons and co-located instances are consistently accepted via unit_gate with conn_preserved. Move a M3 polygon and its associated via instances together as a unit: co-moving polygon p3383 and instance i1643 by -57 dbu on y was accepted (trial:i02.ug.leaf_0001.07); moving the same polygon and instance by +21 dbu on y was also accepted (trial:i03.ug.leaf_0001.03). Move polygon p3515 by -12 dbu on y together with instances i0519 and i0524 was accepted (trial:i02.ug.leaf_0014.08). Move polygon p2916 by +8 dbu on x with instances i2005 and i1790 was accepted (trial:i04.ug.leaf_0002.01); the same polygon moved by -8 dbu on x with the same instances was accepted at iter 5 (trial:i05.ug.leaf_0001.00). Move polygon p2877 by +8 dbu on x with instances i1706 and i1738 was accepted (trial:i04.ug.leaf_0003.02).

## resize_end on Individual M3 Segments (Non-AUX.2 Context)

Resize the high y-end of M3 polygon p3537 by +48 dbu and the high y-end of p2432 by +68 dbu in a single unit crop: both were accepted with conn_preserved (trial:i01.ug.leaf_0095.26). Resize the high y-end of p3537 by -48 dbu: accepted (trial:i03.ug.leaf_0011.07). These per-segment resizes in single-unit crops do not require the cu_pool channel.

Resize the low x-end of M3 polygon p3300 by -88 dbu paired with instance moves of +68 dbu and +172 dbu on x and an add_polygon: the combined op was accepted with conn_preserved (trial:i03.ug.leaf_0002.04).

## add_polygon on M3

A new M3 polygon added at [[11664,11756],[11664,11828],[11908,11828],[11908,11756]] (244 dbu wide x 72 dbu tall, area 17568 dbu^2) satisfied M3.W.1 (min 18 nm) and M3.A.1 (min 504 nm^2) and was accepted as part of a multi-op unit_gate trial (trial:i03.ug.leaf_0002.04). All edges of that polygon are axis-aligned, satisfying the NONORTHOGONAL block constraint.