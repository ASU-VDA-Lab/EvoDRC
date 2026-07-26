## V3 Geometry Constraints

**V3.W.1** sets the minimum V3 width at 18 nm measured along the M4 length direction.

**V3.AUX.1** requires V3 to lie entirely within the intersection of M3 and M4. **V3.M4.AUX.2** adds that V3's dimension perpendicular to the M4 length must exactly match M4's width in that direction — not merely be enclosed, but be coincident on at least two opposite edges inside M4.

**V3.M3.EN.1** requires M3 to enclose V3 by at least 5 nm on at least two opposite sides. The deck checks this using `m3.sized(-5.nm, 0)` and `m3.sized(0, -5.nm)` — V3 must pass at least one of these containment tests.

**V3.M4.EN.2** requires M4 to enclose V3 by at least 11 nm on at least two opposite sides, checked via `m4.sized(-11.nm, 0)` and `m4.sized(0, -11.nm)`.

**V3.S.1** spacing depends on the M4 end-cap classification. The rule distinguishes v3_nec (V3 whose edges are all coincident with M4 edges — no end-cap) from v3_wec (V3 with at least one non-coincident edge — with end-cap). Three cases: 18 nm projected between instances on the same M4 track; 27 nm projected between instances on parallel non-aligned tracks; 18 nm projected between instances on parallel aligned tracks. The spacing check operates on derived mask layers, not directly on V3 outlines.

**V3.S.2** sets a 23 nm minimum euclidean corner-to-corner spacing when both V3 instances are v3_wec (5 nm M4 end-cap present). Violations are those euclidean violations not overlapping any projection violation.

**V3.S.3** sets a 30 nm minimum euclidean corner-to-corner spacing when both V3 instances are v3_nec (no M4 end-cap). Same projection-exclusion logic.

**V3.S.4** sets a 27 nm minimum euclidean separation between one v3_wec and one v3_nec instance.

The NONORTHOGONAL block prohibits any V3 edge at angles other than 0° or 90°.

## Observed Repair Behavior

Both recorded trials touched V3 as part of coordinated multi-layer moves. In trial:i04.ug.leaf_0003.01, 24 move_instance operations repositioned V3-touching cells to absolute coordinates, always in pairs (two instance IDs moved to the same target coordinate per row). Touched layers included M3, M4, and V3. The trial was gated in with connectivity preserved and zero new out-of-crop violations.

In trial:i05.ug.leaf_0003.01, V3-touching instances received delta y-axis moves of +24 dbu or −24 dbu applied symmetrically in opposing pairs (e.g., instances i0367 and i0366 at +24 dbu, instances i0362 and i0360 at −24 dbu). Touched layers included M3, M4, M5, M6, V3, V4, and V5. The per-rule breakdown records new in-crop violations only for M1.A.1 (27), M4.W.5 (2), and V1.M1.EN.1 (39) — no V3 rule appears in that list. The trial was gated in with connectivity preserved.

Move V3 instances in matched pairs rather than individually. Both trials that modified V3 applied paired moves — same absolute target in trial:i04.ug.leaf_0003.01, symmetric delta magnitudes in trial:i05.ug.leaf_0003.01 — and neither introduced V3 violations.

Always co-move the associated M4 shapes when repositioning V3. Both trials touched M4 whenever they touched V3 (trial:i04.ug.leaf_0003.01, trial:i05.ug.leaf_0003.01), consistent with the V3.M4.AUX.2 requirement that V3 width perpendicular to M4 length must exactly equal M4's width. Moving V3 without M4 would violate that exact-match constraint.

Do not move V3 without also verifying M3 enclosure. Both trials touched M3 alongside V3 (trial:i04.ug.leaf_0003.01, trial:i05.ug.leaf_0003.01), and neither produced a V3.M3.EN.1 failure, confirming that joint M3+V3 adjustment maintains the 5 nm opposite-side enclosure.