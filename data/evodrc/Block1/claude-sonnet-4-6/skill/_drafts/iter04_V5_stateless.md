**V5 compliance through instance-level moves**

In every trial recorded for this layer, V5 geometry was modified exclusively through move_instance operations rather than direct polygon edits. Trials trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03, and trial:i04.ug.leaf_0003.02 all list V5 in their touched_layers and apply instance moves that carry V5 vias with the containing cell. Across all three trials, zero V5-specific rule violations (V5.W.1, V5.S.1, V5.S.2, V5.S.3, V5.M5.EN.1, V5.M6.EN.2, V5.AUX.1, V5.M6.AUX.2) appear in the new_in_crop_by_rule breakdown. Moving a V5-containing instance as a unit, with M5 and M6 co-moving, preserves enclosure (V5.M5.EN.1, V5.M6.EN.2), the AUX containment and width-matching constraints (V5.AUX.1, V5.M6.AUX.2), and all spacing rules (V5.S.1, V5.S.2, V5.S.3) without requiring any standalone V5 polygon resize or repositioning.

**No V5 violations introduced; no out-of-crop V5 violations**

All three trials report n_new_out_of_crop: 0 and empty new_out_of_crop_by_rule fields (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03, trial:i04.ug.leaf_0003.02). None of the applied instance moves drove a V5 instance outside the crop boundary. The new_in_crop violations cleared by those trials are entirely on layers M1 through M6 and lower vias (V1, V2, V4); V5 rules contributed zero counts to those totals.

**Move magnitudes applied to V5-bearing instances**

The dominant move vector for V5-containing instances is purely lateral: +32 dbu in x or -16 dbu in x with y = 0. This pattern is consistent across the bulk of the instance sets in trial:i02.ug.leaf_0003.02 and trial:i04.ug.leaf_0003.02. Trial trial:i02.ug.leaf_0004.03 additionally applied small y-components (±24, ±32, ±72 dbu) together with the same ±32/-16 x-offsets. Two instances (i0345, i0505) received a diagonal move of [32,-96] and [-16,-96] dbu respectively; these moves were first proposed in trial:i02.ug.leaf_0003.02 but dropped at assembly due to an inter-leaf conflict, then reapplied without modification in trial:i04.ug.leaf_0003.02 with no V5 violations resulting. This confirms that diagonal instance moves of that magnitude do not violate V5 spacing or enclosure when M5 and M6 move with the via.

**Cross-leaf conflict handling and deferred instance moves**

In iter 2, leaf_0003 and leaf_0004 both proposed moves for an overlapping set of V5-containing instances. The assemble stage dropped 26 move_instance ops from trial:i02.ug.leaf_0003.02 (reason: external_conflict_dropped) because leaf_0004 had a conflicting claim on those instances. Symmetrically, trial:i02.ug.leaf_0004.03 dropped more than 40 ops due to external_conflict_dropped, external_duplicate, or cross_crop_first_wins conflicts with leaf_0003. Both trials were nonetheless accepted (decision: gated_in, conn_preserved: true), demonstrating that partial application of the instance move set is sufficient to maintain net connectivity at V5. The 26 ops dropped from leaf_0003 in iter 2 are the exact set reapplied in trial:i04.ug.leaf_0003.02, where they executed with zero assemble_drops and yielded n_new_in_crop: 8 with V5 remaining violation-free.

**Net connectivity preservation across all moves**

All three trials were accepted with conn_preserved: true. Moving V5-containing instances without any direct V5 geometry edits is sufficient to maintain the M5-V5-M6 via-stack connectivity, as confirmed in trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03, and trial:i04.ug.leaf_0003.02.