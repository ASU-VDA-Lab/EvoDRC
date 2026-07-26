## V2.M3.AUX.2 is the dominant active violation class at iteration 4

The only applied fix recorded for layer V2 targeted V2.M3.AUX.2 (V2 must be exactly the same width as M3 along the direction perpendicular to M3 length). Trial trial:i04.cu.def:VIA_VIA23_1_3_36_36.00 (cu_pool channel, target `def:VIA_VIA23_1_3_36_36`) applied group `v2m3aux2_fix` and reduced the whole-design violation count by 8, from 30 to 22.

## Fix pattern for V2.M3.AUX.2: shrink M3 in the y-axis inside the via cell definition

The applied repair for V2.M3.AUX.2 in trial:i04.cu.def:VIA_VIA23_1_3_36_36.00 consisted of two distinct resize types, all on the y-axis and all negative (shrinking):

- The M3 shape stored directly inside via cell `VIA_VIA23_1_3_36_36` (`op: resize_via_shape`, `shape_index: 0`) was reduced by 40 dbu in y.
- Seven M3 polygons in the flat design (p891 through p897) were each reduced by 64 dbu in y.

Do not resize V2 shapes to fix V2.M3.AUX.2: the entire repair in trial:i04.cu.def:VIA_VIA23_1_3_36_36.00 touched only M3 and the M3 component of the via cell shape, leaving the V2 geometry unchanged. The rule requires V2 to match M3 width perpendicular to M3 length; the correct lever is the overhanging M3, not the via.

The via shape resize magnitude (40 dbu) and the flat polygon resize magnitude (64 dbu) differ. Apply each resize to its own geometry class rather than using a single uniform delta across the entire fix group (trial:i04.cu.def:VIA_VIA23_1_3_36_36.00).

## Targeting via cell definitions resolves clustered V2.M3.AUX.2 violations efficiently

The cu_pool channel fixes one via cell definition at a time (trial:i04.cu.def:VIA_VIA23_1_3_36_36.00 target was `def:VIA_VIA23_1_3_36_36`). A single cell-level fix repaired 8 violations simultaneously, consistent with repeated instantiation of the same cell. Prefer targeting the cell definition rather than individual flat polygon instances when V2.M3.AUX.2 errors cluster around a repeating via cell.

## unit_gate whole-design trial was gated in, not applied

Trial trial:i01.ug.whole_design.00 (unit_gate channel, locus `[0,0,10784,10784]`) performed 19 operations across M1–M5, V1–V4 including move_instance operations and y-axis resize_end operations on polygons p879 and p910. The decision was `gated_in` with reason `conn_preserved`. This trial produced no net violation delta for V2; do not treat its polygon resizes as an established V2 repair pattern since the fix was not applied.

## V2.M3.AUX.2 rule mechanics: both edges of V2 must be coincident with M3 edges

The rule deck for V2.M3.AUX.2 flags any V2 that is either not inside M3 (`v2_aux2_out`) or inside M3 but with fewer than two coincident edges (`v2_aux2_ok` requires `.interacting(v2_aux2_coinc, 2)`). An M3 shape that is wider than V2 in the perpendicular direction will fail because V2 edges do not align with M3 edges on both sides. The fix in trial:i04.cu.def:VIA_VIA23_1_3_36_36.00 corrected this by narrowing M3 in y until both perpendicular M3 edges became coincident with the V2 edges.

## V2.AUX.1 interaction: M3 shrinks for AUX.2 must preserve V2 containment

V2.AUX.1 requires V2 to remain inside both M2 and M3. Any M3 resize applied to fix V2.M3.AUX.2 must not cause M3 to recede past the V2 boundary, or AUX.1 will fire. The trial:i04.cu.def:VIA_VIA23_1_3_36_36.00 fix achieved a net violation reduction of 8 with no recorded AUX.1 regression, confirming that shrinking M3 to match V2 width (not to undercut it) satisfies both rules simultaneously.

## M3.EN.2 enclosure constraint limits how far M3 can be shrunk

V2.M3.EN.2 requires M3 to enclose V2 by at least 5 nm on two opposite sides (either 5 & 5 nm or 5 & 0 nm). When applying y-axis M3 shrinks to fix V2.M3.AUX.2, verify that the remaining M3 extent still meets the 5 nm enclosure requirement on both perpendicular sides. The applied fix in trial:i04.cu.def:VIA_VIA23_1_3_36_36.00 passed without triggering a V2.M3.EN.2 regression, but the enclosure margin must be checked for each unique via cell before applying similar magnitude shrinks.

## Spacing rules V2.S.1–V2.S.4: end-cap classification determines which threshold applies

The spacing rules distinguish between V2 instances that have a 5 nm M3 end-cap (v2_wec, "with end-cap") and those that do not (v2_nec, "no end-cap"). The classification is structural: a V2 is v2_wec when none of its edges are fully coincident with M3 edges (v2_full_flush_m3 is empty for that instance), and v2_nec when at least one set of opposite edges is fully flush with M3. The applicable corner-to-corner Euclidean threshold is:

- Both v2_wec (both with end-cap): 16.4 nm Euclidean on v2_wec_mask → physical spacing 23 nm (V2.S.2)
- Both v2_nec (both without end-cap): 16.12 nm Euclidean on v2_nec_mask → physical spacing 30 nm (V2.S.3)
- Mixed (one v2_wec, one v2_nec): 17.11 nm Euclidean separation → physical spacing 27 nm (V2.S.4)

No spacing violations or spacing-targeted fixes appear in the measured history through iteration 4; these thresholds are rule-derived, not empirically confirmed from trials.

## V2.W.1: minimum width 18 nm along M3 length

V2.W.1 sets 18 nm minimum width along the M3 length direction. No width violations or width-targeted operations appear in the measured history through iteration 4.

## V2.M2.EN.1: M2 must enclose V2 by 5 nm on at least two opposite sides

V2.M2.EN.1 checks that V2 is not interacting with `v2 - m2.sized(-5.nm, 0)` and `v2 - m2.sized(0, -5.nm)` simultaneously, meaning M2 must provide 5 nm enclosure in both x and y on at least one axis pair. No M2 enclosure violations or M2-targeted fixes for V2 appear in the measured history through iteration 4.

## NONORTHOGONAL: all V2 edges must be at 0° or 90°

The global NONORTHOGONAL block flags any edge with angle in (1..89), (91..179), (-179..-91), or (-89..-1). All V2 shapes must be Manhattan rectangles. No nonorthogonal violations or diagonal-geometry operations on V2 appear in the measured history through iteration 4.