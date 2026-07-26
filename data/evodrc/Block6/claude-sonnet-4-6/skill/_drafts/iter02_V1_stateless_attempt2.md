## Operational Scope

All twelve trials in the measured history use the `unit_gate` channel. Every `move_instance` delta_dbu has zero Y component — lateral (X-axis) adjustment is the sole instance-level motion used to repair V1-related violations (trial:i01.ug.Block6_union_row3.00 through trial:i02.ug.leaf_0004.04). Negative-X moves also appear: instance i0074 shifts −36 dbu while i0093 shifts +104 dbu within the same trial (trial:i01.ug.Block6_union_row7.02), showing that counter-directional paired moves are accepted when they increase inter-instance separation.

Every trial is accepted (`decision: gated_in`) with `conn_preserved: true` and zero net DRC-crop-count change (`n_new_in_crop: 0`, `n_new_out_of_crop: 0`).

## M2 Resize Accompanies Instance Move When V1 Enclosure Would Be Broken

V1.M2.EN.2 requires M2 to enclose V1 by at least 5 nm on two opposite sides (5 & 5 nm or 5 & 0 nm). V1.M2.AUX.2 requires V1 to be exactly the same width as M2 along the direction perpendicular to M2 length. When a `move_instance` shifts a V1-carrying instance in X, extend the coincident M2 wire end in the same direction and axis to maintain both constraints. Five of the twelve accepted trials pair a `resize_end` on an M2 polygon with one or more `move_instance` operations (trial:i01.ug.Block6_union_row5.01, trial:i01.ug.Block6_union_row7.02, trial:i01.ug.leaf_0001.04, trial:i01.ug.leaf_0015.06, trial:i02.ug.Block6_union_row4.00). In all five, the `resize_end` axis and end direction match the instance move direction. In four of these five trials the resize delta exceeds the move delta by 20 dbu: trial:i01.ug.Block6_union_row7.02 (+124 vs. +104), trial:i01.ug.leaf_0001.04 (+132 vs. +112), trial:i01.ug.leaf_0015.06 (+48 vs. +28), trial:i02.ug.Block6_union_row4.00 (+132 vs. +112). The remaining trial shows a 56 dbu excess (trial:i01.ug.Block6_union_row5.01: +92 vs. +36). Use a resize delta that is at minimum the move delta plus the V1.M2.EN.2 enclosure margin required to keep V1 inside M2 after the shift.

## Simultaneous Multi-Layer Move Preserves V1.AUX.1 and V1.M1.EN.1

V1.AUX.1 requires V1 to reside inside both M1 and M2. V1.M1.EN.1 requires M1 to enclose V1 by at least 5 nm on one opposite-side pair and at least 2 nm on the other. Move V1-touching instances as complete units that displace M1, M2, and V1 together rather than shifting V1 in isolation. All twelve accepted trials list `touched_layers: ["M1","M2","V1"]` (trial:i01.ug.Block6_union_row3.00 through trial:i02.ug.leaf_0004.04), demonstrating that unit-level moves preserve the M1–V1 and M2–V1 spatial relationships required by both rules.

## Group Move for Spacing Rules

V1.S.1 spacing is evaluated via mask projections that extend the effective V1 footprint using 5 nm M2 end-caps. Move all V1-carrying instances in a unit together in the same direction and magnitude to avoid narrowing intra-unit gaps while resolving inter-unit violations. In trial:i01.ug.Block6_union_row3.00 all three instances shift +72 dbu together; in trial:i01.ug.Block6_union_row5.01 four instances shift +36 dbu together. Trials where instances within the same unit shift by different amounts also succeed when the differential widens rather than narrows the gap: trial:i01.ug.Block6_union_row7.02 shifts i0093 +104 dbu and i0074 −36 dbu, increasing their X separation.

## Move Magnitude Range

Instance move magnitudes that are accepted in this history span 4 dbu to 112 dbu (trial:i02.ug.Block6_union_row7.01 at 4 dbu; trial:i01.ug.leaf_0001.04 and trial:i02.ug.Block6_union_row4.00 at 112 dbu). Small residual moves (4–8 dbu) appear exclusively in iter 2 for instances already repositioned in iter 1, reflecting fine-tuning after a larger initial shift (trial:i02.ug.Block6_union_row7.01 at +4 dbu following the +104 dbu iter-1 shift; trial:i02.ug.Block6_union_row8.02 at +8 dbu following the +28 dbu iter-1 shift).

## Multi-Iteration Residual Correction

Some instances require adjustment in both iteration 1 and iteration 2, with the iter-2 move resolving a residual spacing or enclosure shortfall left after the larger iter-1 shift. Instance i0093 receives +104 dbu in iter 1 (trial:i01.ug.Block6_union_row7.02) and a further +4 dbu in iter 2 (trial:i02.ug.Block6_union_row7.01). Instance i0213 receives +28 dbu in iter 1 (trial:i01.ug.leaf_0015.06) and +8 dbu in iter 2 (trial:i02.ug.Block6_union_row8.02). Instance i0446 receives +36 dbu in iter 1 (trial:i01.ug.Block6_union_row5.01) and +72 dbu in iter 2 (trial:i02.ug.leaf_0004.04). Do not treat a single-iteration fix as final for any unit whose locus recurs in a subsequent iteration; verify residual V1 violations after each accepted move.

## Nonorthogonal Geometry Prohibition

The GEOMETRY.NONORTHOGONAL rule applies to V1. All `move_instance` delta_dbu vectors in the history are axis-aligned with zero Y component; no diagonal or off-axis moves appear (trial:i01.ug.Block6_union_row3.00 through trial:i02.ug.leaf_0004.04). Apply only rectilinear (X-only or Y-only) displacements to V1-bearing instances to avoid generating nonorthogonal V1 edges.