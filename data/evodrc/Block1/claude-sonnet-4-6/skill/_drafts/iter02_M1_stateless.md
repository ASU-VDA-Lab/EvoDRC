## Repair Operation Patterns

**Move-instance is the dominant repair primitive for M1.** Across all gated-in trials in iteration 1, the most common single operation was `move_instance` along the x-axis. Trials trial:i01.ug.leaf_0004.09, trial:i01.ug.leaf_0020.10, and trial:i01.ug.leaf_0031.11 each used exactly one `move_instance` and succeeded. Multi-instance pure-move trials (trial:i01.ug.Block1_union_row10.01, trial:i01.ug.Block1_union_row3.03, trial:i01.ug.Block1_union_row4.04, trial:i01.ug.Block1_union_row9.08) also succeeded without any `resize_end` operations.

**When moves alone are insufficient, pair them with `resize_end` on the x-axis.** Trials that involved both `move_instance` and `resize_end` operations — trial:i01.ug.Block1_union_row1.00, trial:i01.ug.Block1_union_row5.05, trial:i01.ug.Block1_union_row6.06, trial:i01.ug.Block1_union_row8.07, trial:i02.ug.leaf_0001.00 — all passed with conn_preserved=true. The `resize_end` calls in these trials exclusively used axis="x" (end="high" or end="low"), consistent with M1 routing being predominantly horizontal in this design.

**All observed move and resize deltas are along the x-axis only.** No y-axis `move_instance` or `resize_end` operations appear in any M1-touching trial. The single y-axis resize in the history (trial:i01.ug.leaf_0034.12) targeted M3, not M1, and that trial was gated out.

## Connectivity Preservation is the Absolute Gate

**Connectivity preservation (`conn_preserved=true`) is the hard acceptance criterion.** Every gated-in trial — trial:i01.ug.Block1_union_row1.00 through trial:i02.ug.leaf_0001.00 — carried conn_preserved=true. The single gated-out trial, trial:i01.ug.leaf_0034.12, was rejected exclusively because conn_preserved=false (reason="conn_broken"), not because of DRC count. That trial also generated 89 new in-crop violations, but the connectivity failure is the stated reason for rejection.

**New in-crop violations introduced by a repair do not block acceptance as long as connectivity is preserved.** Trials trial:i01.ug.Block1_union_row1.00 (n_new_in_crop=4), trial:i01.ug.Block1_union_row6.06 (n_new_in_crop=1), and trial:i01.ug.leaf_0031.11 (n_new_in_crop=4) were all gated in despite introducing additional violations. Do not abandon a repair solely on the basis of small increases in in-crop violation count; preserve connectivity first.

## Scale and Scope of Multi-Layer Operations

**Successful M1 repairs touch M1, V1, and M2 as a natural co-moving group.** Every gated-in trial in the history has touched_layers containing at least ["M1","M2","V1"]. This reflects the physical reality that moving an M1 instance drags its V1 contacts and the M2 stubs above them.

**Avoid expanding repair scope to M3, M4, V2, or higher layers simultaneously.** The gated-out trial:i01.ug.leaf_0034.12 was the only trial to touch M3, M4, V2 in addition to M1/M2/V1, and it was the only failure. Restrict each repair step to the M1/V1/M2 group; extend to upper layers only as a separate, independently validated operation.

**Large locus area combined with many ops increases risk.** Trial:i01.ug.leaf_0034.12 had the largest locus bounding box in the history (1728–14256 x, 2068–13680 y) and 10 ops spanning four metal layers; it is the only gated-out record. The successful 10-op trial trial:i01.ug.Block1_union_row6.06 stayed within M1/V1/M2 and succeeded. Limit the locus to the minimum region enclosing the violating M1 edges and their directly attached vias.

## Enclosure Rules: V0.M1.EN.1 and V1.M1.EN.1

