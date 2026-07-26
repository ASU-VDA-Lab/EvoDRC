## Observed M2 Violation Classes and Their Triggers

**M2.S.2 (tip-to-side, min 25 nm)** was introduced as 1 new in-crop violation by trial:i02.ug.leaf_0004.03. That trial applied a combined [36, -48] dbu displacement to instance i0015 together with lateral [36, 0] moves on i0459 and i0437. No M2.S.2 violation appeared in any trial where all instance displacements had zero or positive y-components.

**M2.S.4 (narrow tip-to-tip, both edges <24 nm, min 31 nm)** appeared as 1 new in-crop violation in trial:i02.ug.leaf_0010.07. That trial applied [0, -40] dbu moves to both i0015 and i0471, alongside x-only moves of [4, 0] on i0361 and i0239 and [-28, 0] on i0112. The M2.S.4 violation co-appeared with M2.S.7 in the same trial; the x-only ops in the same trial had not produced M2.S.4 violations in earlier trials.

**M2.S.7 (18 nm tip-to-tip co-located with side spacing ≤32 nm, parallel run <35 nm)** appeared as 1 new in-crop violation in trial:i02.ug.leaf_0010.07, the same trial as M2.S.4, driven by the same [0, -40] y-displacements on i0015 and i0471. No M2.S.7 violation appeared in any trial without a negative y-displacement on an M2-touching instance.

No new in-crop violations for M2.W.1, M2.A.1, M2.S.1, M2.S.3, M2.S.5, M2.S.6, M2.S.8, V1.M2.EN.2, V1.M2.AUX.2, or V2.M2.EN.1 appear in any trial across both iterations.

## Negative Y-Displacement as a Consistent Risk Factor for M2 Tip Spacing

Every trial introducing a new M2 spacing violation applied a negative y-displacement to an M2-touching instance: [36, -48] in trial:i02.ug.leaf_0004.03 (M2.S.2) and [0, -40] in trial:i02.ug.leaf_0010.07 (M2.S.4, M2.S.7). No trial using only x-axis instance moves — including large-magnitude moves such as [96, 0] in trial:i02.ug.Block6_union_row7.00, [104, 0] in trial:i02.ug.leaf_0001.01 and trial:i02.ug.leaf_0003.02, and [-40, 0] in trial:i01.ug.Block6_union_row7.03 — produced any new M2 violation. Positive y-axis moves ([0, 48] on i0471 in trial:i01.ug.Block6_union_row3.00 and on i0015 in trial:i01.ug.Block6_union_row5.02) also produced zero new M2 violations. Avoid applying negative y-displacement to instances whose M2 geometries carry tip edges approaching adjacent M2 features; use x-only or positive-y displacements instead.

## Successful Operation Patterns for M2

The following operation types produced zero new M2 violations across all 14 trials in which they appeared:

- **X-axis instance moves** at all tested magnitudes, including [4, 0] (trial:i01.ug.leaf_0001.05, trial:i01.ug.Block6_union_row4.01, trial:i02.ug.leaf_0008.05), [12, 0] (trial:i01.ug.Block6_union_row7.03), [28, 0] (trial:i01.ug.leaf_0015.07, trial:i02.ug.leaf_0008.05), [36, 0] (trial:i01.ug.Block6_union_row4.01, trial:i01.ug.leaf_0011.06, trial:i01.ug.leaf_0018.08, trial:i02.ug.Block6_union_row7.00), [96, 0] (trial:i02.ug.Block6_union_row7.00), and [104, 0] (trial:i02.ug.leaf_0001.01, trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0005.04); and negative x-axis moves [-40, 0] (trial:i01.ug.Block6_union_row7.03) and [-28, 0] (trial:i02.ug.leaf_0010.07).
- **Positive y-axis instance moves** ([0, 48]) on M2-touching instances (trial:i01.ug.Block6_union_row3.00, trial:i01.ug.Block6_union_row5.02).
- **Polygon resize_end on the x-axis**, growing the low end by +60 (trial:i01.ug.Block6_union_row7.03), the high end by +36 (trial:i01.ug.Block6_union_row8.04), +48 (trial:i01.ug.leaf_0015.07), +56 (trial:i02.ug.Block6_union_row7.00), +128 (trial:i02.ug.leaf_0003.02), and +28 (trial:i02.ug.leaf_0008.05).

## Instance Conflict Drops and M2 Repair Interference

Instance i0015 was claimed concurrently by unit leaf_0004 and unit leaf_0010 during iter 2. In trial:i02.ug.leaf_0004.03, the leaf_0010 op ([0, -40] on i0015) was dropped as an external conflict and the leaf_0004 op ([36, -48] on i0015) executed — introducing 1 new M2.S.2 violation. In trial:i02.ug.leaf_0010.07, the leaf_0004 op for i0015 was dropped instead and the leaf_0010 ops ([0, -40] on i0015 and i0471) executed — introducing M2.S.4 and M2.S.7 violations. When the same M2-touching instance is operated on by multiple units in the same iteration, the surviving op after conflict resolution determines the M2 spacing outcome; the dropped op's y-displacement characteristic is not necessarily safer than the surviving op's.

## Via Shape Resize on M2-Adjacent Layers

trial:i02.cu.def:VIA_VIA23_1_3_36_76.00 resized the V2 via cell VIA_VIA23_1_3_36_36 by -40 dbu in y, touching M2, M3, and V2. The DRC count in both evaluated windows (leaf_0009 at 110, leaf_0010 at 138) was unchanged after the resize. The trial was rejected as rejected_net_positive (delta: 0). Shrinking a V2 via shape in y by 40 dbu produced no reduction in M2-region or total DRC count under these conditions.

## Gating Behavior Under New M2 Violations

All trials with conn_preserved:true were gated_in regardless of new in-crop M2 violations. trial:i02.ug.leaf_0004.03 (1 new M2.S.2) and trial:i02.ug.leaf_0010.07 (1 new M2.S.4, 1 new M2.S.7, 75 additional non-M2 violations) both received decision:gated_in. In both cases n_new_out_of_crop was 0. The gating criterion accepts new M2 in-crop violations when connectivity is preserved and no out-of-crop violations are introduced.