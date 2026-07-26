## Effective V4 Repair: Y-Axis M5 Resize in Shared Via Cell Definitions via cu_pool

A y-axis M5 shrink of 88 dbu applied to cell VIA_VIA45_1_2_58_58 through the cu_pool channel reduced total in-crop V4 violations by 16 (trial i04.cu.def:VIA_VIA45_1_2_58_58.00, delta: -8 in unit leaf_0002, -8 in unit leaf_0003). The operation touched M4, M5, and V4 layers only, and the decision was "applied," confirming the repair was committed to the design state.

## Shared Via Cell Repair Propagates to All Instantiating Units

VIA_VIA45_1_2_58_58 is instantiated in at least leaf_0002 and leaf_0003. The single cu_pool resize in trial i04.cu.def:VIA_VIA45_1_2_58_58.00 resolved 8 violations in each unit in one operation. When the same V4 violation pattern recurs across multiple units that share a via cell definition, apply the repair to the cell definition via cu_pool; a single cell-level resize propagates the fix to every instantiating unit simultaneously, as measured in trial i04.cu.def:VIA_VIA45_1_2_58_58.00.

## Unit-Gate Instance Moves Increase V4 In-Crop Violations and Are Not Applied

Instance moves through the unit_gate channel on loci overlapping V4 introduced 2 new in-crop violations per trial and were not applied to the design. Trial i03.ug.leaf_0002.01 (8 move_instance ops plus 2 x-axis resize_end ops on polygon p937, touching M3/M4/M5/V3/V4, locus covering the full design window) recorded n_new_in_crop=2 and decision gated_in. Trial i04.ug.leaf_0003.02 (3 move_instance ops, touching M2/M3/M4/M5/V2/V3/V4) also recorded n_new_in_crop=2 and decision gated_in. Do not use unit_gate instance moves as the primary repair path for V4 violations; every recorded unit_gate trial on a V4-touching locus worsened the in-crop V4 count (trial i03.ug.leaf_0002.01, trial i04.ug.leaf_0003.02).

## Connection Preservation Is Insufficient for V4 Repair Acceptance

Trials i03.ug.leaf_0002.01 and i04.ug.leaf_0003.02 both reported conn_preserved=true yet produced 2 new in-crop violations each, yielding gated_in rather than applied decisions. A V4 repair that preserves connectivity but increases the in-crop violation count does not constitute an acceptable resolution; route V4-specific repairs through cu_pool via-cell geometry adjustments, as demonstrated in trial i04.cu.def:VIA_VIA45_1_2_58_58.00.

## Instance Move Delta Granularity in V4-Touching Unit-Gate Operations

All move_instance delta_dbu values recorded in unit_gate trials on V4-touching loci are integer multiples of 24 dbu: ±24 and ±72 in trial i03.ug.leaf_0002.01, and ±24 in trial i04.ug.leaf_0003.02. Use 24 dbu as the minimum move step when scheduling instance moves near V4 geometry to stay consistent with the snapping granularity observed across both trials.