The new record is already provided inline. Analyzing now.

**Key observations from trial:i03.ug.leaf_0002.01:**
1. 20 instance y-moves only (offsets ±48, ±96 dbu) — no M3 resize_end operations at all
2. M3 appears in `touched_layers` for enclosure evaluation, not reshaping
3. n_new_in_crop=35 accepted; conn_preserved=true, n_new_out_of_crop=0 → gated_in
4. ±48 and ±96 dbu are multiples of 24 dbu, extending the observed y-offset range
5. Contradicts the prescriptive claim that y-moves must be paired with M3 resize_end — this trial refutes that as a universal requirement

---

## V2–M3 Enclosure Violations (V2.M3.EN.2, V2.M3.AUX.2)

Expanding V2 shapes laterally within their M3 landing pad — using paired x-direction move and resize operations — clears V2.M3.EN.2 and V2.M3.AUX.2 violations without introducing out-of-crop leakage. In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, five operations on cell VIA_VIA23_1_3_36_36 (two x-axis moves and three x-axis resizes of V2 shapes) reduced total violations by 78 across windows leaf_0019 (−42) and leaf_0020 (−36) while preserving connectivity. The move+resize pairing — shifting one edge inward while expanding the opposing edge — repositions the via body to satisfy the 5 nm two-opposite-sides enclosure requirement of V2.M3.EN.2 without violating the width-match constraint of V2.M3.AUX.2.

Apply move+resize pairs to V2 shapes in x and keep M3 stationary; the touched-layer record {M2, M3, V2} in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 confirms M3 was read for enclosure evaluation but not reshaped. Letting V2 geometry adapt to a fixed M3 landing pad is the pattern the cu_pool channel uses for this violation class.

## V3–M3 Enclosure Violations (V3.M3.EN.1)

Instance moves in y, at multiples of 24 dbu, satisfy V3.M3.EN.1 when combined with conn_preserved=true and n_new_out_of_crop=0. The observed y-offset magnitudes span 16 dbu (x-only, trial:i02.ug.leaf_0003.03), 24 dbu and 72 dbu (trial:i02.ug.leaf_0010.06), and 48 dbu and 96 dbu (trial:i03.ug.leaf_0002.01); all were accepted with gated_in.

M3 reshape is not universally required alongside y-direction instance moves. Trial:i03.ug.leaf_0002.01 applied 20 y-only instance moves (offsets ±48 and ±96 dbu across 20 instances) with no M3 resize_end operations; M3 appeared only in touched_layers for enclosure evaluation, not as a reshaped layer, and the repair was gated_in with n_new_in_crop=35 and n_new_out_of_crop=0. M3 reshape is needed when moving instances forces an M3 polygon end to lose its V3.M3.EN.1 margin on the receding side; when the existing M3 body retains adequate enclosure margin after the move, omit M3 edits (trial:i02.ug.leaf_0010.06 required M3 resize_end; trial:i03.ug.leaf_0002.01 did not).

For smaller enclosure deficits, a single x-direction instance move suffices without M3 reshaping. Trial:i02.ug.leaf_0003.03 moved instance i0358 by −16 dbu in x, touching M3, M4, and V3, with n_new_in_crop=2 and n_new_out_of_crop=0 (gated_in, conn_preserved). Use instance x-moves for small alignment corrections; apply y-moves at multiples of 24 dbu for larger redistributions, adding M3 resize_end only when required to maintain enclosure on the displaced edge.

## Safe M3 Resize Magnitudes

M3 resize_end operations at y-axis offsets of 24 and 72 dbu (both high-end and low-end expansions and contractions) did not trigger M3.W.1 (minimum width), M3.S.1–M3.S.6 (spacing), or M3.A.1 (minimum area) violations in the contexts observed; the repair was accepted with gated_in status (trial:i02.ug.leaf_0010.06). No measured record establishes safety of M3 resize_end magnitudes outside the 24–72 dbu range observed in this history.

## Gating Criteria and In-Crop Violation Counts

Do not reject a unit_gate proposal solely because n_new_in_crop is large. The gate accepted n_new_in_crop values of 2 (trial:i02.ug.leaf_0003.03), 26 (trial:i02.ug.leaf_0010.06), and 35 (trial:i03.ug.leaf_0002.01) because in all cases conn_preserved=true and n_new_out_of_crop=0. The binding gate criteria are: connectivity preserved AND no violation escaping the crop boundary. New within-crop violations introduced by the repair batch do not block acceptance under these conditions.

## Channel-Specific Operation Patterns

**cu_pool:** Issue move+resize pairs against V2 shapes in x to close V2.M3.EN.2 enclosure gaps from both opposite sides simultaneously. A single batch of 5 ops on one via cell (moves at ±144 dbu x, resizes at +264–288 dbu x) achieved −78 total violations in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00. M3 need not be touched when V2 reshaping alone resolves the enclosure deficit.

**unit_gate:** Move instances in y at multiples of 24 dbu; the range 48 dbu and 96 dbu (trial:i03.ug.leaf_0002.01) and 24 dbu and 72 dbu (trial:i02.ug.leaf_0010.06) are both confirmed safe. Add M3 resize_end operations on the polygon ends that track displaced via connections only when the existing M3 body would otherwise lose V3.M3.EN.1 margin on the receding side (trial:i02.ug.leaf_0010.06 required this; trial:i03.ug.leaf_0002.01 with 20 y-moves passed without any M3 edits). For x-only corrections of ≤16 dbu, instance moves alone without M3 edits pass the gate (trial:i02.ug.leaf_0003.03). All confirmed unit_gate M3 repairs have touched V3 alongside M3, confirming V3.M3.EN.1 as the primary driver for unit_gate M3 involvement through iter 3.