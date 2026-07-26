**M6.AUX.2 — Centerline snap to horizontal routing track grid**

M6.AUX.2 fires when a minimum-width M6 polygon's y-centerline does not satisfy `(cl - 64) % 256 == 0` in dbu. Correction requires moving the polygon along y by the residual offset that lands the centerline on the nearest allowed track position. Observed repair deltas of −64, −32, −16, +16, +32, +64 dbu — all multiples of 16 dbu (half the 32 nm M6.AUX.1 grid step) — are sufficient to resolve AUX.2 violations without introducing new violations; the repair was accepted with n_new_in_crop = 0 and n_new_out_of_crop = 0 (trial:i01.ug.whole_design.00).

**Instance co-movement is required when snapping M6 for AUX.2**

When an M6 polygon is snapped for AUX.2, every instance whose geometry spans that polygon (carrying M5 or V5 layers) must be moved by the identical y-delta in the same operation. In trial:i01.ug.whole_design.00, six M6 polygons and eighteen instances (three instance groups per unique delta, touching M5, M6, and V5) were co-moved with matching deltas; conn_preserved was true and the fix was gated in. Omitting the instance co-move would leave V5 or M5 connectivity broken.

**Batch repair within a single gated operation**

Multiple M6 polygons with distinct snap deltas may be corrected in one batch operation. Trial:i01.ug.whole_design.00 applied six distinct per-polygon y-moves (n_ops = 24 total, including instance moves) in a single accepted repair; no inter-polygon spacing or enclosure violations were induced, confirming that correcting several AUX.2 violations simultaneously is safe provided each polygon's delta is computed independently from its own centerline residual.

**Layer interaction scope for AUX.2 snap**

AUX.2 snap operations must treat M5, M6, and V5 as a coupled set. Trial:i01.ug.whole_design.00 lists touched_layers = ["M5", "M6", "V5"], confirming that a y-snap on M6 propagates into both the via layer immediately below (V5) and the metal layer below that (M5) through instance placement. Repairs scoped to M6 alone are insufficient and will break connectivity.