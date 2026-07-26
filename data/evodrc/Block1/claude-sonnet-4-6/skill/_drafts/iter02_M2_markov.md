**Repair operation types observed**

Accepted trials use `move_instance`, `resize_end`, and direct polygon `move` operations. trial:i02.ug.leaf_0001.00 used only `move_instance` [100,0] and `resize_end` on the high-x end (+60 dbu x-axis), touching only M1/M2/V1, and produced zero new violations. trial:i02.ug.leaf_0003.02 and trial:i02.ug.leaf_0004.03 used direct `move` ops on individual polygons (e.g., p1145, p1144, p1143, p1142, p1563, p1562, p1561) alongside `move_instance` ops, with both x and y delta components. All three iteration-2 trials were accepted (gated_in, conn_preserved=true).

**Y-direction displacement is permitted when connectivity is preserved**

The iteration-1 finding that no accepted trial used y-axis displacement is superseded. trial:i02.ug.leaf_0003.02 includes `move_instance` ops with y-components of −64, −96, and −112 dbu, and polygon `move` ops with y-components of −64, −112, and −96 dbu; it was accepted with 0 out-of-crop violations. trial:i02.ug.leaf_0004.03 includes `move_instance` ops with y-components of +32, +72, +24, −24, and −72 dbu, and a polygon `move` with y=+32 dbu; it was also accepted with 0 out-of-crop violations. Y-direction displacement does not block acceptance provided connectivity is preserved and out-of-crop violations remain zero.

**Connectivity is the hard gate**

Avoid operation sets that break net connectivity. trial:i01.ug.leaf_0034.12 was gated out with `conn_broken` and simultaneously introduced 89 new in-crop DRC violations. Every accepted trial across both iterations carries `conn_preserved=true`. The acceptance channel (unit_gate) tolerates large numbers of new in-crop violations when connectivity holds: trial:i02.ug.leaf_0003.02 introduced 80 new in-crop violations and was accepted; trial:i02.ug.leaf_0004.03 introduced 47 new in-crop violations and was accepted; trial:i02.ug.leaf_0001.00 introduced 0. No accepted trial has introduced out-of-crop violations.

**New in-crop violations are tolerated; out-of-crop violations are not**

The unit_gate channel accepts repairs regardless of how many in-crop violations are introduced, as long as `conn_preserved=true` and `n_new_out_of_crop=0`. The highest accepted in-crop count across both iterations is 80 (trial:i02.ug.leaf_0003.02). Out-of-crop violations have been zero in every accepted trial (trial:i02.ug.leaf_0001.00, trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03, and all iteration-1 accepted trials). Never produce out-of-crop violations.

**M2.S.3 and M2.S.7 violations can be introduced as accepted side effects**

trial:i02.ug.leaf_0004.03 introduced 1 new in-crop M2.S.3 violation and 1 new in-crop M2.S.7 violation alongside violations on other layers, yet was accepted. When the repair target is a different locus, incidental M2 spacing violations introduced within-crop are tolerated by the unit_gate channel. However, these violations remain real DRC errors and may be targeted in a subsequent iteration's repair pass.

**Polygon move operations co-occur with multi-instance repairs**

trial:i02.ug.leaf_0003.02 and trial:i02.ug.leaf_0004.03 each used direct polygon `move` ops (axis and delta_dbu specified per-polygon) in addition to `move_instance`. In both cases the polygon moves applied both x and y displacements to specific polygon ids (p1142–p1145, p1561–p1563). This `move` op is distinct from `resize_end` (which changes only one endpoint) and from `move_instance` (which moves a full cell). Use direct polygon `move` ops when individual wire segments must be repositioned without resizing and without moving the entire instance they belong to.

**Polygon endpoint resizing co-occurs with instance moves**

Several accepted row-level trials from iteration 1 combined `resize_end` on M2 polygon endpoints with `move_instance` on the same row (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row5.05, trial:i01.ug.Block1_union_row6.06, trial:i01.ug.Block1_union_row8.07). trial:i02.ug.leaf_0001.00 confirms the combination: `move_instance` [100,0] paired with `resize_end` axis=x end=high delta=+60 dbu, producing zero new violations. Apply `resize_end` on the high-x or low-x polygon end when an instance move would otherwise leave a wire endpoint misaligned or violate enclosure. Leaf-level repairs with a single instance and no endpoint misalignment require no polygon resize (trial:i01.ug.leaf_0004.09, trial:i01.ug.leaf_0020.10, trial:i01.ug.leaf_0031.11).

**Cross-layer scope: connectivity and out-of-crop are what matter, not layer count**

