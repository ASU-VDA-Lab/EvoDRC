## Width Rules

**Horizontal width bounds (M5.W.1, M5.W.2).** M5 horizontal width must be at least 24 nm and must not exceed 480 nm. Widths that are exact even integer multiples of 24 nm (48, 96, 144, 192, 240, 288, 336, 384, 432, 480 nm) are forbidden by M5.W.3. Widths of 72, 168, 264, 360, or 456 nm are separately forbidden by M5.W.4 because they span an even number of minimum-width routing tracks. Any horizontal resize or polygon move that lands on one of these values creates an immediate violation.

**Vertical width minimum (M5.W.5).** Minimum vertical width of M5 is 44 nm. Instance moves that carry a simultaneous y-component compress M5 segment heights and breach this rule. trial:i02.ug.leaf_0004.03 introduced 12 M5.W.5 violations when a set of instances was moved with mixed x+y deltas (e.g. [32,32], [32,72], [32,-72], [-16,72]). Pure-x instance moves in iter 4 did not generate M5.W.5 violations (trial:i04.ug.leaf_0003.02, 0 M5.W.5 entries).

## Spacing Rules

**Horizontal spacing (M5.S.1).** Minimum horizontal spacing between any two M5 edges is 24 nm, enforced by both projection (for parallel edges) and Euclidean (for all edge pairs). The projection check is 24 nm; the global Euclidean check is 1 nm (catches near-touching corners).

**Vertical spacing (M5.S.2).** Minimum vertical spacing is 40 nm.

**Tip-to-tip without shared parallel run length (M5.S.3).** 40 nm applies to adjacent-track end-to-end gaps when no parallel run length is shared.

**Tip-to-tip with shared parallel run length (M5.S.4).** When two M5 polygons on adjacent tracks do share a parallel run length, the tip-to-tip gap must still be at least 40 nm. trial:i02.ug.leaf_0004.03 introduced 4 M5.S.4 violations through combined x+y instance moves, confirming that any y-displacement of an instance relative to its neighbor can close an existing tip-to-tip gap on M5.

**Minimum parallel run length (M5.S.5).** Two M5 polygons on adjacent tracks that are within 24 nm (exclusive) of each other horizontally must overlap vertically by at least 44 nm.

## Grid and Track Placement

**Vertical-edge x-grid (M5.AUX.1).** All M5 vertical edges must fall on a 24 nm grid. trial:i02.ug.leaf_0004.03 introduced 12 M5.AUX.1 violations when instance x-moves of +32 dbu and -16 dbu were applied; 32 dbu and 16 dbu are not multiples of 24 dbu. Any x-displacement of an instance or polygon that is not a multiple of 24 dbu will violate M5.AUX.1 for every M5 vertical edge belonging to that instance. In contrast, trial:i04.ug.leaf_0003.02 applied the same +32/-16 dbu x-moves and produced only 8 total new violations (rule breakdown not itemized per-rule in that record, but M5.AUX.1 was not listed separately), indicating that prior state after iter-3 adjustments had already accommodated some offsets; the fundamental requirement remains that edge x-coordinates must be multiples of 24 nm in absolute coordinates.

**Routing track centerline constraint (M5.AUX.2).** Minimum-width M5 tracks (those that survive a ±13 nm erosion/dilation) must have their x-centerlines at positions satisfying (center - 48 dbu) mod 192 dbu = 0, i.e., at 48, 240, 432, ... dbu from the origin. The pitch is 192 dbu (= 8 × 24 nm) and the offset is 48 dbu (= 2 × 24 nm). Instance or polygon x-moves must be chosen to keep minimum-width M5 centerlines on these tracks.

**No bends (M5.AUX.3).** M5 polygons must be strictly rectilinear; no corner angles in the range 0°–90° are permitted. trial:i02.ug.leaf_0004.03 introduced 38 M5.AUX.3 violations from instance moves that carried both x and y components simultaneously (e.g. [32,32], [32,72], [-16,72], [32,-72], [32,-96], [-16,32]). When an instance is shifted diagonally, the M5 routing segments connecting it to neighboring instances at different post-move x- or y-positions acquire a bend. Pure-axis moves (x-only or y-only) do not by themselves create bends; mixed-axis moves do. trial:i04.ug.leaf_0003.02, which used only x-axis moves plus two diagonal entries ([32,-96] and [-16,-96]), produced 8 total new violations but did not re-introduce 38 AUX.3 entries, consistent with the fact that the y-component of those two diagonal moves was -96 dbu, a value that is an even multiple of the 48 nm vertical pitch.

**Wide polygon outside edge restriction (M5.AUX.4).** The outside (vertical) edges of wide M5 polygons (those wider than 26 nm after ±13 nm erosion/dilation) must not touch a minimum-width M5 routing track edge. When placing or resizing wide M5 shapes, keep their vertical edges away from track positions defined by the M5.AUX.2 pitch/offset grid.

