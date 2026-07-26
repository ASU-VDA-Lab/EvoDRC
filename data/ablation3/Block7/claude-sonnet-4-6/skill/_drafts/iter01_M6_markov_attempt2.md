**M6.AUX.2 — Horizontal routing-track snap**

Rule M6.AUX.2 requires minimum-width M6 tracks (isolated from wide M6 via a ±17 nm erosion/dilation) to have their centerlines on a grid with pitch 256 dbu and offset 64 dbu, subject to a base alignment of 128 dbu. The repair group `m6_snap` corrects off-grid centerline violations by translating M6 polygons along the y-axis to the nearest valid track position. Trial trial:i01.ug.whole_design.00 demonstrates that multiple M6 polygons carrying distinct snap deltas are corrected in a single batch operation: six polygons (p3801–p3806) received y-deltas of −64, −32, −16, +16, +32, and −64 dbu respectively within one accepted trial (trial:i01.ug).

**Coupled-layer movement**

M6.AUX.2 snap operations treat M5, M6, and V5 as a coupled set. In trial trial:i01.ug.whole_design.00 the `touched_layers` field records all three layers (M5, M6, V5), and each polygon move is paired with instance moves carrying the same delta, propagating the y-correction across all layers simultaneously. Eighteen instance moves accompanied six polygon moves in that trial (trial:i01.ug). Connectivity was preserved (`conn_preserved: true`) and the trial was accepted (`gated_in`), confirming that moving the full coupled set is both necessary and sufficient for a valid repair.

**Observed valid snap-delta magnitudes**

The repair deltas applied in trial trial:i01.ug.whole_design.00 are ±16, ±32, and ±64 dbu along the y-axis. All are integer multiples of 16 dbu and consistent with snapping to the 256 dbu pitch grid. No x-axis moves appeared in this trial; M6.AUX.2 violations are corrected exclusively on the y-axis (trial:i01.ug).