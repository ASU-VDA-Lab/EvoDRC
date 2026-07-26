## Grid Alignment (M5.AUX.1)

Rule M5.AUX.1 requires all M5 vertical edges to land on a 24 nm pitch grid. Instance moves or polygon shifts whose x-component is not an integer multiple of 24 dbu break this alignment. Trial i02.ug.leaf_0004.03 introduced 12 new M5.AUX.1 violations when M5 polygons p1143 and p1142 were moved +32 dbu and -16 dbu along the x-axis respectively; neither delta is divisible by 24, so every previously on-grid vertical edge in those shapes moved off-grid. All x-axis M5 moves must therefore use deltas that are multiples of 24 dbu to avoid M5.AUX.1 violations. The -16 dbu and +32 dbu x-deltas applied by leaf_0004 in trial i02.ug.leaf_0004.03 are the direct measured cause of those 12 new violations.

## No-Bend Constraint (M5.AUX.3)

Rule M5.AUX.3 prohibits M5 geometry from bending; it fires on any M5 corner subtending an angle between 0 and 90 degrees. Trial i02.ug.leaf_0004.03 introduced 38 new M5.AUX.3 violations, the single largest M5 rule contribution in that trial. The triggering ops were instance moves that carried non-zero y-components alongside their x-components (for example, [32, 32], [32, 72], [32, 24], [32, -24], [32, -72], [-16, 32], [-16, 72], [-16, 24], [-16, -24], [-16, -72] dbu), applied to instances i0345, i0505, i0363, i0352, i0331, i0312, i0344, i0317, i0207, i0229, i0141, i0139, i0171, i0170, i0499, i0509, i0412, i0398, i0417, i0421, i0102, i0105, i0026, i0025, i0037, i0045. Moving a routing instance by a vector with both x and y non-zero creates a bend in any M5 segment that spans the instance boundary. Instance moves intended to repair M5 must use pure x-axis or pure y-axis deltas; combined-axis moves directly generate M5.AUX.3 violations at every affected boundary (trial i02.ug.leaf_0004.03).

## Minimum Vertical Width (M5.W.5)

Rule M5.W.5 sets the minimum vertical (y-direction) width of M5 at 44 nm. Trial i02.ug.leaf_0004.03 introduced 12 new M5.W.5 violations. The M5 y-axis polygon moves executed in trial i02.ug.leaf_0003.02—polygon p1561 shifted -96 dbu, p1562 shifted -112 dbu, p1563 shifted -64 dbu—reduced the effective vertical spans of those shapes. The cross_crop_first_wins rule prevented leaf_0004's competing +32 dbu correction on p1561 from applying (trial i02.ug.leaf_0004.03 assemble_drops), locking in the -96 dbu shift from leaf_0003. When large negative y-axis polygon moves shrink vertical M5 extent below 44 dbu (44 nm), M5.W.5 fires. Verify the post-move bounding-box height of any M5 polygon receiving a y-axis shift before committing the delta.

## Tip-to-Tip Spacing (M5.S.4)

Rule M5.S.4 requires a minimum tip-to-tip gap of 40 nm between M5 segments on adjacent tracks that share a parallel run length. Trial i02.ug.leaf_0004.03 introduced 4 new M5.S.4 violations. The operative moves were instance moves carrying both x and y components (as enumerated above), which repositioned M5 segment endpoints relative to neighboring segments and created tip conflicts at the new positions. Pure x-axis instance moves (as executed for many instances in trial i02.ug.leaf_0003.02 that did not generate M5.S.4 violations) do not inherently create new tip-to-tip conflicts, whereas mixed-axis moves that shift segment ends in both dimensions can bring tips into proximity on adjacent tracks.

## V4 Width Match (V4.M5.AUX.2)

Rule V4.M5.AUX.2 requires each V4 via to span exactly the same width as M5 in the direction perpendicular to M5's length. Trial i02.ug.leaf_0003.02 introduced 4 new V4.M5.AUX.2 violations. The causal ops were asymmetric x-axis M5 polygon moves: p1145 and p1143 moved +32 dbu while p1144 and p1142 moved -16 dbu. When M5 horizontal extent changes by different amounts on different polygons, V4 cells whose shapes were previously flush with both M5 edges lose that flush relationship on one or both sides, breaking the exact-width requirement. Symmetric x-axis resizes that maintain the same total M5 horizontal span are required to preserve V4.M5.AUX.2 compliance; asymmetric shifts that alter net M5 width cause V4 mismatch violations. Via resize in the y-axis direction on the via cell itself—as done in trial i01.cu.def:VIA_VIA45_1_2_58_58.01 (resize_via_shape, axis=y, delta=-88 dbu)—resolved via-related violations without disturbing x-axis M5 edge positions and did not generate any V4.M5.AUX.2 violations.

