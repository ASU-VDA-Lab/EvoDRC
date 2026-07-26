The inputs were provided inline. Generating the knowledge section now from the DRC rules and the two measured history records.

---

## Repair Strategies: What Worked

### X-axis move-and-resize on via cell definitions reduces violation counts

In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 (iter 1, cu_pool channel), a combination of asymmetric lateral moves and simultaneous x-axis resizes on three V2 shapes inside cell `VIA_VIA23_1_3_36_36` cut the total violation count by 24 (leaf_0012: 27→15, leaf_0013: 28→16). The applied operation sequence was: move shape_index 0 by −144 dbu on x, move shape_index 2 by +144 dbu on x, then resize all three shapes (indices 0, 1, 2) by +288 dbu on x. This pattern spreads the outer shapes away from the center while widening all shapes along the M3 run direction. The trial touched M2, M3, and V2 together and preserved connectivity (`conn_preserved: true`), so co-modifying enclosing metal layers when adjusting V2 geometry is safe and expected.

**Prescriptive takeaway:** When addressing V2 spacing or width violations inside a via cell definition, apply a symmetric outward move to the flanking shapes (equal magnitude, opposing sign) and a uniform x-axis expansion to all shapes in the same operation. Do not move shapes without the accompanying resize (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 applied all five ops atomically and achieved a net −24 result; no partial-op trial exists to compare against, but the full set was sufficient).

---

### Instance moves in y accepted when conn_preserved, even with small in-crop violation gain

In trial:i04.ug.leaf_0003.02 (iter 4, unit_gate channel), three instance moves of ±24 dbu in y introduced 2 new violations inside the crop window and 0 outside it; the trial was still accepted (`gated_in`) because `conn_preserved` was true. This trial touched V2 as part of a broader multi-layer set (M2, M3, M4, M5, V2, V3, V4), confirming that instance-level y-moves propagate V2 position changes indirectly through the via stack. The gate criterion used by the channel was connectivity preservation, not a zero-new-violation requirement.

**Prescriptive takeaway:** Accept unit_gate instance moves that shift via positions in y provided `conn_preserved` holds, even when they introduce a small number of new in-crop DRC markers (trial:i04.ug.leaf_0003.02 shows 2 new in-crop violations tolerated). Do not treat a non-zero `n_new_in_crop` as a hard block; treat `n_new_out_of_crop > 0` or `conn_preserved: false` as the blocking conditions.

---

## Rule-Specific Repair Notes

### V2.W.1 — minimum width 18 nm along M3 length

The x-axis resize of +288 dbu per shape applied in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 increases shape extent along the M3 run direction. Use x-axis resize (not y-axis) when width violations arise along the M3 length direction.

### V2.S.1 — spacing between V2 instances (18/27/18 nm by track configuration)

The mask-based spacing check (V2.S.1) distinguishes three track configurations. The move-and-resize pattern in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 resolved spacing violations across both leaf_0012 and leaf_0013 simultaneously by adjusting a shared via cell definition, which propagated the geometry fix to all instances of that cell. When multiple windows share the same via cell, repair at the cell definition level rather than per-instance to obtain maximum violation reduction per operation.

### V2.M2.EN.1 and V2.M3.EN.2 — enclosure by M2 and M3

Both enclosure rules require M2 and M3 to be co-modified whenever V2 shapes are resized. Trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 touched all three layers (M2, M3, V2) in a single applied trial, demonstrating that a valid repair to V2 geometry must update the enclosing metal simultaneously. Never resize a V2 shape without verifying that M2 encloses the result by ≥5 nm on at least two opposite sides (V2.M2.EN.1) and that M3 encloses it by 5&5 nm or 5&0 nm on two opposite sides (V2.M3.EN.2).

### V2.AUX.1 and V2.M3.AUX.2 — containment and width-matching

V2.AUX.1 requires V2 to remain inside M2 ∩ M3 at all times. V2.M3.AUX.2 requires V2 to exactly match M3 width in the direction perpendicular to the M3 run. The combined move-and-resize in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 preserved both constraints (the trial was applied with `conn_preserved: true` and produced no noted AUX violations), confirming that symmetric outward moves paired with equal-magnitude resizes maintain the required M3-perpendicular width relationship.

### V2.S.2, V2.S.3, V2.S.4 — corner-to-corner euclidean spacing (23/30/27 nm)

These rules operate on end-cap-extended masks (`v2_wec_mask`, `v2_nec_mask`) and fire only on non-projection-coincident edges. No trial in the current history targeted these rules in isolation. Spacing violations resolved by trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 could include S.2/S.3/S.4 contributions; however, the available records do not attribute the −24 delta to specific rule IDs, so no rule-specific claim can be made beyond what the operation pattern demonstrates.

---

## Operation Ordering and Atomicity

Trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 executed 5 ops in a single applied trial (2 moves + 3 resizes). The decision was "applied" at the trial level, not per-op. Always bundle the full symmetric move-and-resize set for a via cell into one trial submission; splitting it would leave shapes in an intermediate state that may violate enclosure or width rules.

---

## Channel-Specific Notes

- **cu_pool** (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00): targets via cell definitions directly; effective for bulk-reducing violations shared across multiple leaf windows that instantiate the same cell.
- **unit_gate** (trial:i04.ug.leaf_0003.02): targets instance moves; V2 is affected indirectly through the full via stack. The gate criterion is `conn_preserved`, not violation delta alone.