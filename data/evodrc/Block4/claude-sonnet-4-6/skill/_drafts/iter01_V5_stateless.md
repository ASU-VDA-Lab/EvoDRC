## Repair Strategy

The sole measured trial for V5 at iteration 1 is trial:i01.ug.leaf_0025.11 (Block4, unit_gate channel, leaf_0025). Two instances (i0234, i0305) were moved together by delta [0, 64] dbu in the Y axis only; the operation touched layers M5, M6, and V5 simultaneously, preserved connectivity (conn_preserved=true), and was accepted (decision=gated_in). All prescriptive guidance below is grounded exclusively in this record.

---

## Layer Coupling: V5 Must Move with M5 and M6

V5 is structurally coupled to both M5 and M6. Rule V5.AUX.1 requires every V5 polygon to lie inside the intersection of M5 and M6. Rule V5.M6.AUX.2 additionally requires V5 to match M6 exactly in the width direction perpendicular to M6 length (V5 edges must be coincident with M6 edges on at least two sides). Rule V5.M5.EN.1 and V5.M6.EN.2 each require 11 nm enclosure on two opposite sides.

Because of these geometric constraints, any positional change to a V5 instance that does not carry its enclosing M5 and M6 shapes along with it will break V5.AUX.1 or V5.M6.AUX.2 immediately. The accepted move in trial:i01.ug.leaf_0025.11 touches all three layers (M5, M6, V5) for each instance moved, which is consistent with keeping V5 inside its M5/M6 envelope throughout the operation. Do not move V5 in isolation; always include the associated M5 and M6 geometry in the same operation.

---

## Paired Instance Moves Preserve Connectivity

When two instances share a common net through the V5/M5/M6 stack, moving them by the same delta vector preserves the net topology. In trial:i01.ug.leaf_0025.11, i0234 and i0305 each received delta [0, 64] dbu, and the result was conn_preserved=true. Apply the same delta to all instances that are part of the same routed net segment rather than moving one instance and leaving the other fixed.

---

## Width and Enclosure Budget Under a Y-Axis Move

Rule V5.W.1 sets minimum V5 width at 24 nm along the M6 length direction. Rules V5.M5.EN.1 and V5.M6.EN.2 each set 11 nm enclosure on two opposite sides. A pure Y-axis translation (as in trial:i01.ug.leaf_0025.11, delta [0, 64]) leaves the V5 polygon shape unchanged and therefore cannot by itself violate V5.W.1 or alter the relative X-axis enclosure of M5/M6 around V5. The 64 dbu Y move was accepted without triggering enclosure failures in that trial. A Y-axis move is therefore a lower-risk repair direction than an X-axis move when the enclosure margins are near the 11 nm minimum, because it does not compress or expand the sides that the enclosure rule measures.

---

## Spacing Rules (V5.S.1, V5.S.2, V5.S.3)

All three spacing rules share the same 33 nm threshold — same-net projection (V5.S.1), different-net projection (V5.S.2), and corner-to-corner euclidean (V5.S.3). A move that brings any two V5 instances within 33 nm (by projection or corner-to-corner) will trigger one of these rules regardless of net membership. In trial:i01.ug.leaf_0025.11 the move resulted in 9 new in-crop violations; the decision was gated_in because connectivity was preserved, not because the DRC count was zero. Do not interpret a gated_in outcome as implying zero new spacing violations: the trial record shows new violations can appear in-crop and the operation is still accepted when conn_preserved is the gating criterion. Verify post-move V5-to-V5 spacing against the 33 nm floor when the move reduces inter-instance distance.

---

## Nonorthogonal Geometry

The NONORTHOGONAL block applies to V5. Any edge with angle outside {0, 90, 180, 270} degrees fires a GEOMETRY.NONORTHOGONAL violation. The move operation in trial:i01.ug.leaf_0025.11 used integer dbu deltas [0, 64] — a purely axial translation that cannot introduce diagonal edges on a rectangle. Always express V5 move deltas as axis-aligned integer dbu values; do not use rotations or shear transforms on V5 geometry.

---

## Summary of Constraints to Check After Any V5 Repair

Based on the DRC rules and the single accepted trial (trial:i01.ug.leaf_0025.11):

- V5.AUX.1: Confirm V5 remains inside M5 and M6 after move.
- V5.M6.AUX.2: Confirm V5 edges are coincident with M6 edges in the width-perpendicular direction.
- V5.M5.EN.1 / V5.M6.EN.2: Confirm at least two opposite sides retain >= 11 nm enclosure by M5 and M6 respectively.
- V5.W.1: Confirm V5 width along M6 length direction is >= 24 nm.
- V5.S.1 / V5.S.2 / V5.S.3: Confirm all V5-to-V5 distances are >= 33 nm (projection and corner-to-corner).
- GEOMETRY.NONORTHOGONAL: Use only axis-aligned integer dbu deltas.