The iteration-1 conclusion that cross-layer scope causes gating is narrowed by iteration-2 data. trial:i02.ug.leaf_0003.02 and trial:i02.ug.leaf_0004.03 both touched M2 through M6 plus V2 through V5 and were accepted. The gated-out trial:i01.ug.leaf_0034.12 was rejected because it broke connectivity, not solely because it touched higher layers. The operative constraints remain: `conn_preserved=true` and `n_new_out_of_crop=0`. Cross-layer operations that preserve connectivity and produce no out-of-crop violations are accepted by the unit_gate channel.

**Assembly conflict resolution: first_wins for cross-crop, external_conflict_dropped for shared instances**

When two leaf repairs compete for the same instance, the assembler drops one repair's op with reason `external_conflict_dropped` (the other leaf retains its version). When two leaves share a polygon across a crop boundary, the first leaf to claim it wins (`cross_crop_first_wins`). trial:i02.ug.leaf_0003.02 dropped 26 ops due to conflict with leaf_0004; trial:i02.ug.leaf_0004.03 dropped 41 ops due to conflict with leaf_0003. Both were still accepted after drops. The post-drop op set is what the DRC checker evaluates, so a repair plan should be robust to having conflicting ops removed.

**Tip edge length determines which spacing rule applies**

M2.S.1 (18 nm, side-to-side, both edges >36 nm), M2.S.2 (25 nm, tip-to-side, one edge ≤36 nm and one >36 nm), M2.S.3 (27 nm, tip-to-tip, both edges 24–36 nm), M2.S.5 (31 nm, tip-to-tip, one edge 24–36 nm and one <24 nm), and M2.S.4 (31 nm, tip-to-tip, both edges <24 nm) each apply to a distinct edge-length regime. Resizing a polygon endpoint changes the tip edge length and therefore shifts which rule governs the gap. The `resize_end` operations in trial:i01.ug.Block1_union_row5.05 and trial:i01.ug.Block1_union_row6.06 adjusted wire endpoints alongside instance moves, directly affecting the classification of adjacent edges under these rules. trial:i02.ug.leaf_0004.03 introduced 1 new M2.S.3 in-crop violation, confirming that multi-instance y+x displacements can shift edge lengths into the 24–36 nm tip regime.

**M2.S.7 parallel-run-length constraint**

M2.S.7 forbids an 18 nm tip-to-tip gap co-located with a side-to-side spacing ≤32 nm and requires parallel run length ≥35 nm when side spacing falls in that range. `resize_end` operations that extend or contract a polygon in x alter both the tip gap distance and the run-length extent that M2.S.7 measures. The endpoint adjustments in trial:i01.ug.Block1_union_row5.05, trial:i01.ug.Block1_union_row6.06, and trial:i01.ug.Block1_union_row8.07 are consistent with correcting run-length shortfalls at M2.S.7 boundaries. trial:i02.ug.leaf_0004.03 introduced 1 new M2.S.7 in-crop violation as a side effect of its multi-instance move, confirming that large-displacement repairs can push edges into M2.S.7 territory.

**V1 enclosure maintained alongside every M2 move**

V1.M2.EN.2 requires M2 to enclose V1 by ≥5 nm on two opposite sides; V1.M2.AUX.2 requires V1 to match M2 width in the direction perpendicular to the M2 run. Every accepted trial across both iterations touched V1 alongside M2 (trial:i01.ug.Block1_union_row1.00 through trial:i01.ug.leaf_0031.11; trial:i02.ug.leaf_0001.00). Treat V1 adjustment as part of every M2 x-direction repair. The large multi-layer trials trial:i02.ug.leaf_0003.02 and trial:i02.ug.leaf_0004.03 did not list V1 in their touched_layers, which correlates with their higher in-crop violation counts (including V1.M1.EN.1 violations on M1-side enclosures); this does not contradict the V1/M2 rule but illustrates that omitting V1 adjustment creates new enclosure violations.

**Minimum-area floor (M2.A.1)**

M2.A.1 sets a 504 nm-sq area floor. `resize_end` operations that retract a polygon end reduce area; ensure the resulting polygon area does not fall below 504 nm-sq. No accepted trial produced new out-of-crop M2.A.1 violations (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row5.05, trial:i01.ug.Block1_union_row6.06, trial:i01.ug.Block1_union_row8.07, trial:i02.ug.leaf_0001.00), confirming that the endpoint resize magnitudes used in those trials stayed above the area threshold.

**Via-only shape resizes do not clear M2 violations**

trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 (cu_pool channel) resized a VIA23 shape in the y-direction on M3 alone and was rejected with `delta_total=0` — no net change in M2 violation count on either affected window. Avoid standalone via shape resizes as the sole M2 repair operation; the measured record shows zero net benefit on M2 from this approach.