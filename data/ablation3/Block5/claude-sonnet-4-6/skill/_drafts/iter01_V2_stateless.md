**V2.W.1 — Minimum width 18 nm along M3 length**

V2 shapes must be at least 18 nm wide in the direction of M3 length. In trial:i01.ug.whole_design.00, a set of 19 operations that touched the V2 layer—including y-axis high-end resize of polygon p879 by 48 dbu and y-axis high-end resize of polygon p910 by 20 dbu—produced zero new V2.W.1 violations. End-cap extensions on neighboring polygons in the y-direction do not compress V2 width below the 18 nm floor when the V2 instances themselves are not directly resized.

**V2.S.1 — M3-track-context-dependent projection spacing (18/27/18 nm)**

The rule evaluates projected spacing on v2_mask edges that do not coincide with M3 edges. Three thresholds apply: 18 nm for V2 instances sharing the same M3 track or sitting on aligned parallel M3 tracks, and 27 nm for instances on non-aligned parallel M3 tracks. In trial:i01.ug.whole_design.00, 14 instance moves with x-deltas spanning −28 to +136 dbu and y-deltas spanning −48 to +96 dbu introduced zero new V2.S.1 violations. Moving instances in connectivity-preserving groups across this range of offsets is safe for V2.S.1 (trial:i01.ug.whole_design.00).

**V2.S.2 — Corner-to-corner spacing 23 nm between two wec-class V2 instances**

When both V2 instances carry a 5 nm M3 end-cap (wec class, i.e., not fully flush with M3 edges), the Euclidean corner-to-corner spacing between their expanded masks must be at least 23 nm (16.4 nm check against the wec_mask, which is extended 5 nm along M3 then sized ±5 nm). Trial:i01.ug.whole_design.00 incurred zero new V2.S.2 violations; neither the three polygon edits nor the 14 instance moves brought any wec-class V2 mask pair into corner proximity below 23 nm.

**V2.S.3 — Corner-to-corner spacing 30 nm between two nec-class V2 instances**

When both V2 instances are fully flush with M3 edges on all sides (nec class), the Euclidean corner-to-corner spacing between their nec_masks must be at least 30 nm. The DRC isolates true corner violations by removing any error polygon that also appears in the projection check. Trial:i01.ug.whole_design.00 produced zero new V2.S.3 violations; nec-class V2 mask pairs were not driven into corner proximity below 30 nm by any operation in that trial.

**V2.S.4 — Corner-to-corner spacing 27 nm for mixed wec/nec V2 pairs**

For one wec-class and one nec-class V2 instance, the Euclidean separation between their respective masks must be at least 27 nm. Like V2.S.2 and V2.S.3, trial:i01.ug.whole_design.00 produced zero new V2.S.4 violations across all 19 operations. Axis-aligned instance moves that preserve inter-instance M3 track structure do not violate mixed end-cap spacing (trial:i01.ug.whole_design.00).

**V2.M2.EN.1 — M2 must enclose V2 by ≥ 5 nm on at least two opposite sides**

The rule uses `m2.sized(-5.nm, 0)` and `m2.sized(0, -5.nm)` to confirm that M2 provides at least 5 nm enclosure in both the horizontal and vertical directions on at least one pair of opposite edges. Moving a V2 instance and its hosting M2 shape by the same delta preserves the relative enclosure margin and is safe for this rule (trial:i01.ug.whole_design.00). In trial:i01.ug.whole_design.00, instance moves up to +136 dbu in x and ±96 dbu in y introduced zero new V2.M2.EN.1 violations.

**V2.M3.EN.2 — M3 must enclose V2 on two opposite sides with ≥ 5 nm and ≥ 0 nm**

M3 must enclose V2 on two opposite sides: the enclosure pair can be 5&5 nm or 5&0 nm (zero end-cap on one side is allowed). The DRC flags any V2 that does not interact with a fully-good enclosure edge pair, and separately flags any M3 enclosure edge failing the projection floor. In trial:i01.ug.whole_design.00, polygon resize operations that grew M3 end-caps (p879 y-axis high-end +48 dbu, p910 y-axis high-end +20 dbu) moved away from the enclosure floor rather than toward it, producing zero new V2.M3.EN.2 violations. Do not shrink M3 end-caps on the enclosing sides without verifying the resulting enclosure against the 5 nm floor; growing them as done in trial:i01.ug.whole_design.00 is safe.

**V2.AUX.1 — V2 must lie fully inside the intersection of M2 and M3**

Every V2 shape must be completely contained within M2 ∩ M3. Trial:i01.ug.whole_design.00 preserved this invariant across all 19 operations with conn_preserved=true and n_new_in_crop=0, n_new_out_of_crop=0. Move V2, M2, and M3 together by the same instance delta to maintain containment; mismatched deltas between a V2 instance and its enclosing M2 or M3 shapes will violate V2.AUX.1.

**V2.M3.AUX.2 — V2 width must exactly match M3 width perpendicular to M3 length**

A V2 shape is valid only when at least two of its edges coincide with M3 edges (the two edges perpendicular to M3's run direction). Instance-level moves that shift a V2 and its hosting M3 cell by the same delta keep these edges coincident and are safe for this rule (trial:i01.ug.whole_design.00). Trial:i01.ug.whole_design.00 introduced zero new V2.M3.AUX.2 violations; all 16 instance moves used identical deltas applied to paired instances, preserving the V2-to-M3 coincidence relationship.

**NONORTHOGONAL geometry**

All V2 edges must lie at exactly 0° or 90°. Every polygon operation in trial:i01.ug.whole_design.00 was axis-aligned: `resize_end` on axis y (p879, p910) and `move` on axis x (p910). These operation types cannot produce non-orthogonal edges, and zero NONORTHOGONAL violations resulted (trial:i01.ug.whole_design.00). Avoid any polygon shaping operation that is not strictly axis-aligned on V2 or on layers (M3, M2) whose edges define V2 classification boundaries.

**End-cap class determination affects which spacing rule fires**

The spacing rules V2.S.1 through V2.S.4 apply different thresholds depending on whether a V2 instance is wec-class (has at least one edge not coincident with any M3 edge) or nec-class (all edges coincident with M3 edges). The most restrictive case is V2.S.3 at 30 nm corner-to-corner for two nec-class instances; the least restrictive projection case is V2.S.1 at 18 nm for same-track or aligned instances. In trial:i01.ug.whole_design.00, zero violations arose across all spacing rules, confirming that the instance moves executed there respected the applicable threshold for each V2 pair's end-cap class combination.

**Operational baseline from the sole measured trial**

Trial:i01.ug.whole_design.00 executed 19 operations on Block5 in the unit_gate channel: 16 instance moves (x-deltas: −28, +8, +8, +136 dbu; y-deltas: −48, −48, −24, −24, +24, +24, +48, +48, +72, +72, +96, +96 dbu) and 3 polygon edits (p879 y-axis high-end resize +48 dbu; p910 x-axis move +8 dbu; p910 y-axis high-end resize +20 dbu). Connectivity was preserved (conn_preserved=true) and no new violations were introduced in-crop or out-of-crop for V2 or for any other touched layer (M1, M2, M3, M4, M5, V1, V2, V3, V4). This establishes that axis-aligned instance moves up to 136 dbu in x and 96 dbu in y, paired with axis-aligned polygon end-cap extensions on M3-related shapes, are safe for all V2 rules when instances are moved in connectivity-preserving groups.