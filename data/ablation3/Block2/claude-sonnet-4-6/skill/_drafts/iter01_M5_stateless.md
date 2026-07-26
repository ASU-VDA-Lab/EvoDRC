## Via-Level Repairs Reduce M5-Touching Violations Without Modifying M5 Geometry

In trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, three resize operations on V4 (two shapes, +152 dbu in x) and M4 (one shape, +152 dbu in x) within cell `VIA_VIA45_1_2_58_58` produced a net reduction of 16 DRC violations across the whole design (window `unit:whole_design`: 68 → 52) while leaving M5 shapes unmodified. M5 appears in `touched_layers` for that trial but no M5 `op` entries were issued, confirming that the violation count improvement attributed to the M5-touching rules (V4.M5.EN.2, V4.M5.AUX.2) was achieved entirely through via and lower-metal adjustments.

## V4-M5 Enclosure and Width-Match Rules Are the Primary M5-Count Contributors in the V4M5_fix Group

The repair group `V4M5_fix` (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01) targets violations arising at the V4/M5 interface. The two rules in scope are:

- **V4.M5.EN.2**: V4 inside M5 must be enclosed by M5 by at least 11 nm on two opposite sides. Failure occurs when V4 sits too close to a horizontal M5 edge (`m5.sized(-11.nm, 0)`) or vertical M5 edge (`m5.sized(0, -11.nm)`).
- **V4.M5.AUX.2**: V4 must share exactly the same width as the M5 wire in the direction perpendicular to M5 length. Failure occurs when V4 edges do not coincide with M5 edges on at least two sides.

Resizing both V4 shapes by +152 dbu in x within the via cell (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01) resolved multiple instances of these rules simultaneously while preserving connectivity (`conn_preserved: true`).

## X-Axis Via Resizing Is the Confirmed Effective Operation for V4.M5.EN.2 / V4.M5.AUX.2

The sole confirmed repair operation type for M5-related violations at iteration 1 is `resize_via_shape` applied along the `x` axis to V4 shapes (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01). A resize step of +152 dbu in x on each of two V4 shapes, paired with a matching +152 dbu in x on the corresponding M4 shape, achieved the reduction. Do not apply `resize_via_shape` on the `y` axis or to M5 shapes directly when targeting V4.M5.EN.2 or V4.M5.AUX.2; the measured repair modified only V4 and M4 (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01).

## M5 Width and Spacing Rules Carry No Repair Operations at Iteration 1

No operations against M5 geometry were recorded in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01. Rules M5.W.1 (min horizontal width 24 nm), M5.W.2 (max horizontal width 480 nm), M5.W.3 (forbidden even-multiple widths: 48, 96, … 480 nm), M5.W.4 (forbidden even-track-spanning widths: 72, 168, 264, 360, 456 nm), M5.W.5 (min vertical width 44 nm), M5.S.1 (min horizontal spacing 24 nm), M5.S.2 (min vertical spacing 40 nm), M5.S.3/S.4 (tip-to-tip 40 nm), M5.S.5 (min parallel run length 44 nm), M5.AUX.1 (vertical edges on 24 nm grid), M5.AUX.2 (min-width track centerline pitch 192 dbu, offset 48 dbu), M5.AUX.3 (no bends), M5.AUX.4 (wide polygon outside edge must not touch routing track edge), and V5.M5.EN.1 (V5 enclosed by M5 by 11 nm on two opposite sides) have no repair-operation data from the measured history. No claims about fix strategies for those rules are warranted from the available record.