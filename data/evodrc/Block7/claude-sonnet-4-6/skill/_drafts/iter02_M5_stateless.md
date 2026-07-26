## M5 Repair Behaviour — Iteration 2 Knowledge

### M5 Horizontal (x-axis) Resize in Via-Repair Contexts

**Shrinking M5 in x is effective when paired with a coordinated V4 reshape.** In trial:i01.cu.def:VIA_VIA45_1_2_58_58.00 (decision: applied, delta_total -156), the winning repair combined four V4 shape operations—a symmetric move/expand sequence (move -116 dbu, resize +232 dbu per cut shape, two shapes)—with a single M5 x-axis shrink of -152 dbu on shape_index 0. This five-operation bundle reduced violations across two windows (leaf_0103: 407→326, leaf_0104: 385→310). The M5 shrink alone did not drive the fix; it was the final adjustment needed after V4 was widened to maintain V4.M5.AUX.2 compliance (V4 must exactly match M5 width perpendicular to M5 length) and V4.M5.EN.2 compliance (11 nm enclosure on two opposite sides).

**Do not expand M5 in x for a VIA_VIA45 target after a coordinated V4+M5-shrink has already been applied.** In trial:i02.cu.def:VIA_VIA45_1_2_58_58.00 (decision: rejected_net_positive, delta_total +75), a single +56 dbu M5 x-resize increased violations in leaf_0029 (335→374) and leaf_0030 (382→418). Expanding the M5 horizontal extent re-opens spacing and width violations that the iter-1 repair closed.

**Do not shrink M5 in x for a VIA_VIA56 target when pairing with M6 y-expansion.** In trial:i02.cu.def:VIA_VIA56_2_2_66_58.01 (decision: rejected_net_positive, delta_total +234), a -96 dbu M5 x-resize combined with a +128 dbu M6 y-resize drove the largest violation increase observed in this history (leaf_0029: 335→455, leaf_0030: 382→493). M5 x-shrink that does not accompany a matching V4 recenter produces a net-positive outcome when the via's V5 geometry is the primary constraint.

### M5 Vertical (y-axis) Resize — Single-Operation Repairs

**A standalone M5 y-axis shrink on a VIA_VIA45 target matches the violation reduction of the coordinated V4+M5-x bundle but does not win the tournament.** In trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 (decision: lost_tournament, delta_total -156), a single -88 dbu M5 y-resize produced the same net score as trial:i01.cu.def:VIA_VIA45_1_2_58_58.00. The tournament preferred the multi-operation V4+M5-x approach. The M5 y-shrink approach is a valid fallback if the V4 reshape is unavailable, but should be ranked below the coordinated bundle when both are feasible.

### V5 Repair Touching M5 Without Direct M5 Operations

**V5 reshaping can reduce M5-window violations without any M5 op.** In trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 (decision: applied, delta_total -80), all eight operations targeted V5 (symmetric y-axis move/resize pairs across four cut shapes, +512 dbu resize each). M5 appears in touched_layers but received no operations. Window leaf_0103 fell from 407→371 and leaf_0104 from 385→349 as a side-effect. This shows that M5 violations attributable to a VIA_VIA56 target can be cleared by correcting V5 geometry alone—provided V5.M5.EN.1 enclosure (11 nm minimum on two opposite sides) is the root cause.

### Sizing Magnitudes Observed

| Trial | Layer | Axis | Delta (dbu) | Decision |
|---|---|---|---|---|
| i01.cu.def:VIA_VIA45_1_2_58_58.00 | M5 | x | -152 | applied |
| i01.cu.def:VIA_VIA45_1_2_58_58.01 | M5 | y | -88 | lost_tournament |
| i02.cu.def:VIA_VIA45_1_2_58_58.00 | M5 | x | +56 | rejected_net_positive |
| i02.cu.def:VIA_VIA56_2_2_66_58.01 | M5 | x | -96 | rejected_net_positive |

The only M5 operation that produced a net-negative (improving) outcome across both iterations was the -152 dbu x-shrink inside the coordinated V4 bundle (trial:i01.cu.def:VIA_VIA45_1_2_58_58.00). All standalone or improperly paired M5 resizes either lost the tournament or increased violations.

### Grid and Width Constraints That Bound Feasible M5 Moves

Every M5 x-axis edge must land on a 24 nm grid (M5.AUX.1). Minimum-width single-track M5 shapes must be centered on routing tracks spaced at 192 dbu with a 48 dbu offset from origin (M5.AUX.2). The -152 dbu shrink in trial:i01.cu.def:VIA_VIA45_1_2_58_58.00 and the -96 dbu shrink in trial:i02.cu.def:VIA_VIA56_2_2_66_58.01 must both have landed their resulting edges on multiples of 24 nm; neither trial cited an M5.AUX.1 or M5.AUX.2 violation as part of its outcome, confirming those deltas were grid-compatible. When computing candidate M5 x-deltas, constrain to multiples of 24 nm to avoid introducing M5.AUX.1 errors.

M5 horizontal width must stay in [24 nm, 480 nm] (M5.W.1 / M5.W.2), must not equal an even integer multiple of 24 nm (M5.W.3 / M5.W.4), and must not produce a configuration where M5 bends (M5.AUX.3). No violation of these width rules was introduced by the applied operations in this history, but they bound the safe range for any future M5 resize candidate.