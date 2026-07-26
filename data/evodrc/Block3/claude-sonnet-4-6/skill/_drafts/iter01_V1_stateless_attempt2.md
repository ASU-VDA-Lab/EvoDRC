## Repair Pattern Overview

All ten trials in iteration 1 resolved V1 DRC violations without introducing new violations: every trial recorded `decision: "gated_in"` with `n_new_in_crop: 0` and `n_new_out_of_crop: 0` (trial:i01.ug.Block3_union_row1.00, trial:i01.ug.Block3_union_row2.01, trial:i01.ug.Block3_union_row5.02, trial:i01.ug.Block3_union_row8.03, trial:i01.ug.leaf_0006.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0008.06, trial:i01.ug.leaf_0009.07, trial:i01.ug.leaf_0012.08, trial:i01.ug.leaf_0013.09). All touched layers M1, M2, and V1 as a coupled set; V1 is never moved in isolation from its enclosing M1 and M2 geometry.

## Instance Move as the Primary Repair Primitive

Every repair in this iteration includes at least one `move_instance` op. Moves occur exclusively along the x-axis; delta_dbu values are [+36,0], [+72,0], [+108,0], [+136,0], and [-36,0]. Four trials applied only `move_instance` ops without any polygon resize and still achieved clean DRC: trial:i01.ug.Block3_union_row2.01 (two instances moved +36 dbu each), trial:i01.ug.leaf_0006.04 (two instances moved +36 dbu each), trial:i01.ug.leaf_0009.07 (one instance moved +36 dbu), and trial:i01.ug.leaf_0013.09 (one instance moved -36 dbu). Move-only repair is therefore sufficient when the existing M2 polygon already provides the required enclosure at the destination position (V1.M2.EN.2 requires 5 nm enclosure on two opposite sides; V1.M1.EN.1 requires 5 nm on one axis and 2 nm on the orthogonal axis).

## M2 End Extension Required When Instance Displacement Would Violate Enclosure at the New Position

When an instance is moved in +x and the high-x edge of M2 would no longer provide sufficient enclosure of V1 at the new position, the M2 high-x end must be extended simultaneously via `resize_end, axis: x, end: high`. This pattern appears in trial:i01.ug.Block3_union_row1.00, trial:i01.ug.Block3_union_row5.02, trial:i01.ug.Block3_union_row8.03, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0008.06, and trial:i01.ug.leaf_0012.08. In every case the resize_end delta is applied to the M2 polygon that spans the moved V1, not to an unrelated polygon.

The resize_end delta always equals or exceeds the corresponding instance move delta. Measured pairs (move_dbu, resize_dbu):

- trial:i01.ug.Block3_union_row1.00: three pairs of (136, 192) — resize exceeds move by 56 dbu in each pair.
- trial:i01.ug.Block3_union_row5.02: one pair of (36, 36) and two additional instances moved +36 without resize, confirming that M2 end extension is applied only for the specific polygon needing extra coverage.
- trial:i01.ug.Block3_union_row8.03: four pairs — (108, 164), (72, 128), (72, 128), (72, 92) — excesses of 56, 56, 56, and 20 dbu respectively.
- trial:i01.ug.leaf_0007.05: two pairs of (36, 56) — resize exceeds move by 20 dbu per pair.
- trial:i01.ug.leaf_0012.08: one pair of (72, 108) — resize exceeds move by 36 dbu.

Do not set the M2 resize_end delta equal to the instance move delta alone when the pre-move enclosure margin was already at or near the 5 nm minimum; add enough to restore the required enclosure. The minimum required surplus above the instance move delta is determined by the deficit in M2 enclosure of V1 at the destination. All trials above show that surpluses of 20, 36, and 56 dbu were each sufficient in their respective contexts without opening new V1.S.1/V1.S.2/V1.S.3/V1.S.4 spacing violations.

## Y-Axis M2 Resize in Mixed-Axis Repairs

trial:i01.ug.leaf_0008.06 includes a `resize_end, axis: y, end: high, delta_dbu: 20` on polygon p1159 in addition to an x-axis instance move and x-axis M2 extension. This establishes that V1.M2.EN.2 enclosure violations can occur in y when an instance is shifted in x if the via body approaches the y boundary of M2. Apply resize_end on y when the moved instance's y extent approaches the M2 y-boundary within 5 nm (the V1.M2.EN.2 minimum). This trial confirmed the combined x-move plus y-resize plus x-resize sequence introduces no new violations.

## Spacing Rules: Verified Safe Region for Move Magnitudes Used

All repairs that moved vias by up to 136 dbu in x within their respective loci introduced no new V1.S.1, V1.S.2, V1.S.3, or V1.S.4 violations (trial:i01.ug.Block3_union_row1.00, trial:i01.ug.Block3_union_row8.03, trial:i01.ug.leaf_0008.06). V1.S.1 enforces a minimum projection spacing of 17 nm between v1_mask edges orthogonal to M2, and 18 nm between v1_maskav non-M2 edges; confirmed moves stayed within the available spacing budget for their loci. No trial generated a V1.S.2 (minimum 23 nm euclidean corner-to-corner for WEC vias) or V1.S.3 (minimum 30 nm euclidean corner-to-corner for NEC vias) or V1.S.4 (minimum 27 nm corner-to-corner between WEC and NEC) violation.

## M1 Enclosure: No Violations from Any Move or Resize

No trial produced a V1.M1.EN.1 violation. V1.M1.EN.1 requires M1 to enclose V1 by 5 nm on one axis and 2 nm on the orthogonal axis. Because all ops are `move_instance` (which moves V1 and its associated M1 cell together) rather than moving V1 geometry independently of M1, the M1–V1 spatial relationship is preserved by construction. Do not apply independent V1 geometry moves that break M1 co-location; always use `move_instance` when shifting V1 within its cell (trial:i01.ug.Block3_union_row1.00 through trial:i01.ug.leaf_0013.09).

## V1.AUX.1 and V1.M2.AUX.2 Compliance

No trial violated V1.AUX.1 (V1 must be inside M1 & M2) or V1.M2.AUX.2 (V1 width must equal M2 width along the direction perpendicular to M2 length). The `resize_end` ops extend M2 only along M2's length axis; they do not alter M2 width in the perpendicular direction. V1.M2.AUX.2 compliance is therefore maintained by restricting M2 edits to length-axis `resize_end` ops, as observed in trial:i01.ug.Block3_union_row1.00, trial:i01.ug.Block3_union_row8.03, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0012.08.

## Non-Orthogonal Geometry: No Violations Introduced

All polygon ops in this iteration produce axis-aligned rectangular geometry: resize_end is applied to a single axis (x or y) at a single end (high), and move_instance preserves polygon shape. No GEOMETRY.NONORTHOGONAL violation appeared in any trial (trial:i01.ug.Block3_union_row1.00 through trial:i01.ug.leaf_0013.09). Restrict all V1 and M2 polygon modifications to axis-aligned moves and single-axis end extensions to maintain this record.

## Connectivity Preservation Across All Repairs

Every trial records `conn_preserved: true`. Connectivity preservation is confirmed by the `unit_gate` channel gating logic (`reason: "conn_preserved"`). The pairing of instance moves with M2 end extensions at the same high-x end as the movement direction is the mechanism that preserves M2–V1 contact without creating new short-path routes. All ten trials confirm this coupling is sufficient and safe.