## Via Shape Resize in Y-Axis (V4.M5.EN.2, V5.M5.EN.1 context)

The cu_pool operation on cell VIA_VIA45_1_2_58_58 (trial i01.cu.def:VIA_VIA45_1_2_58_58.01) resized the M5 via shape on the y-axis by -88 dbu and achieved a net reduction of 52 violations (26 each in leaf_0034 and leaf_0035) with conn_preserved=true and no new violations introduced. This demonstrates that reducing M5 extension beyond V4 in the vertical direction is a safe, effective repair when the via shape has excess y-extent. The y-axis shrink avoided any perturbation to horizontal M5 edge positions, leaving M5.AUX.1 and V4.M5.AUX.2 unaffected.

## Assembly Conflict Resolution Between Leaves

When two leaves claim the same instance or polygon in the same iteration, the assembler applies cross_crop_first_wins and external_conflict_dropped rules to select one. In trial i02.ug.leaf_0004.03, 41 ops survived to application after leaf_0003's competing ops were assigned priority on shared polygons (p1143, p1142, p1561) and shared instances. The surviving leaf_0004 ops—specifically the combined-axis instance moves—were the direct source of M5.AUX.3 and M5.AUX.1 violations. When leaf_0003 and leaf_0004 both claimed the same instances with differing y-components, the conflict was resolved by dropping one set entirely; the winning set (leaf_0004's mixed-axis moves) still applied and created violations. This means inter-leaf conflicts at shared instances do not prevent violation introduction by the surviving leaf's ops.

## Gate Policy for In-Crop Violations

Trials i02.ug.leaf_0003.02 (80 new in-crop violations) and i02.ug.leaf_0004.03 (47 new in-crop violations) were both accepted with decision gated_in. In both cases conn_preserved=true and n_new_out_of_crop=0. The gate policy accepts operations that introduce new DRC violations inside the crop boundary provided that connectivity is preserved and no violations are created outside the crop. M5 violations introduced under this policy—including M5.AUX.1, M5.AUX.3, M5.W.5, M5.S.4, and V4.M5.AUX.2 from trial i02.ug.leaf_0004.03—remain in the design and must be resolved in subsequent iterations; they are not auto-reverted.

## Routing Track Alignment (M5.AUX.2)

Rule M5.AUX.2 requires minimum-width M5 tracks to lie on vertical routing tracks at a spacing of 192 dbu pitch with a 48 dbu offset. M5 shapes that are minimum-width (identified by the rule as shapes that survive the -13 nm / +13 nm horizontal erosion-dilation) must have their centerlines at positions satisfying (cl - 48) mod 192 == 0 in x. X-axis polygon moves that are not multiples of 192 dbu will displace minimum-width M5 tracks off valid routing positions. The 32 dbu and -16 dbu moves applied in trials i02.ug.leaf_0003.02 and i02.ug.leaf_0004.03 are not multiples of 192 and would move any minimum-width M5 polygon off-track (though no M5.AUX.2 violations appeared in the recorded per-rule deltas for those trials, indicating the moved polygons p1143-p1145 were not minimum-width shapes under that rule's classification).

## Wide M5 Track Edge Constraint (M5.AUX.4)

Rule M5.AUX.4 prohibits the outside vertical edges of wide M5 polygons from aligning with any minimum-width M5 routing track edge. Wide M5 shapes (those surviving a -13 nm horizontal erosion) must not have vertical edges that coincide with the vertical bands of neighboring minimum-width M5 tracks. X-axis moves of wide M5 polygons must account for the positions of all adjacent minimum-width M5 routing tracks to avoid inadvertent alignment.

## Horizontal Width Constraints (M5.W.1, M5.W.2, M5.W.3, M5.W.4)

No M5.W.1, M5.W.2, M5.W.3, or M5.W.4 violations were introduced or resolved in any recorded trial. The x-axis polygon moves of 32 dbu and -16 dbu in trials i02.ug.leaf_0003.02 and i02.ug.leaf_0004.03 did not push any M5 shape below the 24 nm horizontal minimum (M5.W.1), above the 480 nm horizontal maximum (M5.W.2), or onto a forbidden even-multiple width (M5.W.3) or even-track-count width (M5.W.4). These constraints remain clean across all recorded operations.

## Horizontal and Vertical Spacing (M5.S.1, M5.S.2, M5.S.3, M5.S.5)

No M5.S.1, M5.S.2, M5.S.3, or M5.S.5 violations were introduced or resolved in any recorded trial. The instance moves and polygon moves in all trials did not create horizontal gaps below 24 nm between M5 shapes (M5.S.1), vertical gaps below 40 nm (M5.S.2 or M5.S.3), or adjacent-track parallel run lengths below 44 nm (M5.S.5). These rules were not perturbed by any recorded operation.