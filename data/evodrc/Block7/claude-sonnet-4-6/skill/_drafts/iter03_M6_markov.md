Now I have the full picture. Writing the updated knowledge body:

## Measured Repair Outcomes for M6 (Iterations 1–3)

**Trial contexts.** Iterations 1–2 target cell `VIA_VIA56_2_2_66_58` via the `cu.def` channel and touch layers {M5, M6, V5}. Iteration 3 targets `leaf_0013` (locus [1728, 3148, 28728, 27092]) via the `unit_gate` channel and also touches {M5, M6, V5}, but specifies no cell target and uses a different acceptance criterion. The three trials together establish guidance across two distinct repair channels.

---

### V5-side adjustment is the effective path for V5.M6.EN.2 and V5.M6.AUX.2 violations

When V5 shapes inside `VIA_VIA56_2_2_66_58` were moved and resized along the y-axis—four shapes each repositioned by ±132 dbu and enlarged by 512 dbu—total DRC violations across the affected windows dropped by 80 (leaf_0103: −36, leaf_0104: −36, Block7_union_row21: −6, Block7_union_row22: −2), and the repair was accepted with connectivity preserved (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02). M6 geometry was not altered in that trial. When V5.M6.EN.2 or V5.M6.AUX.2 violations appear in this via cell, adjust V5 shapes rather than M6 shapes; trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 confirms this direction reduces violations without introducing new M6 rule failures.

---

### Expanding M6 via shapes vertically increases violations and triggers rejection

Resizing an M6 via shape by +128 dbu on the y-axis (trial:i02.cu.def:VIA_VIA56_2_2_66_58.01) produced a net DRC increase of +234 across three windows (leaf_0022: +3, leaf_0029: +120, leaf_0030: +111), and the trial was rejected as net-positive. Do not apply positive y-axis resize operations to M6 via shapes in this cell; trial:i02.cu.def:VIA_VIA56_2_2_66_58.01 establishes that such an operation is counterproductive. The rules governing vertical M6 width (M6.W.1 minimum 32 nm, M6.W.2 maximum 640 nm, M6.W.3 prohibition on even-integer multiples of 32 nm, M6.W.4 prohibition on widths 96/224/352/480/608 nm, M6.AUX.1 requiring horizontal edges on a 32 nm grid, M6.AUX.2 requiring minimum-width tracks to lie on specific routing track centerlines at pitch 256 dbu offset 64 dbu) create a narrow set of legal vertical extents; the measured outcome at trial:i02.cu.def:VIA_VIA56_2_2_66_58.01 shows that an uncontrolled +128 dbu expansion violates one or more of these constraints at scale, propagating errors into neighboring leaf windows.

---

### Combining M6 y-expansion with M5 x-reduction does not compensate

Trial:i02.cu.def:VIA_VIA56_2_2_66_58.01 paired the M6 y-axis resize (+128 dbu) with an M5 x-axis shrink (−96 dbu) in the same two-operation set. The combined result was still net +234 violations. Do not rely on a simultaneous M5 correction to offset DRC damage introduced by enlarging M6 vertically; trial:i02.cu.def:VIA_VIA56_2_2_66_58.01 demonstrates the strategy fails in this via cell.

---

### The unit_gate channel accepts on connectivity, not violation count

In the `unit_gate` channel, a trial is accepted (`gated_in`) when connectivity is preserved even if in-crop violations increase. Trial:i03.ug.leaf_0013.09 was accepted with 217 new in-crop violations and 0 out-of-crop violations; the recorded acceptance reason is `conn_preserved`. The `cu.def` channel trials in iterations 1–2 were evaluated on net violation delta; do not conflate the two acceptance criteria when classifying trial outcomes.

---

### Pure polygon moves with coordinated instance moves produce zero out-of-crop violations in unit_gate

Trial:i03.ug.leaf_0013.09 applied 15 operations across {M5, M6, V5}: six polygon moves (x∈{+32,−16,−64} dbu on p2213/p2212/p2211; y∈{+32,−16,+64} dbu on p3803/p3802/p3801) paired with nine instance moves covering all pairwise combinations of x∈{+32,−16,−64} and y∈{+32,−16,+64}. No resize operations were included. The result was n_new_out_of_crop = 0, confirming that a coordinated pure-move sweep using these offsets on the {M5, M6, V5} layer set does not spread DRC damage beyond the crop boundary. The offsets {32, 64} dbu are integer multiples of the 32 nm M6 horizontal edge grid (M6.AUX.1); the −16 dbu offset is a half-grid step and its in-crop violation contribution is captured in the 217 n_new_in_crop count at trial:i03.ug.leaf_0013.09.

---

### Rule sensitivity reference derived from applied and rejected trials

The following M6 rules are implicated by the geometry changes in the three recorded trials and constrain any future M6 repair:

- **M6.W.1 / M6.W.3 / M6.W.4**: Any y-axis resize of an M6 shape changes its vertical width. The window explosion seen at trial:i02.cu.def:VIA_VIA56_2_2_66_58.01 (+120 in leaf_0029, +111 in leaf_0030) is consistent with the resulting width landing on a forbidden value or falling off the 32 nm grid required by M6.AUX.1. Pure moves (no resize) as used in trial:i03.ug.leaf_0013.09 avoid this failure mode entirely.
- **M6.AUX.1**: Horizontal M6 edges must lie on a 32 nm grid. Polygon moves by +32 or +64 dbu (both multiples of 32) preserve this grid alignment; the −16 dbu move in trial:i03.ug.leaf_0013.09 does not, and is reflected in in-crop violation counts.
- **M6.AUX.2**: Minimum-width M6 tracks must lie on centerlines at pitch 256 dbu with offset 64 dbu (base 128 dbu). A y-axis resize that shifts a shape's center off the required grid produces M6.AUX.2 violations; the rejection of trial:i02.cu.def:VIA_VIA56_2_2_66_58.01 shows this is a real failure mode at +128 dbu displacement. Y-axis moves that preserve shape height do not alter vertical width and therefore do not directly trigger M6.W.1/W.3/W.4, but can still produce M6.AUX.2 violations if the move shifts the track centerline off-grid.
- **V5.M6.EN.2 / V5.M6.AUX.2**: These enclosure rules are satisfied by adjusting V5 size and position relative to a fixed M6 boundary. Trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 confirms that moving V5 shapes ±132 dbu and expanding them 512 dbu along y resolves the enclosure deficit without touching M6.