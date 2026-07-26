The rejection is precise: prescriptions must not conflate the two distinct acceptance criteria — **net violation reduction** (accepted because DRC count fell) versus **connectivity preservation** (`conn_preserved=true`, accepted even when violations rise). Trial i01 was accepted on violation-reduction grounds; trial i03 was accepted on connectivity grounds despite +217 new in-crop violations. I must cite each trial only for the criterion that actually drove its outcome.

---

## Measured Repair Outcomes for M6 (Iterations 1–3)

**Trial context summary.** Three trials are on record for M6.

- trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 — accepted; net violation reduction (−80 total across four windows); cell VIA_VIA56_2_2_66_58, V5-axis geometry change, M6 untouched.
- trial:i02.cu.def:VIA_VIA56_2_2_66_58.01 — rejected; net violation increase (+234 total across three windows); same cell, M6 y-axis resize + M5 x-axis shrink.
- trial:i03.ug.leaf_0013.09 — accepted; gated_in on `conn_preserved=true`; 217 new violations recorded in-crop, 0 out-of-crop; unit_gate channel, leaf_0013, 15 ops (polygon moves on M5/M6/V5 axes plus nine instance moves), `target: null`.

These three trials supply all empirical grounding below. No other ids exist in the layer history.

---

### The two acceptance criteria are distinct and must not be conflated

The harness applies two separate gates: (1) a trial is accepted because it produces a net reduction in DRC violations; (2) a trial is accepted because `conn_preserved=true` regardless of whether the violation count rises or falls. Trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 was accepted under criterion (1): violations fell by 80 and connectivity was preserved. Trial:i03.ug.leaf_0013.09 was accepted under criterion (2) alone: `conn_preserved=true` and `reason="conn_preserved"` appear in the decision record, while `n_new_in_crop=217` confirms a substantial violation increase. Do not treat the two gated-in outcomes as equivalent evidence of geometric correctness. A trial accepted on connectivity grounds carries no implication that the resulting geometry is DRC-clean.

---

### V5-side adjustment is the effective path for V5.M6.EN.2 and V5.M6.AUX.2 violations (violation-reduction accepted)

When V5 shapes inside `VIA_VIA56_2_2_66_58` were moved and resized along the y-axis—four shapes each repositioned by ±132 dbu and enlarged by 512 dbu—total DRC violations dropped by 80 (leaf_0103: −36, leaf_0104: −36, Block7_union_row21: −6, Block7_union_row22: −2) and the trial was accepted under the net-violation-reduction criterion with connectivity preserved (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02). M6 geometry was not altered in that trial. When V5.M6.EN.2 or V5.M6.AUX.2 violations appear in this via cell, adjust V5 shapes rather than M6 shapes; trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 confirms this direction reduces violations without introducing new M6 rule failures.

---

### Expanding M6 via shapes vertically increases violations and triggers rejection

Resizing an M6 via shape by +128 dbu on the y-axis (trial:i02.cu.def:VIA_VIA56_2_2_66_58.01) produced a net DRC increase of +234 across three windows (leaf_0022: +3, leaf_0029: +120, leaf_0030: +111), and the trial was rejected as net-positive. Do not apply positive y-axis resize operations to M6 via shapes in this cell; trial:i02.cu.def:VIA_VIA56_2_2_66_58.01 establishes that such an operation is counterproductive. The rules governing vertical M6 width (M6.W.1 minimum 32 nm, M6.W.2 maximum 640 nm, M6.W.3 prohibition on even-integer multiples of 32 nm, M6.W.4 prohibition on widths 96/224/352/480/608 nm, M6.AUX.1 requiring horizontal edges on a 32 nm grid, M6.AUX.2 requiring minimum-width tracks to lie on specific routing track centerlines at pitch 256 dbu offset 64 dbu) create a narrow set of legal vertical extents; the measured outcome at trial:i02.cu.def:VIA_VIA56_2_2_66_58.01 shows that an uncontrolled +128 dbu expansion violates one or more of these constraints at scale, propagating errors into neighboring leaf windows.

---

### Combining M6 y-expansion with M5 x-reduction does not compensate

Trial:i02.cu.def:VIA_VIA56_2_2_66_58.01 paired the M6 y-axis resize (+128 dbu) with an M5 x-axis shrink (−96 dbu) in the same two-operation set. The combined result was still net +234 violations. Do not rely on a simultaneous M5 correction to offset DRC damage introduced by enlarging M6 vertically; trial:i02.cu.def:VIA_VIA56_2_2_66_58.01 demonstrates the strategy fails in this via cell.

---

### Polygon moves plus instance moves in the unit_gate channel are accepted on connectivity grounds, not on DRC reduction

Trial:i03.ug.leaf_0013.09 applied 15 operations in leaf_0013 (unit_gate channel): x-axis moves on three M6-region polygons (p2213 +32 dbu, p2212 −16 dbu, p2211 −64 dbu), y-axis moves on three V5-region polygons (p3803 +32 dbu, p3802 −16 dbu, p3801 +64 dbu), and nine instance moves spanning both axes. The trial was gated_in with `reason="conn_preserved"` and `n_new_in_crop=217`, `n_new_out_of_crop=0`. Acceptance was driven by the connectivity criterion, not by violation reduction. Do not interpret trial:i03.ug.leaf_0013.09 as evidence that this operation set improves DRC compliance; the 217 new in-crop violations confirm the geometry is not DRC-clean after these moves.

---

### Rule sensitivity reference derived from applied and rejected trials

The following M6 rules are implicated by the geometry changes in the recorded trials and constrain any future M6 repair:

- **M6.W.1 / M6.W.3 / M6.W.4**: Any y-axis resize of an M6 shape changes its vertical width. The window explosion seen at trial:i02.cu.def:VIA_VIA56_2_2_66_58.01 (+120 in leaf_0029, +111 in leaf_0030) is consistent with the resulting width landing on a forbidden value or falling off the 32 nm grid required by M6.AUX.1.
- **M6.AUX.2**: Minimum-width M6 tracks must lie on centerlines at pitch 256 dbu with offset 64 dbu (base 128 dbu). A y-axis resize that shifts a shape's center off the required grid produces M6.AUX.2 violations; the rejection of trial:i02.cu.def:VIA_VIA56_2_2_66_58.01 shows this is a real failure mode at +128 dbu displacement.
- **V5.M6.EN.2 / V5.M6.AUX.2**: These enclosure rules are satisfied by adjusting V5 size and position relative to a fixed M6 boundary. Trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 confirms that moving V5 shapes ±132 dbu and expanding them 512 dbu along y resolves the enclosure deficit under the violation-reduction criterion without touching M6.