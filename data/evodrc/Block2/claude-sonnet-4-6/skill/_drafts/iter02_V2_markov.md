## Repair Strategy

**Co-modify V2 via cell and M3 metal together in a single repair pass.** Both completed repairs on this layer (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 and trial:i02.cu.def:VIA_VIA23_1_3_36_36.00) applied five operations atomically: one `resize_via_shape` on the V2 cell along Y and four `resize` ops on associated M3 polygons along Y. Each repair achieved `conn_preserved: true` and a delta of −8 violations in the target window. Splitting these into separate passes risks introducing transient violations on whichever layer is modified first.

**Shrink magnitude on M3 (64 dbu per polygon) must exceed the shrink on the V2 cell (40 dbu) when reducing Y-extent.** Both trials applied −64 dbu to four M3 polygons (p962–p965 in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00; p958–p961 in trial:i02.cu.def:VIA_VIA23_1_3_36_36.00) while shrinking the via cell only 40 dbu along Y. This asymmetry is required to simultaneously satisfy M3 end-cap enclosure (V2.M3.EN.2 mandates ≥5 nm enclosure on two opposite sides) and keep the V2 shape within M3 (V2.AUX.1, V2.M3.AUX.2). A uniform shrink at the same magnitude on both layers would leave the via underenclosed or produce a flush edge on the wrong side.

## Layer Interaction

**Repairs to V2 touch M2, M3, and V2 simultaneously.** Both trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 and trial:i02.cu.def:VIA_VIA23_1_3_36_36.00 record `touched_layers: ["M2","M3","V2"]`. This is consistent with the rule set: V2.AUX.1 requires V2 to be inside both M2 and M3, and V2.M2.EN.1 requires M2 to enclose V2 by ≥5 nm on at least two opposite sides. Any Y-axis resize of the via cell requires verifying M2 enclosure even when the driving violation involves M3 geometry. Do not limit repair scope to the single metal layer named in the violation message.

## Via Cell Grouping

**Use group `via23-m3` to collect the V2 cell shape and all associated M3 polygons for coordinated resize.** Both trials label all five operations under group `via23-m3`, covering the `resize_via_shape` op on layer M3 (shape_index 0 of cell VIA_VIA23_1_3_36_36) and the four M3 polygon resizes. Treating the group as a unit ensures the DRC checker sees a consistent intermediate state.

## Connectivity Safety

**A Y-axis shrink of 40 dbu on a V2 via cell is achievable without breaking connectivity in the Block2 / cu_pool context.** Both trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 and trial:i02.cu.def:VIA_VIA23_1_3_36_36.00 report `conn_preserved: true` after this shrink. The minimum V2 width rule V2.W.1 (18 nm along the M3 length direction) sets the hard lower bound; the 40 dbu (= 4 nm at 0.1 nm/dbu) trim is modest relative to the 36×36 nominal cell size named in `VIA_VIA23_1_3_36_36`, so connectivity is preserved with margin at two distinct loci ([1728, 2068, 10368, 9812] and the iter-1 locus).

## Violation Count Dynamics

**Each single multi-operation repair at one locus clears exactly −8 violations in one window and leaves adjacent windows unchanged.** trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 reduced violations by 8 in `unit:leaf_0012` (27→19) while `unit:leaf_0013` held at 28 (delta 0). trial:i02.cu.def:VIA_VIA23_1_3_36_36.00 reduced violations by 8 in `unit:leaf_0003` (20→12) while `unit:leaf_0002` held at 7 (delta 0). The −8 / 0 split across two windows is consistent across both measured repairs. Do not assume a single via-cell repair clears all windows; additional repair passes targeting unchanged windows are required.