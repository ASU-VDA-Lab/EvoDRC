## Repair Decision Gate: Connectivity Over In-Crop Violations

All eleven trials in this iteration were accepted (`decision:"gated_in"`) with `conn_preserved:true` as the controlling criterion, even when new in-crop DRC markers were introduced. Trials trial:i01.ug.Block1_union_row1.00 and trial:i01.ug.leaf_0031.11 each produced `n_new_in_crop:4`, and trial:i01.ug.Block1_union_row6.06 produced `n_new_in_crop:1`; all three were accepted. No trial in this history was rejected. Accept a V1 repair move when `conn_preserved:true` even if `n_new_in_crop` is non-zero.

`n_new_out_of_crop` is zero in every trial. Repair moves must not displace violations across the crop boundary; the instance move magnitudes and resize deltas observed here remain bounded within the crop locus in all eleven cases (trial:i01.ug.Block1_union_row1.00 through trial:i01.ug.leaf_0031.11).

## Layer Co-Repair: M1, M2, V1 Are Always Touched Together

Every accepted trial lists `touched_layers:["M1","M2","V1"]`. V1 geometry is never repaired in isolation. All operations that shift or resize V1-bearing cells propagate changes simultaneously to M1 and M2 in the same operation set, consistent with V1.AUX.1 (V1 must remain inside M1 & M2) and V1.M1.EN.1 / V1.M2.EN.2 (enclosure requirements that must be maintained on both enclosing layers when V1 position changes). See trial:i01.ug.Block1_union_row10.01, trial:i01.ug.Block1_union_row9.08, trial:i01.ug.leaf_0004.09 for single-op or two-op cases where the co-layer discipline is unambiguous.

## Primary Repair Primitives

Two operation types appear across all trials:

**move_instance** — shifts an entire cell instance by `delta_dbu` in x and/or y. This is the dominant primitive; trials trial:i01.ug.Block1_union_row10.01, trial:i01.ug.Block1_union_row8.07, trial:i01.ug.Block1_union_row9.08, and trial:i01.ug.leaf_0004.09 each use only move_instance operations. Moving a full cell instance keeps V1, M1, and M2 geometrically coherent with each other, preserving V1.AUX.1 and V1.M2.AUX.2 without requiring separate per-layer edits.

**resize_end** — extends one end of an M2 polygon along the x-axis (`axis:"x"`, `end:"high"` or `end:"low"`). Used in trials trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row3.03, trial:i01.ug.Block1_union_row4.04, trial:i01.ug.Block1_union_row5.05, and trial:i01.ug.leaf_0020.10. Trial trial:i01.ug.leaf_0031.11 uses `op:"resize"` (no `end` key), which resizes the polygon uniformly on x.

All resize operations in this history target `axis:"x"` only. V1.M2.AUX.2 requires V1 width perpendicular to M2 length to exactly equal M2 width in that direction; for horizontally-routed M2 the perpendicular is y, so M2 body width in y must not be modified. Do not apply resize_end along y when M2 is horizontal (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row5.05 confirm x-only axis use across both `end:"high"` and `end:"low"` variants).

## Move Magnitudes and Grid

Instance move deltas along x cluster around 36 dbu and its multiples: 36, 72 (not observed directly), 108 (trial:i01.ug.Block1_union_row1.00 instance i0507, trial:i01.ug.Block1_union_row8.07 instance i0244). Moves of -32 dbu also appear and are accepted: trial:i01.ug.Block1_union_row6.06 (delta_dbu:[-32,0]) and trial:i01.ug.Block1_union_row8.07 (instance i0258, delta_dbu:[-32,0]). The repair grid is therefore not strictly 36 dbu; 32 dbu increments are valid.

A y-component of -36 dbu appears in one move — instance i0300 in trial:i01.ug.Block1_union_row4.04, delta_dbu:[36,-36] — and the trial was accepted. Small y-offsets equal in magnitude to a standard x-grid step are permissible.

