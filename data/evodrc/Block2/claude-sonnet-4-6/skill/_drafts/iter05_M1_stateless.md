Looking at the DRC rules and the 9 measured trials in this layer's history, I'll write the knowledge body now.

---

**Operation Patterns and Outcomes**

All nine recorded trials for M1 were accepted with `decision: gated_in` because connectivity was preserved (`conn_preserved: true`). Seven trials at iteration 1 introduced zero new violations; one trial at iteration 4 and one at iteration 5 each introduced exactly one new in-crop violation while still being accepted on connectivity grounds.

The dominant repair operation across iterations 1–5 is a positive-X instance move, most frequently at +36 dbu. This displacement was applied successfully in trials trial:i01.ug.Block2_union_row1.00, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.leaf_0004.04, trial:i01.ug.leaf_0007.05, and trial:i01.ug.leaf_0011.06, all of which touched M1 and V1 (and M2) and produced zero new violations. A 64 dbu positive-X move was used in trial:i01.ug.Block2_union_row5.02 with the same clean result. A larger 128 dbu positive-X move was used in trial:i01.ug.leaf_0001.03, also clean. Do not apply displacements that are not multiples of the grid step observed in these trials (36 dbu minimum positive-X unit is the most frequently confirmed step).

**Polygon End Extension Accompanying Instance Moves**

When an instance is moved in X, M1 polygon endpoints must be extended on the same axis to maintain enclosure and connectivity. In trial:i01.ug.Block2_union_row3.01 the move of two instances by +36 dbu was paired with a `resize_end` on polygon p1040 at axis:x, end:high by +36 dbu. In trial:i01.ug.Block2_union_row5.02 two polygon ends (p1059 and p1057) were each extended by +64 dbu on axis:x, end:high to match the +64 dbu instance moves. In trial:i01.ug.leaf_0001.03 two polygon ends were extended by +184 and +176 dbu respectively following a +128 dbu instance move—indicating that the polygon extension magnitude does not need to equal the instance move magnitude exactly, but must be large enough to restore V0.M1.EN.1 and V1.M1.EN.1 enclosure on both projecting sides. In trial:i01.ug.leaf_0011.06 polygon p1052 was extended by +36 dbu end:high accompanying a +36 dbu instance move. Always pair polygon end extensions with instance moves on the same axis when M1 connectivity to V0 or V1 is involved; omitting the extension risks V0.M1.EN.1 or V1.M1.EN.1 violations.

**V0.M1.EN.1 and V1.M1.EN.1 Enclosure**

V0.M1.EN.1 requires M1 to enclose V0 by at least 5 nm on two opposite sides (5&5 or 5&0 projection). V1.M1.EN.1 requires M1 to enclose V1 by 5 nm on one side and 2 nm on the other. All iteration-1 trials that touched both M1 and V1 (trial:i01.ug.Block2_union_row1.00, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0004.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0011.06) repaired without introducing new enclosure violations. This confirms that positive-X instance moves paired with matching polygon end extensions, when keeping the via inside the moved M1 body, satisfy both enclosure rules simultaneously.

**V0.M1.AUX.3 Width Matching**

V0.M1.AUX.3 requires V0 to be exactly the same width as M1 in the direction perpendicular to the M1 run. No trial in this history produced a new V0.M1.AUX.3 violation; all recorded instance moves that shifted V0-bearing M1 wires in X kept the perpendicular dimension unchanged. Resize operations in this history were confined to end:high or end:low extensions along the run axis (X), not the perpendicular (Y), which is consistent with AUX.3 compliance.

**M1.A.1 Minimum Area**

M1.A.1 prohibits M1 polygons with area below 504 nm². At iteration 5, trial:i05.ug.leaf_0002.01 introduced one new M1.A.1 violation (new_in_crop_by_rule: M1.A.1: 1) during a repair that combined a +36 dbu instance move (i0063 in X), a +36 dbu instance move (i0071 in Y), and a +56 dbu resize_end on p1036 at axis:x, end:high. This is the only recorded M1.A.1 failure in the history. The violation was accepted because connectivity was preserved, but the pattern of combining a cross-axis instance shift (Y) with an X-only polygon end extension in the same operation can leave a residual M1 fragment too small to satisfy M1.A.1. Avoid operations that simultaneously shift instances in one axis and extend polygon ends in a different axis within the same repair step when the affected polygon is already near the 504 nm² minimum area threshold.

At iteration 4, trial:i04.ug.leaf_0002.01 used negative-X moves (-64 dbu for four instances and polygon p937) combined with a +36 dbu Y-move on i0063 and polygon p1036, introducing one new in-crop violation (unspecified rule). This is the only trial with negative-X displacements; all zero-violation trials used positive-X displacements. Negative-X moves carry higher risk of introducing new violations than positive-X moves of equivalent magnitude at this layer, as confirmed by the contrast between trial:i04.ug.leaf_0002.01 (1 new violation, negative-X) and trial:i01.ug.Block2_union_row5.02 (0 new violations, positive-X, same 64 dbu magnitude).

**M1.W.1, M1.S.1–S.6, M1.S.6, M1.R.0**

No trial in this history produced violations of M1.W.1 (18 nm minimum width), M1.S.1 (18 nm side-to-side spacing), M1.S.2 (25 nm tip-to-side), M1.S.3 (27 nm tip-to-tip for 24–36 nm edges), M1.S.4 (31 nm tip-to-tip for both edges < 24 nm), M1.S.5 (31 nm mixed tip-to-tip), M1.S.6 (20 nm corner-to-corner), or M1.R.0. The repair operations observed—small positive-X instance moves (36–128 dbu) and matching end extensions—do not bring M1 segments closer together in the transverse direction and do not reduce M1 width, which is consistent with the absence of spacing and width violations across all nine trials.

**Assemble Drops and Cross-Layer Interactions**

In trial:i05.ug.leaf_0002.01, one M3-layer `resize_via_shape` operation was dropped before assembly with reason `cu_pool:rejected_net_positive`. This drop did not affect the M1-specific outcome (the trial was accepted, and the one new violation was M1.A.1, not an M3 rule). When a multi-layer repair bundle includes via shape resizes on adjacent layers, those resizes can be silently dropped at assemble time without blocking acceptance; however, dropped via operations may leave enclosure relationships on M1 in a state that was not fully optimized, which is consistent with the new M1.A.1 violation observed in that same trial.

**NONORTHOGONAL**

The NONORTHOGONAL rule applies to M1 and prohibits any edge with an angle that is not 0 or 90 degrees. All recorded operations in this history are axis-aligned (`axis: x` or `axis: y`, or delta_dbu vectors of the form [d, 0] or [0, d]). No NONORTHOGONAL violation was introduced in any of the nine trials. All future M1 repair operations must maintain strictly orthogonal geometry; instance moves must use integer-grid axis-aligned deltas and polygon end extensions must be along the run axis only.