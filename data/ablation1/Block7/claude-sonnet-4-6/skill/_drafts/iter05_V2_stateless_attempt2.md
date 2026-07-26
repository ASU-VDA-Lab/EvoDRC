## Operation Patterns

**Single-instance V2 moves are the primary accepted repair operation.** Trials that touch only M2, M3, and V2 — with a single `move_instance` on the via cell — are consistently accepted: trial:i02.ug.leaf_0010.13 (delta [0,−36] dbu), trial:i03.ug.leaf_0002.07 (delta [0,+36] dbu), trial:i04.ug.leaf_0002.02 (delta [−36,0] dbu), and trial:i05.ug.leaf_0001.01 (delta [+36,0] dbu). All four carry `decision: gated_in` and `conn_preserved: true`. Moving the V2 instance co-moves its M2 and M3 hosts, preserving V2.AUX.1 (V2 inside M2 and M3), V2.M2.EN.1, V2.M3.EN.2, and V2.M3.AUX.2 without any independent polygon surgery.

**Observed move deltas are multiples of 36 dbu in X and Y.** Across all V2-touching single-via trials the step sizes are 36 dbu (trial:i02.ug.leaf_0010.13, trial:i03.ug.leaf_0002.07, trial:i04.ug.leaf_0002.02, trial:i05.ug.leaf_0001.01). Multi-layer trials also use 36 or 56 dbu X steps (trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row9.21) and 52 or 57 dbu Y steps (trial:i01.ug.Block7_union_row19.09, trial:i03.ug.Block7_union_row19.03, trial:i04.ug.leaf_0008.06). Use grid-aligned steps rather than arbitrary sub-grid offsets.

## Via Shape Resize on M3 Is Rejected

**Do not resize the M3 shape of a via cell to repair V2 violations.** Trial trial:i02.cu.def:VIA_VIA23_1_3_36_36.00 applied `resize_via_shape` to the M3 layer of cell VIA_VIA23_1_3_36_36, shrinking it by 40 dbu in the Y direction. The result was `decision: rejected_net_positive` with zero net reduction in violations across all inspected windows. Shrinking M3 risks violating V2.M3.EN.2 (which requires M3 to enclose V2 by 5 nm on two opposite sides) and V2.M3.AUX.2 (which requires V2 width to match M3 width perpendicular to M3 length). Do not reduce via-cell M3 extent as a repair strategy.

## Multi-Layer Co-Moves

**When V2 violations co-locate with M1/M3/V1 congestion, coordinated multi-instance moves of all affected layers together are accepted.** Trials trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row13.03, trial:i01.ug.Block7_union_row14.04, trial:i01.ug.Block7_union_row19.09, and trial:i01.ug.Block7_union_row9.21 all move 3–9 instances spanning M1, M2, M3, V1, and V2 simultaneously and are accepted. The key constraint is that V2 instances must travel with their enclosing M2 and M3 shapes to keep V2.AUX.1 satisfied; independent movement of V2 without its host metal is not observed in any accepted trial.

**Polygon resize_end operations on M3 or M2 polygons accompanying V2 instance moves are accepted** when the resize keeps the via inside the metal. Trial trial:i04.ug.leaf_0001.01 resizes M3 (p3696 high-X end +108 dbu) and M2 (p3297 low-X end −40 dbu, p2719 high-Y end −12 dbu) while moving V2-touching instances, all accepted. Trial trial:i01.ug.Block7_union_row13.03 resizes M3 polygon p3526 high-X end +4 dbu while moving four instances, accepted. These accompany instance moves rather than acting as standalone repairs.

## Spacing Rule Context

**V2.S.1 spacing depends on M3 end-cap configuration.** The rule distinguishes same-track (18 nm), parallel not-aligned (27 nm), and parallel aligned (18 nm) cases via the `v2_nec`/`v2_wec` mask logic. Move operations observed in accepted trials reposition V2 instances by 36–57 dbu steps, consistent with clearing these spacing thresholds: 18 nm = 180 dbu at 0.1 nm/dbu; a 36 dbu step equals 3.6 nm, so multi-step moves of 108–576 dbu correspond to 10.8–57.6 nm clearance adjustments. Co-moving the M3 segment with the V2 instance preserves the end-cap classification (nec/wec) of the via after the move.

**V2.S.2 (23 nm corner-to-corner, both vias with 5 nm end-cap) and V2.S.3 (30 nm corner-to-corner, both without end-cap) are addressed by the same instance-move strategy.** No trial attempts polygon-level corner clipping or sizing on V2 directly. All corner-spacing violations in the history are resolved by moving the via cell instance, which simultaneously shifts all edges of V2 and its M3 end-cap extension.

## Enclosure Rules

**V2.M2.EN.1 requires 5 nm enclosure on at least two opposite sides; co-moving V2 with M2 preserves this.** Every accepted trial that touches V2 also touches M2 (all entries in the touched_layers arrays include both). No trial moves V2 without M2; do not attempt to move V2 independently of its M2 host.

**V2.M3.EN.2 requires 5&5 nm or 5&0 nm enclosure by M3 on two opposite sides; shrinking M3 violates it.** The rejected trial trial:i02.cu.def:VIA_VIA23_1_3_36_36.00 demonstrates that reducing M3 extent around the via cell produces no net improvement and is refused. All accepted trials keep M3 and V2 moving as a unit.

**V2.M3.AUX.2 fixes require strict width matching.** V2 must equal M3 width perpendicular to M3 length. No accepted trial resizes V2 width independently of M3. The only safe approach observed is moving the via cell instance (which carries fixed internal V2-to-M3 geometry), not resizing individual V2 or M3 polygon edges.

## Connectivity Constraint

**All accepted V2 repairs preserve connectivity (`conn_preserved: true`).** This is a hard filter: every trial in the history that is `gated_in` carries `conn_preserved: true`. The rejected trial trial:i02.cu.def:VIA_VIA23_1_3_36_36.00 also carries `conn_preserved: true` but is rejected on net-positive grounds (violation count did not improve). Do not apply any V2 repair that breaks connectivity; the gate will reject it regardless of DRC improvement.