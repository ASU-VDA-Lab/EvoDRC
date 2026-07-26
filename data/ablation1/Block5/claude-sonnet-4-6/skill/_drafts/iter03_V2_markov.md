## Instance-Move Operations

The unit_gate channel successfully gated a two-instance move in trial:i02.ug.leaf_0001.01, shifting instances i0104 and i0061 each by +8 dbu on the x-axis (locus [3148,4084,3260,7436]) with connectivity preserved and zero new violations introduced inside or outside the crop region. Instance moves along the x-axis that maintain grid alignment can resolve V2 violations while preserving connectivity on layers M2, M3, and V2 simultaneously, as all three were touched in trial:i02.ug.leaf_0001.01 without new violations.

## Via Cell M3 Resize — Context-Dependent Outcome

A −40 dbu y-axis resize on the M3 shape (shape_index 0) of cell VIA_VIA23_1_3_36_36 yielded opposite outcomes in two distinct design states:

- **Iter 2 failure:** trial:i02.cu.def:VIA_VIA23_1_3_36_36.00 produced delta_total=0 and was rejected. No violation reduction in unit:leaf_0001 or any other window.
- **Iter 3 success:** trial:i03.cu.def:VIA_VIA23_1_3_36_36.00 on design_state d7ef52f15998ae055d2a5b6fc44f86ea4d6ad3e65793301d5e4a8f22c84a250a produced delta_total=−8, reducing unit:leaf_0001 from 18 to 10 violations, with unit:leaf_0002 unchanged at 16; decision=applied, conn_preserved=true, touched_layers M2/M3/V2.

The same single-shape M3 y-shrink on the same cell thus can reduce V2 violations when the surrounding design state places V2.S.1 mask-extent violations that the end-cap trim resolves. The iter-2 design state did not present that configuration; do not treat a single-context failure as a permanent prohibition on this operation. The repair is context-gated: apply when the unit containing VIA_VIA23_1_3_36_36 shows an active V2.S.1 violation load that is sensitive to the M3 end-cap extent on the y-axis.

The iter-3 success also demonstrates that a −40 dbu y-axis M3 resize on this cell does not trigger a net V2.M3.AUX.2 violation in practice (conn_preserved=true, no delta worsening in any window), consistent with the y-axis being along the M3 length direction rather than perpendicular to it for this cell's orientation — the resize trims an end-cap and does not alter the M3 width matched by V2 under V2.M3.AUX.2.

## Coordinated V2M3 Group Resize — Worsens Violations

The V2M3_corrected group in trial:i02.cu.def:VIA_VIA23_1_3_36_36.01 applied 10 simultaneous operations: −112 dbu y-shrink on M3 and both V3 shapes of VIA_VIA34_1_2_58_52, −40 dbu y-shrink on M3 of VIA_VIA23_1_3_36_36, and symmetric −32 dbu end-shrinks (both low and high ends) on polygons p891, p892, and p893. The outcome was rejected with delta_total=+5: unit:leaf_0005 worsened from 20 to 28 violations (+8) while unit:leaf_0006 improved from 16 to 13 (−3), for a net increase of 5. Shrinking both ends of V2-connected polygons simultaneously by equal amounts does not correct V2.S.1 spacing violations and actively introduces new violations in adjacent units. Symmetric bilateral end-shrinks on the y-axis must not be applied to V2-touching polygons in this region (trial:i02.cu.def:VIA_VIA23_1_3_36_36.01).

## Rule-Grounded Repair Constraints

**V2.W.1 (18 nm minimum width):** No trial in this history targeted a width violation directly, but the −32 dbu bilateral shrinks in trial:i02.cu.def:VIA_VIA23_1_3_36_36.01 on polygons that touch V2 worsened the total violation count. Any resize that reduces polygon extent along the M3 length direction risks narrowing V2 below the 18 nm minimum.

**V2.M3.AUX.2 (V2 must match M3 width perpendicular to M3 length):** The successful iter-3 single-axis M3 y-shrink (trial:i03.cu.def:VIA_VIA23_1_3_36_36.00, delta_total=−8, applied) did not produce new violations, confirming that for VIA_VIA23_1_3_36_36 in its standard orientation the y-axis is along M3 length and a y-end-cap trim does not violate V2.M3.AUX.2. The iter-2 failure (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00, delta_total=0) was a context miss, not an AUX.2 obstruction. For resizes that do target the direction perpendicular to M3 length, V2 must be co-resized by the same amount; no such perpendicular M3 resize has been attempted in this history.

**V2.S.1 (spacing depends on M3 track alignment and end-cap presence):** The V2.S.1 rule constructs per-via masks that extend 5 nm beyond M3 coincident edges. Trimming the M3 end-cap (y-axis, −40 dbu on VIA_VIA23_1_3_36_36) contracts those masks and resolves projection-based spacing violations between previously non-compliant via pairs — confirmed by trial:i03.cu.def:VIA_VIA23_1_3_36_36.00 (−8 violations in unit:leaf_0001). Conversely, the large-scope group resize in trial:i02.cu.def:VIA_VIA23_1_3_36_36.01 (locus [1728,2068,9072,8732]) shrinking M3 across multiple cells simultaneously disrupted mask geometry for adjacent pairs and increased violations by 8 in unit:leaf_0005, illustrating that multi-cell simultaneous M3 shrinks in a wide locus can create new V2.S.1 interactions even when individual shrinks could be safe in isolation.

**V2.M2.EN.1 (5 nm M2 enclosure on two opposite sides) and V2.AUX.1 (V2 inside M2 and M3):** Neither of these rules generated violations that were directly targeted in any trial. The successful move in trial:i02.ug.leaf_0001.01 (x-axis, +8 dbu) preserved connectivity and produced no new violations, consistent with M2 and M3 enclosures remaining intact after a small x-shift when both connected metal layers move together with the via. The successful M3 end-cap trim in trial:i03.cu.def:VIA_VIA23_1_3_36_36.00 also preserved connectivity with M2 and M3, confirming that y-axis end-cap trims on this cell do not break M2 enclosure.

## Action-Selection Summary

Two repair paths are now confirmed effective in this history:

1. **Instance moves (x-axis, paired metal layers):** trial:i02.ug.leaf_0001.01 achieved zero new violations by shifting both connected metal instances together by +8 dbu. Applicable when V2 violations arise from relative placement of via pairs that can be resolved by lateral shift without breaking grid or enclosure constraints.

2. **Single-cell M3 end-cap trim on VIA_VIA23_1_3_36_36 (y-axis, −40 dbu):** trial:i03.cu.def:VIA_VIA23_1_3_36_36.00 achieved delta_total=−8 in design_state d7ef52f15998ae055d2a5b6fc44f86ea4d6ad3e65793301d5e4a8f22c84a250a. This is a single-operation, targeted end-cap trim that contracts the V2.S.1 mask and resolves spacing violations without triggering V2.M3.AUX.2 or breaking M2/M3 enclosure. The same operation failed in iter 2 (different design state), so apply only when the active violation load in the relevant unit is sensitive to this cell's y-extent.

Do not apply: coordinated group operations that apply symmetric bilateral shrinks to V2-adjacent polygons across a wide locus (trial:i02.cu.def:VIA_VIA23_1_3_36_36.01, delta_total=+5). Do not apply simultaneous multi-cell M3 shrinks spanning large regions without per-cell violation sensitivity analysis.