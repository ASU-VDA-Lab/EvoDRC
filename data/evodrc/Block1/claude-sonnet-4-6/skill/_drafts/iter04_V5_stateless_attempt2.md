**Coordinated movement with M5 and M6**

V5 instances cannot be repositioned independently of M5 and M6. V5.AUX.1 requires V5 to lie entirely inside the intersection of M5 and M6, and V5.M6.AUX.2 requires V5 width to exactly match M6 width along the direction perpendicular to M6 length. In all three accepted trials, V5 appears in `touched_layers` alongside M5 and M6, and `move_instance` operations on V5-bearing instances are part of combined metal-via repair sets (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03, trial:i04.ug.leaf_0003.02). All three trials reached `decision: gated_in` with `conn_preserved: true`.

**Move magnitudes observed for V5-bearing instances**

In trial:i02.ug.leaf_0003.02 and trial:i04.ug.leaf_0003.02, the x-axis moves applied to V5-bearing instances are +32 dbu and -16 dbu. The same x-axis magnitudes appear in trial:i02.ug.leaf_0004.03. Combined x+y moves also occur: [32, -64], [32, -112], [-16, -64], [-16, -112] in trial:i02.ug.leaf_0003.02; [32, -96] and [-16, -96] in both trial:i02.ug.leaf_0003.02 and trial:i04.ug.leaf_0003.02. All of these were gated in.

**No V5 rule violations among recorded per-rule fix counts**

The `per_rule` new-in-crop breakdowns for trial:i02.ug.leaf_0003.02 and trial:i02.ug.leaf_0004.03 list no V5-specific rules (V5.W.1, V5.S.1, V5.S.2, V5.S.3, V5.M5.EN.1, V5.M6.EN.2, V5.AUX.1, V5.M6.AUX.2) as direct fix targets. V5 was touched in both trials as a consequence of repositioning M5 and M6, not as the primary repair target.

**Spacing constraints**

V5.S.1, V5.S.2, and V5.S.3 each require 33 nm minimum separation between V5 instances (same-net projection, different-net projection, and corner-to-corner euclidean). Neither trial:i02.ug.leaf_0003.02 nor trial:i02.ug.leaf_0004.03 records new V5 spacing violations in `per_rule` deltas, confirming that x-axis moves of +32 dbu and -16 dbu applied to V5-bearing instances in those trials did not introduce V5 spacing violations.

**Enclosure maintenance**

V5.M5.EN.1 requires M5 to enclose V5 by at least 11 nm on at least two opposite sides; V5.M6.EN.2 requires M6 to enclose V5 by at least 11 nm on two opposite sides. In all three accepted trials, M5 and M6 geometry is modified in the same operation set that moves V5 instances, keeping enclosure in step with via position (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03, trial:i04.ug.leaf_0003.02).

**Conflict resolution during assembly**

When two leaf units propose incompatible moves for the same V5-bearing instance, the assembler drops one as `external_conflict_dropped`. In trial:i02.ug.leaf_0003.02, moves for instances including i0352, i0312, i0317, i0229, i0139, i0170, i0509, i0398, i0421, i0105, i0025, i0045, i0363, i0331, i0344, i0207, i0141, i0171, i0499, i0412, i0417, i0102, i0026, i0037, i0345, and i0505 were dropped due to conflict with leaf_0004, yet the trial was still gated in. Correspondingly, trial:i02.ug.leaf_0004.03 dropped moves for many of the same instances (e.g., i0345, i0363, i0352, i0331, i0312, i0344, i0317, i0207, i0229, i0141, i0139, i0171, i0170, i0499, i0509, i0412, i0398, i0417, i0421, i0102, i0105, i0026, i0025, i0037, i0045) as `external_conflict_dropped` or `external_duplicate` and was also gated in. Partial execution of a planned move set is sufficient provided connectivity is preserved, as demonstrated by both trial:i02.ug.leaf_0003.02 and trial:i02.ug.leaf_0004.03.

**Orthogonality**

The NONORTHOGONAL rule applies to V5. All move operations in the three trials are axis-aligned or carry integer-dbu x+y components — no non-orthogonal edges are introduced. Apply only axis-aligned moves when repositioning V5 instances (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03, trial:i04.ug.leaf_0003.02).