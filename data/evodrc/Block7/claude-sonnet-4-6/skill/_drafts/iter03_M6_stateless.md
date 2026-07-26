## V5-M6 Enclosure Violations: Prefer V5 Reshaping Over M6 Resizing

When repairing V5.M6.EN.2 or V5.M6.AUX.2 violations in VIA_VIA56_2_2_66_58-family cells, reshape the V5 layer rather than the M6 layer. In trial:i01.cu.def:VIA_VIA56_2_2_66_58.02, applying Y-axis moves (±132 dbu) paired with Y-axis resizes (+512 dbu) solely on V5 shapes reduced total violations by 80 (delta_total -80) and was accepted. The M6 layer was listed as a touched layer but received no direct ops in that repair.

## M6 Y-Axis Resizing in Via-Cell Context Causes Net Violation Growth

Do not resize M6 shapes upward on the Y axis inside VIA_VIA56_2_2_66_58-class cells without first verifying the downstream effect on horizontal-spacing and width rules. In trial:i02.cu.def:VIA_VIA56_2_2_66_58.01, a +128 dbu Y-axis resize on the M6 shape (paired with a -96 dbu X-axis resize on M5) produced a net positive delta of +234 violations across three windows (unit:leaf_0022 +3, unit:leaf_0029 +120, unit:leaf_0030 +111) and was rejected as net_positive. The same via cell that accepted a V5-only fix (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02) rejected an M6-resize fix in the immediately following iteration.

## Small M6 Polygon Moves on Both Axes Pass Connectivity Gate

Moving M6 polygons by small increments on X (observed deltas: +32, -16, -64 dbu on polygons p2213, p2212, p2211 respectively) and Y (observed deltas: +32, -16, +64 dbu on polygons p3803, p3802, p3801 respectively) preserves connectivity and passes the unit gate. In trial:i03.ug.leaf_0013.09, all 15 ops across those polygon moves and associated instance moves resulted in conn_preserved=true and zero new violations outside the crop window (n_new_out_of_crop: 0), and the trial was gated_in. Note that 217 new violations appeared inside the crop (n_new_in_crop: 217); gating accepted these because they were bounded within the crop region and connectivity was intact.

## M6 Horizontal-Edge Grid Alignment Is Active in This Design

M6.AUX.1 requires M6 horizontal edges to land on a 32 nm grid. The Y-axis move deltas observed in trial:i03.ug.leaf_0013.09 (+32, -16, +64 dbu) include a -16 dbu step, which is a half-grid move relative to the 32 nm pitch. That trial was gated_in, confirming the resulting positions remained grid-compliant after the move; starting edge positions must already be on-grid for a half-pitch offset move to preserve grid compliance. Ensure any M6 Y-axis move delta is itself a multiple of 32 dbu, or that the pre-move edge coordinate plus the delta lands on a multiple of 32 nm, before applying.

## M6 Minimum-Width Track Constraints Are Context-Sensitive

M6.AUX.2 requires minimum-width M6 tracks to sit on horizontal routing tracks at pitch 256 dbu with offset 64 dbu from the origin (base 128 dbu). In trial:i03.ug.leaf_0013.09, M6 polygons were moved on the Y axis; gating passed, confirming the post-move centrelines of any minimum-width M6 tracks remained on valid routing tracks. When selecting Y-axis move magnitudes for M6 minimum-width polygons, verify the resulting centerline satisfies (cl - 64) % 256 == 0 before committing.