Resize_end deltas on x range from 36 dbu to 128 dbu across the observed trials: 36 dbu (trial:i01.ug.Block1_union_row5.05, polygons p1297 and p1301; trial:i01.ug.leaf_0020.10, polygon p1253), 52 dbu (trial:i01.ug.Block1_union_row4.04, polygon p1238), 92 dbu (trial:i01.ug.Block1_union_row3.03, polygon p1370; trial:i01.ug.Block1_union_row1.00, polygon p1321), 128 dbu (trial:i01.ug.Block1_union_row1.00, polygon p1320).

## Enclosure Repairs: Pairing move_instance With resize_end

V1.M2.EN.2 requires M2 to enclose V1 by at least 5 nm on two opposite sides (5&5 nm or 5&0 nm permitted). When move_instance shifts a V1-bearing cell in x, the trailing M2 end-cap narrows; resize_end on the trailing end (`end:"low"` when moving positive-x, `end:"high"` when moving negative-x) restores the enclosure margin. This paired pattern appears in trial:i01.ug.Block1_union_row1.00 (two move_instance + two resize_end), trial:i01.ug.Block1_union_row3.03 (one move_instance + one resize_end), and trial:i01.ug.leaf_0020.10 (one move_instance + one resize_end end:"low"). Apply resize_end to the M2 end that loses enclosure margin after a move_instance; do not apply it to the leading end, which gains margin from the same move.

V1.M1.EN.1 requires M1 to enclose V1 by 5&2 nm on opposite sides. M1 is present in `touched_layers` for every trial; the move_instance primitive moves M1 together with V1, maintaining this enclosure automatically without separate M1 resize operations (trial:i01.ug.Block1_union_row10.01, trial:i01.ug.leaf_0004.09).

## Spacing Rule Sensitivity to End-Cap State

V1.S.1 through V1.S.4 use the NEC/WEC classification derived from whether M2 edges are flush with all V1 edges (NEC) or M2 extends past V1 on at least one end (WEC). The end-cap category determines which distance threshold governs: NEC–NEC corner spacing requires 30 nm (V1.S.3), WEC–WEC requires 23 nm (V1.S.2), mixed WEC–NEC requires 27 nm (V1.S.4), and projection-based spacing on the same or aligned M2 track requires 18 nm while non-aligned parallel-track spacing requires 27 nm (V1.S.1).

resize_end operations alter M2 end-cap length and therefore alter end-cap classification for the affected via. Trials trial:i01.ug.Block1_union_row3.03, trial:i01.ug.Block1_union_row4.04, and trial:i01.ug.leaf_0020.10 each apply resize_end and produce `n_new_in_crop:0`, confirming that the resize deltas used (36–92 dbu) resolve V1.M2.EN.2 shortfalls without triggering new V1.S.2/S.3/S.4 violations at the observed inter-via spacings in those crop windows. When resize_end is applied, verify resulting spacing to all neighboring V1 instances against the threshold that matches the post-resize end-cap state of both participants.

## V1.M2.AUX.2 Compliance

V1.M2.AUX.2 requires the V1 footprint width perpendicular to M2 length to exactly match the M2 wire width in that direction. All resize_end and resize operations in this iteration operate exclusively on x (M2 length direction), leaving the y-extent of both V1 and M2 unchanged (trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row5.05, trial:i01.ug.leaf_0031.11). Do not use resize_end on y for horizontal M2 wires; doing so would violate V1.M2.AUX.2.

## Nonorthogonal Geometry

The NONORTHOGONAL rule applies to V1 as to all layers. No nonorthogonal edges are introduced by any trial in this history; all move_instance and resize_end operations displace geometry by axis-aligned integer-dbu amounts, preserving Manhattan geometry. Do not apply fractional or diagonal offsets (trial:i01.ug.Block1_union_row4.04, which uses [36,-36], is still Manhattan — both components are integer-dbu and axis-aligned).