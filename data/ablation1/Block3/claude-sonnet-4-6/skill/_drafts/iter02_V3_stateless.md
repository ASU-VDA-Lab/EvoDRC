Scanning the DRC rules and both history records to write the knowledge body.

---

## Observed repair patterns touching V3

Both accepted trials that modified V3-adjacent geometry used instance moves along the y-axis and, in one case, a polygon resize along the x-axis (trial:i02.ug.leaf_0003.02). Neither trial produced any V3-named DRC violation in the measured delta output. The operations in trial:i02.ug.leaf_0002.01 moved instances ±48 dbu and ±96 dbu (4.8 nm and 9.6 nm) in y; the operations in trial:i02.ug.leaf_0003.02 moved instances ±24 dbu and +72 dbu (2.4 nm and 7.2 nm) in y and also extended polygon p1059 by 64 dbu (6.4 nm) at the low x-end and 320 dbu (32 nm) at the high x-end.

## V3.W.1 — Minimum width 18 nm

V3.W.1 requires every V3 instance to be at least 18 nm wide along the M4 length direction. Neither trial:i02.ug.leaf_0002.01 nor trial:i02.ug.leaf_0003.02 reported a V3.W.1 violation despite both touching the V3 layer, indicating the instance moves and the x-axis resize of p1059 in trial:i02.ug.leaf_0003.02 did not narrow any V3 shape below 18 nm. When resizing a polygon that intersects or neighbors V3, confirm the V3 width in the M4 length direction remains ≥ 18 nm after the operation.

## V3.S.1 — Minimum spacing (same-track / parallel-track / aligned)

V3.S.1 enforces context-dependent minimum spacing: 18 nm for vias on the same M4 track or on aligned parallel tracks, 27 nm for non-aligned parallel tracks. The rule operates on v3_mask geometries derived from whether V3 has a full-flush M4 coincident edge (NEC, no end-cap) or not (WEC, with 5 nm end-cap extension). Neither trial:i02.ug.leaf_0002.01 nor trial:i02.ug.leaf_0003.02 triggered V3.S.1 violations, even after the y-axis instance moves closed or opened inter-via gaps. Do not rely on this observation alone as a spacing clearance bound; the absolute minima from the rule (18 nm same-track, 27 nm non-aligned) remain binding.

## V3.S.2, V3.S.3, V3.S.4 — Corner-to-corner spacing

These rules check euclidean spacing not covered by projection-based V3.S.1: 23 nm corner-to-corner when both vias carry a 5 nm M4 end-cap (V3.S.2), 30 nm when neither does (V3.S.3), 27 nm for one-with / one-without (V3.S.4). No violations from either rule were recorded in trial:i02.ug.leaf_0002.01 or trial:i02.ug.leaf_0003.02. The x-axis resize in trial:i02.ug.leaf_0003.02 extended p1059 by 32 nm at the high end without triggering V3.S.2, V3.S.3, or V3.S.4, indicating sufficient diagonal clearance remained after that resize.

## V3.M3.EN.1 — M3 enclosure ≥ 5 nm on two opposite sides

V3.M3.EN.1 requires M3 to enclose V3 by at least 5 nm on either the left/right pair or the top/bottom pair. The y-axis moves in trial:i02.ug.leaf_0002.01 (up to ±9.6 nm per instance) shifted V3 relative to its M3 enclosure boundary without producing a V3.M3.EN.1 failure, which means the pre-move enclosure margins in that locus exceeded the displacement applied. The resize of p1059 along x in trial:i02.ug.leaf_0003.02 also did not trigger V3.M3.EN.1. When applying y-axis moves to instances containing V3, verify that residual M3 enclosure on the displaced side remains ≥ 5 nm; the available headroom is not universal and depends on the specific M3 geometry at the repair locus.

## V3.M4.EN.2 — M4 enclosure ≥ 11 nm on two opposite sides

V3.M4.EN.2 requires M4 to enclose V3 by at least 11 nm on either the x-pair or y-pair of edges. Neither trial:i02.ug.leaf_0002.01 nor trial:i02.ug.leaf_0003.02 produced a V3.M4.EN.2 violation. The 32 nm high-end x-extension of p1059 in trial:i02.ug.leaf_0003.02 enlarged the M4-related polygon rather than shrinking it, so that resize direction is safe for M4 enclosure of V3. Shrinking M4 geometry toward V3 in either axis is not exercised by these trials and carries enclosure risk not bounded by the measured records.

## V3.AUX.1 — V3 must lie inside M3 ∩ M4

V3.AUX.1 fires whenever any part of a V3 shape falls outside the intersection of M3 and M4. Both trials moved instances that carry V3 without triggering V3.AUX.1, confirming that the y-displacements applied (up to ±9.6 nm in trial:i02.ug.leaf_0002.01, up to +7.2 nm in trial:i02.ug.leaf_0003.02) remained within M3 ∩ M4 at those loci. Larger displacements than those measured have no coverage and must be checked against current M3 and M4 extents before committing.

## V3.M4.AUX.2 — V3 width must match M4 width perpendicular to M4 length

V3.M4.AUX.2 requires V3 to span exactly the full M4 width in the direction perpendicular to M4's length; any V3 edge that does not coincide with two opposite M4 edges in that dimension is a violation. Neither trial:i02.ug.leaf_0002.01 nor trial:i02.ug.leaf_0003.02 recorded a V3.M4.AUX.2 failure. The x-axis resize of p1059 in trial:i02.ug.leaf_0003.02 did not disturb the perpendicular-to-length dimension of the affected V3 shapes. Resizes along the M4 length axis (x in these trials) are safe for V3.M4.AUX.2 as long as the perpendicular width of V3 and M4 remain matched; resizes in the perpendicular direction would directly risk this rule and are not exercised in the measured history.

## Connectivity and acceptance

Both trials were accepted with `conn_preserved=true` and `decision=gated_in`. The new in-crop violations introduced by trial:i02.ug.leaf_0002.01 were on M1.A.1 (4) and V1.M1.EN.1 (4), not on any V3 rule, and the trial was still accepted because connectivity was preserved. trial:i02.ug.leaf_0003.02 introduced 12 new in-crop violations with no per-rule breakdown available, yet was also accepted on the same basis. Accepting trials that introduce non-V3 violations while touching V3 is consistent with the measured records, but those co-introduced violations on other layers remain in the design state and are not cleared by V3 repair operations.