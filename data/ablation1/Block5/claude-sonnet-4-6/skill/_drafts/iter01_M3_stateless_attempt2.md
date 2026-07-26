## M3 Repair Observations — Iteration 1

### Move operations on M3 wires

A single-polygon x-axis move of 8 dbu on polygon p910 introduced 3 new in-crop violations despite preserving connectivity; the unit_gate channel blocked the change with decision `gated_in` (trial:i01.ug.leaf_0010.07). Do not commit M3 move operations solely on the basis that connectivity is preserved — measure in-crop violation deltas before accepting any move (trial:i01.ug.leaf_0010.07).

### Via-shape resize on M3 within chain fixes

A y-axis resize of 48 dbu applied to the M3 shape (shape_index 0) inside cell `VIA_VIA34_1_2_58_52`, coordinated with matching resizes on V3 (two shapes, +88 dbu y each) and on V4/M4 (+88 dbu y), produced a net reduction of 13 violations across two windows (trial:i01.cu.def:VIA_VIA34_1_2_58_52.00). When an M3 via-shape resize is part of a `chain_fix` group that also adjusts the adjacent via and upper-metal shapes, the combined delta can be negative; apply such chains together rather than applying the M3 resize in isolation (trial:i01.cu.def:VIA_VIA34_1_2_58_52.00).

### Enclosure rules V2.M3.EN.2, V2.M3.AUX.2, V3.M3.EN.1

The chain fix in trial:i01.cu.def:VIA_VIA34_1_2_58_52.00 targeted a cell whose name encodes a V3-to-M3 via stack, and the M3 resize was applied along the y-axis. V3.M3.EN.1 requires 5 nm enclosure on at least one pair of opposite sides; a y-axis expansion of the M3 landing pad is consistent with satisfying this rule. When resizing M3 via pads to address enclosure violations, the resize axis must match the enclosure direction that is short — a y-axis resize corrects top/bottom enclosure shortfalls (trial:i01.cu.def:VIA_VIA34_1_2_58_52.00).

### Width and spacing thresholds

The minimum M3 width is 18 nm (M3.W.1). Side-to-side spacing between edges longer than 36 nm is 18 nm (M3.S.1); tip-to-side spacing when one edge is ≤ 36 nm and the other > 36 nm is 25 nm (M3.S.2); tip-to-tip spacing when both edges are 24–36 nm is 27 nm (M3.S.3); tip-to-tip spacing when one edge is 24–36 nm and the other is < 24 nm is 31 nm (M3.S.5); tip-to-tip spacing when both edges are < 24 nm is 31 nm (M3.S.4). The x-axis move of 8 dbu (= 8 nm at 1 nm/dbu) that introduced 3 new violations in trial:i01.ug.leaf_0010.07 is consistent with a 8 nm shift pushing edges into spacing-rule violations in the side-to-side or tip-to-side category; moves of this magnitude on a wire whose neighbors are already near the 18 nm or 25 nm thresholds must be screened against all applicable spacing rules before commitment.