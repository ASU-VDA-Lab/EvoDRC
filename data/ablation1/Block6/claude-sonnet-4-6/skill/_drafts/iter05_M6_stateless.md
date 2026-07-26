## V5.M6.AUX.2: Y-axis V5 resize is the correct fix; x-axis adjustments are inferior

V5.M6.AUX.2 fires when a V5 via sits inside M6 but its width perpendicular to the M6 run direction does not exactly match the M6 extent in that direction — the rule requires V5 edges to be coincident with M6 edges on at least two opposite sides. The measured record establishes a clear ranking between fix strategies applied to cell VIA_VIA56_2_2_66_58.

Resize V5 shapes in the y-axis (perpendicular to M6 length) to fix V5.M6.AUX.2. Trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 (group "v5_m6_aux2_fix") resized all four V5 shapes in y by +248 dbu each, achieved delta_total = −32 across windows leaf_0019 and leaf_0020, and was applied. This directly extends V5 edges in the axis required by the AUX.2 coincidence check.

Do not substitute x-axis moves paired with x-axis resizes when V5.M6.AUX.2 is the target violation. Trial:i01.cu.def:VIA_VIA56_2_2_66_58.01 applied x-axis moves of ±116 dbu and x-axis resizes of +320 dbu to the same four shapes, achieved only delta_total = −16, and lost the tournament. The y-axis strategy (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02) produced twice the reduction and was chosen over the x-axis strategy (trial:i01.cu.def:VIA_VIA56_2_2_66_58.01).

## Apply the same resize delta uniformly to all V5 shapes in the via cell

Both tournament candidates for VIA_VIA56_2_2_66_58 operated on all four shape indices (0, 1, 2, 3) with identical per-axis deltas: trial:i01.cu.def:VIA_VIA56_2_2_66_58.01 used the same ±116 dbu move and +320 dbu x-resize on every shape, and trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 used the same +248 dbu y-resize on every shape. Apply a uniform delta across all shapes in the cell when correcting V5.M6.AUX.2 in standard via array cells.

## M6 polygon y-moves: 32 dbu grid increments and asymmetric pair correction

In trial:i05.ug.leaf_0003.01 (decision: gated_in, iter 5), the m6_fix group moved M6 polygon p2107 by +32 dbu in y and M6 polygon p2106 by −16 dbu in y. M6.AUX.1 mandates that M6 horizontal edges fall on a 32 nm grid; the +32 dbu move on p2107 is an exact multiple of that grid and preserves any on-grid edges that p2107 already had. The −16 dbu move on p2106 corrects a starting offset of 16 dbu (half the AUX.1 pitch), restoring that polygon's edges to the required 32 nm grid; the trial was gated_in without reported M6.AUX.1 violations, confirming the correction succeeded.

The asymmetric pairing (+32 on one polygon, −16 on the adjacent polygon) moves the two polygons apart in y by a combined 48 dbu while preserving approximate vertical centering of the pair. This pattern addresses situations where two adjacent M6 polygons violate M6.S.1 (minimum 32 nm vertical spacing between M6 edges) while both require independent grid re-alignment.

## Instance moves must accompany M6 polygon repositioning

When M6 polygons are repositioned under m6_fix, all connected via and sub-cell instances must move by matching deltas to preserve stack geometry. In trial:i05.ug.leaf_0003.01, the M6 polygon moves (+32 dbu on p2107 and −16 dbu on p2106) were accompanied by moves of eight directly associated instances (i0384 and i0528 by [0, +32]; i0173 and i0027 by [0, −16]) under the same m6_fix group, plus ten additional instance moves at ±24 dbu outside the group. The trial was gated_in; omitting the instance moves when repositioning M6 polygons would risk introducing V5.M6.EN.2 or V5.M6.AUX.2 violations at the via landing pads above and below M6, or V6.M6.EN.1 violations at the V6 landing on top of M6.

## M5 x-axis operations touch M6 as a passenger layer

Trial:i05.cu.def:VIA_VIA45_1_2_58_58.00 (applied, delta_total = −2) moved M5 polygons p1683 (+32 dbu x) and p1682 (−16 dbu x) and resized the V5 shape in cell VIA_VIA56_2_2_66_58 on the M5 layer by −64 dbu in x, under the m5_fix group. M6 appears in touched_layers for this trial, but the operations are M5/V5 x-axis adjustments and the total violation reduction is 2 — with leaf_0002 showing zero change and leaf_0003 carrying the full reduction. Direct M6 DRC benefit from standalone M5/V5 x-resize operations is minimal; substantive M6 violation reduction requires either direct M6 polygon repositioning (as in trial:i05.ug.leaf_0003.01) or V5 y-axis resizing targeting V5.M6.AUX.2 (as in trial:i01.cu.def:VIA_VIA56_2_2_66_58.02).

## assemble_drops: already-applied cu_pool ops are excluded from unit-gate assemblies

Trial:i05.ug.leaf_0003.01 records assemble_drops for four m5_fix operations that had already been applied by the cu_pool channel (confirmed by reason "cu_pool:applied"). These dropped ops included x-axis moves of M5 polygons p1682 and p1683 and x-axis resizes of M5 shapes in VIA_VIA45_1_2_58_58 and VIA_VIA56_2_2_66_58. The M6-touching m5_fix ops that were dropped in the unit-gate assembly correspond exactly to the ops applied in trial:i05.cu.def:VIA_VIA45_1_2_58_58.00, which shared the same design_state as the unit-gate trial's base. Do not re-apply cu_pool-sourced m5_fix or m6_fix ops in unit-gate assemblies when those ops are already recorded as applied at the cu_pool channel for the same design state.