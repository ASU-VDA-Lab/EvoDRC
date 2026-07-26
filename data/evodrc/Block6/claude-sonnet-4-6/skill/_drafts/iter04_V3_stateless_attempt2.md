## Rule Summary

**V3.W.1** requires minimum width of 18 nm along the M4 length direction. **V3.S.1** enforces projection-based spacing: 18 nm between vias on the same M4 track, 27 nm between vias on parallel but non-aligned tracks, and 18 nm between vias on parallel aligned tracks. **V3.S.2**, **V3.S.3**, and **V3.S.4** add Euclidean corner-to-corner spacing requirements that depend on whether each via has a 5 nm M4 end-cap (wec) or no end-cap (nec): 23 nm (both wec), 30 nm (both nec), 27 nm (mixed). **V3.M3.EN.1** requires M3 to enclose V3 by at least 5 nm on at least two opposite sides. **V3.M4.EN.2** requires M4 to enclose V3 by at least 11 nm on at least two opposite sides. **V3.AUX.1** requires V3 to lie entirely within the intersection of M3 and M4. **V3.M4.AUX.2** requires V3 to exactly match M4's width in the direction perpendicular to the M4 run — V3 must share both edges with M4 on that axis (two coincident edges required). The NONORTHOGONAL rule prohibits any non-axis-aligned edge on V3.

## Observed Repair Operations

All four trials in the measured history were accepted (decision: `gated_in`, `conn_preserved: true`). No rejected trials exist in this record set.

Two repair patterns appear across the accepted trials:

**Single-instance x-axis move.** trial:i02.ug.leaf_0003.03 applied one `move_instance` operation (delta_dbu `[-16, 0]`) to instance `i0358`, touching layers M3, M4, and V3, and was accepted with one new in-crop fix and no new out-of-crop violations. trial:i04.ug.leaf_0001.00 applied an identical single `move_instance` at `[-16, 0]` to instance `i0193`, also touching M3, M4, and V3, and was accepted with one new in-crop fix. In both cases the entire M3/M4/V3 stack moved as a unit, preserving all inter-layer relationships.

**Multi-instance y-axis move batch with optional resize_end.** trial:i02.ug.leaf_0010.06 applied 36 operations across 24 `move_instance` calls (y-axis deltas of ±24 dbu and ±72 dbu) and 12 `resize_end` calls on M4 polygons (y-axis, high and low ends, deltas of +24 to +72 dbu), touching M3, M4, M5, V3, and V4, and was accepted with 26 new in-crop fixes. trial:i03.ug.leaf_0002.01 applied 20 `move_instance` operations (y-axis deltas of ±48 dbu and ±96 dbu) across 20 instances, touching M3, M4, M5, V3, and V4, and was accepted with 35 new in-crop fixes.

## Co-movement of the M3/M4/V3 Stack

Every accepted repair that touched V3 moved V3 together with M3 and M4 through `move_instance` rather than repositioning V3 geometry independently (trial:i02.ug.leaf_0003.03, trial:i04.ug.leaf_0001.00, trial:i02.ug.leaf_0010.06, trial:i03.ug.leaf_0002.01). This co-movement pattern maintains V3.AUX.1 (V3 inside M3 ∩ M4), V3.M3.EN.1 (M3 enclosure), V3.M4.EN.2 (M4 enclosure), and V3.M4.AUX.2 (exact width match perpendicular to M4 run) without requiring any independent geometry adjustment to V3 itself. All four accepted trials achieved `conn_preserved: true` using this approach.

## Move Magnitudes in Accepted Repairs

Accepted x-axis move magnitudes: −16 dbu (trial:i02.ug.leaf_0003.03, trial:i04.ug.leaf_0001.00).

Accepted y-axis move magnitudes: ±24 dbu, ±72 dbu (trial:i02.ug.leaf_0010.06); ±48 dbu, ±96 dbu (trial:i03.ug.leaf_0002.01).

Accepted `resize_end` magnitudes on M4 (y-axis): +24 dbu and +72 dbu at both high and low ends (trial:i02.ug.leaf_0010.06). These resizes occurred alongside instance moves and did not trigger new V3 violations, consistent with M4 end-cap adjustments that maintain or extend enclosure margins rather than reducing them.

## Enclosure and Spacing Context

V3.M4.EN.2 requires 11 nm M4 enclosure on at least two opposite sides. The `resize_end` operations in trial:i02.ug.leaf_0010.06 extended M4 polygon ends, which increases the M4 end-cap length. This is consistent with repairing V3.M4.EN.2 violations caused by insufficient M4 extension beyond V3 in the direction along M4. The accepted outcome (26 in-crop fixes, 0 out-of-crop violations) confirms that extending M4 ends simultaneously with repositioning instances is a valid composite repair.

V3.S.1's three spacing thresholds (18 nm same-track, 27 nm parallel not-aligned, 18 nm parallel aligned) are governed by a mask-based projection check that classifies each via as wec (with end-cap, i.e., at least one M4 edge coincident with a V3 edge) or nec (no end-cap, i.e., fully flushed by M4). The y-axis multi-instance moves in trial:i02.ug.leaf_0010.06 and trial:i03.ug.leaf_0002.01 adjusted relative via positions along the M4 track direction, directly affecting same-track and parallel-track spacing margins under V3.S.1.