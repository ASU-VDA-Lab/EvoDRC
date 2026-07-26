Two claims in the current knowledge are directly contradicted by trial:i04.ug.whole_design.00. Dropping both and updating all dependent paragraphs now.

---

## Observed repair patterns

Two trials have been accepted on this layer.

Trial:i03.ug.whole_design.00 (Block3, unit_gate, whole_design locus, iteration 3) combined 20 instance moves (all +x, deltas of 64 or 136 dbu) with 16 polygon resize_end operations on M1/M2 high-x ends (values 84/120/156/192 dbu). Total operation count was 36 (n_ops=36). Connectivity was preserved (conn_preserved=true) and the decision was gated_in.

Trial:i04.ug.whole_design.00 (Block3, unit_gate, whole_design locus, iteration 4) used only 2 move_instance operations: instance i0023 moved −36 dbu in x and instance i0041 moved +36 dbu in x. No resize_end operations were applied to any polygon. Touched layers were M1, M2, and V1. Connectivity was preserved (conn_preserved=true) and the decision was gated_in (trial:i04.ug.whole_design.00).

## Move direction

Both +x and −x instance moves are valid repair directions. Trial:i03.ug.whole_design.00 used only +x deltas (64, 136 dbu); trial:i04.ug.whole_design.00 used −36 dbu for one instance and +36 dbu for the other, and both were accepted. There is no measured basis for restricting moves to a single direction.

## Move magnitudes

Accepted move deltas observed across the two trials: 36, 64, and 136 dbu (absolute value, x-axis). Trial:i04.ug.whole_design.00 confirms that a 36 dbu move magnitude is sufficient to resolve violations without introducing new V1.S.* or V1.W.1 errors in at least one repair context.

## Polygon end-cap extensions (resize_end)

Resize_end operations are not universally required when moving instances. Trial:i04.ug.whole_design.00 achieved gated_in status with zero resize_end operations. Trial:i03.ug.whole_design.00 required 16 resize_end operations (x-axis high end, 84–192 dbu) paired with its 20 instance moves. Whether resize_end is needed depends on the enclosure deficit introduced by the specific move magnitude and the positions of the affected M1/M2 polygon ends relative to the shifted V1 instances.

## Enclosure rules and resize magnitudes

V1.M1.EN.1 requires M1 to enclose V1 by at least 5 nm on one axis and 2 nm on the opposite axis (projection). V1.M2.EN.2 requires M2 to enclose V1 by 5 nm on both opposite sides, or 5 nm and 0 nm (flush). V1.AUX.1 requires V1 to remain inside both M1 and M2. When instance moves create an enclosure deficit, M1/M2 polygon ends must be extended; trial:i03.ug.whole_design.00 used resize_end magnitudes of 84–192 dbu on the x high end to cover varied deficits across 16 polygons. Trial:i04.ug.whole_design.00 moved instances by only ±36 dbu and required no resize_end, consistent with those smaller shifts not exceeding the existing enclosure margin.

V1.M2.AUX.2 requires V1 width perpendicular to M2 length to match M2 width exactly. The resize_end operations in trial:i03.ug.whole_design.00 targeted the x-axis high end only, preserving the V1-to-M2 width match along the perpendicular axis; V1.M2.AUX.2 was not triggered in either accepted trial.

## Spacing rules

V1.S.1 encodes three minimum spacing scenarios: 18 nm on the same M2 track, 27 nm between parallel tracks that are not aligned, and 18 nm between parallel tracks that are aligned. V1.S.2 sets a 23 nm minimum corner-to-corner (euclidean) spacing between two V1 instances that both carry a 5 nm M2 end-cap. V1.S.3 sets 30 nm minimum corner-to-corner spacing when neither instance has a 5 nm end-cap. V1.S.4 sets 27 nm minimum corner-to-corner spacing for a mixed pair (one with, one without a 5 nm end-cap). In both accepted trials, no new V1.S.* violations were introduced: trial:i03.ug.whole_design.00 used moves of 64 and 136 dbu across 20 instances; trial:i04.ug.whole_design.00 used ±36 dbu across 2 instances. The diverging-direction moves in trial:i04.ug.whole_design.00 (one instance moving −x, one moving +x) increased inter-instance spacing rather than reducing it, which is consistent with no new spacing violations.

## Width rule

V1.W.1 sets a minimum V1 width of 18 nm along the M2 length direction. No width-shrinking operations appear in either accepted trial. All polygon operations in trial:i03.ug.whole_design.00 were resize_end extensions on the x high end; trial:i04.ug.whole_design.00 had no polygon operations at all. Both results are consistent with V1.W.1 remaining clean when only instance moves and end-extensions are applied.

## Orthogonality

The NONORTHOGONAL block applies to V1 as part of all_drawing. All instance moves in both accepted trials were along axis-aligned [x, 0] vectors. All polygon operations in trial:i03.ug.whole_design.00 were axis-aligned resize_end operations on the x high end. No non-orthogonal edges were introduced in either trial, and both were accepted without a GEOMETRY.NONORTHOGONAL violation.

## Operation counts and connectivity

Trial:i03.ug.whole_design.00 required 36 total operations and trial:i04.ug.whole_design.00 required 2 total operations; both achieved conn_preserved=true and gated_in. Connectivity preservation is not contingent on a large operation count. The assemble_drops in trial:i04.ug.whole_design.00 (three ops on V4/M4 layers, reason cu_pool:applied) were not applied to V1 and did not affect the V1-layer result.