## Via Enclosure and Width Matching

**V4 enclosure by M5 (V4.M5.EN.2).** V4 must be enclosed by M5 by at least 11 nm on two opposite sides (both horizontal and vertical). Resizing the via shape in the y direction by -88 dbu on cell VIA_VIA45_1_2_58_58 eliminated 52 violations across two windows (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01), demonstrating that an oversized via shape in y is a common root cause for this rule. When a VIA_VIA45 shape protrudes beyond the M5 stripe it lives on, shrinking the via shape (not the metal) is the correct repair.

**V4 width matching (V4.M5.AUX.2).** V4 must be exactly the same width as M5 in the direction perpendicular to the M5 length. trial:i02.ug.leaf_0003.02 introduced 4 V4.M5.AUX.2 violations from instance moves that shifted instances in x by +32 or -16 dbu, repositioning M5 stripes without correspondingly repositioning or resizing the V4 shapes. Any x-move of an instance that changes the effective M5 width as seen by a straddling V4 must be accompanied by a compensating V4 resize or the whole via-containing instance must be moved as a unit.

**V5 enclosure by M5 (V5.M5.EN.1).** V5 must be enclosed by M5 by at least 11 nm on at least two opposite sides.

## Operation Patterns and Constraints

**resize_via_shape (y-axis).** Shrinking a VIA_VIA45 shape in y is a direct, low-risk repair for V4.M5.EN.2 and related enclosure violations. trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 achieved a net -52 violation reduction with a single -88 dbu y-resize. The operation touches M4, M5, and V4, so downstream rules on all three layers must be re-checked after applying it.

**resize_end on M5 polygons.** Adjusting a single endpoint of an M5 polygon (resize_end, axis=y) is usable to satisfy enclosure or spacing constraints without displacing the entire polygon. trial:i02.ug.leaf_0002.01 applied resize_end (axis=y, delta=+44 dbu, end=low) together with a move_instance and produced zero new violations across M4, M5, and V4 layers. A +44 dbu y-extension exactly matches the M5.W.5 minimum vertical width, suggesting the end was at the minimum before the resize.

**Instance x-move granularity.** Observed x-move deltas in the multi-instance repair passes are +32 dbu and -16 dbu (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03, trial:i04.ug.leaf_0003.02). These values are not multiples of 24 dbu (the M5.AUX.1 grid), so their legality depends entirely on the absolute pre-move edge coordinates already being positioned such that post-move coordinates land on 24 nm multiples. Do not apply +32 or -16 dbu x-moves to an instance whose M5 vertical edges are not already pre-offset by the complementary amount.

**Instance y-move granularity.** Observed y-move deltas in iter-4 y-direction repairs are ±48 dbu and ±96 dbu (trial:i04.ug.leaf_0002.01). These are multiples of 48 nm, which satisfies both the M5.W.5 vertical minimum (44 nm) and the M5.S.2 vertical spacing (40 nm) with margin. Choosing y-moves in multiples of 48 dbu keeps M5 segment heights within the legal band without requiring per-segment recalculation.

**Mixed x+y instance moves generate M5.AUX.3 and M5.W.5 violations.** trial:i02.ug.leaf_0004.03 introduced 38 M5.AUX.3 and 12 M5.W.5 violations via diagonal moves. Decompose any required diagonal repositioning into a pure-x move for one iteration and a pure-y move for another, or ensure both components are multiples of their respective legal pitches before combining.

**Cross-leaf conflict resolution.** When two unit repairs (leaves) claim the same instance move, the assembler applies first-wins logic (cross_crop_first_wins) or drops conflicting moves (external_conflict_dropped). trial:i02.ug.leaf_0004.03 shows 41 surviving ops out of a much larger candidate set due to conflicts with leaf_0003. Dropped instance moves leave the design in a partial-repair state that may re-introduce violations in the next iteration; the iteration-4 trials (trial:i04.ug.leaf_0003.02, trial:i04.ug.leaf_0002.01) re-applied the same +32/-16 x-moves and ±48/96 y-moves that were previously dropped, confirming the repair strategy is correct but requires re-application when drops occur.

**Layer interaction scope.** M5 repairs consistently touch M4, V4, and sometimes M6, V5 (trial:i02.ug.leaf_0004.03: M2, M3, M4, M5, M6, V2, V3, V4, V5). When routing M5, always validate the full via stack above (V5/M6) and below (V4/M4) after any M5 polygon move or resize.

**Non-orthogonal geometry.** The NONORTHOGONAL block applies globally. M5 edges must be horizontal (0°) or vertical (90°) only. M5.AUX.3 enforces this structurally for M5 via corner detection; the NONORTHOGONAL rule enforces it via edge-angle filtering. Both are triggered by bends created through diagonal instance moves, as confirmed by trial:i02.ug.leaf_0004.03.