**The 5 nm enclosure requirement on two opposite sides for both V0 and V1 must be maintained after every resize_end.** V0.M1.EN.1 requires M1 to enclose V0 by at least 5 nm on two opposite sides (or 5 & 0 nm if the zero-enclosure end is fully inside). V1.M1.EN.1 requires M1 to enclose V1 by at least 5 nm on one axis and 2 nm on the other. When `resize_end` is applied to pull an M1 edge toward the via (end="low" shrinking, or end="high" on the far side), verify that neither horizontal nor vertical enclosure drops below the minimum. Trial:i01.ug.Block1_union_row8.07 used `resize_end` end="low" (delta_dbu=36 on polygon p1346) alongside a -72 dbu move on instance i0455; this combination was accepted, indicating the enclosure was maintained after the opposing edge was pulled in.

**V0.M1.AUX.3 constrains M1 width at the via to match the via width.** Any `resize_end` that changes M1 width at a V0 location must leave the edge coincident with the via edge on both sides (no non-coincident horizontal or vertical edge of V0 can extend beyond the M1 boundary). Do not resize only one side of an M1 bar crossing a V0 without verifying that the via edge on the perpendicular axis is still flush.

## Spacing Rules: Edge-Length Classification Before Repair

Before selecting a repair delta, classify the M1 edge involved:

- **Edges > 36 nm ("side" edges):** governed by M1.S.1 (18 nm side-to-side) and M1.S.2 tip-to-side (25 nm from a short edge to this long edge). Moves that shift a side edge must clear 18 nm from the nearest parallel side edge.
- **Edges 24–36 nm ("wide tip" edges):** governed by M1.S.3 (27 nm tip-to-tip to another 24–36 nm edge) and M1.S.5 (31 nm to an edge < 24 nm). Moves or resizes involving these edges need more clearance than the side-to-side rule.
- **Edges < 24 nm ("narrow tip" edges):** M1.S.4 (31 nm tip-to-tip to another < 24 nm edge) and M1.S.5 (31 nm to a 24–36 nm edge). These edges require the largest clearance.

The successful resize_end deltas observed (36, 48, 56, 60, 92, 100, 128, 156, 192 dbu) span a wide range. Larger deltas occur in trials with more simultaneous operations (trial:i01.ug.Block1_union_row8.07, trial:i01.ug.Block1_union_row5.05), consistent with coordinated repositioning of multiple instances and their connecting M1 wires.

## Width and Area Minimums

**Do not allow `resize_end` to reduce M1 width below 18 nm (M1.W.1).** The minimum is stated in nm; in the DBU system used here (where observed deltas of 36 correspond to one grid step), any resize that shrinks M1 must leave at least the 18 nm minimum on the closing axis. No gated-in trial produced a resize that violated width — the smallest observed "shrink" delta was -4 dbu on polygon p1214 in the gated-out trial:i01.ug.leaf_0034.12, which was rejected for connectivity reasons, not width; however, this is the only negative resize_end on an M1 polygon and it was part of a failed trial, so exercise caution with sub-grid shrink deltas.

**Ensure M1 polygons after resize retain at least 504 nm² area (M1.A.1).** Narrow M1 stubs that serve only as via landing pads are most at risk. If a `resize_end` shortens a stub in both x and y directions simultaneously, verify the resulting area remains above threshold.

## Corner-to-Corner and Non-Orthogonal Geometry

**M1.S.6 (20 nm corner-to-corner minimum) is distinct from the edge-spacing rules and can be violated by diagonal proximity even when edge-to-edge spacing is satisfied.** No corner-to-corner violation was directly evidenced in the gated-in trials; all accepted repairs kept moves along the x-axis, which preserves corner alignment on the y-axis.

**All M1 edges must remain orthogonal (GEOMETRY.NONORTHOGONAL).** Every observed operation is a pure x- or y-axis move or edge resize. No diagonal moves or rotations appear in any trial. Do not introduce non-axis-aligned geometry; the NONORTHOGONAL check fires on any edge with angle outside {0°, 90°, 180°, 270°}.

## Iteration Context

**Iteration 2 begins from a different design state than iteration 1.** All 12 iteration-1 trials share design_state "796a62668..." while the single iteration-2 trial trial:i02.ug.leaf_0001.00 operates on design_state "72624257...". The iteration-2 repair (move i0300 by 100 dbu + resize_end p1385 by 60 dbu on x-high) succeeded with n_new_in_crop=0 and conn_preserved=true. This is consistent with the pattern that moderate x-axis moves paired with a coordinated resize_end on the same unit close M1 spacing violations without creating new ones or severing nets.