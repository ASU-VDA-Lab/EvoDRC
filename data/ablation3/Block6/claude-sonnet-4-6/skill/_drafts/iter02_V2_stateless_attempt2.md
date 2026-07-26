The single confirmed trial for this layer is `i02.cu.def:VIA_VIA23_1_3_36_36.00` (decision: applied, delta_total: -78, conn_preserved: true). All knowledge below is grounded exclusively in that record.

## Repair Strategy

**Combine x-axis move and resize in a single multi-op sequence.** Trial `i02.cu.def:VIA_VIA23_1_3_36_36.00` applied five operations entirely on the x-axis across three V2 shapes within cell `VIA_VIA23_1_3_36_36`, reducing whole-design violations by 78 while preserving connectivity. No y-axis operations were used.

**Pair a move with a resize on the same shape when adjusting its centroid and extent together.** In trial `i02.cu.def:VIA_VIA23_1_3_36_36.00`, shape 0 received a move of -144 dbu followed by a resize of +288 dbu on the x-axis, and shape 2 received a move of +144 dbu followed by a resize of +288 dbu on the x-axis; both shapes ended with a net x-extent increase of 288 dbu while their edge positions shifted asymmetrically. Shape 1, which required no centroid shift, received only a resize of +288 dbu with no accompanying move.

**Apply uniform resize magnitudes across all affected shapes in a cell.** All three shapes in trial `i02.cu.def:VIA_VIA23_1_3_36_36.00` received the same +288 dbu x-axis resize delta; this uniform expansion resolved the violation set without introducing new violations.

**Move direction must be opposite for shapes on opposing sides of the cell.** In trial `i02.cu.def:VIA_VIA23_1_3_36_36.00`, shape 0 moved -144 dbu (toward the cell's left edge) and shape 2 moved +144 dbu (toward the right edge), while shape 1 (center) required no move. The move magnitude of 144 dbu equals exactly half the resize delta of 288 dbu, which is consistent with expanding a symmetric via array outward from center.

**Touched-layer scope for V2 repairs includes M2 and M3.** Trial `i02.cu.def:VIA_VIA23_1_3_36_36.00` lists touched_layers as M2, M3, and V2; any V2 shape adjustment must be evaluated against both bounding metal layers for enclosure (V2.M2.EN.1, V2.M3.EN.2) and overlap (V2.AUX.1, V2.M3.AUX.2) rules.

## Rule-Specific Observations

**V2.W.1 (minimum width 18 nm):** The +288 dbu x-axis resizes in trial `i02.cu.def:VIA_VIA23_1_3_36_36.00` increased via widths rather than decreased them, which is consistent with resolving a width violation or with providing margin against spacing rules. Do not apply resizes that reduce x-extent below 18 nm.

**V2.AUX.1 / V2.M3.AUX.2 (V2 must stay inside M2 ∩ M3; V2 width must match M3 width perpendicular to M3 length):** Trial `i02.cu.def:VIA_VIA23_1_3_36_36.00` preserved connectivity (conn_preserved: true) after expanding all three V2 shapes, confirming that the chosen resize deltas kept each V2 within its enclosing M2 and M3 regions. Do not resize V2 beyond the M3 boundary perpendicular to M3 length.

**V2.M2.EN.1 / V2.M3.EN.2 (5 nm enclosure on opposite sides):** Because trial `i02.cu.def:VIA_VIA23_1_3_36_36.00` touched M2 and M3 alongside V2 and still passed with conn_preserved: true and a net negative violation count, the enclosure requirements remained satisfied after the combined move-and-resize sequence. Resizing V2 on the x-axis without also verifying M2 and M3 extents on that axis risks creating new enclosure violations.