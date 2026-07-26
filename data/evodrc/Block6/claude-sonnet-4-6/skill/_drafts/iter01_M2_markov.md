**Repair channels and decision outcomes**

Two repair channels operated on M2 geometry in this iteration: `unit_gate` and `cu_pool`. All eight `unit_gate` trials produced a `gated_in` decision with `conn_preserved=true` and zero net violation change (`n_new_in_crop=0`, `n_new_out_of_crop=0`; trials trial:i01.ug.Block6_union_row3.00 through trial:i01.ug.leaf_0018.07). The single `cu_pool` trial produced an `applied` decision with a measured net reduction of 78 violations (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). Connectivity preservation (`conn_preserved=true`) is the acceptance gate for `unit_gate`; the channel does not require a positive violation delta to accept a repair, only that no new violations are introduced and that connectivity is maintained.

**Move direction: exclusively positive-x**

Every `move_instance` operation across all iteration-1 unit_gate trials moved in the +x direction. Observed deltas: +28 dbu (trial:i01.ug.leaf_0015.06), +36 dbu (trial:i01.ug.Block6_union_row5.01, trial:i01.ug.Block6_union_row8.03, trial:i01.ug.leaf_0011.05, trial:i01.ug.leaf_0018.07), +72 dbu (trial:i01.ug.Block6_union_row3.00), +104 dbu (trial:i01.ug.Block6_union_row7.02), +112 dbu (trial:i01.ug.leaf_0001.04). The sole negative-x move was −36 dbu on instance i0074 in trial:i01.ug.Block6_union_row7.02, which co-occurred with a +56 dbu `resize_end` on the low-x end of polygon p1920 in the same trial — net result is a polygon-end pull-in, not a net negative translation of the metal.

**Co-movement of M1 and V1 with M2**

Every unit_gate trial that touched M2 also listed M1 and V1 in `touched_layers` (trials trial:i01.ug.Block6_union_row3.00 through trial:i01.ug.leaf_0018.07). No trial modified M2 in isolation from these adjacent layers. When moving instances to resolve M2 spacing or enclosure violations, always confirm that M1 and V1 elements within those instances move with them; a repair that translates M2 without translating the co-incident V1 or M1 will break V1.M2.EN.2 or V1.M2.AUX.2 enclosure constraints.

**Polygon resize_end accompanies instance moves in four of eight unit_gate trials**

When a move_instance op alone is insufficient to resolve a violation, a `resize_end` on the high-x end of the implicated M2 polygon was applied in addition. Observed pairings: +92 dbu resize with +36 dbu move (trial:i01.ug.Block6_union_row5.01, polygon p2072); +124 dbu resize with +104 dbu move (trial:i01.ug.Block6_union_row7.02, polygon p1903); +132 dbu resize with +112 dbu move (trial:i01.ug.leaf_0001.04, polygon p2016); +48 dbu resize with +28 dbu move (trial:i01.ug.leaf_0015.06, polygon p1923). In every case the resize delta exceeded the move delta, indicating that the M2 polygon end was extended beyond the moved instance boundary — consistent with maintaining V1.M2.EN.2 (minimum 5 nm enclosure of V1 by M2 on two opposite sides) after the via-bearing instance shifts.

**Low-end resize combined with adjacent instance pull-back**

In trial:i01.ug.Block6_union_row7.02, instance i0074 was moved −36 dbu while the low-x end of polygon p1920 was extended +56 dbu. This pattern pulls an instance away from a spacing violation while simultaneously extending the M2 polygon end toward the retreating metal to preserve V1.M2.AUX.2 (V1 must match M2 width perpendicular to M2 length) and V1.M2.EN.2 enclosure. The resize_end on the low-x end absorbs the gap created by the instance retreat.

**Via cell (V2 touching M2) repair via shape resize, not instance move**

The cu_pool trial (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00) resolved 78 violations by modifying the shared via cell definition `VIA_VIA23_1_3_36_36` directly: three V2 shapes were moved and resized in x (move_via_shape and resize_via_shape ops, deltas −144, +264, +288, +144, +264 dbu). The `touched_layers` were M2, M3, and V2 — no M1 or V1. When M2/V2 enclosure violations (V2.M2.EN.1: minimum 5 nm enclosure on two opposite sides) affect a shared via cell used across many placements, resizing the via shape within the cell definition propagates the fix to all instances simultaneously, yielding large violation-count reductions (−42 in leaf_0019, −36 in leaf_0020, trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

**Move granularity and minimum unit**

The smallest observed move or resize increment is 28 dbu (trial:i01.ug.leaf_0015.06), and 36 dbu recurs as the dominant step across five trials. Given M2.W.1 minimum width of 18 nm and M2.S.1 minimum side-to-side spacing of 18 nm, a 36 dbu step corresponds to one minimum M2 pitch (18 nm width + 18 nm space). Repair moves that are multiples of 36 dbu land on a pitch-aligned grid and avoid introducing new M2.S.1 or M2.W.1 violations. The 28 dbu step (trial:i01.ug.leaf_0015.06) does not align to the 36 dbu pitch grid and requires the accompanying resize_end (+48 dbu, polygon p1923) to restore enclosure, confirming that non-pitch moves require endpoint correction.

**All iteration-1 repairs share a single base design state**

Every trial in this iteration — both channels, all nine trials — originates from design state `685706506817f4f5a58d885e68808402b61fcf189fed22cc344fa6dec38c0f99`. Conclusions about repair effectiveness are relative to this single baseline; cross-iteration comparison requires noting when the design state changes.