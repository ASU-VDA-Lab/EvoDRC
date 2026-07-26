## Repair Strategies and Observations for V2

### Via Resize Operations

Resizing a V2-touching via cell along the y-axis does not reliably reduce V2 DRC violations. In trial:i02.cu.def:VIA_VIA23_1_3_36_36.00, a resize_via_shape operation on the M3 shape of cell `VIA_VIA23_1_3_36_36` by −40 dbu along y produced a delta_total of 0 across both affected leaf windows (leaf_0014 and leaf_0015 each held at 175 and 113 violations respectively), and the operation was rejected as net-positive. Do not apply y-axis shrink resizes to M3 shapes in via cells as a primary V2 repair action; measured results show no violation reduction.

### Instance Move Operations

Moving an instance that touches V2, M2, and M3 simultaneously can pass the connectivity gate without introducing new violations. In trial:i04.ug.leaf_0002.01, moving instance i0452 by −36 dbu in x (delta_dbu: [−36, 0]) within unit leaf_0002 was gated in with conn_preserved=true and zero new violations entering or leaving the crop window. Use lateral (x-axis) instance moves as a candidate repair when connectivity can be preserved; avoid y-axis moves or resize operations on the via shape itself, as trial:i02.cu.def:VIA_VIA23_1_3_36_36.00 shows those yield no improvement.

### Rule Interaction Notes

V2.AUX.1 and V2.M3.AUX.2 require V2 to remain inside both M2 and M3 and to match M3 width exactly in the direction perpendicular to M3 length. Both measured trials touched M2, M3, and V2 simultaneously, confirming that any geometric perturbation to a via cell or enclosing instance must keep V2 fully contained and width-matched. The gated-in result in trial:i04.ug.leaf_0002.01 and the zero-delta result in trial:i02.cu.def:VIA_VIA23_1_3_36_36.00 are both consistent with these containment constraints being respected (conn_preserved=true in both cases), but neither trial demonstrated an actual violation count reduction.

### Coverage Gaps

Only two trials exist in the measured history for V2 at iteration 4. No successful repair (delta_total < 0) has been recorded. No operations targeting V2.W.1 (minimum width 18 nm), V2.S.1/S.2/S.3/S.4 (spacing rules), V2.M2.EN.1 (M2 enclosure), or V2.M3.EN.2 (M3 enclosure) have been measured with a positive outcome. Do not assert repair recipes for those rules beyond what the two trials above establish.