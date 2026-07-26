## Observed repair patterns

Two accepted repairs exist for this layer.

**Trial:i03.ug.whole_design.00** (Block3, unit_gate, whole_design locus, iteration 3) combined 20 instance moves (all in the +x direction, deltas of 64 dbu or 136 dbu) with 16 polygon high-x-end extensions (resize_end, x-axis, high end, values 84/120/156/192 dbu). The touched layers were M1, M2, and V1. The trial was accepted with conn_preserved=true.

**Trial:i04.ug.whole_design.00** (Block3, unit_gate, whole_design locus, iteration 4) used only 2 move_instance operations: instance i0023 moved by delta_dbu [-36, 0] and instance i0041 moved by delta_dbu [36, 0]. No resize_end operations were included. The touched layers were M1, M2, and V1. The trial was accepted with conn_preserved=true (trial:i04.ug.whole_design.00).

## Move direction

Both +x and -x instance moves appear in accepted repairs. Trial:i03.ug.whole_design.00 used exclusively +x moves (64 and 136 dbu). Trial:i04.ug.whole_design.00 used a -36 dbu move on i0023 and a +36 dbu move on i0041, and the combined result was accepted. Neither direction is categorically excluded.

## Move magnitudes

Accepted move deltas include 36 dbu (trial:i04.ug.whole_design.00), 64 dbu, and 136 dbu (trial:i03.ug.whole_design.00). The required magnitude depends on the specific enclosure deficit and spacing violation in the design state; both small (36 dbu) and larger (64/136 dbu) values have been used in accepted trials.

## Resize_end is context-dependent

Polygon end-cap extensions (resize_end on M1/M2 high x end) were required in trial:i03.ug.whole_design.00, where 16 such operations accompanied 20 instance moves, and all three enclosure/containment rules (V1.M1.EN.1, V1.M2.EN.2, V1.AUX.1) were satisfied. In trial:i04.ug.whole_design.00, no resize_end operations were present and the 2-operation repair was accepted without triggering enclosure violations. Do not assume resize_end is always required; the need depends on whether the post-move enclosure margins remain within rule limits.

## Enclosure rules and resize magnitudes

V1.M1.EN.1 requires M1 to enclose V1 by at least 5 nm on one axis and 2 nm on the opposite axis (projection). V1.M2.EN.2 requires M2 to enclose V1 by 5 nm on both opposite sides, or 5 nm and 0 nm (flush). V1.AUX.1 requires V1 to remain inside both M1 and M2. When instances are shifted and enclosure margins are insufficient, M1/M2 polygon ends must be extended; trial:i03.ug.whole_design.00 used resize_end magnitudes ranging from 84 to 192 dbu (x high end) to cover different enclosure deficits across 16 affected polygons, and all three enclosure/containment requirements were satisfied in that accepted result. When moves are small enough that enclosure is maintained without extension, resize_end can be omitted, as demonstrated by trial:i04.ug.whole_design.00.

V1.M2.AUX.2 requires V1 width perpendicular to M2 length to match M2 width exactly. The resize_end operations in trial:i03.ug.whole_design.00 targeted the x-axis high end only; this preserves the V1-to-M2 width match along the perpendicular axis, consistent with V1.M2.AUX.2 not being triggered in that accepted trial.

## Spacing rules

V1.S.1 encodes three minimum spacing scenarios: 18 nm on the same M2 track, 27 nm between parallel tracks that are not aligned, and 18 nm between parallel tracks that are aligned. V1.S.2 sets a 23 nm minimum corner-to-corner (euclidean) spacing between two V1 instances that both carry a 5 nm M2 end-cap. V1.S.3 sets 30 nm minimum corner-to-corner spacing when neither instance has a 5 nm end-cap. V1.S.4 sets 27 nm minimum corner-to-corner spacing for a mixed pair (one with, one without a 5 nm end-cap). In trial:i03.ug.whole_design.00, instance moves of 64 and 136 dbu in +x were sufficient to clear spacing violations across the 36-operation repair without triggering new V1.S.* violations. In trial:i04.ug.whole_design.00, moves of 36 dbu in opposing directions also cleared violations without introducing new ones.

## Width rule

V1.W.1 sets a minimum V1 width of 18 nm along the M2 length direction. No width-shrinking operations appear in trial:i03.ug.whole_design.00 or trial:i04.ug.whole_design.00; all polygon operations in the former were end extensions, and the latter contained no polygon operations at all. Both trials were accepted without a V1.W.1 violation.

## Orthogonality

The NONORTHOGONAL block applies to V1 as part of all_drawing. All polygon operations in trial:i03.ug.whole_design.00 were axis-aligned resize_end operations on the x-axis high end, and all instance moves in both trial:i03.ug.whole_design.00 and trial:i04.ug.whole_design.00 were along [x, 0] vectors. No non-orthogonal edges were introduced, and both trials were accepted without a GEOMETRY.NONORTHOGONAL violation.

## Operation counts and connectivity

Trial:i03.ug.whole_design.00 required 36 total operations (n_ops=36): 20 move_instance and 16 resize_end, with conn_preserved=true. Trial:i04.ug.whole_design.00 used only 2 move_instance operations (n_ops=2) and also achieved conn_preserved=true. Connectivity can be preserved with as few as 2 operations when the moves are correctly paired (trial:i04.ug.whole_design.00). Do not assume that larger operation sets are required for connectivity; the minimal set that resolves the specific violations is sufficient.