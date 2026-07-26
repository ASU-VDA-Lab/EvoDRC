## Repair Strategy: Instance-Level Moves, Not Direct Polygon Edits

Both completed trials moved V3 geometry exclusively through `move_instance` operations rather than direct V3 polygon edits. trial:i04.ug.leaf_0003.01 applied 24 `move_instance` ops spanning six y-rows across the locus; trial:i05.ug.leaf_0003.01 applied 18 ops that combined delta-based instance adjustments with M5/M6 polygon moves. In both cases `conn_preserved=true` and `n_new_out_of_crop=0`, confirming that instance-level repositioning is the safe vehicle for V3 repair in this design.

## Instance Pairing

In trial:i04.ug.leaf_0003.01, instances that share a V3 connection were always moved to the same destination coordinates in the same trial: (i0375, i0379) → (2896, 3216); (i0531, i0527) → (13696, 3216); (i0367, i0366) → (2896, 5424); (i0426, i0435) → (13696, 5424); and so on through all six y-rows. Moving a paired set to a common snap point kept every V3 instance inside its enclosing M3 and M4 (V3.AUX.1, V3.M3.EN.1, V3.M4.EN.2) without widening or narrowing V3 shapes relative to M4 (V3.M4.AUX.2). Do not move one member of a pair without also moving its partner to the same destination.

## Snap-Point Grid

All absolute destinations used by trial:i04.ug.leaf_0003.01 are members of a two-column, six-row grid:

- x columns: 2896 dbu (left) and 13696 dbu (right)
- y rows: 3216, 5424, 7536, 9744, 11856, 14064 dbu

The alternating y-row pitch is 2208 dbu and 2112 dbu. Snapping to this grid produced zero new V3.W.1, V3.S.1, V3.S.2, V3.S.3, V3.S.4, V3.M3.EN.1, V3.M4.EN.2, V3.AUX.1, or V3.M4.AUX.2 violations. Destinations that do not land on this grid have not been tested; use these snap points when absolute repositioning is required.

## Small Delta Moves

trial:i05.ug.leaf_0003.01 used ±24 dbu y-deltas for the V3-touching instances within the same locus. Four instances moved +24 dbu (i0367, i0366, i0177, i0168, i0426, i0435, i0030, i0026) and four moved −24 dbu (i0362, i0360, i0424, i0411). These opposing-direction nudges also produced `n_new_out_of_crop=0` and no new V3 rule hits. A ±24 dbu y-adjustment is therefore a confirmed safe incremental step for fine-tuning V3 position after a coarser snap.

## No V3 Violations Were Introduced by Either Trial

The `new_in_crop_by_rule` breakdown recorded in trial:i05.ug.leaf_0003.01 attributes all 68 new in-crop violations to M1.A.1 (27), V1.M1.EN.1 (39), and M4.W.5 (2). No V3 rule appears in that breakdown. trial:i04.ug.leaf_0003.01 recorded the same aggregate count with the same zero out-of-crop result. Both trials touched V3 (field `touched_layers` includes "V3" in both records) without triggering any V3-specific check.

## M5 Assemble-Drops Do Not Affect V3

trial:i05.ug.leaf_0003.01 dropped four ops from the cu_pool (`assemble_drops`): two M5 polygon x-moves and two M5 via x-resizes. None targeted V3 shapes. The V3 outcome (zero new violations, connectivity preserved) was independent of whether those M5 ops were applied or dropped. Do not attempt to use M5 polygon or via resizes as a proxy for correcting V3 spacing or enclosure.

## V3.M4.AUX.2 Implication for Move Direction

V3.M4.AUX.2 requires V3 to match M4's width along the perpendicular-to-M4-length axis and to share exactly two coincident M4 edges. The move operations in both trials displaced V3 instances along y (the M4 length direction in this block), not along x (the perpendicular direction). Moving along the M4 length axis does not alter the perpendicular width relationship; moving along the perpendicular axis risks violating V3.M4.AUX.2. All confirmed safe moves in trial:i04.ug.leaf_0003.01 and trial:i05.ug.leaf_0003.01 were y-axis displacements.

## V3.S.1 Projection-Based Spacing and End-Cap Classification

V3.S.1 distinguishes three spacing regimes (18 nm same-track, 27 nm parallel not-aligned, 18 nm parallel aligned) via projection checks and end-cap masks. The DRC deck separates V3 instances into "no-end-cap" (nec, fully flush with M4 edges) and "with-end-cap" (wec, with ≥1 non-M4 edge) before applying masks and spacing checks. The instance moves in both trials preserved the M4 flush condition for the instances that had it, because the moves were purely translational (no shape resizes), keeping coincident-edge relationships intact. When planning a repair for V3.S.1, verify whether the violating V3 instance is nec or wec before selecting a move direction: a wec instance carries a 5 nm extended mask beyond the M4 edge, so the effective keep-out zone extends 5 nm further than the V3 polygon boundary.

## V3.S.2 / V3.S.3 / V3.S.4 Corner-to-Corner Spacing

These rules operate on Euclidean (not projection) distances between mask-expanded instances. V3.S.2 governs wec-to-wec pairs (23 nm corner-to-corner), V3.S.3 governs nec-to-nec pairs (30 nm corner-to-corner), V3.S.4 governs mixed wec/nec pairs (27 nm corner-to-corner). Neither trial introduced a corner-to-corner violation. The ±24 dbu y-delta moves in trial:i05.ug.leaf_0003.01 and the absolute grid snaps in trial:i04.ug.leaf_0003.01 maintained separation in all three regimes. When nudging V3 instances toward each other (opposing-sign deltas like the +24/−24 pair used in trial:i05.ug.leaf_0003.01), verify the post-move Euclidean corner gap against the applicable threshold (23/27/30 nm) before committing.