## Operation Patterns

**Instance moves are the dominant repair operation for V1.** Across all 44 accepted trials in iterations 1 through 5, `move_instance` is the primary operation; every trial reached `decision:"gated_in"` with `conn_preserved:true`. Lateral (X) or vertical (Y) displacement of instances is a reliable V1 DRC repair strategy.

**X-axis instance displacements of 36 dbu appear most frequently** and succeed across diverse unit types and row contexts (trial:i01.ug.Block7_union_row11.01, trial:i01.ug.Block7_union_row15.05, trial:i02.ug.Block7_union_row6.08, trial:i02.ug.Block7_union_row14.01, trial:i03.ug.Block7_union_row24.05). Larger X moves of 40, 64, 72, and 108 dbu also succeed (trial:i01.ug.Block7_union_row8.20, trial:i01.ug.leaf_0002.23, trial:i01.ug.Block7_union_row7.19).

**Mixed-direction instance moves within one crop** -- some instances moving in +X, others in -X -- succeed (trial:i01.ug.Block7_union_row16.06, trial:i01.ug.Block7_union_row19.09, trial:i01.ug.Block7_union_row20.10). The solver decomposes inter-V1 spacing violations by moving both implicated instances away from each other.

**Y-axis instance displacements** succeed at 44, 52, 57, 64, and 68 dbu (trial:i01.ug.Block7_union_row14.04, trial:i01.ug.Block7_union_row19.09, trial:i04.ug.Block7_union_row13.00, trial:i04.ug.leaf_0007.05, trial:i02.ug.leaf_0032.17).

## Polygon Resize When Instances Move in X

**When a V1-hosting instance moves in X and a connecting M2 polygon spans from that instance to a non-moved anchor, resize the polygon's nearest endpoint with `resize_end` to maintain V1.AUX.1 and V1.M2.EN.2 compliance.** In trial:i01.ug.Block7_union_row3.15, instance i1623 moves -36 in X and polygon p3379 has its high-X end resized +49. In trial:i01.ug.leaf_0002.23, instance i1646 moves +72 in X and polygon p3695 has its high-X end resized +128. In trial:i01.ug.leaf_0008.24, instance i1968 moves +108 in X and polygon p3771 has its high-X end resized +164.

**The resize magnitude is not equal to the instance move delta.** In trial:i01.ug.Block7_union_row3.15 the instance moves 36 dbu while the polygon end extends 49 dbu; in trial:i01.ug.leaf_0002.23 the instance moves 72 dbu while the polygon end extends 128 dbu. The polygon resize must satisfy V1.M2.EN.2's 5 nm minimum enclosure on both sides of V1, not merely restore prior overlap.

**Both ends of a bridging M2 polygon may require simultaneous resize** when two anchors move in opposite X directions. In trial:i04.ug.leaf_0001.01, polygon p3297 has its low-X end resized -40 while polygon p3696 has its high-X end resized +108, coordinated with instance moves of +108 and +60 dbu.

## Polygon Move When Instances Move in Y

**When a V1-hosting instance moves in Y and a connecting M2 polygon spans between two co-moving instances, move the polygon by the same Y delta as the instances.** In trial:i04.ug.leaf_0007.05, instances i0794 and i0810 both move y+68 and polygon p3631 is moved y+68 via a polygon `move` operation. In trial:i03.ug.Block7_union_row17.02, the same polygon p3631 was moved y+57 when instances i0794 and i0810 moved y+57. Applying the instance delta directly to the connecting polygon maintains V1.AUX.1 (V1 inside M2) and V1.M2.EN.2 enclosure.

**When only one end of a Y-spanning M2 polygon must track an instance that moves in Y, apply `resize_end` on the relevant axis end.** In trial:i01.ug.Block7_union_row14.04, instances i0894 and i0920 move y+64 and polygon p3576 has its high-Y end resized +64. In trial:i05.ug.leaf_0004.04, instance i0920 moves y+64 and polygon p3576 has its low-Y end resized -64. The choice of which end to resize depends on which end of the polygon connects to the moved instance.

## V1.AUX.1: V1 Inside M1 and M2

Every trial that touched V1 also touched M1 and M2 in the same operation set (all 44 trials across iterations 1-5). No trial repaired V1 violations by operating on V1 geometry alone; all accepted repairs repositioned V1-hosting instances together with their enclosing M1 and M2 metal. This confirms that V1.AUX.1 (V1 must be inside M1 and M2) requires coordinated movement: moving a V1 instance without updating the surrounding metal, or extending metal without moving the V1 instance, each risks violating containment or enclosure rules.

## V1.M2.AUX.2: V1 Width Must Match M2 Width

V1.M2.AUX.2 requires V1 to be exactly the same width as M2 in the direction perpendicular to M2 length. Repairs that combined instance moves with M2 polygon resizes along the same axis satisfied this constraint (trial:i01.ug.Block7_union_row12.02, trial:i04.ug.leaf_0001.01). No trial resized V1 geometry independently of its host instance, consistent with V1 dimensions being determined by the instance footprint.

## V1.M1.EN.1 and V1.M2.EN.2 Enclosure

Enclosure violations at V1 are repaired by two strategies, both documented in the history:

Moving the V1-hosting instance into enclosing M1 or M2 metal: trial:i01.ug.Block7_union_row20.10 (instances moved +36 to +40 dbu in X), trial:i01.ug.Block7_union_row7.19 (i1446 moves +108, i1442 moves +40).

Extending M2 metal to cover the V1 instance: trial:i01.ug.Block7_union_row10.00 (polygon p3305 resized +50 on high-X end alongside instance moves), trial:i04.ug.leaf_0001.01 (polygon p3696 resized +108 on high-X end, coordinated with instance moves).

V1.M2.EN.2 accepts either 5 & 5 nm or 5 & 0 nm enclosure on opposite sides, giving two valid configurations when placing a V1 relative to an M2 endpoint. V1.M1.EN.1 requires 5 nm on one pair of opposite sides and 2 nm on the other.

## Multi-Layer Fix Scope

Several trials required simultaneous changes to M3 and V2 in addition to M1, M2, and V1 (trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row13.03, trial:i01.ug.Block7_union_row14.04, trial:i01.ug.Block7_union_row9.21, trial:i02.ug.leaf_0023.16, trial:i03.ug.Block7_union_row17.02, trial:i04.ug.Block7_union_row13.00). Multi-layer coordinated moves are a valid repair strategy; all such trials remain `conn_preserved:true`.

## Iteration Convergence

Iterations 1 and 2 cover 22 and 12 crop windows respectively; by iter:5 only 2 trials remain (trial:i05.ug.leaf_0003.03, trial:i05.ug.leaf_0004.04). V1 violations concentrate in a shrinking set of residual leaf units as the design state converges across iterations.