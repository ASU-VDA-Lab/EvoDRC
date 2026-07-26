## Repair History Summary

One trial has been recorded for M6 at iteration 1. No M6 violation count improvement was achieved.

## What the Single Trial Established

The only recorded operation targeted cell `VIA_VIA56_2_2_66_58`, shrinking the M5 enclosure shape along the x-axis by 96 dbu. The trial touched layers M5, M6, and V5 but produced zero reduction in total violations (244 before, 244 after) and was rejected with decision `rejected_net_positive` (trial:i01.cu.def:VIA_VIA56_2_2_66_58.01).

Do not attempt x-axis M5 resize operations on `VIA_VIA56_2_2_66_58`-class cells as a strategy for reducing M6 violations; the measured outcome shows no benefit to the M6 violation count (trial:i01.cu.def:VIA_VIA56_2_2_66_58.01, delta_total=0).

## Rule-Grounded Constraints (Unexercised by Trials)

The following constraints are derived directly from the DRC rules and have not yet been exercised by any recorded trial. No prescriptive repair guidance can be cited from measurement for these rules; they are listed as context for future repair attempts.

**Width rules (M6.W.1 – M6.W.5):**
- Minimum vertical (y-axis) width: 32 nm.
- Maximum vertical width: 640 nm (M6.W.2 uses a 320 nm shrink/grow test).
- Vertical widths that are even integer multiples of 32 nm (64, 128, 192, 256, 320, 384, 448, 512, 576, 640 nm) are forbidden by M6.W.3.
- Vertical widths of 96, 224, 352, 480, or 608 nm are forbidden by M6.W.4.
- Minimum horizontal (x-axis) width: 44 nm.

**Spacing rules (M6.S.1 – M6.S.5):**
- Minimum vertical spacing between M6 polygons: 32 nm (and no overlap, per the 1 dbu catch-all).
- Minimum horizontal spacing between M6 polygons: 40 nm.
- Tip-to-tip spacing on adjacent tracks without shared parallel run length: 40 nm (M6.S.3).
- Tip-to-tip spacing on adjacent tracks with shared parallel run length: 40 nm (M6.S.4).
- Minimum parallel run length on adjacent tracks: 44 nm (M6.S.5).

**Via enclosure rules (V5.M6.EN.2, V6.M6.EN.1):**
- M6 must enclose V5 by at least 11 nm on two opposite sides (one x-direction pair and one y-direction pair, tested independently by `m6.sized(-11.nm, 0)` and `m6.sized(0, -11.nm)`).
- M6 must enclose V6 by at least 11 nm on at least two opposite sides (same test).

**Via width match rule (V5.M6.AUX.2):**
- V5 must be exactly the same width as M6 in the direction perpendicular to the M6 length; any V5 not fully coinciding with M6 edges on two sides triggers this rule.

**Grid and track rules (M6.AUX.1, M6.AUX.2, M6.AUX.4):**
- All M6 horizontal edges must sit on a 32 nm vertical grid (M6.AUX.1; tested via `ongrid(1.dbu, 32.nm)`).
- Minimum-width M6 tracks (those not surviving a 17 nm y-shrink) must have their centerline at positions satisfying `(cl - 64) % 256 == 0` in database units, i.e., on the 256 dbu horizontal routing pitch with a 64 dbu offset (M6.AUX.2).
- Horizontal edges of wide M6 polygons (surviving a 17 nm y-shrink) may not land on a routing track edge occupied by a separate minimum-width M6 track (M6.AUX.4).

**Bend prohibition (M6.AUX.3):**
- M6 polygons must be strictly rectilinear; any corner angle between 0° and 90° (exclusive) triggers M6.AUX.3. M6 may not bend.

**Non-orthogonal prohibition (M6.GEOMETRY.NONORTHOGONAL):**
- All M6 edges must be at exactly 0°, 90°, 180°, or 270°. Any edge with an angle in the range 1–89°, 91–179°, −179–−91°, or −89–−1° triggers this rule.

## Guidance for Future Repairs

Because only one trial exists and it achieved no improvement, no repair strategy for M6 can yet be grounded in measured outcomes. The rule set indicates that M6 violations most commonly arise from: via enclosure deficits (V5.M6.EN.2, V5.M6.AUX.2, V6.M6.EN.1), spacing violations between adjacent M6 wires (M6.S.1 – M6.S.5), and track alignment or grid errors (M6.AUX.1, M6.AUX.2). Future trials should target these categories and generate citations before repair heuristics are recorded here.