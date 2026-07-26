**Gated-in outcomes and violation count**

A `gated_in` decision does not guarantee a violation-free crop region: trial:i01.ug.leaf_0010.07 was accepted `gated_in` with `n_new_in_crop` of 3. trial:i02.ug.leaf_0002.01 was also accepted `gated_in` with `n_new_in_crop` of 0 and `n_new_out_of_crop` of 0, confirming that zero-new-violation gated repairs exist but are not guaranteed by the `gated_in` status alone.

**Observed repair operations on V4-touching instance moves**

trial:i01.ug.leaf_0010.07 applied six `move_instance` operations, all in the Y axis (two instances +72 dbu, two +24 dbu, two −24 dbu), to instances whose touched layers included V4, M4, M5, V3, and M3. Connectivity was preserved (`conn_preserved: true`) and zero new violations appeared outside the crop boundary. Mixed-direction Y moves on the same pass—some upward, some downward—are consistent with simultaneous adjustment of enclosing metal on both sides of a via stack.

trial:i02.ug.leaf_0002.01 applied seven `move_instance` operations on layers M3, M4, M5, V3, V4, with moves combining both X and Y components: i0114 [+32, 0], i0112 [+32, −48], i0073 [+32, +96], i0062 [+32, +48], i0105 [0, −48], i0075 [0, +96], i0076 [0, +48] (all dbu). A polygon-level move on p879 (X +32 dbu) was dropped from the final op set by the conflict-resolution stage (reason: `reserved_by_cu_pool_winner`); the seven instance moves executed. Connectivity was preserved and `n_new_in_crop` was 0. Mixed X+Y instance moves on a single pass touching V4 are therefore observed to be accepted with zero net new violations.

**Resize-via-shape repairs on V4-touching via cells**

trial:i02.cu.def:VIA_VIA45_1_2_58_58.02 applied a single `resize_via_shape` operation to the M5 shape (y-axis, −88 dbu) of via cell VIA_VIA45_1_2_58_58, whose touched layers are M4, M5, and V4. The repair was accepted with `decision: applied` through the `cu_pool` channel, connectivity was preserved, and a net reduction of 15 violations was recorded across two units (leaf_0002: −9, leaf_0003: −6). This is the only measured record of a `resize_via_shape` on a V4-touching via cell; it achieved a net-negative violation delta via the `cu_pool` channel rather than the `unit_gate` channel.

**Assemble-drop behavior and conflict resolution**

trial:i02.ug.leaf_0002.01 records two drop categories alongside accepted operations: a `conflict_with_leaf` drop (p879 X+32 move, reason: `reserved_by_cu_pool_winner`) and two `cu_pool:applied` drops (a p879 Y+96 resize and a `move_via_shape` on a V2-layer shape of VIA_VIA23_1_3_36_36). The executed op set contained none of the three dropped polygon-level or via-shape operations; all seven surviving ops were `move_instance` calls. This demonstrates that conflict resolution can strip polygon-level and via-shape ops from a proposed repair while leaving instance-level ops intact for execution.

**Coverage limits of the measured record**

The iteration-1 and iteration-2 history for V4 contains three trials: trial:i01.ug.leaf_0010.07 (Y-only `move_instance`, `gated_in`, 3 new in-crop violations), trial:i02.ug.leaf_0002.01 (mixed X+Y `move_instance`, `gated_in`, 0 new violations), and trial:i02.cu.def:VIA_VIA45_1_2_58_58.02 (`resize_via_shape` on M5, `cu_pool` channel, `applied`, −15 net violations). Rules V4.W.1, V4.S.1, V4.S.2, V4.S.3, V4.M4.EN.1, V4.M5.EN.2, V4.AUX.1, V4.M5.AUX.2, and the NONORTHOGONAL block have no individually confirmed-clean or confirmed-failing outcomes in the measured record. No prescriptions about minimum widths, spacings, enclosures, net-classification distinctions, corner-to-corner checks, or orthogonality enforcement are supported by the available evidence beyond the observations stated above.