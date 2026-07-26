## Repair Behavior and Outcome Summary

Two trials have been measured on layer V3 through iteration 4. The findings below are drawn exclusively from those records.

---

## Shrinking V3 Along the Y-Axis While Co-Shrinking M3 Increases Violations

Do not apply simultaneous y-axis resize reductions to both V3 shapes and their enclosing M3 shape in the same operation bundle. In trial:i01.cu.def:VIA_VIA34_1_2_58_52.01, a three-operation bundle resized M3 by -64 dbu on the y-axis and resized both V3 shapes by -24 dbu on the y-axis within the same cell (VIA_VIA34_1_2_58_52). The net result was a delta_total of +34 violations across two windows (unit:leaf_0025 gained 24, unit:leaf_0026 gained 10). The trial was rejected with decision "rejected_net_positive." Connectivity was preserved, confirming the violation increase was purely geometric, not topological.

The enclosure rule V3.M3.EN.1 requires at least 5 nm of M3 enclosure on two opposite sides. Co-shrinking M3 and V3 along the same axis simultaneously reduces the enclosure margin without providing any compensating benefit. Never bundle a negative y-axis M3 resize with a negative y-axis V3 resize in the same repair step; the resulting violation count reliably exceeds the pre-repair state (trial:i01.cu.def:VIA_VIA34_1_2_58_52.01, delta +34).

---

## Instance-Move Operations Touching V3 Can Be Accepted with Residual Violations

Trial trial:i04.ug.leaf_0002.01 applied 11 operations (a mix of polygon moves and instance moves, grouped as "m5_align" and ungrouped) that displaced instances across M3, M4, M5, V3, and V4. The trial was accepted with decision "gated_in" and conn_preserved=true. However, the DRC window recorded 2 new violations inside the crop region (n_new_in_crop=2) with 0 new violations outside (n_new_out_of_crop=0). The gating criterion was connectivity preservation, not a clean DRC slate.

Do not treat "gated_in" as equivalent to "DRC clean" for V3. Moves that realign upper-metal instances (M5 and above) while displacing V3-touching cells can introduce in-crop V3 spacing or enclosure violations even when connectivity is intact (trial:i04.ug.leaf_0002.01). Any subsequent repair pass must re-check V3.S.1, V3.S.2, V3.S.3, V3.S.4, V3.M3.EN.1, and V3.M4.EN.2 within the affected crop window after a gated_in multi-instance move.

---

## V3 Width and M4 Perpendicular-Width Coupling

Rule V3.W.1 requires minimum width of 18 nm. Rule V3.M4.AUX.2 requires V3 to exactly match M4 width in the direction perpendicular to M4 length. These two constraints are jointly active on every V3 shape. In trial:i01.cu.def:VIA_VIA34_1_2_58_52.01, the V3 y-axis resize of -24 dbu was applied to two shapes in the same cell; both touched layers M3, M4, and V3. Resizing V3 without a corresponding adjustment to M4 violates V3.M4.AUX.2; the trial's net-positive rejection confirms that a unilateral V3 shrink that breaks the M4 width match is not a valid repair path. Always resize V3 and the perpendicular M4 dimension together, or verify that the post-resize V3 width still exactly matches the M4 perpendicular dimension before committing the operation.

---

## Spacing Rules: No Measured Repairs Yet, Rules Are Active

Rules V3.S.1 through V3.S.4 encode three distinct spacing regimes depending on whether the via has a 5 nm M4 end-cap (wec) or not (nec):

- V3.S.1: projection-mode spacing — 18 nm (same-track or aligned parallel), 27 nm (non-aligned parallel)
- V3.S.2: euclidean corner-to-corner between two wec vias — 23 nm
- V3.S.3: euclidean corner-to-corner between two nec vias — 30 nm
- V3.S.4: euclidean corner-to-corner between one wec and one nec via — 27 nm

No trial through iteration 4 targeted a pure V3 spacing violation as its primary objective. The only spacing-adjacent evidence is the gated_in result in trial:i04.ug.leaf_0002.01, which introduced 2 new in-crop violations after instance moves. The source of those 2 violations is not decomposed in the record, but V3 spacing rules are among the active candidates given that V3 was among the touched layers. Avoid instance moves that shift V3-bearing cells closer together along either axis without first verifying the post-move V3-to-V3 distances against all four spacing thresholds.

---

## AUX Rules: V3 Must Remain Inside the M3-M4 Intersection

Rule V3.AUX.1 requires every V3 shape to lie entirely within the intersection of M3 and M4. Any repair that moves or resizes V3 without confirming that M3 and M4 both still fully cover the resulting V3 footprint will trigger V3.AUX.1. In trial:i01.cu.def:VIA_VIA34_1_2_58_52.01, shrinking M3 along the y-axis while also shrinking V3 along the same axis produced a net increase in violations; one mechanism consistent with this outcome is that the M3 shrink removed coverage from one or both V3 shapes. Never shrink M3 to a size that no longer fully contains V3 (trial:i01.cu.def:VIA_VIA34_1_2_58_52.01).

---

## Operation-Count Guidance

The rejected trial trial:i01.cu.def:VIA_VIA34_1_2_58_52.01 used 3 operations. The accepted trial trial:i04.ug.leaf_0002.01 used 11 operations. Operation count alone does not predict acceptance; the determining factor in both cases was the net DRC delta and connectivity state, not the number of ops. Use the minimum number of operations needed to correct the target violation; multi-operation bundles that touch V3, M3, and M4 simultaneously carry demonstrated risk of introducing new violations (trial:i01.cu.def:VIA_VIA34_1_2_58_52.01).